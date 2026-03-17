#!/bin/bash
# Pull latest code and restart service
set -euo pipefail

REPO_DIR="/opt/claude-vps"
VENV_DIR="$REPO_DIR/.venv"

echo "=== Deploying latest code ==="
git -C "$REPO_DIR" pull --ff-only
"$VENV_DIR/bin/pip" install -r "$REPO_DIR/requirements.txt" -q
systemctl restart claude-vps
echo "[✓] Service restarted"
systemctl status claude-vps --no-pager
