from typing import Final

from typed_envs._env_var import EnvironmentVariable
from typed_envs.typing import EnvRegistry, VarName


ENVIRONMENT: Final[EnvRegistry] = EnvRegistry({})
_ENVIRONMENT_VARIABLES_SET_BY_USER: Final[EnvRegistry] = EnvRegistry({})
_ENVIRONMENT_VARIABLES_USING_DEFAULTS: Final[EnvRegistry] = EnvRegistry({})


def _register_new_env(name: VarName, instance: EnvironmentVariable) -> None:
    ENVIRONMENT[name] = instance
    if instance._using_default:
        _ENVIRONMENT_VARIABLES_USING_DEFAULTS[name] = instance
    else:
        _ENVIRONMENT_VARIABLES_SET_BY_USER[name] = instance


__all__ = [
    "ENVIRONMENT",
    "_ENVIRONMENT_VARIABLES_SET_BY_USER",
    "_ENVIRONMENT_VARIABLES_USING_DEFAULTS",
]
