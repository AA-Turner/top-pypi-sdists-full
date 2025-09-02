"""
Helpers for bootstrapping an instance.
These are used for bootstrapping aws ec2 instances, but these functions are not unique to aws.
Eventually they can be moved to a more generic project.
"""
from typing import List


def managers(hub, sub=None, build: str = "") -> List[str]:
    """
    Find all available heist managers.
    """
    result = []

    if sub is None:
        sub = hub.heist

    # Recurse through subs
    for s in sub._subs:
        if not build:
            new_build = s
        else:
            new_build = ".".join((build, s))
        result.extend(hub.tool.heist.bootstrap.managers(sub=sub[s], build=new_build))

    # Loaded mods are the leaf nodes
    for l in sub._loaded:
        if not build:
            new_build = l
        else:
            new_build = ".".join((build, l))
        if "run" in sub[l]._funcs:
            result.append(new_build)

    return result
