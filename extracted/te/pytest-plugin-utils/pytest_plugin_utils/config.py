"""
Pytest option registry and resolution helpers for this plugin.

Options are registered once, then resolved at read time with a consistent
precedence: runtime overrides > INI > defaults from the registry.
"""

import typing as t
import warnings
from dataclasses import dataclass
from pathlib import Path

import logging
from _pytest.config import Config
from _pytest.config.argparsing import Parser

log = logging.getLogger(__package__)


@dataclass
class OptionDef:
    """
    Internal representation of the options this plugin wants to expose to pytest.
    """

    name: str
    default: t.Any
    help_text: str
    available: t.Literal["all", "ini", "cli_option", None]
    type_hint: t.Any | None
    ini_type: (
        t.Literal[
            "string", "paths", "pathlist", "args", "linelist", "bool", "int", "float"
        ]
        | None
    )


REGISTRY: dict[str, list[OptionDef]] = {}
"configuration options this plugin wants to expose to pytest, keyed by namespace"


def _infer_ini_type(
    type_hint: t.Any,
) -> (
    t.Literal["string", "paths", "pathlist", "args", "linelist", "bool", "int", "float"]
    | None
):
    """
    Infer the pytest INI type string from a Python type hint.

    Supported mappings:
    - bool -> "bool"
    - str -> "string"
    - list[str] -> "linelist"
    - list[Path] -> "paths"

    Unsupported/Not inferred:
    - "args" (list of whitespace-separated strings)
    - "pathlist" (legacy alias for "paths")
    """
    if type_hint is bool:
        return "bool"
    if type_hint is str:
        return "string"

    origin = t.get_origin(type_hint)
    args = t.get_args(type_hint)

    if origin is list:
        if args and args[0] is str:
            return "linelist"
        if args and issubclass(args[0], Path):
            return "paths"

    return None


def set_pytest_option(
    namespace: str,
    name: str,
    *,
    default: t.Any = None,
    help: str = "",
    available: t.Literal["all", "ini", "cli_option", None] = None,
    type_hint: t.Any | None = None,
) -> None:
    """
    Define a pytest option.

    This queues the option for registration (hook_addoption) and
    configuration (hook_configure).

    Args:
        namespace: Unique namespace for this plugin (typically __package__).
        name: The key name (e.g. "api_url"). Use underscores.
        default: The fallback value if not provided via CLI or INI.
        help: Help text for the CLI/INI description.
        available: Where this option should be exposed to the user.
                   - 'cli_option': Adds a --flag.
                   - 'ini': Adds a value to pytest.ini.
                   - 'all': Adds both.
                   - None: Purely internal/runtime (set via code only).
        type_hint: Optional Python type hint (e.g. bool, list[str]) used for
                   validation and INI type inference.
    """
    ini_type = _infer_ini_type(type_hint)
    if namespace not in REGISTRY:
        REGISTRY[namespace] = []
    REGISTRY[namespace].append(
        OptionDef(
            name=name,
            default=default,
            help_text=help,
            available=available,
            type_hint=type_hint,
            ini_type=ini_type,
        )
    )


def register_pytest_options(namespace: str, parser: Parser) -> None:
    """
    Must be called within `pytest_addoption` to register CLI/INI flags.

    CLI options are grouped under a section named after `namespace` in
    `pytest --help`. Group description and ordering are not configurable
    here — call `parser.getgroup` yourself *before* this function if you
    need them:

        def pytest_addoption(parser):
            parser.getgroup("my_plugin", description="My plugin options", after="general")
            register_pytest_options("my_plugin", parser)

    Because pytest returns the existing group on subsequent `getgroup` calls
    with the same name, the description and ordering you set will be preserved.

    Args:
        namespace: Unique namespace for this plugin (typically __package__).
        parser: The pytest parser to register options with.
    """
    group = parser.getgroup(namespace)

    for opt in REGISTRY.get(namespace, []):
        help_text = opt.help_text
        if opt.default is not None:
            help_text = f"{opt.help_text} (default: {opt.default})"

        # CLI Registration
        if opt.available in ("all", "cli_option"):
            cli_name = f"--{opt.name.replace('_', '-')}"
            # CRITICAL: We set default=None here so CLI allows fallback to INI/Runtime
            if opt.type_hint is bool:
                group.addoption(
                    cli_name, action="store_true", default=None, help=help_text
                )
            else:
                group.addoption(cli_name, action="store", default=None, help=help_text)

        # INI Registration
        if opt.available in ("all", "ini"):
            # We set default=None here so INI allows fallback to Runtime default
            parser.addini(opt.name, help=help_text, default=None, type=opt.ini_type)


