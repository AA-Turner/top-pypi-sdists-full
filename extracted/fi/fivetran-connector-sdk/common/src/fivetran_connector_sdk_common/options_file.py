import os
import sys
import tempfile
from typing import Optional, Tuple

from fivetran_connector_sdk_common import constants
from fivetran_connector_sdk_common.connector_helper import (
    config_root_dir_helper, validate_connection_name, validate_naming, validate_proxy_id)
from fivetran_connector_sdk_common.helpers import print_library_log
from fivetran_connector_sdk_common.logger import Logging


def _exit_options_file_error(message: str) -> None:
    print_library_log(message, Logging.Level.SEVERE)
    sys.exit(1)


def default_options_file_path() -> str:
    """Default options file location: ~/.fivetran/connector_sdk/options.toml."""
    return os.path.join(config_root_dir_helper(), constants.OPTIONS_FILENAME)


def _check_toml_supported() -> bool:
    """Local options file support requires the stdlib `tomllib` module (Python 3.11+)."""
    if sys.version_info < (3, 11):
        print_library_log(constants.OPTIONS_FILE_SKIP_MIN_PYTHON_MESSAGE)
        return False
    return True


def _require_existing_path(path: str, source: str) -> None:
    """Exits if `path` (provided via `source`) doesn't exist."""
    if not os.path.isfile(path):
        _exit_options_file_error(f"options file not found at '{path}', provided via {source}")


def find_options_file(args) -> Optional[str]:
    """Locates the options file: --options-file, FIVETRAN_OPTIONS_FILE env var, ./options.toml,
    ~/.fivetran/connector_sdk/options.toml, in that order. None if none apply.
    """
    if not _check_toml_supported():
        return None

    explicit_path = getattr(args, "options_file", None)
    if explicit_path:
        _require_existing_path(explicit_path, "--options-file")
        return explicit_path

    env_path = os.getenv(constants.FIVETRAN_OPTIONS_FILE_ENV, None)
    if env_path:
        _require_existing_path(env_path, constants.FIVETRAN_OPTIONS_FILE_ENV)
        return env_path

    cwd_path = os.path.join(os.getcwd(), constants.OPTIONS_FILENAME)
    if os.path.isfile(cwd_path):
        return cwd_path

    default_path = default_options_file_path()
    if os.path.isfile(default_path):
        return default_path

    return None


def load_options_file(path: str) -> dict:
    """Reads and parses the local options file into profiles keyed by flat profile name."""
    import tomllib
    try:
        with open(path, "rb") as f:
            return _flatten_profiles(tomllib.load(f))
    except tomllib.TOMLDecodeError as e:
        _exit_options_file_error(f"failed to parse options file '{path}': {e}")
    except UnicodeDecodeError as e:
        _exit_options_file_error(f"options file '{path}' is not valid UTF-8: {e}")
    except OSError as e:
        _exit_options_file_error(f"could not read options file '{path}': {e}")


def _flatten_profiles(data: dict) -> dict:
    """Flattens nested TOML tables into flat profile keys -- a hand-written dotted header
    (e.g. `[warehouse_a.connection_a]`) parses as nested tables unless quoted, so this
    normalizes both forms to the same flat-key shape `select_profile` expects.
    """
    flattened = {}
    seen_prefixes = set()
    for key, value in data.items():
        if not isinstance(value, dict):
            _exit_options_file_error(
                f"options file has field '{key}' defined outside of any profile table; move it "
                f"under a profile, e.g. [{constants.DEFAULT_PROFILE_NAME}]")
        _flatten_profile_entry(key, value, flattened, seen_prefixes)
    return flattened


def _flatten_profile_entry(prefix: str, value: dict, flattened: dict, seen_prefixes: set) -> None:
    """Recurses into nested tables (dotted headers like `[a.b]`) into flat profile keys.
    A dict-valued key is only promoted to a sub-profile if it isn't a managed field name --
    managed fields are always strings, so e.g. `destination = {foo = "x"}` is left as the
    field's (invalid) value for `_validate_profile_fields` to reject, instead of silently
    becoming an orphan sub-profile. Duplicate prefixes are rejected as ambiguous.
    """
    if prefix in seen_prefixes:
        _exit_options_file_error(f"options file defines profile '{prefix}' more than once")
    seen_prefixes.add(prefix)

    nested_keys = {key for key, v in value.items() if isinstance(v, dict)}
    if nested_keys and not (nested_keys & constants.MANAGED_OPTIONS_FIELDS):
        for key, sub_value in value.items():
            if isinstance(sub_value, dict):
                _flatten_profile_entry(f"{prefix}.{key}", sub_value, flattened, seen_prefixes)
            else:
                flattened.setdefault(prefix, {})[key] = sub_value
    else:
        flattened[prefix] = value


