from collections import OrderedDict
from typing import Any
from typing import Dict
from typing import List

"""
Util functions for AWS Lambda Function resources.
"""


async def convert_raw_lambda_function_to_present_async(
    hub,
    ctx,
    raw_resource: Dict[str, Any],
    idem_resource_name: str = None,
    tags: List = None,
) -> Dict[str, Any]:
    """
    Converts an AWS Lambda Function resource to a common idem present state.

    Args:
        hub: required for functions in hub.
        raw_resource(Dict[str, Any]): The AWS response to convert.
        idem_resource_name(str, Optional): An Idem name of the resource.
        tags(List, Optional): The AWS Lambda Function tags.

    Returns:
        Dict[str, Any]: Common idem present state.
    """
    describe_parameters = OrderedDict(
        {
            "FunctionArn": "function_arn",
            "Runtime": "runtime",
            "Role": "role",
            "Handler": "handler",
            "Description": "description",
            "Timeout": "function_timeout",
            "MemorySize": "memory_size",
            "VpcConfig": "vpc_config",
            "PackageType": "package_type",
            "DeadLetterConfig": "dead_letter_config",
            "Environment": "environment",
            "KMSKeyArn": "kms_key_arn",
            "TracingConfig": "tracing_config",
            "Layers": "layers",
            "FileSystemConfigs": "file_system_configs",
            "Architectures": "architectures",
        }
    )
    new_function = {"resource_id": idem_resource_name, "name": idem_resource_name}
    result = dict(comment=[], result=True, ret=None)
    for parameter_old_key, parameter_new_key in describe_parameters.items():
        if raw_resource.get(parameter_old_key) is not None:
            new_function.update(
                {parameter_new_key: raw_resource.get(parameter_old_key)}
            )
    config_arn = await hub.exec.boto3.client["lambda"].get_function_code_signing_config(
        ctx, FunctionName=raw_resource.get("FunctionArn")
    )
    result["result"] = config_arn["result"]
    if not result["result"]:
        result["comment"] += config_arn["comment"]

    if config_arn.get("result") and config_arn.get("ret").get("CodeSigningConfigArn"):
        new_function.update(
            {
                "code_signing_config_arn": config_arn.get("ret").get(
                    "CodeSigningConfigArn"
                )
            }
        )

    if raw_resource.get("ImageConfigResponse") and raw_resource.get(
        "ImageConfigResponse"
    ).get("ImageConfig"):
        new_function.update(
            {
                "image_config": (
                    raw_resource.get("ImageConfigResponse").get("ImageConfig")
                ).copy()
            }
        )
    if tags:
        new_function["tags"] = tags.copy()

    new_function["invoke_arn"] = hub.tool.aws.arn_utils.build(
        service="apigateway",
        region=ctx["acct"]["region_name"],
        account_id="lambda",
        resource="path/2015-03-31/functions/"
        + new_function["function_arn"]
        + "/invocations",
    )
    result["ret"] = new_function
    return result
