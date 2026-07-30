"""Variable store + template substitution.

Public API:
    set_var(name, value)              — write to _variable_store
    var(template)                     — read with {{name}} / ${name} substitution
    get_variable_value(...)           — shared resolver callback for Condition/Assertion
    resolve_variable(name, template)  — single resolver for V3 emitters (TYPE/SEARCH/FILL,
                                        conditions, assertions); delegates to var()

Private state:
    _variable_store: dict    — set_var writes here
    _test_params: dict       — separate namespace for test parameters
"""
import base64
import calendar
import json
import logging
import os
import random
import re
import string
import time
from datetime import datetime, timedelta
from typing import Any

from testmu_selenium._errors import TestmuConfigError

_log = logging.getLogger(__name__)

_variable_store: dict[str, Any] = {}
_test_params: dict[str, Any] = {}
_global_variables: list = []
_GLOBAL_PREFIX = "global."

_SENTINEL = object()

# Matches {{name}}, {{name|default}}, ${name}, ${name|default}.
# ``lead`` captures the delimiter so ${...} can resolve from _test_params first
# while {{...}} keeps the namespace-dispatch / store-only chain.
_TEMPLATE_RE = re.compile(r"(?P<lead>\{\{|\$\{)(?P<name>[^}|]+)(?:\|(?P<default>[^}]*))?\}\}?")

# A single dotted segment carrying a list index: results[0].
_BRACKET_RE = re.compile(r"(\w+)\[(\d+)\]")


def set_var(name: str, value: Any) -> None:
    """Write a variable into the store. Subsequent var() calls return it.

    A ``global.``-prefixed name is the persist-namespace form of a global
    variable: its canonical store / resolution key is the BARE name. Generated
    code writes a global output via ``set_var("global.X", value)`` but reads it
    back with the bare reference ``{{X}}`` (codegen never prefixes reads —
    global-ness is a property, not part of the name). So the value is stored
    under the bare key (mirroring ``_resolve_global``, which strips the prefix
    to key ATMS) — otherwise the bare read misses the freshly-set value and gets
    the literal template or a stale authoring-time seed.

    For a global, the value is also written back to the ATMS variables backend
    (V2 parity with update_variable_value_by_name) so a persist-enabled
    global updates on the variables page when this runs standalone — e.g. a
    HyperExecute / code-export run, where the host runtime's in-product persist hook is
    absent. Guarded on LT creds; the in-memory store is always written first so
    resolution is unaffected when the backend write is skipped.
    """
    if name.startswith(_GLOBAL_PREFIX):
        bare = name[len(_GLOBAL_PREFIX):]
        _variable_store[bare] = value
        # Session snapshot updates unconditionally (in-product runtime parity:
        # session data always reflects the latest generated value; is_persist
        # only gates the TMS write). resolveGlobal's is_persist=false fallback
        # reads this — without the upsert it returns the authoring-time value
        # baked into configure(global_variables=[...]).
        _update_session_variable_value(bare, value)
        from testmu_selenium import _config
        if _config.lt_auth:
            _atms_persist_global_variable(bare, value)
    else:
        _variable_store[name] = value


def _parse_if_string(value: Any) -> Any:
    """Parse a JSON string into dict/list so traversal can descend into it."""
    if not isinstance(value, str):
        return value
    try:
        parsed = json.loads(value)
        if isinstance(parsed, (dict, list)):
            return parsed
    except (ValueError, TypeError):
        pass
    return value


def _traverse_store(path: str) -> Any:
    """Resolve a dotted / bracket-indexed path against _variable_store, else None.

    Flat keys are handled by the caller (var()); this only runs when the full key
    is absent. The first segment is the stored root key (e.g. an API_CALL result
    written by set_var); remaining segments descend through dict keys and list
    indices — supporting ``results[0]`` bracket notation and parsing JSON-string
    values along the way (e.g. api_x.response_body.results[0].name.first).
    """
    if "." not in path and "[" not in path:
        return None

    parts = path.split(".")
    root_key = parts[0]
    root_idx = None
    root_match = _BRACKET_RE.fullmatch(root_key)
    if root_match:
        root_key = root_match.group(1)
        root_idx = int(root_match.group(2))

    if root_key not in _variable_store:
        return None
    obj = _parse_if_string(_variable_store[root_key])
    if root_idx is not None:
        if isinstance(obj, list) and root_idx < len(obj):
            obj = obj[root_idx]
        else:
            return None

    for key in parts[1:]:
        obj = _parse_if_string(obj)
        key_match = _BRACKET_RE.fullmatch(key)
        if key_match:
            if not isinstance(obj, dict):
                return None
            obj = _parse_if_string(obj.get(key_match.group(1)))
            idx = int(key_match.group(2))
            if isinstance(obj, list) and idx < len(obj):
                obj = obj[idx]
            else:
                return None
        elif isinstance(obj, dict):
            obj = obj.get(key)
        elif isinstance(obj, list):
            try:
                obj = obj[int(key)]
            except (ValueError, IndexError):
                return None
        else:
            return None
        if obj is None:
            return None
    return obj


