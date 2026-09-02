"""Managed and backend-cached configuration lookup for AI Watch."""

from __future__ import annotations

import json
import os
import platform
import plistlib
import sys
from collections.abc import Callable
from enum import Enum
from pathlib import Path
from typing import TypedDict, cast

from runlayer_cli import regex_safe, runtime
from runlayer_cli.aiwatch_config_cache import read_backend_config

if sys.platform == "win32":
    import winreg
else:
    winreg = None  # type: ignore[assignment]

PREF_DOMAIN = "com.runlayer.aiwatch"
CLI_PREF_DOMAIN = "com.runlayer.cli"
REG_KEY_PATH = r"Software\Runlayer\AIWatch"
CLI_REG_KEY_PATH = r"Software\Runlayer\CLI"

HOST_KEY = "Host"
ORG_API_KEY_KEY = "OrgApiKey"
SKILL_SYNC_ORG_API_KEY_KEY = "SkillSyncOrgApiKey"
ENROLLMENT_KEY_KEY = "EnrollmentKey"
USERNAME_KEY = "Username"
DEVICE_NAME_KEY = "DeviceName"
MODE_KEY = "Mode"
ENFORCEMENT_KEY = "Enforcement"
SESSIONS_KEY = "Sessions"
MCP_USAGE_METADATA_KEY = "MCPUsageMetadata"
SYNC_SKILLS_KEY = "SyncSkills"
GZIP_HOOKS_KEY = "GzipHooks"
AUTO_UPDATE_KEY = "AutoUpdate"
BROWSER_EXTENSION_ID_KEY = "BrowserExtensionId"
BROWSER_EXTENSION_UPDATE_URL_KEY = "BrowserExtensionUpdateUrl"
FIREFOX_BROWSER_EXTENSION_ID_KEY = "FirefoxBrowserExtensionId"
FIREFOX_BROWSER_EXTENSION_INSTALL_URL_KEY = "FirefoxBrowserExtensionInstallUrl"
BROWSER_SURFACE_EXPLORATION_ENABLED_KEY = "BrowserSurfaceExplorationEnabled"
BROWSER_SURFACE_CANDIDATE_TELEMETRY_ENABLED_KEY = (
    "BrowserSurfaceCandidateTelemetryEnabled"
)
DETECT_PROCESSES_KEY = "DetectProcesses"
DETECT_CONTAINERS_KEY = "DetectContainers"
DETECT_DISGUISED_SKILLS_KEY = "DetectDisguisedSkills"
ARTIFACT_LOOKUP_CACHE_KEY = "ArtifactLookupCache"
LLM_ROUTING_KEY = "LlmRouting"
LLM_ROUTING_BASE_URL_KEY = "LlmRoutingBaseUrl"
DETECT_RENAMED_PLUGIN_CACHES_KEY = "DetectRenamedPluginCaches"
PROJECT_DEPTH_KEY = "ProjectDepth"
PROJECT_TIMEOUT_KEY = "ProjectTimeout"
CPU_CORES_KEY = "CpuCores"
MAX_CPU_PERCENT_KEY = "MaxCpuPercent"
MEMORY_LIMIT_MB_KEY = "MemoryLimitMb"
GROK_HOME_KEY = "GrokHome"

# Backend settings sync owns these capability keys on macOS and Windows.
# Enforcement remains the legacy fallback for Mode.
BACKEND_SYNC_OWNED_KEYS: tuple[str, ...] = (
    MODE_KEY,
    ENFORCEMENT_KEY,
    SESSIONS_KEY,
    MCP_USAGE_METADATA_KEY,
    DETECT_PROCESSES_KEY,
    DETECT_CONTAINERS_KEY,
    GZIP_HOOKS_KEY,
    DETECT_DISGUISED_SKILLS_KEY,
    ARTIFACT_LOOKUP_CACHE_KEY,
    LLM_ROUTING_KEY,
    LLM_ROUTING_BASE_URL_KEY,
    PROJECT_DEPTH_KEY,
    PROJECT_TIMEOUT_KEY,
)

