"""Exec functions for AWS API Gateway v2 API resources."""
from typing import Any
from typing import Dict


__func_alias__ = {"list_": "list"}


async def get(hub, ctx, name: str, resource_id: str) -> Dict[str, Any]:
    """
    Get an API resource from AWS

    Args:
        name(str):
            The name of the Idem state

        resource_id(str):
            The API identifier

    Returns:
        Dict[str, Any]:
            Returns API resource

    Examples:
        Call from the CLI:

        .. code-block:: bash

            idem exec aws.apigatewayv2.api.get name="my_resource" resource_id="resource_id"

        Call from code:

        .. code-block:: python

            async def my_func(hub, ctx, name:str, resource_id:str):
                await hub.exec.aws.apigatewayv2.api.get(ctx, name, resource_id)

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.apigatewayv2.api.get
                - kwargs:
                    name: my_resource
                    resource_id: resource_id
    """
    result = dict(comment=[], ret=None, result=True)

    ret = await hub.exec.boto3.client.apigatewayv2.get_api(ctx, ApiId=resource_id)
    if not ret["result"]:
        if "NotFoundException" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.apigatewayv2.api", name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result

    result["ret"] = hub.tool.aws.apigatewayv2.api.convert_raw_api_to_present(
        raw_resource=ret["ret"]
    )
    return result


async def list_(hub, ctx) -> Dict[str, Any]:
    """
    Get a list of API resource from AWS

    Args:
        None

    Returns:
        Dict[str, Any]:
            Returns API resources

    Examples:
        Call from the CLI:

        .. code-block:: bash

            idem exec aws.apigatewayv2.api.list

        Call from code:

        .. code-block:: python

            async def my_func(hub, ctx):
                await hub.exec.aws.apigatewayv2.api.list(ctx)

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.apigatewayv2.api.list
    """
    result = dict(comment=[], ret=None, result=True)

    ret = await hub.exec.boto3.client.apigatewayv2.get_apis(ctx)

    if not ret["result"]:
        if "NotFoundException" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.apigatewayv2.api"
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result

    result["ret"] = []
    for api in ret["ret"]["Items"]:
        result["ret"].append(
            hub.tool.aws.apigatewayv2.api.convert_raw_api_to_present(raw_resource=api)
        )
    return result
