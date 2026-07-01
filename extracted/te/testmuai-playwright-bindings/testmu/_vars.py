"""Variable resolution for testmu.

var(template) resolves {{...}} and ${...} placeholders:
- Pure {{x}} → direct lookup from _variable_store (type-preserving)
- Embedded "prefix {{x}} suffix" → string interpolation
- {{secrets.cat.key}} → os.getenv(key)
- {{global.x}} → ATMS API (when lt_auth) or TESTMU_VAR_x env fallback
- {{environment.x}} → ATMS API (when lt_auth) or TESTMU_VAR_x env fallback
- {{totp.x}} → ATMS seed + pyotp (when lt_auth) or TESTMU_TOTP_x env fallback
- {{smart.x}} → computed smart variables (date/time, random, env info)
- ${x} → test_params lookup, then _variable_store

set_var(name, value) stores into _variable_store (shared across files).
"""

import base64
import calendar
import json
import os
import random
import re
import logging
import string
import time

from datetime import datetime, timedelta

from testmu._errors import TestmuConfigError

_log = logging.getLogger("testmu")

_variable_store: dict = {}
_test_params: dict = {}
_global_variables: list = []
_GLOBAL_PREFIX = "global."

_MUSTACHE_RE = re.compile(r"\{\{(.+?)\}\}")
_DOLLAR_RE = re.compile(r"\$\{(.+?)\}")
_BRACKET_RE = re.compile(r"(\w+)\[(\d+)\]")


def _reset_store():
    """Reset variable store (for testing)."""
    _variable_store.clear()
    _test_params.clear()
    _global_variables.clear()


def _preview(val, max_len=100):
    """Short string preview for log lines (avoids dumping large payloads)."""
    s = str(val)
    return s if len(s) <= max_len else s[:max_len] + "..."


def _is_sensitive_template(template_str):
    """Redact resolved logs for secrets/totp templates."""
    return "{{secrets." in template_str or "{{totp." in template_str


def set_var(name, value):
    """Write a variable into the store. Subsequent var() calls return it.

    A ``global.``-prefixed name is the persist-namespace form of a global
    variable: its canonical store / resolution key is the BARE name. Generated
    code writes a global output via ``set_var("global.X", value)`` but reads it
    back with the bare reference ``{{X}}`` (codegen never prefixes reads —
    global-ness is a property, not part of the name). So the value is stored
    under the bare key — otherwise the bare read misses the freshly-set value
    and returns the literal template or a stale authoring-time seed.

    For a global, the value is also written back to the ATMS variables backend
    (V2 parity with update_variable_value_by_name) so a persist-enabled
    global updates on the variables page when this runs standalone — e.g. a
    HyperExecute / code-export run, where the host runtime's in-product persist hook is
    absent. Guarded on LT creds; the in-memory store is always written first so
    resolution is unaffected when the backend write is skipped.
    """
    _log.info("    [set_var] name=%r value=%s", name, _preview(value))
    if name.startswith(_GLOBAL_PREFIX):
        bare = name[len(_GLOBAL_PREFIX):]
        _variable_store[bare] = value
        from testmu import _config
        if _config.lt_auth:
            _atms_persist_global_variable(bare, value)
    else:
        _variable_store[name] = value


def var(template, path=None, transform=None):
    """Resolve a template string with variable substitution.

    Pure templates (just "{{x}}" or "${x}") do direct lookup and preserve type.
    Embedded templates ("prefix {{x}} suffix") do string interpolation.
    Non-template values are returned as-is (type-preserving).
    """
    if template is None:
        _log.info("    [var] template=None → ''")
        return ""

    # If input has no variable patterns, return original value unchanged (type-preserving)
    template_str = str(template)
    if not _MUSTACHE_RE.search(template_str) and not _DOLLAR_RE.search(template_str):
        return template  # no {{...}} or ${...} — return as-is

    sensitive = _is_sensitive_template(template_str)

    # Check if this is a pure single-variable reference (type-preserving).
    # V3 forbids braces in the name class ("[^{}]+") so fullmatch only accepts a
    # genuine whole-string placeholder; a non-greedy ".+?" would expand across
    # interior "}" to satisfy the anchor, misreading "${A}x${B}" as one var
    # (-> ""). Gated on kane_version: V4 keeps the legacy ".+?" behavior
    # unchanged (the multi-placeholder bug is deliberately not fixed for V4).
    from testmu import _configure

    _name = r"[^{}]+" if _configure.get("kane_version", "v4") == "v3" else r".+?"
    pure_mustache = re.fullmatch(r"\{\{(" + _name + r")\}\}", template_str)
    if pure_mustache:
        resolved = _resolve_single(pure_mustache.group(1))
    else:
        pure_dollar = re.fullmatch(r"\$\{(" + _name + r")\}", template_str)
        if pure_dollar:
            name = pure_dollar.group(1)
            resolved = _test_params.get(name, _variable_store.get(name, ""))
        else:
            # Embedded template — string interpolation
            resolved = template_str
            resolved = _MUSTACHE_RE.sub(lambda m: str(_resolve_single(m.group(1))), resolved)
            resolved = _DOLLAR_RE.sub(
                lambda m: str(
                    _test_params.get(m.group(1), _variable_store.get(m.group(1), ""))
                ),
                resolved,
            )

    if path is not None:
        resolved = _apply_path(resolved, path)
    if transform is not None:
        resolved = _apply_transform(resolved, transform)

    resolved_preview = "[REDACTED]" if sensitive else _preview(resolved)
    _log.info(
        "    [var] %s → %s%s%s",
        _preview(template_str),
        resolved_preview,
        f" path={path}" if path is not None else "",
        f" transform={transform}" if transform is not None else "",
    )
    return resolved


