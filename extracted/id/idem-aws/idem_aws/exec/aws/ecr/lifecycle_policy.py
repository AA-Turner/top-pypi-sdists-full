"""Exec module for managing Amazon EC2 Container Registry (ECR) Lifecycle Policies."""
from typing import Any
from typing import Dict

__func_alias__ = {"list_": "list"}


async def get(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    registry_id: str = None,
    repository_name: str = None,
) -> Dict[str, Any]:
    """Retrieves a Amazon EC2 Container Registry (ECR) Lifecycle Policy created on a repository in a registry.

    Args:
        name(str):
            An Idem name of the resource.

        resource_id(str, Optional):
            The name of the ECR repository in Amazon Web Services. If resource_id is not None, it takes precedence
            in get API call.

        registry_id(str, Optional):
            The Amazon Web Services account ID associated with the registry that contains the repository
            to search. If you do not specify a registry, the default registry is assumed.

        repository_name(str):
            The name of the repository to receive the policy.

    Returns:
        Dict[str, Any]:
            Return image repository in a given registry.

    Examples:
        Calling this exec module function from the cli:

        .. code-block:: bash

            idem exec aws.ecr.lifecycle_policy.get name='idem_name' resource_id='ecr_lifecycle_policy'

        Calling this exec module function from within a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.ecr.lifecycle_policy.get
                - kwargs:
                    name: 'idem_name'
                    resource_id: 'ecr_lifecycle_policy'
    """
    result = dict(comment=[], ret=None, result=True)

    if resource_id:
        if registry_id is None:
            registry_id = resource_id.split("-")[0]

        if repository_name is None:
            repository_name = resource_id.split("-")[1]

    describe_ret = await hub.exec.boto3.client.ecr.get_lifecycle_policy(
        ctx=ctx, registryId=registry_id, repositoryName=repository_name
    )

    if not describe_ret["result"]:
        # Do not return success=false when it is not found.
        if "RepositoryNotFoundException" in str(
            describe_ret["comment"]
        ) or "LifecyclePolicyNotFoundException" in str(describe_ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.ecr.lifecycle_policy", name=resource_id
                )
            )
            result["comment"] += list(describe_ret["comment"])
            return result

        result["comment"] += list(describe_ret["comment"])
        result["result"] = False
        return result

    if not describe_ret["ret"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.ecr.lifecycle_policy", name=resource_id
            )
        )
        return result

    result[
        "ret"
    ] = hub.tool.aws.ecr.conversion_utils.convert_raw_lifecycle_policy_to_present(
        raw_resource=describe_ret.get("ret"),
        idem_resource_name=name,
    )
    return result
