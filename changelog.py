#!/usr/bin/env python3
"""Generate structured CHANGELOG.md from git history using conventional commits."""
import subprocess, os, sys, re
from collections import OrderedDict

def git(*args, repo="."):
    try:
        r = subprocess.run(["git"] + list(args), capture_output=True, text=True, cwd=repo, timeout=15)
        return r.stdout.strip() if r.returncode == 0 else ""
    except: return ""

def get_commits(range_spec, repo):
    raw = git("log", range_spec, "--pretty=format:%s", "--no-merges", repo=repo)
    return [l.strip() for l in raw.split("\n") if l.strip()][::-1] if raw else []

def get_tags(repo):
    raw = git("tag", "--sort=version:refname", repo=repo)
    return raw.split("\n") if raw else []

def categorize(msg):
    lc = msg.lower()
    for prefix, cat in [
        ("feat", "Added"), ("feature", "Added"),
        ("fix", "Fixed"), ("bugfix", "Fixed"),
        ("refactor", "Changed"), ("perf", "Changed"),
        ("docs", "Changed"), ("style", "Changed"),
        ("test", "Changed"), ("chore", "Changed"),
        ("ci", "Changed"), ("build", "Changed"),
        ("revert", "Removed")
    ]:
        if lc.startswith(prefix + ":") or lc.startswith(prefix + "("):
            body = msg.split(":", 1)[1].strip() if ":" in msg else msg
            return cat, body
    return "Added", msg  # default

def build_changelog(repo):
    output = "# Changelog\n\nAll notable changes to this project will be documented in this file.\n\n"
    total = 0
    tags = get_tags(repo)
    
    def add_section(title, entries):
        nonlocal output, total
        if not entries: return
        output += f"## {title}\n\n"
        groups = OrderedDict([("Added", []), ("Fixed", []), ("Changed", []), ("Removed", [])])
        for msg in entries:
            cat, body = categorize(msg)
            if cat in groups: groups[cat].append(body)
        for cat, items in groups.items():
            if items:
                output += f"### {cat}\n"
                for item in items:
                    icon = {"Added": "✨", "Fixed": "🐛", "Changed": "♻️", "Removed": "⏪"}.get(cat, "🔧")
                    output += f"  - {icon} {item}\n"
                    total += 1
                output += "\n"
    
    # Unreleased (commits after newest tag)
    if tags:
        latest = tags[-1]
        commits = get_commits(f"HEAD...{latest}", repo)
        if commits: add_section("[Unreleased]", commits)
    
    # Each tag
    for i, tag in enumerate(tags):
        if i == 0:
            commits = get_commits(tag, repo)
        else:
            commits = get_commits(f"{tags[i-1]}...{tag}", repo)
        add_section(tag, commits)
    
    if not tags:
        add_section("[Unreleased]", get_commits("HEAD", repo))
    
    return output.strip() + "\n", total

# Main
if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate CHANGELOG.md from git history")
    parser.add_argument("--repo", default=os.getcwd())
    parser.add_argument("--output", default="CHANGELOG.md")
    parser.add_argument("--sample", action="store_true")
    args = parser.parse_args()
    
    if args.sample:
        import tempfile, shutil
        demo = tempfile.mkdtemp()
        os.chdir(demo)
        subprocess.run(["git", "init", "-b", "main"], capture_output=True)
        subprocess.run(["git", "config", "user.email", "d@d.com"], capture_output=True)
        subprocess.run(["git", "config", "user.name", "Demo"], capture_output=True)
        
        def demo_commit(msg):
            with open("f.txt","a") as f: f.write(msg[:5]+"\n")
            subprocess.run(["git", "add", "."], capture_output=True)
            subprocess.run(["git", "commit", "-m", msg], capture_output=True)
        
        demo_commit("chore: initial project setup")
        subprocess.run(["git", "tag", "v0.1.0"], capture_output=True)
        demo_commit("feat: add user authentication module")
        demo_commit("fix: resolve race condition in session handler")
        demo_commit("docs: add API documentation")
        subprocess.run(["git", "tag", "v0.2.0"], capture_output=True)
        demo_commit("feat: implement file upload API")
        demo_commit("refactor: simplify database queries")
        demo_commit("fix: prevent XSS in user input")
        subprocess.run(["git", "tag", "v0.3.0"], capture_output=True)
        args.repo = demo
    
    changelog, count = build_changelog(args.repo)
    with open(args.output, "w") as f: f.write(changelog)
    print(f"✅ Generated: {args.output}")
    print(f"📊 {count} changes logged\n")
    print("Preview:")
    print("\n".join(changelog.split("\n")[:30]))
    
    if args.sample:
        os.chdir("/tmp/claude-builders-bounty")
        shutil.rmtree(demo, ignore_errors=True)

