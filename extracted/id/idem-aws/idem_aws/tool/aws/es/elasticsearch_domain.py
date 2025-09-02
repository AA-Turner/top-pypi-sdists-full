import copy
import json
from collections import OrderedDict
from typing import Any
from typing import Dict


async def update_elasticsearch_domain(
    hub,
    ctx,
    resource_id: str,
    current_state: Dict[str, Any],
    desired_state: Dict[str, Any],
    timeout: dict = None,
):
    """Modifies the cluster configuration of the specified Elasticsearch domain. Also allows to upgrade
    domain version.

    Args:
        resource_id(str): The name of the Elasticsearch domain
        current_state(Dict): Previous state of the resource
        desired_state(Dict): New parameters from SLS file.
        timeout(dict, Optional): Timeout configuration for updating AWS Elasticsearch domain.

    Returns:
        Dict[str, Any]
    """
    update_params = dict(
        {
            "DomainName": "domain_name",
            "ElasticsearchClusterConfig": "elastic_search_cluster_config",
            "EBSOptions": "ebs_options",
            "AccessPolicies": "access_policies",
            "SnapshotOptions": "snapshot_options",
            "VPCOptions": "vpc_options",
            "CognitoOptions": "cognito_options",
            "EncryptionAtRestOptions": "encryption_at_rest_options",
            "NodeToNodeEncryptionOptions": "node_to_node_encryption_options",
            "AdvancedOptions": "advanced_options",
            "LogPublishingOptions": "log_publishing_options",
            "DomainEndpointOptions": "domain_endpoint_options",
            "AdvancedSecurityOptions": "advanced_security_options",
            "AutoTuneOptions": "auto_tune_options",
            "DryRun": "dry_run",
        }
    )
    upgrade_params = dict(
        {
            "TargetVersion": "elastic_search_version",
            "PerformCheckOnly": "perform_check_only",
        }
    )

    result = dict(comment=[], result=True, ret=None)
    plan_state = copy.deepcopy(current_state)
    params_to_update = {}
    params_to_upgrade = {}

    # create a dict 'params_to_modify' of raw parameter key mapped to desired value,
    # where the desired value is not none and current value does not match desired value
    for param_raw, param_present in update_params.items():
        if desired_state.get(param_present) is not None and current_state.get(
            param_present
        ) != desired_state.get(param_present):
            params_to_update[param_raw] = desired_state[param_present]

    for param_raw, param_present in upgrade_params.items():
        if desired_state.get(param_present) is not None and current_state.get(
            param_present
        ) != desired_state.get(param_present):
            params_to_upgrade[param_raw] = desired_state[param_present]

    if params_to_update or params_to_upgrade:
        for key, value in params_to_update.items():
            plan_state[update_params.get(key)] = value
        for key, value in params_to_upgrade.items():
            plan_state[upgrade_params.get(key)] = value
        if ctx.get("test", False):
            result["comment"] = hub.tool.aws.comment_utils.would_update_comment(
                resource_type="aws.es.elasticsearch_domain",
                name=current_state["name"],
            )
        else:
            result["comment"] = hub.tool.aws.comment_utils.update_comment(
                resource_type="aws.es.elasticsearch_domain",
                name=current_state["name"],
            )
            waiter_config = hub.tool.aws.waiter_utils.create_waiter_config(
                default_delay=30,
                default_max_attempts=60,
                timeout_config=timeout.get("update") if timeout else None,
            )
            if params_to_update:
                update_ret = (
                    await hub.exec.boto3.client.es.update_elasticsearch_domain_config(
                        ctx, DomainName=resource_id, **params_to_update
                    )
                )
                if not update_ret["result"]:
                    result["result"] = False
                    result["comment"] = update_ret["comment"]
                    return result

                update_waiter_acceptors = [
                    {
                        "matcher": "path",
                        "expected": False,
                        "state": "success",
                        "argument": "DomainStatus.Processing",
                    },
                    {
                        "matcher": "path",
                        "expected": True,
                        "state": "retry",
                        "argument": "DomainStatus.Processing",
                    },
                ]
                update_domain_waiter = hub.tool.boto3.custom_waiter.waiter_wrapper(
                    name="ElasticsearchDomainUpdate",
                    operation="DescribeElasticsearchDomain",
                    argument=["DomainStatus.Processing"],
                    acceptors=update_waiter_acceptors,
                    client=await hub.tool.boto3.client.get_client(ctx, "es"),
                )
                try:
                    await hub.tool.boto3.client.wait(
                        ctx,
                        "es",
                        "ElasticsearchDomainUpdate",
                        update_domain_waiter,
                        DomainName=resource_id,
                        WaiterConfig=waiter_config,
                    )
                except Exception as e:
                    result["comment"] += [str(e)]
                    result["result"] = False
                    return result

            if params_to_upgrade:
                upgrade_ret = (
                    await hub.exec.boto3.client.es.upgrade_elasticsearch_domain(
                        ctx, DomainName=resource_id, **params_to_upgrade
                    )
                )
                if not upgrade_ret["result"]:
                    result["result"] = False
                    result["comment"] = upgrade_ret["comment"]
                    return result
                upgrade_waiter_acceptors = [
                    {
                        "matcher": "path",
                        "expected": False,
                        "state": "success",
                        "argument": "DomainStatus.UpgradeProcessing",
                    },
                    {
                        "matcher": "path",
                        "expected": True,
                        "state": "retry",
                        "argument": "DomainStatus.UpgradeProcessing",
                    },
                ]
                upgrade_domain_waiter = hub.tool.boto3.custom_waiter.waiter_wrapper(
                    name="ElasticsearchDomainUpgrade",
                    operation="DescribeElasticsearchDomain",
                    argument=["DomainStatus.UpgradeProcessing"],
                    acceptors=upgrade_waiter_acceptors,
                    client=await hub.tool.boto3.client.get_client(ctx, "es"),
                )
                try:
                    await hub.tool.boto3.client.wait(
                        ctx,
                        "es",
                        "ElasticsearchDomainUpgrade",
                        upgrade_domain_waiter,
                        DomainName=resource_id,
                        WaiterConfig=waiter_config,
                    )
                except Exception as e:
                    result["comment"] += [str(e)]
                    result["result"] = False

        result["ret"] = plan_state
    else:
        result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
            resource_type="aws.es.elasticsearch_domain",
            name=current_state["name"],
        )
    return result


