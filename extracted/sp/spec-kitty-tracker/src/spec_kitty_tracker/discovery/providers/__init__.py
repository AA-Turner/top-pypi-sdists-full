# Built-in provider discovery modules.
# Each module self-registers its workspace/resource discoverers on import.
# Add new provider imports here as they are implemented.

from spec_kitty_tracker.discovery.providers import github as _github  # noqa: F401
from spec_kitty_tracker.discovery.providers import gitlab as _gitlab  # noqa: F401
from spec_kitty_tracker.discovery.providers import jira as _jira  # noqa: F401
from spec_kitty_tracker.discovery.providers import linear as _linear  # noqa: F401
