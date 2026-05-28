#!/bin/bash
set -euo pipefail

HOOK_DIR="${HOME}/.claude/hooks"
mkdir -p "$HOOK_DIR"
cp "$(dirname "$0")/pre-tool-use.sh" "${HOOK_DIR}/pre-tool-use"
chmod +x "${HOOK_DIR}/pre-tool-use"
echo "✅ Hook installed to ${HOOK_DIR}/pre-tool-use"
echo "📝 Blocked commands will be logged to ${HOOK_DIR}/blocked.log"
