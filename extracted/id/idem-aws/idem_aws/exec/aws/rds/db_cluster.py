"""
Exec module for rds.db_cluster
"""
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List


__func_alias__ = {"list_": "list"}


async def get(hub, ctx, resource_id: str, name: str = None) -> Dict[str, Any]:
    """
    Returns information about Amazon Aurora DB clusters and Multi-AZ DB clusters. For more information on Amazon Aurora
    DB clusters, see  What is Amazon Aurora? in the Amazon Aurora User Guide. For more information on Multi-AZ DB
    clusters, see  Multi-AZ deployments with two readable standby DB instances in the Amazon RDS User Guide. This
    operation can also return information for Amazon Neptune DB instances and Amazon DocumentDB instances.

        Args:
            resource_id (str):
                An identifier of the resource in the provider. Defaults to None.

            name(str, Optional): Idem name of the resource. Defaults to None.

        Examples:

            .. code-block:: bash

                idem exec aws_auto.rds.db_cluster.get.get resource_id=0123456789abcdef

            .. code-block:: python

                async def my_func(hub, ctx):
                    ret = await hub.exec.aws_auto.rds.db_cluster.get.get(ctx, resource_id=0123456789abcdef)

            .. code-block:: yaml

                aws_auto_rds_db_cluster_get_resource:
                  exec.run:
                    - path: aws_auto.rds.db_cluster.get
                    - kwargs:
                        resource_id: 0123456789abcdef

    """

    result = {
        "comment": [],
        "ret": None,
        "result": True,
    }

    ret = await hub.exec.boto3.client.rds.describe_db_clusters(
        ctx=ctx,
        DBClusterIdentifier=resource_id,
    )

    if not ret["result"]:
        if "DBClusterNotFoundFault" in str(ret.get("comment", "")):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.rds.db_cluster",
                    name=name if name else resource_id,
                )
            )
        else:
            ret["result"] = False
        result["comment"] += list(ret["comment"])
        return result
    if not ret["ret"]["DBClusters"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.rds.db_cluster",
                name=name if name else resource_id,
            )
        )
        return result

    resource = ret["ret"]["DBClusters"][0]
    if len(ret["ret"]["DBClusters"]) > 1:
        result["comment"].append(
            f"More than one aws.rds.db_cluster resource was found. Use resource {resource.get('DBClusterIdentifier')}"
        )
    result["ret"] = hub.tool.aws.rds.conversion_utils.convert_raw_db_cluster_to_present(
        idem_resource_name=name if name else resource_id,
        raw_resource=resource,
    )
    return result


async def list_(
    hub,
    ctx,
    filters: List[
        make_dataclass("Filter", [("Name", str), ("Values", List[str])])
    ] = None,
) -> Dict[str, Any]:
    """
    Returns information about Amazon Aurora DB clusters and Multi-AZ DB clusters. For more information on Amazon Aurora
    DB clusters, see  What is Amazon Aurora? in the Amazon Aurora User Guide. For more information on Multi-AZ DB
    clusters, see  Multi-AZ deployments with two readable standby DB instances in the Amazon RDS User Guide. This
    operation can also return information for Amazon Neptune DB instances and Amazon DocumentDB instances.

        Args:
            filters (list[Dict[str, Any]], Optional):
                A filter that specifies one or more DB clusters to describe.

                Supported filters:

                    * clone-group-id:
                        Accepts clone group identifiers. The results list only includes information about the DB
                        clusters associated with these clone groups.

                    * db-cluster-id:
                        Accepts DB cluster identifiers and DB cluster Amazon Resource Names (ARNs). The results list
                        only includes information about the DB clusters identified by these ARNs.

                    * domain:
                        Accepts Active Directory directory IDs.  The results list only includes information about the
                        DB clusters associated with these domains.

                    * engine:
                        Accepts engine names. The results list only includes information about the DB clusters for
                        these engines. Defaults to None.

                * Name (str):
                    The name of the filter. Filter names are case-sensitive.

                * Values (list[str]):
                    One or more filter values. Filter values are case-sensitive.

        Examples:

            .. code-block:: bash

                idem exec aws_auto.rds.db_cluster.list

            .. code-block:: python

                async def my_func(hub, ctx):
                    ret = await hub.exec.aws_auto.rds.db_cluster.list(ctx)

            .. code-block:: yaml

                aws_auto_rds_db_cluster_list_resource:
                  exec.run:
                    - path: aws_auto.rds.db_cluster.list

    """

    result = {
        "comment": [],
        "ret": None,
        "result": True,
    }
    ret = await hub.exec.boto3.client.rds.describe_db_clusters(
        ctx=ctx,
        filters=filters,
    )
    if not ret["result"]:
        result["comment"] += list(ret["comment"])
        return result
    if not ret["ret"]["DBClusters"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.rds.db_cluster",
                name="rds.db_cluster.list",
            )
        )
        return result

    result["ret"] = []
    for resource in ret["ret"]["DBClusters"]:
        result["ret"].append(
            hub.tool.aws.rds.conversion_utils.convert_raw_db_cluster_to_present(
                raw_resource=resource
            )
        )
    return result
