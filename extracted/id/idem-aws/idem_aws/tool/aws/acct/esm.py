from typing import Any
from typing import Dict


async def modify(
    hub, name: str, raw_profile: Dict[str, Any], new_profile: Dict[str, Any]
):
    """
    Copy esm from the raw_profile to the new_profile
    """
    if "esm" in raw_profile:
        new_profile["esm"] = raw_profile["esm"]
