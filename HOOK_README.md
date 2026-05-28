# 🛡️ Claude Code Pre-Tool-Use Hook

Blocks destructive shell commands before they execute and logs all attempts.

## Installation

```bash
# One-liner
bash hooks/install.sh

# Or manually:
cp hooks/pre-tool-use.sh ~/.claude/hooks/pre-tool-use
chmod +x ~/.claude/hooks/pre-tool-use
```

## What it blocks

| Pattern | Severity |
|---------|----------|
| `rm -rf /` | 🔴 Fatal |
| `DROP TABLE / DROP DATABASE` | 🔴 Fatal |
| `DELETE FROM ... WHERE 1=1` | 🔴 Fatal |
| `git push --force` | 🔴 Fatal |
| `TRUNCATE TABLE` | 🔴 Fatal |
| `mkfs.*`, `dd if=/dev/zero` | 🔴 Fatal |
| Fork bombs | 🔴 Fatal |
| `rm -rf` (non-root) | 🟡 Warning |
| `ALTER TABLE`, `DROP *` | 🟡 Warning |

## Logs

All blocked/warned commands are logged to `~/.claude/hooks/blocked.log`:

```
[BLOCKED] 2026-05-28T10:30:00Z | cmd: rm -rf /some/dir | project: /home/user/project | pattern: rm -rf
```

## Test

```bash
# This should be blocked:
bash hooks/pre-tool-use.sh "rm -rf /important-data"

# This should pass:
bash hooks/pre-tool-use.sh "ls -la"
```
