"""Exec module for managing Amazon Neptune DB Cluster Parameter Group."""
from typing import Dict

__func_alias__ = {"list_": "list"}

RESOURCE_TYPE = "aws.neptune.db_cluster_parameter_group"


async def get(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
) -> Dict:
    """Retrieves the specified AWS Neptune DB Cluster Parameter Group.

    It also fetches the db cluster parameters for the supplied resource_id.
    Filters is not supported yet as per documentation for this resource on AWS.
    It returns idem object representation for db_cluster_parameter_group found if resource_id was specified.
    If resource_id wasn't specified, it returns the first resource found.

    Args:
        name(str):
            An Idem name of the resource.
        resource_id(str, Optional):
            DBClusterParameterGroupName of the resource in AWS.

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
           The AWS Neptune DB Cluster Parameter Group in "present" format.

    Examples:
        Calling this exec module function from the cli:

        .. code-block:: bash

            idem exec aws.neptune.db_cluster_parameter_group.get name="idem_name" resource_id="resource_id"

        Calling this exec module function from within a state module in pure python:

        .. code-block:: python

            async def state_function(hub, ctx, name, resource_id, **kwargs):
                ret = await hub.exec.aws.neptune.db_cluster_parameter_group.get(
                    ctx, name=name, resource_id=resource_id
                )
    """
    result = dict(comment=[], ret=None, result=True)
    ret = await hub.tool.aws.neptune.db_cluster_parameter_group.search_raw(
        ctx=ctx, name=name, resource_id=resource_id
    )
    if not ret["result"]:
        if "ParameterGroupNotFound" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type=RESOURCE_TYPE, name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    if not ret["ret"]["DBClusterParameterGroups"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type=RESOURCE_TYPE, name=name
            )
        )
        return result

    resource = ret["ret"]["DBClusterParameterGroups"][0]
    resource_id = resource.get("DBClusterParameterGroupName")
    if len(ret["ret"]["DBClusterParameterGroups"]) > 1:
        result["comment"].append(
            hub.tool.aws.comment_utils.find_more_than_one(
                resource_type=RESOURCE_TYPE, resource_id=resource_id
            )
        )
    arn = resource["DBClusterParameterGroupArn"]
    # get parameters
    parameters_raw = await hub.exec.boto3.client.neptune.describe_db_cluster_parameters(
        ctx=ctx, DBClusterParameterGroupName=resource_id
    )
    if not parameters_raw["result"]:
        result["result"] = False
        result["comment"].append(parameters_raw["comment"])
        return result
    parameters_raw = parameters_raw.get("ret")
    parameters = parameters_raw.get("Parameters")

    # get tags
    tags = await hub.tool.aws.neptune.tag.get_tags_for_resource(ctx, resource_arn=arn)
    if not tags["result"]:
        result["result"] = False
        result["comment"].append(tags["comment"])
        return result
    tags = tags["ret"]
    result[
        "ret"
    ] = hub.tool.aws.neptune.conversion_utils.convert_raw_db_cluster_parameter_group_to_present(
        raw_resource=resource, idem_resource_name=name, tags=tags, parameters=parameters
    )
    return result


async def list_(hub, ctx, name: str = None) -> Dict:
    """Use a list of un-managed neptune db cluster parameter groups as a data-source.

    Args:
        name (str, Optional):
            The name of idem state.

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
           The AWS Neptune DB Cluster Parameter Group in "present" format.

    Examples:
        Calling this exec module function from the cli:

        .. code-block:: bash

            idem exec aws.neptune.db_cluster_parameter_group.list name=name

        Calling this exec module function from within a state module in pure python:

        .. code-block:: python

            async def state_function(hub, ctx, name, **kwargs):
                ret = await hub.exec.aws.neptune.db_cluster_parameter_group.list(
                    ctx, name=name
                )
    """
    result = dict(comment=[], ret=[], result=True)
    ret = await hub.tool.aws.neptune.db_cluster_parameter_group.search_raw(
        ctx=ctx, name=name
    )
    if not ret["result"]:
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    if not ret["ret"]["DBClusterParameterGroups"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
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
        tags = await hub.tool.aws.neptune.tag.get_tags_for_resource(
            ctx, resource_arn=arn
        )
        if not tags["result"]:
            result["result"] = False
            result["comment"].append(tags["comment"])
            return result
        tags = tags["ret"]

        # get parameters
        parameters_raw = (
            await hub.exec.boto3.client.neptune.describe_db_cluster_parameters(
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
            hub.tool.aws.neptune.conversion_utils.convert_raw_db_cluster_parameter_group_to_present(
                raw_resource=db_cluster_parameter_group,
                idem_resource_name=db_cluster_parameter_group_name,
                tags=tags,
                parameters=parameters,
            )
        )
    return result
