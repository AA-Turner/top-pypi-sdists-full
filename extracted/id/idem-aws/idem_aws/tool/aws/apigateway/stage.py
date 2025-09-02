import copy
from collections import OrderedDict
from typing import Any
from typing import Dict
from typing import List


def convert_raw_stage_to_present(
    hub,
    raw_resource: Dict[str, Any],
    resource_id: str,
) -> Dict[str, Any]:
    resource_parameters = OrderedDict(
        {
            "stageName": "name",
            "deploymentId": "deployment_id",
            "cacheClusterEnabled": "cache_cluster_enabled",
            "cacheClusterSize": "cache_cluster_size",
            "variables": "variables",
            "description": "description",
            "canarySettings": "canary_settings",
            "tracingEnabled": "tracing_enabled",
            "documentationVersion": "documentation_version",
            "tags": "tags",
        }
    )

    resource_translated = {
        "resource_id": resource_id,
        "rest_api_id": resource_id.split("-")[0],
        "name": resource_id.split("-")[1],
    }

    for parameter_raw, parameter_present in resource_parameters.items():
        if raw_resource.get(parameter_raw) is not None:
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)

    return resource_translated


async def update(
    hub,
    ctx,
    old_state: Dict[str, Any],
    updateable_parameters: Dict[str, Any],
):
    r"""

    Updates an API Stage Resource.

    Args:
        old_state(dict):
            Previous state of the resource.

        updateable_parameters(dict):
            Parameters from SLS File.

    Returns:
        {"result": True|False, "comment": A message List, "ret": None|Dict}

    """

    result = dict(comment=[], result=True, ret=None)
    patch_ops = []

    new_state = copy.deepcopy(old_state)
    updated = False
    key_final = ""

    for key, value in updateable_parameters.items():
        if key == "cache_cluster_enabled":
            key_final = "cacheClusterEnabled"
        elif key == "cache_cluster_size":
            key_final = "cacheClusterSize"
        elif key == "deployment_id":
            key_final = "deploymentId"
        elif key == "description":
            key_final = "description"
        elif key == "variables":
            key_final = "variables"
        elif key == "tracing_enabled":
            key_final = "tracingEnabled"

        if value != old_state.get(key):
            patch_ops.append(
                {
                    "op": "replace",
                    "path": f"/{key_final}",
                    "value": str(value)
                    if not isinstance(value, List)
                    else ",".join(value),
                }
            )
            new_state[key] = value
            updated = True
        elif old_state.get(key) is None and value is not None:
            patch_ops.append(
                {
                    "op": "add",
                    "path": f"/{key_final}",
                    "value": str(value)
                    if not isinstance(value, List)
                    else ",".join(value),
                }
            )
            new_state[key] = value
            updated = True

    if ctx.get("test", False):
        if updated:
            result["comment"] = hub.tool.aws.comment_utils.would_update_comment(
                resource_type="aws.apigateway.stage",
                name=old_state["name"],
            )
            result["ret"] = new_state
        else:
            result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
                resource_type="aws.apigateway.stage",
                name=old_state["name"],
            )
        return result

    if updated:
        update_ret = await hub.exec.boto3.client.apigateway.update_stage(
            ctx,
            restApiId=old_state["rest_api_id"],
            stageName=old_state["name"],
            patchOperations=patch_ops,
        )
        if not update_ret["result"]:
            result["result"] = False
            result["comment"] = update_ret["comment"]
            return result
        else:
            result["comment"] = hub.tool.aws.comment_utils.update_comment(
                resource_type="aws.apigateway.stage",
                name=old_state["name"],
            )
            result["ret"] = new_state
    else:
        result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
            resource_type="aws.apigateway.stage", name=old_state["name"]
        )

    return result
