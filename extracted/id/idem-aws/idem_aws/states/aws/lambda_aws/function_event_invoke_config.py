"""State module for managing Lambda function asynchronous invocation configuration"""
import copy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any

__contracts__ = ["resource"]

from typing import Dict


async def present(
    hub,
    ctx,
    name: str,
    function_name: str,
    resource_id: str = None,
    qualifier: str = None,
    maximum_retry_attempts: int = None,
    maximum_event_age_in_seconds: int = None,
    destination_config: make_dataclass(
        """A destination configuration for events after they have been sent to a function."""
        "DestinationConfigRequest",
        [
            ("OnSuccess", Dict, field(default=None)),
            ("OnFailure", Dict, field(default=None)),
        ],
    ) = None,
) -> Dict[str, Any]:
    """
    Configures options for asynchronous invocation on a function, version, or alias. If a configuration already
    exists for a function, version, or alias, this operation overwrites it. By default, Lambda retries an asynchronous invocation twice if the function
    returns an error. It retains events in a queue for up to six hours. When an event fails all processing attempts
    or stays in the asynchronous invocation queue for too long, Lambda discards it. To retain discarded events,
    configure a dead-letter queue. To send an invocation record to a queue, topic,
    function, or event bus, specify a destination. You can configure separate destinations for successful
    invocations (on-success) and events that fail all processing attempts (on-failure). You can configure
    destinations in addition to or instead of a dead-letter queue.

    Args:
        name(str): An Idem name of the resource.
        resource_id(str, Optional): The Amazon Resource Name (ARN) of the function. Defaults to None.
        function_name(str):
            The name of the Lambda function. The length constraint applies only to the full ARN. If you  specify only the function name, it is limited to 64 characters in length.
                Name formats
                    * Function name - my-function
                    * Function ARN - ``arn:aws:lambda:us-west-2:123456789012:function:my-function``
                    * Partial ARN - ``123456789012:function:my-function``

        qualifier(str, Optional): A version number or alias name. Defaults to None.
        maximum_retry_attempts(int, Optional): The maximum number of times to retry when the function returns an error. Defaults to None.
        maximum_event_age_in_seconds(int, Optional): The maximum age of a request that Lambda sends to a function for processing. Defaults to None.
        destination_config(Dict, Optional):
            A destination for events after they have been sent to a function for processing.
                * (OnSuccess, Dict, Optional): The destination configuration for successful invocations.
                * (OnFailure, Dict, Optional): The destination configuration for failed invocations.
            Destinations
                * Function - The Amazon Resource Name (ARN) of a Lambda function.
                * Queue - The ARN of an SQS queue.
                * Topic - The ARN of an SNS topic.
                * Event Bus - The ARN of an Amazon EventBridge event bus. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: sls

            function_event_invoke_config-01234672f3336db8:
              aws.lambda_aws.function_event_invoke_config.present:
                - name: value
                - function_name: value
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    before = None
    resource_updated = False
    if resource_id:
        before = await hub.exec.aws.lambda_aws.function_event_invoke_config.get(
            ctx, name=name, resource_id=resource_id
        )
        if not (before["result"] and before["ret"]):
            result["comment"] = before["comment"]
            result["result"] = False
            return result
        result["old_state"] = copy.deepcopy(before["ret"])
        result["new_state"] = copy.deepcopy(result["old_state"])
        desired_resource_parameters = {
            "qualifier": qualifier,
            "maximum_retry_attempts": maximum_retry_attempts,
            "maximum_event_age_in_seconds": maximum_event_age_in_seconds,
            "destination_config": destination_config,
        }
        update_function_event_invoke_config_ret = await hub.tool.aws.lambda_aws.function_event_invoke_config.update_function_event_invoke_config(
            ctx,
            function_name=function_name,
            current_state=result["old_state"],
            desired_state=desired_resource_parameters,
        )
        if not update_function_event_invoke_config_ret["result"]:
            result["result"] = False
            result["comment"] = update_function_event_invoke_config_ret["comment"]
            return result

        result["comment"] = (
            result["comment"] + update_function_event_invoke_config_ret["comment"]
        )
        resource_updated = bool(update_function_event_invoke_config_ret["ret"])

        if ctx.get("test", False) and resource_updated:
            result["new_state"].update(update_function_event_invoke_config_ret["ret"])
            return result

    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "function_name": function_name,
                    "qualifier": qualifier,
                    "maximum_retry_attempts": maximum_retry_attempts,
                    "maximum_event_age_in_seconds": maximum_event_age_in_seconds,
                    "destination_config": destination_config,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.lambda.function_event_invoke_config", name=name
            )
            return result

        create_ret = await hub.exec.boto3.client[
            "lambda"
        ].put_function_event_invoke_config(
            ctx,
            FunctionName=function_name,
            Qualifier=qualifier,
            MaximumRetryAttempts=maximum_retry_attempts,
            MaximumEventAgeInSeconds=maximum_event_age_in_seconds,
            DestinationConfig=destination_config,
        )
        result["result"] = create_ret["result"]
        if not result["result"]:
            result["comment"] = create_ret["comment"]
            return result
        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.lambda.function_event_invoke_config", name=name
        )
    if (not before) or resource_updated:
        after = await hub.exec.aws.lambda_aws.function_event_invoke_config.get(
            ctx, name=name, function_name=function_name, qualifier=qualifier
        )
        if not (after["result"] and after["ret"]):
            result["result"] = False
            result["comment"] += after["comment"]
            return result
        result["new_state"] = copy.deepcopy(after["ret"])

    return result


async def absent(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Deletes the configuration for asynchronous invocation for a function, version, or alias.

    Args:
        name(str): An Idem name of the resource.
        resource_id(str, Optional): The Amazon Resource Name (ARN) of the function. Idem automatically considers this
            resource being absent if this field is not specified.

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: sls

            function_event_invoke_config-01234672f3336db8:
              aws.lambda_aws.function_event_invoke_config.absent:
                - name: value
                - resource_id: value
    """
    already_absent_msg = hub.tool.aws.comment_utils.already_absent_comment(
        resource_type="aws.lambda.function_event_invoke_config", name=name
    )
    result = dict(
        comment=already_absent_msg,
        old_state=None,
        new_state=None,
        name=name,
        result=True,
    )

    if not resource_id:
        return result

    before = await hub.exec.aws.lambda_aws.function_event_invoke_config.get(
        ctx, name=name, resource_id=resource_id
    )

    if not before["result"]:
        result["comment"] = before["comment"]
        result["result"] = False
        return result

    if before["ret"]:
        result["old_state"] = before["ret"]
        if ctx.get("test", False):
            result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
                resource_type="aws.lambda.function_event_invoke_config", name=name
            )
        else:
            function_name = hub.tool.aws.arn_utils.get_resource_name(resource_id)
            qualifier = hub.tool.aws.arn_utils.get_qualifier(resource_id)
            ret = await hub.exec.boto3.client[
                "lambda"
            ].delete_function_event_invoke_config(
                ctx, **{"FunctionName": function_name, "Qualifier": qualifier}
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = ret["comment"]
                return result
            result["comment"] = hub.tool.aws.comment_utils.delete_comment(
                resource_type="aws.lambda.function_event_invoke_config", name=name
            )

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Retrieves a list of configurations for asynchronous invocation for a function.

    Returns:
        Dict[str, Dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe aws.lambda_aws.function_event_invoke_config
    """

    result = {}

    get_functions_ret = await hub.exec.boto3.client["lambda"].list_functions(ctx)
    if not get_functions_ret["result"]:
        hub.log.warning(f"Could not list functions {get_functions_ret['comment']}")
        return result

    for function in get_functions_ret["ret"]["Functions"]:
        function_name = function.get("FunctionName")
        get_event_invoke_configs_ret = await hub.exec.boto3.client[
            "lambda"
        ].list_function_event_invoke_configs(ctx, FunctionName=function_name)

        if not get_event_invoke_configs_ret["result"]:
            hub.log.debug(
                f"Could not get event invoke config for functionName '{function_name}': "
                f"{get_event_invoke_configs_ret['comment']}. Describe will skip this function and continue."
            )
            continue

        for function_event_invoke_config in get_event_invoke_configs_ret["ret"][
            "FunctionEventInvokeConfigs"
        ]:
            resource_arn = function_event_invoke_config.get("FunctionArn")
            # Including fields to match the 'present' function parameters
            resource_translated = hub.tool.aws.lambda_aws.function_event_invoke_config.convert_raw_function_event_invoke_config_to_present(
                function_event_invoke_config,
                function_name=function_name,
            )
            result[resource_arn] = {
                "aws.lambda.function_event_invoke_config.present": [
                    {parameter_key: parameter_value}
                    for parameter_key, parameter_value in resource_translated.items()
                ]
            }
    return result
