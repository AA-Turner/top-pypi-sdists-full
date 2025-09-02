"""Exec module for managing Amazon ECR repository policies."""
from typing import Any
from typing import Dict


async def get(
    hub, ctx, name: str, resource_id: str, registry_id: str = None
) -> Dict[str, Any]:
    """Retrieves the repository policy for the specified repository.

    Args:
        name(str):
            An Idem name of the resource.
        resource_id(str):
            The name of the ECR repository in Amazon Web Services.
        registry_id(str, Optional):
            The Amazon Web Services account ID associated with the registry that contains the repository
            to search. If you do not specify a registry, the default registry is assumed.

    Returns:
        Dict[str, Any]:
            Return the repository policy for the specified repository.

    Examples:
        Calling this exec module function from the cli:

        .. code-block:: bash

            idem exec aws.ecr.repository_policy.get name='idem_name' resource_id='ecr_repository_name'

        Calling this exec module function from within a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.ecr.repository_policy.get
                - kwargs:
                    name: 'idem_name'
                    resource_id: 'ecr_repository_name'
    """
    result = dict(comment=[], ret=None, result=True)

    get_policy_ret = await hub.exec.boto3.client.ecr.get_repository_policy(
        ctx=ctx, registryId=registry_id, repositoryName=resource_id
    )

    # Case: Error
    if not get_policy_ret["result"]:
        # Do not return success=false when it is not found.
        if "RepositoryNotFoundException" in str(
            get_policy_ret["comment"]
        ) or "RepositoryPolicyNotFoundException" in str(get_policy_ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.ecr.repository_policy", name=name
                )
            )
            result["comment"] += list(get_policy_ret["comment"])
            return result

        result["comment"] += list(get_policy_ret["comment"])
        result["result"] = False
        return result

    # Case: Empty results
    if not get_policy_ret["ret"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.ecr.repository_policy", name=resource_id
            )
        )
        return result

    # Case: Result found
    result[
        "ret"
    ] = hub.tool.aws.ecr.conversion_utils.convert_raw_repository_policy_to_present(
        raw_resource=get_policy_ret.get("ret"),
        idem_resource_name=name,
    )

    return result