def get_variable_value(template, variables=None, *args, **kwargs):
    """Resolve a template against the testmu variable store.

    Adapter for the ``Condition``/``Assertion`` ``.evaluate(variables,
    get_variable_value)`` callback shape. Those classes invoke
    ``get_variable_value(template, variables, *args, **kwargs)``; extra args
    are ignored and substitution delegates to ``var()``.

    This exists so generated test code can pass a clean callable reference
    instead of an inline lambda, and so all code emitters share one resolver.
    """
    return var(template)


def _resolve_single(name):
    """Resolve a single variable name (inside {{...}})."""
    parts = name.split(".")

    # {{secrets.cat.key}} → os.getenv(key)
    if parts[0] == "secrets" and len(parts) >= 2:
        key = parts[-1]
        return os.getenv(key, "")

    # {{global.x}} → ATMS (when lt_auth) or env fallback
    if parts[0] == "global" and len(parts) >= 2:
        var_name = parts[1]
        return _resolve_global(var_name)

    # {{environment.x}} → ATMS (when lt_auth) or env fallback
    if parts[0] == "environment" and len(parts) >= 2:
        var_name = parts[1]
        return _resolve_environment(var_name)

    # {{totp.x}} → ATMS seed + pyotp (when lt_auth) or env fallback
    if parts[0] == "totp" and len(parts) >= 2:
        var_name = parts[1]
        return _resolve_totp(var_name)

    # {{smart.x}} → computed smart variable
    if parts[0] == "smart" and len(parts) == 2:
        return _resolve_smart(parts[1])

    # Plain variable — dot-path traversal for names like "response.data.name"
    if "." in name or "[" in name:
        root = parts[0]
        # Handle root with bracket: "items[0].name"
        root_match = _BRACKET_RE.fullmatch(root)
        root_key = root_match.group(1) if root_match else root
        root_val = _variable_store.get(root_key)
        if root_val is not None:
            root_val = _parse_if_string(root_val)
            # Apply bracket index on root if present
            if root_match:
                idx = int(root_match.group(2))
                if isinstance(root_val, list):
                    try:
                        root_val = root_val[idx]
                    except IndexError:
                        return _variable_store.get(name, "")
                else:
                    return _variable_store.get(name, "")
            # Traverse remaining path
            remaining = ".".join(parts[1:])
            if remaining:
                return _apply_path(root_val, remaining)
            return root_val

    # Direct lookup
    return _variable_store.get(name, "")


def _resolve_global(name):
    """Resolve {{global.x}} — ATMS API when LT creds present, env fallback otherwise."""
    from testmu import _config

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


def _resolve_environment(name):
    """Resolve {{environment.x}} — ATMS API with ENVIRONMENT_ID, env fallback otherwise."""
    from testmu import _config

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
        # ENVIRONMENT_ID env var takes precedence (set by forge YAML on cloud
        # runs); fall back to testmu.configure(environment_id=...) baked into
        # the generated test for local-run convenience.
        from testmu import _configure
        environment_id = int(os.getenv("ENVIRONMENT_ID") or _configure.get("environment_id") or 0)
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


def _resolve_totp(name):
    """Resolve {{totp.x}} — ATMS seed + pyotp when LT creds present, env fallback otherwise."""
    from testmu import _config

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


