"""
Exec module for rds.db_instance
"""
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List


__func_alias__ = {"list_": "list"}


async def get(hub, ctx, resource_id: str, name: str = None) -> Dict[str, Any]:
    """
    Returns information about provisioned RDS instances. This operation can also return information for Amazon Neptune
    DB instances and Amazon DocumentDB instances.

        Args:
            resource_id (str):
                An identifier of the resource in the provider. Defaults to None.

            name(str, Optional): Idem name of the resource. Defaults to None.

        Examples:

            .. code-block:: bash

                idem exec aws_auto.rds.db_instance.get resource_id=0123456789abcdef

            .. code-block:: python

                async def my_func(hub, ctx):
                    ret = await hub.exec.aws_auto.rds.db_instance.get(ctx, resource_id="01235789abcdef")

            .. code-block:: yaml

                aws_auto_rds_db_instance_get_resource:
                  exec.run:
                    - path: aws_auto.rds.db_instance.get
                    - resource_id: 0123456789abcdef

    """
    result = {
        "comment": [],
        "ret": None,
        "result": True,
    }
    ret = await hub.exec.boto3.client.rds.describe_db_instances(
        ctx=ctx,
        DBInstanceIdentifier=resource_id,
    )
    if not ret["result"]:
        if "DBInstanceNotFoundFault" in str(ret.get("comment", "")):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.rds.db_instance",
                    name=name if name else resource_id,
                )
            )
        else:
            ret["result"] = False
        result["comment"] += list(ret["comment"])
        return result
    if not ret["ret"]["DBInstances"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.rds.db_instance", name=name if name else resource_id
            )
        )
        return result

    resource = ret["ret"]["DBInstances"][0]
    if len(ret["ret"]["DBInstances"]) > 1:
        result["comment"].append(
            f"More than one aws.rds.db_instance resource was found. Use resource {resource.get('DBInstanceIdentifier')}"
        )
    tags = await hub.exec.boto3.client.rds.list_tags_for_resource(
        ctx, ResourceName=resource["DBInstanceArn"]
    )
    if not tags["result"]:
        result["result"] = False
        result["comment"] = tags["comment"]
        return result
    result[
        "ret"
    ] = hub.tool.aws.rds.conversion_utils.convert_raw_db_instance_to_present(
        raw_resource=resource,
        raw_resource_tags=tags,
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
    Returns information about provisioned RDS instances. This operation can also return information for Amazon
    Neptune DB instances and Amazon DocumentDB instances.

        Args:
            filters (list[Dict[str, Any]], Optional):
                A filter that specifies one or more DB instances to describe.

                Supported filters:
                * db-cluster-id (str, Optional):
                    Accepts DB cluster identifiers and DB cluster Amazon Resource Names (ARNs). The results list only
                    includes information about the DB instances associated with the DB clusters identified by these
                    ARNs.

                * db-instance-id (str, Optional):
                    Accepts DB instance identifiers and DB instance Amazon Resource Names (ARNs). The results list only
                    includes information about the DB instances identified by these ARNs.

                * dbi-resource-id (str, Optional):
                    Accepts DB instance resource identifiers. The results list will only include information about the
                    DB instances identified by these DB instance resource identifiers.

                * domain (str, Optional):
                    Accepts Active Directory directory IDs. The results list only includes information about the DB
                    instances associated with these domains.

                * engine (str, Optional):
                    Accepts engine names. The results list only includes information about the DB instances for these
                    engines. Defaults to None.

                * Name (str):
                    The name of the filter. Filter names are case-sensitive.

                * Values (list[str]):
                    One or more filter values. Filter values are case-sensitive.

        Examples:

            .. code-block:: bash

                idem exec aws_auto.rds.db_instance.list

            .. code-block:: python

                async def my_func(hub, ctx):
                    ret = await hub.exec.aws_auto.rds.db_instance.list(ctx)

            .. code-block:: yaml

                aws_auto_rds_db_instance_list_resource:
                  exec.run:
                    - path: aws_auto.rds.db_instance.list

    """
    result = {
        "comment": [],
        "ret": None,
        "result": True,
    }
    ret = await hub.exec.boto3.client.rds.describe_db_instances(
        ctx=ctx,
        filters=filters,
    )

    result["ret"] = []
    for resource in ret["ret"]["DBInstances"]:
        tags = await hub.exec.boto3.client.rds.list_tags_for_resource(
            ctx,
            ResourceName=resource["DBInstanceArn"],
        )
        if not tags["result"]:
            result["result"] = False
            result["comment"] = tags["comment"]
            return result
        result["ret"].append(
            hub.tool.aws.rds.conversion_utils.convert_raw_db_instance_to_present(
                raw_resource=resource,
                raw_resource_tags=tags,
            )
        )
    return result
