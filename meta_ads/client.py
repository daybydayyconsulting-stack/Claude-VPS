from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from config import get_settings
from functools import lru_cache


@lru_cache
def init_api() -> FacebookAdsApi:
    s = get_settings()
    return FacebookAdsApi.init(
        app_id=s.meta_app_id,
        app_secret=s.meta_app_secret,
        access_token=s.meta_access_token,
    )


def get_ad_account() -> AdAccount:
    init_api()
    s = get_settings()
    return AdAccount(s.meta_ad_account_id)