_STRING_FIELDS: tuple[tuple[str, str], ...] = (
    (HOST_KEY, "host"),
    (ORG_API_KEY_KEY, "org_api_key"),
    (SKILL_SYNC_ORG_API_KEY_KEY, "skill_sync_org_api_key"),
    (ENROLLMENT_KEY_KEY, "enrollment_key"),
    (USERNAME_KEY, "username"),
    (DEVICE_NAME_KEY, "device_name"),
    (BROWSER_EXTENSION_ID_KEY, "browser_extension_id"),
    (BROWSER_EXTENSION_UPDATE_URL_KEY, "browser_extension_update_url"),
    (FIREFOX_BROWSER_EXTENSION_ID_KEY, "firefox_browser_extension_id"),
    (
        FIREFOX_BROWSER_EXTENSION_INSTALL_URL_KEY,
        "firefox_browser_extension_install_url",
    ),
    (GROK_HOME_KEY, "grok_home"),
)

_BOOL_FIELDS: tuple[tuple[str, str], ...] = (
    (ENFORCEMENT_KEY, "enforcement"),
    (SESSIONS_KEY, "sessions"),
    (MCP_USAGE_METADATA_KEY, "mcp_usage_metadata"),
    (SYNC_SKILLS_KEY, "sync_skills"),
    # Gzip for large hook POST bodies. Default OFF: backends that predate gzip
    # request decompression reject compressed bodies outright, and dedicated
    # tenants upgrade on their own cadence — fleets flip this only after their
    # backend upgrade. RUNLAYER_HOOK_GZIP=0 kill switch always wins (relay.py).
    (GZIP_HOOKS_KEY, "gzip_hooks"),
    (AUTO_UPDATE_KEY, "auto_update"),
    (DETECT_PROCESSES_KEY, "detect_processes"),
    (DETECT_CONTAINERS_KEY, "detect_containers"),
    (DETECT_DISGUISED_SKILLS_KEY, "detect_disguised_skills"),
    # MDM/local-config channel only: not in BACKEND_SYNC_OWNED_KEYS because
    # the backend settings snapshot doesn't carry this capability (yet).
    (DETECT_RENAMED_PLUGIN_CACHES_KEY, "detect_renamed_plugin_caches"),
)

# Positive-int scan-tuning fields. Type-only validation here (accept int, reject
# bool / non-int / <= 0); range clamping to the supported max is owned downstream
# by the typer IntRange in commands/scan.py + the scanner backstop.
_INT_FIELDS: tuple[tuple[str, str], ...] = (
    (PROJECT_DEPTH_KEY, "project_depth"),
    (PROJECT_TIMEOUT_KEY, "project_timeout"),
    (CPU_CORES_KEY, "cpu_cores"),
    (MAX_CPU_PERCENT_KEY, "max_cpu_percent"),
    (MEMORY_LIMIT_MB_KEY, "memory_limit_mb"),
)

# Sentinels in the shipped mobileconfig template; ignored as live values to
# protect operators who upload without find-and-replace.
_PLACEHOLDER_PREFIX = "REPLACE_WITH"
_PLACEHOLDER_SUFFIX = "_OR_LEAVE_BLANK"

# Workspace ONE lookup tokens — admins upload com.runlayer.aiwatch.ws1
# .mobileconfig with `{CustomAttribute3}` etc. Live devices receive the
# substituted value; misconfigured fleets land the literal token in managed
# prefs. Filter it out so enroll doesn't POST garbage to /api/v1/mdm/enroll.
# `\p{L}\p{N}_` rather than `\w`: RE2's `\w` is ASCII-only, and this is the one
# narrowing in the CLI migration that would fail OPEN — an unsubstituted token
# like "{Attribut\u00e9}" was filtered out under stdlib's Unicode `\w` and would
# otherwise be POSTed to /api/v1/mdm/enroll. `$` as end-of-text is fine: WS1
# tokens carry no trailing newline.
_WS1_LOOKUP_TOKEN_RE = regex_safe.compile(r"^\{[A-Za-z][\p{L}\p{N}_]*\}$")
_managed_config_provider: Callable[[], ManagedConfig] | None = None


class AIWatchMode(str, Enum):
    """Endpoint behavior selected by the resolved ``Mode`` configuration."""

    MONITOR = "monitor"
    PROTECT = "protect"
    ENFORCE = "enforce"


def _parse_mode(value: object) -> AIWatchMode | None:
    if not isinstance(value, str):
        return None
    try:
        return AIWatchMode(value.strip().lower())
    except ValueError:
        return None


