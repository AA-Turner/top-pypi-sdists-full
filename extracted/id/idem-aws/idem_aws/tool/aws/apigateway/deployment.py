"""Exec module for managing Amazon API Gateway Deployments."""
import copy
from collections import OrderedDict
from typing import Any
from typing import Dict
from typing import List


def convert_raw_deployment_to_present(
    hub,
    raw_resource: Dict[str, Any],
    rest_api_id: str,
    resource_id: str,
    idem_resource_name: str = None,
) -> Dict[str, Any]:
    resource_parameters = OrderedDict(
        {
            "description": "description",
        }
    )

    resource_translated = {
        "resource_id": resource_id,
        "rest_api_id": rest_api_id,
    }

    if idem_resource_name:
        resource_translated["name"] = idem_resource_name

    for parameter_raw, parameter_present in resource_parameters.items():
        if raw_resource.get(parameter_raw) is not None:
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)

    return resource_translated


async def update(
    hub,
    ctx,
    old_state: Dict[str, Any],
    updatable_parameters: Dict[str, Any],
):
    """

    Updates an API Deployment Resource. Updating is only supported for replacing descriptions.

    Args:
        old_state(dict):
            Previous state of the resource.

        updatable_parameters(dict):
            Parameters from SLS File.

    Returns:
        {"result": True|False, "comment": A message List, "ret": None|Dict}

    """

    result = dict(comment=[], result=True, ret=None)
    patch_ops = []

    new_state = copy.deepcopy(old_state)
    updated = False

    for key, value in updatable_parameters.items():
        if old_state.get(key) and value is not None and value != old_state.get(key):
            patch_ops.append(
                {
                    "op": "replace",
                    "path": f"/{key}",
                    "value": str(value)
                    if not isinstance(value, List)
                    else ",".join(value),
                }
            )
            updated = True

    if ctx.get("test", False):
        if updated:
            result["comment"] = hub.tool.aws.comment_utils.would_update_comment(
                resource_type="aws.apigateway.deployment",
                name=old_state["name"],
            )
            result["ret"] = new_state
        else:
            result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
                resource_type="aws.apigateway.deployment",
                name=old_state["name"],
            )
        return result

    if updated:
        update_ret = await hub.exec.boto3.client.apigateway.update_deployment(
            ctx,
            restApiId=old_state["rest_api_id"],
            deploymentId=old_state["resource_id"],
            patchOperations=patch_ops,
        )
        if not update_ret["result"]:
            result["result"] = False
            result["comment"] = update_ret["comment"]
            return result
        else:
            result["comment"] = hub.tool.aws.comment_utils.update_comment(
                resource_type="aws.apigateway.deployment",
                name=old_state["name"],
            )
            result["ret"] = new_state
    else:
        result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
            resource_type="aws.apigateway.deployment", name=old_state["name"]
        )

    return result
