"""Exec module for managing DB Subnet Group resources."""
from typing import Dict
from typing import List

__func_alias__ = {"list_": "list"}


async def get(hub, ctx, resource_id: str):
    """Get Document DB Subnet Group details from AWS given a AWS Document DB Subnet Group Name.

    Args:
        resource_id(str):
            AWS Document DB Subnet Group Name

    Returns:
        .. code-block:: python

            {"result": True|False, "comment": A message List, "ret": None|Dict}

    Examples:
        Calling this exec module function from the cli with resource_id

        .. code-block:: bash

            idem exec aws.docdb.db_subnet_group.get resource_id="resource_id"

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.docdb.db_subnet_group.get
                - kwargs:
                    resource_id: resource_id

    """
    result = dict(comment=[], ret=None, result=True)
    before = await hub.tool.aws.docdb.db_subnet_group.search_raw(
        ctx, DBSubnetGroupName=resource_id
    )
    if not before["result"]:
        if "DBSubnetGroupNotFound" in str(before["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.docdb.db_subnet_group", name=resource_id
                )
            )
            result["comment"] += list(before["comment"])
            return result
        result["result"] = False
        result["comment"] = before["comment"]
        return result
    if before["ret"]["DBSubnetGroups"]:
        resource = before["ret"]["DBSubnetGroups"]
        if len(resource) > 1:
            result["comment"].append(
                f"More than one aws.ec2.docdb.db_subnet_group resource was found. "
                f"Use resource {resource[0]['DBSubnetGroupName']}"
            )
        resource_arn = before["ret"]["DBSubnetGroups"][0].get("DBSubnetGroupArn")
        tags = await hub.tool.aws.docdb.tag.get_tags_for_resource(
            ctx, resource_arn=resource_arn
        )
        if not tags["result"]:
            result["result"] = False
            result["comment"] = tags["comment"]
            return result
        result[
            "ret"
        ] = hub.tool.aws.docdb.db_subnet_group.convert_raw_db_subnet_group_to_present(
            raw_resource=before["ret"]["DBSubnetGroups"][0],
            idem_resource_name=resource_id,
            tags=tags["ret"],
        )
    return result


async def list_(hub, ctx, DBSubnetGroupName: str = None, filters: List = None) -> Dict:
    """Get list of Document DB Subnet Group details from AWS.

    Use an un-managed DocDb Subnet as a data-source. Supply one of the inputs as the filter.

    Args:
        DBSubnetGroupName(str, Optional):
            The name of the DBSubnetGroupName.
        filters(list, Optional):
            One or more filters: for example, tag :<key>, tag-key. A complete list of filters can be found at
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.describe_db_subnet_groups

    Returns:
        .. code-block:: python

            {"result": True|False, "comment": A message List, "ret": None|List}

    Examples:
         Calling from the CLI:

        .. code-block:: bash

            idem exec aws.docdb.db_subnet_group.list DBSubnetGroupName=dbg1 filters='[{"name": "filter_name", "values": ["filter_value1"]}]'

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.docdb.db_subnet_group.list
                - kwargs:
                    DBSubnetGroupName: dbg1
                    filters:
                      - name: filter-name
                        values:
                            - filter_value
    """
    result = dict(comment=[], ret=[], result=True)
    ret = await hub.tool.aws.docdb.db_subnet_group.search_raw(
        ctx=ctx, filters=filters, DBSubnetGroupName=DBSubnetGroupName
    )
    if not ret["result"]:
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    if not ret["ret"]["DBSubnetGroups"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.list_empty_comment(
                resource_type="aws.docdb.db_subnet_group", name=DBSubnetGroupName
            )
        )
        return result
    for subnetGroupName in ret["ret"]["DBSubnetGroups"]:
        name = subnetGroupName.get("DBSubnetGroupName")
        converted_db_group = (
            hub.tool.aws.docdb.db_subnet_group.convert_raw_db_subnet_group_to_present(
                raw_resource=subnetGroupName, idem_resource_name=name
            )
        )
        result["ret"].append(converted_db_group)
    return result
