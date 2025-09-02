"""State module for managing Amazon KMS Keys."""
import copy
from typing import Any
from typing import Dict
from typing import List

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    description: str = "",
    key_usage: str = "ENCRYPT_DECRYPT",
    key_spec: str = "SYMMETRIC_DEFAULT",
    key_state: str = "Enabled",
    origin: str = "AWS_KMS",
    multi_region: bool = False,
    policy: str = None,
    bypass_policy_lockout_safety_check: bool = False,
    enable_key_rotation: bool = False,
    tags: List[Dict[str, Any]] or Dict[str, Any] = None,
    timeout: Dict = None,
) -> Dict[str, Any]:
    """Creates an AWS KMS key.

    Update limitations:
      * ``policy`` can be updated, but cannot be cleared once set.
      * ``multi_region``, ``key_usage``, and ``key_spec`` cannot be updated.
      * ``enable_key_rotation`` cannot be enabled on asymmetric KMS keys.

    Args:
        name(str):
            An Idem name of the resource.
        resource_id(str, Optional):
            The ID or ARN of the key in Amazon Web Services.
        description(str, Optional):
            A description of the KMS key.
        key_usage(str, Optional):
            Determines the cryptographic operations for which you can use the KMS key.
            The default value is ``ENCRYPT_DECRYPT``.
            Valid values are ``ENCRYPT_DECRYPT``, ``GENERATE_VERIFY_MAC``, ``SIGN_VERIFY``.
        key_spec(str, Optional):
            Specifies the type of KMS key to create. The default value is ``SYMMETRIC_DEFAULT``.
            Valid values are ``SYMMETRIC_DEFAULT``, ``HMAC_224``, ``HMAC_256``, ``HMAC_384``, ``HMAC_512``,
            ``RSA_2048``, ``RSA_3072``, ``RSA_4096``, ``ECC_NIST_P256``, ``ECC_NIST_P384``, ``ECC_NIST_P521``,
            ``ECC_SECG_P256K1``, ``SM2``.
        key_state(str, Optional):
            Whether the key is enabled or not. The default value is ``Enabled``.
            Valid values are ``Enabled``, ``Disabled``.
        origin(str, Optional):
            The source of the key material for the KMS key. The default value is ``AWS_KMS``.
            Valid values are ``AWS_KMS``, ``EXTERNAL``, ``AWS_CLOUDHSM``.
        multi_region(bool, Optional):
            Creates a multi-Region primary key that you can replicate into other Amazon Web Services Regions.
            Default value is ``False``.
        policy(str, Optional):
            The key policy to attach to the KMS key. If you do not specify a key policy,
            KMS attaches a default key policy to the KMS key.
        bypass_policy_lockout_safety_check(bool, Optional):
            A flag to indicate whether to bypass the key policy lockout safety check. Default value is ``False``.

            .. warning::
              Setting this value to ``True`` increases the risk that the KMS key becomes unmanageable.
              Do not set this value to ``True`` indiscriminately.

        enable_key_rotation(bool, Optional):
            Whether to enable or disable automatic rotation of the key material of the specified symmetric
            encryption KMS key. Default value is ``False``.
        tags(dict or list, Optional):
            Dict in the format of ``{tag-key: tag-value}`` or List of tags in the format of
            ``[{"TagKey": tag-key, "TagValue": tag-value}]`` to associate with the key.
            To use this parameter, you must have ``kms:TagResource`` permission in an IAM policy.

            * TagKey (*str*):
                The key of the tag.
            * TagValue (*str*):
                The value of the tag.
        timeout(dict, Optional):
            Timeout configuration for update of AWS KMS key.

            * update (*dict, Optional*):
                Timeout configuration when updating a KMS key.

                * delay (*int, Optional*):
                    The amount of time in seconds to wait between attempts. Default value is ``2``.
                * max_attempts (*int, Optional*):
                    Max attempts of waiting for change. Default value is ``120``.

    Request Syntax:
      .. code-block:: sls

        [idem_test_aws_kms_key]:
          aws.kms.key.present:
            - name: 'string'
            - resource_id: 'string'
            - description: 'string'
            - key_usage: 'ENCRYPT_DECRYPT|GENERATE_VERIFY_MAC|SIGN_VERIFY'
            - key_spec: 'SYMMETRIC_DEFAULT|HMAC_224|HMAC_256|HMAC_384|HMAC_512|RSA_2048|RSA_3072|RSA_4096|ECC_NIST_P256|
                        ECC_NIST_P384|ECC_NIST_P521|ECC_SECG_P256K1|SM2'
            - key_state: 'Enabled|Disabled'
            - origin: 'AWS_KMS|EXTERNAL|AWS_CLOUDHSM'
            - multi_region: True|False
            - policy: 'string'
            - bypass_policy_lockout_safety_check: True|False
            - enable_key_rotation: True|False
            - tags:
                - TagKey: 'string'
                  TagValue: 'string'
            - timeout:
                update:
                  delay: int
                  max_attemps: int

    Returns:
        Dict[str, Any]

    Examples:
        .. code-block:: sls

            idem_test_aws_kms_key:
              aws.kms.key.present:
                - name: idem_test_kms_key
                - description: 'AWS KMS KEY'
                - key_usage: 'ENCRYPT_DECRYPT'
                - key_spec: 'SYMMETRIC_DEFAULT'
                - key_state: 'Enabled'
                - origin: 'AWS_KMS'
                - multi_region: False
                - policy:
                    Version: '2012-10-17'
                    Statement:
                      - Sid: 'EnableIAMUserPermissions'
                        Effect: 'Allow'
                        Principal:
                          AWS: 'arn:aws:iam::111122223333:root'
                        Action: ['kms:*']
                        Resource: '*'
                - bypass_policy_lockout_safety_check: False
                - enable_key_rotation: False
                - tags:
                    - TagKey: provider
                      TagValue: idem
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)

    plan_state = {}
    updated_vals = {}

    if isinstance(tags, List):
        tags = hub.tool.aws.tag_utils.convert_tag_list_to_dict_tagkey(tags)

    policy = hub.tool.aws.state_comparison_utils.standardise_json(policy)

    if resource_id:
        before = await hub.exec.aws.kms.key.get(ctx, name=name, resource_id=resource_id)
        if not before["result"] or not before["ret"]:
            result["result"] = False
            result["comment"] = before["comment"]
            return result

        result["comment"] = hub.tool.aws.comment_utils.already_exists_comment(
            resource_type="aws.kms.key", name=name
        )
        result["old_state"] = copy.deepcopy(before["ret"])
        # Used for 'test'
        plan_state = copy.deepcopy(result["old_state"])

        # Update key tags if tags are specified
        if tags is not None and tags != result["old_state"].get("tags"):
            hub.log.debug(f"aws.kms.key '{name}' tags update")
            # For tag operations key_id is used and not resource_id
            update_ret = await hub.tool.aws.kms.tag.update_tags(
                ctx=ctx,
                key_id=resource_id,
                old_tags=result["old_state"].get("tags", []),
                new_tags=tags,
            )

            result["result"] = update_ret["result"]
            result["comment"] += update_ret["comment"]
            if not result["result"]:
                return result

            plan_state["tags"] = update_ret["ret"]
            updated_vals["tags"] = tags

        # Enable/Disable key
        # No updates for key_state "PendingDeletion", which means the key is scheduled to be deleted.
        old_state = result["old_state"].get("key_state", "")
        if key_state != old_state:
            if ctx.get("test", False):
                result["comment"] += [f"Would update state on aws.kms.key '{name}'."]
                plan_state["key_state"] = key_state
            else:
                update_ret = None
                if old_state == "Enabled" and key_state == "Disabled":
                    update_ret = await hub.exec.boto3.client.kms.disable_key(
                        ctx, KeyId=result["old_state"]["resource_id"]
                    )
                elif old_state == "Disabled" and key_state == "Enabled":
                    update_ret = await hub.exec.boto3.client.kms.enable_key(
                        ctx, KeyId=result["old_state"]["resource_id"]
                    )

                if update_ret:
                    hub.log.debug(
                        f"Updated the state of aws.kms.key '{name}' to '{key_state}'."
                    )
                    result["comment"] += [
                        f"Updated aws.kms.key '{name}' state to '{key_state}'."
                    ]
                    updated_vals["key_state"] = key_state
                else:
                    hub.log.warning(
                        f"Failed to update the state of aws.kms.key '{name}' to '{key_state}'. {update_ret['comment']} "
                    )
                    result["result"] = update_ret["result"]
                    result["comment"] += update_ret["comment"]
                    return result

        # Update policy and/or bypass flag if needed and if policy is set
        update_policy = (
            policy
            and not hub.tool.aws.state_comparison_utils.are_policies_equal(
                result["old_state"].get("policy"), policy
            )
        )
        update_bypass_lockout = bypass_policy_lockout_safety_check != result[
            "old_state"
        ].get("bypass_policy_lockout_safety_check", False)
        if policy and (update_policy or update_bypass_lockout):
            if ctx.get("test", False):
                if update_policy:
                    result["comment"] += [
                        f"Would update policy of aws.kms.key '{name}'."
                    ]
                if update_bypass_lockout:
                    result["comment"] += [
                        f"Would update bypass_policy_lockout_safety_check of aws.kms.key '{name}'."
                    ]
                plan_state["policy"] = policy
                plan_state[
                    "bypass_policy_lockout_safety_check"
                ] = bypass_policy_lockout_safety_check
            else:
                update_ret = await hub.exec.boto3.client.kms.put_key_policy(
                    ctx,
                    KeyId=result["old_state"]["resource_id"],
                    Policy=policy,
                    PolicyName="default",
                    BypassPolicyLockoutSafetyCheck=bypass_policy_lockout_safety_check,
                )

                if update_ret["result"]:
                    if update_policy:
                        result["comment"] += [f"Updated aws.kms.key '{name}' policy."]
                        updated_vals["policy"] = policy
                    if update_bypass_lockout:
                        result["comment"] += [
                            f"Updated aws.kms.key '{name}' bypass_policy_lockout_safety_check."
                        ]
                        updated_vals[
                            "bypass_policy_lockout_safety_check"
                        ] = bypass_policy_lockout_safety_check
                else:
                    hub.log.warning(
                        f"Failed to update the policy and/or bypass_policy_lockout_safety_check of "
                        f"aws.kms.key '{name}': {update_ret['comment']}"
                    )
                    result["result"] = update_ret["result"]
                    result["comment"] += update_ret["comment"]
                    return result

        # Update description if needed
        if description and description != result["old_state"].get("description"):
            if ctx.get("test", False):
                result["comment"] += [
                    f"Would update description of aws.kms.key '{name}'."
                ]
                plan_state["description"] = description
            else:
                update_ret = await hub.exec.boto3.client.kms.update_key_description(
                    ctx,
                    KeyId=result["old_state"]["resource_id"],
                    Description=description,
                )

                if update_ret["result"]:
                    result["comment"] += [f"Updated aws.kms.key '{name}' description."]
                    updated_vals["description"] = description
                else:
                    hub.log.warning(
                        f"Failed to update the description of aws.kms.key '{name}': {update_ret['comment']}"
                    )
                    result["result"] = update_ret["result"]
                    result["comment"] += update_ret["comment"]
                    return result
    else:
        try:
            if ctx.get("test", False):
                result["new_state"] = hub.tool.aws.test_state_utils.generate_test_state(
                    enforced_state={},
                    desired_state={
                        "name": name,
                        "resource_id": f"key-{name}-resource_id",
                        "arn": f"key-{name}-arn",
                        "description": description,
                        "key_usage": key_usage,
                        "key_spec": key_spec,
                        "origin": origin,
                        "multi_region": multi_region,
                        "policy": policy,
                        "bypass_policy_lockout_safety_check": bypass_policy_lockout_safety_check,
                        "enable_key_rotation": enable_key_rotation,
                        "tags": tags,
                    },
                )
                result["comment"] += [f"Would create aws.kms.key {name}"]
                return result

            ret = await hub.exec.boto3.client.kms.create_key(
                ctx,
                Description=description,
                KeyUsage=key_usage,
                KeySpec=key_spec,
                Origin=origin,
                MultiRegion=multi_region,
                Policy=policy,
                BypassPolicyLockoutSafetyCheck=bypass_policy_lockout_safety_check,
                Tags=hub.tool.aws.tag_utils.convert_tag_dict_to_list_tagkey(tags)
                if tags
                else None,
            )

            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = ret["comment"]
                return result
            resource_id = ret["ret"]["KeyMetadata"]["KeyId"]
            result["comment"] += [
                f"Created aws.kms.key '{name}' with description '{description}'."
            ]
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] = f"{e.__class__.__name__}: {e}"
            result["result"] = False

    # Set key rotation:
    # Enable it on a newly created key or Enable/Disable on an existing key,
    # only if the key_state is Enabled
    if (enable_key_rotation and result.get("old_state") is None) or (
        result.get("old_state")
        and (
            key_state == "Enabled"
            or (key_state is None and result["old_state"].get("key_state") == "Enabled")
        )
        and enable_key_rotation != result["old_state"].get("enable_key_rotation", False)
    ):
        update_ret = await hub.tool.aws.kms.key.set_key_rotation(
            ctx=ctx,
            resource_id=resource_id,
            enable_key_rotation=enable_key_rotation,
        )
        plan_state["enable_kms_rotation"] = enable_key_rotation
        result["comment"] += update_ret["comment"]
        if not update_ret["result"]:
            result["result"] = False
            return result

    if ctx.get("test", False):
        result["new_state"] = plan_state
    else:
        if updated_vals:
            wait_updates_res = await hub.tool.aws.kms.key.wait_for_updates(
                ctx,
                timeout=timeout.get("update") if timeout else None,
                resource_id=resource_id,
                updates=updated_vals,
            )
            if wait_updates_res["result"] is False:
                # Do not fail just add to comments
                result["comment"] += wait_updates_res["comment"]

            result["new_state"] = wait_updates_res["ret"]
        else:
            after = await hub.exec.aws.kms.key.get(
                ctx, name=name, resource_id=resource_id
            )
            if not after["result"]:
                result["result"] = False
                result["comment"] = after["comment"]
                return result
            result["new_state"] = copy.deepcopy(after["ret"])

    return result


async def absent(
    hub, ctx, name: str, resource_id: str = None, pending_window_in_days: int = 7
) -> Dict[str, Any]:
    """Deletes an AWS KMS key.

    Key cannot be immediately deleted but can be scheduled to be deleted.
    Once the key is set to be deleted in ``pending_window_in_days`` a deletion date is set on the key and it cannot
    be modified. So deleting again with a different ``pending_window_in_days`` is ignored. Also key can be disabled
    using the "present" function with ``key_state: 'Disabled'``.

    Args:
        name(str):
            An Idem name of the resource.
        resource_id(str, Optional):
            The ID or ARN of the key in Amazon Web Services.

            .. warning::
              Idem automatically considers this resource being absent if this field is not specified.

        pending_window_in_days(int, Optional):
            The waiting period, specified in number of days. After the waiting period ends, KMS deletes the KMS key.
            Default value is ``7``.

    Returns:
        Dict[str, Any]

    Request Syntax:
      .. code-block:: sls

        [idem_test_aws_kms_key]:
          aws.kms.key.absent:
            - name: 'string'
            - resource_id: 'string'
            - pending_window_in_days: 'int'

    Examples:
        .. code-block:: sls

            idem_test_aws_kms_key:
              aws.kms.key.absent:
                - name: idem_test_kms_key
                - resource_id: 1234abcd-12ab-34cd-56ef-1234567890ab
                - pending_window_in_days: 2
    """
    result = dict(comment=[], old_state=None, new_state=None, name=name, result=True)
    if not resource_id:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.kms.key", name=name
        )
        return result
    before = await hub.exec.aws.kms.key.get(ctx, name=name, resource_id=resource_id)

    if not before:
        result["comment"] = hub.tool.aws.comment_utils.already_absent_comment(
            resource_type="aws.kms.key", name=name
        )
        return result
    else:
        result["old_state"] = copy.deepcopy(before["ret"])

        if before["ret"].get("deletion_date", None):
            result[
                "comment"
            ] = f"aws.kms.key '{resource_id}' already scheduled to be deleted in '{pending_window_in_days}' days"
            return result

        if ctx.get("test", False):
            result[
                "comment"
            ] = f"Would schedule deletion of aws.kms.key '{resource_id}' in {pending_window_in_days} days"
            return result

        try:
            # Minimum deletion schedule 7 days (from 7 - 30)
            ret = await hub.exec.boto3.client.kms.schedule_key_deletion(
                ctx,
                KeyId=resource_id,
                PendingWindowInDays=pending_window_in_days,
            )
            result["result"] = ret["result"]
            if not result["result"]:
                result["comment"] = ret["comment"]
                result["result"] = False
                return result
            result[
                "comment"
            ] = f"aws.kms.key '{resource_id}' is scheduled for deletion in {pending_window_in_days} days"
        except hub.tool.boto3.exception.ClientError as e:
            result["comment"] += [f"{e.__class__.__name__}: {e}"]

    try:
        after = await hub.exec.aws.kms.key.get(
            ctx, name=name, resource_id=(resource_id if resource_id else name)
        )
        if not after["result"]:
            result["result"] = False
            result["comment"] = after["comment"]
            return result
        result["new_state"] = copy.deepcopy(after["ret"])
    except Exception as e:
        result["comment"] += [str(e)]
        result["result"] = False
    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    """Describes AWS KMS keys in a way that can be recreated/managed with the corresponding "present" function.

    Returns:
        Dict[str, Dict[str, Any]]

    Examples:
        .. code-block:: bash

            $ idem describe aws.kms.key
    """
    result = {}
    ret = await hub.exec.boto3.client.kms.list_keys(ctx)

    if not ret["result"]:
        hub.log.warning(f"Could not describe aws.kms.keys {ret['comment']}")
        return {}

    for key in ret["ret"]["Keys"]:
        key_details = await hub.exec.boto3.client.kms.describe_key(
            ctx, KeyId=key.get("KeyId", None)
        )
        if key_details.get("result") is False:
            hub.log.debug(
                f"Failed to describe key with Id {key.get('KeyId')}: {key_details.get('comment')}"
            )
            continue

        try:
            translated_resource = await hub.tool.aws.kms.conversion_utils.convert_raw_key_to_present_async(
                ctx, raw_resource=key_details["ret"]["KeyMetadata"]
            )
        except Exception as e:
            hub.log.debug(f"Failed to convert key with Id {key.get('KeyId')}: {e}")
            continue

        result[translated_resource["resource_id"]] = {
            "aws.kms.key.present": [
                {parameter_key: parameter_value}
                for parameter_key, parameter_value in translated_resource.items()
            ]
        }

    return result
