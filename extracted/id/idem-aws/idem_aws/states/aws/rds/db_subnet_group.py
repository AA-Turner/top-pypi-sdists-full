"""State operations for RDS db_subnet_group"""
import copy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]

TREQ = {
    "present": {
        "require": [
            "aws.ec2.subnet.present",
        ],
    },
}


async def present(
    hub,
    ctx,
    name: str,
    db_subnet_group_description: str,
    subnets: List[str],
    resource_id: str = None,
    tags: Dict[str, Any]
    or List[
        make_dataclass("Tag", [("Key", str), ("Value", str, field(default=None))])
    ] = None,
) -> Dict[str, Any]:
    """
    Creates a new DB subnet group. DB subnet groups must contain at least one subnet in at least two AZs in the
    Amazon Web Services Region.

    Args:
        name(str):
            The Idem name of the DB subnet group.

        db_subnet_group_description(str):
            DB Subnet Group description

        subnets(List[str]):
            The EC2 Subnet IDs for the DB subnet group

        resource_id(str, Optional):
            AWS RDS DBSubnetGroupName to identify the resource

        tags(Dict or List, Optional):
            Dict in the format of {tag-key: tag-value} or List of tags in the format of [{"Key": tag-key, "Value":
            tag-value}] to associate with the DB instance.

            Each tag consists of a key name and an associated value. Defaults to None.

            * Key (str, Optional): The key of the tag. Constraints: Tag keys are case-sensitive and accept a maximum of
              127 Unicode characters. May not begin with aws:.

            * Value(str, Optional): The value of the tag. Constraints: Tag values are case-sensitive and accept a
              maximum of 256 Unicode characters.

    Request Syntax:
        [db-subnet-group-name]:
          aws.rds.db_subnet_group.absent:
            - db_subnet_group_description: 'string'
            - subnets: 'list'
            - tags:
              - Key: 'string'
                Value: 'string'

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: sls

            new-db-subnet-group:
                aws.rds.db_subnet_group.absent:
                  - db_subnet_group_description: "should not be blank"
                  - subnets:
                    - subnet-03e29c119d78899e1
                    - subnet-04dd5bc5aa08cbd89
                    - subnet-0754289517e31d331
                  - tags:
                    - Key: name
                      Value: new-db-subnet-group
    """

    plan_state = {}
    result = {
        "comment": [],
        "old_state": None,
        "new_state": None,
        "name": name,
        "result": True,
    }
    before = None
    if resource_id:
        before = await hub.exec.aws.rds.db_subnet_group.get(
            ctx,
            resource_id=resource_id,
        )
    tags = (
        hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags)
        if isinstance(tags, List)
        else tags
    )
    old_db_subnet_group = {}
    is_updated = False
    are_tags_updated = False
    db_subnet_group_arn = None
    old_tag = None
    if before and before["result"]:
        try:
            old_db_subnet_group = before["ret"]
            subnet_list = old_db_subnet_group["subnets"]
            if set(subnets) != set(subnet_list):
                is_updated = True
            db_subnet_group_arn = old_db_subnet_group.get("db_subnet_group_arn")
            ret_tag = await hub.exec.boto3.client.rds.list_tags_for_resource(
                ctx, ResourceName=db_subnet_group_arn
            )
            if ret_tag["result"]:
                old_tag = hub.tool.aws.tag_utils.convert_tag_list_to_dict(
                    ret_tag.get("ret").get("TagList")
                )
                old_db_subnet_group["tags"] = old_tag
            else:
                result["comment"] = ret_tag["comment"]
                result["result"] = False
                return result
            plan_state = copy.deepcopy(old_db_subnet_group)
            if ctx.get("test", False):
                plan_state["subnets"] = subnets
                plan_state["subnets"].sort()
                if db_subnet_group_description:
                    plan_state[
                        "db_subnet_group_description"
                    ] = db_subnet_group_description
            else:
                if is_updated:
                    update_ret = await hub.exec.boto3.client.rds.modify_db_subnet_group(
                        ctx,
                        DBSubnetGroupName=name,
                        DBSubnetGroupDescription=db_subnet_group_description,
                        SubnetIds=subnets,
                    )
                    if not update_ret["result"]:
                        result["comment"] += update_ret["comment"]
                        result["result"] = False
                        return result
            if tags is not None and tags != old_tag:
                update_tags_ret = await hub.exec.aws.rds.tag.update_rds_tags(
                    ctx=ctx,
                    resource_arn=db_subnet_group_arn,
                    old_tags=old_tag,
                    new_tags=tags,
                )
                if not update_tags_ret["result"]:
                    result["comment"] += update_tags_ret["comment"]
                    result["result"] = False
                    return result
                are_tags_updated = update_tags_ret["result"]
            if ctx.get("test", False):
                if are_tags_updated:
                    plan_state["tags"] = update_tags_ret["ret"]
            elif is_updated or are_tags_updated:
                result["comment"] += [f"Updated '{name}'"]
            else:
                result["comment"] += [f"'{name}' already exists"]
        except Exception as e:
            result["comment"] += [str(e)]
            result["result"] = False
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "db_subnet_group_description": db_subnet_group_description,
                    "resource_id": resource_id,
                    "subnets": subnets,
                    "tags": tags,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.rds.db_subnet_group", name=name
            )
            return result
        try:
            ret = await hub.exec.boto3.client.rds.create_db_subnet_group(
                ctx,
                DBSubnetGroupName=name,
                DBSubnetGroupDescription=db_subnet_group_description,
                SubnetIds=subnets,
                Tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags)
                if tags
                else None,
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = ret["comment"]
                return result
            db_subnet_group_arn = (
                ret["ret"].get("DBSubnetGroup").get("DBSubnetGroupArn")
            )
            result["comment"] = result[
                "comment"
            ] + hub.tool.aws.comment_utils.create_comment(
                resource_type="aws.rds.db_subnet_group", name=name
            )
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]
            result["result"] = False
            return result

    try:
        if ctx.get("test", False):
            new_db_subnet_group = plan_state
        elif is_updated or not (before and before["result"]):
            after = await hub.exec.aws.rds.db_subnet_group.get(
                ctx,
                resource_id=name,
            )
            new_db_subnet_group = after["ret"]
        else:
            new_db_subnet_group = copy.deepcopy(old_db_subnet_group)

        if not ctx.get("test", False):
            if are_tags_updated or not (before and before["result"]):
                ret_tag = await hub.exec.boto3.client.rds.list_tags_for_resource(
                    ctx, ResourceName=db_subnet_group_arn
                )
                new_db_subnet_group[
                    "tags"
                ] = hub.tool.aws.tag_utils.convert_tag_list_to_dict(
                    ret_tag.get("ret").get("TagList")
                )
            else:
                new_db_subnet_group["tags"] = old_tag

        result["old_state"] = old_db_subnet_group
        result["new_state"] = new_db_subnet_group
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
    Deletes a DB subnet group.  The specified database subnet group must not be associated with any DB instances.

    Args:
        name(str):
            The Idem name of the DB subnet group.

        resource_id(str, Optional):
            The AWS RDS DBSubnetGroupName to identify the resource

    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: sls

            resource_is_absent:
              aws.rds.db_subnet_group.absent:
                - name: value
    """

    result = {
        "comment": [],
        "old_state": None,
        "new_state": None,
        "name": name,
        "result": True,
    }
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.rds.db_subnet_group", name=name
        )
        return result
    try:
        before = await hub.exec.boto3.client.rds.describe_db_subnet_groups(
            ctx, DBSubnetGroupName=resource_id
        )
        if not before:
            result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
                resource_type="aws.rds.db_subnet_group", name=name
            )
            return result
        else:
            tags = await hub.exec.boto3.client.rds.list_tags_for_resource(
                ctx,
                ResourceName=(before["ret"]["DBSubnetGroups"][0]).get(
                    "DBSubnetGroupArn"
                ),
            )
            result[
                "old_state"
            ] = hub.tool.aws.rds.conversion_utils.convert_raw_db_subnet_group_to_present(
                resource=before["ret"]["DBSubnetGroups"][0],
                tags=hub.tool.aws.tag_utils.convert_tag_list_to_dict(
                    tags.get("ret").get("TagList")
                )
                if tags.get("result")
                else None,
            )
            if ctx.get("test", False):
                result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
                    resource_type="aws.rds.db_subnet_group", name=name
                )
                return result
            else:
                try:
                    ret = await hub.exec.boto3.client.rds.delete_db_subnet_group(
                        ctx, DBSubnetGroupName=name
                    )
                    result["result"] = ret["result"]
                    if not result["result"]:
                        result["comment"] = ret["comment"]
                        result["result"] = False
                        return result
                    result["comment"] = hub.tool.aws.comment_utils.delete_comment(
                        resource_type="aws.rds.db_subnet_group", name=name
                    )
                except hub.tool.boto3.exception.ClientError as e:
                    result["comment"] += [f"{e.__class__.__name__}: {e}"]
                    result["result"] = False
    except Exception as e:
        result["comment"] += [str(e)]
        result["result"] = False
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """
    Describe the resource in a way that can be recreated/managed with the corresponding "present" function


    Returns a list of DBSubnetGroup descriptions. For an overview of CIDR ranges, go to the Wikipedia Tutorial.


    Returns:
        Dict[str, Any]

    Examples:

        .. code-block:: bash

            $ idem describe aws.rds.db_subnet_group
    """

    result = {}
    try:
        ret = await hub.exec.boto3.client.rds.describe_db_subnet_groups(ctx)
        if not ret["result"]:
            hub.log.warning(f"Could not describe db_subnet_group {ret['comment']}")
            return {}

        for db_subnet_group in ret["ret"]["DBSubnetGroups"]:
            db_subnet_group_id = db_subnet_group.get("DBSubnetGroupName")
            tags = None
            ret_tags = await hub.exec.boto3.client.rds.list_tags_for_resource(
                ctx, ResourceName=db_subnet_group.get("DBSubnetGroupArn")
            )
            if not ret_tags:
                result["comment"] = ret_tags["comment"]
                result["result"] = False
            else:
                tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict(
                    ret_tags.get("ret").get("TagList")
                )
            resource_converted = hub.tool.aws.rds.conversion_utils.convert_raw_db_subnet_group_to_present(
                resource=db_subnet_group,
                tags=tags,
            )
            result[db_subnet_group_id] = {
                "aws.rds.db_subnet_group.present": [
                    {parameter_key: parameter_value}
                    for parameter_key, parameter_value in resource_converted.items()
                ]
            }
    except Exception as e:
        result["comment"] = str(e)
        result["result"] = False
    return result
