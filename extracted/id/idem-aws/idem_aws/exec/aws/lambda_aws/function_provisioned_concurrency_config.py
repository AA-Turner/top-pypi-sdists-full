"""Exec module for managing Lambda provisioned concurrency config."""
__func_alias__ = {"list_": "list"}


async def get(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    function_name: str = None,
    qualifier: str = None,
):
    """Get the provisioned concurrency configuration for a function's alias or version.

    Args:
        name(str): An Idem name of the resource.
        resource_id(str, Optional): The Amazon Resource Name (ARN) of the function. If not supplied, the function name and qualifier are required to get the resource.
        function_name(str, Optional): The name of the Lambda function, version, or alias. If not supplied, the function name will be extracted fom the resource_id.
        qualifier(str, Optional): A version number or alias name.  If not supplied, the qualifier will be extracted fom the resource_id.

    Returns:
        .. code-block:: python

           {"result": True|False, "comment": A message List, "ret": None|Dict}

    Examples:
        Calling this exec module function from the cli with resource_id

        .. code-block:: bash

            idem exec aws.lambda_aws.function_provisioned_concurrency_config.get resource_id="resource_id" name="name"


        Calling this exec module function from the cli with function_name and qualifier.

        .. code-block:: bash

            idem exec aws.lambda_aws.function_provisioned_concurrency_config.get function_name="function_name" qualifier="qualifier" name="name"


        Calling this exec module function from within a state module in pure python

        .. code-block:: python

            async def state_function(hub, ctx, name, resource_id, **kwargs):
                ret = await aws.lambda_aws.function_provisioned_concurrency_config.get(ctx, resource_id=resource_id, name=name, **kwargs)
    """
    result = dict(comment=[], ret=None, result=True)

    if resource_id:
        function_name = hub.tool.aws.arn_utils.get_resource_name(resource_id)
        qualifier = hub.tool.aws.arn_utils.get_qualifier(resource_id)

    before = await hub.exec.boto3.client["lambda"].get_provisioned_concurrency_config(
        ctx, FunctionName=function_name, Qualifier=qualifier
    )

    if not before["result"]:
        if "ProvisionedConcurrencyConfigNotFoundException" in str(before["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.lambda.function_provisioned_concurrency_config",
                    name=name,
                )
            )
            result["comment"] += list(before["comment"])
            return result
        result["result"] = False
        result["comment"] = list(before["comment"])
        return result

    # get_provisioned_concurrency_config method does not return function ARN. Hence build function ARN which will be set as resource_id
    account_details = await hub.exec.boto3.client.sts.get_caller_identity(ctx)
    account_id = account_details["ret"]["Account"]
    region_name = ctx["acct"]["region_name"]
    function_arn = hub.tool.aws.arn_utils.build(
        service="lambda",
        region=region_name,
        account_id=account_id,
        resource="function:" + function_name + ":" + qualifier,
    )

    result[
        "ret"
    ] = hub.tool.aws.lambda_aws.function_provisioned_concurrency_config.convert_raw_function_concurrency_config_to_present(
        before["ret"],
        function_name=function_name,
        idem_resource_name=name,
        function_arn=function_arn,
    )

    return result


async def list_(hub, ctx, function_name: str):
    """Retrieves a list of provisioned concurrency configurations for a function.

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

            idem exec aws.lambda_aws.function_provisioned_concurrency_config.list function_name="function_name"


        Calling this exec module function from within a state module in pure python

        .. code-block:: python

            async def state_function(hub, ctx, name, resource_id, **kwargs):
                ret = await aws.lambda_aws.function_provisioned_concurrency_config.list(ctx, function_name=function_name)
    """
    result = dict(comment=[], ret=[], result=True)

    list_provisioned_concurrency_configs_ret = await hub.exec.boto3.client[
        "lambda"
    ].list_provisioned_concurrency_configs(ctx, FunctionName=function_name)
    if not list_provisioned_concurrency_configs_ret["result"]:
        result["comment"] += list(list_provisioned_concurrency_configs_ret["comment"])
        result["result"] = False
        return result

    for (
        function_provisioned_concurrency_config
    ) in list_provisioned_concurrency_configs_ret["ret"][
        "ProvisionedConcurrencyConfigs"
    ]:
        result["ret"].append(
            hub.tool.aws.lambda_aws.function_provisioned_concurrency_config.convert_raw_function_concurrency_config_to_present(
                function_provisioned_concurrency_config,
                function_name=function_name,
            )
        )
    return result
