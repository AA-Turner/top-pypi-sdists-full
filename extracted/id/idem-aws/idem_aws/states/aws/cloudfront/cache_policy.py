"""State module for managing Cloudfront Cache policies."""
import copy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    default_ttl: int,
    max_ttl: int,
    min_ttl: int,
    parameter_in_cache_key_and_forward_to_origin: make_dataclass(
        "ParametersInCacheKeyAndForwardedToOrigin",
        [
            ("EnableAcceptEncodingGzip", bool),
            (
                "HeadersConfig",
                make_dataclass(
                    "CachePolicyHeadersConfig",
                    [
                        ("HeaderBehavior", str),
                        (
                            "Headers",
                            make_dataclass(
                                "Headers",
                                [
                                    ("Quantity", int),
                                    ("Items", List[str], field(default=None)),
                                ],
                            ),
                            field(default=None),
                        ),
                    ],
                ),
            ),
            (
                "CookiesConfig",
                make_dataclass(
                    "CachePolicyCookiesConfig",
                    [
                        ("CookieBehavior", str),
                        (
                            "Cookies",
                            make_dataclass(
                                "CookieNames",
                                [
                                    ("Quantity", int),
                                    ("Items", List[str], field(default=None)),
                                ],
                            ),
                            field(default=None),
                        ),
                    ],
                ),
            ),
            (
                "QueryStringsConfig",
                make_dataclass(
                    "CachePolicyQueryStringsConfig",
                    [
                        ("QueryStringBehavior", str),
                        (
                            "QueryStrings",
                            make_dataclass(
                                "QueryStringNames",
                                [
                                    ("Quantity", int),
                                    ("Items", List[str], field(default=None)),
                                ],
                            ),
                            field(default=None),
                        ),
                    ],
                ),
            ),
            ("EnableAcceptEncodingBrotli", bool, field(default=None)),
        ],
    ) = None,
    comment: str = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Creates a cache policy.

    After you create a cache policy, you can attach it to one or more cache behaviors. When
    it’s attached to a cache behavior, the cache policy determines the following:   The values that CloudFront
    includes in the cache key. These values can include HTTP headers, cookies, and URL query strings. CloudFront
    uses the cache key to find an object in its cache that it can return to the viewer.   The default, minimum, and
    maximum time to live (TTL) values that you want objects to stay in the CloudFront cache.   The headers, cookies,
    and query strings that are included in the cache key are automatically included in requests that CloudFront
    sends to the origin. CloudFront sends a request when it can’t find an object in its cache that matches the
    request’s cache key. If you want to send values to the origin but not include them in the cache key, use
    OriginRequestPolicy. For more information about cache policies, see Controlling the cache key in the Amazon
    CloudFront Developer Guide.

    Args:
        name(str):
            An Idem name of the resource.

        resource_id(str, optional):
            An identifier of the resource in the provider. Defaults to None.

        cache_policy_config(dict[str, Any]):
            A cache policy configuration.

        comment (str, optional):
            A comment to describe the cache policy. The comment cannot be longer than 128 characters.

        default_ttl (int, optional):
            The default amount of time, in seconds, that you want objects to stay in the CloudFront cache
            before CloudFront sends another request to the origin to see if the object has been updated.
            CloudFront uses this value as the object’s time to live (TTL) only when the origin does not send
            Cache-Control or Expires headers with the object. For more information, see Managing How Long
            Content Stays in an Edge Cache (Expiration) in the Amazon CloudFront Developer Guide. The
            default value for this field is 86400 seconds (one day). If the value of MinTTL is more than
            86400 seconds, then the default value for this field is the same as the value of MinTTL.

        max_ttl (int, optional):
            The maximum amount of time, in seconds, that objects stay in the CloudFront cache before
            CloudFront sends another request to the origin to see if the object has been updated. CloudFront
            uses this value only when the origin sends Cache-Control or Expires headers with the object. For
            more information, see Managing How Long Content Stays in an Edge Cache (Expiration) in the
            Amazon CloudFront Developer Guide. The default value for this field is 31536000 seconds (one
            year). If the value of MinTTL or DefaultTTL is more than 31536000 seconds, then the default
            value for this field is the same as the value of DefaultTTL.

        min_ttl (int):
            The minimum amount of time, in seconds, that you want objects to stay in the CloudFront cache
            before CloudFront sends another request to the origin to see if the object has been updated. For
            more information, see Managing How Long Content Stays in an Edge Cache (Expiration) in the
            Amazon CloudFront Developer Guide.

        parameter_in_cache_key_and_forward_to_origin (Dict[str, Any], optional):
            The HTTP headers, cookies, and URL query strings to include in the cache key. The values
            included in the cache key are automatically included in requests that CloudFront sends to the
            origin.

            * EnableAcceptEncodingGzip (bool):
                A flag that can affect whether the Accept-Encoding HTTP header is
                included in the cache key and included in requests that CloudFront sends to the origin. This field is
                related to the EnableAcceptEncodingBrotli field. If one or both of these fields is true and the viewer
                request includes the Accept-Encoding header, then CloudFront does the following:
                Normalizes the value of the viewer’s Accept-Encoding header   Includes the normalized header in the
                cache key Includes the normalized header in the request to the origin, if a request is necessary.
                For more information, see Compression support in the Amazon CloudFront Developer Guide. If you set
                this value to true, and this cache behavior also has an origin request policy attached, do not
                include the Accept-Encoding header in the origin request policy. CloudFront always includes the
                Accept-Encoding header in origin requests when the value of this field is true, so including
                this header in an origin request policy has no effect. If both of these fields are false, then
                CloudFront treats the Accept-Encoding header the same as any other HTTP header in the viewer
                request. By default, it’s not included in the cache key and it’s not included in origin
                requests. In this case, you can manually add Accept-Encoding to the headers whitelist like any
                other HTTP header.

            * EnableAcceptEncodingBrotli (bool, optional):
                A flag that can affect whether the Accept-Encoding HTTP header is included in the cache key and
                included in requests that CloudFront sends to the origin. This field is related to the
                EnableAcceptEncodingGzip field. If one or both of these fields is true and the viewer request
                includes the Accept-Encoding header, then CloudFront does the following:   Normalizes the value
                of the viewer’s Accept-Encoding header   Includes the normalized header in the cache key
                Includes the normalized header in the request to the origin, if a request is necessary   For
                more information, see Compression support in the Amazon CloudFront Developer Guide. If you set
                this value to true, and this cache behavior also has an origin request policy attached, do not
                include the Accept-Encoding header in the origin request policy. CloudFront always includes the
                Accept-Encoding header in origin requests when the value of this field is true, so including
                this header in an origin request policy has no effect. If both of these fields are false, then
                CloudFront treats the Accept-Encoding header the same as any other HTTP header in the viewer
                request. By default, it’s not included in the cache key and it’s not included in origin
                requests. In this case, you can manually add Accept-Encoding to the headers whitelist like any
                other HTTP header.

            * HeadersConfig (Dict[str, Any]):
                An object that determines whether any HTTP headers (and if so, which headers) are included in
                the cache key and automatically included in requests that CloudFront sends to the origin.

                * HeaderBehavior (str):
                    Determines whether any HTTP headers are included in the cache key and automatically
                    included in requests that CloudFront sends to the origin. Valid values are:    none – HTTP headers are not
                    included in the cache key and are not automatically included in requests that CloudFront sends to the
                    origin. Even when this field is set to none, any headers that are listed in an OriginRequestPolicy
                    are included in origin requests.    whitelist – The HTTP headers that are listed in the Headers type
                    are included in the cache key and are automatically included in requests that CloudFront sends to the
                    origin.

                    * Headers (Dict[str, Any], optional): Contains a list of HTTP header names.
                        * Quantity (int): The number of header names in the Items list.
                        * Items (list[str], optional): A list of HTTP header names.

            * CookiesConfig (Dict[str, Any]):
                An object that determines whether any cookies in viewer requests (and if so, which cookies) are
                included in the cache key and automatically included in requests that CloudFront sends to the
                origin.

                * CookieBehavior (str):
                    Determines whether any cookies in viewer requests are included in the cache key and
                    automatically included in requests that CloudFront sends to the origin. Valid values are:
                    none – Cookies in viewer requests are not included in the cache key and are not automatically
                    included in requests that CloudFront sends to the origin. Even when this field is set to none,
                    any cookies that are listed in an OriginRequestPolicy are included in origin requests.
                    whitelist – The cookies in viewer requests that are listed in the CookieNames type are included
                    in the cache key and automatically included in requests that CloudFront sends to the origin.
                    allExcept – All cookies in viewer requests that are  not  listed in the CookieNames type are
                    included in the cache key and automatically included in requests that CloudFront sends to the
                    origin.    all – All cookies in viewer requests are included in the cache key and are
                    automatically included in requests that CloudFront sends to the origin.

                    * Cookies (Dict[str, Any], optional):
                        Contains a list of cookie names.
                        * Quantity (int): The number of cookie names in the Items list.
                        * Items (list[str], optional): A list of cookie names.

            * QueryStringsConfig (Dict[str, Any]):
                An object that determines whether any URL query strings in viewer requests (and if so, which
                query strings) are included in the cache key and automatically included in requests that
                CloudFront sends to the origin.

                * QueryStringBehavior (str):
                    Determines whether any URL query strings in viewer requests are included in the cache key and
                    automatically included in requests that CloudFront sends to the origin. Valid values are:
                    none – Query strings in viewer requests are not included in the cache key and are not
                    automatically included in requests that CloudFront sends to the origin. Even when this field is
                    set to none, any query strings that are listed in an OriginRequestPolicy are included in origin
                    requests.    whitelist – The query strings in viewer requests that are listed in the
                    QueryStringNames type are included in the cache key and automatically included in requests that
                    CloudFront sends to the origin.    allExcept – All query strings in viewer requests that are
                    not  listed in the QueryStringNames type are included in the cache key and automatically
                    included in requests that CloudFront sends to the origin.    all – All query strings in viewer
                    requests are included in the cache key and are automatically included in requests that
                    CloudFront sends to the origin.

                    * QueryStrings (Dict[str, Any], optional):
                        Contains the specific query strings in viewer requests that either  are  or  are not  included
                        in the cache key and automatically included in requests that CloudFront sends to the origin. The
                        behavior depends on whether the QueryStringBehavior field in the CachePolicyQueryStringsConfig
                        type is set to whitelist (the listed query strings  are  included) or allExcept (the listed
                        query strings  are not  included, but all other query strings are).

                        * Quantity (int): The number of query string names in the Items list.
                        * Items (list[str], optional): A list of query string names.

    Request Syntax:

        .. code-block:: sls

            resource_is_present:
              aws_auto.cloudfront.cache_policy.present:
                - name: "string"
                - comment: "string"
                - default_ttl: "int"
                - max_ttl: "int"
                - min_ttl: "int"
                - parameter_in_cache_key_and_forward_to_origin:
                    CookiesConfig:
                      CookieBehavior: "string"
                    EnableAcceptEncodingBrotli: "bool"
                    EnableAcceptEncodingGzip: "bool"
                    HeadersConfig:
                      HeaderBehavior: "string"
                    QueryStringsConfig:
                      QueryStringBehavior: "string"
                - etag: "string"

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: sls

            resource_is_present:
              aws_auto.cloudfront.cache_policy.present:
                - name: value
                - comment: idem test
                - default_ttl: 86400
                - max_ttl: 31536000
                - min_ttl: 1
                - parameter_in_cache_key_and_forward_to_origin:
                    CookiesConfig:
                      CookieBehavior: none
                    EnableAcceptEncodingBrotli: true
                    EnableAcceptEncodingGzip: true
                    HeadersConfig:
                      HeaderBehavior: none
                    QueryStringsConfig:
                      QueryStringBehavior: none
                - etag: E23ZP02F085DFQ
    """

    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    before = None
    resource_updated = False
    if resource_id:
        before = await hub.exec.aws.cloudfront.cache_policy.get(
            ctx, name=name, resource_id=resource_id
        )
        if not before["result"] or not before["ret"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result
        result["old_state"] = copy.deepcopy(before["ret"])
        plan_state = copy.deepcopy(result["old_state"])

        # check update
        update_ret = await hub.tool.aws.cloudfront.cloudfront_utils.update_cache_policy(
            ctx=ctx,
            name=name,
            before=result["old_state"],
            resource_id=resource_id,
            comment=comment,
            default_ttl=default_ttl,
            max_ttl=max_ttl,
            min_ttl=min_ttl,
            parameter_in_cache_key_and_forward_to_origin=parameter_in_cache_key_and_forward_to_origin,
            if_match=before["ret"].get("etag"),
        )
        result["comment"] = update_ret["comment"]
        result["result"] = update_ret["result"]
        resource_updated = bool(update_ret["ret"])
        if update_ret["ret"]:
            if ctx.get("test", False):
                for modified_param in update_ret["ret"]:
                    plan_state[modified_param] = update_ret["ret"][modified_param]
                result["comment"] += hub.tool.aws.comment_utils.would_update_comment(
                    resource_type="aws.cloudfront.cache_policy", name=name
                )
            else:
                result["comment"] += hub.tool.aws.comment_utils.update_comment(
                    resource_type="aws.cloudfront.cache_policy", name=name
                )

    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "comment": comment,
                    "default_ttl": default_ttl,
                    "max_ttl": max_ttl,
                    "min_ttl": min_ttl,
                    "parameter_in_cache_key_and_forward_to_origin": parameter_in_cache_key_and_forward_to_origin,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.cloudfront.cache_policy", name=name
            )
            return result

        cache_policy_config = {
            "Comment": comment,
            "Name": name,
            "DefaultTTL": default_ttl,
            "MaxTTL": max_ttl,
            "MinTTL": min_ttl,
            "ParametersInCacheKeyAndForwardedToOrigin": parameter_in_cache_key_and_forward_to_origin,
        }
        cache_policy_config = (
            hub.tool.aws.cloudfront.cloudfront_utils.sanitize_policy_config(
                cache_policy_config
            )
        )
        ret = await hub.exec.boto3.client.cloudfront.create_cache_policy(
            ctx, CachePolicyConfig=cache_policy_config
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.cloudfront.cache_policy", name=name
        )
        resource_id = ret["ret"]["CachePolicy"]["Id"]

    if ctx.get("test", False):
        result["new_state"] = plan_state
    elif (not before) or resource_updated:
        after = await hub.exec.aws.cloudfront.cache_policy.get(
            ctx, name=name, resource_id=resource_id
        )
        if not after["result"]:
            result["result"] = False
            result["comment"] = after["comment"]
            return result
        result["new_state"] = copy.deepcopy(after["ret"])
    else:
        result["new_state"] = copy.deepcopy(result["old_state"])

    return result


async def absent(hub, ctx, name: str, resource_id: str = None) -> Dict[str, Any]:
    """
    Deletes a cache policy.

    You cannot delete a cache policy if it’s attached to a cache behavior. First update your distributions to remove the
    cache policy from all cache behaviors, then delete the cache policy. To delete a cache policy, you must provide the
    policy’s identifier and version.

    Args:
        name(str):
            An Idem name of the resource.

        resource_id(str, Optional):
            An identifier of the resource in the provider.

    Request Syntax:

        .. code-block:: sls

            resource_is_absent:
              aws_auto.cloudfront.cache_policy.absent:
                - name: "string"
                - resource_id: "string"

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: sls

            resource_is_absent:
              aws_auto.cloudfront.cache_policy.absent:
                - name: value
                - resource_id: value
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.cloudfront.cache_policy", name=name
        )
        return result

    before = await hub.exec.aws.cloudfront.cache_policy.get(
        ctx, name=name, resource_id=resource_id
    )

    if not before["result"]:
        result["result"] = False
        result["comment"] = before["comment"]
        return result

    if not before["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.cloudfront.cache_policy", name=name
        )

    elif ctx.get("test", False):
        result["old_state"] = before["ret"]
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.cloudfront.cache_policy", name=name
        )
        return result
    else:
        result["old_state"] = before["ret"]

        ret = await hub.exec.boto3.client.cloudfront.delete_cache_policy(
            ctx, Id=resource_id, IfMatch=before["ret"]["etag"]
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            result["result"] = False
            return result

        result["comment"] = hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.cloudfront.cache_policy", name=name
        )

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """
    Describe the resource in a way that can be recreated/managed with the corresponding "present" function

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: bash

            $ idem describe aws_auto.cloudfront.cache_policy
    """
    result = {}

    ret = await hub.exec.aws.cloudfront.cache_policy.list(ctx)
    if not ret["result"]:
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result

    for policy in ret["ret"]:
        resource_id = policy.get("resource_id")

        result[resource_id] = {
            "aws.cloudfront.cache_policy.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in policy.items()
            ]
        }

    return result
