"""
Utilities for generating Click options.
"""

import re
from collections.abc import Callable, Collection, Iterable, Mapping, Sequence
from datetime import date, datetime, timedelta
from enum import Enum
from functools import partial, update_wrapper
from pathlib import Path
from typing import (
    Any,
    Protocol,
    TypeVar,
    cast,
    get_args,
    get_origin,
    overload,
)

import click
from click.core import ParameterSource

from . import _core, cls_utils, converters
from ._compat import PY_311
from .cli_utils import (
    NO_DEFAULT,
    Default,
    DefaultFactorySentinel,
    StrDict,
    TypeArgsMaker,
    TypeHandlerFunc,
    get_default,
)
from .constants import CLICK_METADATA_KEY as METADATA_KEY
from .converters import Converter, default_converter
from .loaders import EnvLoader, Loader
from .processors import Processor
from .types import (
    SECRET_REPR,
    ST,
    LoadedValue,
    LoaderMeta,
    MergedSettings,
    OptionInfo,
    OptionList,
    Secret,
    SecretStr,
    SettingsClass,
)


if PY_311:
    from enum import IntEnum, StrEnum
else:
    IntEnum = StrEnum = None  # type: ignore


__all__ = [
    "DEFAULT_TYPES",
    "ClickHandler",
    "ClickOptionFactory",
    "DecoratorFactory",
    "F",
    "OptionGroupFactory",
    "click_options",
    "handle_datetime",
    "handle_enum",
    "handle_enum_by_name",
    "handle_enum_by_value",
    "handle_pattern",
    "handle_secret",
    "pass_settings",
]


CTX_KEY = "settings"


Callback = Callable[[click.Context, click.Option, Any], Any]
F = TypeVar("F", bound=Callable[..., Any])
"""TypeVar for arbitrary functions."""
Decorator = Callable[[F], F]


def click_options(
    settings_cls: type[ST],
    loaders: str | Sequence[Loader],
    *,
    processors: Sequence[Processor] = (),
    converter: Converter | None = None,
    base_dir: Path = Path(),
    type_args_maker: TypeArgsMaker | None = None,
    argname: str | None = None,
    decorator_factory: "DecoratorFactory | None" = None,
    show_envvars_in_help: bool = False,
    reload_settings_on_invoke: bool = False,
) -> Callable[[F], F]:
    r"""
    **Decorator:** Generate :program:`Click` options for a CLI which override
    settings loaded via :func:`.load_settings()`.

    Args:
        settings_cls: The settings class to generate options for.

        loaders: Either a string with your app name or a list of
            :class:`.Loader`\ s.  If it's a string, use it with
            :func:`~typed_settings.default_loaders()` to get the default
            loaders.

        processors: A list of settings :class:`.Processor`'s.

        converter: An optional :class:`.Converter` used for converting
            option values to the required type.

            By default, :data:`typed_settings.default_converter()` is used.

        base_dir: Base directory for resolving relative paths in default option values.

        type_args_maker: The type args maker that is used to generate keyword
            arguments for :func:`click.option()`.  By default, use
            :class:`.TypeArgsMaker` with :class:`ClickHandler`.

        argname: An optional argument name for the settings instance that is
            passed to the CLI.  If it is set, the settings instances is no
            longer passed as positional argument but as key word argument.

            This allows a CLI function to be decorated with this function
            multiple times.

        decorator_factory: A class that generates Click decorators for options
            and settings classes.  This allows you to, e.g., use
            `option groups`_ via :class:`OptionGroupFactory`.  The default
            generates normal Click options via :class:`ClickOptionFactory`.

            .. _option groups: https://click-option-group.readthedocs.io

        show_envvars_in_help: If ``True`` and if the
            :class:`~typed_settings.loaders.EnvLoader` is being used, show the
            names of the environment variable a value is loaded from.

        reload_settings_on_invoke: By default, the default values will be loaded (from
            config files and env vars) when the CLI is created.  If you set this to
            ``True``, the defaults are reloaded when the CLI is invoked.  This makes
            running the CLI slower but can improve testability, because you can change
            the values of env vars in tests without needing to create a new CLI
            function.

    Return:
        A decorator for a click command.

    Raise:
        InvalidSettingsError: If an instance of *cls* cannot be created for the given
            settings.

    Example:
        .. code-block:: python

           import click
           import typed_settings as ts

           @ts.settings
           class Settings: ...

           @click.command()
           @ts.click_options(Settings, "example")
           def cli(settings: Settings) -> None:
               print(settings)

    .. versionchanged:: 1.0.0
       Instead of a list of loaders, you can also just pass an application
       name.
    .. versionchanged:: 1.1.0
       Added the *argname* parameter.
    .. versionchanged:: 1.1.0
       Added the *decorator_factory* parameter.
    .. versionchanged:: 2.0.0
       Renamed *type_handler* to *type_args_maker* and changed it's type to
       ``TypeArgsMaker``.
    .. versionchanged:: 23.0.0
       Made *converter*, *type_args_maker*, *argname*, and *decorator_factory*
       a keyword-only argument
    .. versionchanged:: 23.0.0
       Added the *processors* argument
    .. versionchanged:: 23.1.0
       Added the *base_dir* argument
    .. versionchanged:: 24.5.0
       Added the *reload_settings_on_invoke* argument
    """
    if isinstance(loaders, str):
        loaders = _core.default_loaders(loaders)

    env_loader: EnvLoader | None = None
    if show_envvars_in_help:
        _loaders = [ldr for ldr in loaders if isinstance(ldr, EnvLoader)]
        if _loaders:
            env_loader = _loaders[-1]

    converter = converter or default_converter()
    state = _core.SettingsState(settings_cls, loaders, processors, converter, base_dir)
    grouped_options = cls_utils.group_options(state.settings_class, state.options)
    type_args_maker = type_args_maker or TypeArgsMaker(ClickHandler())
    decorator_factory = decorator_factory or ClickOptionFactory()

    ts_decorator = _get_ts_decorator(
        state,
        grouped_options,
        type_args_maker,
        argname,
        decorator_factory,
        env_loader,
        reload_settings_on_invoke=reload_settings_on_invoke,
    )
    return ts_decorator