def _is_placeholder(value: str) -> bool:
    return (
        _PLACEHOLDER_PREFIX in value
        or value.endswith(_PLACEHOLDER_SUFFIX)
        or bool(_WS1_LOOKUP_TOKEN_RE.match(value))
    )


class ManagedConfig(TypedDict, total=False):
    """Subset of MDM-managed settings relevant to scan + hook flows."""

    daemon_enabled: bool
    llm_routing: bool
    llm_routing_base_url: str
    host: str
    org_api_key: str
    skill_sync_org_api_key: str
    enrollment_key: str
    username: str
    device_name: str
    browser_extension_id: str
    browser_extension_update_url: str
    firefox_browser_extension_id: str
    firefox_browser_extension_install_url: str
    mode: AIWatchMode
    enforcement: bool
    sessions: bool
    mcp_usage_metadata: bool
    sync_skills: bool
    gzip_hooks: bool
    hook_wire_encodings: tuple[str, ...]
    browser_mode: AIWatchMode
    browser_sessions: bool
    browser_extension_enabled: bool
    auto_update: bool
    detect_processes: bool
    detect_containers: bool
    detect_disguised_skills: bool
    artifact_lookup_cache: bool
    detect_renamed_plugin_caches: bool
    project_depth: int
    project_timeout: int
    cpu_cores: int
    max_cpu_percent: int
    memory_limit_mb: int
    grok_home: str


SECRET_FIELDS: frozenset[str] = frozenset(
    {
        "enrollment_key",
        "org_api_key",
        "skill_sync_org_api_key",
    }
)


MACOS_PLIST_PATHS: tuple[Path, ...] = (
    Path("/Library/Managed Preferences") / f"{PREF_DOMAIN}.plist",
    Path("/Library/Preferences") / f"{PREF_DOMAIN}.plist",
)
CLI_MACOS_PLIST_PATHS: tuple[Path, ...] = (
    Path("/Library/Managed Preferences") / f"{CLI_PREF_DOMAIN}.plist",
    Path("/Library/Preferences") / f"{CLI_PREF_DOMAIN}.plist",
)

# Linux has no MDM channel; the package ships a root-owned JSON config with the
# same keys (and JSON's bool/int types map 1:1 onto the plist semantics in
# _parse_mapping). Must stay world-readable: per-user scan children read it
# after the cron wrapper drops privileges — which is why the standard
# deployment delivers OrgApiKey via the root-only credentials env file, never
# this config. The reader still parses an OrgApiKey key if an operator puts
# one here (platform parity with the plist/registry readers); the shipped
# template just never does, because this file is world-readable.
LINUX_CONFIG_PATHS: tuple[Path, ...] = (Path("/etc/runlayer/aiwatch/config.json"),)


def read_managed_config() -> ManagedConfig:
    """Return managed settings with a matching backend snapshot overlaid."""
    if _managed_config_provider is not None:
        return _managed_config_provider().copy()
    return _read_managed_config_uncached()


def set_managed_config_provider(
    provider: Callable[[], ManagedConfig] | None,
) -> None:
    """Install a caller-owned cache provider, or restore direct OS reads."""
    global _managed_config_provider
    _managed_config_provider = provider


