import copy
from collections import OrderedDict
from typing import Any
from typing import Dict
from typing import List


def convert_raw_method_response_to_present(
    hub,
    raw_resource: Dict[str, Any],
    resource_id: str,
    idem_resource_name: str = None,
) -> Dict[str, Any]:
    resource_parameters = OrderedDict(
        {
            "responseParameters": "response_parameters",
            "responseModels": "response_models",
        }
    )

    resource_translated = {
        "name": idem_resource_name,
        "resource_id": resource_id,
        "rest_api_id": resource_id.split("-")[0],
        "parent_resource_id": resource_id.split("-")[1],
        "http_method": resource_id.split("-")[2],
        "status_code": resource_id.split("-")[3],
    }
    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in raw_resource:
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)

    return resource_translated


async def update(
    hub, ctx, old_state: Dict[str, Any], updatable_resource_parameters: Dict[str, Any]
):
    """

    Updates an API Gateway Method Response

    Args:
        hub:

        ctx:

        old_state(Dict):
            Previous state of the resource.

        updatable_resource_parameters(Dict):
            Parameters from SLS File.

    Returns:
        Dict[str, Any]

    """

    result = dict(comment=[], result=True, ret=None)
    patch_ops = []

    new_state = copy.deepcopy(old_state)
    updated = False

    for key, value in updatable_resource_parameters.items():
        if key == "response_parameters":
            key_final = "responseParameters"
        elif key == "response_models":
            key_final = "responseModels"

        if old_state.get(key) and value is not None and value != old_state.get(key):
            for items_key, items_val in value.items():
                patch_ops.append(
                    {
                        "op": "replace",
                        "path": f"/{key_final}/{items_key}",
                        "value": str(items_val)
                        if not isinstance(value, List)
                        else ",".join(value),
                    }
                )
            updated = True
        elif old_state.get(key) is None and value is not None:
            for items_key, items_val in value.items():
                patch_ops.append(
                    {
                        "op": "add",
                        "path": f"/{key_final}/{items_key}",
                        "value": str(items_val)
                        if not isinstance(value, List)
                        else ",".join(value),
                    }
                )
            new_state[key] = value
            updated = True

    if ctx.get("test", False):
        if updated:
            result["comment"] = hub.tool.aws.comment_utils.would_update_comment(
                resource_type="aws.apigateway.method_response", name=old_state["name"]
            )
            result["ret"] = new_state
        else:
            result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
                resource_type="aws.apigateway.method_response", name=old_state["name"]
            )
        return result

    if updated:
        update_ret = await hub.exec.boto3.client.apigateway.update_method_response(
            ctx,
            restApiId=old_state["rest_api_id"],
            resourceId=old_state["parent_resource_id"],
            httpMethod=old_state["http_method"],
            statusCode=old_state["status_code"],
            patchOperations=patch_ops,
        )
        if not update_ret["result"]:
            result["result"] = False
            result["comment"] = update_ret["comment"]
            return result
        else:
            result["comment"] = hub.tool.aws.comment_utils.update_comment(
                resource_type="aws.apigateway.method_response", name=old_state["name"]
            )
            result["ret"] = new_state
    else:
        result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
            resource_type="aws.apigateway.method_response", name=old_state["name"]
        )

    return result
