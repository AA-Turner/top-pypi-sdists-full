""" State module for managing Elastic Container Registry (Amazon ECR) Lifecycle Policy. """
import copy
from typing import Any
from typing import Dict

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    repository_name: str,
    lifecycle_policy_text: Dict or str,
    resource_id: str = None,
    registry_id: str = None,
) -> Dict[str, Any]:
    """Creates or updates the lifecycle policy for the specified repository. For more information, see Lifecycle policy
    template.

    Args:
        name(str):
            An Idem name of the resource.

        resource_id(str, Optional):
            An identifier of the resource in the provider. Defaults to None.

        registry_id(str, Optional):
            The Amazon Web Services account ID associated with the registry that contains the repository. If you do not
            specify a registry, the default registry is assumed. Defaults to None.

        repository_name(str):
            The name of the repository to receive the policy.

        lifecycle_policy_text(dict or str):
            The JSON repository policy text to apply to the repository.

    Request Syntax:
        .. code-block:: sls

            [stream-name]:
              aws.ecr.lifecycle_policy.present:
                - name: "string"
                - repository_name: "string"
                - resource_id: "string"
                - registry_id: "string"
                - lifecycle_policy_text: "string"

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_present:
              aws.ecr.lifecycle_policy.present:
                - name: idem_test_lifecycle_policy
                - repository_name: idem_test_ecr_repository
                - lifecycle_policy_text: value
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    plan_state = {}
    before = None
    resource_updated = False
    lifecycle_policy_text = hub.tool.aws.state_comparison_utils.standardise_json(
        lifecycle_policy_text
    )

    if resource_id:
        if registry_id is None:
            registry_id = resource_id.split("-")[0]

        before = await hub.exec.aws.ecr.lifecycle_policy.get(
            ctx,
            name=name,
            resource_id=resource_id,
            registry_id=registry_id,
            repository_name=repository_name,
        )
        if not before["result"] or not before["ret"]:
            result["result"] = False
            result["comment"] += before["comment"]
            return result

        result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
            resource_type="aws.ecr.lifecycle_policy", name=name
        )
        result["old_state"] = copy.deepcopy(before["ret"])
        plan_state = copy.deepcopy(result["old_state"])
        result["new_state"] = copy.deepcopy(before["ret"])

        if (
            lifecycle_policy_text
            and not hub.tool.aws.state_comparison_utils.are_policies_equal(
                result["old_state"]["lifecycle_policy_text"], lifecycle_policy_text
            )
        ):
            if ctx.get("test", False):
                result["comment"] += hub.tool.aws.comment_utils.would_update_comment(
                    resource_type="aws.ecr.lifecycle_policy", name=name
                )
                result["new_state"]["lifecycle_policy_text"] = lifecycle_policy_text
                return result

            update_return = await hub.exec.boto3.client.ecr.put_lifecycle_policy(
                ctx=ctx,
                registryId=registry_id,
                repositoryName=repository_name,
                lifecyclePolicyText=lifecycle_policy_text,
            )
            result["comment"] += update_return["comment"]
            if not update_return["result"]:
                result["result"] = False
                return result
            resource_updated = bool(update_return["ret"])
            if resource_updated:
                result["comment"] += hub.tool.aws.comment_utils.update_comment(
                    resource_type="aws.ecr.lifecycle_policy", name=name
                )
    else:
        if ctx.get("test", False):
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "repository_name": repository_name,
                    "lifecycle_policy_text": lifecycle_policy_text,
                    "registry_id": registry_id,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.ecr.lifecycle_policy", name=name
            )
            return result
        ret = await hub.exec.boto3.client.ecr.put_lifecycle_policy(
            ctx,
            registryId=registry_id,
            repositoryName=repository_name,
            lifecyclePolicyText=lifecycle_policy_text,
        )
        if not ret["result"] and not ret["ret"]:
            result["comment"] = ret["comment"]
            result["result"] = False
            return result
        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.ecr.lifecycle_policy", name=name
        )

    if ctx.get("test", False):
        result["new_state"] = plan_state
    elif (not result["old_state"]) or resource_updated:
        after = await hub.exec.aws.ecr.lifecycle_policy.get(
            ctx,
            name=name,
            resource_id=resource_id,
            registry_id=registry_id,
            repository_name=repository_name,
        )
        if not after["result"] or not after["ret"]:
            result["result"] = False
            result["comment"] += after["comment"]
            return result
        result["new_state"] = copy.deepcopy(after["ret"])
    else:
        result["new_state"] = copy.deepcopy(result["old_state"])
    return result


async def absent(
    hub,
    ctx,
    name: str,
    repository_name: str = None,
    resource_id: str = None,
    registry_id: str = None,
) -> Dict[str, Any]:
    """Deletes the lifecycle policy associated with the specified repository.

    Args:
        name(str):
            An Idem name of the resource.

        repository_name(str, Optional):
            The name of the ECR repository in Amazon Web Services that contains the policy to delete.

        resource_id(str, Optional):
            The registry id and repository name with a separator '-'. Format: ``[registry_id]-[repository_name]``.

            .. warning::
              Idem automatically considers this resource being absent if this field is not specified.

        registry_id(str, Optional):
            The Amazon Web Services account ID associated with the registry that contains the repository. If you do not
            specify a registry, the default registry is assumed. Defaults to None.

    Request Syntax:
      .. code-block:: sls

           [lifecycle_policy-name]:
              aws.ecr.lifecycle_policy.absent:
                - name: 'string'
                - repository_name: 'string'
                - resource_id: 'string'
                - registry_id: 'string'

    Returns:
      Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_absent:
              aws.ecr.lifecycle_policy.absent:
                - name: idem_test_policy
                - repository_name: idem_test_repository
                - resource_id: idem_test_ecr_registry-idem_test_ecr_repository
                - registry_id: idem_test_registry
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.ecr.lifecycle_policy", name=name
        )
        return result
    else:
        if registry_id is None:
            registry_id = resource_id.split("-")[0]
            repository_name = resource_id.split("-")[1]

    before = await hub.exec.aws.ecr.lifecycle_policy.get(
        ctx,
        name=name,
        resource_id=resource_id,
        registry_id=registry_id,
        repository_name=repository_name,
    )
    if not before["result"]:
        result["comment"] = before["comment"]
        result["result"] = False
        return result

    if not before["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.ecr.lifecycle_policy", name=name
        )
    else:
        result["old_state"] = before["ret"]
        if ctx.get("test", False):
            result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
                resource_type="aws.ecr.lifecycle_policy", name=name
            )
            return result
        else:
            ret = await hub.exec.boto3.client.ecr.delete_lifecycle_policy(
                ctx,
                registryId=registry_id,
                repositoryName=repository_name,
            )
            if not ret["result"]:
                result["comment"] = before["comment"]
                result["result"] = False
                return result
            result["comment"] = hub.tool.aws.comment_utils.delete_comment(
                resource_type="aws.ecr.lifecycle_policy", name=name
            )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Pass required params to get an Amazon Elastic Container Registry (Amazon ECR) Lifecycle Policy resource.

    Describe the resource in a way that can be recreated/managed with the corresponding "present" function.
    To describe all the repository policies, we first need to list all the repositories, and then we get the policy
    associated to each repository

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.ecr.lifecycle_policy
    """
    result = {}
    describe_ret = await hub.exec.aws.ecr.repository.list(ctx)
    if not describe_ret["result"]:
        hub.log.warning(f"Could not describe repositories: {describe_ret['comment']}")
        return result

    for repository in describe_ret["ret"]:
        registry_id = repository.get("registry_id")
        repository_name = repository.get("name")

        policy_ret = await hub.exec.aws.ecr.lifecycle_policy.get(
            ctx,
            name=repository_name,
            resource_id=(f"{registry_id}-{repository_name}"),
            registry_id=registry_id,
            repository_name=repository_name,
        )

        if not policy_ret["result"]:
            hub.log.warning(
                f"Could not get lifecycle policy for repository '{registry_id}/{repository_name}': "
                f"{policy_ret['comment']}. Describe will skip this lifecycle policy and continue."
            )
            continue

        if not policy_ret.get("ret"):
            hub.log.debug(
                f"No lifecycle policy for repository '{registry_id}/{repository_name}' exists: "
                f"{policy_ret['comment']}. Describe will skip this lifecycle policy and continue."
            )
            continue

        resource = policy_ret.get("ret")
        result[resource.get("resource_id")] = {
            "aws.ecr.lifecycle_policy.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource.items()
            ]
        }
    return result
