"""States module for managing Rds Db Proxy Targets."""
import copy
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    db_proxy_name: str,
    target_group_name: str,
    db_instance_identifiers: List[str] = None,
    db_cluster_identifiers: List[str] = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    """
    Associate one or more DBProxyTarget data structures with a DBProxyTargetGroup.

    Args:
        name(str): Idem name of the resource.

        db_proxy_name(str): The identifier of the DBProxy that is associated with the DBProxyTargetGroup.

        target_group_name(str, Optional): The identifier of the DBProxyTargetGroup. Defaults to None.

        db_instance_identifiers(List[str], Optional): One or more DB instance identifiers. Defaults to None.

        db_cluster_identifiers(List[str], Optional): One or more DB cluster identifiers. Defaults to None.

        resource_id(str, Optional): Db_proxy_target unique ID. Defaults to None.

    Returns:
        Dict[str, Any]

    Example:
        .. code-block:: sls


          idem_test_aws_auto.rds.db_proxy_target_is_present:
              aws_auto.aws_auto.rds.db_proxy_target.present:
              - db_proxy_name: string
              - target_group_name: string
              - db_instance_identifiers:
                - value
              - db_cluster_identifiers:
                - value
              - tags: dict


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
        before = await hub.exec.aws.rds.db_proxy_target.get(
            ctx, name=name, resource_id=resource_id
        )
        if not before["result"] or not before["ret"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result

        result["old_state"] = current_state = copy.deepcopy(before["ret"])
        result["comment"] += hub.tool.aws.comment_utils.already_exists_comment(
            resource_type="aws.rds.db_proxy_target", name=name
        )
        result["new_state"] = copy.deepcopy(result["old_state"])
        return result

    if ctx.get("test", False):
        result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
            enforced_state={}, desired_state=desired_state
        )
        result["comment"] += hub.tool.aws.comment_utils.would_create_comment(
            resource_type="aws.rds.db_proxy_target", name=name
        )
        return result

    create_ret = await hub.exec.aws.rds.db_proxy_target.create(
        ctx,
        **desired_state,
    )
    result["result"] = create_ret["result"]

    if result["result"]:
        result["comment"] += hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.rds.db_proxy_target", name=name
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

    after = await hub.exec.aws.rds.db_proxy_target.get(
        ctx, name=name, resource_id=resource_id
    )
    result["new_state"] = after.ret
    return result


async def absent(
    hub,
    ctx,
    name: str,
    db_instance_identifiers: List[str] = None,
    db_cluster_identifiers: List[str] = None,
    resource_id: str = None,
) -> Dict[str, Any]:
    """

    Remove the association between one or more DBProxyTarget data structures and a DBProxyTargetGroup.

    Args:
        name(str): Idem name of the resource.

        db_instance_identifiers(List[str], Optional): One or more DB instance identifiers. Defaults to None.

        db_cluster_identifiers(List[str], Optional): One or more DB cluster identifiers. Defaults to None.

        resource_id(str, Optional): Db_proxy_target unique ID. Defaults to None.

    Returns:
        Dict[str, Any]

    Example:
        .. code-block:: sls


            idem_test_aws_auto.rds.db_proxy_target_is_absent:
              aws_auto.aws_auto.rds.db_proxy_target.absent:
              - target_group_name: string
              - db_instance_identifiers:
                - value
              - db_cluster_identifiers:
                - value


    """

    result = dict(
        comment=[], old_state={}, new_state={}, name=name, result=True, rerun_data=None
    )

    if not resource_id:
        resource_id = (ctx.old_state or {}).get("resource_id")

    # This is to make absent idempotent. If absent is run again, it would be a no-op
    if not resource_id:
        result["comment"] += hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.rds.db_proxy_target", name=name
        )
        return result

    before = await hub.exec.aws.rds.db_proxy_target.get(
        ctx, name=name, resource_id=resource_id
    )

    # Case: Error
    if not before["result"]:
        result["result"] = False
        result["comment"] = before["comment"]
        return result

    # Case: Not Found
    if not before["ret"]:
        result["comment"] += hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.rds.db_proxy_target", name=name
        )
        return result

    result["old_state"] = before["ret"]

    if ctx.get("test", False):
        result["comment"].append(
            f"Would delete aws.rds.db_proxy_target '{name}'",
        )
        return result

    delete_ret = await hub.exec.aws.rds.db_proxy_target.delete(
        ctx,
        name=name,
        resource_id=resource_id,
        db_cluster_identifiers=db_cluster_identifiers,
        db_instance_identifiers=db_instance_identifiers,
    )

    result["result"] = delete_ret["result"]

    if not result["result"]:
        # If there is any failure in delete, it should reconcile.
        # The type of data is less important here to use default reconciliation
        # If there are no changes for 3 runs with rerun_data, then it will come out of execution
        result["rerun_data"] = resource_id
        result["comment"].append(delete_ret["comment"])
    else:
        result["comment"] += hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.rds.db_proxy_target", name=name
        )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """
    Describe the resource in a way that can be recreated/managed with the corresponding "present" function

    Returns information about DBProxyTarget objects. This API supports pagination.

    Returns:
        Dict[str, Any]

    Example:

        .. code-block:: bash

            $ idem describe aws_auto.rds.db_proxy_target
    """

    result = {}

    db_proxy_ret = await hub.exec.aws.rds.db_proxy.list(ctx)

    if not db_proxy_ret or not db_proxy_ret["result"]:
        hub.log.warning(
            f"Could not describe aws.rds.db_proxy {db_proxy_ret['comment']}"
        )
        return result
    for db_proxy in db_proxy_ret["ret"]:
        ret = await hub.exec.aws.rds.db_proxy_target.list(
            ctx, db_proxy_name=db_proxy["resource_id"]
        )
        if not ret or not ret["result"]:
            hub.log.warning(
                f"Could not describe aws.rds.db_proxy_target {ret['comment']}"
            )
            return result
        for resource in ret["ret"]:
            resource_id = resource.get("resource_id")
            result[resource_id] = {
                "aws.rds.db_proxy_target.present": [
                    {parameter_key: parameter_value}
                    for parameter_key, parameter_value in resource.items()
                ]
            }
    return result
