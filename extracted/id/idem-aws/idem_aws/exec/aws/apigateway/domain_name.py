"""Exec module for AWS API Gateway Domain Name resources."""
__func_alias__ = {"list_": "list"}

from typing import Dict


async def get(hub, ctx, name: str, resource_id: str) -> Dict:
    """
    Get an API Gateway domain name resource from AWS with the domain name as the resource_id.

    Args:
        name(str):
            The name of the Idem state domain name.
        resource_id(str):
            AWS API Gateway domain name.

    Returns:
        Dict[str, Any]

    Examples:

        Calling from the CLI:

        .. code-block:: bash

            $ idem exec aws.apigateway.domain_name.get name="unmanaged_domain_names"


        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.apigateway.domain_name.get
                - kwargs:
                    name: unmanaged_domain_name
                    resource_id: resource_id

    """
    result = dict(comment=[], ret=None, result=True)
    ret = await hub.exec.boto3.client.apigateway.get_domain_name(
        ctx=ctx, domainName=resource_id
    )
    if not ret["result"]:
        if "NotFoundException" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.apigateway.domain_name", name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result

    result[
        "ret"
    ] = hub.tool.aws.apigateway.domain_name.convert_raw_domain_name_to_present(
        raw_resource=ret["ret"], idem_resource_name=name
    )
    return result


async def list_(hub, ctx, name: str = None):
    """Get the list of domain names for AWS APIGateway.

    Args:
        name (str, Optional):
            The name of the Idem state for logging.

    Returns:
        Dict[str, Any]

    Examples:
        Calling from the CLI:

        .. code-block:: bash

            idem exec aws.apigateway.domain_name.list

        Calling this exec module function from within a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.apigateway.domain_name.list
                - kwargs:
                    name: my-resource-name
    """
    result = dict(comment=[], ret=[], result=True)
    get_domain_names_ret = await hub.exec.boto3.client.apigateway.get_domain_names(ctx)
    if (
        "NotFoundException" in str(get_domain_names_ret["comment"])
        or get_domain_names_ret["ret"]["items"] == []
    ):
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.apigateway.domain_name", name="domain_name_resource"
            )
        )
        return []
    for domain_name in get_domain_names_ret["ret"]["items"]:
        idem_resource_name = domain_name["domainName"]
        get_translated_resource = (
            hub.tool.aws.apigateway.domain_name.convert_raw_domain_name_to_present(
                raw_resource=domain_name, idem_resource_name=idem_resource_name
            )
        )
        result["ret"].append(get_translated_resource)
    return result
