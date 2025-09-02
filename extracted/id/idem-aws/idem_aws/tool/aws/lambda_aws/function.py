from collections import OrderedDict
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

from dict_tools import data
from dict_tools import differ


async def compare_inputs_and_update_lambda_function(
    hub,
    ctx,
    name: str,
    code: make_dataclass(
        """The code for the function.""" "FunctionCode",
        [
            ("ZipFile", bytes, field(default=None)),
            ("S3Bucket", str, field(default=None)),
            ("S3Key", str, field(default=None)),
            ("S3ObjectVersion", str, field(default=None)),
            ("ImageUri", str, field(default=None)),
        ],
    ),
    resource_id: str = None,
    plan_state: Dict[str, Any] = None,
    old_state: Dict[str, Any] = None,
    zip_file: Dict[str, Any] = None,
    s3_bucket: str = None,
    s3_key: str = None,
    s3_object_version: str = None,
    image_uri: str = None,
    publish: str = None,
    revision_id: str = None,
    architectures: List[str] = None,
    role: str = None,
    handler: str = None,
    description: str = None,
    function_timeout: int = None,
    memory_size: int = None,
    vpc_config: make_dataclass(
        """Configuration for network connectivity to Amazon Web Services resources in a VPC"""
        "VpcConfig",
        [
            ("SubnetIds", List[str], field(default=None)),
            ("SecurityGroupIds", List[str], field(default=None)),
        ],
    ) = None,
    environment: make_dataclass(
        """Environment variables that are accessible from function code"""
        "Environment",
        [("Variables", Dict[str, str], field(default=None))],
    ) = None,
    runtime: str = None,
    dead_letter_config: make_dataclass(
        """A dead letter queue configuration to specify the queue or topic where Lambda sends asynchronous events"""
        "DeadLetterConfig",
        [("TargetArn", str, field(default=None))],
    ) = None,
    kms_key_arn: str = None,
    tracing_config: make_dataclass(
        """Config to sample and trace a subset of incoming requests with X-Ray."""
        "TracingConfig",
        [("Mode", str, field(default=None))],
    ) = None,
    layers: List[str] = None,
    file_system_configs: List[
        make_dataclass(
            """Config for connection settings for an Amazon EFS file system."""
            "FileSystemConfig",
            [("Arn", str), ("LocalMountPath", str)],
        )
    ] = None,
    image_config: make_dataclass(
        """Container image configuration values that override the values in the container image Dockerfile."""
        "ImageConfig",
        [
            ("EntryPoint", List[str], field(default=None)),
            ("Command", List[str], field(default=None)),
            ("WorkingDirectory", str, field(default=None)),
        ],
    ) = None,
    timeout: Dict = None,
):
    """
    Updates a Lambda function's code. If code signing is enabled for the function, the code package must be signed by
    a trusted publisher. The function's code is locked when you publish a version. You can't modify the code of a
    published version, only the unpublished version.

    Modify the version-specific settings of a Lambda function. When you update a function, Lambda provisions an
    instance of the function and its supporting resources. If your function connects to a VPC, this process can take
    a minute. During this time, you can't modify the function, but you can still invoke it. Updates the configuration
    for asynchronous invocation for a function, version, or alias.

    Update function's code, configuration, function's event invoke config This function compares data with new params
    and invokes update actions with appropriate arguments.

    Args:
        plan_state: idem --test state for update on AWS Lambda.
        name: The name of the Lambda function.
        code: a dictionary detailing existing code config.
        resource_id: The name/ ARN/ partial ARN of the AWS Lambda function, version, or alias.
        runtime(str, Optional): The identifier of the function's runtime. Runtime is required if the deployment package is a ``.zip`` file archive.
        revision_id(str, Optional): Only update the function if the revision ID matches the ID that's specified.
            Use this option to avoid modifying a function that has changed since you last read it.
        architectures(list, Optional): The instruction set architecture that the function supports. Enter a string array
            with one of the valid values (arm64 or x86_64). The default value is x86_64.
        image_config(Dict[str, Any], Optional):
            Container image configuration values that override the values in the container image Dockerfile. Defaults to None.
                * EntryPoint (list[str], Optional): Specifies the entry point to their application, which is typically the location of the runtime executable.
                * Command (list[str], Optional): Specifies parameters that you want to pass in with ENTRYPOINT.
                * WorkingDirectory (str, Optional): Specifies the working directory.
        file_system_configs(list[Dict[str, Any]], Optional):
            Connection settings for an Amazon EFS file system. Defaults to None.
                * Arn (str): The Amazon Resource Name (ARN) of the Amazon EFS access point that provides access to the file system.
                * LocalMountPath (str): The path where the function can access the file system, starting with /mnt/.
        layers(list, Optional): A list of function layers to add to the function's execution environment. Specify each layer by its ARN, including the version.
        tags(Dict[str, str], Optional): A list of tags to apply to the function. Defaults to None.
        tracing_config(Dict[str, Any], Optional):
            Set Mode to Active to sample and trace a subset of incoming requests with X-Ray. Defaults to None.
                * Mode (str, Optional): The tracing mode.
        kms_key_arn(str, Optional): The ARN of the Amazon Web Services Key Management Service (KMS) key that's used to encrypt your function's environment variables. If it's not provided, Lambda uses a default service key.
        environment(Dict[str, Any], Optional):
            Environment variables that are accessible from function code during execution. Defaults to None.
                * Variables (Dict[str, str], Optional): Environment variable key-value pairs. For more information, see Using Lambda environment variables.
        dead_letter_config(Dict[str, Any], Optional):
            A dead letter queue configuration that specifies the queue or topic where Lambda sends asynchronous events when they fail processing. Defaults to None.
                * TargetArn (str, Optional): The Amazon Resource Name (ARN) of an Amazon SQS queue or Amazon SNS topic.
                * package_type (str, Optional): The type of deployment package. Set to Image for container image and set Zip for ZIP archive.
        vpc_config(Dict[str, Any], Optional):
            For network connectivity to Amazon Web Services resources in a VPC, specify a list of security groups and subnets in the VPC. When you connect a function to a VPC, it can only access resources and the internet through that VPC. For more information, see VPC Settings. Defaults to None.
                * SubnetIds (list[str], Optional): A list of VPC subnet IDs.
                * SecurityGroupIds (list[str], Optional): A list of VPC security groups IDs.
        publish(bool, Optional): Set to true to publish the first version of the function during creation.
        memory_size(int, Optional): The amount of memory available to the function at runtime. Increasing the function memory also increases its CPU allocation.
            The default value is 128 MB. The value can be any multiple of 1 MB.
        function_timeout(int, Optional): The amount of time (in seconds) that Lambda allows a function to run before stopping it. The default is 3 seconds. The maximum allowed value is 900 seconds.
        description(str, Optional): A description of the function.
        handler(str, Optional): The name of the method within your code that Lambda calls to execute your function.
            Handler is required if the deployment package is a ``.zip`` file archive. The format includes the file name.
            It can also include namespaces and other qualifiers, depending on the runtime.
        timeout(Dict, Optional): Timeout configuration for create/update/deletion of AWS Lambda Function.
            * update (str) -- Timeout configuration for updating AWS Lambda Function
                * delay -- The amount of time in seconds to wait between attempts.
                * max_attempts -- Customized timeout configuration containing delay and max attempts.

    Returns:
        {"result": True|False, "comment": ("A tuple",), "ret": None}

    """
    result = dict(comment=[], result=True, ret=None)
    params_to_modify = {}
    modify_params = OrderedDict(
        {
            "Architectures": "architectures",
            "RevisionId": "revision_id",
            "ImageUri": "image_uri",
        }
    )
    for parameter_raw, parameter_present in modify_params.items():
        if locals()[parameter_present] is not None:
            if isinstance(locals()[parameter_present], list):
                if not hub.tool.aws.state_comparison_utils.are_lists_identical(
                    locals()[parameter_present], old_state.get(parameter_present)
                ):
                    params_to_modify[parameter_raw] = locals()[parameter_present]
            elif isinstance(locals()[parameter_present], Dict):
                if data.recursive_diff(
                    locals()[parameter_present],
                    old_state.get(parameter_present),
                    ignore_order=True,
                ):
                    params_to_modify[parameter_raw] = locals()[parameter_present]
            else:
                if locals()[parameter_present] != old_state.get(parameter_present):
                    params_to_modify[parameter_raw] = locals()[parameter_present]

    # update for lambda function code
    if params_to_modify:
        if ctx.get("test", False):
            result["comment"] += hub.tool.aws.comment_utils.would_update_comment(
                resource_type="aws.lambda.function", name=name
            )
            for key, value in params_to_modify.items():
                plan_state[modify_params.get(key)] = value
        else:
            modify_ret = await hub.exec.boto3.client["lambda"].update_function_code(
                ctx=ctx,
                FunctionName=resource_id,
                ZipFile=zip_file,
                S3Bucket=s3_bucket,
                S3Key=s3_key,
                S3ObjectVersion=s3_object_version,
                Publish=publish,
                **params_to_modify,
            )
            result["result"] = result["result"] and modify_ret["result"]
            result["comment"] += hub.tool.aws.comment_utils.update_comment(
                resource_type="aws.lambda.function", name=name
            )
            if not modify_ret["result"]:
                result["comment"] += modify_ret["comment"]
                result["result"] = False
                return result

            waiter_config = hub.tool.aws.waiter_utils.create_waiter_config(
                default_delay=1,
                default_max_attempts=20,
                timeout_config=timeout.get("update") if timeout else None,
            )
            try:
                await hub.tool.boto3.client.wait(
                    ctx,
                    "lambda",
                    "function_updated",
                    FunctionName=resource_id,
                    WaiterConfig=waiter_config,
                )
            except Exception as e:
                result["comment"] += [str(e)]
                result["result"] = False

    # update for lambda function configuration
    params_to_modify_for_config = {}
    modify_params_for_config = OrderedDict(
        {
            "Role": "role",
            "Handler": "handler",
            "Description": "description",
            "Timeout": "function_timeout",
            "MemorySize": "memory_size",
            "VpcConfig": "vpc_config",
            "Environment": "environment",
            "Runtime": "runtime",
            "DeadLetterConfig": "dead_letter_config",
            "KMSKeyArn": "kms_key_arn",
            "TracingConfig": "tracing_config",
            "RevisionId": "revision_id",
            "Layers": "layers",
            "FileSystemConfigs": "file_system_configs",
            "ImageConfig": "image_config",
        }
    )
    for (
        parameter_raw_for_config,
        parameter_present_for_config,
    ) in modify_params_for_config.items():
        # Add to modify list only if parameter is changed
        if locals()[parameter_present_for_config] is not None:
            if isinstance(locals()[parameter_present_for_config], list):
                if not hub.tool.aws.state_comparison_utils.are_lists_identical(
                    locals()[parameter_present_for_config],
                    old_state.get(parameter_present_for_config),
                ):
                    params_to_modify_for_config[parameter_raw_for_config] = locals()[
                        parameter_present_for_config
                    ]
            elif isinstance(locals()[parameter_present_for_config], Dict):
                if data.recursive_diff(
                    locals()[parameter_present_for_config],
                    old_state.get(parameter_present_for_config),
                    ignore_order=True,
                ):
                    params_to_modify_for_config[parameter_raw_for_config] = locals()[
                        parameter_present_for_config
                    ]
            else:
                if locals()[parameter_present_for_config] != old_state.get(
                    parameter_present_for_config
                ):
                    params_to_modify_for_config[parameter_raw_for_config] = locals()[
                        parameter_present_for_config
                    ]

    if params_to_modify_for_config:
        if ctx.get("test", False):
            result["comment"] += hub.tool.aws.comment_utils.would_update_comment(
                resource_type="aws.lambda.function", name=name
            )
            for key, value in params_to_modify_for_config.items():
                plan_state[modify_params_for_config.get(key)] = value
        else:
            modify_ret_for_config = await hub.exec.boto3.client[
                "lambda"
            ].update_function_configuration(
                ctx=ctx, FunctionName=resource_id, **params_to_modify_for_config
            )
            result["result"] = result["result"] and modify_ret_for_config["result"]
            result["comment"] += hub.tool.aws.comment_utils.update_comment(
                resource_type="aws.lambda.function", name=name
            )
            if not modify_ret_for_config["result"]:
                result["comment"] += modify_ret_for_config["comment"]
                result["result"] = False
                return result

            waiter_config_for_config = hub.tool.aws.waiter_utils.create_waiter_config(
                default_delay=1,
                default_max_attempts=20,
                timeout_config=timeout.get("update") if timeout else None,
            )
            try:
                await hub.tool.boto3.client.wait(
                    ctx,
                    "lambda",
                    "function_updated",
                    FunctionName=resource_id,
                    WaiterConfig=waiter_config_for_config,
                )
            except Exception as e:
                result["comment"] += [str(e)]
                result["result"] = False
    return result
