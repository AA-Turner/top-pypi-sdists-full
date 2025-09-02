import copy
from collections import OrderedDict
from typing import Any
from typing import Dict
from typing import List


def convert_raw_base_path_mapping_to_present(
    hub,
    raw_resource: Dict[str, Any],
    domain_name: str,
) -> Dict[str, Any]:
    """
    Convert AWS API Gateway Resource to a common idem present state.

    Args:
        hub: required for functions in hub.
        raw_resource(str): The AWS response to convert.
        domain_name(str): The domain name of the BasePathMapping resource to create.

    Returns:
        Dict[str, Any]
    """
    rest_api_id = raw_resource["restApiId"]
    base_path = raw_resource["basePath"]

    resource_id = f"{domain_name}/{base_path}"

    resource_parameters = OrderedDict(
        {
            "basePath": "base_path",
            "stage": "stage",
        }
    )

    resource_translated = {
        # "name": idem_resource_name,
        "domain_name": domain_name,
        "resource_id": resource_id,
        "rest_api_id": rest_api_id,
    }

    for parameter_raw, parameter_present in resource_parameters.items():
        if raw_resource.get(parameter_raw):
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)

    return resource_translated


async def update(
    hub,
    ctx,
    domain_name: str,
    old_state: Dict[str, Any],
    updatable_parameters: Dict[str, Any],
):
    """
    Updates an API Gateway domain_name base path mapping.

    Args:
        domain_name(str):
            Apigateway the domain name for base path mapping
        old_state(dict):
            Previous state of the base path mapping resource.
        updatable_parameters(dict):
            Parameters from SLS File.

    Returns:
        Dict[str, Any]
    """
    result = dict(comment=[], result=True, ret=None)
    patch_operations = []
    new_state = copy.deepcopy(old_state)
    to_be_updated = False
    base_path = updatable_parameters["base_path"]
    f"{domain_name}/{base_path}"
    for key, value in updatable_parameters.items():
        if key == "rest_api_id":
            key_final = "restApiId"
        if key == "base_path":
            key_final = "basePath"
        if key == "stage":
            key_final = "stage"
        if (
            old_state.get(key) is not None
            and value is not None
            and value != old_state.get(key)
        ):
            patch_operations.append(
                {
                    "op": "replace",
                    "path": f"/{key_final}",
                    "value": str(value)
                    if not isinstance(value, List)
                    else ",".join(value),
                }
            )
            new_state[key] = value
            to_be_updated = True
    if ctx.get("test", False):
        if to_be_updated:
            result["comment"] = hub.tool.aws.comment_utils.would_update_comment(
                resource_type="aws.apigateway.base_path_mapping",
                name=old_state["domain_name"],
            )
            result["ret"] = new_state
        else:
            result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
                resource_type="aws.apigateway.base_path_mapping",
                name=old_state["domain_name"],
            )
            return result
    if to_be_updated:
        update_ret = await hub.exec.boto3.client.apigateway.update_base_path_mapping(
            ctx,
            domainName=domain_name,
            basePath=base_path,
            patchOperations=patch_operations,
        )
        result["comment"] = hub.tool.aws.comment_utils.update_comment(
            resource_type="aws.apigateway.base_path_mapping",
            name=old_state["domain_name"],
        )
        if not update_ret["result"]:
            result["result"] = False
            result["comment"] = update_ret["comment"]
    return result
