from facebook_business.adobjects.adsinsights import AdsInsights
from meta_ads.client import get_ad_account
from datetime import date, timedelta


DEFAULT_FIELDS = [
    AdsInsights.Field.campaign_id,
    AdsInsights.Field.campaign_name,
    AdsInsights.Field.adset_id,
    AdsInsights.Field.adset_name,
    AdsInsights.Field.ad_id,
    AdsInsights.Field.ad_name,
    AdsInsights.Field.impressions,
    AdsInsights.Field.clicks,
    AdsInsights.Field.spend,
    AdsInsights.Field.reach,
    AdsInsights.Field.cpm,
    AdsInsights.Field.cpc,
    AdsInsights.Field.ctr,
    AdsInsights.Field.actions,
    AdsInsights.Field.action_values,
    AdsInsights.Field.roas,
    AdsInsights.Field.date_start,
    AdsInsights.Field.date_stop,
]


def get_account_insights(
    date_from: str | None = None,
    date_to: str | None = None,
    level: str = "campaign",
) -> list[dict]:
    account = get_ad_account()

    if not date_from:
        date_from = (date.today() - timedelta(days=7)).isoformat()
    if not date_to:
        date_to = date.today().isoformat()

    params = {
        "level": level,  # campaign | adset | ad
        "time_range": {"since": date_from, "until": date_to},
        "time_increment": 1,
    }

    insights = account.get_insights(fields=DEFAULT_FIELDS, params=params)
    return [i.export_all_data() for i in insights]


def get_roas_summary(date_from: str | None = None, date_to: str | None = None) -> dict:
    rows = get_account_insights(date_from, date_to, level="account")
    if not rows:
        return {"spend": 0, "revenue": 0, "roas": 0, "period": f"{date_from} → {date_to}"}

    row = rows[0]
    spend = float(row.get("spend", 0))
    revenue = 0.0
    for av in row.get("action_values", []):
        if av.get("action_type") == "purchase":
            revenue += float(av.get("value", 0))

    roas = round(revenue / spend, 2) if spend > 0 else 0
    return {
        "spend": spend,
        "revenue": revenue,
        "roas": roas,
        "period": f"{row.get('date_start')} → {row.get('date_stop')}",
    }