def _resolve_smart(name):
    """Resolve {{smart.x}} — computed smart variables.

    Matches the smart variable resolution in the TestMu generated test pipeline.
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
        return now.replace(day=calendar.monthrange(now.year, now.month)[1]).strftime(
            "%Y-%m-%d"
        )

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
        return (
            "".join(random.choices(string.ascii_lowercase + string.digits, k=10))
            + "@example.com"
        )
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


def _atms_auth_headers():
    """Build Basic-auth headers using LT credentials from environment."""
    username = os.getenv("LT_USERNAME", "")
    access_key = os.getenv("LT_ACCESS_KEY", "")
    encoded = base64.b64encode(f"{username}:{access_key}".encode()).decode()
    return {
        "Content-Type": "application/json",
        "Authorization": f"Basic {encoded}",
    }


def _atms_get_variable(variable_name, environment_id=0):
    """GET {ATMS_URL}/api/v1/variables/{name} — returns the data dict."""
    import requests

    atms_url = os.getenv("ATMS_URL", "https://test-manager-api.lambdatest.com")
    url = f"{atms_url}/api/v1/variables/{variable_name}?environment_id={environment_id}"
    resp = requests.get(url=url, headers=_atms_auth_headers())
    if resp.status_code != 200:
        raise RuntimeError(
            f"ATMS variable lookup failed ({resp.status_code}): {resp.text}"
        )
    return resp.json()["data"]


def _atms_get_totp_seed(variable_name):
    """GET {ATMS_URL}/api/v1/variables/totp/{name} — returns the seed string."""
    import requests

    atms_url = os.getenv("ATMS_URL", "https://test-manager-api.lambdatest.com")
    url = f"{atms_url}/api/v1/variables/totp/{variable_name}"
    resp = requests.get(url=url, headers=_atms_auth_headers())
    if resp.status_code != 200:
        raise RuntimeError(
            f"ATMS TOTP seed lookup failed ({resp.status_code}): {resp.text}"
        )
    return resp.json()["data"]


def _atms_persist_global_variable(name, value):
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
        elif resp.status_code == 403:
            _log.info(f"global.{name} not persist-enabled (403) — session value only")
        else:
            _log.warning(f"ATMS persist for global.{name} failed ({resp.status_code}): {resp.text}")
    except Exception as exc:
        _log.warning(f"ATMS persist for global.{name} failed: {exc}")


# ---------------------------------------------------------------------------
# is_persist write-back helper
# ---------------------------------------------------------------------------


def _session_variable_value(name):
    """Return session_value (or value) for a named global variable from _global_variables."""
    for gv in _global_variables:
        if gv.get("name") == name:
            return gv.get("session_value", gv.get("value"))
    return None


# ---------------------------------------------------------------------------
# Path navigation
# ---------------------------------------------------------------------------


def _parse_if_string(val):
    """Try to parse a string value as JSON to recover dict/list."""
    if not isinstance(val, str):
        return val
    try:
        parsed = json.loads(val)
        if isinstance(parsed, (dict, list)):
            return parsed
    except (ValueError, TypeError):
        pass
    return val


_SENTINEL = object()  # used to detect missing keys without confusing None values


def _apply_path(value, path):
    """Navigate into a resolved value using a dot/bracket path.

    Examples:
        path="data.name"          on {"data": {"name": "Alice"}}   → "Alice"
        path="[1].id"             on [{"id": 1}, {"id": 2}]        → 2
        path="data.users[0].name" on {"data": {"users": [{"name": "Bob"}]}} → "Bob"

    Parses string values as JSON before traversal so stringified dicts/lists work.
    Returns the original value when the path cannot be fully navigated.
    """
    if path is None:
        return value

    obj = _parse_if_string(value)

    # Split path into segments, handling leading [N] bracket notation.
    # e.g. "[1].id" → ["[1]", "id"],  "data.users[0].name" → ["data", "users[0]", "name"]
    raw_segments = path.split(".")
    segments = [s for s in raw_segments if s]

    for seg in segments:
        obj = _parse_if_string(obj)

        # Bracket-only segment: "[N]"
        bracket_only = re.fullmatch(r"\[(\d+)\]", seg)
        if bracket_only:
            idx = int(bracket_only.group(1))
            if isinstance(obj, list):
                try:
                    obj = obj[idx]
                except IndexError:
                    return value
            else:
                return value
            continue

        # Mixed segment: "key[N]"
        mixed = _BRACKET_RE.fullmatch(seg)
        if mixed:
            key, idx = mixed.group(1), int(mixed.group(2))
            if isinstance(obj, dict):
                inner = obj.get(key, _SENTINEL)
                if inner is _SENTINEL:
                    return value
                inner = _parse_if_string(inner)
                if isinstance(inner, list):
                    try:
                        obj = inner[idx]
                    except IndexError:
                        return value
                else:
                    return value
            else:
                return value
            continue

        # Plain key or integer index
        if isinstance(obj, dict):
            result = obj.get(seg, _SENTINEL)
            if result is _SENTINEL:
                return value
            obj = result
        elif isinstance(obj, list):
            try:
                obj = obj[int(seg)]
            except (ValueError, IndexError):
                return value
        else:
            return value

    return obj


# ---------------------------------------------------------------------------
# Transforms
# ---------------------------------------------------------------------------


def _apply_transform(value, transform):
    """Apply a named transform to a resolved value.

    Supported transforms: upper, lower, trim, str, int, float, bool.
    Unknown transforms return value unchanged.
    """
    if transform is None or value is None:
        return value
    t = transform.strip().lower()
    if t == "upper":
        return str(value).upper()
    if t == "lower":
        return str(value).lower()
    if t == "trim":
        return str(value).strip()
    if t == "str":
        return str(value)
    if t == "int":
        try:
            return int(value)
        except (ValueError, TypeError):
            return value
    if t == "float":
        try:
            return float(value)
        except (ValueError, TypeError):
            return value
    if t == "bool":
        if isinstance(value, bool):
            return value
        return str(value).lower() in ("true", "1", "yes")
    _log.warning(f"Unknown transform '{transform}' — returning value unchanged")
    return value
