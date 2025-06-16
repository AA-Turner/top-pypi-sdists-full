import logging
import os
from contextlib import suppress
from typing import Any, Dict, Final, Optional, Type, TypeVar

from typed_envs import registry
from typed_envs._env_var import EnvironmentVariable
from typed_envs.registry import _register_new_env
from typed_envs.typing import StringConverter, VarName


T = TypeVar("T")


class EnvVarFactory:
    """Factory for creating :class:`EnvironmentVariable` instances with optional prefix."""

    def __init__(self, env_var_prefix: Optional[str] = None) -> None:
        """
        Initializes the :class:`EnvVarFactory` with an optional prefix for environment variables.

        Args:
            env_var_prefix: An optional string prefix to be added to environment variable names.
        """
        self.prefix: Final = env_var_prefix
        self.__use_prefix: Final = env_var_prefix is not None
        self.__default_string_converters: Final[Dict[Type, StringConverter]] = {}

    @property
    def default_string_converters(self) -> Dict[Type, StringConverter]:
        return self.__default_string_converters.copy()

    @property
    def use_prefix(self) -> bool:
        return self.__use_prefix

    def create_env(
        self,
        env_var_name: str,
        env_var_type: Type[T],
        default: Any,
        *init_args,
        string_converter: Optional[StringConverter] = None,
        verbose: bool = True,
        **init_kwargs: Any,
    ) -> "EnvironmentVariable[T]":
        """
        Creates a new :class:`EnvironmentVariable` object with the specified parameters.

        Args:
            env_var_name: The name of the environment variable.
            env_var_type: The type of the environment variable.
            default: The default value for the environment variable.
            *init_args: Additional positional arguments for initialization.
            string_converter: An optional callable to convert the string value from the environment.
            verbose: If True, logs the environment variable details.
            **init_kwargs: Additional keyword arguments for initialization.

        Returns:
            An instance of :class:`EnvironmentVariable` with the specified type and value.

        Example:
            Create an environment variable with an integer type using an `EnvVarFactory` instance:

            ```python
            from typed_envs.factory import EnvVarFactory
            factory = EnvVarFactory()
            some_var = factory.create_env("SET_WITH_THIS_ENV", int, 10)

            >>> isinstance(some_var, int)
            True
            >>> isinstance(some_var, EnvironmentVariable)
            True
            ```

            Differences between `some_var` and `int(10)`:
            - `some_var` will type check as both `int` and :class:`EnvironmentVariable`.
            - `some_var.__repr__()` includes contextual information about the :class:`EnvironmentVariable`.

            ```python
            >>> some_var
            <EnvironmentVariable[name=`SET_WITH_THIS_ENV`, type=int, default_value=10, current_value=10, using_default=True]>
            >>> str(some_var)
            "10"
            >>> some_var + 5
            15
            >>> 20 / some_var
            2
            ```

        See Also:
            - :func:`typed_envs.create_env` for creating environment variables without a prefix.
        """
        # Validate name
        if not isinstance(env_var_name, str):
            raise TypeError("env_var_name must be string, not {env_var_name}")

        if not env_var_name:
            raise ValueError("env_var_name must not be empty")

        # Get full name
        if self.__use_prefix:
            full_name = VarName(f"{self.prefix}_{env_var_name}")
        else:
            full_name = VarName(env_var_name)

        # Get value
        var_value = os.environ.get(full_name)
        using_default = var_value is None
        var_value = var_value or default
        if env_var_type is bool:
            if isinstance(var_value, str) and var_value.lower() == "false":
                var_value = False
            else:
                with suppress(ValueError):
                    # if var_value is "0" or "1"
                    var_value = int(var_value)
                var_value = bool(var_value)
        if any(iter_typ in env_var_type.__bases__ for iter_typ in [list, tuple, set]):
            var_value = var_value.split(",")

        # Convert value, if applicable
        if string_converter is None:
            string_converter = self.__default_string_converters.get(env_var_type)
        if string_converter is not None and not (
            using_default and isinstance(default, env_var_type)
        ):
            var_value = string_converter(var_value)

        # Create environment variable
        instance = EnvironmentVariable[env_var_type](  # type: ignore [valid-type]
            var_value, *init_args, **init_kwargs
        )
        # Set additional attributes
        instance._init_arg0 = var_value
        instance._env_name = full_name
        instance._default_value = default
        instance._using_default = using_default

        # Finish up
        if verbose:
            # This code prints envs on script startup for convenience of your users.
            try:
                logger.info(instance.__repr__())
            except RecursionError:
                logger.debug(
                    "unable to properly display your `%s` %s env due to RecursionError",
                    full_name,
                    instance.__class__.__base__,
                )
                with suppress(RecursionError):
                    logger.debug(
                        "Here is your `%s` env in string form: %s",
                        full_name,
                        str(instance),
                    )
        _register_new_env(full_name, instance)
        return instance

    def register_string_converter(
        self, register_for: Type, converter: StringConverter
    ) -> None:
        if register_for in self.__default_string_converters:
            raise ValueError(
                f"There is already a string converter registered for {register_for}"
            )
        elif not callable(converter):
            raise ValueError("converter must be callable")
        self.__default_string_converters[register_for] = converter


# NOTE: While we create the TYPEDENVS_SHUTUP object in the ENVIRONMENT_VARIABLES file as an example,
#       we cannot use it here without creating a circular import.

logger: Final[logging.Logger] = logging.getLogger("typed_envs")

from typed_envs import ENVIRONMENT_VARIABLES

if ENVIRONMENT_VARIABLES.SHUTUP:
    logger.disabled = True
else:
    if not logger.hasHandlers():
        logger.addHandler(logging.StreamHandler())
    if not logger.isEnabledFor(logging.INFO):
        logger.setLevel(logging.INFO)


default_factory: Final[EnvVarFactory] = EnvVarFactory()