def _resolve_single(name: str) -> Any:
    """Dispatch reserved namespaces ({{secrets|global|environment|totp|smart.x}}).

    Returns _SENTINEL when ``name`` is not a reserved-namespace reference, so the
    caller falls through to the existing flat-store / dotted-path resolution.
    global/environment/totp may raise TestmuConfigError on hard failure.
    """
    parts = name.split(".")
    if parts[0] == "secrets" and len(parts) >= 2:
        return os.getenv(parts[-1], "")
    if parts[0] == "global" and len(parts) >= 2:
        return _resolve_global(parts[1])
    if parts[0] == "environment" and len(parts) >= 2:
        return _resolve_environment(parts[1])
    if parts[0] == "totp" and len(parts) >= 2:
        return _resolve_totp(parts[1])
    if parts[0] == "smart" and len(parts) == 2:
        return _resolve_smart(parts[1])
    return _SENTINEL


def _resolve_global(name: str) -> str:
    """Resolve {{global.x}} — ATMS API when LT creds present, env fallback otherwise."""
    from testmu_selenium import _config
    if not _config.lt_auth:
        fallback = os.getenv(f"TESTMU_VAR_{name}")
        if fallback is not None:
            return fallback
        raise TestmuConfigError(
            f"Variable {{{{global.{name}}}}} cannot be resolved: "
            f"no LT credentials and no TESTMU_VAR_{name} env var set"
        )
    # LT creds present — call ATMS
    try:
        data = _atms_get_variable(name)
        resolved = data.get("value", "")
        # is_persist=False means use the session_value if available
        if not data.get("is_persist", True):
            session_val = _session_variable_value(name)
            if session_val is not None:
                resolved = session_val
        _log.info(f"global.{name} resolved from ATMS")
        return resolved
    except Exception as exc:
        _log.warning(f"ATMS variable lookup for global.{name} failed: {exc}")
        fallback = os.getenv(f"TESTMU_VAR_{name}")
        if fallback is not None:
            return fallback
        raise TestmuConfigError(
            f"Variable {{{{global.{name}}}}} cannot be resolved: ATMS failed and no TESTMU_VAR_{name} env var set"
        ) from exc


def _resolve_environment(name: str) -> str:
    """Resolve {{environment.x}} — ATMS API with ENVIRONMENT_ID, env fallback otherwise."""
    from testmu_selenium import _config
    if not _config.lt_auth:
        fallback = os.getenv(f"TESTMU_VAR_{name}")
        if fallback is not None:
            return fallback
        raise TestmuConfigError(
            f"Variable {{{{environment.{name}}}}} cannot be resolved: "
            f"no LT credentials and no TESTMU_VAR_{name} env var set"
        )
    # LT creds present — call ATMS with ENVIRONMENT_ID
    try:
        environment_id = int(os.getenv("ENVIRONMENT_ID", "0"))
        data = _atms_get_variable(name, environment_id=environment_id)
        resolved = data.get("value", "")
        _log.info(f"environment.{name} resolved from ATMS (env_id={environment_id})")
        return resolved
    except Exception as exc:
        _log.warning(f"ATMS variable lookup for environment.{name} failed: {exc}")
        fallback = os.getenv(f"TESTMU_VAR_{name}")
        if fallback is not None:
            return fallback
        raise TestmuConfigError(
            f"Variable {{{{environment.{name}}}}} cannot be resolved: ATMS failed and no TESTMU_VAR_{name} env var set"
        ) from exc


