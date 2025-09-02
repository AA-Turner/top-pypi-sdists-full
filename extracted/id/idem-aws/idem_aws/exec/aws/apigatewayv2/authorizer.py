"""Exec functions for AWS API Gateway v2 Authorizer resources."""
from typing import Any
from typing import Dict


async def get(hub, ctx, name: str, resource_id: str, api_id: str) -> Dict[str, Any]:
    """Gets an Authorizer.

    Args:
        name(str):
            The name of the Idem state.

        resource_id(str):
            The authorizer identifier.

        api_id(str):
            The API identifier.

    Returns:
        Dict[str, Any]:
            Returns an Authorizer.

    Examples:
        Call from the CLI:

        .. code-block:: bash

            idem exec aws.apigatewayv2.authorizer.get name="my_resource" resource_id="authorizer_id" api_id="api_id"

        Call from code:

        .. code-block:: python

            async def my_func(hub, ctx, name:str, resource_id:str, api_id: str):
                await hub.exec.aws.apigatewayv2.authorizer.get(ctx, name, resource_id, api_id)

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.apigatewayv2.authorizer.get
                - kwargs:
                    name: my_resource
                    resource_id: authorizer_id
                    api_id: api_id
    """
    result = dict(comment=[], ret=None, result=True)
    ret = await hub.exec.boto3.client.apigatewayv2.get_authorizer(
        ctx, ApiId=api_id, AuthorizerId=resource_id
    )
    if not ret["result"]:
        if "NotFoundException" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.apigatewayv2.authorizer", name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    result[
        "ret"
    ] = hub.tool.aws.apigatewayv2.authorizer.convert_raw_authorizer_to_present(
        api_id=api_id, raw_resource=ret["ret"]
    )
    return result
