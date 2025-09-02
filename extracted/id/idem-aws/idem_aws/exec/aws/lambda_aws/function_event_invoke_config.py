"""Exec module for managing Lambda function asynchronous invocation configuration"""
__func_alias__ = {"list_": "list"}


async def get(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    function_name: str = None,
    qualifier: str = None,
):
    """Get the configuration for asynchronous invocation for a function, version, or alias.

    Args:
        name(str): An Idem name of the resource.
        resource_id(str, Optional): The Amazon Resource Name (ARN) of the function. If not supplied, the function name is required to get the resource.
        function_name(str, Optional): The name of the Lambda function. If not supplied, function_name is parsed from the resource_id.
        qualifier(str, Optional): A version number or alias name. Defaults to None.

    Returns:
        .. code-block:: python

           {"result": True|False, "comment": A message List, "ret": None|Dict}

    Examples:
        Calling this exec module function from the cli with resource_id

        .. code-block:: bash

            idem exec aws.lambda_aws.function_event_invoke_config.get resource_id="resource_id" name="name"


        Calling this exec module function from the cli with function_name and qualifier.

        .. code-block:: bash

            idem exec aws.lambda_aws.function_event_invoke_config.get function_name="function_name" name="name"


        Calling this exec module function from within a state module in pure python

        .. code-block:: python

            async def state_function(hub, ctx, name, resource_id, **kwargs):
                ret = await aws.lambda_aws.function_event_invoke_config.get(ctx, resource_id=resource_id, name=name, **kwargs)
    """
    result = dict(comment=[], ret=None, result=True)

    if resource_id:
        function_name = hub.tool.aws.arn_utils.get_resource_name(resource_id)
        qualifier = hub.tool.aws.arn_utils.get_qualifier(resource_id)

    before = await hub.exec.boto3.client["lambda"].get_function_event_invoke_config(
        ctx, FunctionName=function_name, Qualifier=qualifier
    )

    if not before["result"]:
        if "ResourceNotFoundException" in str(before["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.lambda.function_event_invoke_config", name=name
                )
            )
            result["comment"] += list(before["comment"])
            return result
        result["result"] = False
        result["comment"] = list(before["comment"])
        return result

    result[
        "ret"
    ] = hub.tool.aws.lambda_aws.function_event_invoke_config.convert_raw_function_event_invoke_config_to_present(
        before["ret"], function_name=function_name, idem_resource_name=name
    )

    return result


async def list_(hub, ctx, function_name: str):
    """Retrieves a list of configurations for asynchronous invocation for a function.

    Args:
        function_name(str):
            The name of the Lambda function.
                Name formats
                    * Function name - my-function.
                    * Function ARN - ``arn:aws:lambda:us-west-2:123456789012:function:my-function``.
                    * Partial ARN - ``123456789012:function:my-function``.
    Returns:
        .. code-block:: python

           {"result": True|False, "comment": A message List, "ret": None|Dict}

    Examples:
        Calling this exec module function from the cli with function_name

        .. code-block:: bash

            idem exec aws.lambda_aws.function_event_invoke_config.list function_name="function_name"


        Calling this exec module function from within a state module in pure python

        .. code-block:: python

            async def state_function(hub, ctx, name, resource_id, **kwargs):
                ret = await aws.lambda_aws.function_event_invoke_config.list(ctx, function_name=function_name)
    """
    result = dict(comment=[], ret=[], result=True)

    list_event_invoke_configs_ret = await hub.exec.boto3.client[
        "lambda"
    ].list_function_event_invoke_configs(ctx, FunctionName=function_name)
    if not list_event_invoke_configs_ret["result"]:
        result["comment"].append(
            f"Could not get event invoke config for functionName '{function_name}': "
            f"{list_event_invoke_configs_ret['comment']}."
        )
        result["result"] = False
        return result

    for function_event_invoke_config in list_event_invoke_configs_ret["ret"][
        "FunctionEventInvokeConfigs"
    ]:
        result["ret"].append(
            hub.tool.aws.lambda_aws.function_event_invoke_config.convert_raw_function_event_invoke_config_to_present(
                function_event_invoke_config,
                function_name=function_name,
            )
        )
    return result
