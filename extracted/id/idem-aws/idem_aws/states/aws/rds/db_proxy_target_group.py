"""States module for managing Rds Db Proxy Target Groups."""
import copy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

from dict_tools import differ

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
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
) -> Dict[str, Any]:
    """
    Args:
        name(str): Idem name of the resource.

        db_proxy_name(str): The Name of the DB Proxy.

        target_group_name(str, Optional): Name of the target group.

        connection_pool_config: The settings that determine the size and behavior of the connection pool for the target group.
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

        resource_id(str, Optional): Db_proxy_target_group unique ID. Defaults to None.

    Returns:
        Dict[str, Any]

    Example:
        .. code-block:: sls


          idem_test_aws.rds.db_proxy_target_group_is_present:
              aws.aws.rds.db_proxy_target_group.present:
                - db_proxy_name: idem-test-db-proxy
                - connection_pool_config:
                    MaxConnectionsPercent: 80
                    MaxIdleConnectionsPercent: 20
                    ConnectionBorrowTimeout: 100




    """

    result = dict(
        comment=[], old_state={}, new_state={}, name=name, result=True, rerun_data=None
    )

    desired_state = {
        k: v
        for k, v in locals().items()
        if k not in ("hub", "ctx", "kwargs", "result") and v is not None
    }

    current_state = None
    if resource_id:
        before = await hub.exec.aws.rds.db_proxy_target_group.get(
            ctx, name=name, resource_id=resource_id
        )
        if not before["result"] or not before["ret"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result

        result["old_state"] = current_state = copy.deepcopy(before["ret"])
        result["comment"] += hub.tool.aws.comment_utils.already_exists_comment(
            resource_type="aws.rds.db_proxy_target_group", name=name
        )

    if current_state and connection_pool_config:
        # If there are changes in desired state from existing state
        changes = differ.deep_diff(
            current_state.get("connection_pool_config"), connection_pool_config
        )

        if bool(changes.get("new")):
            if ctx.test:
                result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                    enforced_state={}, desired_state=desired_state
                )
                result["comment"] += hub.tool.aws.comment_utils.would_create_comment(
                    resource_type="aws.rds.db_proxy_target_group", name=name
                )
                return result
            else:
                # Update the resource
                update_ret = await hub.exec.aws.rds.db_proxy_target_group.update(
                    ctx,
                    **desired_state,
                )
                result["result"] = update_ret["result"]

                if result["result"]:
                    result["comment"] += hub.tool.aws.comment_utils.update_comment(
                        resource_type="aws.rds.db_proxy_target_group", name=name
                    )
                else:
                    result["comment"].append(update_ret["comment"])
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={}, desired_state=desired_state
            )
            result["comment"] += hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.rds.db_proxy_target_group", name=name
            )
            return result

        create_ret = await hub.exec.aws.rds.db_proxy_target_group.update(
            ctx,
            **desired_state,
        )
        result["result"] = create_ret["result"]

        if result["result"]:
            result["comment"] += hub.tool.aws.comment_utils.create_comment(
                resource_type="aws.rds.db_proxy_target_group", name=name
            )
            resource_id = create_ret["ret"].get("resource_id")
            # Safeguard for any future errors so that the resource_id is saved in the ESM
            result["new_state"] = dict(name=name, resource_id=resource_id)
        else:
            result["comment"].append(create_ret["comment"])

    if not result["result"]:
        # If there is any failure in create/update, it should reconcile.
        # The type of data is less important here to use default reconciliation
        # If there are no changes for 3 runs with rerun_data, then it will come out of execution
        result["rerun_data"] = dict(name=name, resource_id=resource_id)

    after = await hub.exec.aws.rds.db_proxy_target_group.get(
        ctx, name=name, resource_id=resource_id
    )
    result["new_state"] = after.ret
    return result


async def absent(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
) -> Dict[str, Any]:
    """

    Args:
        name(str): Idem name of the resource.

        resource_id(str, Optional): Db_proxy_target_group unique ID. Defaults to None.

    Returns:
        Dict[str, Any]

    Example:
        .. code-block:: sls


            idem_test_aws.rds.db_proxy_target_group_is_absent:
              aws.aws.rds.db_proxy_target_group.absent: []


    """

    result = dict(
        comment=[], old_state={}, new_state={}, name=name, result=True, rerun_data=None
    )
    result["comment"].append("DB Proxy Target group cannot be deleted.")
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """
    Describe the resource in a way that can be recreated/managed with the corresponding "present" function



    Returns:
        Dict[str, Any]

    Example:

        .. code-block:: bash

            $ idem describe aws.rds.db_proxy_target_group
    """

    result = {}
    db_proxy_ret = await hub.exec.aws.rds.db_proxy.list(ctx)

    if not db_proxy_ret or not db_proxy_ret["result"]:
        hub.log.warning(
            f"Could not describe aws.rds.db_proxy {db_proxy_ret['comment']}"
        )
        return result
    for db_proxy in db_proxy_ret["ret"]:
        ret = await hub.exec.aws.rds.db_proxy_target_group.list(
            ctx, db_proxy_name=db_proxy.get("resource_id")
        )

        if not ret or not ret["result"]:
            hub.log.warning(
                f"Could not describe aws.rds.db_proxy_target_group {ret['comment']}"
            )
            return result

        for resource in ret["ret"]:
            resource_id = resource.get("resource_id")
            result[resource_id] = {
                "aws.rds.db_proxy_target_group.present": [
                    {parameter_key: parameter_value}
                    for parameter_key, parameter_value in resource.items()
                ]
            }
    return result
