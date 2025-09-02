"""Exec module for managing Amazon ECR Images."""
from typing import Any
from typing import Dict

__func_alias__ = {"list_": "list"}


async def get(
    hub,
    ctx,
    name: str,
    repository_name: str,
    registry_id: str = None,
    image_digest: str = None,
    image_tag: str = None,
) -> Dict[str, Any]:
    """Retrieves the specified AWS ECR Image details.

    Args:
        name(str):
            The name of the Idem state.
        repository_name(str):
            The name of repository that contains the image.
        registry_id(str, Optional):
            The Amazon Web Services account ID associated with the registry that contains the repository that contains the images.
            If you do not specify a registry, the default registry is assumed.
        image_digest(str, Optional):
            The sha256 digest of the image manifest. Either `image_digest` or `image_tag` has to be provided.
        image_tag(str, Optional):
            The tag used for the image. Either `image_digest` or `image_tag` has to be provided.

    Examples:
        Calling this exec module function from the cli:

        .. code-block:: bash

            idem exec aws.ecr.image.get name='idem_name' repository_name='ecr_repository_name' image_tag='ecr_image_tag'

        Calling this exec module function from within a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.ecr.image.get
                - kwargs:
                    name: 'idem_name'
                    repository_name: 'ecr_repository_name'
                    image_tag: 'ecr_image_tag'
    """
    result = dict(comment=[], ret=None, result=True)

    image_id = {}
    if image_digest:
        image_id["imageDigest"] = image_digest
    elif image_tag:
        image_id["imageTag"] = image_tag
    else:
        result["result"] = False
        result["comment"].append(
            "Either `image_digest` or `image_tag` has to be provided"
        )
        return result

    ret = await hub.exec.boto3.client.ecr.describe_images(
        ctx, registryId=registry_id, repositoryName=repository_name, imageIds=[image_id]
    )
    if not ret["result"]:
        if "RepositoryNotFoundException" in str(
            ret["comment"]
        ) or "ImageNotFoundException" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.ecr.image", name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result

    if not ret["ret"].get("imageDetails"):
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.ecr.image", name=name
            )
        )
        return result

    if len(ret["ret"]["imageDetails"]) > 1:
        result["comment"].append(
            hub.tool.aws.comment_utils.find_more_than_one(
                resource_type="aws.ecr.image", resource_id=name
            )
        )

    result["ret"] = hub.tool.aws.ecr.conversion_utils.convert_raw_image_to_present(
        raw_resource=ret["ret"]["imageDetails"][0],
        idem_resource_name=name,
    )

    return result


async def list_(
    hub,
    ctx,
    repository_name: str,
    registry_id: str = None,
) -> Dict[str, Any]:
    """Lists AWS ECR Images for a Repository.

    Arg:
        repository_name(str):
            The name of repository with images to be listed.

        registry_id(str, Optional):
            The Amazon Web Services account ID associated with the registry that contains the repository in which to list images.
            If you do not specify a registry, the default registry is assumed.

    Examples:
        Calling this exec module function from the cli:

        .. code-block:: bash

            idem exec aws.ecr.image.list repository_name='ecr_repository_name'

        Calling this exec module function from within a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.ecr.image.list
                - kwargs:
                    repository_name: 'ecr_repository_name'
    """
    result = dict(comment=[], ret=[], result=True)

    ret = await hub.exec.boto3.client.ecr.describe_images(
        ctx=ctx,
        repositoryName=repository_name,
        registryId=registry_id,
    )
    if not ret["result"]:
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result

    if not ret["ret"].get("imageDetails"):
        result["comment"].append(
            hub.tool.aws.comment_utils.list_empty_comment(
                resource_type="aws.ecr.image", name=repository_name
            )
        )
        return result

    for image in ret["ret"]["imageDetails"]:
        result["ret"].append(
            hub.tool.aws.ecr.conversion_utils.convert_raw_image_to_present(
                raw_resource=image
            )
        )

    return result
