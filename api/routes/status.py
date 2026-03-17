from fastapi import APIRouter, Depends
from api.auth import require_api_key
from meta_ads.client import get_ad_account
from config import get_settings

router = APIRouter(prefix="/status", tags=["Status"])


@router.get("/health")
def health():
    """Public health check — no auth required."""
    return {"status": "ok", "service": "claude-vps"}


@router.get("/meta")
def meta_connection_check(_: str = Depends(require_api_key)):
    """Verify Meta Ads API credentials are valid."""
    try:
        account = get_ad_account()
        data = account.api_get(fields=["id", "name", "account_status", "currency"])
        return {
            "connected": True,
            "account_id": data.get("id"),
            "account_name": data.get("name"),
            "currency": data.get("currency"),
            "account_status": data.get("account_status"),
        }
    except Exception as e:
        return {"connected": False, "error": str(e)}
