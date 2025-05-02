from hatchling.plugin import hookimpl
from hatch_polylith_bricks.polylith.hatch.hooks.bricks import PolylithBricksHook

@hookimpl
def hatch_register_build_hook():
    return PolylithBricksHook