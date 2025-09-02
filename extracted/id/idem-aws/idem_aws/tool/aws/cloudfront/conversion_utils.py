import copy
from collections import OrderedDict
from typing import Any
from typing import Dict

"""
Util functions to convert raw resource state from AWS CloudFront to present input format.
"""


def convert_raw_distribution_to_present(
    hub,
    ctx,
    raw_resource: Dict[str, Any],
    idem_resource_name: str = None,
) -> Dict[str, Any]:
    resource_id = raw_resource.get("Id")
    resource_translated = {
        "name": idem_resource_name,
        "resource_id": resource_id,
        "arn": raw_resource.get("ARN"),
    }
    resource_parameters = OrderedDict(
        {
            "CallerReference": "caller_reference",
            "Comment": "comment",
            "Origins": "origins",
            "DefaultCacheBehavior": "default_cache_behaviour",
            "Logging": "logging",
            "Enabled": "enabled",
            "ViewerCertificate": "viewer_certificate",
            "Aliases": "aliases",
            "PriceClass": "price_class",
            "DefaultRootObject": "default_root_object",
            "OriginGroups": "origin_groups",
            "CacheBehaviors": "cache_behaviors",
            "CustomErrorResponses": "custom_error_responses",
            "Restrictions": "restrictions",
            "WebACLId": "web_acl_id",
            "HttpVersion": "http_version",
            "IsIPV6Enabled": "is_ipv6_enabled",
        }
    )

    distribution_config = raw_resource["DistributionConfig"]
    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in distribution_config:
            resource_translated[parameter_present] = (
                dict(distribution_config.get(parameter_raw).copy())
                if isinstance(distribution_config.get(parameter_raw), dict)
                else distribution_config.get(parameter_raw)
            )

    if raw_resource.get("Tags") is not None:
        resource_translated["tags"] = hub.tool.aws.tag_utils.convert_tag_list_to_dict(
            raw_resource.get("Tags")
        )
    if raw_resource.get("ETag") is not None:
        resource_translated["ETag"] = raw_resource.get("ETag")

    return hub.tool.aws.ec2.instance.data.sanitize_dict(resource_translated)


def convert_raw_cache_policy_to_present(
    hub,
    ctx,
    raw_resource: Dict[str, Any],
    idem_resource_name: str = None,
) -> Dict[str, Any]:
    resource_id = raw_resource.get("Id")
    resource_translated = {
        "name": idem_resource_name,
        "resource_id": resource_id,
    }
    resource_parameters = OrderedDict(
        {
            "Comment": "comment",
            "Name": "name",
            "DefaultTTL": "default_ttl",
            "MaxTTL": "max_ttl",
            "MinTTL": "min_ttl",
            "ParametersInCacheKeyAndForwardedToOrigin": "parameter_in_cache_key_and_forward_to_origin",
        }
    )

    cache_policy_config = raw_resource["CachePolicyConfig"]
    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in cache_policy_config:
            resource_translated[parameter_present] = (
                copy.deepcopy(dict(cache_policy_config.get(parameter_raw)))
                if isinstance(cache_policy_config.get(parameter_raw), dict)
                else cache_policy_config.get(parameter_raw)
            )
    if raw_resource.get("ETag") is not None:
        resource_translated["etag"] = raw_resource.get("ETag")
    resource_translated = hub.tool.aws.cloudfront.cloudfront_utils.sanitize_dict(
        resource_translated
    )
    return resource_translated


def convert_raw_origin_request_policy_to_present(
    hub,
    ctx,
    raw_resource: Dict[str, Any],
    idem_resource_name: str = None,
) -> Dict[str, Any]:
    resource_id = raw_resource.get("Id")
    resource_translated = {
        "name": idem_resource_name,
        "resource_id": resource_id,
    }
    resource_parameters = OrderedDict(
        {
            "Comment": "comment",
            "Name": "name",
            "HeadersConfig": "headers_config",
            "CookiesConfig": "cookies_config",
            "QueryStringsConfig": "query_strings_config",
        }
    )

    origin_request_config = raw_resource["OriginRequestPolicyConfig"]
    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in origin_request_config:
            resource_translated[parameter_present] = (
                dict(origin_request_config.get(parameter_raw).copy())
                if isinstance(origin_request_config.get(parameter_raw), dict)
                else origin_request_config.get(parameter_raw)
            )

    if raw_resource.get("ETag") is not None:
        resource_translated["etag"] = raw_resource.get("ETag")

    resource_translated = hub.tool.aws.cloudfront.cloudfront_utils.sanitize_dict(
        resource_translated
    )
    return resource_translated
