import copy
from collections import OrderedDict
from typing import Any
from typing import Dict
from typing import List

STATE_NAME = "aws.neptune.db_instance"


async def search_raw(
    hub, ctx, name: str, resource_id: str = None, filters: List = None
) -> Dict:
    """
    Fetch one or more neptune db instances from AWS. The return will be in the same format as what the boto3 api returns.

    Args:
        name(str): The name of the Idem state.
        resource_id(str, Optional): AWS Neptune DBInstanceIdentifier to identify the resource.
        filters(list, Optional): A filter that specifies one or more DB instances to describe.
            Supported filters:
            db-cluster-id - Accepts DB cluster identifiers and DB cluster Amazon Resource Names (ARNs). The results list will only include information about the DB instances associated with the DB clusters identified by these ARNs.
            engine - Accepts an engine name (such as neptune ), and restricts the results list to DB instances created by that engine.

    Returns:
        {"result": True|False, "comment": A message List, "ret": Dict}
    """
    result = dict(comment=[], ret=None, result=True)
    syntax_validation = hub.tool.aws.search_utils.search_filter_syntax_validation(
        filters=filters
    )
    if not syntax_validation["result"]:
        result["result"] = False
        result["comment"] = list(syntax_validation["comment"])
        return result
    boto3_filter = hub.tool.aws.search_utils.convert_search_filter_to_boto3(
        filters=filters
    )
    ret = await hub.exec.boto3.client.neptune.describe_db_instances(
        ctx,
        DBInstanceIdentifier=resource_id if resource_id else None,
        Filters=boto3_filter,
    )
    result["result"] = ret["result"]
    result["comment"] = list(ret["comment"])
    result["ret"] = ret["ret"]
    return result


