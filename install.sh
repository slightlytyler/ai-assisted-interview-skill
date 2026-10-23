#!/usr/bin/env bash
# Symlink the interview skill into the global Claude Code skills folder,
# so edits in this repo take effect without reinstalling.
set -euo pipefail

src="$(cd "$(dirname "$0")" && pwd)/skill/interview"
dest="$HOME/.claude/skills/interview"

mkdir -p "$(dirname "$dest")"

if [ -L "$dest" ]; then
  rm "$dest"
elif [ -e "$dest" ]; then
  echo "error: $dest exists and is not a symlink; move it aside first" >&2
  exit 1
fi

ln -s "$src" "$dest"
echo "linked $dest -> $src"
