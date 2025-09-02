from collections import OrderedDict
from typing import Any
from typing import Dict

"""
Util functions for AWS Lambda Function Permission resources.
"""


def convert_raw_lambda_permission_to_present(
    hub,
    raw_resource: Dict[str, Any],
    function_name: str,
    revision_id: str = None,
) -> Dict[str, Any]:
    """
    Converts an AWS Lambda Function Permission resource to a common idem present state.

    Args:
        hub: required for functions in hub.
        raw_resource(Dict[str, Any]): The AWS response to convert.
        function_name(str): The name of the AWS Lambda Function.
        revision_id(str, Optional): The revision ID of the policy.

    Returns:
        Dict[str, Any]: Common idem present state.
    """
    describe_parameters = OrderedDict(
        {
            "Sid": "resource_id",
            "Action": "action",
            "Principal": "principal",
            "Effect": "effect",
        }
    )
    translated_resource = {}
    for parameter_raw, parameter_present in describe_parameters.items():
        if parameter_raw in raw_resource:
            translated_resource[parameter_present] = raw_resource.get(parameter_raw)
    translated_resource["name"] = raw_resource["Sid"]
    translated_resource["function_name"] = function_name

    if revision_id:
        translated_resource["revision_id"] = revision_id

    qualifier = hub.tool.aws.arn_utils.get_qualifier(raw_resource.get("Resource"))
    if qualifier:
        translated_resource["qualifier"] = qualifier

    condition = raw_resource.get("Condition")
    if condition:
        stringEquals = condition.get("StringEquals")
        if stringEquals:
            source_account = stringEquals.get("AWS:SourceAccount")
            if source_account:
                translated_resource["source_account"] = source_account
            event_source_token = stringEquals.get("lambda:EventSourceToken")
            if event_source_token:
                translated_resource["event_source_token"] = event_source_token
            principal_org_id = stringEquals.get("aws:PrincipalOrgID")
            if principal_org_id:
                translated_resource["principal_org_id"] = principal_org_id
            function_url_auth_type = stringEquals.get("lambda:FunctionUrlAuthType")
            if function_url_auth_type:
                translated_resource["function_url_auth_type"] = function_url_auth_type

        arnLike = condition.get("ArnLike")
        if arnLike:
            translated_resource["source_arn"] = arnLike.get("AWS:SourceArn")

    return translated_resource
