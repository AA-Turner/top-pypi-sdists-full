"""States module for managing EC2 VPC Endpoint Service Configurations."""
import copy
from typing import Any
from typing import Dict
from typing import List

from dict_tools import differ

__contracts__ = ["resource", "allow_sync_sls_name_and_name_tag"]


async def present(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    acceptance_required: bool = None,
    private_dns_name: str = None,
    network_load_balancer_arns: List[str] = None,
    gateway_load_balancer_arns: List[str] = None,
    supported_ip_address_types: List[str] = None,
    client_token: str = None,
    tags: Dict[str, str] or List = None,
) -> Dict[str, Any]:
    """
    Creates a VPC endpoint service to which service consumers (Amazon Web Services accounts, users, and IAM roles)
    can connect.

    Before you create an endpoint service, you must create one of the following for your service:

        * A Network Load Balancer. Service consumers connect to your service using an interface endpoint.

        * A Gateway Load Balancer. Service consumers connect to your service using a Gateway Load Balancer endpoint.

    If you set the private DNS name, you must prove that you own the private DNS domain name.
    For more information, see the Amazon Web Services PrivateLink Guide.

    Args:
        name(str, Optional): Idem name of the resource. Defaults to None.

        acceptance_required(bool, Optional): Indicates whether requests from service consumers to create an endpoint to your service must be
            accepted manually. Defaults to None.

        private_dns_name(str, Optional): (Interface endpoint configuration) The private DNS name to assign to the VPC endpoint service. Defaults to None.

        network_load_balancer_arns(List[str], Optional): The Amazon Resource Names (ARNs) of the Network Load Balancers. Defaults to None.

        gateway_load_balancer_arns(List[str], Optional): The Amazon Resource Names (ARNs) of the Gateway Load Balancers. Defaults to None.

        supported_ip_address_types(List[str], Optional): The supported IP address types. The possible values are ipv4 and ipv6. Defaults to None.

        client_token(str, Optional): Unique, case-sensitive identifier that you provide to ensure the idempotency of the request. For
            more information, see How to ensure idempotency. Defaults to None.

        tags (Dict or List, Optional): Dict in the format of {tag-key: tag-value} or List of tags in the format of [{"Key": tag-key, "Value": tag-value}] to associate with the VPC. Each tag consists of a key name and an associated value. Defaults to None.

            * Key (str, Optional): The key of the tag. Constraints: Tag keys are case-sensitive and accept a maximum of 127 Unicode characters. May not begin with aws:.
            * Value(str, Optional): The value of the tag. Constraints: Tag values are case-sensitive and accept a maximum of 256 Unicode characters.

    Returns:
        Dict[str, Any]

    Example:
        .. code-block:: sls

          my-vpc-endpoint-service-configuration:
            aws.ec2.vpc_endpoint_service_configuration.present:
              - acceptance_required: bool
              - private_dns_name: string
              - network_load_balancer_arns:
                - value
              - gateway_load_balancer_arns:
                - value
              - supported_ip_address_types:
                - value
              - client_token: string
              - tags:
                  - Key: string
                    Value: string
    """

    desired_state = {
        k: v
        for k, v in locals().items()
        if k not in ("hub", "ctx", "kwargs") and v is not None
    }

    result = dict(
        comment=[], old_state={}, new_state={}, name=name, result=True, rerun_data=None
    )

    current_state = None

    if isinstance(tags, List):
        tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags)

    if resource_id:
        before = await hub.exec.aws.ec2.vpc_endpoint_service_configuration.get(
            ctx, name=name, resource_id=resource_id
        )
        if not before["result"] or not before["ret"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result

        result["old_state"] = current_state = copy.deepcopy(before["ret"])
        result["comment"].append(
            f"'aws.ec2.vpc_endpoint_service_configuration: {name}' already exists"
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
                result["comment"].append(
                    f"Would update aws.ec2.vpc_endpoint_service_configuration: '{name}'",
                )
                return result
            else:
                # Get new desired state for the vpc_endpoint_service_configuration
                desired_state = hub.tool.aws.ec2.vpc_endpoint_service_configuration.evaluate_update_desired_state(
                    ctx=ctx, current_state=current_state, desired_state=desired_state
                )

                # Update the resource
                update_ret = (
                    await hub.exec.aws.ec2.vpc_endpoint_service_configuration.update(
                        ctx,
                        **desired_state,
                    )
                )

                bool(update_ret["ret"])
                result["result"] = update_ret["result"]

                if result["result"]:
                    result["comment"].append(
                        f"Updated aws.ec2.vpc_endpoint_service_configuration '{name}'"
                    )
                else:
                    result["comment"].append(update_ret["comment"])
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={}, desired_state=desired_state
            )
            result["comment"].append(
                f"Would create aws.ec2.vpc_endpoint_service_configuration '{name}'",
            )
            return result

        create_ret = await hub.exec.aws.ec2.vpc_endpoint_service_configuration.create(
            ctx,
            **desired_state,
        )
        result["result"] = create_ret["result"]

        if result["result"]:
            result["comment"] = hub.tool.aws.comment_utils.create_comment(
                resource_type="aws.ec2.vpc_endpoint_service_configuration",
                name=name,
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

    after = await hub.exec.aws.ec2.vpc_endpoint_service_configuration.get(
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
    Deletes the specified VPC endpoint service configurations. Before you can delete an endpoint service
    configuration, you must reject any Available or PendingAcceptance interface endpoint connections that are
    attached to the service.

    Args:
        name(str): Idem name of the resource.

        resource_id(str, Optional): The ID of the service. Defaults to None.

    Returns:
        Dict[str, Any]

    Example:
        .. code-block:: sls

            my-vpc-endpoint-service-configuration:
                aws.ec2.vpc_endpoint_service_configuration.absent:
                  - name: my-vpc-endpoint-service-configuration
                  - resource_id: value
    """

    result = dict(
        comment=[], old_state={}, new_state={}, name=name, result=True, rerun_data=None
    )

    if not resource_id:
        resource_id = (ctx.old_state or {}).get("resource_id")

    # This is to make absent idempotent. If absent is run again, it would be a no-op
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.ec2.vpc_endpoint_service_configuration", name=name
        )
        return result

    before = await hub.exec.aws.ec2.vpc_endpoint_service_configuration.get(
        ctx, name=name, resource_id=resource_id
    )

    # Case: Error
    if not before["result"]:
        result["result"] = False
        result["comment"] = before["comment"]
        return result

    # Case: Not Found
    if not before["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.ec2.vpc_endpoint_service_configuration", name=name
        )
        return result

    result["old_state"] = before["ret"]

    if ctx.get("test", False):
        result["comment"].append(
            f"Would delete aws.ec2.vpc_endpoint_service_configuration '{name}'",
        )
        return result

    delete_ret = await hub.exec.aws.ec2.vpc_endpoint_service_configuration.delete(
        ctx,
        name=name,
        resource_id=resource_id,
    )

    result["result"] = delete_ret["result"]

    if not result["result"]:
        # If there is any failure in delete, it should reconcile.
        # The type of data is less important here to use default reconciliation
        # If there are no changes for 3 runs with rerun_data, then it will come out of execution
        result["rerun_data"] = resource_id
        result["comment"].append(delete_ret["result"])

    result["comment"] = hub.tool.aws.comment_utils.delete_comment(
        resource_type="aws.ec2.vpc_endpoint_service_configuration", name=name
    )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """
    Describes the VPC endpoint service configurations in your account (your services).

    Returns:
        Dict[str, Any]

    Example:

        .. code-block:: bash

            $ idem describe aws.ec2.vpc_endpoint_service_configuration
    """

    result = {}

    ret = await hub.exec.aws.ec2.vpc_endpoint_service_configuration.list(ctx)

    if not ret or not ret["result"]:
        hub.log.warning(
            f"Could not describe aws.ec2.vpc_endpoint_service_configuration {ret['comment']}"
        )
        return result

    for resource in ret["ret"]:
        resource_id = resource.get("resource_id")
        result[resource_id] = {
            "aws.ec2.vpc_endpoint_service_configuration.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource.items()
            ]
        }
    return result
