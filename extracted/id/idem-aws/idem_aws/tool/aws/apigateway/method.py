import copy
from collections import OrderedDict
from typing import Any
from typing import Dict
from typing import List


def convert_raw_method_to_present(
    hub,
    raw_resource: Any,
    resource_id: str,
    idem_resource_name: str = None,
) -> Dict[str, Any]:
    """Convert AWS API Gateway Method to a common idem present state.

    Args:
        resource_id(str): Idem Resource ID that is generated once the resource is created.

        raw_resource(dict[str, Any]): The AWS response to convert.

        idem_resource_name(str, Optional): The idem name of the resource.

    Returns:
        dict[str, Any]: Common idem present state
    """

    resource_parameters = OrderedDict(
        {
            "httpMethod": "http_method",
            "authorizationType": "authorization_type",
            "apiKeyRequired": "api_key_required",
        }
    )

    resource_translated = {
        "resource_id": resource_id,
        "rest_api_id": resource_id.split("-")[0],
        "parent_resource_id": resource_id.split("-")[1],
    }
    for parameter_raw, parameter_present in resource_parameters.items():
        if idem_resource_name:
            resource_translated["name"] = idem_resource_name
        if raw_resource.get(parameter_raw) is not None:
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)

    return resource_translated


async def update(
    hub,
    ctx,
    old_state: Dict[str, Any],
    update_parameters: Dict[str, Any],
):
    """Updates an API Gateway Method

    Args:
        old_state(dict): Previous state of resource

        update_parameters(dict): Parameters from SLS File

    Returns:
        dict[str, Any]
    """

    result = dict(comment=[], result=True, ret=None)
    patch_ops = []

    new_state = copy.deepcopy(old_state)
    updated = False

    for key, value in update_parameters.items():
        if key == "api_key_required":
            key_final = "apiKeyRequired"
        elif key == "authorization_type":
            key_final = "authorizationType"
        elif key == "http_method":
            key_final = "httpMethod"

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
            updated = True
        elif old_state.get(key) is None:
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
                resource_type="aws.apigateway.method", name=old_state["name"]
            )
            result["ret"] = new_state
        else:
            result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
                resource_type="aws.apigateway.method", name=old_state["name"]
            )
        return result

    if updated:
        update_ret = await hub.exec.boto3.client.apigateway.update_method(
            ctx,
            restApiId=old_state["rest_api_id"],
            resourceId=old_state["parent_resource_id"],
            httpMethod=old_state["http_method"],
            patchOperations=patch_ops,
        )
        if not update_ret["result"]:
            result["result"] = False
            result["comment"] = update_ret["comment"]
            return result
        else:
            result["comment"] = hub.tool.aws.comment_utils.update_comment(
                resource_type="aws.apigateway.method", name=old_state["name"]
            )
            result["ret"] = new_state
    else:
        result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
            resource_type="aws.apigateway.method", name=old_state["name"]
        )

    return result
