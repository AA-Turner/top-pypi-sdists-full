"""
This module demonstrates the creation of environment variables using the
:class:`~typed_envs.factory.EnvVarFactory` class with a specified prefix.
"""

from typing import TYPE_CHECKING, Final

from typed_envs.factory import EnvVarFactory

if TYPE_CHECKING:
    from typed_envs._env_var import EnvironmentVariable


_factory: Final[EnvVarFactory] = EnvVarFactory("TYPEDENVS")
"""The :class:`~typed_envs.factory.EnvVarFactory` is initialized with the
prefix "TYPEDENVS", which is automatically added to the environment variable
names created by this factory.
"""

SHUTUP: Final["EnvironmentVariable[bool]"] = _factory.create_env(
    "SHUTUP", bool, False, verbose=False
)
"""An environment variable named "TYPEDENVS_SHUTUP" of type :class:`bool`.
It defaults to `False` if not set in the environment. If the environment
variable is set to any non-empty string, it will be interpreted as `True`.

Examples:
    To access the `SHUTUP` environment variable, you can use it as a regular
    boolean:

    >>> from typed_envs.ENVIRONMENT_VARIABLES import SHUTUP
    >>> isinstance(SHUTUP, bool)
    True
    >>> SHUTUP
    <EnvironmentVariable[name=`TYPEDENVS_SHUTUP`, type=bool, default_value=False, current_value=False, using_default=True]>

    If you set the environment variable `TYPEDENVS_SHUTUP` to a non-empty
    string, it will be interpreted as `True`:

    >>> import os
    >>> os.environ['TYPEDENVS_SHUTUP'] = '1'
    >>> from typed_envs.ENVIRONMENT_VARIABLES import SHUTUP
    >>> SHUTUP
    <EnvironmentVariable[name=`TYPEDENVS_SHUTUP`, type=bool, default_value=False, current_value=True, using_default=False]>

See Also:
    - :class:`~typed_envs.factory.EnvVarFactory` for creating environment
      variables with custom prefixes.
    - :class:`~typed_envs._env_var.EnvironmentVariable` for details on how
      environment variables are represented and used.
"""
