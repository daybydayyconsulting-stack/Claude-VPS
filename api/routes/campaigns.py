from fastapi import APIRouter, Depends, Query
from typing import Optional
from api.auth import require_api_key
from meta_ads import campaigns

router = APIRouter(prefix="/campaigns", tags=["Campaigns"])


@router.get("/")
def list_campaigns(
    status: Optional[str] = Query(None, description="ACTIVE | PAUSED | ARCHIVED"),
    _: str = Depends(require_api_key),
):
    return campaigns.list_campaigns(status)


@router.get("/{campaign_id}")
def get_campaign(campaign_id: str, _: str = Depends(require_api_key)):
    return campaigns.get_campaign(campaign_id)


@router.patch("/{campaign_id}/status")
def update_status(
    campaign_id: str,
    status: str = Query(..., description="ACTIVE | PAUSED | ARCHIVED"),
    _: str = Depends(require_api_key),
):
    return campaigns.update_campaign_status(campaign_id, status)


@router.get("/adsets/")
def list_adsets(
    campaign_id: Optional[str] = Query(None),
    _: str = Depends(require_api_key),
):
    return campaigns.list_adsets(campaign_id)


@router.patch("/adsets/{adset_id}/budget")
def update_adset_budget(
    adset_id: str,
    daily_budget_cents: int = Query(..., description="Daily budget in cents (EUR/USD)"),
    _: str = Depends(require_api_key),
):
    return campaigns.update_adset_budget(adset_id, daily_budget_cents)


@router.get("/ads/")
def list_ads(
    adset_id: Optional[str] = Query(None),
    _: str = Depends(require_api_key),
):
    return campaigns.list_ads(adset_id)
