import copy
from typing import Any
from typing import Dict


async def get(hub, ctx, name, resource_id: str = None):
    """
    Provides details about a specific instance profile as a data-source

    Args:
        name(str):
            The AWS Instance Profile name

        resource_id(str, Optional):
            AWS Instance Profile name to identify the resource

    Returns:
        dict[str, Any]:
            Returns the instance profile

    Examples:
        Calling this exec module function from the cli:

        .. code-block:: bash

            idem exec aws.iam.instance_profile.get name="name" resource_id="resource_id"

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.iam.instance_profile.get
                - kwargs:
                    name: name
                    resource_id: resource_id
    """
    result = dict(comment=[], ret=None, result=True)

    ret = await hub.exec.boto3.client.iam.get_instance_profile(
        ctx, InstanceProfileName=resource_id if resource_id else name
    )

    if not ret["result"]:
        if "NoSuchEntity" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.iam.instance_profile", name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result

    resource = ret["ret"]["InstanceProfile"]
    result[
        "ret"
    ] = hub.tool.aws.iam.conversion_utils.convert_raw_instance_profile_to_present(
        resource
    )
    return result


async def update_instance_profile_tags(
    hub,
    ctx,
    instance_profile_name: str,
    old_tags: Dict[str, Any],
    new_tags: Dict[str, Any],
):
    """
    Update tags of AWS IAM Instance Profile

    TODO - this method might fail with localstack but is successful with a real AWS account

    Args:
        instance_profile_name(str):
            The AWS Instance Profile name

        old_tags(dict):
            A dict of old tags

        new_tags(dict):
            A dict of new tags

    Returns:
        dict[str, Any]:
            Tags after the update

    Examples:
        Calling this exec module function from the cli:

        .. code-block:: bash

            idem exec aws.iam.instance_profile.update_instance_profile_tags instance_profile_name="name" old_tags='{}' new_tags='{}'

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.iam.instance_profile.update_instance_profile_tags
                - kwargs:
                    instance_profile_name: name
                    old_tags:
                        old_tag: old_val
                    new_tags:
                        new_tag: new_val
    """
    result = dict(comment=[], result=True, ret=None)

    tags_to_add = {}
    tags_to_remove = {}
    if new_tags is not None:
        tags_to_remove, tags_to_add = hub.tool.aws.tag_utils.diff_tags_dict(
            old_tags=old_tags, new_tags=new_tags
        )
    if (not tags_to_remove) and (not tags_to_add):
        result["ret"] = copy.deepcopy(old_tags if old_tags else {})
        return result
    if tags_to_remove:
        if not ctx.get("test", False):
            delete_ret = await hub.exec.boto3.client.iam.untag_instance_profile(
                ctx,
                InstanceProfileName=instance_profile_name,
                TagKeys=list(tags_to_remove.keys()),
            )
            if not delete_ret["result"]:
                result["comment"] = delete_ret["comment"]
                result["result"] = False
                return result
    if tags_to_add:
        if not ctx.get("test", False):
            add_ret = await hub.exec.boto3.client.iam.tag_instance_profile(
                ctx,
                InstanceProfileName=instance_profile_name,
                Tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags=tags_to_add),
            )
            if not add_ret["result"]:
                result["comment"] = add_ret["comment"]
                result["result"] = False
                return result

    result["ret"] = new_tags
    if ctx.get("test", False):
        result["comment"] = hub.tool.aws.comment_utils.would_update_tags_comment(
            tags_to_remove=tags_to_remove, tags_to_add=tags_to_add
        )
    else:
        result["comment"] = hub.tool.aws.comment_utils.update_tags_comment(
            tags_to_remove=tags_to_remove, tags_to_add=tags_to_add
        )
    return result
