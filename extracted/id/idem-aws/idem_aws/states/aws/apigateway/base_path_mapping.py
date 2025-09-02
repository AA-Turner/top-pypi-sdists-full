"""State module for managing AWS Api Gateway Base Path Mapping resources."""
import copy
from typing import Any
from typing import Dict

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    rest_api_id: str,
    domain_name: str,
    base_path: str = None,
    stage: str = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    """
    Creates a new resource or modifies an existing one.

    Args:
        name(str): An idem name of the resource.
        rest_api_id(str): AWS rest api id of the associated Api.
        domain_name(str): The domain name of the BasePathMapping resource to create.
        base_path(str, Optional): The base path name that callers of the API must provide as part of the URL after the domain name.
                            This value must be unique for all of the mappings across a single API.
                            Specify '(none)' if you do not want callers to specify a base path name after the domain name.
        stage(str, Optional): The name of the API's stage that you want to use for this mapping.
                                Specify '(none)' if you want callers to explicitly specify the stage name after any base path name.
        resource_id(str, Optional): Idem Resource ID that is generated once the resource is created..

    Request Syntax:
        [idem_test_aws_apigateway_resource]:
          aws.apigateway.resource.present:
            - name: 'string'
            - rest_api_id: 'string'
            - domain_name: 'string'
            - stage: 'string'
            - base_path: 'string'

    Returns:
        Dict[str, Any]

    Example:
        [idem_test_aws_apigateway_resource]:
          aws.apigateway.resource.present:
            - name: api.idem-jedi-test.com
            - rest_api_id: 1s6c0ucab9
            - domain_name: api.idem-jedi-test.com
            - stage: staging
            - base_path: idem
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    resource_updated = False
    before_ret = None
    if resource_id:
        before_ret = await hub.exec.aws.apigateway.base_path_mapping.get(
            ctx,
            domain_name=domain_name,
            base_path=base_path,
            resource_id=resource_id,
        )
        if not before_ret["result"] or not before_ret["ret"]:
            result["result"] = False
            result["comment"] = before_ret["comment"]
            return result
        result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
            resource_type="aws.apigateway.base_path_mapping", name=domain_name
        )
        result["old_state"] = before_ret["ret"]
        result["new_state"] = copy.deepcopy(result["old_state"])
        update_parameters = {
            "rest_api_id": rest_api_id,
            "stage": stage,
            "base_path": base_path,
        }
        update_base_path = await hub.tool.aws.apigateway.base_path_mapping.update(
            ctx,
            domain_name=domain_name,
            old_state=result["old_state"],
            updatable_parameters=update_parameters,
        )
        if not update_base_path["result"]:
            result["result"] = False
            result["comment"] = update_base_path["comment"]
            return result
        result["comment"] += update_base_path["comment"]
        resource_updated = bool(update_base_path["ret"])
        if resource_updated and ctx.get("test", False):
            result["new_state"].update(update_base_path["ret"])
        if resource_updated:
            if ctx.get("test", False):
                result["comment"] = result[
                    "comment"
                ] + hub.tool.aws.comment_utils.would_update_comment(
                    resource_type="aws.apigateway.base_path_mapping", name=name
                )
                return result
            else:
                result["comment"] = result[
                    "comment"
                ] + hub.tool.aws.comment_utils.update_comment(
                    resource_type="aws.apigateway.base_path_mapping", name=name
                )
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "domain_name": domain_name,
                    "rest_api_id": rest_api_id,
                    "stage": stage,
                    "base_path": base_path,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.apigateway.base_path_mapping", name=name
            )
            return result

        ret = await hub.exec.boto3.client.apigateway.create_base_path_mapping(
            ctx,
            restApiId=rest_api_id,
            domainName=domain_name,
            stage=stage,
            basePath=base_path,
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.apigateway.base_path_mapping", name=domain_name
        )
    if (not before_ret) or resource_updated:
        resource_id = f"{domain_name}/{base_path}"
        get_ret = await hub.exec.aws.apigateway.base_path_mapping.get(
            ctx,
            resource_id=resource_id,
        )
        if not (get_ret["result"] and get_ret["ret"]):
            result["result"] = False
            result["comment"] = get_ret["comment"]
            return result
        result["new_state"] = get_ret["ret"]
    else:
        result["new_state"] = copy.deepcopy(result["old_state"])
    return result


async def absent(
    hub,
    ctx,
    name: str,
    domain_name: str = None,
    base_path: str = None,
    resource_id: str = None,
):
    """
    Deletes the specified base path mapping.

    Args:
        name(str): The Idem name of the resource.
        domain_name(str, Optional): the domain name of the BasePathMapping resource to delete.
        base_path(str, Optional): The base path name of the BasePathMapping resource to delete.
                                    To specify an empty base path, set this parameter to '(none)' .
        resource_id(str, Optional): AWS Resource id. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: sls

            idem_test_aws_apigateway_base_path_mapping:
              aws.apigateway.base_path_mapping.absent:
                - name: value
                - resource_id: value


    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.apigateway.base_path_mapping", name=name
        )
        return result

    before_ret = await hub.exec.aws.apigateway.base_path_mapping.get(
        ctx, resource_id=resource_id
    )

    if not before_ret["result"]:
        result["result"] = False
        result["comment"] = before_ret["comment"]
        return result

    if not before_ret["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.apigateway.base_path_mapping", name=name
        )
        return result

    if not domain_name or not base_path:
        result["comment"] = hub.tool.aws.comment_utils.missing_args_for_absent_comment(
            resource_type="aws.apigateway.base_path_mapping",
            name=name,
            args=["domain_name", "base_type"],
        )
        result["result"] = False
        return result

    if ctx.get("test", False):
        result["old_state"] = before_ret["ret"]
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.apigateway.base_path_mapping", name=name
        )
        return result

    else:
        result["old_state"] = before_ret["ret"]
        delete_ret = await hub.exec.boto3.client.apigateway.delete_base_path_mapping(
            ctx,
            domainName=domain_name,
            basePath=base_path,
        )

        if not delete_ret["result"]:
            result["result"] = False
            result["comment"] = delete_ret["comment"]
            return result

        result["comment"] = hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.apigateway.base_path_mapping", name=name
        )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """
    Describe the API Gateway base path mapping associated with a specific API.

    Returns a list of apigateway.base_path_mapping descriptions

    Returns:
        Dict[str, Any]


    Examples:

        .. code-block:: bash

            $ idem describe aws.apigateway.base_path_mapping

    """

    result = {}

    get_domain_names_ret = await hub.exec.boto3.client.apigateway.get_domain_names(ctx)
    if not get_domain_names_ret["result"]:
        hub.log.warning(f"Could not get domain_names {get_domain_names_ret['comment']}")
        return result

    for domain_name in get_domain_names_ret["ret"]["items"]:
        domain_name = domain_name.get("domainName")
        get_base_path_mappings_ret = (
            await hub.exec.aws.apigateway.base_path_mapping.list(
                ctx,
                domain_name=domain_name,
            )
        )
        if not get_base_path_mappings_ret["result"]:
            hub.log.debug(
                f"Could not get base path mappings for domain name '{domain_name}': "
                f"{get_base_path_mappings_ret['comment']}. Describe will skip this domain name and continue."
            )
            continue

        for base_path_mapping in get_base_path_mappings_ret["ret"]:
            result[base_path_mapping["resource_id"]] = {
                "aws.apigateway.base_path_mapping.present": [
                    {parameter_key: parameter_value}
                    for parameter_key, parameter_value in base_path_mapping.items()
                ]
            }
    return result