def _get_ts_decorator(  # noqa: C901
    state: _core.SettingsState[ST],
    grouped_options: list[tuple[type, OptionList]],
    type_args_maker: TypeArgsMaker,
    argname: str | None,
    decorator_factory: "DecoratorFactory",
    env_loader: EnvLoader | None,
    reload_settings_on_invoke: bool,
) -> Callable[[F], F]:
    """
    Return a wrapper function that decorates the wrapped function with the Click
    decorators.
    """

    def _load_cli_settings(
        ctx: click.Context, initial_default_settings: dict[str, LoadedValue]
    ) -> ST:
        """
        Load settings for loaders, update them with CLI args and return the settings
        cls.
        """
        if reload_settings_on_invoke:
            default_settings = _core._load_settings(state)
        else:
            default_settings = initial_default_settings
        meta = LoaderMeta("Command line args")
        cli_options = ctx.obj.get(CTX_KEY, {})
        cli_settings: MergedSettings = {}
        for option in state.options:
            path = option.path
            if path in cli_options:  # pragma: no cover
                # "path" *should* always be in "cli_options", b/c we *currently*
                # generate CLI options for all options.  But let's stay safe here
                # in case the behavior changes in the future.
                cli_settings[path] = LoadedValue(cli_options[path], meta)
            elif path in default_settings:
                cli_settings[path] = default_settings[path]
            # else:
            #     This is the case, when the default should be used and it is a
            #     factory function.  The _DefaultsLoader did not invoke it yet.
        settings = _core.convert(cli_settings, state)
        return settings

    def _add_option_decorators(
        wrapped_f: F,
        state: _core.SettingsState[ST],
        initial_default_settings: dict[str, LoadedValue],
    ) -> F:
        """
        Generate "click.option()" decorators and decorate the *wrapped_f* with them.
        """
        option_decorator = decorator_factory.get_option_decorator()
        for g_cls, g_opts in reversed(grouped_options):
            for oinfo in reversed(g_opts):
                default = get_default(oinfo, initial_default_settings, state.converter)
                envvar = env_loader.get_envvar(oinfo) if env_loader else None
                option = _mk_option(
                    option_decorator,  # type: ignore[arg-type]
                    oinfo,
                    default,
                    type_args_maker,
                    envvar,
                )
                wrapped_f = option(wrapped_f)  # type: ignore[assignment,arg-type]
            wrapped_f = decorator_factory.get_group_decorator(g_cls)(
                wrapped_f  # type: ignore[arg-type]
            )
        return wrapped_f

    def ts_decorator(orig_f: F) -> F:
        """
        The wrapper that actually decorates a function with all options.
        """
        # If "reload_settings_on_invoke" is True, these initial default settings will
        # be reloaded on each invocation.  The help texts remain unchanged, though.
        initial_default_settings = _core._load_settings(state)

        # Create a *cls* instances from the settings dict stored in
        # :attr:`click.Context.obj` and passes it to the decorated function *orig_f*.
        # def new_func(*args: "P.args", **kwargs: "P.kwargs") -> "R":
        def new_func(*args: Any, **kwargs: Any) -> Any:
            ctx = click.get_current_context()
            if ctx.obj is None:
                ctx.obj = {}
            elif not isinstance(ctx.obj, dict):
                raise RuntimeError(
                    f"'ctx.obj' must be a dict when you use Typed Settings, got: "
                    f"{type(ctx.obj).__name__}"
                )

            # Load settings and determine how to pass them to "orig_f()"
            settings = _load_cli_settings(ctx, initial_default_settings)
            if argname:
                ctx_key = argname
                kwargs = {argname: settings, **kwargs}  # type: ignore
            else:
                ctx_key = CTX_KEY
                args = (settings, *args)  # type: ignore

            ctx.obj[ctx_key] = settings

            return orig_f(*args, **kwargs)

        wrapped_f = cast(F, update_wrapper(new_func, orig_f))
        wrapped_f = _add_option_decorators(wrapped_f, state, initial_default_settings)
        return wrapped_f

    return ts_decorator


