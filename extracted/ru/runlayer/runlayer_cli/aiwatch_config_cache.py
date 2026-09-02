"""Protected local cache for backend-authoritative AI Watch settings."""

from __future__ import annotations

import hashlib
import hmac
import json
import os
import platform
import sys
import tempfile
from pathlib import Path
from typing import Literal, TypedDict, cast

if sys.version_info >= (3, 11):
    from typing import NotRequired
else:
    from typing_extensions import NotRequired

if sys.platform == "win32":
    import winreg
else:
    winreg = None  # type: ignore[assignment]

MACOS_CACHE_PATH = Path("/var/db/com.runlayer.aiwatch/backend-config.json")
# Root-written 0644 under a root-owned 0755 dir — same trust model as macOS:
# any user can read the snapshot, only root can replace it. Written by the
# root cron refresh step (run-aiwatch-scan.sh -> ``aiwatch config refresh``).
LINUX_CACHE_PATH = Path("/var/lib/runlayer/aiwatch/backend-config.json")
WINDOWS_REG_KEY_PATH = r"Software\Runlayer\AIWatch"
WINDOWS_CONFIG_VALUE = "BackendConfig"

_CONFIG_VERSION: Literal[1] = 1
_VALID_MODES = frozenset({"monitor", "protect", "enforce"})
_MAX_PROJECT_DEPTH = 20
_MAX_PROJECT_TIMEOUT = 300

SyncedAIWatchMode = Literal["monitor", "protect", "enforce"]


class SyncedAIWatchConfig(TypedDict):
    """Complete backend-owned settings snapshot understood by this binary."""

    version: Literal[1]
    daemon_enabled: bool
    llm_routing: NotRequired[bool]
    llm_routing_base_url: NotRequired[str]
    remove_uv_tool: bool
    mode: SyncedAIWatchMode
    sessions: bool
    mcp_usage_metadata: bool
    browser_mode: SyncedAIWatchMode
    browser_sessions: bool
    browser_extension_enabled: NotRequired[bool]
    hook_wire_encodings: NotRequired[tuple[str, ...]]
    gzip_hooks: NotRequired[bool]
    browser_extension_update_url: NotRequired[str]
    firefox_browser_extension_install_url: NotRequired[str]
    detect_processes: bool
    detect_containers: bool
    detect_disguised_skills: bool
    artifact_lookup_cache: bool
    project_depth: int
    project_timeout: int


