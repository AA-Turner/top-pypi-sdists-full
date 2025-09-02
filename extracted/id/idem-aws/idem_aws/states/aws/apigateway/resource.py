"""State module for managing Amazon API Gateway Resources."""
import copy
from typing import Any
from typing import Dict

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    rest_api_id: str,
    parent_id: str,
    path_part: str,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Creates a new resource or modifies an existing one.

    Args:
        name (str): An idem name of the resource.

        rest_api_id (str): AWS rest_api id of the associated RestApi.

        parent_id (str): The parent resource's id.

        path_part (str): The last path segment for this resource.

        resource_id (str, Optional): AWS Resource id. Defaults to None.

    Returns:
        dict[str, Any]

    Examples:
        .. code-block:: sls

            idem_test_aws_apigateway_resource:
              aws.apigateway.resource.present:
                - name: test_resource
                - rest_api_id: ${aws.apigateway.rest_api:test_rest_api:resource_id}
                - parent_id: ${aws.apigateway.rest_api:test_rest_api:root_resource_id}
                - path_part: 'stack'

            idem_test_aws_apigateway_rest_api:
              aws.apigateway.rest_api.present:
                - name: test_rest_api

        Note that either ``idem_test_aws_apigateway_rest_api`` or ``test_rest_api`` can be used in the reference;
        ``${aws.apigateway.rest_api:idem_test_aws_apigateway_rest_api:resource_id}`` would work above.

        .. code-block:: sls

            [idem_test_aws_apigateway_resource]:
              aws.apigateway.resource.present:
                - name: 'string'
                - rest_api_id: 'string'
                - parent_id: 'string'
                - path_part: 'string'
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    before = None
    resource_updated = False

    if resource_id:
        before = await hub.exec.aws.apigateway.resource.get(
            ctx, name=name, resource_id=resource_id, rest_api_id=rest_api_id
        )
        if not before["result"]:
            result["comment"] = before["comment"]
            result["result"] = False
            return result

    if before and before["ret"]:
        result[
            "old_state"
        ] = hub.tool.aws.apigateway.resource.convert_raw_resource_to_present(
            before["ret"], idem_resource_name=name, rest_api_id=rest_api_id
        )

        result["new_state"] = copy.deepcopy(result["old_state"])
        update_parameters = dict(
            {
                "parent_id": parent_id,
                "path_part": path_part,
            }
        )

        update_resource_ret = await hub.tool.aws.apigateway.resource.update_resource(
            ctx,
            old_state=result["old_state"],
            update_parameters=update_parameters,
        )

        if not update_resource_ret["result"]:
            result["result"] = False
            result["comment"] = update_resource_ret["comment"]
            return result
        result["comment"] += update_resource_ret["comment"]
        resource_updated = bool(update_resource_ret["ret"])

        if resource_updated:
            if ctx.get("test", False):
                result["comment"] = result[
                    "comment"
                ] + hub.tool.aws.comment_utils.would_update_comment(
                    resource_type="aws.apigateway.resource", name=name
                )
                result["new_state"].update(update_resource_ret["ret"])
                return result

    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "rest_api_id": rest_api_id,
                    "parent_id": parent_id,
                    "path_part": path_part,
                },
            )

            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.apigateway.resource", name=name
            )
            return result

        ret = await hub.exec.boto3.client.apigateway.create_resource(
            ctx, restApiId=rest_api_id, parentId=parent_id, pathPart=path_part
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        resource_id = ret["ret"]["id"]
        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.apigateway.resource", name=name
        )

    if (not before) or resource_updated:
        after = await hub.exec.boto3.client.apigateway.get_resource(
            ctx, resourceId=resource_id, restApiId=rest_api_id
        )
        if not (after["result"] and after["ret"]):
            result["result"] = False
            result["comment"] += after["comment"]
            return result
        resource_translated = (
            hub.tool.aws.apigateway.resource.convert_raw_resource_to_present(
                after["ret"], idem_resource_name=name, rest_api_id=rest_api_id
            )
        )
        result["new_state"] = resource_translated

    return result