@overload
def pass_settings(f: None = None, *, argname: str | None = ...) -> Callable[[F], F]: ...


@overload
def pass_settings(f: F, *, argname: str | None = ...) -> F: ...


def pass_settings(
    f: F | None = None,
    *,
    argname: str | None = None,
) -> F | Callable[[F], F]:
    """
    **Decorator:** Mark a callback as wanting to receive the innermost settings
    instance as first argument.

    If you specify an *argname* in :func:`click_options()`, you must specify
    the same name here in order to get the correct settings instance.  The
    settings instance is then passed as keyword argument.

    Args:
        f: If this decorator is applied without any arguments, this is the to be
            decrorated function.  If you pass any keyword arguments, this is ``None``.
        argname: An optional argument name.  If it is set, the settings
            instance is no longer passed as positional argument but as key
            word argument.

    Return:
        A decorator for a click command.

    Example:
        .. code-block:: python

           import click
           import typed_settings as ts

           @ts.settings
           class Settings: ...

           @click.group()
           @click_options(Settings, "example", argname="my_settings")
           def cli(my_settings):
               pass

           @cli.command()
           # Use the same "argname" as above!
           @pass_settings(argname="my_settings")
           def sub_cmd(*, my_settings):
               print(my_settings)

    .. versionchanged:: 1.1.0
       Add the *argname* parameter.
    """
    ctx_key = argname or CTX_KEY

    def decorator(f: F) -> F:
        def new_func(*args: Any, **kwargs: Any) -> Any:
            ctx = click.get_current_context()
            node: click.Context | None = ctx
            settings = None
            while node is not None:
                if isinstance(node.obj, dict) and ctx_key in node.obj:
                    settings = node.obj[ctx_key]
                    break
                node = node.parent

            if argname:
                kwargs = {argname: settings, **kwargs}
            else:
                args = (settings, *args)

            return ctx.invoke(f, *args, **kwargs)

        return cast(F, update_wrapper(new_func, f))

    if f is None:
        return decorator

    return decorator(f)


class TSOption(click.Option):
    def value_from_envvar(self, ctx: click.Context) -> Any | None:
        return None


class DecoratorFactory(Protocol):
    """
    **Protocol:** Methods that a Click decorator factory must implement.

    The decorators returned by the procol methods are used to construct the
    Click options and possibly option groups.

    .. versionadded:: 1.1.0
    """

    def get_option_decorator(self) -> Callable[..., Decorator[F]]:
        """
        Return the decorator that is used for creating Click options.

        It must be compatible with :func:`click.option()`.
        """
        ...

    def get_group_decorator(self, settings_cls: type) -> Decorator[F]:
        """
        Return a decorator for the current settings class.

        This can, e.g., be used to group option by settings class.
        """
        ...


