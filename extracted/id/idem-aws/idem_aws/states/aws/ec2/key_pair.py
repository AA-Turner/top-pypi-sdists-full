"""
State module for managing EC2 Key Pairs

hub.exec.boto3.client.ec2.create_key_pair
hub.exec.boto3.client.ec2.delete_key_pair
hub.exec.boto3.client.ec2.describe_key_pairs
hub.exec.boto3.client.ec2.import_key_pair
resource = hub.tool.boto3.resource.crate(ctx,"ec2", "KeyPair", name)
"""
import copy
from typing import Any
from typing import Dict

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    public_key: str,
    resource_id: str = None,
    tags: Dict[str, str] = None,
) -> Dict[str, Any]:
    """Creates an ED25519 or 2048-bit RSA key pair with the specified name and in the specified PEM or PPK format that
    you can use with an Amazon EC2 instance.

    A key pair is used to control login access to EC2 instances. The key pair is available only in the Amazon Web
    Services Region in which you create it.

    Currently, this resource requires an existing user-supplied key pair. This key pair's public key will be registered
    with AWS to allow logging-in to EC2 instances. When importing an existing key pair the public key material may be in
    any format supported by AWS. Supported formats are described in Amazon docs:
    https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-key-pairs.html#how-to-generate-your-own-key-and-import-it-to-aws
    For more information, see the Amazon ec2 Developer Guide.
    Please note that, for security reasons, you cannot download the keypairs themselves.
    You'll simply be given their name and fingerprint.

    Args:
        name(str):
            The name for your new key pair.

        public_key(str):
            The public key material.

        resource_id(str, Optional):
            The key pair id.

        tags(Dict, Optional):
            dict of tags to assign to the key pair in the format of ``{"tag-key": "tag-value"}`` or dict in the format of
            ``{tag-key: tag-value}``. Defaults to None.

            * tag-key (str):
                The key of the tag. Tag keys are case-sensitive and accept a maximum of 127 Unicode characters.

            * tag-value (str):
                The value of the tag. Tag values are case-sensitive and accept a maximum of 255 Unicode characters.

    Request Syntax:
       .. code-block:: sls

          [key_pair_name]:
            aws.ec2.key_pair.present:
              - resource_id: 'string'
              - name: 'string'
              - public_key: 'string'
              - tags: Dict[str, str]
                  'string': 'string'
                  'string': 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_present:
              aws.ec2.key_pair.present:
                - name: value
                - public_key: value
                - tags:
                    first_key: first_value
                    second_key: second_value
    """

    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    resource_updated = False
    if resource_id:
        before = await hub.exec.aws.ec2.key_pair.get(
            ctx, name=name, filters=[{"name": "key-pair-id", "values": [resource_id]}]
        )

        if not before.get("result") and not before.get("ret"):
            result["result"] = False
            result["comment"] = before["comment"]
            return result

        result["old_state"] = copy.deepcopy(before["ret"])
        plan_state = copy.deepcopy(result["old_state"])
        old_tags = result["old_state"].get("tags")

        if tags is not None and tags != old_tags:
            update_ret = await hub.tool.aws.ec2.tag.update_tags(
                ctx,
                resource_id=resource_id,
                old_tags=old_tags,
                new_tags=tags,
            )
            result["result"] = update_ret["result"]
            result["comment"] = update_ret["comment"]

            if not update_ret["result"]:
                return result
            resource_updated = resource_updated or bool(update_ret["result"])

        if resource_updated:
            if ctx.get("test", False):
                plan_state["tags"] = update_ret["ret"]
                result["comment"] += hub.tool.aws.comment_utils.would_update_comment(
                    "aws.ec2.key_pair", name
                )
            else:
                result["comment"] += hub.tool.aws.comment_utils.update_comment(
                    "aws.ec2.key_pair", name
                )
        else:
            result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
                "aws.ec2.key_pair", name
            )
    else:
        if ctx.get("test", False):
            result["comment"] = hub.tool.aws.comment_utils.would_create_comment(
                resource_type="aws.ec2.key_pair", name=name
            )
            result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                enforced_state={},
                desired_state={
                    "name": name,
                    "resource_id": resource_id,
                    "public_key": public_key,
                    "tags": tags,
                },
            )
            return result

        ret = await hub.exec.boto3.client.ec2.import_key_pair(
            ctx,
            KeyName=name,
            PublicKeyMaterial=public_key,
            TagSpecifications=[
                {
                    "ResourceType": "key-pair",
                    "Tags": hub.tool.aws.tag_utils.convert_tag_dict_to_list(tags),
                }
            ]
            if tags
            else None,
        )

        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            return result
        result["comment"] = hub.tool.aws.comment_utils.create_comment(
            resource_type="aws.ec2.key_pair", name=name
        )

    if ctx.get("test", False):
        result["new_state"] = plan_state
    elif (not result["old_state"]) or resource_updated:
        after = await hub.exec.aws.ec2.key_pair.get(ctx, name=name)
        if not after["result"]:
            result["comment"] = after["comment"]
            result["result"] = after["result"]
            return result
        result["new_state"] = copy.deepcopy(after["ret"])
    else:
        result["new_state"] = copy.deepcopy(result["old_state"])

    return result


