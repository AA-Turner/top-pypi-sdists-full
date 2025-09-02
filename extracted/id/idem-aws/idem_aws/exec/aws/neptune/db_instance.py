"""Exec module for managing Amazon Neptune DB Instance."""
from typing import Dict
from typing import List

__func_alias__ = {"list_": "list"}

RESOURCE_TYPE = "aws.neptune.db_instance"


async def get(
    hub, ctx, name: str, resource_id: str = None, filters: List = None
) -> Dict:
    """Fetch and use an un-managed neptune db instance as a data-source.

    Args:
        name(str):
            The name of the Idem state.
        resource_id(str, Optional):
            AWS Neptune DBInstanceIdentifier to identify the resource.
        filters(list, Optional):
            A filter that specifies one or more DB instances to describe.
            Supported filters are,

            * db-cluster(str, Optional):
                Accepts DB cluster identifiers and DB cluster Amazon Resource Names (ARNs). The results list will only include information about the DB instances associated with the DB clusters identified by these ARNs.
            * engine(str, Optional):
                Accepts an engine name (such as neptune ), and restricts the results list to DB instances created by that engine.

    .. note::
        If filters used matches more than one neptune db instance, idem will default to fetching the first result.

    Returns:
        Dict[bool, list, dict or None]:

        result(bool):
            Whether the result of the function has been successful (``True``) or not (``False``).
        comment(list):
            A list of messages.
        ret(dict or None):
           The AWS Neptune DB Instance in "present" format.

    Examples:
        Calling this exec module function from the cli:

        .. code-block:: bash

            idem exec aws.neptune.db_instance.get name="idem_name" resource_id="resource_id"

        Calling this exec module function from within a state module in pure python:

        .. code-block:: python

            async def state_function(hub, ctx, name, resource_id, **kwargs):
                ret = await hub.exec.aws.neptune.db_instance.get(
                    ctx, name=name, resource_id=resource_id
                )
    """
    result = dict(comment=[], ret=None, result=True)
    ret = await hub.tool.aws.neptune.db_instance.search_raw(
        ctx=ctx, name=name, resource_id=resource_id, filters=filters
    )
    if not ret["result"]:
        if "DBInstanceNotFoundFault" in str(ret["comment"]):
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
    if not ret["ret"]["DBInstances"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type=RESOURCE_TYPE, name=name
            )
        )
        return result

    resource = ret["ret"]["DBInstances"][0]
    if len(ret["ret"]["DBInstances"]) > 1:
        result["comment"].append(
            hub.tool.aws.comment_utils.find_more_than_one(
                resource_type=RESOURCE_TYPE,
                resource_id=resource.get("DBInstanceIdentifier"),
            )
        )
    arn = resource["DBInstanceArn"]
    # get tags
    tags = await hub.tool.aws.neptune.tag.get_tags_for_resource(ctx, resource_arn=arn)
    if not tags["result"]:
        result["result"] = False
        result["comment"] = tags["comment"]
        return result
    tags = tags["ret"]
    result[
        "ret"
    ] = hub.tool.aws.neptune.conversion_utils.convert_raw_db_instance_to_present(
        raw_resource=resource, idem_resource_name=name, tags=tags
    )
    return result


async def list_(hub, ctx, name: str = None, filters: List = None) -> Dict:
    """Use a list of un-managed neptune db instances as a data-source. Supply one of the inputs as the filter.

    Args:
        name (str, Optional):
            The name of idem state.

        filters (list, Optional):
            A filter that specifies one or more DB instances to describe.
            Supported filters are,

            * db-cluster(str, Optional):
                Accepts DB cluster identifiers and DB cluster Amazon Resource Names (ARNs). The results list will only include information about the DB instances associated with the DB clusters identified by these ARNs.
            * engine(str, Optional):
                Accepts an engine name (such as neptune ), and restricts the results list to DB instances created by that engine.

    Returns:
        Dict[bool, list, dict or None]:

        result(bool):
            Whether the result of the function has been successful (``True``) or not (``False``).
        comment(list):
            A list of messages.
        ret(dict or None):
           The AWS Neptune DB Instance in "present" format.

    Examples:
        Calling this exec module function from the cli:

        .. code-block:: bash

            idem exec aws.neptune.db_instance.list name="idem_name" filters=[db-cluster-id="", engine=""]

        Calling this exec module function from within a state module in pure python:

        .. code-block:: python

            async def state_function(hub, ctx, name, resource_id, **kwargs):
                ret = await hub.exec.aws.neptune.db_instance.get(
                    ctx, name=name, filters=[db-cluster-id="", engine=""]
                )
    """
    result = dict(comment=[], ret=[], result=True)
    ret = await hub.tool.aws.neptune.db_instance.search_raw(
        ctx=ctx, name=name, filters=filters
    )
    if not ret["result"]:
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    if not ret["ret"]["DBInstances"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type=RESOURCE_TYPE, name=name
            )
        )
        return result
    for db_instance in ret["ret"]["DBInstances"]:
        db_instance_identifier = db_instance.get("DBInstanceIdentifier")
        arn = db_instance["DBInstanceArn"]
        tags = await hub.tool.aws.neptune.tag.get_tags_for_resource(
            ctx, resource_arn=arn
        )
        tags = tags["ret"]
        result["ret"].append(
            hub.tool.aws.neptune.conversion_utils.convert_raw_db_instance_to_present(
                raw_resource=db_instance,
                idem_resource_name=db_instance_identifier,
                tags=tags,
            )
        )
    return result
