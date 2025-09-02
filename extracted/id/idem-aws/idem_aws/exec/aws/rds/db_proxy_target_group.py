"""Exec module for managing Rds Db Proxy Target Groups."""
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["soft_fail"]

__func_alias__ = {"list_": "list"}


async def get(
    hub,
    ctx,
    resource_id: str,
    target_group_name="default",
    filters: List[
        make_dataclass("Filter", [("Name", str), ("Values", List[str])])
    ] = None,
    name: str = None,
) -> Dict[str, Any]:
    """
    Args:
        resource_id(str): Name of the DB Proxy.

        target_group_name(str, Optional): Name of the DB Proxy Target Group.

        filters(List[dict[str, Any]], Optional): This parameter is not currently supported. Defaults to None.

            * Name (str): The name of the filter. Filter names are case-sensitive.

            * Values (List[str]): One or more filter values. Filter values are case-sensitive.

        name(str, Optional): Idem name of the resource. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:
        Resource State:

        .. code-block:: sls

            unmanaged_resource:
              exec.run:
                - path: aws.rds.db_proxy_target_group.get
                - kwargs:
                  resource_id: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec aws.rds.db_proxy_target_group.get resource_id=value
    """

    result = dict(comment=[], ret=None, result=True)

    # Read documentation: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html
    get_db_proxy_target_group = (
        await hub.exec.boto3.client.rds.describe_db_proxy_target_groups(
            ctx=ctx,
            **{
                "DBProxyName": resource_id,
                "TargetGroupName": target_group_name,
                "Filters": filters,
            },
        )
    )

    # Case: Error
    if not get_db_proxy_target_group["result"]:
        # Do not return success=false when it is not found.
        # Most of the resources would return "*NotFound*" type of exception when it is 404
        if "DBProxyTargetGroupNotFoundFault" in str(
            get_db_proxy_target_group["comment"]
        ) or "DBProxyNotFoundFault" in str(get_db_proxy_target_group["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.rds.db_proxy_target_group", name=resource_id
                )
            )
            result["comment"].append(get_db_proxy_target_group["comment"])
            return result

        result["comment"].append(get_db_proxy_target_group["comment"])
        result["result"] = False
        return result

    # Case: Empty results
    if not get_db_proxy_target_group["ret"] or not get_db_proxy_target_group["ret"].get(
        "TargetGroups"
    ):
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.rds.db_proxy_target_group", name=resource_id
            )
        )
        return result

    raw_resource = get_db_proxy_target_group["ret"]["TargetGroups"][0]

    # Possible Resource attributes:
    result[
        "ret"
    ] = await hub.tool.aws.rds.db_proxy_target_group.convert_raw_resource_to_present_async(
        ctx=ctx,
        resource_id=resource_id,
        raw_resource=raw_resource,
        idem_resource_name=name,
    )

    return result


async def list_(
    hub,
    ctx,
    db_proxy_name: str,
    target_group_name="default",
    filters: List[
        make_dataclass("Filter", [("Name", str), ("Values", List[str])])
    ] = None,
    name: str = None,
) -> Dict[str, Any]:
    """
    Args:
        db_proxy_name(str): Name of the DB Proxy.

        target_group_name(str, Optional): Name of the DB Proxy Target Group.

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
                - path: aws.rds.db_proxy_target_group.list
                - kwargs:


        Exec call from the CLI:

        .. code-block:: bash

            idem exec aws.rds.db_proxy_target_group.list

        Describe call from the CLI:

        .. code-block:: bash

            $ idem describe aws.rds.db_proxy_target_group

    """

    result = dict(comment=[], ret=[], result=True)

    # Read documentation: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html
    get_db_proxy_target_group = (
        await hub.exec.boto3.client.rds.describe_db_proxy_target_groups(
            ctx=ctx,
            **{
                "DBProxyName": db_proxy_name,
                "TargetGroupName": target_group_name,
                "Filters": filters,
            },
        )
    )

    if not get_db_proxy_target_group["result"]:
        result["comment"].append(get_db_proxy_target_group["comment"])
        result["result"] = False
        return result

    if not get_db_proxy_target_group["ret"].get("TargetGroups"):
        result["comment"].append(
            hub.tool.aws.comment_utils.list_empty_comment(
                resource_type="aws.rds.db_proxy_target_group", name=db_proxy_name
            )
        )
        return result

    # Possible Resource attributes:
    for resource in get_db_proxy_target_group["ret"]["TargetGroups"]:
        result["ret"].append(
            await hub.tool.aws.rds.db_proxy_target_group.convert_raw_resource_to_present_async(
                ctx=ctx,
                resource_id=db_proxy_name,
                raw_resource=resource,
                idem_resource_name=name if name else db_proxy_name,
            )
        )
    return result


