from typing import TYPE_CHECKING, Any, Callable, Dict, NewType

if TYPE_CHECKING:
    from typed_envs._env_var import EnvironmentVariable


VarName = NewType("VarName", str)
VarValue = NewType("VarValue", str)

EnvRegistry = NewType("EnvRegistry", Dict[VarName, "EnvironmentVariable"])

StringConverter = Callable[[str], Any]
