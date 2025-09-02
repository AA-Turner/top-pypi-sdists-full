"""State module for managing Amazon Configuration Aggregator."""
import copy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    account_aggregation_sources: List[
        make_dataclass(
            "AccountAggregationSource",
            [
                ("AccountIds", List[str]),
                ("AllAwsRegions", bool, field(default=None)),
                ("AwsRegions", List[str], field(default=None)),
            ],
        )
    ] = None,
    organization_aggregation_source: make_dataclass(
        "OrganizationAggregationSource",
        [
            ("RoleArn", str),
            ("AwsRegions", List[str], field(default=None)),
            ("AllAwsRegions", bool, field(default=None)),
        ],
    ) = None,
    tags: List[
        make_dataclass(
            "Tag",
            [("Key", str, field(default=None)), ("Value", str, field(default=None))],
        )
    ] = None,
) -> Dict[str, Any]:
    """Creates an Amazon Configuration Aggregator.

    Creates and updates the configuration aggregator with the selected source accounts and regions.

    Args:
        name(str):
            An Idem name of the resource.

        resource_id(str, Optional):
            An identifier of the resource in the provider, a name of Configuration Aggregator. Defaults to None.

        account_aggregation_sources(List[Dict[str, Any]], Optional):
            A list of AccountAggregationSource object. Defaults to None.
                * AccountIds (List[str]): The 12-digit account ID of the account being aggregated.
                * AllAwsRegions (bool, optional): If true, aggregate existing Config regions and future regions.
                * AwsRegions (List[str], optional): The source regions being aggregated.

        organization_aggregation_source(Dict[str, Any], Optional):
            An OrganizationAggregationSource object. Defaults to None.
                * RoleArn (str): ARN of the IAM role.
                * AwsRegions (List[str], optional): The source regions being aggregated.
                * AllAwsRegions (bool, optional): If true, aggregate existing Config regions and future regions.

        tags(List[Dict[str, Any]], Optional): An array of tag object. Defaults to None.
            * Key (str, optional): One part of a key-value pair that make up a tag. A key is a general label that acts like a
            category for more specific tag values.
            * Value (str, optional): The optional part of a key-value pair that make up a tag. A value acts as a descriptor within a
            tag category (key).

    Request Syntax:
        aws.config.configuration_aggregator.present:
            - name: 'string'
            - resource_id: 'string'
            - account_aggregation_sources:
                - AccountIds:
                    - 'string'
                  AllAwsRegions: True|False
                  AwsRegions:
                    - 'string'
            organization_aggregation_source:
                - RoleArn: 'string'
                  AwsRegions:
                    - 'string'
                  AwsRegions: True|False

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_present:
              aws.config.configuration_aggregator.present:
                - name: value
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    before = None
    resource_updated = False
    if not resource_id:
        resource_id = name
    if resource_id:
        before = await hub.exec.aws.config.configuration_aggregator.get(
            ctx, name=resource_id
        )
    if before["ret"]:
        result["old_state"] = before["ret"]
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "account_aggregation_sources": account_aggregation_sources,
                    "organization_aggregation_source": organization_aggregation_source,
                    "tags": tags,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_update_comment(
                resource_type="aws.config.configuration_aggregator", name=name
            )
            return result
        resource_updated = (
            await hub.tool.aws.config.config_utils.is_configuration_aggregator_updated(
                before=before["ret"],
                account_aggregation_sources=account_aggregation_sources,
                organization_aggregation_source=organization_aggregation_source,
            )
        )
        if resource_updated:
            ret = await hub.exec.boto3.client.config.put_configuration_aggregator(
                ctx,
                ConfigurationAggregatorName=name,
                AccountAggregationSources=account_aggregation_sources,
                OrganizationAggregationSource=organization_aggregation_source,
                Tags=tags,
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = ret["comment"]
                return result
            result["comment"] = hub.tool.aws.comment_utils.update_comment(
                resource_type="aws.config.configuration_aggregator", name=name
            )
        else:
            result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
                resource_type="aws.config.configuration_aggregator", name=name
            )
            result["new_state"] = copy.deepcopy(result["old_state"])
        return result
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "account_aggregation_sources": account_aggregation_sources,
                    "organization_aggregation_source": organization_aggregation_source,
                    "tags": tags,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.config.configuration_aggregator", name=resource_id
            )
            return result

        ret = await hub.exec.boto3.client.config.put_configuration_aggregator(
            ctx,
            ConfigurationAggregatorName=name,
            AccountAggregationSources=account_aggregation_sources,
            OrganizationAggregationSource=organization_aggregation_source,
            Tags=tags,
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.config.configuration_aggregator", name=resource_id
        )

        if before or resource_updated:
            resource_id = ret["ret"]["ConfigurationAggregator"][
                "ConfigurationAggregatorName"
            ]
            after = await hub.exec.aws.config.configuration_aggregator.get(
                ctx, name=resource_id
            )
            result["new_state"] = after["ret"]
        else:
            result["new_state"] = copy.deepcopy(result["old_state"])
    return result


async def absent(hub, ctx, name: str, resource_id: str = None) -> Dict[str, Any]:
    """Deletes the specified configuration aggregator and the aggregated data associated with the aggregator.

    Args:
        name(str):
            An Idem name of the resource.

        resource_id(str, Optional):
            An identifier of the resource in the provider.

    Request Syntax:
        aws.config.configuration_aggregator.absent:
            - name: 'string'
            - resource_id: 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_absent:
              aws.config.configuration_aggregator.absent:
                - name: value
                - resource_id: value
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        resource_id = name
    before = await hub.exec.aws.config.configuration_aggregator.get(
        ctx, name=resource_id
    )
    if not before["ret"]:
        result["old_state"] = before["ret"]
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.config.configuration_aggregator", name=name
        )
    elif ctx.get("test", False):
        result["old_state"] = before["ret"]

        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.config.configuration_aggregator", name=name
        )
        return result
    else:
        result["old_state"] = before["ret"]

        ret = await hub.exec.boto3.client.config.delete_configuration_aggregator(
            ctx, ConfigurationAggregatorName=name
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.config.configuration_aggregator", name=name
        )

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Examples:
        .. code-block:: bash

            $ idem describe aws.config.configuration_aggregator
    """
    result = {}
    ret = await hub.exec.aws.config.configuration_aggregator.list(ctx)

    if not ret["result"]:
        hub.log.warning(f"Could not describe configuration_aggregator {ret['comment']}")
        return {}

    for configuration_aggregator in ret["ret"]:
        result[configuration_aggregator["name"]] = {
            "aws.config.configuration_aggregator.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in configuration_aggregator.items()
            ]
        }
    return result
