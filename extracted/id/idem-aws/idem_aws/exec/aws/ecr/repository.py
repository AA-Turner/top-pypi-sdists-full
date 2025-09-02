"""Exec module for managing Amazon ECR repositories."""
from typing import Any
from typing import Dict
from typing import List

__func_alias__ = {"list_": "list"}


async def get(
    hub, ctx, name: str, resource_id: str, registry_id: str = None
) -> Dict[str, Any]:
    """Retrieves an image repository in a registry.

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
            Return image repository in a given registry.

    Examples:
        Calling this exec module function from the cli:

        .. code-block:: bash

            idem exec aws.ecr.repository.get name='idem_name' resource_id='ecr_repository_name'

        Calling this exec module function from within a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.ecr.repository.get
                - kwargs:
                    name: 'idem_name'
                    resource_id: 'ecr_repository_name'
    """
    result = dict(comment=[], ret=None, result=True)

    describe_ret = await hub.exec.boto3.client.ecr.describe_repositories(
        ctx=ctx, registryId=registry_id, repositoryNames=[resource_id]
    )

    # Case: Error
    if not describe_ret["result"]:
        # Do not return success=false when it is not found.
        if "RepositoryNotFoundException" in str(describe_ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.ecr.repository", name=resource_id
                )
            )
            result["comment"] += list(describe_ret["comment"])
            return result

        result["comment"] += list(describe_ret["comment"])
        result["result"] = False
        return result

    # Case: Empty results
    if not describe_ret["ret"].get("repositories"):
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.ecr.repository", name=resource_id
            )
        )
        return result

    # Case: More than one found
    if len(describe_ret["ret"].get("repositories")) > 1:
        result["comment"].append(
            hub.tool.aws.comment_utils.find_more_than_one(
                resource_type="aws.ecr.repository",
                resource_id=resource_id,
            )
        )

    # Case: One matching record is found (If more than one is found, then taking first)
    repository = describe_ret["ret"].get("repositories")[0]

    tags_results = await hub.tool.aws.ecr.tag.get_resource_tags(
        ctx=ctx, resource_arn=repository.get("repositoryArn")
    )

    result["ret"] = hub.tool.aws.ecr.conversion_utils.convert_raw_repository_to_present(
        raw_resource=repository,
        tags=tags_results.get("ret"),
        idem_resource_name=name,
    )

    return result


async def list_(
    hub, ctx, registry_id: str = None, repository_names: List[str] = None
) -> Dict[str, Any]:
    """Retrieves image repositories in a registry.

    Args:
        registry_id(str, Optional):
            The Amazon Web Services account ID associated with the registry that
            contains  the  repositories to be described. If you do not specify a
            registry, the default registry is assumed.
        repository_names(list[str], Optional):
            A list of repositories to describe.

    Returns:
        Dict[str, Any]:
            Return image repositories in a given registry.

    Examples:
        Calling this exec module function from the cli:

        .. code-block:: bash

            idem exec aws.ecr.repository.list

        Calling this exec module function with repository name from the cli:

        .. code-block:: bash

            idem exec aws.ecr.repository.list repository_names=['repository_name_01', 'repository_name_02']

        Calling this exec module function from within a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.ecr.repository.list
    """
    result = dict(comment=[], ret=[], result=True)

    ret = await hub.exec.boto3.client.ecr.describe_repositories(
        ctx=ctx, registryId=registry_id, repositoryNames=repository_names
    )

    if not ret["result"]:
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result

    if not ret["ret"].get("repositories"):
        result["comment"].append(
            hub.tool.aws.comment_utils.list_empty_comment(
                resource_type="aws.ecr.repository", name=None
            )
        )
        return result

    for repository in ret["ret"]["repositories"]:
        tags_results = await hub.tool.aws.ecr.tag.get_resource_tags(
            ctx=ctx, resource_arn=repository.get("repositoryArn")
        )

        result["ret"].append(
            hub.tool.aws.ecr.conversion_utils.convert_raw_repository_to_present(
                raw_resource=repository,
                idem_resource_name=repository.get("repositoryName"),
                tags=tags_results.get("ret"),
            )
        )

    return result
