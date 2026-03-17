# Claude VPS — Meta Ads Remote Control

DaybyDay agency VPS server for managing Meta Ads campaigns via REST API.

## Architecture

```
Claude VPS (Ubuntu 24.04)
├── FastAPI server (port 8000)         ← remote control API
│   ├── /status/health                 ← public health check
│   ├── /status/meta                   ← verify Meta connection
│   ├── /campaigns/                    ← list/get/pause/activate
│   ├── /campaigns/adsets/             ← manage ad sets + budgets
│   ├── /campaigns/ads/                ← list ads
│   └── /insights/                     ← performance data + ROAS
└── systemd service (auto-restart)
```

## Quick Start

### 1. Server setup (run as root)

```bash
curl -fsSL https://raw.githubusercontent.com/daybydayyconsulting-stack/Claude-VPS/main/scripts/setup.sh | bash
```

### 2. Configure credentials

```bash
nano /opt/claude-vps/.env
```

Fill in your Meta Ads credentials (see `.env.example`).

**Get your Meta credentials:**
- App ID & Secret: developers.facebook.com/apps
- Access Token: Graph API Explorer (developers.facebook.com/tools/explorer)
- Ad Account ID: Business Settings -> Ad Accounts (business.facebook.com/settings/ad-accounts)

**Generate API key:**
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### 3. Start the service

```bash
systemctl start claude-vps
systemctl status claude-vps
```

### 4. Verify connection

```bash
# Health check (no auth)
curl http://localhost:8000/status/health

# Meta Ads connection check
curl -H "X-API-Key: YOUR_API_KEY" http://localhost:8000/status/meta
```

## API Reference

Interactive docs available at: `http://YOUR_SERVER_IP:8000/docs`

All endpoints except `/status/health` require the header:
```
X-API-Key: your_api_secret_key
```

### Key endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/status/health` | Health check |
| GET | `/status/meta` | Verify Meta connection |
| GET | `/campaigns/?status=ACTIVE` | List campaigns |
| PATCH | `/campaigns/{id}/status?status=PAUSED` | Pause/activate campaign |
| GET | `/campaigns/adsets/?campaign_id=...` | List ad sets |
| PATCH | `/campaigns/adsets/{id}/budget?daily_budget_cents=5000` | Update budget (cents) |
| GET | `/insights/?level=campaign&date_from=2026-03-01` | Performance data |
| GET | `/insights/roas?date_from=2026-03-01` | ROAS summary |

## Deploy updates

```bash
/opt/claude-vps/scripts/deploy.sh
```

## Logs

```bash
journalctl -u claude-vps -f
```

## Security

- API protected by `X-API-Key` header
- `.env` file has `chmod 600` (root-only read)
- Service runs as dedicated low-privilege user `claude-vps`
- Systemd `NoNewPrivileges=true` and `PrivateTmp=true`
- Restrict port 8000 to trusted IPs only:

```bash
ufw allow from YOUR_OFFICE_IP to any port 8000
ufw deny 8000
```
