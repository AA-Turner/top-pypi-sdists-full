"""State module for managing Cloudfront Origin request policies."""
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
    headers_config: make_dataclass(
        "OriginRequestPolicyHeadersConfig",
        [
            ("HeaderBehavior", str),
            (
                "Headers",
                make_dataclass(
                    "Headers",
                    [("Quantity", int), ("Items", List[str], field(default=None))],
                ),
                field(default=None),
            ),
        ],
    ) = None,
    cookies_config: make_dataclass(
        "OriginRequestPolicyCookiesConfig",
        [
            ("CookieBehavior", str),
            (
                "Cookies",
                make_dataclass(
                    "CookieNames",
                    [("Quantity", int), ("Items", List[str], field(default=None))],
                ),
                field(default=None),
            ),
        ],
    ) = None,
    query_strings_config: make_dataclass(
        "OriginRequestPolicyQueryStringsConfig",
        [
            ("QueryStringBehavior", str),
            (
                "QueryStrings",
                make_dataclass(
                    "QueryStringNames",
                    [("Quantity", int), ("Items", List[str], field(default=None))],
                ),
                field(default=None),
            ),
        ],
    ) = None,
    comment: str = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Creates an origin request policy.

    After you create an origin request policy, you can attach it to one or morecache behaviors. When it’s attached to a
    cache behavior, the origin request policy determines the values th includes the following: The request body and the
    URL path (without the domain name) from the viewer request.

    The headers that CloudFront automatically includes in every origin request, including Host, User-Agent, and
    X-Amz-Cf-Id.   All HTTP headers, cookies, and URL query strings that are specified in the cache policy or the
    origin request policy. These can include items from the viewer request and, in the case of headers, additional
    ones that are added by CloudFront.   CloudFront sends a request when it can’t find a valid object in its cache
    that matches the request. If you want to send values to the origin and also include them in the cache key, use
    CachePolicy. For more information about origin request policies, see Controlling origin requests in the Amazon
    CloudFront Developer Guide.

    Args:
        name(str):
            An Idem name of the resource.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

        comment (str, Optional):
            A comment to describe the origin request policy. The comment cannot be longer than 128
            characters.

        headers_config (dict):
            The HTTP headers to include in origin requests. These can include headers from viewer requests
            and additional headers added by CloudFront.

            * HeaderBehavior (str):
                Determines whether any HTTP headers are included in requests that CloudFront sends to the
                origin. Valid values are:    none – HTTP headers are not included in requests that CloudFront
                sends to the origin. Even when this field is set to none, any headers that are listed in a
                CachePolicy are included in origin requests.    whitelist – The HTTP headers that are listed in
                the Headers type are included in requests that CloudFront sends to the origin.    allViewer –
                All HTTP headers in viewer requests are included in requests that CloudFront sends to the
                origin.    allViewerAndWhitelistCloudFront – All HTTP headers in viewer requests and the
                additional CloudFront headers that are listed in the Headers type are included in requests that
                CloudFront sends to the origin. The additional headers are added by CloudFront.

                * Headers (Dict[str, Any], Optional):
                    Contains a list of HTTP header names.
                    * Quantity (int): The number of header names in the Items list.
                    * Items (list[str], Optional): A list of HTTP header names.

        cookies_config (dict):
            The cookies from viewer requests to include in origin requests.

            * CookieBehavior (str):
                Determines whether cookies in viewer requests are included in requests that CloudFront sends to
                the origin. Valid values are:    none – Cookies in viewer requests are not included in requests
                that CloudFront sends to the origin. Even when this field is set to none, any cookies that are
                listed in a CachePolicy are included in origin requests.    whitelist – The cookies in viewer
                requests that are listed in the CookieNames type are included in requests that CloudFront sends
                to the origin.    all – All cookies in viewer requests are included in requests that CloudFront
                sends to the origin.

                * Cookies (Dict[str, Any], Optional):
                    Contains a list of cookie names.
                    * Quantity (int): The number of cookie names in the Items list.
                    * Items (list[str], Optional): A list of cookie names.

        query_strings_config (dict):
            The URL query strings from viewer requests to include in origin requests.

            * QueryStringBehavior (str):
                Determines whether any URL query strings in viewer requests are included in requests that
                CloudFront sends to the origin. Valid values are:    none – Query strings in viewer requests are
                not included in requests that CloudFront sends to the origin. Even when this field is set to
                none, any query strings that are listed in a CachePolicy are included in origin requests.
                whitelist – The query strings in viewer requests that are listed in the QueryStringNames type
                are included in requests that CloudFront sends to the origin.    all – All query strings in
                viewer requests are included in requests that CloudFront sends to the origin.

                * QueryStrings (Dict[str, Any], Optional):
                    Contains a list of the query strings in viewer requests that are included in requests that CloudFront sends to the origin.
                    * Quantity (int): The number of query string names in the Items list.
                    * Items (list[str], Optional): A list of query string names.

    Request Syntax:

        .. code-block:: sls

            resource_is_present:
              aws.cloudfront.origin_request_policy.present:
                - name: "string"
                - comment: "string"
                - headers_config:
                    HeaderBehavior: "dict"
                - cookies_config:
                    CookieBehavior: "dict"
                - query_strings_config:
                    QueryStringBehavior: "dict"

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: sls

            resource_is_present:
              aws.cloudfront.origin_request_policy.present:
                - name: value
                - comment: value
                - headers_config:
                    HeaderBehavior: none
                - cookies_config:
                    CookieBehavior: none
                - query_strings_config:
                    QueryStringBehavior: none
    """

    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    before = None
    resource_updated = False
    if resource_id:
        before = await hub.exec.aws.cloudfront.origin_request_policy.get(
            ctx, name=name, resource_id=resource_id
        )
        if not before["result"] or not before["ret"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result
        result["old_state"] = copy.deepcopy(before["ret"])
        plan_state = copy.deepcopy(result["old_state"])

        # check update
        update_ret = (
            await hub.tool.aws.cloudfront.cloudfront_utils.update_origin_request_policy(
                ctx=ctx,
                name=name,
                before=result["old_state"],
                resource_id=resource_id,
                comment=comment,
                headers_config=headers_config,
                cookies_config=cookies_config,
                query_strings_config=query_strings_config,
                if_match=before["ret"].get("etag"),
            )
        )
        result["comment"] = update_ret["comment"]
        result["result"] = update_ret["result"]
        resource_updated = bool(update_ret["ret"])
        if update_ret["ret"]:
            if ctx.get("test", False):
                for modified_param in update_ret["ret"]:
                    plan_state[modified_param] = update_ret["ret"][modified_param]
                result["comment"] += hub.tool.aws.comment_utils.would_update_comment(
                    resource_type="aws.cloudfront.origin_request_policy", name=name
                )
            else:
                result["comment"] += hub.tool.aws.comment_utils.update_comment(
                    resource_type="aws.cloudfront.origin_request_policy", name=name
                )

    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "comment": comment,
                    "headers_config": headers_config,
                    "cookies_config": cookies_config,
                    "query_strings_config": query_strings_config,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.cloudfront.origin_request_policy", name=name
            )
            return result

        origin_request_policy_config = {
            "Comment": comment,
            "Name": name,
            "HeadersConfig": headers_config,
            "CookiesConfig": cookies_config,
            "QueryStringsConfig": query_strings_config,
        }
        origin_request_policy_config = (
            hub.tool.aws.cloudfront.cloudfront_utils.sanitize_policy_config(
                origin_request_policy_config
            )
        )
        ret = await hub.exec.boto3.client.cloudfront.create_origin_request_policy(
            ctx, OriginRequestPolicyConfig=origin_request_policy_config
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.cloudfront.origin_request_policy", name=name
        )
        resource_id = ret["ret"]["OriginRequestPolicy"]["Id"]

    if ctx.get("test", False):
        result["new_state"] = plan_state
    elif (not before) or resource_updated:
        after = await hub.exec.aws.cloudfront.origin_request_policy.get(
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
    """Deletes an origin request policy.

    You cannot delete an origin request policy if it’s attached to any cache behaviors. First update your distributions
    to remove the origin request policy from all cache behaviors, then delete the origin request policy. To delete an
    origin request policy, you must provide the policy’s identifier and version.

    Args:
        name(str):
            An Idem name of the resource.

        resource_id(str):
            An identifier of the resource in the provider.

    Request Syntax:

        .. code-block:: sls

            resource_is_absent:
              aws_auto.cloudfront.origin_request_policy.absent:
                - name: "string"
                - resource_id: "string"

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: sls

            resource_is_absent:
              aws_auto.cloudfront.origin_request_policy.absent:
                - name: value
                - resource_id: value
    """

    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.cloudfront.origin_request_policy", name=name
        )
        return result

    before = await hub.exec.aws.cloudfront.origin_request_policy.get(
        ctx, name=name, resource_id=resource_id
    )

    if not before["result"]:
        result["result"] = False
        result["comment"] = before["comment"]
        return result

    if not before["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.cloudfront.origin_request_policy", name=name
        )

    elif ctx.get("test", False):
        result["old_state"] = before["ret"]
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.cloudfront.origin_request_policy", name=name
        )
        return result
    else:
        result["old_state"] = before["ret"]

        ret = await hub.exec.boto3.client.cloudfront.delete_origin_request_policy(
            ctx, Id=resource_id, IfMatch=before["ret"]["etag"]
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            result["result"] = False
            return result

        result["comment"] = hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.cloudfront.origin_request_policy", name=name
        )

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """
    Describe the resource in a way that can be recreated/managed with the corresponding "present" function

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: bash

            $ idem describe aws_auto.cloudfront.origin_request_policy
    """

    result = {}

    ret = await hub.exec.aws.cloudfront.origin_request_policy.list(ctx)
    if not ret["result"]:
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result

    for policy in ret["ret"]:
        resource_id = policy.get("resource_id")

        result[resource_id] = {
            "aws.cloudfront.origin_request_policy.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in policy.items()
            ]
        }

    return result
