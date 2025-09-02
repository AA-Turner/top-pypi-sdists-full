from typing import Any
from typing import Dict


def convert_raw_function_concurrency_config_to_present(
    hub,
    raw_resource: Dict[str, Any],
    function_name: str = None,
    idem_resource_name: str = None,
    function_arn: str = None,
) -> Dict[str, Any]:
    """
    Convert AWS returned data structure to correct idem function_provisioned_concurrency_config present state

     Args:
        hub: required for functions in hub
        raw_resource(Dict): The aws response to convert
        function_name (str, Optional): The name of the Lambda function
        idem_resource_name(str, Optional): An Idem name of the resource.
        function_arn(str, Optional): The Amazon Resource Name (ARN) of the function alias or version.

    Returns: Valid idem state for function_provisioned_concurrency_config of type Dict['string', Any]
    """

    function_arn_from_resource = raw_resource.get("FunctionArn")
    function_arn = (
        function_arn_from_resource if function_arn_from_resource else function_arn
    )

    resource_translated = {
        "name": idem_resource_name if idem_resource_name else function_arn,
        "resource_id": function_arn,
        "function_name": function_name,
    }

    provisioned_concurrent_executions = raw_resource.get(
        "RequestedProvisionedConcurrentExecutions"
    )
    if provisioned_concurrent_executions is not None:
        resource_translated[
            "provisioned_concurrent_executions"
        ] = provisioned_concurrent_executions

    qualifier = hub.tool.aws.arn_utils.get_qualifier(function_arn)
    if qualifier:
        resource_translated["qualifier"] = qualifier

    return resource_translated
