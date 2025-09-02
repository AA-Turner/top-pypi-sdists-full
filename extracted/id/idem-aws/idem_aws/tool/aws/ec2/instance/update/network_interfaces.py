from typing import Any
from typing import Dict
from typing import List


async def apply(
    hub,
    ctx,
    resource,
    *,
    old_value: List[Dict[str, Any]],
    new_value: List[Dict[str, Any]],
    comments: List[str],
) -> bool:
    """
    Modify an ec2 instance based on a single parameter in its "present" state

    - network_interfaces:
        - network_interface_id: 'string'
          device_index: 123
          network_card_index: 123

    Args:
        hub:
        ctx: The ctx from a state module call
        resource: An ec2 instance resource object
        old_value: The previous value from the attributes of an existing instance
        new_value: The desired value from the ec2 instance present state parameters
        comments: A running list of comments abound the update process
    """
    result = True
    # attach/detach network interfaces as needed
    new_interfaces = {n.get("network_interface_id"): n for n in new_value}
    old_interfaces = {n.get("network_interface_id"): n for n in old_value}

    interfaces_to_attach = set(new_interfaces.keys()) - set(old_interfaces.keys())
    interfaces_to_delete = set(old_interfaces.keys()) - set(new_interfaces.keys())
    for network_interface_id, old_interface in old_interfaces.items():
        new_interface = new_interfaces.get(network_interface_id, {})
        if not new_interface:
            comments.append(
                f"Network Interface removed from instance: {network_interface_id}"
            )
            # Remove the interface
            interfaces_to_delete.add(network_interface_id)
        else:
            if old_interface.get("device_index") != new_interface.get(
                "device_index"
            ) and new_interface.get("device_index"):
                comments.append(
                    "Network Interface moved from device index "
                    f"{old_interface.get('device_index')} to {new_interface.get('device_index')}"
                )
                # Remove the interface and attach it to the new index
                interfaces_to_delete.add(network_interface_id)
                interfaces_to_attach.add(network_interface_id)
            if old_interface.get("network_card_index") != new_interface.get(
                "network_card_index"
            ) and new_interface.get("network_card_index"):
                comments.append(
                    "Network Interface moved from network card index "
                    f"{old_interface.get('network_card_index')} to {new_interface.get('network_card_index')}"
                )
                # Remove the interface and attach it to the new index
                interfaces_to_delete.add(network_interface_id)
                interfaces_to_attach.add(network_interface_id)

    # detach interfaces
    for network_interface_id in interfaces_to_delete:
        attachment_ret = (
            await hub.exec.boto3.client.ec2.describe_network_interface_attribtue(
                ctx, Attribute="attachment", NetworkInterfaceId=network_interface_id
            )
        )
        if not attachment_ret.result:
            comments.append(attachment_ret.comment)
            continue

        attachment = attachment_ret.ret.get("Attachment", {})

        # detach the network interface from the instance
        ret = await hub.exec.boto3.client.ec2.attach_network_interface(
            AttachmentId=attachment.get("AttachmentId")
        )
        result &= ret.result
        if not ret.result:
            comments.append(ret.comment)

    # attach interfaces
    for network_interface_id in interfaces_to_attach:
        network_interface = new_interfaces[network_interface_id]
        kwargs = {}
        if network_interface.get("device_index") is not None:
            kwargs["DeviceIndex"] = network_interface["device_index"]
        if network_interface.get("network_card_index") is not None:
            kwargs["NetworkCardIndex"] = network_interface["network_card_index"]
        ret = await hub.exec.boto3.client.ec2.attach_network_interface(
            ctx,
            NetworkInterfaceId=network_interface_id,
            InstanceId=resource.id,
            **kwargs,
        )
        result &= ret.result
        if not ret.result:
            comments.append(ret.comment)

    return result