async def absent(
    hub, ctx, name: str, rest_api_id: str = None, resource_id: str = None
) -> Dict[str, Any]:
    """Deletes the specified resource.

    Args:
        name (str): The Idem name of the resource.

        rest_api_id (str, Optional): AWS rest_api id of the associated RestApi.

        resource_id (str, Optional): AWS Resource id. Defaults to None.

    Returns:
        dict[str, Any]

    Examples:

        .. code-block:: sls

            resource_is_absent:
              aws.apigateway.resource.absent:
                - name: value
                - resource_id: value
                - rest_api_id: value
    """
    result = dict(
        comment=[],
        old_state=None,
        new_state=None,
        name=name,
        result=True,
    )

    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.apigateway.resource", name=name
        )
        return result

    if not rest_api_id:
        result["comment"] = hub.tool.aws.comment_utils.missing_args_for_absent_comment(
            resource_type="aws.apigateway.resource", name=name, args=["rest_api_id"]
        )
        result["result"] = False
        return result

    before_ret = await hub.exec.boto3.client.apigateway.get_resource(
        ctx, resourceId=resource_id, restApiId=rest_api_id
    )

    if not before_ret["result"]:
        if "NotFoundException" not in str(before_ret["comment"][0]):
            result["result"] = False
            result["comment"] = before_ret["comment"]
        else:
            result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
                resource_type="aws.apigateway.resource", name=name
            )
        return result

    result[
        "old_state"
    ] = hub.tool.aws.apigateway.resource.convert_raw_resource_to_present(
        raw_resource=before_ret["ret"],
        rest_api_id=rest_api_id,
    )
    if ctx.get("test", False):
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.apigateway.resource", name=name
        )
        return result

    ret = await hub.exec.boto3.client.apigateway.delete_resource(
        ctx, restApiId=rest_api_id, resourceId=resource_id
    )

    if not ret["result"]:
        result["result"] = False
        result["comment"] = ret["comment"]
        return result

    result["comment"] = hub.tool.aws.comment_utils.delete_comment(
        resource_type="aws.apigateway.resource", name=name
    )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the API Gateway Resources associated with a specific Rest API.

    Returns a list of apigateway.resource descriptions

    Returns:
        dict[str, Any]

    Examples:

        .. code-block:: bash

            $ idem describe aws.apigateway.resource

    """

    result = {}

    get_rest_apis_ret = await hub.exec.boto3.client.apigateway.get_rest_apis(ctx)
    if not get_rest_apis_ret["result"]:
        hub.log.warning(f"Could not get Rest Apis {get_rest_apis_ret['comment']}")
        return result

    for rest_api in get_rest_apis_ret["ret"]["items"]:
        rest_api_name = rest_api.get("name")
        rest_api_id = rest_api.get("id")

        get_resources_ret = await hub.exec.boto3.client.apigateway.get_resources(
            ctx, restApiId=rest_api_id
        )
        if not get_resources_ret["result"]:
            hub.log.debug(
                f"Could not get Resources for Rest Api '{rest_api_name}': "
                f"{get_resources_ret['comment']}. Describe will skip this Rest Api and continue."
            )
            continue

        for resource in get_resources_ret["ret"]["items"]:
            # the resource response will always have a dictionary of size 2 which contains
            # just the parentId and an empty name, and we should filter those out
            if len(resource) != 2:
                resource_translated = (
                    hub.tool.aws.apigateway.resource.convert_raw_resource_to_present(
                        raw_resource=resource,
                        rest_api_id=rest_api_id,
                    )
                )

                result[resource_translated["resource_id"]] = {
                    "aws.apigateway.resource.present": [
                        {parameter_key: parameter_value}
                        for parameter_key, parameter_value in resource_translated.items()
                    ]
                }

    return result
