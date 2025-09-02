"""State module for managing Amazon Cloudwatchlogs Resource Policy."""
import copy
from typing import Any
from typing import Dict

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    policy_document: str,
    resource_id: str = None,
) -> Dict[str, Any]:
    """Creates or updates a resource policy allowing other Amazon Web Services services to put log events to this account, such as Amazon Route 53.

    An account can have up to 10 resource policies per Amazon Web Services Region.

    Args:
        name(str):
            Name of the new policy. An Idem name of the resource

        policy_document(str): Details
            of the new policy, including the identity of the principal that is enabled to
            put logs to this account. This is formatted as a JSON string. This parameter is required.

        resource_id(str, Optional):
            AWS CloudWatchLogs resource policy name prefix

    Request Syntax:
        .. code-block:: sls

            [log_group_resource_policy_name]:
              aws.cloudwatchlogs.resource_policy.present:
               - name: 'string'
               - policy_document: 'string'
               - resource_id: 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

             resource_policy_is_present:
               aws.cloudwatchlogs.resource_policy.present:
                 - name: policy-tu62879
                 - policy_document: '{ "Version": "2012-10-17", "Statement": [ { "Sid": "Route53LogsToCloudWatchLogs",
                        "Effect": "Allow", "Principal": { "Service": [ "route53.amazonaws.com" ] }, "Action":
                        "logs:PutLogEvents", "Resource": "logArn", "Condition": { "ArnLike": { "aws:SourceArn":
                        "myRoute53ResourceArn" }, "StringEquals": { "aws:SourceAccount": "myAwsAccountId" } } } ] }'
                 - resource_id: policy-tu62879
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    plan_state = {}
    resource_policy_updated = False
    before = await hub.exec.aws.cloudwatchlogs.resource_policy.get(
        ctx, name=resource_id
    )
    if before["result"] and before["ret"]:
        result["comment"] += [f"'{name}' already exists"]
        result[
            "old_state"
        ] = hub.tool.aws.cloudwatchlogs.conversion_utils.convert_raw_log_group_resource_policy_to_present(
            ctx, raw_resource=before["ret"], idem_resource_name=resource_id
        )
        plan_state = copy.deepcopy(result["old_state"])
        if ctx.get("test", False):
            plan_state["policy_document"] = policy_document
        else:
            if policy_document != plan_state["policy_document"]:
                update_ret = await hub.exec.boto3.client.logs.put_resource_policy(
                    ctx, policyName=name, policyDocument=policy_document
                )
                if not update_ret["result"]:
                    result["comment"] += update_ret["comment"]
                    result["result"] = False
                    return result
                resource_policy_updated = True
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "policy_document": policy_document,
                    "resource_id": name,
                },
            )
            result["comment"] += [
                f"Would create aws.cloudwatchlogs.resource_policy '{name}'"
            ]
            return result
        try:
            ret = await hub.exec.boto3.client.logs.put_resource_policy(
                ctx, policyName=name, policyDocument=policy_document
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] += ret["comment"]
                return result
            resource_id = name
            result["comment"] += [
                f"Created aws.cloudwatchlogs.resource_policy '{name}'"
            ]
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]
            result["result"] = False

    if ctx.get("test", False):
        result["new_state"] = plan_state
    elif not (before and before["result"] and before["ret"]) or resource_policy_updated:
        before = await hub.exec.aws.cloudwatchlogs.resource_policy.get(
            ctx, name=resource_id
        )
        result["result"] = result["result"] and before["result"]
        if not result["result"]:
            result["comment"] += before["comment"]
        result[
            "new_state"
        ] = hub.tool.aws.cloudwatchlogs.conversion_utils.convert_raw_log_group_resource_policy_to_present(
            ctx, raw_resource=before["ret"], idem_resource_name=resource_id
        )
    else:
        result["new_state"] = copy.deepcopy(result["old_state"])
    return result


async def absent(hub, ctx, name: str, resource_id: str = None) -> Dict[str, Any]:
    """Deletes a resource policy from this account.

    This revokes the access of the identities in that policy to put log events to this account.

    Args:
        name(str):
            The name of the policy to be revoked. An Idem name of the resource

        resource_id(str, Optional):
            AWS CloudWatchLogs resource policy name prefix

    Request Syntax:
        .. code-block:: sls

            [log_group_resource_policy_name]:
              aws.cloudwatchlogs.resource_policy.absent:
              - name: 'string'
              - resource_id: 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_policy_is_absent:
              aws.cloudwatchlogs.resource_policy.absent:
                - name: policy-tu62879
                - resource_id: policy-tu62879
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    before = await hub.exec.aws.cloudwatchlogs.resource_policy.get(
        ctx, name=resource_id
    )
    if not (before["result"] and before["ret"]):
        result["comment"] += [
            f"aws.cloudwatchlogs.resource_policy '{name}' already absent"
        ]
    else:
        result[
            "old_state"
        ] = hub.tool.aws.cloudwatchlogs.conversion_utils.convert_raw_log_group_resource_policy_to_present(
            ctx, raw_resource=before["ret"], idem_resource_name=resource_id
        )
        if ctx.get("test", False):
            result["comment"] += [
                f"Would delete aws.cloudwatchlogs.resource_policy '{name}'"
            ]
            return result
        else:
            try:
                ret = await hub.exec.boto3.client.logs.delete_resource_policy(
                    ctx, policyName=name
                )
                result["result"] = ret["result"] and result["result"]
                if not result["result"]:
                    result["comment"] += ret["comment"]
                    return result
                result["comment"] += [
                    f"Deleted aws.cloudwatchlogs.resource_policy '{name}'"
                ]
            except hub.tool.boto3.exception.ClientError as e:
                result["comment"] += [f"{e.__class__.__name__}: {e}"]
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Lists the resource policies in this account.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.cloudwatchlogs.resource_policy
    """
    result = {}
    ret = await hub.exec.boto3.client.logs.describe_resource_policies(ctx)
    if not ret["result"]:
        hub.log.warning(
            f"Could not describe CloudWatchLogs Resource Policies {ret['comment']}"
        )
        return {}

    for resource in ret["ret"]["resourcePolicies"]:
        resource_id = resource.get("policyName")
        resource_translated = hub.tool.aws.cloudwatchlogs.conversion_utils.convert_raw_log_group_resource_policy_to_present(
            ctx, raw_resource=resource, idem_resource_name=resource_id
        )
        result[resource_id] = {
            "aws.cloudwatchlogs.resource_policy.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource_translated.items()
            ]
        }
    return result
