import copy
from collections import OrderedDict
from typing import Any
from typing import Dict


def convert_raw_rest_api_to_present(
    hub,
    raw_resource: Dict[str, Any],
    idem_resource_name: str = None,
) -> Dict[str, Any]:
    """Convert AWS returned data structure to correct idem apigateway.rest_api present state

     Args:
        raw_resource: The aws response to convert

        idem_resource_name (str, Optional): An idem name of the resource

    Returns: Valid idem state for apigateway.rest_api of type dict['string', Any]
    """
    resource_id = raw_resource.get("id")
    resource_parameters = OrderedDict(
        {
            "description": "description",
            "version": "version",
            "binaryMediaTypes": "binary_media_types",
            "minimumCompressionSize": "minimum_compression_size",
            "apiKeySource": "api_key_source",
            "endpointConfiguration": "endpoint_configuration",
            "policy": "policy",
            "tags": "tags",
            "disableExecuteApiEndpoint": "disable_execute_api_endpoint",
            "rootResourceId": "root_resource_id",
        }
    )
    resource_translated = {"name": idem_resource_name, "resource_id": resource_id}
    for parameter_raw, parameter_present in resource_parameters.items():
        if raw_resource.get(parameter_raw) is not None:
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)

    return resource_translated


async def update_rest_api(
    hub, ctx, old_state: Dict[str, Any], updatable_resource_parameters: Dict[str, Any]
):
    """Updates an AWS API Gateway API resource.

    Args:
        old_state (dict): Previous state of the rest_api resource

        updatable_resource_parameters (dict): Parameters from SLS file.

    Returns:
        dict[str, Any]
    """
    result = dict(comment=[], result=True, ret=None)
    patch_operations = []

    new_state = copy.deepcopy(old_state)
    resource_updated = False
    for key, value in updatable_resource_parameters.items():
        if value is not None:
            if key == "endpoint_configuration":
                if len(value["types"]) != len(old_state[key]["types"]):
                    # there can be multiple types at once, but add/remove aren't supported.
                    # see https://docs.aws.amazon.com/apigateway/latest/api/patch-operations.html
                    result["comment"] += [
                        f"AWS doesn't support changing the number of endpoint types. You are trying to go from "
                        f"{value['types']} to {old_state[key]['types']}. The lengths must be "
                        f"equal; {len(value['types'])} != {len(old_state[key]['types'])}."
                    ]
                    result["result"] = False
                    return result
                for i in range(len(value["types"])):
                    if value["types"][i] != old_state[key]["types"][i]:
                        patch_operations.append(
                            {
                                "op": "replace",
                                "path": f"/endpointConfiguration/types/{old_state[key]['types'][i]}",
                                "value": value["types"][i],
                            }
                        )
                        new_state[key]["types"][i] = value["types"][i]
                        resource_updated = True

                old_vpc_endpoint_ids = old_state["endpoint_configuration"].get(
                    "vpcEndpointIds", []
                )
                new_vpc_endpoint_ids = value.get("vpcEndpointIds", [])
                if not (
                    hub.tool.aws.state_comparison_utils.are_lists_identical(
                        old_vpc_endpoint_ids,
                        new_vpc_endpoint_ids,
                    )
                ):
                    endpoints_to_remove = list(
                        set(old_vpc_endpoint_ids).difference(set(new_vpc_endpoint_ids))
                    )
                    endpoints_to_add = list(
                        set(new_vpc_endpoint_ids).difference(set(old_vpc_endpoint_ids))
                    )
                    if endpoints_to_remove:
                        patch_operations.append(
                            {
                                "op": "remove",
                                "path": f"/endpointConfiguration/vpcEndpointIds",
                                "value": ",".join(endpoints_to_remove),
                            }
                        )
                    if endpoints_to_add:
                        patch_operations.append(
                            {
                                "op": "add",
                                "path": f"/endpointConfiguration/vpcEndpointIds",
                                "value": ",".join(endpoints_to_add),
                            }
                        )

                    new_state["endpoint_configuration"][
                        "vpcEndpointIds"
                    ] = new_vpc_endpoint_ids
                    resource_updated = True
            elif (
                isinstance(value, list)
                and not hub.tool.aws.state_comparison_utils.are_lists_identical(
                    value,
                    old_state.get(key, []),
                )
                or value != old_state[key]
            ):
                if old_state.get(key):
                    patch_operations.append(
                        {
                            "op": "replace",
                            "path": f"/{key}",
                            "value": str(value)
                            if not isinstance(value, list)
                            else ",".join(value),
                        }
                    )
                else:
                    patch_operations.append(
                        {
                            "op": "add",
                            "path": f"/{key}",
                            "value": str(value)
                            if not isinstance(value, list)
                            else ",".join(value),
                        }
                    )
                new_state[key] = value
                resource_updated = True
    if ctx.get("test", False):
        if resource_updated:
            result["ret"] = new_state
        return result

    if resource_updated:
        update_ret = await hub.exec.boto3.client.apigateway.update_rest_api(
            ctx, restApiId=old_state["resource_id"], patchOperations=patch_operations
        )
        if not update_ret["result"]:
            result["result"] = False
            result["comment"] += update_ret["comment"]
            return result
        else:
            result["comment"] += hub.tool.aws.comment_utils.update_comment(
                resource_type="aws.apigateway.rest_api", name=old_state["name"]
            )
            result["ret"] = new_state

    else:
        result["comment"] += hub.tool.aws.comment_utils.already_exists_comment(
            resource_type="aws.apigateway.rest_api", name=old_state["name"]
        )

    return result