def _resolve_totp(name: str) -> str:
    """Resolve {{totp.x}} — ATMS seed + pyotp when LT creds present, env fallback otherwise."""
    from testmu_selenium import _config
    if not _config.lt_auth:
        seed = os.getenv(f"TESTMU_TOTP_{name}")
        if seed:
            import pyotp
            return pyotp.TOTP(seed).now()
        raise TestmuConfigError(
            f"Variable {{{{totp.{name}}}}} cannot be resolved: "
            f"no LT credentials and no TESTMU_TOTP_{name} env var set"
        )
    # LT creds present — call ATMS for TOTP seed
    try:
        seed = _atms_get_totp_seed(name)
        if not seed:
            raise ValueError("empty TOTP seed returned from ATMS")
        import pyotp
        totp_val = pyotp.TOTP(seed).now()
        _log.info(f"totp.{name} TOTP generated (value hidden)")
        return totp_val
    except Exception as exc:
        _log.warning(f"ATMS TOTP lookup for totp.{name} failed: {exc}")
        seed = os.getenv(f"TESTMU_TOTP_{name}")
        if seed:
            import pyotp
            return pyotp.TOTP(seed).now()
        raise TestmuConfigError(
            f"Variable {{{{totp.{name}}}}} cannot be resolved: ATMS failed and no TESTMU_TOTP_{name} env var set"
        ) from exc


# ---------------------------------------------------------------------------
# Smart variable resolution
# ---------------------------------------------------------------------------

def _resolve_smart(name: str) -> str:
    """Resolve {{smart.x}} — computed smart variables.

    Matches the smart-variable contract defined by the code exporter.
    """
    now = datetime.now()

    # Date/time variables
    if name == "current_date":
        return now.strftime("%Y-%m-%d")
    if name == "current_day":
        return now.strftime("%A")
    if name == "current_month_number":
        return now.strftime("%m")
    if name == "current_year":
        return now.strftime("%Y")
    if name == "current_month":
        return now.strftime("%B")
    if name == "current_hour":
        return now.strftime("%H")
    if name == "current_minute":
        return now.strftime("%M")
    if name == "current_timestamp":
        return now.strftime("%Y-%m-%d %H:%M:%S")
    if name == "current_timezone":
        return time.strftime("%Z")

    # Date calculations
    if name == "next_day":
        return (now + timedelta(days=1)).strftime("%Y-%m-%d")
    if name == "previous_day":
        return (now - timedelta(days=1)).strftime("%Y-%m-%d")
    if name == "start_of_week":
        return (now - timedelta(days=now.weekday())).strftime("%Y-%m-%d")
    if name == "end_of_week":
        return (now + timedelta(days=6 - now.weekday())).strftime("%Y-%m-%d")
    if name == "start_of_month":
        return now.replace(day=1).strftime("%Y-%m-%d")
    if name == "end_of_month":
        return now.replace(day=calendar.monthrange(now.year, now.month)[1]).strftime("%Y-%m-%d")

    # Random variables
    if name == "random_int":
        return str(random.randint(100, 999))
    if name == "random_float":
        return str(round(random.uniform(1, 100), 2))
    if name == "random_string_8":
        return "".join(random.choices(string.ascii_letters + string.digits, k=8))
    if name == "random_string_56":
        return "".join(random.choices(string.ascii_letters + string.digits, k=56))
    if name == "random_email":
        return "".join(random.choices(string.ascii_lowercase + string.digits, k=10)) + "@example.com"
    if name == "random_phone":
        return str(random.randint(1000000000, 9999999999))

    # Static geo variables
    if name == "latitude":
        return "13.2257"
    if name == "longitude":
        return "77.5750"
    if name == "country":
        return "India"
    if name == "city":
        return "Doddaballapura"
    if name == "ip_address":
        return "143.110.182.88"

    # Environment/system info (from SmartVariableArgConst)
    if name == "user_name":
        return os.getenv("LT_USERNAME", "")
    if name == "os_type" or name == "os":
        return os.getenv("smart_os", "")
    if name == "os_version":
        return os.getenv("smart_os_version", "")
    if name == "browser_name":
        return os.getenv("smart_browser_name", "")
    if name == "browser_version":
        return os.getenv("smart_browser_version", "")

    _log.warning(f"Unknown smart variable: smart.{name}")
    return ""


# ---------------------------------------------------------------------------
# ATMS HTTP helpers
# ---------------------------------------------------------------------------

