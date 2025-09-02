"""State module for managing IAM Service linked role."""
import copy
import re
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]

delete_waiter_acceptors = [
    {
        "matcher": "error",
        "expected": "NoSuchEntity",
        "state": "retry",
        "argument": "Error.Code",
    },
    {
        "matcher": "path",
        "expected": "SUCCEEDED",
        "state": "success",
        "argument": "Status",
    },
    {
        "matcher": "path",
        "expected": "FAILED",
        "state": "success",
        "argument": "Status",
    },
    {
        "matcher": "path",
        "expected": "IN_PROGRESS",
        "state": "retry",
        "argument": "Status",
    },
    {
        "matcher": "path",
        "expected": "NOT_STARTED",
        "state": "retry",
        "argument": "Status",
    },
]


async def present(
    hub,
    ctx,
    name: str,
    service_name: str,
    custom_suffix: str = None,
    resource_id: str = None,
    description: str = None,
    tags: Dict[str, Any]
    or List[
        make_dataclass(
            "Tag",
            [("Key", str, field(default=None)), ("Value", str, field(default=None))],
        )
    ] = None,
) -> Dict[str, Any]:
    """Creates an IAM role that is linked to a specific Amazon Web Services service.

    The service controls the attached policies and when the role can be deleted. This helps ensure that the service is
    not broken by an unexpectedly changed or deleted role, which could put your Amazon Web Services resources into an
    unknown state.

    Note:
        1. Updates to role name, custom suffix and description are not allowed by AWS. Only tags can be updated.
        2. All service linked roles does not support custom suffix

    Args:
        name(str):
            The name of the idem resource.

        service_name(str):
            The service principal for the Amazon Web Services service to which this role is attached.
            for example: elasticbeanstalk.amazonaws.com

        custom_suffix(str, Optional):
            A string that you provide, which is combined with the service-provided prefix to form the complete service
            linked role name

        resource_id(str, Optional):
            AWS IAM Role Name.

        description(str, Optional):
            A description of the service linked role. Defaults to None.

        tags(dict or list, Optional):
            Dict in the format of ``{tag-key: tag-value}`` or List of tags in the format of
            ``[{"Key": tag-key, "Value": tag-value}]`` to associate with the new service linked role. Each tag consists
            of a key name and an associated value. Defaults to None.

            * Key (str):
                The key name that can be used to look up or retrieve the associated value. For example,
                Department or Cost Center are common choices.

            * Value (str):
                The value associated with this tag. For example, tags with a key name of Department could have
                values such as Human Resources, Accounting, and Support. Tags with a key name of Cost Center
                might have values that consist of the number associated with the different cost centers in your
                company. Typically, many resources have tags with the same key name but with different values.
                Amazon Web Services always interprets the tag Value as a single string. If you need to store an
                array, you can store comma-separated values in the string. However, you must interpret the value
                in your code.

    Request Syntax:
        .. code-block:: sls

            [iam-service-linked-role-name]:
              aws.iam.service_linked_role.present:
                - name: 'string'
                - service_name: 'string'
                - custom_suffix: 'string'
                - resource_id: 'string'
                - description: 'string'
                - tags:
                  - Key: 'string'
                    Value: 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            AWSServiceRoleForAutoScaling:
              aws.iam.service_linked_role.present:
                - name: AWSServiceRoleForAutoScaling
                - resource_id: AWSServiceRoleForAutoScaling
                - service_name: autoscaling.amazonaws.com
                - custom_suffix: test_suffix
                - description: This is custom description
                - tags:
                  - Key: firstkey
                    Value: firstvalue
                  - Key: 2ndkey
                    Value: 2ndvalue
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    before = None
    resource_tag_updated = False
    resource_description_updated = False
    resource = await hub.tool.boto3.resource.create(
        ctx, "iam", "Role", resource_id if resource_id else name
    )
    before = await hub.tool.boto3.resource.describe(resource)
    if isinstance(tags, List):
        tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags)
    if before:
        result[
            "old_state"
        ] = hub.tool.aws.iam.service_linked_role.convert_raw_service_linked_role_to_present(
            before
        )

        resource_description_updated = description != result["old_state"].get(
            "description"
        )
        resource_tag_updated = tags != result["old_state"].get("tags")
        result["new_state"] = copy.deepcopy(result["old_state"])
        if not resource_tag_updated and not resource_description_updated:
            result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
                resource_type="aws.iam.service_linked_role", name=name
            )
            return result
        else:
            if resource_tag_updated:
                update_ret = await hub.exec.aws.iam.role.update_role_tags(
                    ctx,
                    role_name=resource_id,
                    old_tags=result["old_state"].get("tags"),
                    new_tags=tags,
                )
                result["result"] = update_ret["result"]
                result["new_state"]["tags"] = tags
                result["comment"] += update_ret["comment"]
            if resource_description_updated:
                update_ret = await hub.exec.aws.iam.role.update_role(
                    ctx, old_state=result["old_state"], description=description
                )
                result["result"] = update_ret["result"]
                result["new_state"]["description"] = description
                result["comment"] += update_ret["comment"]
            return result

    if ctx.get("test", False):
        result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
            enforced_state={},
            desired_state={
                "name": name,
                "service_name": service_name,
                "custom_suffix": custom_suffix,
                "description": description,
                "resource_id": resource_id if resource_id else name,
                "tags": tags,
                "arn": "arn_known_after_present",
            },
        )
        operation = (
            "update"
            if before and (resource_tag_updated or resource_description_updated)
            else "create"
        )
        result["comment"] += [f"Would {operation} aws.iam.service_linked_role '{name}'"]
        return result
    else:
        create_role_ret = await hub.exec.boto3.client.iam.create_service_linked_role(
            ctx=ctx,
            AWSServiceName=service_name,
            Description=description,
            CustomSuffix=custom_suffix,
        )
        if not create_role_ret["result"]:
            result["comment"] = create_role_ret["comment"]
            result["result"] = False
            return result
        role_name = create_role_ret["ret"]["Role"].get("RoleName")
        if tags:
            add_tag_ret = await hub.exec.boto3.client.iam.tag_role(
                ctx,
                RoleName=role_name,
                Tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags),
            )
            if not add_tag_ret["result"]:
                result["comment"] = add_tag_ret["comment"]
                result["result"] = False
                return result

        created_resource = await hub.tool.boto3.resource.create(
            ctx, "iam", "Role", role_name
        )
        after_ret = await hub.tool.boto3.resource.describe(created_resource)
        result[
            "new_state"
        ] = hub.tool.aws.iam.service_linked_role.convert_raw_service_linked_role_to_present(
            after_ret
        )
        if not before:
            result["comment"] = hub.tool.aws.comment_utils.create_comment(
                resource_type="aws.iam.service_linked_role", name=name
            )
    return result


async def absent(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    timeout: Dict = None,
) -> Dict[str, Any]:
    """Submits a service-linked role deletion request and returns a DeletionTaskId , which can be used to check the
    status of the deletion.

    Args:
        name(str):
            AWS IAM service linked Role Name.

        resource_id(str, Optional):
            AWS IAM service linked Role Name. If not specified, Idem will use "name" parameter to identify the IAM service
            linked role on AWS.

        timeout(Dict, Optional):
            Timeout configuration for deletion of AWS service linked role.
            * delete (dict):
                Timeout configuration for deletion of a Nat Gateway
                * delay: The amount of time in seconds to wait between attempts.
                * max_attempts: Customized timeout configuration containing delay and max attempts.


    Request Syntax:
        .. code-block:: sls

            [service_linked_role-resource-id]:
              aws.iam.service_linked_role.absent:
                - name: "string"
                - resource_id: "string"

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_absent:
              aws.iam.service_linked_role.absent:
                - resource_id: AWSServiceRoleForAutoScaling
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    resource_id = resource_id if resource_id else name
    resource = await hub.tool.boto3.resource.create(ctx, "iam", "Role", resource_id)
    before = await hub.tool.boto3.resource.describe(resource)

    if not before:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.iam.service_linked_role", name=name
        )
    elif ctx.get("test", False):
        result[
            "old_state"
        ] = hub.tool.aws.iam.service_linked_role.convert_raw_service_linked_role_to_present(
            before
        )
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.iam.service_linked_role", name=name
        )
        return result
    else:
        try:
            result[
                "old_state"
            ] = hub.tool.aws.iam.service_linked_role.convert_raw_service_linked_role_to_present(
                before
            )

            ret = await hub.exec.boto3.client.iam.delete_service_linked_role(
                ctx=ctx, RoleName=resource_id
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = ret["comment"]
                return result
            deletionTaskId = ret["ret"].get("DeletionTaskId")
            # Custom waiter for delete
            # TODO - Use Reconciliation Loop
            waiter_config = hub.tool.aws.waiter_utils.create_waiter_config(
                default_delay=15,
                default_max_attempts=40,
                timeout_config=timeout.get("delete") if timeout else None,
            )
            cluster_waiter = hub.tool.boto3.custom_waiter.waiter_wrapper(
                name="ServiceLinkedRoleDelete",
                operation="GetServiceLinkedRoleDeletionStatus",
                argument=["Status", "Error.Code"],
                acceptors=delete_waiter_acceptors,
                client=await hub.tool.boto3.client.get_client(ctx, "iam"),
            )
            await hub.tool.boto3.client.wait(
                ctx,
                "iam",
                "ServiceLinkedRoleDelete",
                cluster_waiter,
                DeletionTaskId=deletionTaskId,
                WaiterConfig=waiter_config,
            )
            deletion_status_ret = (
                await hub.exec.boto3.client.iam.get_service_linked_role_deletion_status(
                    ctx=ctx, DeletionTaskId=deletionTaskId
                )
            )
            if deletion_status_ret["result"]:
                deletion_status = deletion_status_ret["ret"]["Status"]
                if deletion_status == "FAILED":
                    result["result"] = False
                    result["comment"] += [
                        deletion_status_ret["ret"]["Reason"].get("Reason")
                    ]
                    return result
                elif deletion_status == "SUCCEEDED":
                    result["comment"] = hub.tool.aws.comment_utils.delete_comment(
                        resource_type="aws.iam.service_linked_role", name=name
                    )
            else:
                result["result"] = False
                result["comment"] += deletion_status_ret["comment"]
                return result
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function

    Lists the IAM service linked roles. If there are none, the operation returns an empty list.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.iam.service_linked_role
    """
    result = {}
    ret = await hub.exec.boto3.client.iam.list_roles(ctx)

    if not ret["result"]:
        hub.log.warning(f"Could not describe service_linked_role {ret['comment']}")
        return {}

    for role in ret["ret"]["Roles"]:
        # By default list_roles provides all role
        # Service linked roles have path something like 'Path': '/aws-service-role/autoscaling.amazonaws.com/'
        # and other all roles have path as "/"
        if not re.search("/aws-service-role/*", str(role)):
            continue
        resource = await hub.tool.boto3.resource.create(
            ctx, "iam", "Role", role.get("RoleName")
        )
        resource = await hub.tool.boto3.resource.describe(resource)
        translated_resource = hub.tool.aws.iam.service_linked_role.convert_raw_service_linked_role_to_present(
            resource
        )
        resource_key = f"iam-service_linked_role-{translated_resource['resource_id']}"
        result[resource_key] = {
            "aws.iam.service_linked_role.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in translated_resource.items()
            ]
        }
    return result
