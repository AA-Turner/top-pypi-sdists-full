#!/usr/bin/env bash
# Install the post-commit hook that auto-syncs the source tree's
# drydock/*.py to site-packages on every commit. CLAUDE.md learning
# #4: import paths lie — source tree is shadowed by site-packages
# from any project cwd, so fixes are invisible to the running TUI
# until auto_release fires (every 6 hours). This hook closes that
# gap.
#
# Run once after cloning the repo:
#   bash scripts/install_post_commit_hook.sh
set -e

REPO=/data3/drydock
HOOK="$REPO/.git/hooks/post-commit"

cat > "$HOOK" <<'HOOK_BODY'
#!/usr/bin/env bash
# Auto-sync source to site-packages on every commit.
# Pause flag: touch /data3/drydock/.pause_sync_to_site_packages
set -e

if [ -f /data3/drydock/.pause_sync_to_site_packages ]; then
  exit 0
fi

SITE=/home/bobef/miniforge3/envs/drydock/lib/python3.14/site-packages/drydock
SRC=/data3/drydock/drydock

if [ ! -d "$SITE" ] || [ ! -d "$SRC" ]; then
  exit 0
fi

# Full mirror (minus __pycache__). DO NOT use --include/--exclude='*'
# selective filters: drydock ships .tcss/.json/.txt assets that aren't
# in any simple include list, and a selective rsync DELETES them from
# site-packages, breaking the TUI on the next launch.
rsync -a --exclude='__pycache__' "$SRC/" "$SITE/" >/dev/null 2>&1 || true

find "$SITE" -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
HOOK_BODY

chmod +x "$HOOK"
echo "Installed $HOOK"