async def update(
    hub,
    ctx,
    name: str,
    resource_id: str,
    desired_state: Dict,
    is_created: bool,
    timeout: Dict,
) -> Dict[str, Any]:
    """
    Updates the neptune db instance represented by the provided resource_id to the desired state.
    If is_created flag is set to True, the comment in result is not updated as it is assumed that
    the resource is being updated right after it was created to apply remaining parameters.
    """
    # below is the mapping of boto3 string parameters applicable for modification of neptune db_instance in idem
    # it contains all accepted string parameters
    modify_str_params = OrderedDict(
        {
            "DBInstanceClass": "db_instance_class",
            "DBSubnetGroupName": "db_subnet_group_name",
            "MasterUserPassword": "master_user_password",
            "DBParameterGroupName": "db_parameter_group_name",
            "BackupRetentionPeriod": "backup_retention_period",
            "PreferredBackupWindow": "preferred_backup_window",
            "PreferredMaintenanceWindow": "preferred_maintenance_window",
            "EngineVersion": "engine_version",
            "LicenseModel": "license_model",
            "OptionGroupName": "option_group_name",
            "StorageType": "storage_type",
            "TdeCredentialArn": "tde_credential_arn",
            "TdeCredentialPassword": "tde_credential_password",
            "CACertificateIdentifier": "ca_certificate_identifier",
            "Domain": "domain",
            "MonitoringRoleArn": "monitoring_role_arn",
            "DomainIAMRoleName": "domain_iam_role_name",
            "PerformanceInsightsKMSKeyId": "performance_insights_kms_key_id",
        }
    )
    # below is mapping of boto3 list params applicable for modifying neptune db_instance
    modify_list_of_str_params = {
        "DBSecurityGroups": "db_security_groups",
        "VpcSecurityGroupIds": "vpc_security_group_ids",
    }
    # below is mapping of boto3 int params applicable for modifying neptune db_instance
    modify_int_params = {
        "AllocatedStorage": "allocated_storage",
        "DBPortNumber": "port",
        "Iops": "iops",
        "MonitoringInterval": "monitoring_interval",
        "PromotionTier": "promotion_tier",
    }
    # below is mapping of boto3 bool params applicable for modifying neptune db_instance
    modify_bool_params = {
        "MultiAZ": "multi_az",
        "ApplyImmediately": "apply_immediately",
        "AllowMajorVersionUpgrade": "allow_major_version_upgrade",
        "AutoMinorVersionUpgrade": "auto_minor_version_upgrade",
        "PubliclyAccessible": "publicly_accessible",
        "CopyTagsToSnapshot": "copy_tags_to_snapshot",
        "EnableIAMDatabaseAuthentication": "enable_iam_database_authentication",
        "EnablePerformanceInsights": "enable_performance_insights",
        "DeletionProtection": "deletion_protection",
    }

    result = dict(comment=[], old_state=None, new_state=None, result=True)
    if ctx.get("test", False) and is_created:
        current_state = desired_state
    else:
        current_state_result = await hub.exec.aws.neptune.db_instance.get(
            ctx=ctx, name=name, resource_id=resource_id
        )
        if not (
            current_state_result
            and current_state_result["result"]
            and current_state_result["ret"]
        ):
            result["result"] = False
            result["comment"] = current_state_result["comment"]
            return result
        current_state = current_state_result["ret"]
    if not is_created:
        result["old_state"] = current_state
    resource_arn = current_state.get("db_instance_arn")
    params_to_modify = {}
    plan_state = copy.deepcopy(current_state)

    # create a dict 'params_to_modify' of raw parameter key of type string mapped to desired string value,
    # where the desired value is not none and current value does not match desired value

    # process all string parameters
    for param_raw, param_present in modify_str_params.items():
        if type(desired_state.get(param_present)) == str and current_state.get(
            param_present
        ) != desired_state.get(param_present):
            params_to_modify[param_raw] = desired_state[param_present]
            plan_state[param_present] = desired_state[param_present]

    # process list[string] data
    for param_raw, param_present in modify_list_of_str_params.items():
        if type(desired_state.get(param_present)) == list and set(
            current_state.get(param_present)
        ) != set(desired_state.get(param_present)):
            params_to_modify[param_raw] = desired_state[param_present]
            plan_state[param_present] = desired_state[param_present]

    # process integer params
    for param_raw, param_present in modify_int_params.items():
        if type(desired_state.get(param_present)) == int and current_state.get(
            param_present
        ) != desired_state.get(param_present):
            params_to_modify[param_raw] = desired_state[param_present]
            plan_state[param_present] = desired_state[param_present]

    # process bools
    for param_raw, param_present in modify_bool_params.items():
        if type(desired_state.get(param_present)) == bool and current_state.get(
            param_present
        ) != desired_state.get(param_present):
            params_to_modify[param_raw] = desired_state[param_present]
            plan_state[param_present] = desired_state[param_present]

    # process CloudwatchLogsExportConfiguration as a special case, since this parameter is not part of describe and is not returned by AWS
    # If user specifies this, just pass it along to boto3 and consider this resource to be updated
    if desired_state.get("CloudwatchLogsExportConfiguration"):
        params_to_modify["CloudwatchLogsExportConfiguration"] = desired_state[
            "cloudwatch_logs_export_configuration"
        ]
        plan_state[param_present] = desired_state[param_present]

    # if we have some parameters to modify, apply it
    if params_to_modify:
        if ctx.get("test", False):
            if not is_created:
                result["comment"] = hub.tool.aws.comment_utils.would_update_comment(
                    resource_type=STATE_NAME, name=name
                )
        else:
            modify_db_instance_result = (
                await hub.exec.boto3.client.neptune.modify_db_instance(
                    ctx, DBInstanceIdentifier=resource_id, **params_to_modify
                )
            )
            if not modify_db_instance_result["result"]:
                result["comment"] = modify_db_instance_result["comment"]
                result["result"] = False
                return result
            # wait for update of instance
            waiter_config = hub.tool.aws.waiter_utils.create_waiter_config(
                default_delay=15,
                default_max_attempts=40,
                timeout_config=timeout.get("update") if timeout else None,
            )
            try:
                await hub.tool.boto3.client.wait(
                    ctx,
                    "neptune",
                    "db_instance_available",
                    None,
                    30,
                    DBInstanceIdentifier=resource_id,
                    WaiterConfig=waiter_config,
                )
            except Exception as e:
                result["comment"] += [str(e)]
                result["result"] = False
            if not is_created:
                result["comment"] = result[
                    "comment"
                ] + hub.tool.aws.comment_utils.update_comment(
                    resource_type=STATE_NAME, name=name
                )

    # modify tags if it has changed
    old_tags = current_state.get("tags")
    new_tags = desired_state.get("tags")
    if new_tags is not None and new_tags != old_tags:
        # below code updates tags on AWS only if it is not a test run
        update_tags_ret = await hub.tool.aws.neptune.tag.update_tags(
            ctx=ctx,
            resource_arn=resource_arn,
            old_tags=old_tags,
            new_tags=new_tags,
        )
        if not update_tags_ret["result"]:
            result["comment"] = update_tags_ret["comment"]
            result["result"] = False
            hub.log.debug(f"Failed updating tags for aws.neptune.db_instance '{name}'")
            return result
        # update comment if tags were updated
        if not is_created:
            result["comment"] = hub.tool.aws.comment_utils.update_comment(
                resource_type=STATE_NAME, name=name
            )
            result["comment"] += update_tags_ret["comment"]

        if ctx.get("test", False) and update_tags_ret["ret"] is not None:
            plan_state["tags"] = update_tags_ret["ret"]
            if not is_created:
                result["comment"] = hub.tool.aws.comment_utils.would_update_comment(
                    resource_type=STATE_NAME, name=resource_id
                )
                result["comment"] += update_tags_ret["comment"]

    # set new_state
    if ctx.get("test", False):
        result["new_state"] = plan_state
    else:
        current_db_instance_result = await hub.exec.aws.neptune.db_instance.get(
            ctx=ctx, name=name, resource_id=resource_id
        )
        if not (
            current_db_instance_result
            and current_db_instance_result["result"]
            and current_db_instance_result["ret"]
        ):
            result["result"] = False
            result["comment"] += current_db_instance_result["comment"]
            return result
        result["new_state"] = current_db_instance_result["ret"]

    return result
