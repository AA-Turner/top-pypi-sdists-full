from enum import (
    Enum,
)
from os import (
    environ,
)

from fa_purity import (
    Cmd,
)


class Envs(Enum):
    PROD = "production"
    DEV = "development"


def current_app_env() -> Cmd[Envs]:
    def _action() -> Envs:
        return Envs(environ.get("OBSERVES_ENV", "production"))

    return Cmd.wrap_impure(_action)


def observes_debug() -> Cmd[bool]:
    def _action() -> bool:
        _debug = environ.get("OBSERVES_DEBUG", "")
        return _debug.lower() == "true"

    return Cmd.wrap_impure(_action)