async def update(
    hub,
    ctx,
    db_proxy_name: str,
    target_group_name: str = "default",
    connection_pool_config: make_dataclass(
        "ConnectionPoolConfiguration",
        [
            ("MaxConnectionsPercent", int, field(default=None)),
            ("MaxIdleConnectionsPercent", int, field(default=None)),
            ("ConnectionBorrowTimeout", int, field(default=None)),
            ("SessionPinningFilters", List[str], field(default=None)),
            ("InitQuery", str, field(default=None)),
        ],
    ) = None,
    resource_id: str = None,
    name: str = None,
) -> Dict[str, Any]:
    """
    Args:
        db_proxy_name(str): Name of the DB Proxy.

        target_group_name(str, Optional): Name of the DB Proxy Target Group

        connection_pool_config(Dict[str, Any], Optional): The settings that determine the size and behavior of the connection pool for the target group.
            * MaxConnectionsPercent (int) –
                The maximum size of the connection pool for each target in a target group. The value is expressed as a
                percentage of the max_connections setting for the RDS DB instance or Aurora DB cluster used by the target group.
                If you specify MaxIdleConnectionsPercent, then you must also include a value for this parameter.
                Default: 10 for RDS for Microsoft SQL Server, and 100 for all other engines
                Constraints: Must be between 1 and 100.

            * MaxIdleConnectionsPercent (int) –
                Controls how actively the proxy closes idle database connections in the connection pool.
                The value is expressed as a percentage of the max_connections setting for the RDS DB instance or
                Aurora DB cluster used by the target group. With a high value, the proxy leaves a high percentage of
                idle database connections open. A low value causes the proxy to close more idle connections and return
                them to the database.
                If you specify this parameter, then you must also include a value for MaxConnectionsPercent.
                Default: The default value is half of the value of MaxConnectionsPercent. For example,
                if MaxConnectionsPercent is 80, then the default value of MaxIdleConnectionsPercent is 40.
                If the value of MaxConnectionsPercent isn’t specified, then for SQL Server,
                MaxIdleConnectionsPercent is 5, and for all other engines, the default is 50.
                Constraints: Must be between 0 and the value of MaxConnectionsPercent.

            * ConnectionBorrowTimeout (integer):
                The number of seconds for a proxy to wait for a connection to become available in the connection pool.
                Only applies when the proxy has opened its maximum number of connections and all connections
                are busy with client sessions.
                Default: 120
                Constraints: between 1 and 3600, or 0 representing unlimited

            * SessionPinningFilters (List[str]):
                Each item in the list represents a class of SQL operations that normally cause all later statements in
                a session using a proxy to be pinned to the same underlying database connection. Including an item in
                the list exempts that class of SQL operations from the pinning behavior.
                Default: no session pinning filters

            * InitQuery (str):
                One or more SQL statements for the proxy to run when opening each new database connection.
                Typically used with SET statements to make sure that each connection has identical settings such as
                time zone and character set. For multiple statements, use semicolons as the separator.
                You can also include multiple variables in a single SET statement, such as SET x=1, y=2.
                Default: no initialization query

        resource_id(str, Optional): Name of the DB Proxy.

        name(str, Optional): Idem name of the resource. Defaults to None.

    Returns:
        Dict[str, Any]

    Examples:
        Using in a state:

        .. code-block:: sls

            resource_is_present:
              aws.rds.db_proxy_target_group.present:
                - tags: value

        Exec call from the CLI:

        .. code-block:: bash

            idem exec aws.rds.db_proxy_target_group.create resource_id=value
    """

    result = dict(comment=[], ret={}, result=True)

    # Read documentation: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/rds.html
    modify_target_group = await hub.exec.boto3.client.rds.modify_db_proxy_target_group(
        ctx,
        **{
            "TargetGroupName": "default",
            "DBProxyName": db_proxy_name,
            "ConnectionPoolConfig": connection_pool_config,
        },
    )

    result["result"] = modify_target_group["result"]
    if not result["result"]:
        result["comment"].append(modify_target_group["comment"])
        return result

    result["comment"].append(
        f"Updated aws.rds.db_proxy_target_group '{name}'",
    )

    raw_resource = modify_target_group["ret"].get("DBProxyTargetGroup", {})
    result["ret"]["resource_id"] = raw_resource.get("DBProxyName")
    result["ret"]["name"] = name

    return result
