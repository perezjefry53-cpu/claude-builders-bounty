#!/bin/bash
# Wrapper that calls changelog.py
DIR="$(cd "$(dirname "$0")" && pwd)"
exec python3 "$DIR/changelog.py" "$@"
