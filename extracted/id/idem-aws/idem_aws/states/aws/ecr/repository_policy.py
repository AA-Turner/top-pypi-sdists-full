"""State module for managing Amazon ECR Repository Policies."""
import copy
from typing import Any
from typing import Dict

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    repository_name: str,
    policy_text: Dict or str,
    resource_id: str = None,
    registry_id: str = None,
    force: bool = False,
) -> Dict[str, Any]:
    """Applies a repository policy to the specified AWS ECR repository to control access permissions.

    Args:
        name(str):
            An Idem name of the resource.
        repository_name(str):
            The name of the ECR repository in Amazon Web Services to receive the policy.
        policy_text(dict or str):
            The JSON repository policy text to apply to the repository.
        resource_id(str, Optional):
            The registry id and repository name with a separator '-'. Format: ``[registry_id]-[repository_name]``.
        registry_id(str, Optional):
            The Amazon Web Services account ID associated with the registry that contains the repository. If you
            do not specify a registry, the default registry is assumed.
        force(bool, Optional):
            If the policy you are attempting to set on a repository policy would prevent you from setting another policy
            in the future, you must force the SetRepositoryPolicy operation. This is intended to prevent accidental repository lock outs.

    Request Syntax:
      .. code-block:: sls

        [idem_test_aws_ecr_repository_policy]:
          aws.ecr.repository_policy.present:
            - name: 'string'
            - repository_name: 'string'
            - policy_text: 'string'
            - registry_id: 'string'
            - force: True|False

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            idem_test_aws_ecr_repository_policy:
              aws.ecr.repository.present:
                - name: idem_test_ecr_policy
                - repository_name: idem_test_ecr_repository
                - policy_text:
                    Version: '2012-10-17'
                    Statement:
                      - Sid: 'DenyPull'
                        Effect: 'Deny'
                        Principal: '*'
                        Action: ['ecr:BatchGetImage', 'ecr:GetDownloadUrlForLayer']
                - registry_id: idem_test_ecr_registry
                - force: True
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    resource_updated = False
    policy_text = hub.tool.aws.state_comparison_utils.standardise_json(policy_text)

    if resource_id:
        if registry_id is None:
            registry_id = resource_id.split("-")[0]

    before_ret = await hub.exec.aws.ecr.repository_policy.get(
        ctx,
        name=repository_name,
        registry_id=registry_id,
        resource_id=repository_name,
    )

    # Case: If there is something found
    if before_ret["result"] and before_ret["ret"]:
        result["comment"] += [f"aws.ecr.repository_policy '{name}' already exists"]
        result["old_state"] = copy.deepcopy(before_ret.get("ret"))
        result["new_state"] = copy.deepcopy(before_ret.get("ret"))

        if policy_text and not hub.tool.aws.state_comparison_utils.are_policies_equal(
            result["old_state"]["policy_text"], policy_text
        ):
            if ctx.get("test", False):
                result["comment"] += [
                    f"Would update policy_text for aws.ecr.repository_policy '{name}'"
                ]
                result["new_state"]["policy_text"] = policy_text
                return result

            update_ret = await hub.exec.boto3.client.ecr.set_repository_policy(
                ctx,
                registryId=registry_id,
                repositoryName=repository_name,
                policyText=policy_text,
                force=force,
            )
            if not update_ret["result"]:
                result["result"] = False
                result["comment"] += update_ret["comment"]
                return result

            result["comment"] += [f"Updated aws.ecr.repository_policy '{name}'"]
            resource_updated = True
    else:
        if ctx.get("test", False):
            result[
                "new_state"
            ] = raw_resource = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "resource_id": f"{registry_id}-{repository_name}",
                    "registry_id": registry_id,
                    "repository_name": repository_name,
                    "policy_text": policy_text,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.ecr.repository_policy", name=name
            )
            return result

        set_policy_ret = await hub.exec.boto3.client.ecr.set_repository_policy(
            ctx,
            registryId=registry_id,
            repositoryName=repository_name,
            policyText=policy_text,
            force=force,
        )
        if not set_policy_ret["result"]:
            result["result"] = False
            result["comment"] = set_policy_ret["comment"]
            return result

        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.ecr.repository_policy", name=name
        )

    # Case: If something got updated or old_state is not present
    if (not result["old_state"]) or resource_updated:
        after_ret = await hub.exec.aws.ecr.repository_policy.get(
            ctx, name=name, registry_id=registry_id, resource_id=repository_name
        )

        if not after_ret["result"]:
            result["result"] = False
            result["comment"] += after_ret["comment"]
            return result

        result["new_state"] = copy.deepcopy(after_ret.get("ret"))

    return result


async def absent(
    hub,
    ctx,
    name: str,
    repository_name: str = None,
    resource_id: str = None,
    registry_id: str = None,
) -> Dict[str, Any]:
    """Deletes the policy associated with the specified AWS ECR repository.

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
            The Amazon Web Services account ID associated with the registry that contains the repository policy to
            delete. If you do not specify a registry, the default registry is assumed.

    Request syntax:
      .. code-block:: sls

        [idem_test_aws_ecr_repository_policy]:
          aws.ecr.repository_policy.absent:
            - name: 'string'
            - repository_name: 'string'
            - resource_id: 'string'
            - registry_id: 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            idem_test_aws_ecr_repository_policy:
              aws.ecr.repository_policy.absent:
                - name: idem_test_ecr_policy
                - repository_name: idem_test_ecr_repository
                - resource_id: idem_test_ecr_registry-idem_test_ecr_repository
                - registry_id: idem_test_ecr_registry
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.ecr.repository_policy", name=name
        )
        return result
    else:
        if registry_id is None:
            registry_id = resource_id.split("-")[0]

    before_ret = await hub.exec.aws.ecr.repository_policy.get(
        ctx,
        name=name,
        registry_id=registry_id,
        resource_id=repository_name,
    )

    # Case: Error
    if not before_ret["result"]:
        result["result"] = False
        result["comment"] = before_ret["comment"]
        return result

    # Any case forward, the old_state should carry current state in old_state
    result["old_state"] = copy.deepcopy(before_ret["ret"])

    if not before_ret["ret"]:
        # Case: already absent
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.ecr.repository_policy", name=name
        )
        return result
    elif ctx.get("test", False):
        # Case: --test context
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.ecr.repository_policy", name=name
        )
        return result

    delete_ret = await hub.exec.boto3.client.ecr.delete_repository_policy(
        ctx, registryId=registry_id, repositoryName=repository_name
    )

    # Case: Failed to delete
    if not delete_ret["result"]:
        result["result"] = False
        result["comment"] = delete_ret["comment"]
        return result

    # Case: All good, add deleted comment
    result["comment"] = hub.tool.aws.comment_utils.delete_comment(
        resource_type="aws.ecr.repository_policy", name=name
    )

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describes policies for AWS ECR repositories in a registry in a way that can be recreated/managed with the corresponding "present" function.

    Returns:
        Dict[str, Dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe aws.ecr.repository_policy
    """
    result = {}

    # To describe all the repository policies, we first need to list all the repositories,
    # and then we get the policy associated to each repository
    describe_ret = await hub.exec.aws.ecr.repository.list(ctx)
    if not describe_ret["result"]:
        hub.log.warning(f"Could not describe repositories: {describe_ret['comment']}")
        return result

    for repository in describe_ret["ret"]:
        registry_id = repository.get("registry_id")
        repository_name = repository.get("name")

        get_policy_ret = await hub.exec.aws.ecr.repository_policy.get(
            ctx,
            name=repository_name,
            registry_id=registry_id,
            resource_id=repository_name,
        )

        # Case: failure to get a policy
        if not get_policy_ret["result"]:
            hub.log.warning(
                f"Could not get policy for repository '{registry_id}/{repository_name}': "
                f"{get_policy_ret['comment']}. Describe will skip this repository and continue."
            )
            continue

        # Case: There is no policy for the repository
        if not get_policy_ret.get("ret"):
            hub.log.debug(
                f"No policy for repository '{registry_id}/{repository_name}' exists: "
                f"{get_policy_ret['comment']}. Describe will skip this repository and continue."
            )
            continue

        resource = get_policy_ret.get("ret")
        result[resource.get("name")] = {
            "aws.ecr.repository_policy.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource.items()
            ]
        }

    return result
