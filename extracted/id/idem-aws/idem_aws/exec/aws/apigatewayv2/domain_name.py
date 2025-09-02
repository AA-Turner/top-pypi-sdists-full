"""Exec functions for AWS API Gateway v2 Domain Name resources."""
from typing import Any
from typing import Dict


async def get(hub, ctx, name, resource_id: str) -> Dict[str, Any]:
    """Gets a domain name.

    Args:
        name(str):
            The name of the Idem state.

        resource_id(str):
            The domain name.

    Returns:
        Dict[str, Any]:
            Returns a domain name.

    Examples:
        Call from the CLI:

        .. code-block:: bash

            idem exec aws.apigatewayv2.domain_name.get name="my_resource" resource_id="domain_name"

        Call from code:

        .. code-block:: python

            async def my_func(hub, ctx, name:str, resource_id:str):
                await hub.exec.aws.apigatewayv2.domain_name.get(ctx, name, resource_id)

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.apigatewayv2.domain_name.get
                - kwargs:
                    name: my_resource
                    resource_id: domain_name
    """
    result = dict(comment=[], ret=None, result=True)

    ret = await hub.exec.boto3.client.apigatewayv2.get_domain_name(
        ctx, DomainName=resource_id
    )
    if not ret["result"]:
        if "NotFoundException" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.apigatewayv2.domain_name", name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result

    result[
        "ret"
    ] = hub.tool.aws.apigatewayv2.domain_name.convert_raw_domain_name_to_present(
        raw_resource=ret["ret"]
    )
    return result
