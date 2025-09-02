"""Exec module for managing Amazon DocDB DB Cluster Parameter Group."""
from typing import Dict
from typing import List

__func_alias__ = {"list_": "list"}

RESOURCE_TYPE = "aws.docdb.db_cluster_parameter_group"


async def get(hub, ctx, name: str, resource_id: str = None):
    """Retrieves the specified AWS Document DB Cluster Parameter Group.

    Args:
        resource_id(str, Optional):
            AWS Document DB Cluster Parameter Group Name.
        name(str):
            An Idem name of the resource.

    Examples:
        Calling this exec module function from the cli:

        .. code-block:: bash

            idem exec aws.docdb.db_cluster_parameter_group.get resource_id="resource_id" name="name"

        .. code-block:: python

            async def state_function(hub, ctx, name, resource_id, **kwargs):
                ret = await hub.exec.aws.docdb.db_cluster_parameter_group.get(
                    ctx, name=name, resource_id=resource_id
                )

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.docdb.db_cluster_parameter_group.get
                - kwargs:
                    name: name
                    resource_id: resource_id

    """
    result = dict(comment=[], ret=None, result=True)
    before = await hub.tool.aws.docdb.db_cluster_parameter_group.search_raw(
        ctx, resource_id=resource_id
    )
    if not before["result"]:
        if "ParameterGroupNotFound" in str(before["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type=RESOURCE_TYPE,
                    name=name,
                )
            )
            result["comment"].append(before["comment"])
            return result
        result["result"] = False
        result["comment"].append(before["comment"])
        return result
    if not before["ret"]["DBClusterParameterGroups"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.ec2.vpc", name=name
            )
        )
        return result

    resource = before["ret"]["DBClusterParameterGroups"]
    if len(resource) > 1:
        result["comment"].append(
            hub.tool.aws.comment_utils.find_more_than_one(
                resource_id=resource_id, resource_type=RESOURCE_TYPE
            )
        )
    resource_arn = before["ret"]["DBClusterParameterGroups"][0].get(
        "DBClusterParameterGroupArn"
    )

    tags = await hub.exec.boto3.client.docdb.list_tags_for_resource(
        ctx, ResourceName=resource_arn
    )
    if not tags["result"]:
        result["result"] = False
        result["comment"].append(tags["comment"])
        return result

    parameters_raw = await hub.exec.boto3.client.docdb.describe_db_cluster_parameters(
        ctx=ctx, DBClusterParameterGroupName=resource_id
    )
    if not parameters_raw["result"]:
        result["result"] = False
        result["comment"].append(parameters_raw["comment"])
        return result
    parameters_raw = parameters_raw.get("ret")
    parameters = parameters_raw.get("Parameters")

    result[
        "ret"
    ] = hub.tool.aws.docdb.db_cluster_parameter_group.convert_raw_db_cluster_parameter_group_to_present(
        raw_resource=before["ret"]["DBClusterParameterGroups"][0],
        idem_resource_name=resource_id,
        tags=hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags["ret"]["TagList"]),
        parameters=parameters,
    )
    return result


async def list_(hub, ctx, name: str = None, filters: List = None) -> Dict:
    """Use a list of un-managed docdb db cluster parameter groups as a data-source.

    Args:
        name(str, Optional):
            The name of idem state.

        filters(list, Optional):
            One or more filters, dictionary of attribute value pair which will be converted to boto3 filter
            format.

    .. note::
        At the time of writing this module, filters parameter is not supported for this resource as per
        AWS documentation so idem-aws has omitted it.

    Returns:
        Dict[bool, list, dict or None]:

        result(bool):
            Whether the result of the function has been successful (``True``) or not (``False``).
        comment(list):
            A list of messages.
        ret(dict or None):
           The AWS DocDB DB Cluster Parameter Group in "present" format.

    Examples:
        Calling this exec module function from the cli:

        .. code-block:: bash

            idem exec aws.docdb.db_cluster_parameter_group.list name=name

        Calling this exec module function from within a state module in pure python:

        .. code-block:: python

            async def state_function(hub, ctx, name, **kwargs):
                ret = await hub.exec.aws.docdb.db_cluster_parameter_group.list(
                    ctx, name=name
                )

        Calling this exec module function from within a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.docdb.db_cluster_parameter_group.list
                - kwargs:
                    name: 'test-doc-db-cluster-param-group'


    """
    result = dict(comment=[], ret=[], result=True)
    ret = await hub.tool.aws.docdb.db_cluster_parameter_group.search_raw(
        ctx=ctx, filters=filters
    )
    if not ret["result"]:
        result["comment"].append(ret["comment"])
        result["result"] = False
        return result
    if not ret["ret"]["DBClusterParameterGroups"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.list_empty_comment(
                resource_type=RESOURCE_TYPE, name=name
            )
        )
        return result
    for db_cluster_parameter_group in ret["ret"]["DBClusterParameterGroups"]:
        db_cluster_parameter_group_name = db_cluster_parameter_group.get(
            "DBClusterParameterGroupName"
        )
        arn = db_cluster_parameter_group["DBClusterParameterGroupArn"]

        # get tags
        tags = await hub.tool.aws.docdb.tag.get_tags_for_resource(
            ctx=ctx, resource_arn=arn
        )
        if not tags["result"]:
            result["result"] = False
            result["comment"].append(tags["comment"])
            return result
        tags = tags["ret"]

        parameters_raw = (
            await hub.exec.boto3.client.docdb.describe_db_cluster_parameters(
                ctx=ctx, DBClusterParameterGroupName=db_cluster_parameter_group_name
            )
        )
        if not parameters_raw["result"]:
            result["result"] = False
            result["comment"].append(parameters_raw["comment"])
            return result
        parameters_raw = parameters_raw.get("ret")
        parameters = parameters_raw.get("Parameters")

        result["ret"].append(
            hub.tool.aws.docdb.db_cluster_parameter_group.convert_raw_db_cluster_parameter_group_to_present(
                raw_resource=db_cluster_parameter_group,
                idem_resource_name=db_cluster_parameter_group_name,
                tags=tags,
                parameters=parameters,
            )
        )
    return result