class ClickOptionFactory:
    """
    Factory for default Click decorators.
    """

    def get_option_decorator(self) -> Callable[..., Decorator[F]]:
        """
        Return :func:`click.option()`.
        """
        return partial(click.option, cls=TSOption)

    def get_group_decorator(self, settings_cls: SettingsClass) -> Decorator[F]:
        """
        Return a no-op decorator that leaves the decorated function unchanged.
        """
        return lambda f: f


class OptionGroupFactory:
    """
    Factory got generating Click option groups via
    https://click-option-group.readthedocs.io.
    """

    def __init__(self) -> None:
        try:
            from click_option_group import GroupedOption, optgroup
        except ImportError as e:
            raise ModuleNotFoundError(
                "Module 'click_option_group' not installed.  Please run "
                "'python -m pip install -U typed-settings[option-groups]'"
            ) from e
        self.optgroup = optgroup

        class TSGroupedOption(GroupedOption):
            def value_from_envvar(self, ctx: click.Context) -> Any | None:
                return None

        self.opt_cls = TSGroupedOption

    def get_option_decorator(self) -> Callable[..., Decorator[F]]:
        """
        Return :class:`click_option_group.optgroup` option.
        """
        return partial(self.optgroup.option, cls=self.opt_cls)

    def get_group_decorator(self, settings_cls: SettingsClass) -> Decorator[F]:
        """
        Return a :class:`click_option_group.optgroup` group instantiated with
        the first line of *settings_cls*'s docstring.
        """
        try:
            name = settings_cls.__doc__.strip().splitlines()[0]  # type: ignore
        except (AttributeError, IndexError):
            name = f"{settings_cls.__name__} options"
        return cast(Decorator[F], self.optgroup.group(name))


def handle_datetime(typ: type, default: Default, is_optional: bool) -> StrDict:
    """
    Use :class:`click.DateTime` as option type and convert the default value
    to an ISO string.
    """
    kwargs: StrDict = {
        "type": click.DateTime(
            ["%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M:%S%z"]
        ),
    }
    if isinstance(default, datetime):
        kwargs["default"] = default.isoformat()
    elif is_optional:
        kwargs["default"] = None
    return kwargs


def handle_date(typ: type, default: Default, is_optional: bool) -> StrDict:
    """
    Use :class:`click.DateTime` as option type and convert the default value
    to an ISO string.
    """
    cli_typ = partial(converters.to_date, cls=date)
    cli_typ.__name__ = converters.to_date.__name__  # type: ignore[attr-defined]
    kwargs: StrDict = {
        "type": cli_typ,
        "metavar": "[%Y-%m-%d]",
    }
    if isinstance(default, date):
        kwargs["default"] = default.isoformat()
    elif is_optional:
        kwargs["default"] = None
    return kwargs


def handle_timedelta(typ: type, default: Default, is_optional: bool) -> StrDict:
    """
    Use :class:`click.DateTime` as option type and convert the default value
    to an ISO string.
    """
    cli_typ = partial(converters.to_timedelta, cls=timedelta)
    cli_typ.__name__ = converters.to_timedelta.__name__  # type: ignore[attr-defined]
    kwargs: StrDict = {
        "type": cli_typ,
        "metavar": "[-][Dd][HHh][MMm][SS[.ffffff]s]",
    }
    if isinstance(default, timedelta):
        kwargs["default"] = converters.timedelta_to_str(default)
    elif is_optional:
        kwargs["default"] = None
    return kwargs


def handle_enum_by_name(
    typ: type[Enum], default: Default, is_optional: bool
) -> StrDict:
    """
    Use :class:`click.Choice` as option type and use the enum value's name as
    default.
    """
    kwargs: StrDict = {"type": click.Choice([str(k) for k in typ.__members__])}
    if isinstance(default, typ):
        # Convert Enum instance to string
        kwargs["default"] = default.name
    elif is_optional:
        kwargs["default"] = None

    return kwargs


handle_enum = handle_enum_by_name


def handle_enum_by_value(
    typ: type[Enum], default: Default, is_optional: bool
) -> StrDict:
    """
    Use :class:`click.Choice` as option type and use the enum value's name as
    default.
    """
    kwargs: StrDict = {"type": click.Choice([str(v) for v in typ.__members__.values()])}
    if isinstance(default, typ):
        # Convert Enum instance to string
        kwargs["default"] = str(default.value)
    elif is_optional:
        kwargs["default"] = None

    return kwargs