def parse_aiwatch_config(data: object) -> SyncedAIWatchConfig:
    """Validate one complete snapshot; partial or invalid state is rejected."""
    if not isinstance(data, dict):
        raise ValueError("AI Watch config must be an object")
    payload = cast(dict[str, object], data)
    if type(payload.get("version")) is not int or payload["version"] != 1:
        raise ValueError("invalid AI Watch config version")

    mode = payload.get("mode")
    if not isinstance(mode, str) or mode not in _VALID_MODES:
        raise ValueError("invalid AI Watch mode")
    browser_mode = payload.get("browser_mode", mode)
    if not isinstance(browser_mode, str) or browser_mode not in _VALID_MODES:
        raise ValueError("invalid browser AI Watch mode")
    browser_sessions = payload.get("browser_sessions", payload.get("sessions"))
    if type(browser_sessions) is not bool:
        raise ValueError("invalid AI Watch config field: browser_sessions")
    daemon_enabled = payload.get("daemon_enabled", False)
    if type(daemon_enabled) is not bool:
        daemon_enabled = False
    llm_routing = payload.get("llm_routing", False)
    if type(llm_routing) is not bool:
        llm_routing = False
    llm_routing_base_url = payload.get("llm_routing_base_url")
    if llm_routing_base_url is not None and (
        not isinstance(llm_routing_base_url, str) or not llm_routing_base_url
    ):
        llm_routing_base_url = None
    mcp_usage_metadata = payload.get("mcp_usage_metadata", False)
    if type(mcp_usage_metadata) is not bool:
        raise ValueError("invalid AI Watch config field: mcp_usage_metadata")
    # Wire-codec capability advertisement: unknown names are dropped (a
    # future backend codec must not make this client claim support), and a
    # malformed value fails dark to absent — downstream falls back to gzip.
    raw_encodings = payload.get("hook_wire_encodings")
    hook_wire_encodings: tuple[str, ...] | None = None
    if isinstance(raw_encodings, list):
        # Lazy on purpose: this module sits on the CLI startup path
        # (main -> mdm_config), and a top-level hook_transport import drags
        # the whole SDK package onto every invocation — the eager-load
        # contract cli/AGENTS.md documents and
        # test_main_does_not_eager_load_relay enforces.
        from runlayer_sdk.hook_transport import KNOWN_WIRE_ENCODINGS

        hook_wire_encodings = tuple(
            e for e in raw_encodings if isinstance(e, str) and e in KNOWN_WIRE_ENCODINGS
        )

    remove_uv_tool = payload.get("remove_uv_tool", False)
    if type(remove_uv_tool) is not bool:
        remove_uv_tool = False
    detect_disguised_skills = payload.get("detect_disguised_skills", False)
    if type(detect_disguised_skills) is not bool:
        detect_disguised_skills = False
    artifact_lookup_cache = payload.get("artifact_lookup_cache", False)
    if type(artifact_lookup_cache) is not bool:
        artifact_lookup_cache = False

    # Optional-field policy: REQUIRED fields raise (whole snapshot rejected),
    # COERCED fields (remove_uv_tool, daemon_enabled) default on malformed
    # values because a boolean answer is always needed, and OPTIONAL rollout
    # gates like this one fail dark to absent — downstream falls back to the
    # locally-managed value. Pick the weakest tier a new field can live with.
    gzip_hooks = payload.get("gzip_hooks")

    browser_extension_enabled = payload.get("browser_extension_enabled")
    if (
        browser_extension_enabled is not None
        and type(browser_extension_enabled) is not bool
    ):
        raise ValueError("invalid AI Watch config field: browser_extension_enabled")
    browser_extension_update_url = payload.get("browser_extension_update_url")
    if browser_extension_update_url is not None and (
        not isinstance(browser_extension_update_url, str)
        or not browser_extension_update_url
    ):
        raise ValueError("invalid AI Watch config field: browser_extension_update_url")
    firefox_browser_extension_install_url = payload.get(
        "firefox_browser_extension_install_url"
    )
    if firefox_browser_extension_install_url is not None and (
        not isinstance(firefox_browser_extension_install_url, str)
        or not firefox_browser_extension_install_url
    ):
        raise ValueError(
            "invalid AI Watch config field: firefox_browser_extension_install_url"
        )

    config: SyncedAIWatchConfig = {
        "version": _CONFIG_VERSION,
        # Optional rollout gate: old/malformed values fail dark without
        # invalidating the otherwise-complete last-known-good snapshot.
        "daemon_enabled": daemon_enabled,
        "remove_uv_tool": remove_uv_tool,
        "mode": cast(SyncedAIWatchMode, mode),
        "sessions": _require_bool(payload, "sessions"),
        "mcp_usage_metadata": mcp_usage_metadata,
        "browser_mode": cast(SyncedAIWatchMode, browser_mode),
        "browser_sessions": browser_sessions,
        "detect_processes": _require_bool(payload, "detect_processes"),
        "detect_containers": _require_bool(payload, "detect_containers"),
        "detect_disguised_skills": detect_disguised_skills,
        "artifact_lookup_cache": artifact_lookup_cache,
        "project_depth": _require_bounded_int(
            payload,
            "project_depth",
            maximum=_MAX_PROJECT_DEPTH,
        ),
        "project_timeout": _require_bounded_int(
            payload,
            "project_timeout",
            maximum=_MAX_PROJECT_TIMEOUT,
        ),
    }
    if hook_wire_encodings is not None:
        config["hook_wire_encodings"] = hook_wire_encodings
    if type(browser_extension_enabled) is bool:
        config["browser_extension_enabled"] = browser_extension_enabled
    if type(gzip_hooks) is bool:
        config["gzip_hooks"] = gzip_hooks
    if "llm_routing" in payload:
        config["llm_routing"] = llm_routing
    if isinstance(llm_routing_base_url, str):
        config["llm_routing_base_url"] = llm_routing_base_url
    if isinstance(browser_extension_update_url, str):
        config["browser_extension_update_url"] = browser_extension_update_url
    if isinstance(firefox_browser_extension_install_url, str):
        config["firefox_browser_extension_install_url"] = (
            firefox_browser_extension_install_url
        )
    return config


def hash_org_api_key(org_api_key: str) -> str:
    """Return the key identity used to bind cached state to one configuration."""
    return hashlib.sha256(org_api_key.encode()).hexdigest()


def read_backend_config(org_api_key: str) -> SyncedAIWatchConfig | None:
    """Read a valid snapshot cached for this org key on supported hosts."""
    system = platform.system()
    if system == "Darwin":
        return _read_posix(MACOS_CACHE_PATH, org_api_key)
    if system == "Windows":
        return _read_windows(org_api_key)
    if system == "Linux":
        return _read_posix(LINUX_CACHE_PATH, org_api_key)
    return None


