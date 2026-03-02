from typing import Tuple, Dict

from stigg.generated import FetchEntitlementsQuery, GetPaywallInput, FetchEntitlementQuery, GetActiveSubscriptionsInput


def build_get_entitlement_data(edge_url: str, query: FetchEntitlementQuery) -> Tuple[str, Dict]:
  url = f"{edge_url}/v1/c/{query.customer_id}/entitlements.json"
  params = {}
  if query.resource_id is not None:
    params["resourceId"] = query.resource_id

  if query.feature_id is not None:
    params["featureId"] = query.feature_id

  if query.options is not None and query.options.requested_usage is not None:
    params['requestedUsage'] = query.options.requested_usage

  return url, params


def build_get_entitlements_data(edge_url: str, query: FetchEntitlementsQuery) -> Tuple[str, Dict]:
    url = f"{edge_url}/v1/c/{query.customer_id}/entitlements.json"
    params = {}
    if query.resource_id is not None:
        params["resourceId"] = query.resource_id

    return url, params


def build_get_entitlements_state_data(edge_url: str, query: FetchEntitlementsQuery) -> Tuple[str, Dict]:
    url = f"{edge_url}/v1/c/{query.customer_id}/entitlements-state.json"
    params = {}
    if query.resource_id is not None:
        params["resourceId"] = query.resource_id

    return url, params


def build_get_paywall_data(edge_url: str, _input: GetPaywallInput) -> Tuple[str, Dict]:
    if _input.product_id is not None:
        url = f"{edge_url}/v1/p/{_input.product_id}/paywall.json"
    else:
        url = f"{edge_url}/v1/paywall.json"

    params = {}
    if _input.billing_country_code is not None:
        params["billingCountryCode"] = _input.billing_country_code

    if _input.fetch_all_countries_prices is not None:
        params["fetchAllCountriesPrices"] = _input.fetch_all_countries_prices

    if _input.include_hidden_plans is not None:
        params["includeHiddenPlans"] = _input.include_hidden_plans

    return url, params

def build_get_subscriptions_data(edge_url: str, _input: GetActiveSubscriptionsInput) -> Tuple[str, Dict]:
    url = f"{edge_url}/v1/c/{_input.customer_id}/subscriptions.json"

    params = {}
    if _input.resource_id is not None:
        params["resourceId"] = _input.resource_id

    if _input.resource_ids is not None:
        params["resourceIds"] = _input.resource_ids

    return url, params
