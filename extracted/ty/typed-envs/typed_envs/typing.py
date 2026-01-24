from typing import TYPE_CHECKING, Any, Callable, NewType

if TYPE_CHECKING:
    from typed_envs._env_var import EnvironmentVariable  # noqa


VarName = NewType("VarName", str)
VarValue = NewType("VarValue", str)

EnvRegistry = NewType("EnvRegistry", dict[VarName, "EnvironmentVariable[Any]"])

StringConverter = Callable[[str], Any]
