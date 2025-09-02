from typing import Any
from typing import Dict
from typing import List

from dict_tools import data


async def update_distribution(
    hub,
    ctx,
    name: str,
    before: Dict[str, Any],
    resource_id: str,
    caller_reference: str,
    origins: Dict,
    default_cache_behaviour: Dict[str, Any],
    comment: str,
    logging: Dict[str, Any],
    enabled: str,
    viewer_certificate: str,
    aliases: Dict,
    price_class: str,
    default_root_object: str,
    origin_groups: Dict[str, Any],
    cache_behaviors: Dict[str, Any],
    custom_error_responses: Dict[str, Any],
    restrictions: Dict[str, Any],
    web_acl_id: str,
    http_version: str,
    is_ipv6_enabled: bool,
    if_match: str,
    timeout: Dict[str, Any],
):
    result = dict(comment=[], result=True, ret=None)
    # cloudfront distribution requires all params to be sent for update call even though one parameter change.
    # we will check if at least one attribute is changed and send the update request if any of the attribute changes.

    update_allowed_params = [
        "origins",
        "default_cache_behaviour",
        "comment",
        "logging",
        "enabled",
        "viewer_certificate",
        "aliases",
        "price_class",
        "default_root_object",
        "origin_groups",
        "cache_behaviors",
        "custom_error_responses",
        "restrictions",
        "web_acl_id",
        "http_version",
        "is_ipv6_enabled",
    ]

    modified_params = {}
    for parameter in update_allowed_params:
        if locals()[parameter] is not None:
            if isinstance(locals()[parameter], List) or isinstance(
                locals()[parameter], Dict
            ):
                if data.recursive_diff(
                    before.get(parameter),
                    locals()[parameter],
                    ignore_order=True,
                    ignore_missing_keys=True,
                ):
                    modified_params[parameter] = locals()[parameter]
            elif before.get(parameter) != locals()[parameter]:
                modified_params[parameter] = locals()[parameter]

    if modified_params:
        result["ret"] = modified_params
        if not ctx.get("test", False):
            distribution_config = {
                "CallerReference": caller_reference,
                "Origins": origins,
                "DefaultCacheBehavior": default_cache_behaviour,
                "Comment": comment,
                "Logging": logging,
                "Enabled": enabled,
                "ViewerCertificate": viewer_certificate,
                "Aliases": aliases,
                "PriceClass": price_class,
                "DefaultRootObject": default_root_object,
                "OriginGroups": origin_groups,
                "CacheBehaviors": cache_behaviors,
                "CustomErrorResponses": custom_error_responses,
                "Restrictions": restrictions,
                "WebACLId": web_acl_id,
                "HttpVersion": http_version,
                "IsIPV6Enabled": is_ipv6_enabled,
            }
            # Even though some params are optional in create, most of them are mandatory (at least default values) in
            # update call. Refer
            # https://docs.aws.amazon.com/AmazonCloudFront/latest/DeveloperGuide/distribution-overview-required-fields.html
            # we will sanitize the distribution config and fill in missing fields with default values.

            distribution_config = hub.tool.aws.cloudfront.distribution_utils.sanitize_distribution_config_for_update(
                distribution_config
            )

            ret = await hub.exec.boto3.client.cloudfront.update_distribution(
                ctx,
                DistributionConfig=distribution_config,
                Id=resource_id,
                IfMatch=if_match,
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = ret["comment"]
                return result

            waiter_ret = await hub.tool.aws.cloudfront.distribution.distribution_waiter(
                ctx, name, resource_id, timeout, "update"
            )
            if not waiter_ret["result"]:
                result["result"] = False
                result["comment"] += waiter_ret["comment"]
            result["comment"] = hub.tool.aws.comment_utils.update_comment(
                resource_type="aws.cloudfront.distribution", name=name
            )
    return result


async def disable_distribution(
    hub,
    ctx,
    name: str,
    resource_id: str,
    before: Dict[str, Any],
    if_match: str,
    timeout: Dict[str, Any],
):
    return await hub.tool.aws.cloudfront.distribution.update_distribution(
        ctx=ctx,
        name=name,
        before=before,
        resource_id=resource_id,
        caller_reference=before.get("caller_reference"),
        origins=before.get("origins"),
        default_cache_behaviour=before.get("default_cache_behaviour"),
        comment=before.get("comment"),
        logging=before.get("logging"),
        enabled=False,
        viewer_certificate=before.get("viewer_certificate"),
        aliases=before.get("aliases"),
        price_class=before.get("price_class"),
        default_root_object=before.get("default_root_object"),
        origin_groups=before.get("origin_groups"),
        cache_behaviors=before.get("cache_behaviors"),
        custom_error_responses=before.get("custom_error_responses"),
        restrictions=before.get("restrictions"),
        web_acl_id=before.get("web_acl_id"),
        http_version=before.get("http_version"),
        is_ipv6_enabled=before.get("is_ipv6_enabled"),
        if_match=if_match,
        timeout=timeout,
    )


async def distribution_waiter(
    hub, ctx, name: str, resource_id: str, timeout: Dict, operation_type: str
):
    """

    Waiter to wait for the distribution to become active.

        Args:
           hub:
           ctx:
           name(str): An Idem name of the resource.
           resource_id(str): Id of the distribution to Identify the resource
           timeout(Dict, Optional): Timeout configuration for creating or updating distribution.
            * create (Dict) -- Timeout configuration for creating distribution
                * delay(int, default=60) -- The amount of time in seconds to wait between attempts.
                * max_attempts(int, default=40) -- Customized timeout configuration containing delay and max attempts.
            * update (str) -- Timeout configuration for updating distribution
                * delay(int, default=60) -- The amount of time in seconds to wait between attempts.
                * max_attempts(int, default=40) -- Customized timeout configuration containing delay and max attempts.
           operation_type(str): create or update operation

        Returns:
            Dict[str, Any]
    """

    result = dict(comment=[], result=True, ret={})
    waiter_config = hub.tool.aws.waiter_utils.create_waiter_config(
        default_delay=60,
        default_max_attempts=35,
        timeout_config=timeout.get(operation_type) if timeout else None,
    )
    hub.log.debug(f"Waiting on {operation_type} aws.cloudfront.distribution '{name}'")
    try:
        await hub.tool.boto3.client.wait(
            ctx,
            "cloudfront",
            "distribution_deployed",
            Id=resource_id,
            WaiterConfig=waiter_config,
        )
    except Exception as e:
        result["comment"] += [str(e)]
        result["result"] = False
    return result
