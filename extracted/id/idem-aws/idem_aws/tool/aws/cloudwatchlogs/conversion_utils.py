from typing import Any
from typing import Dict

"""
Util functions to convert raw resource state from AWS CloudwatchLog Resource Policy to present input format.
"""


def convert_raw_log_group_resource_policy_to_present(
    hub, ctx, raw_resource: Dict[str, Any], idem_resource_name: str = None
) -> Dict[str, Any]:
    resource_id = raw_resource.get("policyName")
    resource_translated = {
        "name": idem_resource_name,
        "resource_id": resource_id,
        "policy_document": raw_resource.get("policyDocument"),
    }
    return resource_translated
