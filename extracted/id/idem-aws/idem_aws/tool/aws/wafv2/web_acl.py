from collections import OrderedDict
from typing import Any
from typing import Dict


async def update(
    hub,
    ctx,
    name: str,
    raw_resource: Dict[str, Any],
    resource_parameters: Dict[str, None],
    scope: str,
    resource_id: str,
    lock_token: str,
):
    """

    Args:
        hub:
        ctx:
        name: Name of resource going to update.
        raw_resource: Old state of resource or existing resource details.
        resource_parameters: Parameters from sls file
        scope: Specifies whether this is for an Amazon CloudFront distribution or for a regional application.
        resource_id: The unique identifier for the web ACL.
        lock_token: A token used for optimistic locking.

    Returns:
        {"result": True|False, "comment": ("A tuple",), "ret": {}}
    """

    parameters = OrderedDict(
        {
            "Name": "name",
            "DefaultAction": "default_action",
            "VisibilityConfig": "visibility_config",
            "Description": "description",
            "Rules": "rules",
            "CustomResponseBodies": "custom_response_bodies",
            "CaptchaConfig": "captcha_config",
        }
    )
    parameters_to_update = {}
    result = dict(comment=[], result=True, ret=None)
    resource_parameters.pop("Tags", None)

    for key, value in resource_parameters.items():
        if value is None or value == raw_resource[key]:
            continue
        parameters_to_update[key] = resource_parameters[key]

    if parameters_to_update:
        if not ctx.get("test", False):
            update_ret = await hub.exec.boto3.client.wafv2.update_web_acl(
                ctx,
                Scope=scope,
                Id=resource_id,
                LockToken=lock_token,
                **resource_parameters,
            )
            if not update_ret["result"]:
                result["comment"] = update_ret["comment"]
                result["result"] = False
                return result
            result["comment"] += [f"Updated '{name}'"]

        result["ret"] = {}
        for parameter_raw, parameter_present in parameters.items():
            if parameter_raw in parameters_to_update:
                result["ret"][parameter_present] = parameters_to_update[parameter_raw]

    return result
