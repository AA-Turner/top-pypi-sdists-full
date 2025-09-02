from typing import Any
from typing import Dict
from typing import List


async def is_resource_updated(
    hub,
    before: Dict[str, Any],
    role_arn: str,
    recording_group: Dict,
):
    if role_arn != before.get("role_arn"):
        return True

    if recording_group != before.get("recording_group"):
        return True

    return False


async def is_account_agg_source_list_equal(
    hub, new_list: List[Dict], old_list: List[Dict]
):
    new_list.sort()
    old_list.sort()
    return new_list == old_list


async def is_configuration_aggregator_updated(
    hub,
    before: Dict[str, Any],
    account_aggregation_sources: List[Dict],
    organization_aggregation_source: Dict,
):
    # Flag to check if resource is updated or not
    if (
        account_aggregation_sources is not None
        and before.get("account_aggregation_sources") is not None
    ):
        if not await hub.tool.aws.config.config_utils.is_account_agg_source_list_equal(
            account_aggregation_sources, before.get("account_aggregation_sources")
        ):
            return True
    if (
        account_aggregation_sources is None
        and before.get("account_aggregation_sources") is not None
    ) or (
        account_aggregation_sources is not None
        and before.get("account_aggregation_sources") is None
    ):
        return True
    return not hub.tool.aws.state_comparison_utils.compare_dicts(
        organization_aggregation_source, before.get("organization_aggregation_source")
    )
