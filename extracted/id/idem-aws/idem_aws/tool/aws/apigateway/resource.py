import copy
from collections import OrderedDict
from typing import Any
from typing import Dict


def convert_raw_resource_to_present(
    hub,
    raw_resource: Dict[str, Any],
    idem_resource_name: str = None,
    rest_api_id: str = None,
) -> Dict[str, Any]:
    """Convert AWS API Gateway Resource to a common idem present state.

    Args:
        raw_resource (dict[str, Any]): The AWS response to convert.

        idem_resource_name (str, Optional): The resource name if applicable,
            otherwise resource name will be taken from raw_resource.

        rest_api_id (str, Optional): Rest Api id associated with the Rest Api to which the Resource belongs.

    Returns:
        dict[str, Any]: Common idem present state
    """

    resource_id = raw_resource.get("id")

    if idem_resource_name:
        name = idem_resource_name
    else:
        name = raw_resource.get("pathPart")

    resource_parameters = OrderedDict(
        {
            "parentId": "parent_id",
            "pathPart": "path_part",
            "path": "path",
        }
    )

    resource_translated = {
        "name": name,
        "resource_id": resource_id,
        "rest_api_id": rest_api_id,
    }
    for parameter_raw, parameter_present in resource_parameters.items():
        resource_translated[parameter_present] = raw_resource.get(parameter_raw)

    return resource_translated


async def update_resource(
    hub, ctx, old_state: Dict[str, Any], update_parameters: Dict[str, any]
):
    """Updates an API Gateway Resource

    Args:
        old_state (dict): Previous state o  f resource

        update_parameters (dict): Parameters from SLS File

    Returns:
        dict[str, Any]
    """

    result = dict(comment=[], result=True, ret=None)
    patch_ops = []

    new_state = copy.deepcopy(old_state)
    updated = False

    for key, value in update_parameters.items():
        if key == "parent_id":
            key_final = "parentId"
        else:
            key_final = "pathPart"

        if old_state.get(key) and value != old_state.get(key):
            patch_ops.append(
                {
                    "op": "replace",
                    "path": f"/{key_final}",
                    "value": str(value)
                    if not isinstance(value, list)
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
                    if not isinstance(value, list)
                    else ",".join(value),
                }
            )

            new_state[key] = value
            updated = True

    if ctx.get("test", False):
        if updated:
            result["comment"] = hub.tool.aws.comment_utils.would_update_comment(
                resource_type="aws.apigateway.resource", name=old_state["name"]
            )
            result["ret"] = new_state
        else:
            result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
                resource_type="aws.apigateway.resource", name=old_state["name"]
            )
        return result

    if updated:
        update_ret = await hub.exec.boto3.client.apigateway.update_resource(
            ctx,
            restApiId=old_state["rest_api_id"],
            resourceId=old_state["resource_id"],
            patchOperations=patch_ops,
        )
        if not update_ret["result"]:
            result["result"] = False
            result["comment"] = update_ret["comment"]
            return result
        else:
            result["comment"] = hub.tool.aws.comment_utils.update_comment(
                resource_type="aws.apigateway.resource", name=old_state["name"]
            )
            result["ret"] = new_state
    else:
        result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
            resource_type="aws.apigateway.resource", name=old_state["name"]
        )

    return result
