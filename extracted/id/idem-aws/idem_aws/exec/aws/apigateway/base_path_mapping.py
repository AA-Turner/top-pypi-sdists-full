"""Exec module for AWS API Gateway Base Path Mapping resources."""
__func_alias__ = {"list_": "list"}


async def get(
    hub,
    ctx,
    domain_name: str = None,
    base_path: str = None,
    resource_id: str = None,
):
    """
    Get a single API Gateway base path mapping from AWS. The function returns None if no resource is found.
    The get api call requires either of resource_id or the combination of base_path and domain name. So the user is free to choose between either the resource_id or base_path and domain name. But, both these sets are not required.
    When using domain_name and base_path as input parameters, both are mandatory. While, using resource_id, the other two parameters can be skipped, and hence they come as optional parameters in the signature.

    Args:
        domain_name(str, Optional):
            The parent domain name of the base_path_mapping resource to be described.
        base_path(str, Optional):
            The base path name that callers of the API must provide as part
            of the URL after the domain name. This value must be unique for all of the mappings
            across a single API. Specify '(none)' if you do not want callers to specify any base
            path name after the domain name.
        resource_id(str, Optional):
            Idem Resource ID that is generated once the resource is created.


    Examples:
        Calling from the CLI:

        .. code-block:: bash

            $ idem exec aws.apigateway.base_path_mapping.get domain_name="unmanaged_apigateway_base_path_mapping_domain_name" base_path = "unmanaged_apigateway_base_path_mapping"

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.apigateway.base_path_mapping.get
                - kwargs:
                    domain_name: domain_name_of_base_path
                    base_path: value

        .. code-block:: bash

            $ idem exec aws.apigateway.base_path_mapping.get resource_id = "base_path_mapping_unique_id"

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.apigateway.base_path_mapping.get
                - kwargs:
                    resource_id: unique_id_created
    """
    result = dict(comment=[], ret=None, result=True)
    # If resource_id is specified then it overrides any domain_name and base_path provided
    if resource_id:
        domain_name = resource_id.split("/")[0]
        base_path = resource_id.split("/")[1]
    get_base_path_mapping = (
        await hub.exec.boto3.client.apigateway.get_base_path_mapping(
            ctx, domainName=domain_name, basePath=base_path
        )
    )
    if not get_base_path_mapping["result"]:
        if "NotFoundException" in str(get_base_path_mapping["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.apigateway.base_path_mapping", name=domain_name
                )
            )
            result["comment"] += list(get_base_path_mapping["comment"])
            return result
        result["comment"] += list(get_base_path_mapping["comment"])
        result["result"] = False
        return result

    result[
        "ret"
    ] = hub.tool.aws.apigateway.base_path_mapping.convert_raw_base_path_mapping_to_present(
        raw_resource=get_base_path_mapping["ret"],
        domain_name=domain_name,
    )
    return result


async def list_(hub, ctx, domain_name: str):
    """
    Get the list of base path mappings for the given domain name for AWS APIGateway.

    Args:
        domain_name(str):
            The parent domain name of the base_path_mapping resource to be described.

    Returns:
        Dict[str, Any]

    Examples:
        Calling from the CLI:

        .. code-block:: bash

            idem exec aws.apigateway.base_path_mapping.list domain_name="unmanaged_apigateway_base_path_mapping_domain_name"

        Calling this exec module function from within a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.apigateway.base_path_mapping.list
                - kwargs:
                    domain_name: domain_name_of_base_paths
    """
    result = dict(comment=[], ret=[], result=True)
    get_base_path_mappings = (
        await hub.exec.boto3.client.apigateway.get_base_path_mappings(
            ctx, domainName=domain_name
        )
    )
    if not get_base_path_mappings["result"]:
        result["comment"] += list(get_base_path_mappings["comment"])
        result["result"] = False
        return result
    if (
        "NotFoundException" in str(get_base_path_mappings["comment"])
        or get_base_path_mappings["ret"] == {}
        or get_base_path_mappings["ret"]["items"] == []
    ):
        result["comment"].append(
            hub.tool.aws.comment_utils.list_empty_comment(
                resource_type="aws.apigateway.base_path_mapping", name="domain_name"
            )
        )
        return result

    for base_path_map in get_base_path_mappings["ret"]["items"]:
        resource_translated = hub.tool.aws.apigateway.base_path_mapping.convert_raw_base_path_mapping_to_present(
            raw_resource=base_path_map,
            domain_name=domain_name,
        )
        result["ret"].append(resource_translated)
    return result