def _read_managed_config_uncached() -> ManagedConfig:
    """Read managed settings directly from the platform and backend snapshot."""
    system = platform.system()
    managed: ManagedConfig
    if system == "Darwin":
        paths = MACOS_PLIST_PATHS
        if not runtime.is_aiwatch_runtime():
            paths = CLI_MACOS_PLIST_PATHS + paths
        managed = _read_macos(paths)
    elif system == "Windows":
        managed = _read_windows()
    elif system == "Linux":
        managed = _read_linux(LINUX_CONFIG_PATHS)
    else:
        managed = {}

    if system in {"Darwin", "Windows", "Linux"}:
        org_api_key = managed.get("org_api_key")
        if not org_api_key and system == "Linux":
            # On Linux the org key never sits in the world-readable managed
            # config — the root cron wrapper sources the 0600 credentials file
            # and hands the key to scan children as RUNLAYER_API_KEY. Bind the
            # snapshot to that key so rotation still invalidates cached
            # settings.
            org_api_key = os.environ.get("RUNLAYER_API_KEY") or None
        backend_config = read_backend_config(org_api_key) if org_api_key else None
        if backend_config is not None:
            managed["daemon_enabled"] = backend_config["daemon_enabled"]
            if "llm_routing" in backend_config:
                managed["llm_routing"] = backend_config["llm_routing"]
            llm_routing_base_url = backend_config.get("llm_routing_base_url")
            if llm_routing_base_url is not None:
                managed["llm_routing_base_url"] = llm_routing_base_url
            mode = _parse_mode(backend_config["mode"])
            if mode is not None:
                managed["mode"] = mode
                managed["sessions"] = backend_config["sessions"]
                managed["mcp_usage_metadata"] = backend_config["mcp_usage_metadata"]
                browser_mode = _parse_mode(backend_config["browser_mode"])
                if browser_mode is not None:
                    managed["browser_mode"] = browser_mode
                managed["browser_sessions"] = backend_config["browser_sessions"]
                browser_extension_enabled = backend_config.get(
                    "browser_extension_enabled"
                )
                if browser_extension_enabled is not None:
                    managed["browser_extension_enabled"] = browser_extension_enabled
                browser_extension_update_url = backend_config.get(
                    "browser_extension_update_url"
                )
                if browser_extension_update_url is not None:
                    managed["browser_extension_update_url"] = (
                        browser_extension_update_url
                    )
                firefox_browser_extension_install_url = backend_config.get(
                    "firefox_browser_extension_install_url"
                )
                if firefox_browser_extension_install_url is not None:
                    managed["firefox_browser_extension_install_url"] = (
                        firefox_browser_extension_install_url
                    )
                managed["detect_processes"] = backend_config["detect_processes"]
                managed["detect_containers"] = backend_config["detect_containers"]
                hook_wire_encodings = backend_config.get("hook_wire_encodings")
                if hook_wire_encodings is not None:
                    managed["hook_wire_encodings"] = hook_wire_encodings
                # Backend value wins over any locally-managed GzipHooks key
                # (same as every other overlaid field); absent snapshot key
                # leaves the local value as bootstrap/back-compat.
                gzip_hooks = backend_config.get("gzip_hooks")
                if gzip_hooks is not None:
                    managed["gzip_hooks"] = gzip_hooks
                managed["detect_disguised_skills"] = backend_config.get(
                    "detect_disguised_skills", False
                )
                managed["artifact_lookup_cache"] = backend_config.get(
                    "artifact_lookup_cache", False
                )
                managed["project_depth"] = backend_config["project_depth"]
                managed["project_timeout"] = backend_config["project_timeout"]
    return managed


def resolve_include_pipeline(
    all_events: bool, managed: ManagedConfig | None = None
) -> bool:
    """Whether to install event/session hooks alongside enforcement hooks.

    Config-driven and scope-independent: ``--all-events`` always wins. Otherwise,
    only explicit ``Sessions=true`` includes the event/session pipeline; a
    missing setting fails closed.
    """
    if all_events:
        return True
    if managed is None:
        managed = read_managed_config()
    return bool(managed.get("sessions", False))


def resolve_enforcement(managed: ManagedConfig | None = None) -> bool:
    """Whether full MCP/source governance is enabled for this fleet.

    ``Mode=enforce`` wins when present. Without a valid ``Mode``, the legacy
    ``Enforcement`` boolean remains the source of truth.
    """
    return resolve_mode(managed) is AIWatchMode.ENFORCE


def resolve_mode(managed: ManagedConfig | None = None) -> AIWatchMode:
    """Resolve explicit ``Mode`` first, then fall back to ``Enforcement``.

    Invalid values are treated as absent so a typo cannot silently discard a
    fleet's existing legacy enforcement setting.
    """
    if managed is None:
        managed = read_managed_config()
    mode = _parse_mode(managed.get("mode"))
    if mode is not None:
        return mode
    if managed.get("enforcement") is True:
        return AIWatchMode.ENFORCE
    return AIWatchMode.MONITOR


