import warnings
from collections.abc import Callable
from enum import Enum
from typing import TYPE_CHECKING


class RunAs(str, Enum):
    """Which identity SDK requests run as.

    - ``AUTO`` — follow the workflow's ``on_behalf_of`` flag: the executing
      user's credentials when the workflow runs on behalf of a user, the
      deployment's service credentials otherwise. Client requests require
      workflow context. This is the default policy.
    - ``DEPLOYMENT`` — always the deployment's (worker's) service identity.
    """

    AUTO = "auto"
    DEPLOYMENT = "deployment"


def _deprecated_alias_getattr(module_name: str) -> Callable[[str], type[RunAs]]:
    def __getattr__(name: str) -> type[RunAs]:
        if name != "ConnectorRunAs":
            raise AttributeError(f"module {module_name!r} has no attribute {name!r}")
        warnings.warn(
            "ConnectorRunAs is deprecated and will be removed in v4; use RunAs instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        return RunAs

    return __getattr__


if TYPE_CHECKING:
    ConnectorRunAs = RunAs
else:
    __getattr__ = _deprecated_alias_getattr(__name__)
