"""Exec module for managing Rds Db Proxy Targets."""
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["soft_fail"]

__func_alias__ = {"list_": "list"}


async def get(
    hub,
    ctx,
    db_proxy_name: str = None,
    resource_id: str = None,
    target_group_name: str = None,
    name: str = None,
) -> Dict[str, Any]:
    """

    Returns information about DBProxyTarget objects. This API supports pagination.

    Args:
        db_proxy_name(str, Optional): The identifier of the DBProxyTarget to describe.

        resource_id(str, Optional): Db_proxy_target unique ID.

        target_group_name(str, Optional): The identifier of the DBProxyTargetGroup to describe. Defaults to None.

        name(str, Optional): Idem name of the resource. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:
        Resource State:

        .. code-block:: sls

            unmanaged_resource:
              exec.run:
                - path: aws.rds.db_proxy_target.get
                - kwargs:
                  db_proxy_name: value
                  resource_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec aws.rds.db_proxy_target.get db_proxy_name=value, resource_id=value
    """

    result = dict(comment=[], ret=None, result=True)
    if resource_id:
        resource_id_arr = resource_id.split("/")
        if len(resource_id_arr) < 4:
            result["result"] = False
            result["comment"].append(
                "Invalid resource_id. resource_id should be in format {db_proxy_name}/{target_group_name}/{target_group_type}/{rds_instance_id}"
            )
            return result
        db_proxy_name = resource_id_arr[0]
        target_group_name = resource_id_arr[1]
    db_proxy_target_get = await hub.exec.boto3.client.rds.describe_db_proxy_targets(
        ctx=ctx,
        **{"DBProxyName": db_proxy_name, "TargetGroupName": target_group_name},
    )

    # Case: Error
    if not db_proxy_target_get["result"]:
        # Do not return success=false when it is not found.
        # Most of the resources would return "*NotFound*" type of exception when it is 404
        if (
            "DBProxyNotFoundFault" in str(db_proxy_target_get["comment"])
            or "DBProxyTargetNotFoundFault" in str(db_proxy_target_get["comment"])
            or "DBProxyTargetGroupNotFoundFault" in str(db_proxy_target_get["comment"])
        ):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.rds.db_proxy_target", name=resource_id
                )
            )
            result["comment"].append(db_proxy_target_get["comment"])
            return result

        result["comment"].append(db_proxy_target_get["comment"])
        result["result"] = False
        return result

    # Case: Empty results
    if not db_proxy_target_get["ret"] or not db_proxy_target_get["ret"]["Targets"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.rds.db_proxy_target", name=resource_id
            )
        )
        return result

    if len(db_proxy_target_get["ret"]["Targets"]) > 1:
        result["comment"].append(
            hub.tool.aws.comment_utils.find_more_than_one(
                resource_id=resource_id, resource_type="aws.rds.db_proxy_target"
            )
        )

    raw_resource = db_proxy_target_get["ret"]["Targets"][0]
    result[
        "ret"
    ] = await hub.tool.aws.rds.db_proxy_target.convert_raw_resource_to_present_async(
        ctx=ctx,
        resource_id=resource_id,
        raw_resource=raw_resource,
        idem_resource_name=name,
        db_proxy_name=db_proxy_name,
        target_group_name=target_group_name,
    )

    return result


async def list_(
    hub,
    ctx,
    db_proxy_name: str,
    target_group_name: str = "default",
    name: str = None,
) -> Dict[str, Any]:
    """
    Returns information about DBProxyTarget objects. This API supports pagination.

    Args:
        db_proxy_name(str): The identifier of the DBProxy to describe.

        target_group_name(str): The identifier of the DBProxyTargetGroup to describe. Defaults to None.

        filters(List[dict[str, Any]], Optional): This parameter is not currently supported. Defaults to None.

            * Name (str): The name of the filter. Filter names are case-sensitive.

            * Values (List[str]): One or more filter values. Filter values are case-sensitive.

        name(str, Optional): Idem name of the resource. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:

        Resource State:

        .. code-block:: sls

            unmanaged_resources:
              exec.run:
                - path: aws.rds.db_proxy_target.list
                - kwargs:
                  db_proxy_name: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec aws.rds.db_proxy_target.list db_proxy_name=value

        Describe call from the CLI:

        .. code-block:: bash

            $ idem describe aws.rds.db_proxy_target

    """

    result = dict(comment=[], ret=[], result=True)

    ret = await hub.exec.boto3.client.rds.describe_db_proxy_targets(
        ctx=ctx,
        **{
            "DBProxyName": db_proxy_name,
            "TargetGroupName": target_group_name,
        },
    )

    if not ret["result"]:
        result["comment"].append(ret["comment"])
        result["result"] = False
        return result

    if not ret["ret"].get("Targets"):
        result["comment"].append(
            hub.tool.aws.comment_utils.list_empty_comment(
                resource_type="aws.rds.db_proxy_target", name=None
            )
        )
        return result

    for resource in ret["ret"]["Targets"]:
        resource_id = hub.tool.aws.rds.db_proxy_target.create_resource_id(
            resource, db_proxy_name, target_group_name
        )
        result["ret"].append(
            await hub.tool.aws.rds.db_proxy_target.convert_raw_resource_to_present_async(
                ctx=ctx,
                resource_id=resource_id,
                raw_resource=resource,
                idem_resource_name=name if name else resource_id,
                db_proxy_name=db_proxy_name,
                target_group_name=target_group_name,
            )
        )
    return result


