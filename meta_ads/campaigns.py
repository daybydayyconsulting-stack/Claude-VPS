from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adset import AdSet
from facebook_business.adobjects.ad import Ad
from meta_ads.client import get_ad_account
from typing import Optional


CAMPAIGN_FIELDS = [
    Campaign.Field.id,
    Campaign.Field.name,
    Campaign.Field.status,
    Campaign.Field.objective,
    Campaign.Field.daily_budget,
    Campaign.Field.lifetime_budget,
    Campaign.Field.start_time,
    Campaign.Field.stop_time,
    Campaign.Field.created_time,
    Campaign.Field.updated_time,
]

ADSET_FIELDS = [
    AdSet.Field.id,
    AdSet.Field.name,
    AdSet.Field.status,
    AdSet.Field.campaign_id,
    AdSet.Field.daily_budget,
    AdSet.Field.bid_amount,
    AdSet.Field.targeting,
    AdSet.Field.start_time,
    AdSet.Field.end_time,
]

AD_FIELDS = [
    Ad.Field.id,
    Ad.Field.name,
    Ad.Field.status,
    Ad.Field.adset_id,
    Ad.Field.campaign_id,
    Ad.Field.creative,
    Ad.Field.created_time,
    Ad.Field.updated_time,
]


def list_campaigns(status: Optional[str] = None) -> list[dict]:
    account = get_ad_account()
    params = {}
    if status:
        params["effective_status"] = [status.upper()]
    campaigns = account.get_campaigns(fields=CAMPAIGN_FIELDS, params=params)
    return [c.export_all_data() for c in campaigns]


def get_campaign(campaign_id: str) -> dict:
    campaign = Campaign(campaign_id)
    campaign.api_get(fields=CAMPAIGN_FIELDS)
    return campaign.export_all_data()


def update_campaign_status(campaign_id: str, status: str) -> dict:
    """status: ACTIVE | PAUSED | ARCHIVED"""
    campaign = Campaign(campaign_id)
    campaign.api_update(params={"status": status.upper()})
    return {"campaign_id": campaign_id, "status": status.upper()}


def list_adsets(campaign_id: Optional[str] = None) -> list[dict]:
    account = get_ad_account()
    params = {}
    if campaign_id:
        params["campaign_id"] = campaign_id
    adsets = account.get_ad_sets(fields=ADSET_FIELDS, params=params)
    return [a.export_all_data() for a in adsets]


def update_adset_budget(adset_id: str, daily_budget_cents: int) -> dict:
    adset = AdSet(adset_id)
    adset.api_update(params={"daily_budget": daily_budget_cents})
    return {"adset_id": adset_id, "daily_budget_cents": daily_budget_cents}


def list_ads(adset_id: Optional[str] = None) -> list[dict]:
    account = get_ad_account()
    params = {}
    if adset_id:
        params["adset_id"] = adset_id
    ads = account.get_ads(fields=AD_FIELDS, params=params)
    return [a.export_all_data() for a in ads]
