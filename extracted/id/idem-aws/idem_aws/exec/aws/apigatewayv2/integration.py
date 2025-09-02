"""Exec functions for AWS API Gateway v2 Integration resources."""
from typing import Any
from typing import Dict


async def get(
    hub, ctx, resource_id: str, api_id: str, name: str = None
) -> Dict[str, Any]:
    """Gets an Integration.

    Args:
        resource_id(str):
            The integration ID.

        api_id(str):
            The API identifier.

        name(str, Optional):
            The name of the Idem state.

    Returns:
        Dict[str, Any]:
            Returns an integration.

    Examples:
        Call from the CLI:

        .. code-block:: bash

            idem exec aws.apigatewayv2.integration.get resource_id="integration_id" api_id="api_id" name="my_resource"

        Call from code:

        .. code-block:: python

            async def my_func(hub, ctx, resource_id:str, api_id: str, name:str = None):
                await hub.exec.aws.apigatewayv2.integration.get(ctx, resource_id, api_id, name)

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.apigatewayv2.integration.get
                - kwargs:
                    resource_id: integration_id
                    api_id: api_id
                    name: my_resource
    """
    result = dict(comment=[], ret=None, result=True)
    ret = await hub.exec.boto3.client.apigatewayv2.get_integration(
        ctx, ApiId=api_id, IntegrationId=resource_id
    )
    if not ret["result"]:
        if "NotFoundException" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.apigatewayv2.integration", name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    result[
        "ret"
    ] = hub.tool.aws.apigatewayv2.integration.convert_raw_integration_to_present(
        api_id=api_id,
        raw_resource=ret["ret"],
        idem_resource_name=name if name is not None else resource_id,
    )
    return result
