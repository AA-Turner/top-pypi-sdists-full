"""
Exec module for rds.db_subnet_group
"""
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List


__func_alias__ = {"list_": "list"}


async def get(hub, ctx, resource_id: str, name: str = None) -> Dict[str, Any]:
    """
    Returns a list of DBSubnetGroup descriptions. If a DBSubnetGroupName is specified, the list will contain only the
    descriptions of the specified DBSubnetGroup. For an overview of CIDR ranges, go to the Wikipedia Tutorial.

        Args:
            resource_id(str):
                An identifier of the resource in the provider. Defaults to None.

            name(str, Optional):
                An Idem name of the resource

        Examples:

            .. code-block:: bash

                idem exec aws_auto.rds.db_subnet_group.get.get resource_id=01235789abcdef

            .. code-block:: python

                async def my_func(hub, ctx):
                    ret = await hub.exec.aws_auto.rds.db_subnet_group.get.get(ctx, resource_id="012345789abcedf")

            .. code-block:: yaml

                aws_auto_rds_db_subnet_group_get_resource:
                  exec.run:
                    - path: aws_auto.rds.db_subnet_group.get
                    - resource_id: 0123456789abcdef

    """

    result = {
        "comment": [],
        "ret": None,
        "result": True,
    }
    ret = await hub.exec.boto3.client.rds.describe_db_subnet_groups(
        ctx=ctx,
        DBSubnetGroupName=resource_id,
    )
    if not ret["result"]:
        if "DBSubnetGroupNotFoundFault" in str(ret.get("comment", "")):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.rds.db_subnet_group",
                    name=name if name else resource_id,
                )
            )
        else:
            ret["result"] = False
        result["comment"] += list(ret["comment"])
        return result

    if not ret["ret"]["DBSubnetGroups"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.rds.db_subnet_group",
                name=name if name else resource_id,
            )
        )
        return result

    resource = ret["ret"]["DBSubnetGroups"][0]
    if len(ret["ret"]["DBSubnetGroups"]) > 1:
        result["comment"].append(
            f"More than one aws.rds.db_subnet_group resource was found. Use resource {resource.get('DBSubnetGroupName')}"
        )

    result[
        "ret"
    ] = hub.tool.aws.rds.conversion_utils.convert_raw_db_subnet_group_to_present(
        resource=resource
    )

    return result


async def list_(
    hub,
    ctx,
    name: str = None,
    filters: List[
        make_dataclass("Filter", [("Name", str), ("Values", List[str])])
    ] = None,
) -> Dict[str, Any]:
    """
    Returns a list of DBSubnetGroup descriptions. If a DBSubnetGroupName is specified, the list will contain only the
    descriptions of the specified DBSubnetGroup. For an overview of CIDR ranges, go to the Wikipedia Tutorial.

        Args:
            name(str):
                An Idem name of the resource.

            filters(list[Dict[str, Any]], Optional):
                This parameter isn't currently supported. Defaults to None.

                * Name (str):
                    The name of the filter. Filter names are case-sensitive.

                * Values (list[str]):
                    One or more filter values. Filter values are case-sensitive.

        Examples:

            .. code-block:: bash

                idem exec aws_auto.rds.db_subnet_group.list

            .. code-block:: python

                async def my_func(hub, ctx):
                    ret = await hub.exec.aws_auto.rds.db_subnet_group.list(ctx)

            .. code-block:: yaml

                aws_auto_rds_db_subnet_group_list_resource:
                  exec.run:
                    - path: aws_auto.rds.db_subnet_group.list

    """

    result = {
        "comment": [],
        "ret": None,
        "result": True,
    }
    ret = await hub.exec.boto3.client.rds.describe_db_subnet_groups(
        ctx=ctx,
        filters=filters,
    )
    if not ret["result"]:
        result["comment"] += list(ret["comment"])
        return result
    if not ret["ret"]["DBSubnetGroups"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.rds.db_subnet_group", name=name
            )
        )
        return result

    result["ret"] = []
    for resource in ret["ret"]["DBSubnetGroups"]:
        result["ret"].append(
            hub.tool.aws.rds.conversion_utils.convert_raw_db_subnet_group_to_present(
                resource=resource
            )
        )
    return result
