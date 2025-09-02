import copy
from collections import OrderedDict
from typing import Any
from typing import Dict


def convert_raw_function_event_invoke_config_to_present(
    hub,
    raw_resource: Dict[str, Any],
    function_name: str = None,
    idem_resource_name: str = None,
) -> Dict[str, Any]:
    """
    Convert AWS returned data structure to correct idem function_event_invoke_config present state

     Args:
        hub: required for functions in hub
        raw_resource(Dict): The aws response to convert
        function_name (str, Optional): The name of the Lambda function
        idem_resource_name(str, Optional): An Idem name of the resource.

    Returns: Valid idem state for function_event_invoke_config of type Dict['string', Any]
    """
    function_arn = raw_resource.get("FunctionArn")
    resource_parameters = OrderedDict(
        {
            "MaximumRetryAttempts": "maximum_retry_attempts",
            "MaximumEventAgeInSeconds": "maximum_event_age_in_seconds",
            "DestinationConfig": "destination_config",
        }
    )
    resource_translated = {
        "name": idem_resource_name if idem_resource_name else function_arn,
        "resource_id": function_arn,
        "function_name": function_name,
    }
    for parameter_raw, parameter_present in resource_parameters.items():
        if raw_resource.get(parameter_raw) is not None:
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)

    qualifier = hub.tool.aws.arn_utils.get_qualifier(function_arn)
    if qualifier:
        resource_translated["qualifier"] = qualifier

    return resource_translated


async def update_function_event_invoke_config(
    hub,
    ctx,
    function_name: str,
    current_state: Dict[str, Any],
    desired_state: Dict[str, Any],
):
    """
    Updates configuration options for asynchronous invocation on a function

    Args:
        hub: required for functions in hub.
        ctx: context.
        function_name(str): The name of the Lambda function
        current_state(Dict): Previous state of the resource
        desired_state(Dict): Parameters from SLS file.

    Returns:
        Dict[str, Any]
    """
    modify_params = dict(
        {
            "Qualifier": "qualifier",
            "MaximumRetryAttempts": "maximum_retry_attempts",
            "MaximumEventAgeInSeconds": "maximum_event_age_in_seconds",
            "DestinationConfig": "destination_config",
        }
    )
    result = dict(comment=[], result=True, ret=None)
    plan_state = copy.deepcopy(current_state)
    params_to_modify = {}

    # create a dict 'params_to_modify' of raw parameter key mapped to desired value,
    # where the desired value is not none and current value does not match desired value
    for param_raw, param_present in modify_params.items():
        if desired_state.get(param_present) is not None and current_state.get(
            param_present
        ) != desired_state.get(param_present):
            params_to_modify[param_raw] = desired_state[param_present]

    if params_to_modify:
        for key, value in params_to_modify.items():
            plan_state[modify_params.get(key)] = value
        if ctx.get("test", False):
            result["comment"] = hub.tool.aws.comment_utils.would_update_comment(
                resource_type="aws.lambda.function_event_invoke_config",
                name=current_state["name"],
            )
        else:
            update_ret = await hub.exec.boto3.client[
                "lambda"
            ].update_function_event_invoke_config(
                ctx, FunctionName=function_name, **params_to_modify
            )
            if not update_ret["result"]:
                result["result"] = False
                result["comment"] = update_ret["comment"]
                return result
            result["comment"] = hub.tool.aws.comment_utils.update_comment(
                resource_type="aws.lambda.function_event_invoke_config",
                name=current_state["name"],
            )
        result["ret"] = plan_state
    else:
        result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
            resource_type="aws.lambda.function_event_invoke_config",
            name=current_state["name"],
        )

    return result
