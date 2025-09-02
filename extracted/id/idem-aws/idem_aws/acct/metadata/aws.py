from typing import Any
from typing import Dict

from dict_tools.data import NamespaceDict


async def gather(hub, profile: Dict[str, Any]):
    identity_ctx = NamespaceDict(acct=profile)
    acct_details = await hub.exec.aws.sts.caller_identity.get(identity_ctx)
    if acct_details.result:
        return {
            "attribute_value": acct_details["ret"]["Account"],
            "attribute_key": "Account",
            "provider": "AWS",
            "region_name": hub.tool.boto3.region.get(identity_ctx),
        }
    return {}