def handle_pattern(
    typ: type[re.Pattern], default: Default, is_optional: bool
) -> StrDict:
    """
    Use "re.compile()" as func param type so that the resulting value is a
    :class:`re.Pattern`.
    """
    kwargs: StrDict = {
        "type": re.compile,
        "metavar": "PATTERN",
    }
    if isinstance(default, typ):
        # Convert Enum instance to string
        kwargs["default"] = default.pattern
    elif is_optional:
        kwargs["default"] = None

    return kwargs


def handle_secret(typ: type[Secret], default: Default, is_optional: bool) -> StrDict:
    """
    Handle :class:`typed_settings.types.Secret` types.
    """
    metavar = "SECRET"
    if isinstance(typ, type):
        cli_type = str
        has_default = isinstance(default, typ)
    else:
        args = get_args(typ)
        cli_type = args[0]
        if cli_type is not str:
            metavar = f"SECRET_{cli_type.__name__.upper()}"
        has_default = isinstance(default, get_origin(typ))

    def cb(c: click.Context, p: click.Parameter, v: Any) -> Secret | None:
        if v is not None:
            return Secret(v)
        return None

    kwargs: StrDict = {
        "type": cli_type,
        "metavar": metavar,
        "callback": cb,
    }
    if has_default:
        kwargs["default"] = default.get_secret_value()  # type: ignore[union-attr]
        kwargs["is_secret"] = True
    elif is_optional:
        kwargs["default"] = None

    return kwargs


#: Default handlers for click option types.
DEFAULT_TYPES: dict[type, TypeHandlerFunc] = {
    datetime: handle_datetime,
    date: handle_date,
    timedelta: handle_timedelta,
    **(
        {
            IntEnum: handle_enum_by_value,
            StrEnum: handle_enum_by_value,
        }
        if PY_311
        else {}
    ),
    Enum: handle_enum_by_name,
    re.Pattern: handle_pattern,
    Secret: handle_secret,
}


class ClickHandler:
    """
    Implementation of the :class:`~typed_settings.cli_utils.TypeHandler`
    protocol for Click.

    Args:
        extra_types: A dict mapping types to specialized handler functions.
            Use :data:`DEFAULT_TYPES` by default.

    .. versionadded:: 2.0.0
    """

    def __init__(self, extra_types: dict[type, TypeHandlerFunc] | None = None) -> None:
        self.extra_types = extra_types or DEFAULT_TYPES

    def get_scalar_handlers(self) -> dict[type, TypeHandlerFunc]:
        return self.extra_types

    def handle_scalar(
        self,
        type: type | None,
        default: Default,
        is_optional: bool,
    ) -> StrDict:
        kwargs: StrDict = {"type": type}
        if default not in (None, NO_DEFAULT):
            kwargs["default"] = default
        elif is_optional:
            kwargs["default"] = None
        if type:
            if issubclass(type, bool):
                kwargs["is_flag"] = True
            elif issubclass(type, SecretStr):
                kwargs["metavar"] = "TEXT"

        return kwargs

    def handle_literal(
        self, type: type | None, default: Default, is_optional: bool
    ) -> StrDict:
        """
        Use :class:`click.Choice` as option type and use the literal's values as
        choices.
        """
        values = get_args(type)
        if not all(isinstance(v, str) for v in values):
            raise ValueError(f"All Literal values must be strings: {values!r}")
        kwargs: StrDict = {"type": click.Choice([str(v) for v in values])}
        if default in values:
            kwargs["default"] = default
        elif is_optional:
            kwargs["default"] = None

        return kwargs

    def handle_tuple(
        self,
        type_args_maker: TypeArgsMaker,
        types: tuple[Any, ...],
        default: tuple | None,
        is_optional: bool,
    ) -> StrDict:
        kwargs = {
            "type": types,
            "nargs": len(types),
            "default": default,
        }
        return kwargs

    def handle_collection(
        self,
        type_args_maker: TypeArgsMaker,
        types: tuple[Any, ...],
        default: Collection[Any] | None,
        is_optional: bool,
    ) -> StrDict:
        kwargs = type_args_maker.get_kwargs(types[0], NO_DEFAULT)
        kwargs["default"] = default
        kwargs["multiple"] = True
        return kwargs

    def handle_mapping(
        self,
        type_args_maker: TypeArgsMaker,
        types: tuple[Any, ...],
        default: Default,
        is_optional: bool,
    ) -> StrDict:
        def cb(
            ctx: click.Context,
            param: click.Option,
            value: Iterable[str] | None,
        ) -> dict[str, str] | None:
            if not value:
                return {}
            splitted = [v.partition("=") for v in value]
            items = {k: v for k, _, v in splitted}
            return items

        kwargs = {
            "metavar": "KEY=VALUE",
            "multiple": True,
            "callback": cb,
        }
        if not isinstance(default, Mapping):
            default = {}
        kwargs["default"] = [f"{k}={v}" for k, v in default.items()]

        return kwargs


