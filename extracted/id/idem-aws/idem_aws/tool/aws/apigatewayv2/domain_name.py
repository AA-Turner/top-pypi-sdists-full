from collections import OrderedDict
from typing import Any
from typing import Dict
from typing import List

"""
Util functions for AWS API Gateway v2 Domain Name resources.
"""


async def update(
    hub,
    ctx,
    resource_id: str,
    raw_resource: Dict[str, Any],
    resource_parameters: Dict[str, None],
) -> Dict[str, Any]:
    """
    Updates an AWS API Gateway v2 Domain Name resource.

    Args:
        hub: required for functions in hub.
        ctx: context.
        resource_id(str): The Domain Name resource identifier in Amazon Web Services.
        raw_resource(Dict): Existing resource parameters in Amazon Web Services.
        resource_parameters(Dict): Parameters from SLS file.

    Returns:
        Dict[str, Any]
    """

    result = dict(comment=[], result=True, ret=None)

    parameters = OrderedDict(
        {
            "domain_name_configurations": "DomainNameConfigurations",
            "mutual_tls_authentication": "MutualTlsAuthentication",
        }
    )

    parameters_to_update = {}

    domain_name_configurations = resource_parameters.get("domain_name_configurations")
    if domain_name_configurations is not None:
        if not hub.tool.aws.apigatewayv2.domain_name.are_domain_name_configurations_identical(
            domain_name_configurations,
            raw_resource.get("domain_name_configurations"),
        ):
            parameters_to_update[
                "DomainNameConfigurations"
            ] = domain_name_configurations

        resource_parameters.pop("domain_name_configurations")

    for key, value in resource_parameters.items():
        if value is not None and value != raw_resource.get(key):
            parameters_to_update[parameters[key]] = resource_parameters[key]

    if parameters_to_update:
        result["ret"] = {}
        for parameter_present, parameter_raw in parameters.items():
            if parameter_raw in parameters_to_update:
                result["ret"][parameter_present] = parameters_to_update[parameter_raw]

        if ctx.get("test", False):
            result["comment"] = (
                f"Would update parameters: " + ",".join(result["ret"].keys()),
            )
        else:
            update_ret = await hub.exec.boto3.client.apigatewayv2.update_domain_name(
                ctx,
                DomainName=resource_id,
                **parameters_to_update,
            )
            if not update_ret["result"]:
                result["result"] = False
                result["comment"] = update_ret["comment"]
                return result

            result["comment"] = (
                f"Updated parameters: " + ",".join(result["ret"].keys()),
            )

    return result


def convert_raw_domain_name_to_present(
    hub, raw_resource: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Convert AWS API Gateway v2 Domain Name resource to a common idem present state.

    Args:
        hub: required for functions in hub.
        raw_resource(Dict[str, Any]): The AWS response to convert.

    Returns:
        Dict[str, Any]: Common idem present state
    """

    resource_parameters = OrderedDict(
        {
            "ApiMappingSelectionExpression": "api_mapping_selection_expression",
            "DomainNameConfigurations": "domain_name_configurations",
            "MutualTlsAuthentication": "mutual_tls_authentication",
            "Tags": "tags",
        }
    )
    resource_translated = {
        "resource_id": raw_resource.get("DomainName"),
        "name": raw_resource.get("DomainName"),
    }

    for parameter_raw, parameter_present in resource_parameters.items():
        if raw_resource.get(parameter_raw) is not None:
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)

    return resource_translated


def are_domain_name_configurations_identical(
    hub,
    new_configuration: List,
    old_configuration: List,
) -> bool:
    """
    Compares the new and old domain name configurations.

    Args:
        hub: required for functions in hub.
        new_configuration(List): The new domain name configuration parameters.
        old_configuration(List): The old domain name configuration parameters.

    Returns:
        bool: true if there are no differences between the new and old domain name configurations.
    """

    if (new_configuration is None or len(new_configuration) == 0) and (
        old_configuration is None or len(old_configuration) == 0
    ):
        return True
    if (
        new_configuration is None
        or len(new_configuration) == 0
        or old_configuration is None
        or len(old_configuration) == 0
    ):
        return False

    diff = [
        i
        for i in new_configuration + old_configuration
        if i not in new_configuration or i not in old_configuration
    ]

    return len(diff) == 0
