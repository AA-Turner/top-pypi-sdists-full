import datetime
from typing import Any
from typing import Dict
from typing import List


def sanitize_dict(hub, data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Iterate over a present state and verify that all the options are serializable
    """
    result = {}

    for key, value in data.items():
        if value is None:
            continue
        result[key] = hub.tool.aws.cloudfront.cloudfront_utils.sanitize_value(value)

    return result


def sanitize_list(hub, data: List[Any]) -> List[Any]:
    """
    Iterate over a present state and verify that all the options are serializable
    """
    result = []

    for value in data:
        if value is None:
            continue
        result.append(hub.tool.aws.cloudfront.cloudfront_utils.sanitize_value(value))

    return result


def sanitize_value(hub, data: Any) -> Any:
    """
    Iterate over a present state and verify that all the options are serializable
    """

    if isinstance(data, Dict):
        return hub.tool.aws.cloudfront.cloudfront_utils.sanitize_dict(data)
    elif isinstance(data, datetime.datetime):
        return str(data)
    elif isinstance(data, List):
        return hub.tool.aws.cloudfront.cloudfront_utils.sanitize_list(data)
    else:
        return data


def sanitize_policy_config(hub, original_policy_config: Dict[str, Any]):
    updated_policy_config = {}

    for (
        policy_option_key,
        policy_option_value,
    ) in original_policy_config.items():
        if policy_option_value is not None:
            updated_policy_config[policy_option_key] = policy_option_value

    return updated_policy_config


async def update_cache_policy(
    hub,
    ctx,
    name: str,
    before: Dict[str, Any],
    resource_id: str,
    comment: str,
    default_ttl: int,
    max_ttl: int,
    min_ttl: int,
    parameter_in_cache_key_and_forward_to_origin: Dict[str, Any],
    if_match: str,
):
    result = dict(comment=[], result=True, ret=None)
    # cloudfront cache_policy requires all params to be sent for update call even though one parameter change.
    # we will check if at least one attribute is changed and send the update request if any of the attribute changes.

    update_allowed_params = [
        "comment",
        "name",
        "default_ttl",
        "max_ttl",
        "min_ttl",
        "parameter_in_cache_key_and_forward_to_origin",
    ]

    modified_params = {}
    for parameter in update_allowed_params:
        if (
            locals()[parameter] is not None
            and before.get(parameter) != locals()[parameter]
        ):
            modified_params[parameter] = locals()[parameter]

    if modified_params:
        result["ret"] = modified_params
        if not ctx.get("test", False):
            cache_policy_config = {
                "Comment": comment,
                "Name": name,
                "DefaultTTL": default_ttl,
                "MaxTTL": max_ttl,
                "MinTTL": min_ttl,
                "ParametersInCacheKeyAndForwardedToOrigin": parameter_in_cache_key_and_forward_to_origin,
            }
            # Even though some params are optional in create, most of them are mandatory (at least default values) in
            # update call. Refer
            # https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/cache_policy-overview-required-fields.html
            # we will sanitize the cache_policy config and fill in missing fields with default values.

            cache_policy_config = (
                hub.tool.aws.cloudfront.cloudfront_utils.sanitize_policy_config(
                    cache_policy_config
                )
            )

            ret = await hub.exec.boto3.client.cloudfront.update_cache_policy(
                ctx,
                CachePolicyConfig=cache_policy_config,
                Id=resource_id,
                IfMatch=if_match,
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = ret["comment"]
                return result

    return result


async def update_origin_request_policy(
    hub,
    ctx,
    name: str,
    before: Dict[str, Any],
    resource_id: str,
    comment: str,
    headers_config: Dict[str, Any],
    cookies_config: Dict[str, Any],
    query_strings_config: Dict[str, Any],
    if_match: str,
):
    result = dict(comment=[], result=True, ret=None)
    # cloudfront origin request policy requires all params to be sent for update call even though one parameter change.
    # we will check if at least one attribute is changed and send the update request if any of the attribute changes.

    update_allowed_params = [
        "comment",
        "name",
        "headers_config",
        "cookies_config",
        "query_strings_config",
    ]

    modified_params = {}
    for parameter in update_allowed_params:
        if (
            locals()[parameter] is not None
            and before.get(parameter) != locals()[parameter]
        ):
            modified_params[parameter] = locals()[parameter]

    if modified_params:
        result["ret"] = modified_params
        if not ctx.get("test", False):
            origin_request_policy_config = {
                "Comment": comment,
                "Name": name,
                "HeadersConfig": headers_config,
                "CookiesConfig": cookies_config,
                "QueryStringsConfig": query_strings_config,
            }
            # Even though some params are optional in create, most of them are mandatory (at least default values) in
            # update call. Refer
            # https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/cache_policy-overview-required-fields.html
            # we will sanitize the origin_request config and fill in missing fields with default values.

            origin_request_policy_config = (
                hub.tool.aws.cloudfront.cloudfront_utils.sanitize_policy_config(
                    origin_request_policy_config
                )
            )

            ret = await hub.exec.boto3.client.cloudfront.update_origin_request_policy(
                ctx,
                OriginRequestPolicyConfig=origin_request_policy_config,
                Id=resource_id,
                IfMatch=if_match,
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = ret["comment"]
                return result

    return result
