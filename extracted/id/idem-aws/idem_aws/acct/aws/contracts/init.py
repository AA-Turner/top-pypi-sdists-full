from typing import Any
from typing import Dict


def sig_gather(hub, profiles) -> Dict[str, Any]:
    ...


async def post_gather(hub, ctx) -> Dict[str, Any]:
    """
    This function is called after any "idem_aws.acct.aws.*.gather" function.
    Modifications to profiles should happen in plugins located in "idem_aws.tool.aws.acct".
    Modifications to profiles should NOT occur explicitly in this function.
    """
    profiles = ctx.ret or {}

    hub.log.info(f"Read {len(profiles)} profiles from {ctx.ref}")

    for name, raw_profile in profiles.items():
        new_profile = {}
        # Apply modifications to the new_profile before using it
        await hub.tool.aws.acct.key_name.modify(name, raw_profile, new_profile)
        # Log whether this is a new profile or if the mods are overwriting an existing profile
        if name in profiles:
            hub.log.debug(f"Modified profile '{name}' for the current run")
        else:
            hub.log.debug(f"Created new profile '{name}'")

        # Add the fully modified profile to all the profiles
        profiles[name] = new_profile

    return profiles
