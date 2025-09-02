"""State module for managing RDS DB Parameter Group."""
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
    description: str = None,
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
    """Creates a new DB parameter group.

    A DB parameter group is initially created with the default parameters for the
    database engine used by the DB instance. To provide custom values for any of the parameters, you can specify
    parameters.  Once you've created a DB parameter group, you can associate it with your DB instance.

    When you associate a new DB parameter group with a running DB instance, you need to reboot the DB instance without
    failover for the new DB parameter group and associated settings to take effect.

    After you create a DB parameter group, you should wait at least 5 minutes before creating your first DB instance
    that uses that DB parameter group as the default parameter group. This allows Amazon RDS to fully complete the
    create action before the parameter group is used as the default for a new DB instance. This is especially important
    for parameters that are critical when creating the default database for a DB instance, such as the character set
    for the default database defined by the character_set_database parameter.

    You can use the Parameter Groups option of the Amazon RDS console to verify that your DB parameter group has been
    created or modified.

    Args:
        name(str):
            An Idem name of the resource.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

        db_parameter_group_family(str):
            The DB parameter group family name. A DB parameter group can be associated with one and only one
            DB parameter group family, and can be applied only to a DB instance running a database engine
            and engine version compatible with that DB parameter group family.

            To list all of the available parameter group families for a DB engine, use the following command:

            .. code-block:: bash

                aws rds describe-db-engine-versions --query "DBEngineVersions[].DBParameterGroupFamily" --engine <engine>

            For example, to list all of the available parameter group families for the MySQL DB engine, use the
            following command:

            .. code-block:: bash

                aws rds describe-db-engine-versions --query "DBEngineVersions[].DBParameterGroupFamily" --engine mysql

            The output contains duplicates.

            The following are the valid DB engine values:

              * aurora (for MySQL 5.6-compatible Aurora)
              * aurora-mysql (for MySQL 5.7-compatible and MySQL 8.0-compatible Aurora)
              * aurora-postgresql
              * mariadb
              * mysql
              * oracle-ee
              * oracle-ee-cdb
              * oracle-se2
              * oracle-se2-cdb
              * postgres
              * sqlserver-ee
              * sqlserver-se
              * sqlserver-ex
              * sqlserver-web

        description(str):
            The description for the DB parameter group.

        tags(Dict or List, Optional):
            Dict in the format of {tag-key: tag-value} or List of tags in the format of [{"Key": tag-key, "Value":
            tag-value}] to associate with the DB parameter group.

            Each tag consists of a key name and an associated value. Defaults to None.

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

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_present:
              aws.rds.db_parameter_group.present:
              - name: 'test'
              - resource_id: 'test'
              - db_parameter_group_family: 'aurora-mysql5.7'
              - description: 'test'
              - tags:
                 - Key: 'test'
                   Value: 'test1'
                 - Key: 'test2'
                   Value: 'test2'
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
        before = await hub.exec.aws.rds.db_parameter_group.get(
            ctx=ctx, name=resource_id
        )
        if not before["result"] or not before["ret"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result

        result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
            resource_type="aws.rds.db_parameter_group", name=name
        )
        result["old_state"] = copy.deepcopy(before["ret"])
        plan_state = copy.deepcopy(result["old_state"])

        update_tags_ret = None
        # Update tags
        if tags is not None:
            update_tags_ret = await hub.exec.aws.rds.tag.update_rds_tags(
                ctx=ctx,
                resource_arn=result["old_state"].get("db_parameter_group_arn"),
                old_tags=result["old_state"].get("tags"),
                new_tags=tags,
            )
            result["comment"] += update_tags_ret["comment"]
            result["result"] = update_tags_ret["result"]
            resource_updated = update_tags_ret["result"]
            if ctx.get("test", False) and update_tags_ret["ret"] is not None:
                plan_state["tags"] = update_tags_ret["ret"]
        if parameters is not None:
            update_ret = await hub.tool.aws.rds.parameters.modify_db_parameter_group(
                ctx=ctx,
                resource_name=result["old_state"].get("resource_id"),
                old_parameters=result["old_state"].get("parameters"),
                new_parameters=parameters,
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
                resource_type="aws.rds.db_parameter_group", name=name
            )
            return result
        ret = await hub.exec.boto3.client.rds.create_db_parameter_group(
            ctx,
            **{
                "DBParameterGroupName": name,
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

        resource_id = ret["ret"]["DBParameterGroup"]["DBParameterGroupName"]
        result["new_state"] = {"name": name, "resource_id": resource_id}

        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.rds.db_parameter_group", name=name
        )

        # Modify the db group parameters
        if parameters is not None:
            ret_parameter = await hub.exec.boto3.client.rds.describe_db_parameters(
                ctx, DBParameterGroupName=resource_id
            )
            if not ret_parameter["result"]:
                result["comment"] += ret_parameter["comment"]
                result["result"] = ret_parameter["result"]
            else:
                update_ret = (
                    await hub.tool.aws.rds.parameters.modify_db_parameter_group(
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
            after = await hub.exec.aws.rds.db_parameter_group.get(
                ctx=ctx, name=resource_id
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


async def absent(hub, ctx, name: str, resource_id: str = None) -> Dict[str, Any]:
    """Deletes a specified DB parameter group.

    The DB parameter group to be deleted can't be associated with any DB
    instances.

    Args:
        resource_id(str):
            An identifier of the resource in the provider.

        name(str, Optional):
            The name of the DB parameter group.

            Constraints:

              * Must be the name of an existing DB parameter group.
              * You can't delete a default DB parameter group.
              * Can't be associated with any DB instances.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_absent:
              aws.rds.db_parameter_group.absent:
                - name: value
                - resource_id: value
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.rds.db_parameter_group", name=name
        )
        return result
    before = await hub.exec.aws.rds.db_parameter_group.get(ctx=ctx, name=resource_id)
    if not before["result"]:
        result["result"] = False
        result["comment"] = before["comment"]
        return result

    if not before["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.rds.db_parameter_group", name=name
        )
    elif ctx.get("test", False):
        result["old_state"] = before["ret"]
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.rds.db_parameter_group", name=name
        )
    else:
        result["old_state"] = before["ret"]
        ret = await hub.exec.boto3.client.rds.delete_db_parameter_group(
            ctx, DBParameterGroupName=resource_id
        )
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.rds.db_parameter_group", name=name
        )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Returns a list of DB Parameter Group descriptions.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.rds.db_parameter_group
    """
    result = {}
    ret = await hub.exec.aws.rds.db_parameter_group.list(
        ctx, name="aws.rds.db_parameter_group.describe"
    )
    if not ret["result"]:
        hub.log.warning(f"Could not describe db_parameter_group {ret['comment']}")
        return {}

    for resource in ret["ret"]:
        result[resource.get("resource_id")] = {
            "aws.rds.db_parameter_group.present": [resource]
        }
    return result