def write_backend_config(
    config: SyncedAIWatchConfig,
    org_api_key: str,
) -> bool:
    """Persist one complete snapshot on supported hosts."""
    validated_config = parse_aiwatch_config(config)
    payload = {
        **validated_config,
        "org_api_key_hash": hash_org_api_key(org_api_key),
    }

    system = platform.system()
    if system == "Darwin":
        _write_posix(MACOS_CACHE_PATH, payload)
        return True
    if system == "Windows":
        _write_windows(payload)
        return True
    if system == "Linux":
        # Both /var/lib/runlayer and /var/lib/runlayer/aiwatch are Runlayer-owned.
        _write_posix(LINUX_CACHE_PATH, payload, owned_directory_depth=2)
        return True
    return False


def _require_bool(payload: dict[str, object], key: str) -> bool:
    value = payload.get(key)
    if type(value) is not bool:
        raise ValueError(f"invalid AI Watch config field: {key}")
    return value


def _require_bounded_int(
    payload: dict[str, object],
    key: str,
    *,
    maximum: int,
) -> int:
    value = payload.get(key)
    if type(value) is not int or value < 1 or value > maximum:
        raise ValueError(f"invalid AI Watch config field: {key}")
    return value


def _read_posix(cache_path: Path, org_api_key: str) -> SyncedAIWatchConfig | None:
    try:
        data = json.loads(cache_path.read_text(encoding="utf-8"))
    except (FileNotFoundError, PermissionError, OSError, ValueError, UnicodeError):
        return None
    return _read_cache_payload(data, org_api_key)


def _write_posix(
    cache_path: Path,
    payload: dict[str, object],
    *,
    owned_directory_depth: int = 1,
) -> None:
    """Atomically publish one world-readable snapshot under 0755 directories.

    ``owned_directory_depth`` counts trailing Runlayer-owned directories
    (e.g. ``runlayer/aiwatch``) that are always forced to 0755, healing trees
    a prior restrictive-umask run left 0700 and unreadable to non-root scan
    children. Pre-existing system ancestors keep their modes; ancestors this
    write creates are opened up because readers must traverse them.
    """
    parent = cache_path.parent
    missing_ancestors: list[Path] = []
    ancestor = parent.parent
    while not ancestor.exists():
        missing_ancestors.append(ancestor)
        ancestor = ancestor.parent

    parent.mkdir(mode=0o755, parents=True, exist_ok=True)
    for missing_ancestor in missing_ancestors:
        missing_ancestor.chmod(0o755)
    owned_directory = parent
    for _ in range(owned_directory_depth):
        owned_directory.chmod(0o755)
        owned_directory = owned_directory.parent
    fd, temporary_name = tempfile.mkstemp(
        dir=parent,
        prefix=f".{cache_path.name}.",
    )
    temporary_path = Path(temporary_name)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as temporary_file:
            json.dump(payload, temporary_file, separators=(",", ":"))
            temporary_file.write("\n")
            temporary_file.flush()
            os.fsync(temporary_file.fileno())
        os.chmod(temporary_path, 0o644)
        os.replace(temporary_path, cache_path)
    finally:
        temporary_path.unlink(missing_ok=True)


def _read_windows(org_api_key: str) -> SyncedAIWatchConfig | None:
    if winreg is None:
        return None
    try:
        with winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            WINDOWS_REG_KEY_PATH,
            0,
            winreg.KEY_READ,
        ) as key:
            serialized = _read_reg_string(key, WINDOWS_CONFIG_VALUE)
    except OSError:
        return None
    if serialized is None:
        return None
    try:
        data = json.loads(serialized)
    except (ValueError, UnicodeError):
        return None
    return _read_cache_payload(data, org_api_key)


def _write_windows(payload: dict[str, object]) -> None:
    if winreg is None:
        raise OSError("Windows registry is unavailable")
    serialized = json.dumps(payload, separators=(",", ":"))
    with winreg.CreateKeyEx(
        winreg.HKEY_LOCAL_MACHINE,
        WINDOWS_REG_KEY_PATH,
        0,
        winreg.KEY_SET_VALUE,
    ) as key:
        winreg.SetValueEx(key, WINDOWS_CONFIG_VALUE, 0, winreg.REG_SZ, serialized)


def _read_reg_string(key: object, name: str) -> str | None:
    if winreg is None:
        return None
    try:
        value, reg_type = winreg.QueryValueEx(key, name)
    except FileNotFoundError:
        return None
    if reg_type != winreg.REG_SZ or not isinstance(value, str) or not value:
        return None
    return value


def _read_cache_payload(
    data: object,
    org_api_key: str,
) -> SyncedAIWatchConfig | None:
    if not isinstance(data, dict):
        return None
    payload = cast(dict[str, object], data)
    cached_hash = payload.get("org_api_key_hash")
    if not isinstance(cached_hash, str) or not hmac.compare_digest(
        cached_hash,
        hash_org_api_key(org_api_key),
    ):
        return None
    try:
        return parse_aiwatch_config(payload)
    except ValueError:
        return None
