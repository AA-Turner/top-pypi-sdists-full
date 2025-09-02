"""State module for managing Lambda function"""
import copy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]

STATE_NAME = "aws.lambda.function"


async def present(
    hub,
    ctx,
    name: str,
    role: str,
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
    runtime: str = None,
    handler: str = None,
    description: str = None,
    function_timeout: int = None,
    memory_size: int = None,
    publish: bool = None,
    vpc_config: make_dataclass(
        """Configuration for network connectivity to Amazon Web Services resources in a VPC"""
        "VpcConfig",
        [
            ("SubnetIds", List[str], field(default=None)),
            ("SecurityGroupIds", List[str], field(default=None)),
        ],
    ) = None,
    package_type: str = None,
    dead_letter_config: make_dataclass(
        """A dead letter queue configuration to specify the queue or topic where Lambda sends asynchronous events"""
        "DeadLetterConfig",
        [("TargetArn", str, field(default=None))],
    ) = None,
    environment: make_dataclass(
        """Environment variables that are accessible from function code"""
        "Environment",
        [("Variables", Dict[str, str], field(default=None))],
    ) = None,
    kms_key_arn: str = None,
    tracing_config: make_dataclass(
        """Config to sample and trace a subset of incoming requests with X-Ray."""
        "TracingConfig",
        [("Mode", str, field(default=None))],
    ) = None,
    tags: Dict[str, str] = None,
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
    code_signing_config_arn: str = None,
    architectures: List[str] = None,
    qualifier: str = None,
    maximum_retry_attempts: str = None,
    maximum_event_age_in_seconds: str = None,
    destination_config: str = None,
    revision_id: str = None,
    timeout: Dict = None,
) -> Dict[str, Any]:
    """
    Creates a Lambda function. To create a function, you need a deployment package and an execution role. The
    deployment package is a .zip file archive or container image that contains your function code. The execution role
    grants the function permission to use Amazon Web Services, such as Amazon CloudWatch Logs for log
    streaming and X-Ray for request tracing.

    When you create a function, Lambda provisions an instance of the function and its supporting resources. If your
    function connects to a VPC, this process can take a minute or so. During this time, you can't invoke or modify
    the function. The State , StateReason , and StateReasonCode fields in the response indicate when the function is ready to invoke.

    A function has an unpublished version, and can have published versions and aliases. The unpublished version
    changes when you update your function's code and configuration. A published version is a snapshot of your
    function code and configuration that can't be changed. An alias is a named resource that maps to a version,
    and can be changed to map to a different version. Use the Publish parameter to create version 1 of your function
    from its initial configuration.

    Args:
        resource_id(str): The name/ ARN/ partial ARN of the AWS Lambda function, version, or alias.
        name(str):
            The name of the Lambda function. The length constraint applies only to the full ARN. If you specify only the function name, it is limited to 64 characters in length.
                Name formats
                    * Function name - my-function .
                    * Function ARN - ``arn:aws:lambda:us-west-2:123456789012:function:my-function`` .
                    * Partial ARN - ``123456789012:function:my-function`` .
        role(str): The Amazon Resource Name (ARN) of the function's execution role.
        code(Dict[str, Any]):
            The code for the function.
                * ZipFile (ByteString, Optional): The base64-encoded contents of the deployment package. Amazon Web Services SDK and Amazon Web Services CLI clients handle the encoding for you.
                * S3Bucket (str, Optional): An Amazon S3 bucket in the same Amazon Web Services Region as your function. The bucket can be in a different Amazon Web Services account.
                * S3Key (str, Optional): The Amazon S3 key of the deployment package.
                * S3ObjectVersion (str, Optional): For versioned objects, the version of the deployment package object to use.
                * ImageUri (str, Optional): URI of a container image in the Amazon ECR registry.
        runtime(str, Optional): The identifier of the function's runtime. Runtime is required if the deployment package is a ``.zip`` file archive.
        revision_id(str, Optional): Only update the function if the revision ID matches the ID that's specified.
            Use this option to avoid modifying a function that has changed since you last read it.
        destination_config(dict, Optional): A destination for events after they have been sent to a function for processing.
        maximum_event_age_in_seconds(int, Optional): The maximum age of a request that Lambda sends to a function for processing.
        maximum_retry_attempts (int, Optional): The maximum number of times to retry when the function returns an error.
        qualifier(str): The version of the Lambda function.
        architectures(list, Optional): The instruction set architecture that the function supports. Enter a string array
            with one of the valid values (arm64 or x86_64). The default value is x86_64.
        code_signing_config_arn(str, Optional): To enable code signing for this function, specify the ARN of a code-signing configuration.
            A code-signing configuration includes a set of signing profiles, which define the trusted publishers for this function.
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
        timeout(Dict, Optional):
            Timeout configuration for create/update/deletion of AWS IAM Policy.
                * create (Dict):
                    Timeout configuration for creating AWS IAM Policy
                        * delay (int, Optional): The amount of time in seconds to wait between attempts.
                        * max_attempts (int, Optional): Customized timeout configuration containing delay and max attempts.
                * update (Dict, Optional):
                    Timeout configuration for updating AWS IAM Policy
                        * delay (int, Optional): The amount of time in seconds to wait between attempts.
                        * max_attempts (int, Optional): Customized timeout configuration containing delay and max attempts.

    Request Syntax:
        .. code-block:: sls

            [lambda_function-id]:
              aws.lambda.function.present:
                - name: 'string'
                - runtime: 'string'
                - role: 'string'
                - code: 'Dict'
                - handler: 'string'
                - description: 'string'
                - function_timeout: 'int'
                - memory_size: 'int'
                - publish: 'bool'
                - vpc_config: 'Dict'
                - package_type: 'string'
                - dead_letter_config: 'string'
                - environment: 'Dict'
                - kms_key_arn: 'string'
                - tracing_config: 'Dict'
                - layers: 'list'
                - file_system_configs: 'list'
                - image_config: 'Dict'
                - code_signing_config_arn: 'string'
                - architectures: 'list'
                - version: 'string'
                 - tags:
                    Key: Value

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: sls

            test_idem_lambda_function:
              aws.lambda.function.present:
                - name: test_idem_lambda_function
                - resource_id: test_idem_lambda_function
                - run_time: nodejs12.x
                - role: arn:aws:iam::123456789012:role/lambda-role
                - code:
                      S3Bucket: my-bucket-1xpuxmplzrlbh
                      S3Key: function.zip
                - tags:
                    DEPARTMENT: Assets
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    are_tags_updated = False
    is_function_updated = False
    existing_tags = {}
    plan_state = {}
    function_arn = None
    before = await hub.exec.boto3.client["lambda"].get_function(
        ctx=ctx, FunctionName=resource_id, Qualifier=qualifier
    )
    if before["result"] and before["ret"].get("Configuration"):
        function = before["ret"].get("Configuration")
        function_arn = function.get("FunctionArn")
        existing_tags = before.get("ret").get("Tags")
        resource_converted = await hub.tool.aws.lambda_aws.conversion_utils.convert_raw_lambda_function_to_present_async(
            ctx,
            raw_resource=function,
            idem_resource_name=name,
            tags=existing_tags,
        )
        result["result"] = result["result"] and resource_converted["result"]
        if not result["result"]:
            result["comment"] += resource_converted["comment"]
        result["old_state"] = resource_converted["ret"]
        plan_state = copy.deepcopy(result["old_state"])

        update_return = await hub.tool.aws.lambda_aws.function.compare_inputs_and_update_lambda_function(
            ctx,
            name=name,
            code=code,
            resource_id=resource_id,
            plan_state=plan_state,
            old_state=result["old_state"],
            zip_file=code.get("ZipFile"),
            s3_bucket=code.get("S3Bucket"),
            s3_key=code.get("S3Key"),
            s3_object_version=code.get("S3ObjectVersion"),
            image_uri=code.get("ImageUri"),
            publish=publish,
            revision_id=revision_id,
            architectures=architectures,
            role=role,
            handler=handler,
            description=description,
            function_timeout=function_timeout,
            memory_size=memory_size,
            vpc_config=vpc_config,
            environment=environment,
            runtime=runtime,
            dead_letter_config=dead_letter_config,
            kms_key_arn=kms_key_arn,
            tracing_config=tracing_config,
            layers=layers,
            file_system_configs=file_system_configs,
            image_config=image_config,
            timeout=timeout,
        )
        result["result"] = result["result"] and update_return["result"]
        result["comment"] += update_return["comment"]
        if result["result"]:
            is_function_updated = True

        if tags is not None:
            # Update tags
            update_tags_result = await hub.tool.aws.lambda_aws.tag.update_tags(
                ctx=ctx,
                resource_arn=function_arn,
                old_tags=existing_tags,
                new_tags=tags,
            )
            result["comment"] += update_tags_result["comment"]
            result["result"] = result["result"] and update_tags_result["result"]

            if not result["result"]:
                return result
            are_tags_updated = result["result"]

            if ctx.get("test", False) and (update_tags_result["ret"] is not None):
                plan_state["tags"] = update_tags_result["ret"]
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "role": role,
                    "code": code,
                    "resource_id": name,
                    "runtime": runtime,
                    "handler": handler,
                    "description": description,
                    "function_timeout": function_timeout,
                    "memory_size": memory_size,
                    "publish": publish,
                    "vpc_config": vpc_config,
                    "package_type": package_type,
                    "dead_letter_config": dead_letter_config,
                    "environment": environment,
                    "kms_key_arn": kms_key_arn,
                    "tracing_config": tracing_config,
                    "tags": tags,
                    "layers": layers,
                    "file_system_configs": file_system_configs,
                    "image_config": image_config,
                    "code_signing_config_arn": code_signing_config_arn,
                    "architectures": architectures,
                    "qualifier": qualifier,
                    "maximum_retry_attempts": maximum_retry_attempts,
                    "maximum_event_age_in_seconds": maximum_event_age_in_seconds,
                    "destination_config": destination_config,
                    "revision_id": revision_id,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type=STATE_NAME, name=name
            )
            return result
        try:
            ret = await hub.exec.boto3.client["lambda"].create_function(
                ctx,
                FunctionName=name,
                Runtime=runtime,
                Role=role,
                Handler=handler,
                Code=code,
                Description=description,
                Timeout=function_timeout,
                MemorySize=memory_size,
                Publish=publish,
                VpcConfig=vpc_config,
                PackageType=package_type,
                DeadLetterConfig=dead_letter_config,
                Environment=environment,
                KMSKeyArn=kms_key_arn,
                TracingConfig=tracing_config,
                Tags=tags,
                Layers=layers,
                FileSystemConfigs=file_system_configs,
                ImageConfig=image_config,
                CodeSigningConfigArn=code_signing_config_arn,
                Architectures=architectures,
            )
            result["result"] = ret["result"]
            if not ret["result"]:
                result["comment"] += ret["comment"]
                return result

            waiter_config = hub.tool.aws.waiter_utils.create_waiter_config(
                default_delay=1,
                default_max_attempts=20,
                timeout_config=timeout.get("create") if timeout else None,
            )
            hub.log.debug(f"Waiting on creating aws.lambda.function '{name}'")
            try:
                await hub.tool.boto3.client.wait(
                    ctx,
                    "lambda",
                    "function_active",
                    FunctionName=ret["ret"]["FunctionArn"],
                    WaiterConfig=waiter_config,
                )
            except Exception as e:
                result["comment"] += [str(e)]
                result["result"] = False
            resource_id = ret["ret"]["FunctionName"]
            function_arn = ret["ret"]["FunctionArn"]
            existing_tags = tags
            ret["comment"] = result[
                "comment"
            ] + hub.tool.aws.comment_utils.create_comment(
                resource_type=STATE_NAME, name=name
            )
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]
            result["result"] = False

    if ctx.get("test", False):
        result["new_state"] = plan_state
    elif not (before and before["result"]) or is_function_updated:
        after = await hub.exec.boto3.client["lambda"].get_function(
            ctx, FunctionName=resource_id, Qualifier=qualifier
        )
        final_updated_tags = (
            after.get("ret").get("Tags") if are_tags_updated else existing_tags
        )
        resource_converted = await hub.tool.aws.lambda_aws.conversion_utils.convert_raw_lambda_function_to_present_async(
            ctx=ctx,
            raw_resource=after["ret"].get("Configuration"),
            idem_resource_name=name,
            tags=final_updated_tags,
        )
        result["result"] = result["result"] and resource_converted["result"]
        if not result["result"]:
            result["comment"] += resource_converted["comment"]
        result["new_state"] = resource_converted["ret"]
    else:
        result["new_state"] = copy.deepcopy(result["old_state"])
    return result


async def absent(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    qualifier: str = None,
) -> Dict[str, Any]:
    """
    Deletes a Lambda function. To delete a specific function version, use the Qualifier parameter.
    Otherwise, all versions and aliases are deleted.

    For Amazon Web Service services and resources that invoke your function directly, delete the trigger in the service where you
    originally configured it.

    Args:
        resource_id(str, Optional): The name/ ARN/ partial ARN of the AWS Lambda function, version, or alias.
        qualifier(str, Optional): Specify a version or alias to get details about a published version of the function.
        name(str):
            The name of the Lambda function, version, or alias.
                Name formats
                    * Function name - my-function (name-only), my-function:v1 (with alias).
                    * Function ARN - ``arn:aws:lambda:us-west-2:123456789012:function:my-function`` .
                    * Partial ARN - ``123456789012:function:my-function`` .

    Request Syntax:
        .. code-block:: sls

            [lambda_function-id]:
              aws.lambda.function.absent:
                - name: 'string'
                - qualifier: 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            test_idem_lambda_function
                aws.lambda.function.absent:
                    - name: test_idem_lambda_function
                    - qualifier: 1
    """

    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type=STATE_NAME, name=name
        )
        return result
    before = await hub.exec.boto3.client["lambda"].get_function(
        ctx, FunctionName=resource_id, Qualifier=qualifier
    )
    if not before["result"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type=STATE_NAME, name=name
        )
    else:
        existing_tags = before.get("ret").get("Tags")
        resource_converted = await hub.tool.aws.lambda_aws.conversion_utils.convert_raw_lambda_function_to_present_async(
            ctx,
            raw_resource=before["ret"].get("Configuration"),
            idem_resource_name=resource_id,
            tags=existing_tags,
        )
        result["result"] = result["result"] and resource_converted["result"]
        if not result["result"]:
            result["comment"] += resource_converted["comment"]
        result["old_state"] = resource_converted["ret"]
        if ctx.get("test", False):
            result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
                resource_type=STATE_NAME, name=name
            )
            return result
        else:
            try:
                ret = await hub.exec.boto3.client["lambda"].delete_function(
                    ctx, FunctionName=resource_id, Qualifier=qualifier
                )
                result["result"] = ret["result"]
                if not result["result"]:
                    result["comment"] = ret["comment"]
                    return result
                result["comment"] = hub.tool.aws.comment_utils.delete_comment(
                    resource_type=STATE_NAME, name=name
                )
                after = await hub.exec.boto3.client["lambda"].get_function(
                    ctx, FunctionName=resource_id, Qualifier=qualifier
                )
                if after["result"] and after["ret"]:
                    resource_converted = await hub.tool.aws.lambda_aws.conversion_utils.convert_raw_lambda_function_to_present_async(
                        ctx,
                        raw_resource=after["ret"].get("Configuration"),
                        idem_resource_name=resource_id,
                        tags=existing_tags,
                    )
                    result["result"] = result["result"] and resource_converted["result"]
                    if not result["result"]:
                        result["comment"] = [
                            result["comment"] + resource_converted["comment"]
                        ]
                    result["new_state"] = resource_converted["ret"]
            except hub.tool.boto3.exception.ClientError as e:
                result["comment"] += [f"{e.__class__.__name__}: {e}"]
                result["result"] = False
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """
    Returns a list of Lambda functions, with the version-specific configuration of each. Lambda returns up to 50
    functions per call.

    Returns:
        Dict[str, Dict[str, Any]]

    Examples:

        .. code-block:: bash

            $ idem describe aws.lambda.function
    """

    result = {}

    ret = await hub.exec.boto3.client["lambda"].list_functions(ctx)
    if not ret["result"]:
        hub.log.warning(f"Could not describe function {ret['comment']}")
        return result
    if ret["ret"] and ret["ret"].get("Functions"):
        for function in ret["ret"].get("Functions"):
            tags = await hub.exec.boto3.client["lambda"].list_tags(
                ctx, Resource=function.get("FunctionArn")
            )
            resource_converted = await hub.tool.aws.lambda_aws.conversion_utils.convert_raw_lambda_function_to_present_async(
                ctx,
                raw_resource=function,
                idem_resource_name=function.get("FunctionName"),
                tags=tags.get("ret").get("Tags") if tags.get("result") else None,
            )
            if not resource_converted["result"]:
                hub.log.warning(
                    f"Could not describe {STATE_NAME} '{function.get('FunctionName')}' "
                    f"with error {resource_converted['comment']}"
                )
            else:
                result[function.get("FunctionName")] = {
                    "aws.lambda.function.present": [
                        {parameter_key: parameter_value}
                        for parameter_key, parameter_value in resource_converted[
                            "ret"
                        ].items()
                    ]
                }
    return result