async def absent(hub, ctx, name: str, resource_id: str = None) -> Dict[str, Any]:
    """Deletes the specified key pair.

    Args:
        resource_id(str):
            An identifier of the resource in the provider.

        name(str, Optional):
            Name of the key_pair. Defaults to None.

    Request Syntax:
       .. code-block:: sls

          [key_pair_name]:
            aws.ec2.key_pair.absent:
              - resource_id: 'string'
              - name: 'string'

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            resource_is_absent:
              aws.ec2.key_pair.absent:
                - resource_id: idem-test-key_pair
                - name: idem-test-key_pair
    """

    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.ec2.key_pair", name=name
        )
        return result

    before = await hub.exec.aws.ec2.key_pair.get(
        ctx, name=name, filters=[{"name": "key-pair-id", "values": [resource_id]}]
    )

    if not before["result"]:
        result["comment"] = before["comment"]
        result["result"] = False
        return result
    if not before["ret"]:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.ec2.key_pair", name=name
        )
    elif ctx.get("test", False):
        result["old_state"] = copy.deepcopy(before["ret"])
        result["comment"] = hub.tool.aws.comment_utils.would_delete_comment(
            resource_type="aws.ec2.key_pair", name=name
        )
        return result
    else:
        result["old_state"] = copy.deepcopy(before["ret"])
        ret = await hub.exec.boto3.client.ec2.delete_key_pair(ctx, KeyName=name)
        result["result"] = ret["result"]
        if not result["result"]:
            result["comment"] = ret["comment"]
            result["result"] = False
            return result
        result["comment"] = hub.tool.aws.comment_utils.delete_comment(
            resource_type="aws.ec2.key_pair", name=name
        )
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describe the resource in a way that can be recreated/managed with the corresponding "present" function

    Returns information about all key pairs in the user's account.

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: bash

            $ idem describe aws.ec2.key_pair
    """

    result = {}
    ret = await hub.exec.boto3.client.ec2.describe_key_pairs(ctx, IncludePublicKey=True)

    if not ret["result"]:
        hub.log.warning(f"Could not describe key_pair {ret['comment']}")
        return result

    for key_pair in ret["ret"]["KeyPairs"]:
        resource_name = key_pair.get("KeyName")
        resource_translated = (
            hub.tool.aws.ec2.conversion_utils.convert_raw_key_pair_to_present(
                raw_resource=key_pair
            )
        )
        result[resource_name] = {
            "aws.ec2.key_pair.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in resource_translated.items()
            ]
        }

    return result
