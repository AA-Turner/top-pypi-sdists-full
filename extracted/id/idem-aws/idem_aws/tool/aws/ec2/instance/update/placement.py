from typing import Any
from typing import Dict
from typing import List

# Update all these attributes together
__update_group__ = [
    "affinity",
    "host_id",
    "tenancy",
    "group_name",
    "partition_number",
    "host_resource_group_arn",
]
__update_state__ = "stopped"


async def apply(
    hub,
    ctx,
    resource,
    *,
    old_value: Dict[str, Any],
    new_value: Dict[str, Any],
    comments: List[str],
) -> bool:
    """
    Modify an ec2 instance based on a single parameter in it's "present" state

    Args:
        hub:
        ctx: The ctx from a state module call
        resource: An ec2 instance resource object
        old_value: The previous value from the attributes of an existing instance
        new_value: The desired value from the ec2 instance present state parameters
        comments: A running list of comments abound the update process
    """
    result = True

    group_name = new_value.get("group_name")
    if "group_name" in old_value and not new_value.get("group_name"):
        # An empty string removes the instance from the placement group
        group_name = ""

    # Modify the placement
    ret = await hub.exec.boto3.client.ec2.modify_instance_placement(
        ctx,
        InstanceId=resource.id,
        Affinity=new_value.get("affinity"),
        GroupName=group_name,
        HostId=new_value.get("host_id"),
        Tenancy=new_value.get("tenancy"),
        PartitionNumber=new_value.get("partition_number"),
        HostResourceGroupArn=new_value.get("host_resource_group_arn"),
    )
    if ret.comment:
        comments.append(ret.comment)
    result &= ret.result

    return result
