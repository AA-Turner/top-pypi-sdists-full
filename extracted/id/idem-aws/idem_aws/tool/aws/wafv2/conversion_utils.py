"""Conversion util functions to support AWS WAFV2 resources."""
import json
from collections import OrderedDict
from typing import Any
from typing import Dict


def convert_raw_web_acl_resource_association_to_present(
    hub,
    web_acl_arn: str,
    resource_arn: str,
    idem_resource_name: str = None,
) -> Dict[str, Any]:
    """Util functions to convert raw resource state from Associate Web ACL to present input format.

    Args:
        web_acl_arn:
            The Amazon Resource Name (ARN) of the web ACL that you want to associate with the resource.
        resource_arn:
            The Amazon Resource Name (ARN) of the resource to associate with the web ACL.
        idem_resource_name:
            The idem name for the resource.

    Returns:
        Dict[str, Any]
    """
    resource_id = resource_arn
    translated_resource = {
        "name": idem_resource_name,
        "resource_id": resource_id,
        "web_acl_arn": web_acl_arn,
        "resource_arn": resource_arn,
    }
    return translated_resource


def convert_raw_regex_pattern_set_to_present(
    hub, ctx, raw_resource: Dict[str, Any], scope: str, tags: Dict[str, str]
) -> Dict[str, Any]:
    """Util functions to convert raw resource state from regex pattern state to present input format.

    Args:
        raw_resource(dict): Old state of resource or existing resource details.
        scope(str): Specifies whether this is for an Amazon CloudFront distribution or for a regional application.
        tags(dict): Dict in the format of {tag-key: tag-value}

    Returns:
        Dict[str, Any]
    """
    resource_parameters = OrderedDict(
        {
            "Name": "name",
            "Description": "description",
            "RegularExpressionList": "regular_expression_list",
            "Id": "resource_id",
            "ARN": "arn",
        }
    )
    resource_translated = {"scope": scope, "tags": tags}
    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in raw_resource and raw_resource.get(parameter_raw):
            resource_translated[parameter_present] = json.loads(
                json.dumps(raw_resource.get(parameter_raw))
            )

    return resource_translated


async def convert_raw_web_acl_to_present_async(
    hub,
    ctx,
    raw_resource: Dict[str, Any],
    idem_resource_name: str = None,
    scope: str = None,
) -> Dict[str, Any]:
    """Util functions to convert raw resource state from Web ACL to present input format.

    Args:
        raw_resource:
            Old state of resource or existing resource details.
        idem_resource_name:
            Resource name.
        scope:
            Specifies whether this is for an Amazon CloudFront distribution or for a regional application.

    Returns:
        Dict[str, Any]
    """

    result = dict(comment=[], result=True, ret=None)
    resource_id = raw_resource.get("Id")
    web_acl_arn = raw_resource.get("ARN")
    resource_parameters = OrderedDict(
        {
            "DefaultAction": "default_action",
            "Description": "description",
            "Rules": "rules",
            "VisibilityConfig": "visibility_config",
            "CustomResponseBodies": "custom_response_bodies",
            "CaptchaConfig": "captcha_config",
        }
    )
    resource_translated = {
        "name": idem_resource_name,
        "resource_id": resource_id,
        "scope": scope,
        "web_acl_arn": web_acl_arn,
    }
    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in raw_resource and raw_resource.get(parameter_raw):
            resource_translated[parameter_present] = json.loads(
                json.dumps(raw_resource.get(parameter_raw))
            )

    ret_tag = await hub.exec.boto3.client.wafv2.list_tags_for_resource(
        ctx, ResourceARN=web_acl_arn
    )
    result["result"] = ret_tag["result"]
    if not result["result"]:
        result["comment"] += ret_tag["comment"]
        return result
    if (
        ret_tag["ret"]
        and ret_tag["ret"]["TagInfoForResource"]
        and ret_tag["ret"]["TagInfoForResource"].get("TagList")
    ):
        resource_translated["tags"] = hub.tool.aws.tag_utils.convert_tag_list_to_dict(
            ret_tag["ret"]["TagInfoForResource"].get("TagList")
        )
    result["ret"] = resource_translated
    return result


def convert_raw_ip_set_to_present(
    hub,
    scope: str,
    raw_resource: Dict[str, Any],
    tags: Dict[str, Any] = None,
) -> Dict[str, Any]:
    """Convert AWS returned data structure to correct idem wafv2 ip_set resource to present state.

     Args:
        hub:
            The redistributed pop central hub.
        ctx:
            A dict with the keys/values for the execution of the Idem run located in
            `hub.idem.RUNS[ctx['run_name']]`.
        scope (str) --
            Specifies whether this is for an Amazon CloudFront distribution or for a regional
            application. A regional application can be an Application Load Balancer (ALB), an Amazon API Gateway
            REST API, or an AppSync GraphQL API.
            To work with CloudFront, you must also specify the Region US East (N. Virginia) as follows:
            CLI - Specify the Region when you use the CloudFront scope: --scope=CLOUDFRONT --region=us-east-1 .
            API and SDKs - For all calls, use the Region endpoint us-east-1.
        raw_resource:
            The aws response to convert
        tags (List, Optional):
            The tags of the resource. Defaults to None.

    Returns:
        Dict[str, Any]
    """
    resource_translated = {
        "scope": scope,
    }

    resource_parameters_keys_case_mapping = OrderedDict(
        {
            "Name": "name",
            "Id": "resource_id",
            "Description": "description",
            "IPAddressVersion": "ip_address_version",
            "Addresses": "addresses",
            "Tags": "tags",
            "ARN": "arn",
            "LockToken": "lock_token",
        }
    )
    if (
        raw_resource
        and raw_resource.get("ret")
        and raw_resource.get("ret").get("IPSet")
    ):
        for (
            camel_case_key,
            snake_case_key,
        ) in resource_parameters_keys_case_mapping.items():
            if raw_resource["ret"]["IPSet"].get(camel_case_key):
                resource_translated[snake_case_key] = raw_resource["ret"]["IPSet"].get(
                    camel_case_key
                )
    if (
        raw_resource
        and raw_resource.get("ret")
        and raw_resource.get("ret").get("LockToken")
    ):
        resource_translated["lock_token"] = raw_resource.get("ret").get("LockToken")

    if tags or tags == {}:
        resource_translated["tags"] = tags
    return resource_translated
