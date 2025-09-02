"""Exec module for managing Amazon IAM Policies."""
import copy
from typing import Any
from typing import Dict
from typing import List


async def update(
    hub,
    ctx,
    policy_arn: str,
    policy_version_id: str,
    new_policy_document: str,
    timeout: Dict = None,
) -> Dict[str, Any]:
    """
    Update the policy document of an existing managed policy.

    Args:
        hub: The redistributed pop central hub.
        ctx: A dict with the keys/values for the execution of the Idem run located in
        `hub.idem.RUNS[ctx['run_name']]`.
        policy_arn: The Amazon Resource Name (ARN) of the managed policy that you want information about.
        policy_version_id: Identifies the policy version to retrieve. This parameter allows (through its regex pattern)
         a string of characters that consists of the lowercase letter 'v' followed by one or two digits, and optionally
          followed by a period '.' and a string of letters and digits.
        new_policy_document: The JSON policy document that you want to use as the content for the new policy.
        timeout(Dict, Optional): Timeout configuration for create/update/deletion of AWS IAM Policy.
            * update (str) -- Timeout configuration for updating AWS IAM Policy
                * delay -- The amount of time in seconds to wait between attempts.
                * max_attempts -- Customized timeout configuration containing delay and max attempts.

    Returns:
        {"result": True|False, "comment": Tuple, "ret": None}
    """
    result = dict(comment=[], result=True, ret=None)
    if new_policy_document is None:
        result["comment"] += [
            f"Skip aws.iam.policy update. New policy document is None"
        ]
        return result
    get_ret = await hub.exec.boto3.client.iam.get_policy_version(
        ctx=ctx, PolicyArn=policy_arn, VersionId=policy_version_id
    )
    if not get_ret["result"]:
        result["result"] = False
        result["comment"] = get_ret["comment"]
        return result
    old_policy = get_ret["ret"]
    if old_policy.get("PolicyVersion").get("Document") == new_policy_document:
        result["comment"] += ["No need to update aws.iam.policy policy document"]
        return result
    try:
        # Update the policy document by creating a new policy document, set it to default, and then delete the old
        # policy document
        create_ret = await hub.exec.boto3.client.iam.create_policy_version(
            ctx=ctx,
            PolicyArn=policy_arn,
            PolicyDocument=new_policy_document,
            SetAsDefault=True,
        )
        if not create_ret["result"]:
            result["result"] = False
            result["comment"] = create_ret["comment"]
            return result
        waiter_config = hub.tool.aws.waiter_utils.create_waiter_config(
            default_delay=1,
            default_max_attempts=40,
            timeout_config=timeout.get("update") if timeout else None,
        )
        hub.log.debug(f"Waiting on updating aws.iam.policy '{policy_arn}'")
        try:
            await hub.tool.boto3.client.wait(
                ctx,
                "iam",
                "policy_exists",
                PolicyArn=policy_arn,
                WaiterConfig=waiter_config,
            )
        except Exception as e:
            result["comment"] += [str(e)]
            result["result"] = False
        delete_ret = await hub.exec.boto3.client.iam.delete_policy_version(
            ctx=ctx, PolicyArn=policy_arn, VersionId=policy_version_id
        )
        if not delete_ret["result"]:
            hub.log.warning(
                f"hub.tool.aws.iam.policy.update failed to delete policy document with version"
                f" {policy_version_id} . Manual cleanup may be needed."
            )
            result["comment"] += [
                f"hub.tool.aws.iam.policy.update failed to delete policy document with version"
                f" {policy_version_id} . Manual cleanup may be needed."
            ]
        else:
            result["comment"] += [
                f"hub.tool.aws.iam.policy.update updated policy document to version"
                f" {create_ret['ret'].get('PolicyVersion').get('VersionId')}"
            ]
    except Exception as e:
        result["comment"] += [str(e)]
        result["result"] = False
    return result


async def update_tags(
    hub,
    ctx,
    police_arn: str,
    old_tags: List[Dict[str, Any]] or Dict[str, str] = None,
    new_tags: List[Dict[str, Any]] or Dict[str, str] = None,
) -> Dict[str, Any]:
    """
    Update tags of AWS IAM Policy

    Args:
        hub: The redistributed pop central hub.
        ctx: A dict with the keys/values for the execution of the Idem run located in
        `hub.idem.RUNS[ctx['run_name']]`.
        police_arn: The ARN of the IAM customer managed policy to which you want to add tags.
         This parameter allows (through its regex pattern) a string of characters consisting of upper and lowercase
          alphanumeric characters with no spaces. You can also include any of the following characters: _+=,.@-
        old_tags (List or Dict): list of old tags in the format of [{"Key": tag-key, "Value": tag-value}] or dict in the format of
                                 {tag-key: tag-value}
        new_tags (List or Dict): list of new tags in the format of [{"Key": tag-key, "Value": tag-value}] or dict in the format of
                                 {tag-key: tag-value}

    Returns:
        {"result": True|False, "comment": Tuple, "ret": Dict}
    """
    tags_to_add = {}
    tags_to_remove = {}
    if isinstance(old_tags, List):
        old_tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict(old_tags)
    if isinstance(new_tags, List):
        new_tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict(new_tags)
    if new_tags is not None:
        tags_to_remove, tags_to_add = hub.tool.aws.tag_utils.diff_tags_dict(
            old_tags=old_tags, new_tags=new_tags
        )
    result = dict(comment=[], result=True, ret={})
    if (not tags_to_remove) and (not tags_to_add):
        result["ret"] = copy.deepcopy(old_tags if old_tags else {})
        return result
    if tags_to_remove:
        if not ctx.get("test", False):
            delete_ret = await hub.exec.boto3.client.iam.untag_policy(
                ctx, PolicyArn=police_arn, TagKeys=list(tags_to_remove.keys())
            )
            if not delete_ret["result"]:
                result["comment"] = delete_ret["comment"]
                result["result"] = False
                return result
    if tags_to_add:
        if not ctx.get("test", False):
            add_ret = await hub.exec.boto3.client.iam.tag_policy(
                ctx,
                PolicyArn=police_arn,
                Tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags_to_add),
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
