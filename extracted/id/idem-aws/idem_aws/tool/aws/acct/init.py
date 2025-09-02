from typing import Any
from typing import Dict


async def modify(
    hub, name: str, raw_profile: Dict[str, Any], new_profile: Dict[str, Any]
):
    """
    Apply all the acct profile modifications in a deliberate order.
    """
    # Initialize "new_profile" with standardized keys.
    # This is the first modification that should be run
    await hub.tool.aws.acct.key_name.modify(name, raw_profile, new_profile)

    # This mod uses everything gathered so far as ctx for assuming a role, it should run after the essential mods
    await hub.tool.aws.acct.assume_role.modify(name, raw_profile, new_profile)

    # Unordered modifications
    await hub.tool.aws.acct.esm.modify(name, raw_profile, new_profile)
