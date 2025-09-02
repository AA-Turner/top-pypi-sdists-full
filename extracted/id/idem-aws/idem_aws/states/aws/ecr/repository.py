"""State module for managing Amazon ECR Repositories."""
import copy
from dataclasses import field
from dataclasses import make_dataclass
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    registry_id: str = None,
    image_tag_mutability: str = None,
    image_scanning_configuration: make_dataclass(
        """The image scanning configuration for the repository."""
        "ImageScanningConfiguration",
        [("scanOnPush", bool, field(default=None))],
    ) = None,
    encryption_configuration: make_dataclass(
        """The encryption configuration for the repository."""
        "EncryptionConfiguration",
        [("encryptionType", str), ("kmsKey", str, field(default=None))],
    ) = None,
    tags: Dict[str, Any]
    or List[
        make_dataclass("Tag", [("Key", str), ("Value", str, field(default=None))])
    ] = None,
) -> Dict[str, Any]:
    """Creates an AWS ECR repository.

    Repository properties cannot be updated after creation, only tags can be updated.

    Args:
        name(str):
            An Idem name of the resource.
        resource_id(str, Optional):
            The name of the ECR repository in Amazon Web Services.
        registry_id(str, Optional):
            The Amazon Web Services account ID associated with the registry to create the repository. If you
            do not specify a registry, the default registry is assumed.
        image_tag_mutability(str, Optional):
            The tag mutability setting for the repository. If this parameter is omitted, the default setting
            of ``MUTABLE`` will be used which will allow image tags to be overwritten. If ``IMMUTABLE`` is
            specified, all image tags within the repository will be immutable which will prevent them from
            being overwritten.
        image_scanning_configuration(dict, Optional):
            The image scanning configuration for the repository.

            * scanOnPush (*bool, Optional*):
                The setting that determines whether images are scanned after being pushed to a repository.
                If set to true , images will be scanned after being pushed. If this parameter is not specified,
                it will default to false and images will not be scanned unless a scan is manually started.
        encryption_configuration(dict, Optional):
            The encryption configuration for the repository.

            * encryptionType (*str*):
                The encryption type to use. If you use the ``KMS`` encryption type, the contents of the repository will be encrypted
                using server-side encryption with Key Management Service key stored in KMS. If you use the ``AES256`` encryption type,
                Amazon ECR uses server-side encryption with Amazon S3-managed encryption keys which encrypts the images in the
                repository using an AES-256 encryption algorithm.
            * kmsKey (*str, Optional*):
                If you use the KMS encryption type, specify the KMS key to use for encryption. The alias, key ID,
                or full ARN of the KMS key can be specified. The key must exist in the same Region as the repository.
                If no key is specified, the default Amazon Web Services managed KMS key for Amazon ECR will be used.
        tags(dict or list, Optional):
            Dict in the format of ``{tag-key: tag-value}`` or List of tags in the format of
            ``[{"Key": tag-key, "Value": tag-value}]`` to associate with the repository.

            * Key (*str*):
                One part of a key-value pair that make up a tag. A key is a general label that acts like a category for more specific
                tag values. Tag keys can have a maximum character length of 128 characters
            * Value (*str*):
                A value acts as a descriptor within a tag category (key). Tag values can have a maximum length of 256 characters.

    Request Syntax:
      .. code-block:: sls

        [idem_test_aws_ecr_repository]:
          aws.ecr.repository.present:
            - name: 'string'
            - registry_id: 'string'
            - image_tag_mutability: 'MUTABLE|IMMUTABLE'
            - image_scanning_configuration:
                scanOnPush: True|False
            - encryption_configuration:
                encryptionType: 'AES256|KMS'
                kmsKey: 'string'
            - tags:
              - Key: 'string'
                Value: 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            idem_test_aws_ecr_repository:
              aws.ecr.repository.present:
                - name: idem_test_ecr_repository
                - registry_id: idem_test_ecr_registry
                - image_tag_mutability: 'MUTABLE'
                - image_scanning_configuration:
                    scanOnPush: False
                - encryption_configuration:
                    encryptionType: 'AES256'
                - tags:
                  - Key: provider
                    Value: idem
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    before_ret = None
    if resource_id:
        before_ret = await hub.exec.aws.ecr.repository.get(
            ctx, name=name, resource_id=resource_id, registry_id=registry_id
        )

    if isinstance(tags, List):
        tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict(tags)

    # Repositories cannot be updated after creation with the Amazon Web Service API,
    # only repository tags can be updated
    if before_ret and before_ret["ret"]:  # resource present
        result["comment"] += [f"aws.ecr.repository '{name}' already exists"]

        updated = False
        result["old_state"] = copy.deepcopy(before_ret["ret"])

        if tags is not None and tags != result["old_state"].get("tags"):
            update_tags_ret = await hub.tool.aws.ecr.tag.update_tags(
                ctx=ctx,
                resource_arn=result["old_state"].get("repository_arn"),
                old_tags=result["old_state"].get("tags"),
                new_tags=tags,
            )

            if not update_tags_ret["result"]:
                result["result"] = False
                result["comment"] += update_tags_ret["comment"]
                return result

            updated = updated or bool(update_tags_ret["result"])
            result["comment"] += update_tags_ret["comment"]

            if ctx.get("test", False) and updated:
                result["new_state"] = copy.deepcopy(result["old_state"])
                if len(update_tags_ret["ret"]) > 0:
                    result["new_state"]["tags"] = update_tags_ret["ret"]
                else:
                    result["new_state"]["tags"] = None
                result["comment"] += [
                    f"Would have updated tags for aws.ecr.repository '{name}'"
                ]
                return result

        if not updated:
            result["new_state"] = copy.deepcopy(result["old_state"])
            return result

        result["comment"] += [f"Updated aws.ecr.repository '{name}'"]
    else:
        if ctx.get("test", False):
            result[
                "new_state"
            ] = raw_resource = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "resource_id": name,
                    "registry_id": registry_id,
                    "repository_name": name,
                    "image_tag_mutability": image_tag_mutability,
                    "image_scanning_configuration": image_scanning_configuration,
                    "encryption_configuration": encryption_configuration,
                    "tags": tags,
                },
            )
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.ecr.repository", name=name
            )
            return result

        create_ret = await hub.exec.boto3.client.ecr.create_repository(
            ctx,
            registryId=registry_id,
            repositoryName=name,
            imageTagMutability=image_tag_mutability,
            imageScanningConfiguration=image_scanning_configuration,
            encryptionConfiguration=encryption_configuration,
            tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags)
            if tags
            else None,
        )
        if not result["result"]:
            result["result"] = False
            result["comment"] = create_ret["comment"]
            return result

        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.ecr.repository", name=name
        )
        resource_id = name

    new_state = await hub.exec.aws.ecr.repository.get(
        ctx, name=name, resource_id=resource_id, registry_id=registry_id
    )

    result["new_state"] = copy.deepcopy(new_state["ret"])

    return result


async def absent(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    registry_id: str = None,
    force: bool = None,
) -> Dict[str, Any]:
    """Deletes an AWS ECR repository.

    If the repository contains images, you must either delete all images in the repository or
    use the force option to delete the repository.

    Args:
        name(str):
            An Idem name of the resource.
        resource_id(str, Optional):
            The name of the ECR repository in Amazon Web Services.

            .. warning::
              Idem automatically considers this resource being absent if this field is not specified.

        registry_id(str, Optional):
            The Amazon Web Services account ID associated with the registry that contains the repository to
            delete. If you do not specify a registry, the default registry is assumed.
        force(bool, Optional):
            If a repository contains images, forces the deletion.

    Request syntax:
      .. code-block:: sls

        [idem_test_aws_ecr_repository]:
          aws.ecr.repository.absent:
            - name: 'string'
            - resource_id: 'string'
            - registry_id: 'string'
            - force: True|False

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            idem_test_aws_ecr_repository:
              aws.ecr.repository.absent:
                - name: idem_test_ecr_repository
                - resource_id: idem_test_ecr_repository
                - registry_id: idem_test_ecr_registry
                - force: True
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.ecr.repository", name=name
        )
        return result

    before_ret = await hub.exec.aws.ecr.repository.get(
        ctx, name=name, resource_id=resource_id, registry_id=registry_id
    )

    # Case: Error
    if not before_ret["result"]:
        result["result"] = False
        result["comment"] = before_ret["comment"]
        return result

    # Case: No repository in the result
    if not before_ret["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.ecr.repository", name=name
        )
        return result
    elif ctx.get("test", False):
        # Case: --test context
        result["old_state"] = before_ret["ret"]
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.ecr.repository", name=name
        )
        return result

    # Case: Found the old state
    result["old_state"] = copy.deepcopy(before_ret["ret"])
    delete_ret = await hub.exec.boto3.client.ecr.delete_repository(
        ctx, repositoryName=resource_id, registryId=registry_id, force=force
    )

    if not delete_ret["result"]:
        result["result"] = False
        result["comment"] = delete_ret["comment"]
        return result

    result["comment"] = hub.tool.aws.comment_utils.delete_comment(
        resource_type="aws.ecr.repository", name=name
    )

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describes AWS ECR repositories in a registry in a way that can be recreated/managed with the corresponding "present" function.

    Returns:
        Dict[str, Dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe aws.ecr.repository
    """
    result = {}

    describe_ret = await hub.exec.aws.ecr.repository.list(ctx)
    if not describe_ret["result"]:
        hub.log.warning(f"Could not describe repository: {describe_ret['comment']}")
        return result

    for repository in describe_ret["ret"]:
        resource_id = repository.get("repository_name")
        result[resource_id] = {
            "aws.ecr.repository.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in repository.items()
            ]
        }

    return result
