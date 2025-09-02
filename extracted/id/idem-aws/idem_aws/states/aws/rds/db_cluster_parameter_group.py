"""
hub.exec.boto3.client.rds.copy_db_cluster_parameter_group
hub.exec.boto3.client.rds.create_db_cluster_parameter_group
hub.exec.boto3.client.rds.delete_db_cluster_parameter_group
hub.exec.boto3.client.rds.describe_db_cluster_parameter_groups
hub.exec.boto3.client.rds.modify_db_cluster_parameter_group
hub.exec.boto3.client.rds.reset_db_cluster_parameter_group
"""
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
    db_parameter_group_family: str,
    description: str,
    resource_id: str = None,
    tags: Dict[str, Any]
    or List[
        make_dataclass("Tag", [("Key", str), ("Value", str, field(default=None))])
    ] = None,
    parameters: List[
        make_dataclass(
            "Parameter",
            [
                ("ParameterName", str),
                ("ParameterValue", str),
                ("ApplyMethod", str, field(default=None)),
            ],
        )
    ] = None,
) -> Dict[str, Any]:
    """Creates a new DB cluster parameter group.

    Parameters in a DB cluster parameter group apply to all of the instances in a DB cluster.

    A DB cluster parameter group is initially created with the default parameters for the database engine used by
    instances in the DB cluster. To provide custom values for any of the parameters, you must modify the group after
    creating it using ModifyDBClusterParameterGroup. Once you've created a DB cluster parameter group, you need to
    associate it with your DB cluster using ModifyDBCluster.

    When you associate a new DB cluster parameter group with a running Aurora DB cluster, reboot the DB instances in the
    DB cluster without failover for the new DB cluster parameter group and associated settings to take effect.

    Args:
        name(str):
            An Idem name of the resource.

        resource_id(str, Optional):
            AWS DB Cluster Parameter Group name.

        db_parameter_group_family(str):
            The DB cluster parameter group family name. A DB cluster parameter group can be associated with one and
            only one DB cluster parameter group family, and can be applied only to a DB cluster running a database
            engine and engine version compatible with that DB cluster parameter group family.

            Example: ``aurora5.6``, ``aurora-postgresql9.6``, ``mysql8.0``, etc.

        description(str):
            The description for the DB cluster parameter group.

        tags(Dict or List, Optional):
            Dict in the format of {tag-key: tag-value} or List of tags in the format of ``[{"Key": tag-key, "Value":
            tag-value}]`` to associate with the DB cluster parameter group.  Each tag consists of a key name and an
            associated value. Defaults to None.

            * Key (str, Optional): The key of the tag. Constraints: Tag keys are case-sensitive and accept a maximum of
              127 Unicode characters. May not begin with aws:.

            * Value(str, Optional): The value of the tag. Constraints: Tag values are case-sensitive and accept a
              maximum of 256 Unicode characters.

        parameters(List, Optional):
            Parameters in the DB parameter group. Defaults to None.

            Parameter support the following:

            * ParameterName (str): Specifies the name of the parameter.
            * ParameterValue (str): Specifies the value of the parameter.
            * ApplyMethod (str, Optional): Indicates when to apply parameter updates.

    Request Syntax:
        .. code-block:: sls

          [db-cluster-parameter-group-name]:
            aws.rds.db_cluster_parameter_group.present:
              - name: 'string'
              - resource_id: 'string'
              - db_parameter_group_family: 'string'
              - description: 'string'
              - tags:
                  - Key: 'string'
                    Value: 'string'
              - parameters:
                  - ParameterName: 'aurora_disable_hash_join'
                    ParameterValue: '1'
                    ApplyMethod: 'immediate'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_present:
              aws.rds.db_cluster_parameter_group.present:
                - name: db-cluster-parameter-group-1
                - resource_id: db-cluster-parameter-group-1
                - db_parameter_group_family: aurora-5.6
                - description: Test description
                - tags:
                    - Key: Name
                      Value: db-cluster-parameter-group-1
                - parameters:
                    - ParameterName: 'aurora_disable_hash_join'
                      ParameterValue: '1'
                      ApplyMethod: 'immediate'
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    before = None
    resource_updated = False
    plan_state = None

    tags = (
        hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags)
        if isinstance(tags, List)
        else tags
    )
    if resource_id:
        before = await hub.exec.aws.rds.db_cluster_parameter_group.get(
            ctx=ctx, resource_id=resource_id, name=name
        )
        if not before["result"] or not before["ret"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result

        result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
            resource_type="aws.rds.db_cluster_parameter_group", name=name
        )
        result["old_state"] = copy.deepcopy(before["ret"])
        plan_state = copy.deepcopy(result["old_state"])

        # Update tags
        if tags is not None:
            update_tags_ret = await hub.exec.aws.rds.tag.update_rds_tags(
                ctx=ctx,
                resource_arn=result["old_state"].get("db_cluster_parameter_group_arn"),
                old_tags=result["old_state"].get("tags"),
                new_tags=tags,
            )
            result["comment"] += update_tags_ret["comment"]
            result["result"] = update_tags_ret["result"]
            resource_updated = update_tags_ret["result"]
            if ctx.get("test", False) and update_tags_ret["ret"] is not None:
                plan_state["tags"] = update_tags_ret["ret"]
        if parameters is not None:
            update_ret = (
                await hub.tool.aws.rds.parameters.modify_db_cluster_parameter_group(
                    ctx=ctx,
                    resource_name=result["old_state"].get("resource_id"),
                    old_parameters=result["old_state"].get("parameters"),
                    new_parameters=parameters,
                )
            )
            result["comment"] += update_ret["comment"]
            result["result"] = result["result"] and update_ret["result"]
            resource_updated = resource_updated or bool(update_ret["ret"])
            if ctx.get("test", False) and update_ret["ret"] is not None:
                plan_state["parameters"] = update_ret["ret"].get("parameters")
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "resource_id": resource_id,
                    "db_parameter_group_family": db_parameter_group_family,
                    "description": description,
                    "tags": tags,
                    "parameters": parameters,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.rds.db_cluster_parameter_group", name=name
            )
            return result
        ret = await hub.exec.boto3.client.rds.create_db_cluster_parameter_group(
            ctx,
            **{
                "DBClusterParameterGroupName": name,
                "DBParameterGroupFamily": db_parameter_group_family,
                "Description": description,
                "Tags": hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags)
                if tags
                else None,
            },
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result

        resource_id = ret["ret"]["DBClusterParameterGroup"][
            "DBClusterParameterGroupName"
        ]
        result["new_state"] = {"name": name, "resource_id": resource_id}

        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.rds.db_cluster_parameter_group", name=name
        )

        # Modify the db cluster group parameters
        if parameters is not None:
            ret_parameter = (
                await hub.exec.boto3.client.rds.describe_db_cluster_parameters(
                    ctx, DBClusterParameterGroupName=resource_id
                )
            )
            if not ret_parameter["result"]:
                result["comment"] += ret_parameter["comment"]
                result["result"] = ret_parameter["result"]
            else:
                update_ret = (
                    await hub.tool.aws.rds.parameters.modify_db_cluster_parameter_group(
                        ctx=ctx,
                        resource_name=resource_id,
                        old_parameters=ret_parameter["ret"]["Parameters"],
                        new_parameters=parameters,
                    )
                )

                result["comment"] += update_ret["comment"]
                result["result"] = result["result"] and update_ret["result"]
    try:
        if ctx.get("test", False):
            result["new_state"] = plan_state
        elif (not before) or resource_updated:
            after = await hub.exec.aws.rds.db_cluster_parameter_group.get(
                ctx=ctx, resource_id=resource_id, name=name
            )
            if not after["result"] or not after["ret"]:
                result["result"] = False
                result["comment"] += after["comment"]
                return result
            result["new_state"] = copy.deepcopy(after["ret"])
        else:
            result["new_state"] = copy.deepcopy(result["old_state"])
    except Exception as e:
        result["comment"] += [str(e)]
        result["result"] = False
    return result


async def absent(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
) -> Dict[str, Any]:
    """
    Deletes a specified DB cluster parameter group. The DB cluster parameter group to be deleted can't be associated
    with any DB clusters. For more information on Amazon Aurora, see  What is Amazon Aurora? in the Amazon Aurora
    User Guide.  For more information on Multi-AZ DB clusters, see  Multi-AZ deployments with two readable standby
    DB instances in the Amazon RDS User Guide.

    Args:
        name(str):
            An Idem name of the resource

        resource_id(str, Optional):
            AWS DB Cluster Parameter Group name. Constraints: Must be the name of an existing DB cluster parameter
            group. You can't delete a default DB cluster parameter group. Can't be associated with any DB clusters.

    Request Syntax:
        .. code-block:: sls

            [resource-id]:
              aws.rds.db_cluster_parameter_group.absent:
                - name: 'string'
                - resource_id: 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_absent:
              aws.rds.db_cluster_parameter_group.absent:
                - name: db-cluster-parameter-group-test-name
                - resource_id: db-cluster-parameter-group-test-name
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.rds.db_cluster_parameter_group", name=name
        )
        return result
    before = await hub.exec.aws.rds.db_cluster_parameter_group.get(
        ctx=ctx, resource_id=resource_id, name=name
    )
    if not before["result"]:
        result["result"] = False
        result["comment"] = before["comment"]
        return result

    if not before["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.rds.db_cluster_parameter_group", name=name
        )
    elif ctx.get("test", False):
        result["old_state"] = before["ret"]
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.rds.db_cluster_parameter_group", name=name
        )
    else:
        result["old_state"] = before["ret"]
        ret = await hub.exec.boto3.client.rds.delete_db_cluster_parameter_group(
            ctx, DBClusterParameterGroupName=resource_id
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.rds.db_cluster_parameter_group", name=name
        )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """
    Describe the resource in a way that can be recreated/managed with the corresponding "present" function.

    Returns a list of DBClusterParameterGroup descriptions. If a DBClusterParameterGroupName parameter is specified,
    the list will contain only the description of the specified DB cluster parameter group.  For more information on
    Amazon Aurora, see  What is Amazon Aurora? in the Amazon Aurora User Guide.  For more information on Multi-AZ DB
    clusters, see  Multi-AZ deployments with two readable standby DB instances in the Amazon RDS User Guide.

    Returns:
        Dict[str, Dict[str, Any]]

    Examples:

        .. code-block:: bash

            $ idem describe aws.rds.db_cluster_parameter_group
    """

    result = {}
    ret = await hub.exec.aws.rds.db_cluster_parameter_group.list(
        ctx, name="aws.rds.db_cluster_parameter_group.describe"
    )
    if not ret["result"]:
        hub.log.warning(
            f"Could not describe db_cluster_parameter_group {ret['comment']}"
        )
        return {}

    for resource in ret["ret"]:
        result[resource.get("resource_id")] = {
            "aws.rds.db_cluster_parameter_group.present": [resource]
        }
    return result