async def create(
    hub,
    ctx,
    db_proxy_name: str,
    target_group_name: str,
    db_instance_identifiers: List[str] = None,
    db_cluster_identifiers: List[str] = None,
    resource_id: str = None,
    name: str = None,
) -> Dict[str, Any]:
    """
    Associate one or more DBProxyTarget data structures with a DBProxyTargetGroup.

    Args:
        db_proxy_name(str): The identifier of the DBProxy that is associated with the DBProxyTargetGroup.

        target_group_name(str, Optional): The identifier of the DBProxyTargetGroup. Defaults to None.

        db_instance_identifiers(List[str], Optional): One or more DB instance identifiers. Defaults to None.

        db_cluster_identifiers(List[str], Optional): One or more DB cluster identifiers. Defaults to None.

        resource_id(str, Optional): Db_proxy_target unique ID. Defaults to None.

        name(str, Optional): Idem name of the resource. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:
        Using in a state:

        .. code-block:: sls

            resource_is_present:
              aws.rds.db_proxy_target.present:
                - db_proxy_name: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec aws.rds.db_proxy_target.create db_proxy_name=value
    """

    result = dict(comment=[], ret={}, result=True)

    desired_state = {
        k: v
        for k, v in locals().items()
        if k not in ("hub", "ctx", "kwargs", "result") and v is not None
    }

    resource_to_raw_input_mapping = {
        "db_proxy_name": "DBProxyName",
        "target_group_name": "TargetGroupName",
        "db_instance_identifiers": "DBInstanceIdentifiers",
        "db_cluster_identifiers": "DBClusterIdentifiers",
    }

    payload = {}
    for key, value in desired_state.items():
        if key in resource_to_raw_input_mapping.keys() and value is not None:
            payload[resource_to_raw_input_mapping[key]] = desired_state.get(key)

    ret = await hub.exec.boto3.client.rds.register_db_proxy_targets(ctx, **payload)

    result["result"] = ret["result"]
    if not result["result"]:
        result["comment"].append(ret["comment"])
        return result

    result["comment"].append(
        f"Created aws.rds.db_proxy_target '{name}'",
    )

    raw_resource = ret["ret"].get("DBProxyTargets")[0]
    result["ret"]["resource_id"] = hub.tool.aws.rds.db_proxy_target.create_resource_id(
        raw_resource, db_proxy_name, target_group_name
    )
    result["ret"]["name"] = name

    return result


async def delete(
    hub,
    ctx,
    resource_id: str,
    db_instance_identifiers: List[str] = None,
    db_cluster_identifiers: List[str] = None,
    name: str = None,
) -> Dict[str, Any]:
    """
    Remove the association between one or more DBProxyTarget data structures and a DBProxyTargetGroup.

    Args:
        resource_id(str): Db_proxy_target unique ID.

        db_instance_identifiers(List[str], Optional): One or more DB instance identifiers. Defaults to None.

        db_cluster_identifiers(List[str], Optional): One or more DB cluster identifiers. Defaults to None.

        name(str, Optional): Idem name of the resource. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:
        Resource State:

        .. code-block:: sls

            resource_is_absent:
              aws.rds.db_proxy_target.absent:
                - db_proxy_name: value
                - resource_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec aws.rds.db_proxy_target.delete db_proxy_name=value, resource_id=value
    """

    result = dict(comment=[], ret=None, result=True)
    resource_id_arr = resource_id.split("/")
    if len(resource_id_arr) < 4:
        result["result"] = False
        result["comment"].append(
            "Invalid resource_id. resource_id should be in format {db_proxy_name}/{target_group_name}/{target_group_type}/{rds_instance_id}"
        )
        return result
    db_proxy_name = resource_id_arr[0]
    target_group_name = resource_id_arr[1]

    delete_ret = await hub.exec.boto3.client.rds.deregister_db_proxy_targets(
        ctx,
        **{
            "DBProxyName": db_proxy_name,
            "TargetGroupName": target_group_name,
            "DBInstanceIdentifiers": db_instance_identifiers,
            "DBClusterIdentifiers": db_cluster_identifiers,
        },
    )

    result["result"] = delete_ret["result"]

    if not result["result"]:
        result["comment"] = delete_ret["comment"]
        result["result"] = False
        return result

    result["comment"] = hub.tool.aws.comment_utils.delete_comment(
        resource_type="aws.rds.db_proxy_target", name=name
    )

    return result
