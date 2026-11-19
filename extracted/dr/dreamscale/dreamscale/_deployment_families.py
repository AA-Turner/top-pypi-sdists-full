"""Current client contracts and any additional deployment adapters installed by the service."""

from dreamscale_core import families as public
from dreamscale_transport import families as registered

# The released Transport registry preserves historical contracts for existing callers.
# Prefer current Core descriptors in the SDK and retain service-only adapters when installed.
_public = {family.id: family for family in public.FAMILIES}
FAMILIES = tuple(
    entry if getattr(entry, "sdk_module", None) else _public.get(entry.id, entry)
    for entry in registered.FAMILIES
)
_by_id = {entry.id: entry for entry in FAMILIES}


def family(family_id: str):
    return _by_id[family_id]
