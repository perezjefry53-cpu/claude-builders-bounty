# 🪵 CHANGELOG Generator

Automatically generate a structured `CHANGELOG.md` from your project's git history using conventional commits.

## How it works

1. Scans git history since the last tag
2. Categorizes commits using conventional commit prefixes:
   - `feat:` → ✨ **Added**
   - `fix:` → 🐛 **Fixed**
   - `refactor:` / `perf:` / `docs:` / `chore:` → ♻️ **Changed**
   - `revert:` → ⏪ **Removed**
3. Groups changes by version tag
4. Outputs a clean `CHANGELOG.md`

## Usage (3 steps)

```bash
# 1. Run in your project
python3 changelog.py

# 2. Or use the shell wrapper
bash changelog.sh

# 3. See a demo
bash changelog.sh --sample
```

Options:
- `--repo DIR` — path to git repo (default: current dir)
- `--output FILE` — output file (default: CHANGELOG.md)
- `--sample` — generate from a demo repo

## Example output

```markdown
# Changelog

## [Unreleased]
### Added
  - ✨ add file upload API

## v1.0.0
### Fixed
  - 🐛 resolve race condition
### Changed
  - ♻️ refactor database layer
```

## Requirements

- Python 3.6+
- Git 2.x
- Conventional commit messages (optional, uncategorized commits default to "Added")

## In Claude Code

Use `/generate-changelog` in any project with `bash changelog.sh`.
