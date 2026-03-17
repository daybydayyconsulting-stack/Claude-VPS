from fastapi import APIRouter, Depends, Query
from typing import Optional
from api.auth import require_api_key
from meta_ads import insights

router = APIRouter(prefix="/insights", tags=["Insights"])


@router.get("/")
def get_insights(
    date_from: Optional[str] = Query(None, description="YYYY-MM-DD"),
    date_to: Optional[str] = Query(None, description="YYYY-MM-DD"),
    level: str = Query("campaign", description="campaign | adset | ad | account"),
    _: str = Depends(require_api_key),
):
    return insights.get_account_insights(date_from, date_to, level)


@router.get("/roas")
def get_roas(
    date_from: Optional[str] = Query(None, description="YYYY-MM-DD"),
    date_to: Optional[str] = Query(None, description="YYYY-MM-DD"),
    _: str = Depends(require_api_key),
):
    return insights.get_roas_summary(date_from, date_to)