def _atms_auth_headers() -> dict:
    """Build Basic-auth headers using LT credentials from environment."""
    username = os.getenv("LT_USERNAME", "")
    access_key = os.getenv("LT_ACCESS_KEY", "")
    encoded = base64.b64encode(f"{username}:{access_key}".encode()).decode()
    return {
        "Content-Type": "application/json",
        "Authorization": f"Basic {encoded}",
    }


_ATMS_DEFAULT_URL = "https://test-manager-api.lambdatest.com"


def _atms_get_variable(variable_name: str, environment_id: int = 0) -> dict:
    """GET {ATMS_URL}/api/v1/variables/{name} — returns the data dict."""
    import requests
    # Bug-D1 fix: default to the production test-manager URL (matches PW sibling).
    # "" causes "No scheme supplied" errors when ATMS_URL env var is unset.
    atms_url = os.getenv("ATMS_URL", _ATMS_DEFAULT_URL)
    url = f"{atms_url}/api/v1/variables/{variable_name}?environment_id={environment_id}"
    resp = requests.get(url=url, headers=_atms_auth_headers())
    if resp.status_code != 200:
        raise RuntimeError(f"ATMS variable lookup failed ({resp.status_code}): {resp.text}")
    return resp.json()["data"]


def _atms_get_totp_seed(variable_name: str) -> str:
    """GET {ATMS_URL}/api/v1/variables/totp/{name} — returns the seed string."""
    import requests
    # Bug-D1 fix: same default as _atms_get_variable (matches PW sibling).
    atms_url = os.getenv("ATMS_URL", _ATMS_DEFAULT_URL)
    url = f"{atms_url}/api/v1/variables/totp/{variable_name}"
    resp = requests.get(url=url, headers=_atms_auth_headers())
    if resp.status_code != 200:
        raise RuntimeError(f"ATMS TOTP seed lookup failed ({resp.status_code}): {resp.text}")
    return resp.json()["data"]


# ---------------------------------------------------------------------------
# is_persist write-back helper
# ---------------------------------------------------------------------------

def _atms_persist_global_variable(name: str, value: Any) -> None:
    """Write a global variable's new value back to ATMS so it shows on the
    variables page — V2 parity with update_variable_value_by_name.

    PUT {ATMS_URL}/api/v1/variables/name/{name}. The server decides persistence
    exactly as V2 relies on: 200 = persisted; 403 = the variable is not
    persist-enabled (session value only, no error). Any failure is swallowed so a
    backend hiccup never breaks the running test. ``name`` is the bare name (the
    ``global.`` prefix already stripped). Reuses the same ATMS_URL / LT-cred auth
    as the read path (_atms_get_variable).
    """
    import requests
    atms_url = os.getenv("ATMS_URL", "")
    if not atms_url:
        return
    url = f"{atms_url}/api/v1/variables/name/{name}"
    payload = {
        "value": str(value) if value is not None else "",
        "value_type": "string",
        "type": "variable",
        "environment_id": 0,
    }
    try:
        resp = requests.put(url=url, headers=_atms_auth_headers(), json=payload)
        if resp.status_code == 200:
            _log.info(f"global.{name} persisted to ATMS")
        elif resp.status_code in (403, 500):
            # ATMS rejects the write-back for persist-off variables (403 by
            # design, 500 observed in practice). Not an error: the session
            # value is already updated locally, so just say persistence is off.
            _log.info(f"global.{name} variable persistence is off — session value only")
        else:
            _log.warning(f"ATMS persist for global.{name} failed ({resp.status_code}): {resp.text}")
    except Exception as exc:
        _log.warning(f"ATMS persist for global.{name} failed: {exc}")


def _session_variable_value(name: str) -> Any:
    """Return session_value (or value) for a named global variable from _global_variables."""
    for gv in _global_variables:
        if gv.get("name") == name:
            return gv.get("session_value", gv.get("value"))
    return None


def _update_session_variable_value(name: str, value: Any) -> None:
    """Upsert the session snapshot for a global variable (bare name).

    Mirrors the in-product runtime: the session value always tracks the latest
    generated value, independent of is_persist. Entries missing from the baked
    configure() metadata are appended so a later is_persist=false read still
    finds the runtime value.
    """
    for gv in _global_variables:
        if gv.get("name") == name:
            gv["session_value"] = value
            return
    _global_variables.append({"name": name, "session_value": value})


