import asyncio
from typing import Any
from typing import Dict


async def wait_for_updates(
    hub, ctx, timeout: Dict, resource_id: str, updates: Dict
) -> Dict[str, Any]:
    """
    Wait for key attribute updates.
    Possible attributes: description, state, policy, tags

    :param timeout: dictionary with 'delay in seconds and 'max_attempts'
    :param resource_id: key resource id
    :param updates: dictionary of key attribute and new value
    :return:
    """

    ret = dict(comment=[], result=True, ret=None)

    if updates is None or len(updates) == 0:
        hub.log.debug(f"No updates for KMS key '{resource_id}'")
        ret["comment"] += [f"No updates for KMS key '{resource_id}'"]
        return ret

    # sleep time seconds
    delay = timeout.get("delay", 2) if timeout else 2
    max_attempts = timeout.get("max_attempts", 120) if timeout else 120
    count = 1
    while count <= max_attempts and updates:
        hub.log.info(
            f"Waiting for key {resource_id} updates: '{updates.keys()}' for the {count} time"
        )
        await asyncio.sleep(delay)

        raw_key = await hub.exec.boto3.client.kms.describe_key(ctx, KeyId=resource_id)
        key = await hub.tool.aws.kms.conversion_utils.convert_raw_key_to_present_async(
            ctx, raw_resource=raw_key["ret"]["KeyMetadata"]
        )
        completed_updates = []
        for attr, value in updates.items():
            if key.get(attr) == value:
                hub.log.debug(f"aws.kms.key '{resource_id}' '{attr}' was updated.")
                completed_updates.append(attr)
        for updated_attr in completed_updates:
            updates.pop(updated_attr)
        count = count + 1

    ret["ret"] = key
    if updates:
        ret["result"] = False
        ret["comment"] += [
            f"Timed out waiting for aws.kms.key '{resource_id}' updates: {updates.keys()}"
        ]
    return ret


async def set_key_rotation(hub, ctx, resource_id: str, enable_key_rotation: bool):
    """
    Enable or disable key rotation on the KMS key

    :param hub:
    :param ctx:
    :param resource_id: resource id for the key
    :param enable_key_rotation: True to enable key rotation, if not yet enabled and False to disable
    :return:
    """
    result = dict(comment=[], result=True, ret=None)

    if ctx.get("test", False):
        operation = "Would enable" if enable_key_rotation else "Would disable"
        result["comment"] += [
            f"{operation} key rotation for aws.kms.key '{resource_id}'"
        ]
        return result

    if enable_key_rotation:
        ret = await hub.exec.boto3.client.kms.enable_key_rotation(
            ctx,
            KeyId=resource_id,
        )
    else:
        ret = await hub.exec.boto3.client.kms.disable_key_rotation(
            ctx,
            KeyId=resource_id,
        )

    if not ret["result"]:
        result["comment"] = ret["comment"]
        result["result"] = False
    else:
        operation = "Enabled" if enable_key_rotation else "Disabled"
        result["comment"] += [
            f"{operation} key rotation for aws.kms.key '{resource_id}'"
        ]

    return result