def resolve_install_hooks(managed: ManagedConfig | None = None) -> bool:
    """Whether this deployment wants any hooks installed at all.

    Protect and Enforce require scanner-capable hooks. Monitor requires hooks
    when Sessions or metadata-only MCP usage observation is enabled. A valid
    Mode overrides legacy Enforcement; absent/invalid Mode preserves the old
    bool mapping. The fail-closed default is Monitor + Sessions off, which
    removes Runlayer hook entries while preserving third-party hooks.
    """
    if managed is None:
        managed = read_managed_config()
    mode = resolve_mode(managed)
    sessions = bool(managed.get("sessions", False))
    # Delegate the metadata term so install and dispatch agree on what the
    # metadata-only profile requires (explicit Sessions=false). A plist with
    # MCPUsageMetadata=true but the Sessions key absent must fail closed to
    # no hooks — an independent term here would install hooks that dispatch
    # then runs in the full Monitor profile.
    return (
        mode is not AIWatchMode.MONITOR
        or sessions
        or resolve_mcp_usage_metadata_only(managed)
    )


def resolve_mcp_usage_metadata_only(
    managed: ManagedConfig | None = None,
) -> bool:
    """Whether hooks must emit only MCP call names, without session content."""
    if managed is None:
        managed = read_managed_config()
    return (
        resolve_mode(managed) is AIWatchMode.MONITOR
        and managed.get("sessions") is False
        and managed.get("mcp_usage_metadata") is True
    )


def daemon_gate_open(managed: ManagedConfig) -> bool:
    """Whether the org-key rollout gate enables hook daemon IPC.

    Single predicate for both sides of the IPC boundary (client dispatch and
    daemon serve/drain) so the enablement decision cannot drift.
    """
    org_api_key = managed.get("org_api_key")
    return (
        isinstance(org_api_key, str)
        and bool(org_api_key)
        and managed.get("daemon_enabled") is True
    )


def resolve_sync_skills(managed: ManagedConfig | None = None) -> bool:
    """Whether native skill sync runs on the scan tick.

    On by default. MDM can disable it explicitly with the ``SyncSkills``
    boolean without touching the rest of the scan/hook deployment.
    """
    if managed is None:
        managed = read_managed_config()
    return bool(managed.get("sync_skills", True))


def resolve_llm_routing(managed: ManagedConfig | None = None) -> bool:
    """Whether local AI clients should route through the LLM gateway."""
    if managed is None:
        managed = read_managed_config()
    return bool(
        managed.get("llm_routing", False) and managed.get("llm_routing_base_url", "")
    )


def resolve_auto_update(managed: ManagedConfig | None = None) -> bool:
    """Whether the privileged AI Watch self-update job may install a target.

    Auto-update is on by default. MDM can disable it explicitly with the
    ``AutoUpdate`` boolean without removing the scheduler or credentials.
    """
    if managed is None:
        managed = read_managed_config()
    return bool(managed.get("auto_update", True))


def _merge_first_wins(result: ManagedConfig, parsed: ManagedConfig) -> None:
    parsed_dict = cast(dict[str, object], parsed)
    result_dict = cast(dict[str, object], result)
    for _, attr in _STRING_FIELDS:
        if attr in parsed_dict and attr not in result_dict:
            result_dict[attr] = parsed_dict[attr]

    # Mode supersedes legacy Enforcement only within the same trust source.
    # Once a higher-priority source supplies either field, lower-priority
    # sources must not fill the other one and cross-override that policy.
    policy_fields = ("mode", "enforcement")
    if not any(field in result_dict for field in policy_fields):
        for field in policy_fields:
            if field in parsed_dict:
                result_dict[field] = parsed_dict[field]

    for _, attr in _BOOL_FIELDS:
        if attr != "enforcement" and attr in parsed_dict and attr not in result_dict:
            result_dict[attr] = parsed_dict[attr]
    for _, attr in _INT_FIELDS:
        if attr in parsed_dict and attr not in result_dict:
            result_dict[attr] = parsed_dict[attr]


def _read_macos(paths: tuple[Path, ...]) -> ManagedConfig:
    # First-wins merge across plists (matches _read_windows registry merging).
    result: ManagedConfig = {}
    for path in paths:
        try:
            with path.open("rb") as f:
                data = plistlib.load(f)
        except (FileNotFoundError, PermissionError, OSError):
            continue
        except plistlib.InvalidFileException:
            continue
        _merge_first_wins(result, _parse_mapping(data))
    return result


def _read_linux(paths: tuple[Path, ...]) -> ManagedConfig:
    # First-wins merge across config files (matches _read_macos plist merging).
    result: ManagedConfig = {}
    for path in paths:
        try:
            with path.open("rb") as f:
                data = json.load(f)
        except (FileNotFoundError, PermissionError, OSError):
            continue
        except (ValueError, UnicodeDecodeError):
            # json.JSONDecodeError subclasses ValueError.
            continue
        _merge_first_wins(result, _parse_mapping(data))
    return result