def var(template: Any, default: Any = None) -> Any:
    """Resolve {{name}} / ${name} templates against _variable_store.

    If the entire input is one template ({{name}} alone), returns the native value
    (preserving int/dict/list types). If the template is embedded in a string, returns
    a string with all matches substituted. If no template, returns the input unchanged.

    A flat store key is matched first; when it is absent the name is treated as a
    dotted / bracket-indexed path and traversed into the stored value (so
    {{api_x.response_body.results[0].name.first}} resolves against the object
    stored under ``api_x``).
    """
    if not isinstance(template, str):
        return template

    # Whole-string template? Return native value.
    full_match = _TEMPLATE_RE.fullmatch(template.strip())
    if full_match:
        name = full_match.group("name").strip()
        fallback = full_match.group("default")
        # ${name}: test_params FIRST, then store/traverse. No namespace dispatch.
        if full_match.group("lead") == "${":
            if name in _test_params:
                return _test_params[name]
            if name in _variable_store:
                return _variable_store[name]
            traversed = _traverse_store(name)
            if traversed is not None:
                return traversed
            if fallback is not None:
                return fallback
            if default is not None:
                return default
            return template  # unresolved — return literal
        ns = _resolve_single(name)
        if ns is not _SENTINEL:
            return ns
        if name in _variable_store:
            return _variable_store[name]
        traversed = _traverse_store(name)
        if traversed is not None:
            return traversed
        if fallback is not None:
            return fallback
        if default is not None:
            return default
        return template  # unresolved — return literal

    # Embedded — substitute all matches as strings.
    def _sub(m: "re.Match") -> str:
        name = m.group("name").strip()
        fallback = m.group("default")
        # ${name}: test_params FIRST, then store/traverse. No namespace dispatch.
        if m.group("lead") == "${":
            if name in _test_params:
                return str(_test_params[name])
            if name in _variable_store:
                return str(_variable_store[name])
            traversed = _traverse_store(name)
            if traversed is not None:
                return str(traversed)
            if fallback is not None:
                return fallback
            return m.group(0)  # leave literal if unresolved
        ns = _resolve_single(name)
        if ns is not _SENTINEL:
            return str(ns)
        if name in _variable_store:
            return str(_variable_store[name])
        traversed = _traverse_store(name)
        if traversed is not None:
            return str(traversed)
        if fallback is not None:
            return fallback
        return m.group(0)  # leave literal if unresolved

    return _TEMPLATE_RE.sub(_sub, template)


def clear_state() -> None:
    """Clear all variables. Used between tests."""
    _variable_store.clear()
    _test_params.clear()
    _global_variables.clear()


def get_variable_value(template: Any, variables: Any = None, *args: Any, **kwargs: Any) -> Any:
    """Resolve a template against the testmu_selenium variable store.

    Adapter for the runtime-helper ``Condition``/``Assertion``/``Mathmatic``
    ``.evaluate(variables, get_variable_value)`` callback shape. They invoke
    ``get_variable_value(template, variables, *args, **kwargs)``; we ignore the
    extra args and delegate the substitution to ``var()``.

    This exists so generated test.py can pass a clean callable reference
    instead of an inline lambda — and so all V3 emitters share one resolver.
    """
    return var(template)


def resolve_variable(name: Any, template: Any = None) -> Any:
    """Resolve a {{...}} / ${...} variable reference for generated tests.

    Single resolver shared by every V3 emitter (TYPE/SEARCH/FILL, conditions,
    assertions). Two call shapes:
      * ``template`` carries the ``{{...}}`` / ``${...}`` text -> resolve it
        directly via ``var()`` (handles pure / embedded / dotted-bracket / ${}
        forms and native-type preservation);
      * ``template`` is a plain fallback -> resolve ``{{name}}`` from the store,
        returning the plain ``template`` when the name is absent.

    Reserved namespaces (global/environment/totp) raise TestmuConfigError on
    hard failure. Bug-D2 fix: these errors propagate rather than being caught
    and silently returning the raw mustache literal (which caused false-passes
    where a test looked green but the variable was never resolved).
    """
    template_str = str(template) if template is not None else ""
    if "{{" in template_str or "${" in template_str:
        # Bug-D2 fix: let TestmuConfigError propagate — reserved-ns failures must
        # be loud (false-pass from swallowing was worse than a loud abort).
        return var(template)
    if name:
        wrapped = "{{" + str(name) + "}}"
        # Bug-D2 fix: same — bare-name path must also propagate hard failures.
        resolved = var(wrapped)
        if resolved != wrapped:
            return resolved
    return template
