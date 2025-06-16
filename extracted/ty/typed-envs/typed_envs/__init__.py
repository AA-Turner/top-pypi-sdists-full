from typing import Any, Optional, Type, TypeVar

from typed_envs._env_var import EnvironmentVariable
from typed_envs.factory import EnvVarFactory, logger, default_factory
from typed_envs.registry import (
    ENVIRONMENT,
    _ENVIRONMENT_VARIABLES_SET_BY_USER,
    _ENVIRONMENT_VARIABLES_USING_DEFAULTS,
)
from typed_envs.typing import StringConverter


description = """\
typed_envs is used to create specialized `EnvironmentVariable` objects that behave exactly the same as any other instance of the `typ` used to create them.

typed_envs is used for:
    - defining your envs in a readable, user friendly way
    - enhancing type hints for the returned instances
    - enhancing __repr__ of the returned instance with extra contextual information
"""

description_addon = """\

In the example below, `some_var` can be used just like as any other `int` object.

```
import typed_envs
some_var = typed_envs.create_env("SET_WITH_THIS_ENV", int, 10)
>>> isinstance(some_var, int)
True
>>> isinstance(some_var, EnvironmentVariable)
True
```

There are only 2 differences between `some_var` and `int(10)`:
    - `some_var` will properly type check as an instance of both `int` and `EnvironmentVariable`
    - `some_var.__repr__()` will include contextual information about the `EnvironmentVariable`.

```
>>> some_var
<EnvironmentVariable[name=`SET_WITH_THIS_ENV`, type=int, default_value=10, current_value=10, using_default=True]>
>>> str(some_var)
"10"
>>> some_var + 5
15
>>> 20 / some_var
2
```

"""

T = TypeVar("T")


def create_env(
    name: str,
    typ: Type[T],
    default: Any,
    *init_args,
    string_converter: Optional[StringConverter] = None,
    verbose: bool = True,
    **init_kwargs
) -> "EnvironmentVariable[T]":
    """
    Returns a new :class:`EnvironmentVariable` object with no prefix specified.

    Functionally, :class:`EnvironmentVariable` objects will work exactly the same as any instance of specified `typ`.

    Args:
        name: The name of the environment variable.
        typ: The type of the environment variable. This determines the type of the value that the environment variable will hold.
        default: The default value for the environment variable if not specified in the current environment.
        *init_args: Additional positional arguments for initialization of the environment variable.
        string_converter: An optional callable to convert the string value from the environment.
        verbose: If True, logs the environment variable details for debugging and informational purposes.
        **init_kwargs: Additional keyword arguments for initialization of the environment variable.

    Examples:
        In the example below, `some_var` can be used just like any other `int` object.

        >>> import typed_envs
        >>> some_var = typed_envs.create_env("SET_WITH_THIS_ENV", int, 10)
        >>> isinstance(some_var, int)
        True
        >>> isinstance(some_var, EnvironmentVariable)
        True

        There are only 2 differences between `some_var` and `int(10)`:
        - `some_var` will properly type check as an instance of both `int` and :class:`EnvironmentVariable`
        - `some_var.__repr__()` will include contextual information about the :class:`EnvironmentVariable`.

        >>> some_var
        <EnvironmentVariable[name=`SET_WITH_THIS_ENV`, type=int, default_value=10, current_value=10, using_default=True]>
        >>> str(some_var)
        "10"
        >>> some_var + 5
        15
        >>> 20 / some_var
        2

    See Also:
        :class:`EnvVarFactory` for creating environment variables with a prefix.
    """
    return default_factory.create_env(
        name,
        typ,
        default,
        *init_args,
        string_converter=string_converter,
        verbose=verbose,
        **init_kwargs
    )


__all__ = [
    "create_env",
    "EnvVarFactory",
    "ENVIRONMENT",
    "_ENVIRONMENT_VARIABLES_SET_BY_USER",
    "_ENVIRONMENT_VARIABLES_USING_DEFAULTS",
]

# Just putting these here so I don't accidentally remove the 'unused' import
EnvironmentVariable
logger
