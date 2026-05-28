#!/usr/bin/env bash
# =============================================
#  Claude Code Pre-Tool-Use Hook
#  Blocks destructive commands and logs attempts
#  Install: cp this to ~/.claude/hooks/pre-tool-use
# =============================================

set -euo pipefail

BLOCKED_LOG="${HOME}/.claude/hooks/blocked.log"
HOOK_DIR="$(cd "$(dirname "$0")" && pwd)"

# Patterns that should ALWAYS be blocked (fatals)
DESTRUCTIVE_PATTERNS=(
  'rm -rf /'
  'rm -rf --no-preserve-root'
  'DROP TABLE'
  'DROP DATABASE'
  'TRUNCATE TABLE'
  'DELETE FROM [^ ]+ WHERE 1=1'
  'DELETE FROM [^ ]+ WHERE true'
  'DELETE FROM [^ ]+;'
  'DELETE FROM [^ ]+$'
  'UPDATE [^ ]+ SET .+ WHERE 1=1'
  'UPDATE [^ ]+ SET .+ WHERE true'
  'git push --force'
  'git push -f'
  'git push origin \+'
  'format[[:space:]]*[CD]:'
  'mkfs\.'
  'dd if=/dev/zero'
  'dd if=/dev/random'
  'chmod -R 000 /'
  'chown -R .+ /'
  '> /dev/sda'
  ':(){ :|:& };:'  # fork bomb
)

# Warning-only patterns (logged, not blocked)
WARNING_PATTERNS=(
  'rm -rf'
  'git push --force-with-lease'
  'DROP'
  'ALTER TABLE'
  'TRUNCATE'
  'DELETE'
  'UPDATE [^ ]+ SET'
)

# Command being inspected (passed via environment)
COMMAND="${CLAUDE_TOOL_COMMAND:-${*:-}}"
PROJECT_PATH="${CLAUDE_PROJECT_DIR:-${PWD}}"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

log_block() {
  mkdir -p "$(dirname "$BLOCKED_LOG")"
  echo "[BLOCKED] ${TIMESTAMP} | cmd: ${COMMAND} | project: ${PROJECT_PATH} | pattern: ${1}" >> "$BLOCKED_LOG"
}

log_warning() {
  mkdir -p "$(dirname "$BLOCKED_LOG")"
  echo "[WARNING] ${TIMESTAMP} | cmd: ${COMMAND} | project: ${PROJECT_PATH} | pattern: ${1}" >> "$BLOCKED_LOG"
}

# Check destructive patterns
for pattern in "${DESTRUCTIVE_PATTERNS[@]}"; do
  if echo "$COMMAND" | grep -qiE "$pattern" 2>/dev/null; then
    log_block "$pattern"
    cat << 'BLOCKED_MSG'
╔══════════════════════════════════════════════════════╗
║  🚫 BLOCKED: Destructive command detected           ║
╠══════════════════════════════════════════════════════╣
║  This command matches a destructive pattern and     ║
║  has been prevented from executing.                 ║
║                                                      ║
║  Logged to: ~/.claude/hooks/blocked.log             ║
╚══════════════════════════════════════════════════════╝
BLOCKED_MSG
    exit 1
  fi
done

# Check warning patterns
for pattern in "${WARNING_PATTERNS[@]}"; do
  if echo "$COMMAND" | grep -qiE "$pattern" 2>/dev/null; then
    log_warning "$pattern"
    cat << 'WARN_MSG'
╔══════════════════════════════════════════════════════╗
║  ⚠️  WARNING: Potentially destructive pattern       ║
╠══════════════════════════════════════════════════════╣
║  This command uses patterns that could be            ║
║  destructive. Please verify the command intent       ║
║  before confirming.                                  ║
║                                                      ║
║  Logged to: ~/.claude/hooks/blocked.log             ║
╚══════════════════════════════════════════════════════╝
WARN_MSG
    exit 1  # Still block warning patterns by default
  fi
done

exit 0
