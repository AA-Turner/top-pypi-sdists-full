"""Exec module for managing AWS WAFV2 IPSet resources."""
__func_alias__ = {"list_": "list"}


async def get(hub, ctx, name: str, scope: str, resource_id: str):
    """Get an IPSets resource from AWS WAFV2.

    Get a single IPSet from AWS. The function returns None when no resource is found.

    Args:
        name(str):
            This is the name of the IPSet in AWS.

        scope(str):
            Specifies whether this is for an Amazon CloudFront distribution or for a regional application.
            Scope is required to find the resource id for the given IPSet.
            For regional applications, you can use any of the endpoints in the list. A regional application can be an
            Application Load Balancer (ALB), an Amazon API Gateway REST API, an AppSync GraphQL API, or an Amazon
            Cognito user pool. For Amazon CloudFront applications, you must use the API endpoint listed for US East (N. Virginia): us-east-1.

        resource_id(str):
            It is a unique identifier for the ip set in AWS.

    Examples:
        Calling from the CLI:

        .. code-block:: bash

            idem exec aws.wafv2.ip_set.get name= "unmanaged_ipsets" scope="REGIONAL" resource_id="resource_id"

        Calling this exec module function from within a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.wafv2.ip_set.get
                - kwargs:
                    name: unmanaged-resource-name
                    scope: scope-name
                    resource_id: aws-resource-id
    """
    result = dict(comment=[], ret=None, result=True)
    get_response = await hub.exec.boto3.client.wafv2.get_ip_set(
        ctx, Name=name, Scope=scope, Id=resource_id
    )
    if not get_response["result"]:
        if "WAFNonexistentItemException" in str(get_response["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.wafv2.ip_set", name=name
                )
            )
            result["comment"] += list(get_response["comment"])
            return result
        result["result"] = False
        result["comment"] = list(get_response["comment"])
        return result
    response = get_response["ret"]
    arn = response["IPSet"]["ARN"]
    tags_ret = await hub.tool.aws.wafv2.tag.get_tags_for_resource(ctx, resource_arn=arn)
    tags = tags_ret["ret"]
    if not tags_ret["result"]:
        result["result"] = False
        result["comment"] += list(tags_ret["comment"])
        return result
    result["ret"] = hub.tool.aws.wafv2.conversion_utils.convert_raw_ip_set_to_present(
        scope=scope,
        raw_resource=get_response,
        tags=tags,
    )
    return result


async def list_(hub, ctx, scope: str):
    """Get the list of IPSets resources from AWS WAFV2.

    Args:
        scope(str):
            Specifies whether this is for an Amazon CloudFront distribution or for a regional application.
            Scope is required to find the resource id for the given IPSet. For regional applications, you can use any of
            the endpoints in the list. A regional application can be an Application Load Balancer (ALB), an Amazon API
            Gateway REST API, an AppSync GraphQL API, or an Amazon Cognito user pool. For Amazon CloudFront
            applications, you must use the API endpoint listed for US East (N. Virginia): us-east-1.

    Examples:
        Calling from the CLI:

        .. code-block:: bash

            idem exec aws.wafv2.ip_set.list scope="REGIONAL"

        Calling this exec module function from within a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.wafv2.ip_set.list
                - kwargs:
                    scope: scope-name
    """
    result = dict(comment=[], ret=[], result=True)
    ret = await hub.exec.boto3.client.wafv2.list_ip_sets(ctx, Scope=scope)
    if not ret["result"]:
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    if not "IPSets" in ret["ret"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.list_empty_comment(
                resource_type="aws.wafv2.ip_set", name=scope
            )
        )
        return result
    for ipset in ret["ret"]["IPSets"]:
        idem_resource_name = ipset["Name"]
        resource_id = ipset["Id"]
        raw_resource = await hub.exec.aws.wafv2.ip_set.get(
            ctx, name=idem_resource_name, scope=scope, resource_id=resource_id
        )
        if not raw_resource["result"]:
            result["comment"] += list(ret["comment"])
            result["result"] = False
            return result
        result["ret"].append(raw_resource)
    return result
