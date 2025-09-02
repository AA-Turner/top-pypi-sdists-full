from typing import Any
from typing import Dict
from typing import List

STOPPED = "stopped"
RUNNING = "running"


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
    Compare the kwargs of the present function to the presentized attributes of the instance
    """
    result = True

    current_state = old_value
    desired_state = new_value

    # Get the current_state/desired state for running
    initially_running = current_state.get("running")

    # Determine the groups that attributes need to be updated with
    grouping = hub.tool.aws.ec2.instance.update.init.group(
        current_state=current_state, desired_state=desired_state, comments=comments
    )
    if not grouping:
        return False

    # Start with the attributes that work with the instance in the current running state
    # This will minimize number of shutdown/restarts as we update the instance
    if initially_running:
        first_group = grouping["needs_running"]
        second_group = grouping["needs_stopped"]
    else:
        first_group = grouping["needs_stopped"]
        second_group = grouping["needs_running"]

    # Add the attributes that don't care about the current state to the first group
    first_group.extend(grouping["needs_any"])

    # Run the first group
    result &= await hub.tool.aws.ec2.instance.update.init.apply_group(
        ctx,
        resource,
        first_group,
        update_groups=grouping["groups"],
        old_value=old_value,
        new_value=new_value,
        comments=comments,
    )

    # Stop now if we were unable to update the first group.  No need to change the instance's state
    if not result:
        return False

    # Change the state of the instance to the opposite of the starting state
    if second_group:
        if initially_running:
            ret = await hub.exec.aws.ec2.instance.stop(ctx, instance_id=resource.id)
            result &= ret.result
            if ret.comment:
                comments.append(ret.comment)
        else:
            ret = await hub.exec.aws.ec2.instance.start(ctx, instance_id=resource.id)
            result &= ret.result
            if ret.comment:
                comments.append(ret.comment)

    # Stop now if unable to toggle the running state
    if not result:
        return False

    try:
        # Return with the second group's result
        result &= await hub.tool.aws.ec2.instance.update.init.apply_group(
            ctx,
            resource,
            second_group,
            update_groups=grouping["groups"],
            old_value=old_value,
            new_value=new_value,
            comments=comments,
        )
    # If anything in the second group fails, revert the running state
    finally:
        # The running state is modified here
        # Check the current state and match it with desired state
        get = await hub.exec.aws.ec2.instance.get(ctx, resource_id=resource.id)
        current_state = get.ret
        result &= get.result
        if get.comment:
            comments.append(get.comment)

        # Stop now if we can't get current state
        if not result:
            return False

        if desired_state.get(RUNNING) and not current_state.get(RUNNING):
            ret = await hub.exec.aws.ec2.instance.start(ctx, instance_id=resource.id)
            result &= ret.result
            if ret.comment:
                comments.append(ret.comment)
        elif not desired_state.get(RUNNING) and current_state.get(RUNNING):
            ret = await hub.exec.aws.ec2.instance.stop(ctx, instance_id=resource.id)
            result &= ret.result
            if ret.comment:
                comments.append(ret.comment)

    return result


def group(
    hub,
    current_state: Dict[str, Any],
    desired_state: Dict[str, Any],
    comments: List[str],
) -> Dict[str, Any]:
    """
    Group attributes by the state the instance needs to be in for the change
    """
    update_needs_stopped = []
    update_needs_running = []
    update_needs_any = []
    update_group: Dict[str, List[str]] = {}

    # Group attributes together to determine how to do the update
    for attribute, new_attr_value in desired_state.items():
        if desired_state.get(attribute) is None:
            # There is no new value for the attribute
            continue
        if desired_state.get(attribute) == current_state.get(attribute):
            # This specific attribute is in the proper state
            continue

        # Check if this attribute is part of an update group
        # Such as updating affinity and tenancy together as "placement"
        for mod in hub.tool.aws.ec2.instance.update:
            group_ = getattr(mod, "__update_group__", [])
            if attribute in group_:
                attribute_update_group = mod.__name__
                if attribute_update_group not in update_group:
                    update_group[attribute_update_group] = []
                update_group[attribute_update_group].append(attribute)

                # Now treat the update group as the mod and attribute
                attribute = attribute_update_group
                break

        if attribute not in hub.tool.aws.ec2.instance.update:
            comments.append(f"No plugin available to modify attribute {attribute}")
            continue

        # Determine which state this group needs to be in
        mod = hub.tool.aws.ec2.instance.update[attribute]

        # Determine what state the VM needs to be in to update this attribute
        if getattr(mod, "__update_state__", None) == STOPPED:
            # This attribute can only be modified while stopped
            update_needs_stopped.append(attribute)
        elif getattr(mod, "__update_state__", None) == RUNNING:
            # This attribute can only be modified while running
            update_needs_running.append(attribute)
        else:
            # This attribute has no extra needs, add it to the first update group
            update_needs_any.append(attribute)

    return {
        "needs_stopped": update_needs_stopped,
        "needs_running": update_needs_running,
        "needs_any": update_needs_any,
        "groups": update_group,
    }


async def apply_group(
    hub,
    ctx,
    resource,
    current_group: List[str],
    *,
    update_groups: Dict[str, List[str]],
    old_value: Dict[str, Any],
    new_value: Dict[str, Any],
    comments: List[str],
) -> bool:
    """
    Apply updates to an instance based on the current group
    """
    result = True
    for attribute in current_group:
        if ctx.test:
            comments += [f"Would update aws.ec2.instance: {attribute}"]
            continue

        update_group = None
        for g in update_groups:
            if attribute in g:
                update_group = g
                break

        if update_group:
            # pass all the attributes together
            result &= await hub.tool.aws.ec2.instance.update[attribute].apply(
                ctx,
                resource,
                old_value={
                    attr: val
                    for attr, val in old_value.items()
                    if attr in update_groups[update_group]
                },
                new_value={
                    attr: val
                    for attr, val in new_value.items()
                    if attr in update_groups[update_group]
                },
                comments=comments,
            )
            if not result:
                comments.append(
                    f"Unable to update aws.ec2.instance attribute: {attribute}"
                )
                break
            continue

        # Call the appropriate tool to update each parameter that needs updating
        result &= await hub.tool.aws.ec2.instance.update[attribute].apply(
            ctx,
            resource,
            old_value=old_value.get(attribute),
            new_value=new_value.get(attribute),
            comments=comments,
        )
        if not result:
            comments.append(f"Unable to update aws.ec2.instance attribute: {attribute}")
            break
    return result
