"""Exec module for managing KMS Keys."""
from typing import Dict

__func_alias__ = {"list_": "list"}


async def get(
    hub,
    ctx,
    name,
    resource_id,
) -> Dict:
    """Get a KMS Key resource from AWS.

    Args:
        name(str):
            The name of the Idem state.

        resource_id(str):
            Key ARN or alias ARN or alias name
            To specify a KMS key, use its key ID, key ARN, alias name, or alias ARN.
            When using an alias name, prefix it with "alias/". To specify a KMS key in a different Amazon Web Services
            account, you must use the key ARN or alias ARN.

    """
    result = dict(comment=[], ret=None, result=True)
    ret = await hub.exec.boto3.client.kms.describe_key(ctx, KeyId=resource_id)
    if not ret["result"]:
        if "NotFoundException" in str(ret["comment"]):
            result["comment"].append(
                hub.tool.aws.comment_utils.get_empty_comment(
                    resource_type="aws.kms.key", name=name
                )
            )
            result["comment"] += list(ret["comment"])
            return result
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    if not ret["ret"]["KeyMetadata"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.kms.key", name=name
            )
        )
        return result

    result[
        "ret"
    ] = await hub.tool.aws.kms.conversion_utils.convert_raw_key_to_present_async(
        ctx, raw_resource=ret["ret"]["KeyMetadata"]
    )
    return result


async def list_(
    hub,
    ctx,
    name,
) -> Dict:
    """Fetch a list of Kms Keys from AWS.

    Args:
        name(str):
            The name of the Idem state.
    """
    result = dict(comment=[], ret=[], result=True)
    ret = await hub.exec.boto3.client.kms.list_keys(ctx)
    if not ret["result"]:
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    if not ret["ret"]["Keys"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.list_empty_comment(
                resource_type="aws.kms.key", name=name
            )
        )
        return result
    for key in ret["ret"]["Keys"]:
        key_details = await hub.exec.boto3.client.kms.describe_key(
            ctx, KeyId=key["KeyId"]
        )
        if key_details.get("result") is False:
            hub.log.debug(
                f"Failed to describe key with Id {key.get('KeyId')}: {key_details.get('comment')}"
            )
            continue

        try:
            result["ret"].append(
                await hub.tool.aws.kms.conversion_utils.convert_raw_key_to_present_async(
                    ctx, raw_resource=key_details["ret"]["KeyMetadata"]
                )
            )
        except Exception as e:
            hub.log.debug(f"Failed to convert key with Id {key.get('KeyId')}: {e}")
            continue
    return result
