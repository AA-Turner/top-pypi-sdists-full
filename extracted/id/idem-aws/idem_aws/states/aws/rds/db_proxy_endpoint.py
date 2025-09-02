"""States module for managing Rds Db Proxy Endpoints."""
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
    db_proxy_endpoint_name: str,
    vpc_subnet_ids: List[str],
    vpc_security_group_ids: List[str] = None,
    target_role: str = "READ_WRITE",
    tags: Dict[str, str] = None,
    resource_id: str = None,
    timeout: make_dataclass(
        """Timeout configuration.""" "Timeout",
        [
            (
                "create",
                make_dataclass(
                    "CreateTimeout",
                    [
                        ("delay", int, field(default=None)),
                        ("max_attempts", int, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
            (
                "update",
                make_dataclass(
                    "UpdateTimeout",
                    [
                        ("delay", int, field(default=None)),
                        ("max_attempts", int, field(default=None)),
                    ],
                ),
                field(default=None),
            ),
        ],
    ) = None,
) -> Dict[str, Any]:
    """
    Creates a DBProxyEndpoint. Only applies to proxies that are associated with Aurora DB clusters. You can use DB
    proxy endpoints to specify read/write or read-only access to the DB cluster. You can also use DB proxy endpoints
    to access a DB proxy through a different VPC than the proxy's default VPC.

    Args:
        db_proxy_name(str): The name of the DB proxy associated with the DB proxy endpoint that you create.

        db_proxy_endpoint_name(str): The name of the DB proxy endpoint to create.

        vpc_subnet_ids(List[str]): The VPC subnet IDs for the DB proxy endpoint that you create. You can specify a different set of
            subnet IDs than for the original DB proxy.

        name(str): Idem name of the resource.

        vpc_security_group_ids(List[str], Optional): The VPC security group IDs for the DB proxy endpoint that you create. You can specify a
            different set of security group IDs than for the original DB proxy. The default is the default
            security group for the VPC. Defaults to None.

        target_role(str, Optional): A value that indicates whether the DB proxy endpoint can be used for read/write or read-only
            operations. The default is READ_WRITE. The only role that proxies for RDS for Microsoft SQL
            Server support is READ_WRITE. Defaults to READ_WRITE.

        tags(Dict[str, str], Optional): The tags to apply to the resource.

        resource_id(str, Optional): Db_proxy_endpoint unique ID. Defaults to None.

        timeout(dict, Optional):
            Timeout configuration for create/update of AWS DB Cluster.

            * create (*dict, Optional*):
                Timeout configuration for creating DB Cluster.

                * delay(*int, Optional*):
                    The amount of time in seconds to wait between attempts.

                * max_attempts(*int, Optional*):
                    Customized timeout configuration containing delay and max attempts.

            * update(*dict, Optional*):
                Timeout configuration for updating DB Cluster

                * delay(*int, Optional*):
                    The amount of time in seconds to wait between attempts.

                * max_attempts(*int, Optional*):
                    Customized timeout configuration containing delay and max attempts.

    Returns:
        Dict[str, Any]

    Example:
        .. code-block:: sls


          idem_test_aws_auto.rds.db_proxy_endpoint_is_present:
              aws_auto.aws_auto.rds.db_proxy_endpoint.present:
              - db_proxy_name: string
              - db_proxy_endpoint_name: string
              - vpc_subnet_ids:
                - value
              - vpc_security_group_ids:
                - value
              - target_role: string
              - tags:
                  key: value


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

    if isinstance(tags, List):
        tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags)

    if resource_id:
        before = await hub.exec.aws.rds.db_proxy_endpoint.get(
            ctx, name=name, resource_id=resource_id
        )
        if not before["result"] or not before["ret"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result

        result["old_state"] = current_state = copy.deepcopy(before["ret"])
        result["comment"] += hub.tool.aws.comment_utils.already_exists_comment(
            resource_type="aws.rds.db_proxy_endpoint", name=name
        )

    if current_state:
        # If there are changes in desired state from existing state
        changes = differ.deep_diff(
            current_state if current_state else {}, desired_state
        )
        if bool(changes.get("new")):
            if ctx.test:
                result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                    enforced_state={}, desired_state=desired_state
                )
                result["comment"] += hub.tool.aws.comment_utils.would_update_comment(
                    resource_type="aws.rds.db_proxy_endpoint", name=name
                )
                return result
            else:
                # Update the resource
                update_ret = await hub.exec.aws.rds.db_proxy_endpoint.update(
                    ctx,
                    resource_id=resource_id,
                    tags=tags,
                    new_db_proxy_endpoint_name=db_proxy_endpoint_name,
                    vpc_security_group_ids=vpc_security_group_ids,
                    name=name,
                )
                result["result"] = update_ret["result"]
                if result["result"]:
                    resource_id = update_ret["ret"].get("resource_id", resource_id)
                    result["comment"] += hub.tool.aws.comment_utils.update_comment(
                        resource_type="aws.rds.db_proxy_endpoint", name=name
                    )
                else:
                    result["comment"].append(update_ret["comment"])
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={}, desired_state=desired_state
            )
            result["comment"] += hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.rds.db_proxy_endpoint", name=name
            )
            return result

        create_ret = await hub.exec.aws.rds.db_proxy_endpoint.create(
            ctx,
            **desired_state,
        )
        result["result"] = create_ret["result"]

        if result["result"]:
            result["comment"] = hub.tool.aws.comment_utils.create_comment(
                resource_type="aws.rds.db_proxy_endpoint", name=name
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

    after = await hub.exec.aws.rds.db_proxy_endpoint.get(
        ctx, name=name, resource_id=resource_id
    )
    result["new_state"] = after.ret
    return result


async def absent(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    timeout: make_dataclass(
        """Specifies timeout for deletion of DB Proxy Endpoint.""" "Timeout",
        [
            (
                "delete",
                make_dataclass(
                    "DeleteTimeout",
                    [
                        ("delay", int, field(default=40)),
                        ("max_attempts", int, field(default=60)),
                    ],
                ),
                field(default=None),
            ),
        ],
    ) = None,
) -> Dict[str, Any]:
    """

    Deletes a DBProxyEndpoint. Doing so removes the ability to access the DB proxy using the endpoint that you
    defined. The endpoint that you delete might have provided capabilities such as read/write or read-only
    operations, or using a different VPC than the DB proxy's default VPC.

    Args:
        name(str): Idem name of the resource.

        resource_id(str): The name of the DB proxy endpoint to delete.

        timeout(dict, Optional):
            Timeout configuration for delete of AWS RDS DB Proxy.

            * delete (*dict, Optional*):
                Timeout configuration for deleting DB Cluster.

                * delay(*int, Optional*):
                    The amount of time in seconds to wait between attempts.

                * max_attempts(*int, Optional*):
                    Customized timeout configuration containing delay and max attempts.

    Returns:
        Dict[str, Any]

    Example:
        .. code-block:: sls


            idem_test_aws_auto.rds.db_proxy_endpoint_is_absent:
              aws_auto.aws_auto.rds.db_proxy_endpoint.absent:
              - db_proxy_endpoint_name: string


    """

    result = dict(
        comment=[], old_state={}, new_state={}, name=name, result=True, rerun_data=None
    )

    if not resource_id:
        resource_id = (ctx.old_state or {}).get("resource_id")

    if not resource_id:
        result["comment"] += hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.rds.db_proxy_endpoint", name=name
        )
        return result

    before = await hub.exec.aws.rds.db_proxy_endpoint.get(
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
            resource_type="aws.rds.db_proxy_endpoint", name=name
        )
        return result

    result["old_state"] = before["ret"]

    if ctx.get("test", False):
        result["comment"].append(
            f"Would delete aws.rds.db_proxy_endpoint '{name}'",
        )
        return result

    delete_ret = await hub.exec.aws.rds.db_proxy_endpoint.delete(
        ctx, name=name, resource_id=resource_id, timeout=timeout
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
            resource_type="aws.rds.db_proxy_endpoint", name=name
        )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """
    Describe the resource in a way that can be recreated/managed with the corresponding "present" function

    Returns information about DB proxy endpoints.


    Returns:
        Dict[str, Any]

    Example:

        .. code-block:: bash

            $ idem describe aws_auto.rds.db_proxy_endpoint
    """

    result = {}
    ret = await hub.exec.aws.rds.db_proxy_endpoint.list(ctx)

    if not ret or not ret["result"]:
        hub.log.warning(
            f"Could not describe aws.rds.db_proxy_endpoint {ret['comment']}"
        )
        return result

    for resource in ret["ret"]:
        resource_id = resource.get("resource_id")
        result[resource_id] = {
            "aws.rds.db_proxy_endpoint.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource.items()
            ]
        }
    return result