def _smart_cast[T](value: t.Any, type_hint: type[T] | None) -> T | t.Any:
    """
    Cast a value to the expected type if it's not already correct.
    This handles cases where CLI arguments (always strings) need conversion,
    or where default values might not match the strict type.
    """
    log.debug("casting value raw_value=%s target_type=%s", value, type_hint)

    if type_hint is None:
        return value

    # Handle GenericAlias types (e.g. list[str]) for isinstance checks
    origin = t.get_origin(type_hint)
    check_type = origin if origin is not None else type_hint

    try:
        if isinstance(value, check_type):
            log.debug("value already correct type, no conversion needed")
            return value
    except TypeError:
        # Fallback if isinstance fails (e.g. some complex types)
        pass

    if value is None:
        return None

    # Casting logic for strings (from CLI or raw defaults)
    if type_hint is bool and isinstance(value, str):
        result = value.lower() in ("true", "1", "yes", "on")
        log.debug("converted string to bool converted_value=%s", result)
        return result

    if origin is list and isinstance(value, str):
        # list("foo") produces ['f', 'o', 'o'], so handle string-to-list specially
        # by splitting on newlines (CLI args or raw strings from config)
        result = [v.strip() for v in value.splitlines() if v.strip()]
        log.debug("converted string to list converted_value=%s", result)
        return result

    # Generic fallback: call type_hint(value) as constructor
    try:
        if origin is not None:
            result = t.cast(type, origin)(value)
        else:
            result = t.cast(type, type_hint)(value)
        log.debug("converted using type constructor converted_value=%s", result)
        return result
    except (TypeError, ValueError) as e:
        log.debug("failed to convert value error=%s", str(e))
        raise TypeError(
            f"Cannot cast value of type {type(value)} to {type_hint}"
        ) from e


@t.overload
def get_pytest_option[T](
    namespace: str, config: Config, key: str, *, type_hint: type[T]
) -> T | None: ...


@t.overload
def get_pytest_option(
    namespace: str, config: Config, key: str, *, type_hint: None = None
) -> t.Any | None: ...


def get_pytest_option(
    namespace: str, config: Config, key: str, *, type_hint: t.Any | None = None
) -> t.Any | None:
    """
    Retrieve a configuration value from runtime overrides, CLI, or INI files.

    Priority chain:
    1. Runtime overrides (via config.option in pytest_configure)
    2. CLI arguments (e.g., --my-key)
    3. Configuration files (pytest.ini, pyproject.toml)

    Args:
            namespace: Unique namespace for this plugin (typically __package__).
            config: The pytest Config object.
            key: The option name (use underscores).
            type_hint: Optional expected type for validation and smart casting.

    Returns:
            The resolved value, optionally casted. Returns None if not found.
    """
    log.debug(
        "getting pytest option namespace=%s key=%s type_hint=%s",
        namespace,
        key,
        type_hint,
    )

    normalized_key = key.replace("-", "_")
    opt = next(
        (
            entry
            for entry in REGISTRY.get(namespace, [])
            if entry.name == normalized_key
        ),
        None,
    )

    # Validation
    if type_hint is not None and opt is not None and opt.type_hint is not None:
        if type_hint != opt.type_hint:
            warnings.warn(
                f"Type mismatch for option '{key}': requested {type_hint}, configured {opt.type_hint}"
            )

    # CLI/runtime value from config.option (argparse Namespace)
    val = getattr(config.option, normalized_key, None)
    source = None

    if val in (None, ""):
        # INI value from pytest.ini or pyproject.toml
        try:
            val = config.getini(normalized_key)
            if val not in (None, ""):
                source = "ini"
        except (ValueError, KeyError):
            val = None

    else:
        source = "cli"

    if val in (None, ""):
        # Default value from the registry
        if opt is not None:
            val = opt.default
            source = "default"

    log.debug("resolved raw value key=%s raw_value=%s source=%s", key, val, source)

    # Determine effective type hint
    effective_type_hint = type_hint
    if effective_type_hint is None and opt is not None:
        effective_type_hint = opt.type_hint

    # Smart cast
    if val is not None and effective_type_hint is not None:
        try:
            result = _smart_cast(val, effective_type_hint)
            log.debug(
                "returning converted value key=%s converted_value=%s", key, result
            )
            return result
        except TypeError as e:
            # warning? or just return val?
            # Let's log a warning and return val to be safe
            warnings.warn(f"Failed to cast option '{key}': {e}")
            log.debug(
                "returning raw value after conversion failure key=%s value=%s", key, val
            )
            return val

    log.debug("returning raw value key=%s value=%s", key, val)
    return val