def _read_windows() -> ManagedConfig:
    if winreg is None:
        return {}

    result: ManagedConfig = {}
    paths = (REG_KEY_PATH,)
    if not runtime.is_aiwatch_runtime():
        paths = (CLI_REG_KEY_PATH, REG_KEY_PATH)
    # Domain-major, matching macOS: the CLI path in either hive beats the
    # AI Watch path, so the same "AI Watch at machine layer, CLI at user
    # layer" scenario resolves identically on both platforms. Within a
    # domain, HKLM beats HKCU.
    for path in paths:
        for hive in (winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER):
            try:
                with winreg.OpenKey(hive, path, 0, winreg.KEY_READ) as key:
                    parsed: ManagedConfig = {}
                    parsed_dict = cast(dict[str, object], parsed)
                    for reg_name, attr in _STRING_FIELDS:
                        str_value = _reg_read_string(key, reg_name)
                        if str_value:
                            parsed_dict[attr] = str_value
                    mode = _parse_mode(_reg_read_string(key, MODE_KEY))
                    if mode is not None:
                        parsed_dict["mode"] = mode
                    for reg_name, attr in _BOOL_FIELDS:
                        bool_value = _reg_read_bool(key, reg_name)
                        if bool_value is not None:
                            parsed_dict[attr] = bool_value
                    for reg_name, attr in _INT_FIELDS:
                        int_value = _reg_read_int(key, reg_name)
                        if int_value is not None:
                            parsed_dict[attr] = int_value
            except OSError:
                continue
            _merge_first_wins(result, parsed)
    return result


def _reg_read_string(key: object, name: str) -> str | None:
    if winreg is None:
        return None
    try:
        value, reg_type = winreg.QueryValueEx(key, name)
    except FileNotFoundError:
        return None
    if reg_type != winreg.REG_SZ:
        return None
    if not isinstance(value, str) or not value or _is_placeholder(value):
        return None
    return value


def _reg_read_bool(key: object, name: str) -> bool | None:
    """Read a REG_DWORD as bool (0 -> False, non-zero -> True). None when absent/wrong-type."""
    if winreg is None:
        return None
    try:
        value, reg_type = winreg.QueryValueEx(key, name)
    except FileNotFoundError:
        return None
    if reg_type != winreg.REG_DWORD:
        return None
    if not isinstance(value, int):
        return None
    return value != 0


def _reg_read_int(key: object, name: str) -> int | None:
    """Read a positive REG_DWORD as int. None when absent/wrong-type/<= 0.

    REG_DWORD always reads back as a plain int (never bool), so only the
    positive-value guard is needed; range clamping happens downstream.
    """
    if winreg is None:
        return None
    try:
        value, reg_type = winreg.QueryValueEx(key, name)
    except FileNotFoundError:
        return None
    if reg_type != winreg.REG_DWORD:
        return None
    if not isinstance(value, int) or value <= 0:
        return None
    return value


def _parse_mapping(data: object) -> ManagedConfig:
    if not isinstance(data, dict):
        return {}
    mapping = cast(dict[str, object], data)
    result: ManagedConfig = {}
    result_dict = cast(dict[str, object], result)
    mode = _parse_mode(mapping.get(MODE_KEY))
    if mode is not None:
        result_dict["mode"] = mode
    for plist_key, attr in _STRING_FIELDS:
        value = mapping.get(plist_key)
        if isinstance(value, str) and value and not _is_placeholder(value):
            result_dict[attr] = value
    for plist_key, attr in _BOOL_FIELDS:
        value = mapping.get(plist_key)
        # Reject ints (plistlib gives `True is 1` parity, but `isinstance(1, bool)` is False, so
        # we only accept literal bool nodes; string "false" is dropped by the type check).
        if isinstance(value, bool):
            result_dict[attr] = value
    for plist_key, attr in _INT_FIELDS:
        value = mapping.get(plist_key)
        # Accept positive <integer> nodes only. `isinstance(True, int)` is True, so
        # exclude bool explicitly; non-int and <= 0 are dropped (treated as absent).
        if isinstance(value, int) and not isinstance(value, bool) and value > 0:
            result_dict[attr] = value
    return result
