from typing import Dict
from typing import List


async def apply(
    hub,
    ctx,
    resource,
    *,
    old_value: List[Dict[str, str]],
    new_value: List[Dict[str, str]],
    comments: List[str],
) -> bool:
    """
    Modify an ec2 instance based on a single parameter in it's "present" state

      - block_device_mappings:
        - device_name: /dev/xvda
          volume_id : vol-0f0c6dac5d13b9dc4
          delete_on_termination: False

    Args:
        hub:
        ctx: The ctx from a state module call
        resource: An ec2 instance resource object
        old_value: The previous value from the attributes of an existing instance
        new_value: The desired value from the ec2 instance present state parameters
        comments: A running list of comments abound the update process
    """
    old_volume_attachments = {
        bdm["device_name"]: bdm for bdm in old_value if "device_name" in bdm
    }
    new_volume_attachments = {
        bdm["device_name"]: bdm for bdm in new_value if "device_name" in bdm
    }

    # If a device name is in the old mappings, but not the new, it's a volume to detach
    volumes_to_remove = set(old_volume_attachments.keys()) - set(
        new_volume_attachments.keys()
    )
    # If a device name is in the new mappings, but not the old, its a new volume to attach
    volumes_to_attach = set(new_volume_attachments.keys()) - set(
        old_volume_attachments.keys()
    )

    # If a volume exists in both places then check if the volume_id has changed
    volumes_to_move = set(old_volume_attachments.keys()).intersection(
        set(new_volume_attachments.keys())
    )
    for device_name in volumes_to_move:
        if (
            old_volume_attachments[device_name]["volume_id"]
            != new_volume_attachments[device_name]["volume_id"]
        ):
            # Detach the volume from the old location and attach it to the new location
            volumes_to_remove[device_name] = old_volume_attachments[device_name]
            volumes_to_attach[device_name] = new_volume_attachments[device_name]

    # Allow moving the root device, but not detaching it without putting something else in its place
    if (
        resource.root_device_name in volumes_to_remove
        and resource.root_device_name not in volumes_to_attach
    ):
        volumes_to_remove.remove(resource.root_device_name)

    # Detach old volumes
    for device_name in volumes_to_remove:
        volume_id = old_volume_attachments[device_name]["volume_id"]
        ret = await hub.exec.boto3.client.ec2.detach_volume(
            ctx,
            Device=device_name,
            InstanceId=resource.id,
            VolumeId=volume_id,
            Force=True,
        )
        if ret.comment:
            comments.append(ret.comment)
        if not ret.result:
            comments.append(f"Could not detach volume: {volume_id} from instance")
            return False

    # Attach new volumes
    for device_name in volumes_to_attach:
        volume_id = new_volume_attachments[device_name]["volume_id"]
        ret = await hub.exec.boto3.client.ec2.attach_volume(
            ctx, Device=device_name, InstanceId=resource.id, VolumeId=volume_id
        )
        if ret.comment:
            comments.append(ret.comment)
        if not ret.result:
            comments.append(f"Could not attach volume: {volume_id} to instance")
            return False

    # modify attachment attributes as needed
    block_device_mappings = list()
    for device_name in new_volume_attachments:
        old_bdm = old_volume_attachments.get(device_name)
        new_bdm = new_volume_attachments[device_name]

        if new_bdm != old_bdm:
            new_bdm_attachment = dict(
                DeviceName=new_bdm["device_name"],
                Ebs=dict(
                    DeleteOnTermination=new_bdm.get("delete_on_termination", True),
                    VolumeId=new_bdm["volume_id"],
                ),
            )
            block_device_mappings.append(new_bdm_attachment)

        if block_device_mappings:
            response = resource.modify_attribute(
                BlockDeviceMappings=block_device_mappings
            )
            if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
                comments.append(
                    f"Unable to set delete_on_termination for volume: {device_name}"
                )
                return False
    return True
