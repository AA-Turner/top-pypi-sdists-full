"""Exec module for managing Amazon DocDB DB Cluster."""
from typing import List

__func_alias__ = {"list_": "list"}

RESOURCE_TYPE = "aws.docdb.db_cluster"


async def get(hub, ctx, name: str, resource_id: str = None):
    """Retrieves the specified AWS Document DB Cluster.

    Args:
        resource_id(str, Optional):
            AWS Document DB Cluster Identifier. If resource_id is not given name will be used to retrieve the DB Cluster.
        name(str):
            An Idem name of the resource.

    Examples:
        Calling this exec module function from the cli:

        .. code-block:: bash

            idem exec aws.docdb.db_cluster.get resource_id="resource_id" name="name"

        .. code-block:: python

            async def state_function(hub, ctx, name, resource_id, **kwargs):
                ret = await hub.exec.aws.docdb.db_cluster.get(
                    ctx, name=name, resource_id=resource_id
                )

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.docdb.db_cluster.get
                - kwargs:
                    name: name
                    resource_id: resource_id

    """
    result = dict(comment=[], result=True, ret=None, resource_arn=None)

    raw_db_cluster_result = await hub.exec.boto3.client.docdb.describe_db_clusters(
        ctx, DBClusterIdentifier=resource_id if resource_id else name
    )
    if not raw_db_cluster_result["result"]:
        if "DBClusterNotFoundFault" in str(raw_db_cluster_result["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type=RESOURCE_TYPE,
                    name=name,
                )
            )
            result["comment"].append(raw_db_cluster_result["comment"])
            return result
        result["result"] = False
        result["comment"].append(raw_db_cluster_result["comment"])
        return result

    # if we don't find db_cluster with provided resource id, fail the request
    if not (raw_db_cluster_result["ret"].get("DBClusters")):
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type=RESOURCE_TYPE,
                name=name,
            )
        )
        return result
    if len(raw_db_cluster_result["ret"].get("DBClusters")) > 1:
        result["comment"].append(
            hub.tool.aws.comment_utils.find_more_than_one(
                resource_id=resource_id, resource_type=RESOURCE_TYPE
            )
        )
    resource_arn = raw_db_cluster_result["ret"].get("DBClusters")[0].get("DBClusterArn")
    tags = await hub.tool.aws.docdb.tag.get_tags_for_resource(
        ctx, resource_arn=resource_arn
    )
    # if failure while fetching tags, fail the request
    if not tags["result"]:
        result["result"] = False
        result["comment"].append(tags["comment"])
        return result
    tags = tags["ret"]
    result["ret"] = hub.tool.aws.docdb.db_cluster.convert_raw_db_cluster_to_present(
        raw_resource=raw_db_cluster_result["ret"]["DBClusters"][0],
        idem_resource_name=name,
        tags=tags,
    )
    return result


async def list_(hub, ctx, name: str = None, filters: List = None):
    """

    Args:
        name(str, Optional):
            The name of idem state.
        filters(list, Optional):
            One or more filters, A complete list of filters can be found at
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/docdb.html#DocDB.Client.describe_db_clusters

    Returns:
        Dict[bool, list, dict or None]:

        result(bool):
            Whether the result of the function has been successful (``True``) or not (``False``).
        comment(list):
            A list of messages.
        ret(dict or None):
           The AWS Doc DB Cluster in "present" format.

    Examples:
        Calling this exec module function from the cli:

        .. code-block:: bash

            idem exec aws.docdb.db_cluster.list name="idem_name"

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.docdb.db_cluster.list
                - kwargs:
                    name: dbg1
                    filters:
                      - name: filter-name
                        values:
                            - filter_value


    """
    result = dict(comment=[], ret=[], result=True)

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

    ret = await hub.exec.boto3.client.docdb.describe_db_clusters(
        ctx, Filters=boto3_filter
    )
    if not ret["result"]:
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    if not ret["ret"]["DBClusters"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.list_empty_comment(
                resource_type=RESOURCE_TYPE, name=name
            )
        )
        return result
    result["comment"] = list(ret["comment"])
    for db_cluster in ret["ret"]["DBClusters"]:
        db_cluster_identifier = db_cluster.get("DBClusterIdentifier")
        arn = db_cluster["DBClusterArn"]
        tags = await hub.tool.aws.docdb.tag.get_tags_for_resource(ctx, resource_arn=arn)
        if not tags["result"]:
            result["result"] = False
            result["comment"].append(tags["comment"])
            return result
        tags = tags["ret"]
        result["ret"].append(
            hub.tool.aws.docdb.db_cluster.convert_raw_db_cluster_to_present(
                raw_resource=db_cluster,
                idem_resource_name=db_cluster_identifier,
                tags=tags,
            )
        )
    return result