def convert_raw_elasticsearch_domain_to_present(
    hub,
    raw_resource: Dict[str, Any],
    idem_resource_name: str = None,
    tags: Dict[str, str] = None,
) -> Dict[str, Any]:
    """
    Convert AWS returned data structure to correct idem elasticsearch_domain present state

     Args:
        raw_resource(Dict): The aws response to convert
        idem_resource_name(str, Optional): An Idem name of the resource.
        tags(Dict, Optional): tags for Elasticsearch domain.

    Returns:
        Dict[str, Any]
    """
    domain_name = raw_resource.get("DomainName")
    resource_parameters = OrderedDict(
        {
            "DomainName": "domain_name",
            "ElasticsearchVersion": "elastic_search_version",
            "ElasticsearchClusterConfig": "elastic_search_cluster_config",
            "EBSOptions": "ebs_options",
            "AccessPolicies": "access_policies",
            "SnapshotOptions": "snapshot_options",
            "VPCOptions": "vpc_options",
            "CognitoOptions": "cognito_options",
            "EncryptionAtRestOptions": "encryption_at_rest_options",
            "NodeToNodeEncryptionOptions": "node_to_node_encryption_options",
            "AdvancedOptions": "advanced_options",
            "LogPublishingOptions": "log_publishing_options",
            "DomainEndpointOptions": "domain_endpoint_options",
            "AdvancedSecurityOptions": "advanced_security_options",
            "AutoTuneOptions": "auto_tune_options",
        }
    )
    resource_translated = {
        "name": idem_resource_name if idem_resource_name else domain_name,
        "resource_id": domain_name,
    }
    for parameter_raw, parameter_present in resource_parameters.items():
        if raw_resource.get(parameter_raw) is not None:
            resource_translated[parameter_present] = json.loads(
                json.dumps(raw_resource.get(parameter_raw))
            )
    if tags:
        resource_translated["tags"] = tags.copy()

    return resource_translated
