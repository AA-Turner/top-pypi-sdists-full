"""States module for managing EC2 VPC Endpoint Service Permissions."""
import copy
from typing import Any
from typing import Dict

from dict_tools import differ

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    service_id: str,
    principal_arn: str,
    resource_id: str = None,
) -> Dict[str, Any]:
    """
    Modifies the permissions for your VPC endpoint service. You can add or remove permissions for service consumers
    (Amazon Web Services accounts, users, and IAM roles) to connect to your endpoint service.

    If you grant permissions to all principals, the service is public. Any users who know the name of a public service can send a
    request to attach an endpoint. If the service does not require manual approval, attachments are automatically
    approved.

    Args:
        name(str): Idem name of the resource.

        service_id(str): The ID of the service.

        principal_arn(str, Optional): The Amazon Resource Name (ARN) of the principal. To grant permissions to all principals, specify an asterisk (*).

        resource_id(str): The ID of the service permission. Defaults to None.

    Returns:
        Dict[str, Any]

    Example:
        .. code-block:: sls

          my-vpc-endpoint-service-permission:
            aws.ec2.vpc_endpoint_service_permission.present:
              - service_id: value
              - principal_arn: value
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
        before = await hub.exec.aws.ec2.vpc_endpoint_service_permission.get(
            ctx, name=name, service_id=service_id, principal_arn=principal_arn
        )

        if not before["result"] or not before["ret"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result

        result["old_state"] = current_state = copy.deepcopy(before["ret"])
        result["comment"].append(
            f"'aws.ec2.vpc_endpoint_service_permission: {name}' already exists"
        )

    if current_state:
        # If provided principal is not in current set of principals, add it
        needs_update = (
            "principal_arn" in current_state
            and current_state["principal_arn"] != principal_arn
        )

        if needs_update:
            if ctx.test:
                result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                    enforced_state={}, desired_state=desired_state
                )
                result["comment"].append(
                    f"Would update aws.ec2.vpc_endpoint_service_permission '{name}'"
                )
                return result
            else:
                update_ret = await hub.exec.aws.ec2.vpc_endpoint_service_permission.update(
                    ctx,
                    **{
                        "service_id": service_id,
                        # requested becomes new principal to add
                        "add_allowed_principals": [principal_arn],
                        # current becomes principal to be removed
                        "remove_allowed_principals": [current_state["principal_arn"]],
                    },
                )
                result["result"] = update_ret["result"]

                if result["result"]:
                    result["comment"].append(
                        f"Updated aws.ec2.vpc_endpoint_service_permission '{name}'"
                    )
                else:
                    result["comment"].append(update_ret["comment"])
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={}, desired_state=desired_state
            )
            result["comment"].append(
                f"Would create aws.ec2.vpc_endpoint_service_permission '{name}'"
            )
            return result

        create_ret = await hub.exec.aws.ec2.vpc_endpoint_service_permission.create(
            ctx, **{"service_id": service_id, "add_allowed_principals": [principal_arn]}
        )
        result["result"] = create_ret["result"]

        if result["result"]:
            result["comment"] = hub.tool.aws.comment_utils.create_comment(
                resource_type="aws.ec2.vpc_endpoint_service_permission", name=name
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

    after = await hub.exec.aws.ec2.vpc_endpoint_service_permission.get(
        ctx, name=name, service_id=service_id, principal_arn=principal_arn
    )
    result["new_state"] = after.ret
    return result


async def absent(
    hub,
    ctx,
    name: str,
    service_id: str,
    principal_arn: str,
    resource_id: str = None,
) -> Dict[str, Any]:
    """
    Removes the permissions for your VPC endpoint service. You can remove permissions for service consumers
    (Amazon Web Services accounts, users, and IAM roles) to connect to your endpoint service.

    Args:
        name(str): Idem name of the resource.

        service_id(str): The ID of the service.

        principal_arn(str, Optional): The Amazon Resource Name (ARN) of the principal.

        resource_id(str, Optional): The ID of the service permission.

    Returns:
        Dict[str, Any]

    Example:
        .. code-block:: sls

            my-vpc-endpoint-service-permission:
              aws.ec2.vpc_endpoint_service_permission.absent:
                - service_id: value
                - principal_arn: value
    """

    result = dict(
        comment=[], old_state={}, new_state={}, name=name, result=True, rerun_data=None
    )

    if not resource_id:
        resource_id = (ctx.old_state or {}).get("resource_id")

    # This is to make absent idempotent. If absent is run again, it would be a no-op
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.ec2.vpc_endpoint_service_permission", name=name
        )
        return result

    before = await hub.exec.aws.ec2.vpc_endpoint_service_permission.get(
        ctx, name=name, service_id=service_id, principal_arn=principal_arn
    )

    # Case: Error
    if not before["result"]:
        result["result"] = False
        result["comment"] = before["comment"]
        return result

    # Case: Not Found
    if not before["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.ec2.vpc_endpoint_service_permission", name=name
        )
        return result

    result["old_state"] = before["ret"]

    if ctx.get("test", False):
        result["comment"].append(
            f"Would delete aws.ec2.vpc_endpoint_service_permission '{name}'",
        )
        return result

    delete_ret = await hub.exec.aws.ec2.vpc_endpoint_service_permission.delete(
        ctx, name=name, service_id=service_id, remove_allowed_principals=[principal_arn]
    )

    result["result"] = delete_ret["result"]

    if not result["result"]:
        # If there is any failure in delete, it should reconcile.
        # The type of data is less important here to use default reconciliation
        # If there are no changes for 3 runs with rerun_data, then it will come out of execution
        result["rerun_data"] = resource_id
        result["comment"].append(delete_ret["result"])

    result["comment"] = hub.tool.aws.comment_utils.delete_comment(
        resource_type="aws.ec2.vpc_endpoint_service_permission", name=name
    )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """
    Describes the principals (service consumers) that are permitted to discover your VPC endpoint service.

    Returns:
        Dict[str, Any]

    Example:

        .. code-block:: bash

            $ idem describe aws.ec2.vpc_endpoint_service_permission
    """

    result = {}

    services_ret = await hub.exec.aws.ec2.vpc_endpoint_service_configuration.list(ctx)

    if not services_ret or not services_ret["result"]:
        hub.log.warning(
            f"Could not describe aws.ec2.vpc_endpoint_service_configuration {services_ret['comment']}"
        )
        return result

    for service_resource in services_ret["ret"]:
        service_id = service_resource.get("resource_id")

        ret = await hub.exec.aws.ec2.vpc_endpoint_service_permission.list(
            ctx, service_id
        )

        if not ret or not ret["result"]:
            hub.log.warning(
                f"Could not describe aws.ec2.vpc_endpoint_service_permission {ret['comment']}"
            )

        for service_permission_resource in ret["ret"]:
            resource_id = service_permission_resource.get("resource_id")
            result[resource_id] = {
                "aws.ec2.vpc_endpoint_service_permission.present": [
                    {parameter_key: parameter_value}
                    for parameter_key, parameter_value in service_permission_resource.items()
                ]
            }

    return result