def _mk_option(
    option_fn: Callable[..., Decorator[F]],
    oinfo: OptionInfo,
    default: Default,
    type_args_maker: TypeArgsMaker,
    envvar: str | None,
) -> Decorator[F]:
    """
    Recursively creates click options and returns them as a list.
    """
    user_config = dict(oinfo.metadata.get(METADATA_KEY, {}))

    # The option type specifies the default option kwargs
    kwargs = type_args_maker.get_kwargs(oinfo.cls, default)
    if envvar:
        kwargs["envvar"] = envvar
        kwargs["show_envvar"] = True

    param_decls: tuple[str, ...]
    user_param_decls: str | Sequence[str]
    user_param_decls = user_config.pop("param_decls", ())
    if not user_param_decls:
        option_name = oinfo.path.replace(".", "-").replace("_", "-")
        if kwargs.get("is_flag"):
            param_decls = (f"--{option_name}/--no-{option_name}",)
        else:
            param_decls = (f"--{option_name}",)
    elif isinstance(user_param_decls, str):
        param_decls = (user_param_decls,)
    else:
        param_decls = tuple(user_param_decls)

    # The type's kwargs should not be able to set these values since they are
    # needed for everything to work:
    kwargs["show_default"] = True
    kwargs["expose_value"] = False
    kwargs["callback"] = _make_callback(
        oinfo.path, kwargs.get("callback"), user_config.pop("callback", None)
    )

    # Get "help" from the user_config *now*, because we may need to update it
    # below.  Also replace "None" with "".
    kwargs["help"] = user_config.pop("help", None) or ""

    is_secret = any([oinfo.is_secret, kwargs.pop("is_secret", False)])
    if "default" in kwargs:  # pragma: no cover
        if is_secret:
            kwargs["show_default"] = SECRET_REPR
    else:
        kwargs["required"] = True

    # The user has the last word, though.
    kwargs.update(user_config)

    return option_fn(*param_decls, **kwargs)


def _make_callback(
    path: str,
    type_callback: Callback | None,
    user_callback: Callback | None,
) -> Callback:
    """
    Generate a callback that adds option values to the settings instance in the
    context.

    It also calls a type's callback if there should be one.
    """

    def cb(ctx: click.Context, param: click.Option, value: Any) -> Any:
        param_source = ctx.get_parameter_source(param.name or "")

        # We may not want to add "value" to the settings dict for various reasons:
        param_source_default = param_source is ParameterSource.DEFAULT
        if param_source_default and isinstance(param.default, DefaultFactorySentinel):
            # Don't add the value to the settings dict if it has a default factory.
            # The factory should be invoked later.
            return value
        if param_source_default and value not in (None, (), {}):
            # Don't add default values (that come from loaded settings) because this
            # would override the original LoaderMeta.
            # Only make an exception for "None" and empty containers to handle
            # "Optional[T]" with no explicit default (e.g., "myflag: bool | None").
            return value

        if type_callback is not None:
            value = type_callback(ctx, param, value)
        if user_callback is not None:
            value = user_callback(ctx, param, value)

        if ctx.obj is None:
            ctx.obj = {}

        elif not isinstance(ctx.obj, dict):
            raise RuntimeError(
                f"'ctx.obj' must be a dict when you use Typed Settings, got: "
                f"{type(ctx.obj).__name__}"
            )

        settings = ctx.obj.setdefault(CTX_KEY, {})
        settings[path] = value

        return value

    return cb
