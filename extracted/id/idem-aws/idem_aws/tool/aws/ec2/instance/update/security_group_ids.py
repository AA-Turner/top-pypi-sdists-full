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

    Args:
        resource: An ec2 instance resource object
        old_value: The previous value from the attributes of an existing instance
        new_value: The desired value from the ec2 instance present state parameters
        comments: A running list of comments abound the update process

    Example:
        - security_group_ids:
          - sg-0839b8c0df83f79f4
          - sg-0c8313e7fd3d8e48b
    """
    if old_value == new_value:
        return True

    ret = await hub.exec.boto3.client.ec2.modify_instance_attribute(
        ctx,
        InstanceId=resource.id,
        Groups=new_value,
    )
    if not ret.result:
        comments.append(ret.comment)

    return ret.result
