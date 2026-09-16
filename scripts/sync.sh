#!/bin/sh
# Sync the GitHub Pages entry point (index.html) with the frontend app.
# Source of truth: frontend/genome_editing.html
# Usage:
#   sh scripts/sync.sh            # copy frontend -> index.html
#   sh scripts/sync.sh --reverse  # copy index.html -> frontend (if edited via Pages preview)
#   sh scripts/sync.sh --check    # exit 1 if out of sync (useful in CI)
set -eu

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FRONTEND="$ROOT/frontend/genome_editing.html"
INDEX="$ROOT/index.html"

usage() {
  echo "Usage: sh scripts/sync.sh [--reverse|--check]" >&2
}

case "${1:-}" in
  "")
    cp "$FRONTEND" "$INDEX"
    echo "Synced: frontend/genome_editing.html -> index.html"
    ;;
  --reverse)
    cp "$INDEX" "$FRONTEND"
    echo "Synced: index.html -> frontend/genome_editing.html"
    ;;
  --check)
    if cmp -s "$FRONTEND" "$INDEX"; then
      echo "In sync."
    else
      echo "Out of sync: index.html differs from frontend/genome_editing.html" >&2
      exit 1
    fi
    ;;
  -h|--help) usage ;;
  *) usage; exit 2 ;;
esac
