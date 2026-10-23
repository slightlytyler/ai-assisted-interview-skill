#!/usr/bin/env bash
# Create a fresh rehearsal copy of the playground repo as its own git repo.
# Usage: ./new-playground.sh [dest]   (default: ~/interview-playground)
set -euo pipefail

src="$(cd "$(dirname "$0")" && pwd)/playground"
dest="${1:-$HOME/interview-playground}"

if [ -e "$dest" ]; then
  echo "error: $dest already exists; remove it or pass another path" >&2
  exit 1
fi

cp -R "$src" "$dest"
git -C "$dest" init -q
git -C "$dest" add -A
git -C "$dest" commit -q -m "Starter repo"
echo "ready: cd $dest && claude, then run /interview"
