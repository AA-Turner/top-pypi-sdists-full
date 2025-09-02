from typing import Any
from typing import Dict

__func_alias__ = {"list_": "list"}


async def get(hub, ctx, name: str, resource_id: str, scope: str) -> Dict[str, Any]:
    """Function for getting the wafv2 regular expression pattern set with name, Id and scope

    Returns the state of a wafv2 regular expression pattern set

    Args:
        name(str): The name of the regex pattern set.
        resource_id(str): An identifier of the resource in the provider. Defaults to None.
        scope(str): Specifies whether this is for an Amazon CloudFront distribution or for a regional application. A
            regional application can be an Application Load Balancer (ALB), an Amazon API Gateway REST API,
            or an AppSync GraphQL API.  To work with CloudFront, you must also specify the Region US East
            (N. Virginia) as follows:    CLI - Specify the Region when you use the CloudFront scope:
            --scope=CLOUDFRONT --region=us-east-1.    API and SDKs - For all calls, use the Region endpoint
            us-east-1.

    Returns
        Dict[bool, list, dict or None]:

        result(bool):
            Whether the result of the function has been successful (``True``) or not (``False``).
        comment(list):
            A list of messages.
        ret(dict or None):
           The WAFV2 regular expression pattern set in "present" format.

    Examples:
        Calling this exec module function from the cli:

        .. code-block:: bash

            idem exec aws.wafv2.regex_pattern_set.get name="idem_name" resource_id="resource_id" scope="REGIONAL"

        Calling this exec module function from within a state module in pure python:

        .. code-block:: python

            async def state_function(hub, ctx, name, resource_id, **kwargs):
                ret = await hub.exec.aws.wafv2.regex_pattern_set.get(
                    ctx, name=name, resource_id=resource_id, scope="REGIONAL"
                )
    """
    result = dict(ret=None, comment=[], result=True)
    is_invalid_scope_and_region = (
        hub.tool.aws.wafv2.regex_pattern_set.check_if_invalid_scope_and_region(
            ctx["acct"].get("region_name"), scope
        )
    )
    if is_invalid_scope_and_region:
        result["result"] = False
        result["comment"].append(is_invalid_scope_and_region)
        return result
    ret = await hub.exec.boto3.client.wafv2.get_regex_pattern_set(
        ctx=ctx, Name=name, Scope=scope, Id=resource_id
    )
    if not ret["result"]:
        if "WAFNonexistentItemException" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.wafv2.regex_pattern_set", name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    if not ret["ret"]["RegexPatternSet"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.wafv2.regex_pattern_set", name=name
            )
        )
        return result

    resource = ret["ret"]["RegexPatternSet"]
    tags = []
    ret_tag = await hub.exec.boto3.client.wafv2.list_tags_for_resource(
        ctx, ResourceARN=resource["ARN"]
    )
    if not ret_tag["result"]:
        result["result"] = False
        result["comment"] = list(ret_tag["comment"])
        return result
    if (
        ret_tag["ret"]
        and ret_tag["ret"]["TagInfoForResource"]
        and ret_tag["ret"]["TagInfoForResource"].get("TagList")
    ):
        tags = ret_tag["ret"]["TagInfoForResource"].get("TagList")

    result[
        "ret"
    ] = hub.tool.aws.wafv2.conversion_utils.convert_raw_regex_pattern_set_to_present(
        ctx,
        raw_resource=resource,
        scope=scope,
        tags=hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags),
    )
    result["ret"]["LockToken"] = ret["ret"]["LockToken"]
    return result


async def list_(hub, ctx, name: str, scope: str) -> Dict:
    """Fetch a list of WAFV2 regex pattern sets

    Args:
        name(str): The name of the Idem state.
        scope(str): Specifies whether this is for an Amazon CloudFront distribution or for a regional application. A
            regional application can be an Application Load Balancer (ALB), an Amazon API Gateway REST API,
            or an AppSync GraphQL API.  To work with CloudFront, you must also specify the Region US East
            (N. Virginia) as follows:    CLI - Specify the Region when you use the CloudFront scope:
            --scope=CLOUDFRONT --region=us-east-1.    API and SDKs - For all calls, use the Region endpoint
            us-east-1.

    Returns
        Dict[bool, list, dict or None]:

        result(bool):
            Whether the result of the function has been successful (``True``) or not (``False``).
        comment(list):
            A list of messages.
        ret(list or None):
           List of WAFV2 regular expression pattern sets in "present" format.

    Examples:
        Calling this exec module function from the cli:

        .. code-block:: bash

            idem exec aws.wafv2.regex_pattern_set.list scope="REGIONAL"

        Calling this exec module function from within a state module in pure python:

        .. code-block:: python

            async def state_function(hub, ctx, name, resource_id, **kwargs):
                ret = await hub.exec.aws.wafv2.regex_pattern_set.list(
                    ctx, scope="REGIONAL"
                )

    """
    result = dict(ret=[], comment=[], result=True)
    is_invalid_scope_and_region = (
        hub.tool.aws.wafv2.regex_pattern_set.check_if_invalid_scope_and_region(
            ctx["acct"].get("region_name"), scope
        )
    )
    if is_invalid_scope_and_region:
        result["result"] = False
        result["comment"].append(is_invalid_scope_and_region)
        return result

    ret = await hub.exec.boto3.client.wafv2.list_regex_pattern_sets(
        ctx=ctx, Scope=scope
    )
    if not ret["result"]:
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    if not ret["ret"]["RegexPatternSets"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.list_empty_comment(
                resource_type="aws.wafv2.regex_pattern_set", name=name
            )
        )
        return result
    for regex_pattern_set in ret["ret"]["RegexPatternSets"]:
        get_regex_ret = await hub.exec.aws.wafv2.regex_pattern_set.get(
            ctx=ctx,
            name=regex_pattern_set["Name"],
            resource_id=regex_pattern_set["Id"],
            scope=scope,
        )
        if not get_regex_ret["result"]:
            result["comment"] += list(get_regex_ret["comment"])
            result["result"] = False
            return result
        result["ret"].append(get_regex_ret["ret"])
    return result
