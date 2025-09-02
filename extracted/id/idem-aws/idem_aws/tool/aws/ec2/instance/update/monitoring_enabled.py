from typing import List


async def apply(
    hub, ctx, resource, *, old_value: bool, new_value: bool, comments: List[str]
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
    if new_value:
        # Start monitoring the instance
        ret = await hub.exec.boto3.client.ec2.monitor_instances(
            ctx, InstanceIds=[resource.id]
        )
        if ret.comment:
            comments.append(ret.comment)

        await hub.pop.loop.sleep(1)

        return ret.result
    else:
        # Stop monitoring the instance
        ret = await hub.exec.boto3.client.ec2.unmonitor_instances(
            ctx, InstanceIds=[resource.id]
        )

        if ret.comment:
            comments.append(ret.comment)

        return ret.result
