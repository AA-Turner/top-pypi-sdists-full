import copy
from collections import OrderedDict
from typing import Any
from typing import Dict
from typing import List


def convert_raw_integration_to_present(
    hub,
    raw_resource: Dict[str, Any],
    resource_id: str,
    idem_resource_name: str = None,
) -> Dict[str, Any]:
    resource_parameters = OrderedDict(
        {
            "type": "input_type",
            "passthroughBehavior": "passthrough_behavior",
            "timeoutInMillis": "timeout_in_millis",
            "cacheNamespace": "cache_namespace",
            "cacheKeyParameters": "cache_key_parameters",
            "integrationResponses": "integration_responses",
            "httpMethod": "integration_http_method",
            "uri": "uri",
        }
    )

    rest_api_id, parent_resource_id, http_method = resource_id.split("-")

    resource_translated = {
        "resource_id": resource_id,
        "rest_api_id": rest_api_id,
        "parent_resource_id": parent_resource_id,
        "http_method": http_method,
    }

    if idem_resource_name:
        resource_translated["name"] = idem_resource_name

    for parameter_raw, parameter_present in resource_parameters.items():
        if raw_resource.get(parameter_raw):
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)

    return resource_translated


async def update(
    hub,
    ctx,
    old_state: Dict[str, Any],
    updatable_parameters: Dict[str, Any],
):
    """
    Updates an API Gateway Integration.

    Args:
        old_state(dict): Previous state of the resource.

        updatable_parameters(dict): Parameters from SLS File.

    Returns:
        dict[str, Any]
    """

    result = dict(comment=[], result=True, ret=None)
    patch_ops = []

    new_state = copy.deepcopy(old_state)
    updated = False

    for key, value in updatable_parameters.items():
        if key == "passthrough_behavior":
            key_final = "passthroughBehavior"
        elif key == "connection_id":
            key_final = "connectionId"
        elif key == "cache_key_parameters":
            key_final = "cacheKeyParameters"
        elif key == "cache_namespace":
            key_final = "cacheNamespace"
        elif key == "timeout_in_millis":
            key_final = "timeoutInMillis"
        elif key == "input_type":
            key_final = "type"
        if old_state.get(key) and value is not None and value != old_state.get(key):
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
                resource_type="aws.apigateway.integration", name=old_state["name"]
            )
            result["ret"] = new_state
        else:
            result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
                resource_type="aws.apigateway.integration", name=old_state["name"]
            )
        return result

    if updated:
        update_ret = await hub.exec.boto3.client.apigateway.update_integration(
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
                resource_type="aws.apigateway.integration", name=old_state["name"]
            )
            result["ret"] = new_state
    else:
        result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
            resource_type="aws.apigateway.integration", name=old_state["name"]
        )

    return result
