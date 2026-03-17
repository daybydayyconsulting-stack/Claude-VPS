#!/bin/bash
# DaybyDay Claude VPS — Setup Script
# Run as root on a fresh Ubuntu 24.04 server
set -euo pipefail

REPO_DIR="/opt/claude-vps"
SERVICE_USER="claude-vps"
PYTHON_BIN="python3"
VENV_DIR="$REPO_DIR/.venv"

echo "=== Claude VPS Setup ==="

# 1. System dependencies
apt-get update -qq
apt-get install -y python3 python3-pip python3-venv git curl

# 2. Create service user
if ! id "$SERVICE_USER" &>/dev/null; then
    useradd -r -s /bin/false -d "$REPO_DIR" "$SERVICE_USER"
    echo "[✓] Service user '$SERVICE_USER' created"
fi

# 3. Clone or update repo
if [ -d "$REPO_DIR/.git" ]; then
    git -C "$REPO_DIR" pull --ff-only
    echo "[✓] Repo updated"
else
    git clone https://github.com/daybydayyconsulting-stack/Claude-VPS.git "$REPO_DIR"
    echo "[✓] Repo cloned to $REPO_DIR"
fi

# 4. Python virtual environment
$PYTHON_BIN -m venv "$VENV_DIR"
"$VENV_DIR/bin/pip" install --upgrade pip -q
"$VENV_DIR/bin/pip" install -r "$REPO_DIR/requirements.txt" -q
echo "[✓] Python dependencies installed"

# 5. Environment file
if [ ! -f "$REPO_DIR/.env" ]; then
    cp "$REPO_DIR/.env.example" "$REPO_DIR/.env"
    echo ""
    echo "[!] .env file created. Edit it now:"
    echo "    nano $REPO_DIR/.env"
    echo ""
fi

# 6. Permissions
chown -R "$SERVICE_USER:$SERVICE_USER" "$REPO_DIR"
chmod 600 "$REPO_DIR/.env"

# 7. Install systemd service
cp "$REPO_DIR/systemd/claude-vps.service" /etc/systemd/system/
systemctl daemon-reload
systemctl enable claude-vps
echo "[✓] Systemd service installed and enabled"

echo ""
echo "=== Setup complete ==="
echo "Next steps:"
echo "  1. Edit credentials:  nano $REPO_DIR/.env"
echo "  2. Start service:     systemctl start claude-vps"
echo "  3. Check status:      systemctl status claude-vps"
echo "  4. View logs:         journalctl -u claude-vps -f"
echo "  5. Test API:          curl http://localhost:8000/status/health"
