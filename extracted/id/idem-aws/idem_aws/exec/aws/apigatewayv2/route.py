"""Exec functions for AWS API Gateway v2 API resources."""
from typing import Any
from typing import Dict


__func_alias__ = {"list_": "list"}


async def get(hub, ctx, name: str, api_id: str, route_id: str) -> Dict[str, Any]:
    """Get a route resource from AWS.

    Args:
        name(str):
            The name of the Idem state.

        api_id(str):
            The API identifier.

        route_id(str):
            The route ID.

    Returns:
        Dict[str, Any]:
            Returns a route.

    Examples:
        Call from the CLI:

        .. code-block:: bash

            idem exec aws.apigatewayv2.route.get name="my_resource" api_id="api_id" route_id="route_id"

        Call from code:

        .. code-block:: python

            async def my_func(hub, ctx, name:str, api_id:str, route_id:str):
                await hub.exec.aws.apigatewayv2.route.get(ctx, name, api_id, route_id)

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.apigatewayv2.route.get
                - kwargs:
                    name: my_resource
                    api_id: api_id
                    route_id: route_id
    """
    result = dict(comment=[], ret=None, result=True)

    ret = await hub.exec.boto3.client.apigatewayv2.get_route(
        ctx, ApiId=api_id, RouteId=route_id
    )
    if not ret["result"]:
        if "NotFoundException" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.apigatewayv2.route", name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result

    result["ret"] = hub.tool.aws.apigatewayv2.route.convert_raw_route_to_present(
        raw_resource=ret["ret"],
        api_id=api_id,
    )
    return result


async def list_(hub, ctx, api_id: str) -> Dict[str, Any]:
    """Get a list of route resources from AWS.

    Args:
        api_id(str):
            The API identifier.

    Returns:
        Dict[str, Any]:
            Returns a route.

    Examples:
        Call from the CLI:

        .. code-block:: bash

            idem exec aws.apigatewayv2.route.get name="my_resource" api_id="api_id"

        Call from code:

        .. code-block:: python

            async def my_func(hub, ctx, name:str, api_id:str):
                await hub.exec.aws.apigatewayv2.route.get(ctx, name, api_id)

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.apigatewayv2.route.get
                - kwargs:
                    name: my_resource
                    api_id: api_id
    """
    result = dict(comment=[], ret=None, result=True)

    ret = await hub.exec.boto3.client.apigatewayv2.get_routes(ctx, ApiId=api_id)

    if not ret["result"]:
        if "NotFoundException" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.apigatewayv2.route", name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result

    result["ret"] = []
    for item in ret["ret"]["Items"]:
        result["ret"].append(
            hub.tool.aws.apigatewayv2.route.convert_raw_route_to_present(
                raw_resource=item,
                api_id=api_id,
            )
        )
    return result
