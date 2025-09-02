"""State module for managing Lambda provisioned concurrency config."""
import copy
from typing import Any

__contracts__ = ["resource"]

from typing import Dict


async def present(
    hub,
    ctx,
    name: str,
    function_name: str,
    qualifier: str,
    provisioned_concurrent_executions: int,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Adds a provisioned concurrency configuration to a function's alias or version.

    Args:
        name(str): An Idem name of the resource.
        function_name(str):
            The name of the Lambda function. The length constraint applies only to the full ARN. If you  specify only the function name, it is limited to 64 characters in length.
                Name formats:
                    * Function name - my-function.
                    * Function ARN - ``arn:aws:lambda:us-west-2:123456789012:function:my-function`` .
                    * Partial ARN - ``123456789012:function:my-function`` .
        qualifier(str): A version number or alias name. Defaults to None.
        provisioned_concurrent_executions(int): The amount of provisioned concurrency to allocate for the version or alias.
        resource_id(str, Optional): The Amazon Resource Name (ARN) of the function. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            function_provisioned_concurrency_config-01234672f3336db8:
              aws.lambda_aws.function_provisioned_concurrency_config.present:
                - name: value
                - function_name: value
                - qualifier: value
                - provisioned_concurrent_executions: int
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    before = None
    resource_updated = False
    if resource_id:
        before = (
            await hub.exec.aws.lambda_aws.function_provisioned_concurrency_config.get(
                ctx, name=name, resource_id=resource_id
            )
        )
        if not (before["result"] and before["ret"]):
            result["comment"] = before["comment"]
            result["result"] = False
            return result
        result["old_state"] = copy.deepcopy(before["ret"])
        result["new_state"] = copy.deepcopy(result["old_state"])

        old_provisioned_concurrent_executions = result["old_state"].get(
            "provisioned_concurrent_executions"
        )
        if old_provisioned_concurrent_executions != provisioned_concurrent_executions:
            if ctx.get("test", False):
                result["comment"] = hub.tool.aws.comment_utils.would_update_comment(
                    resource_type="aws.lambda.function_provisioned_concurrency_config",
                    name=name,
                )
                result["new_state"][
                    "provisioned_concurrent_executions"
                ] = provisioned_concurrent_executions
                return result
            else:
                update_ret = await hub.exec.boto3.client[
                    "lambda"
                ].put_provisioned_concurrency_config(
                    ctx,
                    FunctionName=function_name,
                    Qualifier=qualifier,
                    ProvisionedConcurrentExecutions=provisioned_concurrent_executions,
                )
                if not update_ret["result"]:
                    result["result"] = False
                    result["comment"] = update_ret["comment"]
                    return result
                result["comment"] = hub.tool.aws.comment_utils.update_comment(
                    resource_type="aws.lambda.function_provisioned_concurrency_config",
                    name=name,
                )
                resource_updated = True
        else:
            result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
                resource_type="aws.lambda.function_provisioned_concurrency_config",
                name=name,
            )

    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "function_name": function_name,
                    "qualifier": qualifier,
                    "provisioned_concurrent_executions": provisioned_concurrent_executions,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.lambda.function_provisioned_concurrency_config",
                name=name,
            )
            return result

        create_ret = await hub.exec.boto3.client[
            "lambda"
        ].put_provisioned_concurrency_config(
            ctx,
            FunctionName=function_name,
            Qualifier=qualifier,
            ProvisionedConcurrentExecutions=provisioned_concurrent_executions,
        )
        result["result"] = create_ret["result"]
        if not result["result"]:
            result["comment"] = create_ret["comment"]
            return result
        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.lambda.function_provisioned_concurrency_config",
            name=name,
        )
    if (not before) or resource_updated:
        after = (
            await hub.exec.aws.lambda_aws.function_provisioned_concurrency_config.get(
                ctx, name=name, function_name=function_name, qualifier=qualifier
            )
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
    """Deletes the provisioned concurrency configuration for a function.

    Args:
        name(str): An Idem name of the resource.
        resource_id(str, Optional): The Amazon Resource Name (ARN) of the function. Idem automatically considers this
            resource being absent if this field is not specified.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            function_provisioned_concurrency_config-01234672f3336db8:
              aws.lambda_aws.function_provisioned_concurrency_config.absent:
                - name: value
                - resource_id: value
    """
    already_absent_msg = hub.tool.aws.comment_utils.already_absent_comment(
        resource_type="aws.lambda.function_provisioned_concurrency_config", name=name
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

    before = await hub.exec.aws.lambda_aws.function_provisioned_concurrency_config.get(
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
                resource_type="aws.lambda.function_provisioned_concurrency_config",
                name=name,
            )
        else:
            function_name = hub.tool.aws.arn_utils.get_resource_name(resource_id)
            qualifier = hub.tool.aws.arn_utils.get_qualifier(resource_id)
            ret = await hub.exec.boto3.client[
                "lambda"
            ].delete_provisioned_concurrency_config(
                ctx, **{"FunctionName": function_name, "Qualifier": qualifier}
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = ret["comment"]
                return result
            result["comment"] = hub.tool.aws.comment_utils.delete_comment(
                resource_type="aws.lambda.function_provisioned_concurrency_config",
                name=name,
            )

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Retrieves a list of provisioned concurrency configurations for a function.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.lambda_aws.function_provisioned_concurrency_config
    """
    result = {}

    get_functions_ret = await hub.exec.boto3.client["lambda"].list_functions(ctx)
    if not get_functions_ret["result"]:
        hub.log.warning(f"Could not list functions {get_functions_ret['comment']}")
        return result

    for function in get_functions_ret["ret"]["Functions"]:
        function_name = function.get("FunctionName")
        list_concurrency_configs_ret = (
            await hub.exec.aws.lambda_aws.function_provisioned_concurrency_config.list(
                ctx, function_name=function_name
            )
        )

        if not list_concurrency_configs_ret["result"]:
            hub.log.debug(
                f"Could not list provisioned concurrency configs for functionName '{function_name}': "
                f"{list_concurrency_configs_ret['comment']}. Describe will skip this function and continue."
            )
            continue

        for function_concurrency_config in list_concurrency_configs_ret["ret"]:
            # We set function ARN as name of the resource when performing describe
            resource_arn = function_concurrency_config.get("name")
            result[resource_arn] = {
                "aws.lambda.function_provisioned_concurrency_config.present": [
                    {parameter_key: parameter_value}
                    for parameter_key, parameter_value in function_concurrency_config.items()
                ]
            }
    return result
