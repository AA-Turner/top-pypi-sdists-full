from typing import Any
from typing import Dict


def sanitize_distribution_config(hub, original_distribution_config: Dict[str, Any]):
    updated_distribution_config = {}

    for (
        distribution_option_key,
        distribution_option_value,
    ) in original_distribution_config.items():
        if distribution_option_value is not None:
            updated_distribution_config[
                distribution_option_key
            ] = distribution_option_value

    return updated_distribution_config


def sanitize_distribution_config_for_update(
    hub, original_distribution_config: Dict[str, Any]
):
    updated_distribution_config = {}
    mandatory_params_in_update_with_defaults = {
        "Aliases": {"Quantity": 0},
        "DefaultRootObject": "",
        "CacheBehaviors": {"Quantity": 0},
        "CustomErrorResponses": {"Quantity": 0},
        "Logging": {
            "Enabled": False,
            "IncludeCookies": False,
            "Bucket": "",
            "Prefix": "",
        },
        "PriceClass": "PriceClass_All",
        "ViewerCertificate": {
            "CertificateSource": "cloudfront",
            "CloudFrontDefaultCertificate": True,
            "MinimumProtocolVersion": "TLSv1",
            "SSLSupportMethod": "vip",
        },
        "Restrictions": {"GeoRestriction": {"RestrictionType": "none", "Quantity": 0}},
        "WebACLId": "",
        "HttpVersion": "http2",
    }
    for (
        distribution_option_key,
        distribution_option_value,
    ) in original_distribution_config.items():
        if distribution_option_value is not None:
            updated_distribution_config[
                distribution_option_key
            ] = distribution_option_value
        elif distribution_option_key in mandatory_params_in_update_with_defaults:
            updated_distribution_config[
                distribution_option_key
            ] = mandatory_params_in_update_with_defaults[distribution_option_key]

    if "Origins" in updated_distribution_config:
        for item in updated_distribution_config["Origins"].get("Items", []):
            if "CustomHeaders" not in item:
                item["CustomHeaders"] = {"Quantity": 0}
            if "OriginPath" not in item:
                item["OriginPath"] = ""

    if (
        "DefaultCacheBehavior" in updated_distribution_config
        and "SmoothStreaming" not in updated_distribution_config["DefaultCacheBehavior"]
    ):
        updated_distribution_config["DefaultCacheBehavior"]["SmoothStreaming"] = False

    return updated_distribution_config