def _validate_profile_fields(profile_name: str, options: dict) -> None:
    # Rejects a stored `api_key` and any key outside the managed fields.
    if constants.API_KEY_FIELD in options:
        _exit_options_file_error(
            f"profile '{profile_name}' in the options file contains 'api_key'; api_key must "
            "never be stored in the options file, please remove it")

    unrecognised = sorted(options.keys() - constants.MANAGED_OPTIONS_FIELDS)
    if unrecognised:
        _exit_options_file_error(
            f"profile '{profile_name}' in the options file contains unsupported field(s) "
            f"{unrecognised}; please remove or correct them")

    multiline = sorted(
        key for key, value in options.items()
        if isinstance(value, str) and ("\n" in value or "\r" in value))
    if multiline:
        _exit_options_file_error(
            f"profile '{profile_name}' in the options file has multi-line value(s) for "
            f"{multiline}; options file values must be single-line strings")

    # connection, naming, and proxy_id get the same shared local validation a CLI-provided value
    # would (see connector_helper.py's validate_connection_name/validate_naming/validate_proxy_id,
    # also used by get_connection_name/get_proxy_id); the remaining fields are validated by the
    # API server, so the generic type check below is enough for them. The validated value is
    # written back -- these validators coerce a non-string TOML value (e.g. proxy_id = 123) to
    # str and strip/normalize it, and callers must see that normalized value, not the raw one.
    if "connection" in options:
        options["connection"] = validate_connection_name(options["connection"])
    if "naming" in options:
        options["naming"] = validate_naming(options["naming"])
    if "proxy_id" in options:
        options["proxy_id"] = validate_proxy_id(options["proxy_id"])

    locally_validated = {"connection", "naming", "proxy_id"}
    non_string = sorted(
        key for key, value in options.items()
        if key not in locally_validated and not isinstance(value, str))
    if non_string:
        _exit_options_file_error(
            f"profile '{profile_name}' in the options file has non-string value(s) for "
            f"{non_string}; options file values must be strings")


def select_profile(options_data: dict, profile_name: Optional[str],
                   hint_profile: Optional[str] = None) -> Tuple[dict, bool]:
    """Selects a profile by name, falling back to [default] when none is requested (or named
    "default"). A named profile never inherits from [default]; a missing one exits, suggesting
    `hint_profile` if given. Returns (profile fields, whether a profile actually applied).
    """
    if profile_name and profile_name != constants.DEFAULT_PROFILE_NAME:
        if profile_name not in options_data:
            message = f"profile '{profile_name}' not found in options file"
            if hint_profile and hint_profile != profile_name and hint_profile in options_data:
                message += f"; did you mean '--profile {hint_profile}'?"
            _exit_options_file_error(message)
        _validate_profile_fields(profile_name, options_data[profile_name])
        return options_data[profile_name], True

    default_profile = options_data.get(constants.DEFAULT_PROFILE_NAME)
    if default_profile is None:
        print_library_log(
            f"profile '{constants.DEFAULT_PROFILE_NAME}' not found in options file; continuing "
            "without options-file values for unresolved fields",
            Logging.Level.INFO)
        return {}, False
    _validate_profile_fields(constants.DEFAULT_PROFILE_NAME, default_profile)
    return default_profile, True


_SENSITIVE_FIELDS = frozenset({constants.API_KEY_FIELD})


def _reject_sensitive_fields(profile_name: str, options: dict) -> None:
    """api_key must never be persisted to the options file; backstop at the single write path."""
    leaked = _SENSITIVE_FIELDS & options.keys()
    if leaked:
        raise ValueError(
            f"refusing to write options file: profile '{profile_name}' contains "
            f"sensitive field(s) {sorted(leaked)}, which must never be persisted")


def _reject_unsupported_fields(profile_name: str, options: dict) -> None:
    """Backstop so a caller bug can't write a field `_validate_profile_fields` would then
    reject on the next read -- same single-write-path principle as `_reject_sensitive_fields`.
    """
    unrecognised = sorted(options.keys() - constants.MANAGED_OPTIONS_FIELDS)
    if unrecognised:
        raise ValueError(
            f"refusing to write options file: profile '{profile_name}' contains "
            f"unsupported field(s) {unrecognised}")


def _escape_toml_string(value: str) -> str:
    """Escapes a string for use as a TOML basic string value."""
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return escaped.replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")


def _serialize_profiles(profiles: dict) -> str:
    """Serializes profiles to TOML text. None values are omitted.
    """
    sections = []
    for profile_name, options in profiles.items():
        _reject_sensitive_fields(profile_name, options)
        _reject_unsupported_fields(profile_name, options)
        # Table header is always quoted -- one code path regardless of profile-name content.
        lines = [f'["{_escape_toml_string(profile_name)}"]']
        for key, value in options.items():
            if value is None:
                continue
            lines.append(f'{key} = "{_escape_toml_string(str(value))}"')
        sections.append("\n".join(lines))
    return "\n\n".join(sections) + "\n" if sections else ""


def write_options_file(path: str, profiles: dict, extra_header: str = "") -> None:
    """Writes `profiles` to `path` as TOML. `extra_header` is optional extra text inserted
    between the header comment and the profiles (migration.py's commented [default] block),
    so it lands in the same write instead of a second pass over the file.
    """
    directory = os.path.dirname(path) or "."
    os.makedirs(directory, exist_ok=True)
    content = constants.OPTIONS_FILE_HEADER_COMMENT + extra_header + _serialize_profiles(profiles)

    tmp_path = None
    try:
        with tempfile.NamedTemporaryFile("w", dir=directory, delete=False, encoding=constants.UTF_8) as tmp_file:
            tmp_file.write(content)
            tmp_path = tmp_file.name
        os.replace(tmp_path, path)
    except Exception:
        if tmp_path and os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise


def _load_profiles_or_empty(path: str) -> dict:
    """Loads existing profiles, or an empty set if the file doesn't exist yet."""
    return load_options_file(path) if os.path.isfile(path) else {}


def update_profile_fields(path: str, profile_name: str, profile_fields: dict, extra_header: str = "") -> None:
    """Replaces a single profile's fields, overwriting whatever it previously held; every
    other profile is re-written unchanged. `extra_header` is forwarded to `write_options_file`
    so a caller rewriting a file right after creating it (e.g. migration's write-back) can
    re-supply the same commented [default] block instead of it being dropped.
    """
    profiles = _load_profiles_or_empty(path)
    profiles[profile_name] = profile_fields
    write_options_file(path, profiles, extra_header=extra_header)
