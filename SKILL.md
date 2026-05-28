---
name: generate-changelog
description: Generate a structured CHANGELOG.md from a project's git history using conventional commits.
---

# Generate Changelog Skill

Automatically creates a `CHANGELOG.md` from your git history.

## Usage

```bash
# In your project directory:
bash changelog.sh

# Or specify a repo:
bash changelog.sh --repo /path/to/repo

# See demo output:
bash changelog.sh --sample
```

## How it works

1. Fetches all commits since the last git tag
2. Auto-categorizes by conventional commit prefix:
   - `feat:` → ✨ Added
   - `fix:` → 🐛 Fixed
   - `refactor:` → ♻️ Changed
   - `perf:` → ⚡ Performance
   - `docs:` → 📝 Documentation
   - `chore:` → 🔧 Maintenance
3. Groups by version tags (newest first)
4. Outputs a clean, formatted `CHANGELOG.md`

## Requirements

- `bash` 4+
- `git` 2.x
- Conventional commit messages

## Example output

```markdown
# Changelog

## [Unreleased]
- ✨ Add user authentication module
- 🐛 Fix off-by-one error in counter

## v1.0.0
- ✨ Initial release with core features
```

Call with `/generate-changelog` in Claude Code or run `bash changelog.sh` directly.
