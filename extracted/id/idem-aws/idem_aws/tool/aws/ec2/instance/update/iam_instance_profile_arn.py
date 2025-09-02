from typing import List


async def apply(
    hub, ctx, resource, *, old_value, new_value, comments: List[str]
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
    if not old_value:
        # Associate the new iam instance profile
        ret = await hub.exec.boto3.client.ec2.associate_iam_instance_profile(
            ctx,
            InstanceId=resource.id,
            IamInstanceProfile={
                "Arn": new_value,
            },
        )
        if ret.comment:
            comments.append(ret.comment)
        return ret.result

    # Get the association id
    ret = await hub.exec.boto3.client.ec2.describe_iam_instance_profile_associations(
        ctx, Filters=[{"Name": "instance-id", "Values": [resource.id]}]
    )
    if ret.comment:
        comments.append(ret.comment)
    if not ret:
        return False

    association_id = None
    for association in ret.ret["IamInstanceProfileAssociations"]:
        if association["State"] == "associated":
            association_id = association["AssociationId"]
            break

    if not new_value:
        # disassociate the previous iam profile
        if association_id:
            ret = await hub.exec.boto3.client.ec2.disassociate_iam_instance_profile(
                ctx, AssociationId=association_id
            )
            if ret.comment:
                comments.append(ret.comment)
            return ret.result
        comments.append(f"Iam profile is already disassociated")
        return True
    else:
        # Replace the old iam instance profile with the new one
        ret = await hub.exec.boto3.client.ec2.replace_iam_instance_profile(
            ctx,
            InstanceId=resource.id,
            IamInstanceProfile=dict(Arn=new_value, AssociationId=association_id),
        )
        if ret.comment:
            comments.append(ret.comment)
        return ret.result
