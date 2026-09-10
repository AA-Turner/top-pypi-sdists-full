"""Dependency-free, best-effort AI Watch cleanup for macOS uninstallers."""

from __future__ import annotations

import copy
import io
import json
import os
import plistlib
import secrets
import shlex
import shutil
import signal
import stat
import subprocess
import time
from pathlib import Path
from typing import Any, Callable, TypedDict
from urllib.parse import urlparse


_RUNLAYER_SCRIPT_NAMES = frozenset(
    {
        "aiwatch-hook",
        "aiwatch-hook.exe",
        "aiwatch-enforce",
        "aiwatch-enforce.exe",
        "runlayer-hook",
        "runlayer-hook.exe",
        "runlayer-hook.sh",
        "runlayer-cursor-hook.sh",
        "runlayer-claude-hook.sh",
    }
)
_COMMAND_FIELDS = ("command", "bash", "powershell")
_RUNLAYER_CHROME_EXTENSION_ID = "jijfcalfdbnjfpfcalkodmgmfijpfddi"
_RUNLAYER_FIREFOX_EXTENSION_ID = "aiwatch@runlayer.com"
_MANAGED_IGNORE_START = "# >>> Runlayer managed - do not edit >>>"
_MANAGED_IGNORE_END = "# <<< Runlayer managed <<<"
_CLINE_MARKER = "# runlayer-owned Cline hook — safe to delete"
_MAX_CONFIG_BYTES = 16 * 1024 * 1024

_SUBPROCESS_TIMEOUT_SECONDS = 5.0
_HOME_CHILD_TIMEOUT_SECONDS = 8.0
_GLOBAL_WATCHDOG_SECONDS = 120
_UNINSTALL_LOG_ROOT = Path("/Library/Logs")
_UNINSTALL_LOG_PATH = _UNINSTALL_LOG_ROOT / "Runlayer" / "aiwatch-uninstall.log"

_USERS_ROOT = Path("/Users")
_ROOT_HOME = Path("/private/var/root")
_SYSTEM_PREFERENCES_DIR = Path("/Library/Preferences")
_MACOS_MANAGED_CONFIG_PATHS = (
    Path("/Library/Managed Preferences/com.runlayer.aiwatch.plist"),
    _SYSTEM_PREFERENCES_DIR / "com.runlayer.aiwatch.plist",
)
_GROK_HOME_KEY = "GrokHome"
_HOST_KEY = "Host"
_AGENT_LABELS = (
    "com.runlayer.aiwatch",
    "com.runlayer.aiwatch.enroll",
    "com.runlayer.aiwatch.daemon",
)
_DAEMON_LABELS = (
    "com.runlayer.aiwatch.bootstrap",
    "com.runlayer.aiwatch.update",
)

_ENTERPRISE_JSON_HOOK_PATHS: tuple[tuple[Path, bool], ...] = (
    (Path("/Library/Application Support/Cursor/hooks.json"), True),
    (Path("/Library/Application Support/Windsurf/hooks.json"), True),
    (Path("/private/etc/codex/hooks.json"), True),
    (Path("/Library/Application Support/QwenCode/settings.json"), False),
    (Path("/Library/Application Support/GeminiCli/settings.json"), True),
    (Path("/private/etc/github-copilot/policy.d/runlayer.json"), True),
    (
        Path("/Library/Application Support/ClaudeCode/managed-settings.json"),
        False,
    ),
)
_ENTERPRISE_LEGACY_ROOTS: tuple[tuple[Path, str | None], ...] = (
    (
        Path("/Library/Application Support/Cursor"),
        "runlayer-cursor-hook.sh",
    ),
    (
        Path("/Library/Application Support/ClaudeCode"),
        "runlayer-claude-hook.sh",
    ),
    (Path("/Library/Application Support/Windsurf"), None),
    (Path("/Library/Application Support/GeminiCli"), None),
    (Path("/private/etc/codex"), None),
    (Path("/private/etc/github-copilot/policy.d"), None),
)
_PACKAGE_PATHS = (
    Path("/usr/local/bin/aiwatch"),
    Path("/usr/local/bin/aiwatch-hook"),
    Path("/usr/local/bin/aiwatch-enforce"),
    Path("/usr/local/lib/runlayer/aiwatch"),
    Path("/usr/local/lib/runlayer/aiwatch-enforce"),
    Path("/Library/LaunchAgents/com.runlayer.aiwatch.plist"),
    Path("/Library/LaunchAgents/com.runlayer.aiwatch.enroll.plist"),
    Path("/Library/LaunchAgents/com.runlayer.aiwatch.daemon.plist"),
    Path("/Library/LaunchDaemons/com.runlayer.aiwatch.bootstrap.plist"),
    Path("/Library/LaunchDaemons/com.runlayer.aiwatch.update.plist"),
    Path("/var/db/com.runlayer.aiwatch"),
    _SYSTEM_PREFERENCES_DIR / "com.runlayer.aiwatch.plist",
    _SYSTEM_PREFERENCES_DIR / "com.runlayer.aiwatch.version.plist",
    Path("/Library/Google/Chrome/NativeMessagingHosts/com.runlayer.aiwatch.json"),
    Path(
        "/Library/Application Support/Mozilla/NativeMessagingHosts/"
        "com.runlayer.aiwatch.json"
    ),
)
_RECEIPT_IDS = (
    "com.runlayer.aiwatch",
    "com.runlayer.aiwatch-enforce",
)
_FIREFOX_CANONICAL_POLICY_PATH = _SYSTEM_PREFERENCES_DIR / "org.mozilla.firefox.plist"
_FIREFOX_POLICY_PATHS = (
    _FIREFOX_CANONICAL_POLICY_PATH,
    Path("/Library/Managed Preferences/org.mozilla.firefox.plist"),
)
_CHROME_FORCE_INSTALL_POLICY_PATH = Path(
    "/Library/Managed Preferences/com.google.Chrome.plist"
)
_CHROME_MANAGED_PREFERENCES_DIR = Path("/Library/Managed Preferences")
_CHROME_EXTERNAL_EXTENSIONS_DIR = Path(
    "/Library/Application Support/Google/Chrome/External Extensions"
)
_CHROME_TENANT_MANIFEST_PREFIX = "/api/v1/binary-packages/browser-extension/chrome/"

# LLM routing state the dep-free uninstaller must mirror from the install-side
# ``llm_routing.unroute`` teardown for MDM scope. These constants are dep-free
# ports of the matching keys in ``hook_install.llm_routing`` (which the
# uninstaller cannot import without pulling in tolerant_json/mdm_config/etc.).
_CLAUDE_HELPER_KEY = "apiKeyHelper"
_CLAUDE_ROUTING_ENV_KEYS = (
    "ANTHROPIC_BASE_URL",
    "CLAUDE_CODE_API_KEY_HELPER_TTL_MS",
    "ANTHROPIC_AUTH_TOKEN",
    "ANTHROPIC_API_KEY",
    "CLAUDE_CODE_OAUTH_TOKEN",
    "CLAUDE_CODE_USE_BEDROCK",
    "CLAUDE_CODE_USE_VERTEX",
    "CLAUDE_CODE_USE_FOUNDRY",
)
_CODEX_PROVIDER_TABLE = "[model_providers.runlayer]"
_LLM_ROUTING_CREDENTIAL_RELATIVE_PATH = (
    Path(".runlayer") / "aiwatch" / "llm-routing-credential"
)


class _FileSnapshot(TypedDict):
    data: bytes
    mode: int
    uid: int
    gid: int
    device: int
    inode: int


class _TextFileSnapshot(_FileSnapshot):
    text: str


class _ParentHandle(TypedDict):
    fds: list[int]
    parent_fd: int
    name: str


class _YamlItem(TypedDict):
    start: int
    end: int
    runlayer: bool


class _YamlEvent(TypedDict):
    start: int
    end: int
    items: list[_YamlItem]


class _LocalUsers(TypedDict):
    homes: list[Path]
    uids: set[int]


class _ManagedCleanupConfig(TypedDict):
    grok_home: str | None
    host: str | None


class _RemovalResult(TypedDict):
    ok: bool
    changed: bool


class _PreferenceCleanupResult(TypedDict):
    ok: bool
    preferences_changed: bool


def _normalized_token(token: str) -> str:
    return token.strip().strip("\"'").strip(";&|()")


def _token_basename(token: str) -> str:
    normalized = _normalized_token(token).replace("\\", "/")
    return normalized.rsplit("/", 1)[-1].casefold()


def _command_tokens(command: str) -> list[str]:
    try:
        return shlex.split(command, posix=True)
    except ValueError:
        try:
            return shlex.split(command, posix=False)
        except ValueError:
            return command.split()


def _is_script_boundary(char: str, *, before: bool) -> bool:
    punctuation = "/\\\"'&" if before else "\"';&|"
    return char.isspace() or char in punctuation


def _contains_runlayer_script(command: str) -> bool:
    folded = command.casefold()
    for name in _RUNLAYER_SCRIPT_NAMES:
        start = 0
        while True:
            index = folded.find(name, start)
            if index < 0:
                break
            end = index + len(name)
            before_ok = index == 0 or _is_script_boundary(
                folded[index - 1], before=True
            )
            after_ok = end == len(folded) or _is_script_boundary(
                folded[end], before=False
            )
            if before_ok and after_ok:
                return True
            start = index + 1
    return False


def is_runlayer_command(command: str) -> bool:
    """Return whether a hook command invokes a current or legacy Runlayer hook."""
    if not isinstance(command, str) or not command.strip():
        return False

    tokens = _command_tokens(command)
    for token in tokens:
        if _token_basename(token) in _RUNLAYER_SCRIPT_NAMES:
            return True
    if _contains_runlayer_script(command):
        return True

    normalized = [_normalized_token(token).casefold() for token in tokens]
    basenames = [_token_basename(token) for token in tokens]
    for index, basename in enumerate(basenames[:-1]):
        if basename in {"aiwatch", "aiwatch.exe", "runlayer", "runlayer.exe"}:
            if normalized[index + 1] == "hook":
                return True
    return any(
        token == "-m" and normalized[index + 1] == "runlayer_cli.hook"
        for index, token in enumerate(normalized[:-1])
    )


def _is_runlayer_helper(value: object) -> bool:
    """``<aiwatch> credential claude`` in any of the forms the installer writes.

    Dep-free port of ``hook_install.llm_routing._is_runlayer_helper``: matches the
    credential-helper command shape (head + ``["credential", "claude"]``) so foreign
    helpers — including ``/opt/acme/credential claude`` — are preserved.
    """
    if not isinstance(value, str):
        return False
    parts = value.split()
    if parts[-2:] != ["credential", "claude"]:
        return False
    head = parts[:-2]
    if head[-2:] == ["-m", "runlayer_cli.aiwatch"]:
        return True
    if not head:
        return False
    # Separator-agnostic: a quoted Windows path splits on its spaces too.
    name = head[-1].strip('"').replace("\\", "/").rsplit("/", 1)[-1].casefold()
    return name in {"aiwatch", "aiwatch.exe"}


def _entry_command(entry: dict[str, Any]) -> str:
    command = entry.get("command")
    if not isinstance(command, str):
        return ""
    args = entry.get("args")
    if not isinstance(args, list) or not all(isinstance(arg, str) for arg in args):
        return command
    quoted = (
        len(command) >= 2 and command[0] == command[-1] and command[0] in {'"', "'"}
    )
    executable = (
        f'"{command}"'
        if any(char.isspace() for char in command) and not quoted
        else command
    )
    return " ".join((executable, *args))


def _without_runlayer_entry(entry: dict[str, Any]) -> dict[str, Any] | None:
    result = copy.deepcopy(entry)
    nested = result.get("hooks")
    nested_changed = False
    if isinstance(nested, list):
        kept_nested: list[Any] = []
        for inner in nested:
            if isinstance(inner, dict):
                cleaned = _without_runlayer_entry(inner)
                if cleaned is None:
                    nested_changed = True
                else:
                    nested_changed = nested_changed or cleaned != inner
                    kept_nested.append(cleaned)
            else:
                kept_nested.append(copy.deepcopy(inner))
        if nested_changed:
            if kept_nested:
                result["hooks"] = kept_nested
            else:
                result.pop("hooks", None)

    removed_command = False
    command = result.get("command")
    if isinstance(command, str):
        if is_runlayer_command(_entry_command(result)):
            result.pop("command", None)
            result.pop("args", None)
            removed_command = True

    for field in ("bash", "powershell"):
        value = result.get(field)
        if isinstance(value, str):
            if is_runlayer_command(value):
                result.pop(field, None)
                removed_command = True

    if nested_changed or removed_command:
        has_command = any(
            isinstance(result.get(field), str) and bool(result[field].strip())
            for field in _COMMAND_FIELDS
        )
        has_nested = isinstance(result.get("hooks"), list) and bool(result["hooks"])
        if not has_command and not has_nested:
            return None
    return result


def without_runlayer_hooks(hooks: dict[str, Any]) -> dict[str, Any]:
    """Remove Runlayer hooks while preserving unrelated flat and nested entries."""
    if not isinstance(hooks, dict):
        return {}
    result: dict[str, Any] = {}
    for event_name, entries in hooks.items():
        if not isinstance(entries, list):
            result[event_name] = copy.deepcopy(entries)
            continue
        kept: list[Any] = []
        for entry in entries:
            if isinstance(entry, dict):
                cleaned = _without_runlayer_entry(entry)
                if cleaned is not None:
                    kept.append(cleaned)
            else:
                kept.append(copy.deepcopy(entry))
        if kept:
            result[event_name] = kept
    return result


def _path_is_safe(path: Path, anchor: Path | None) -> bool:
    if anchor is None:
        try:
            return not path.is_symlink()
        except OSError:
            return False

    try:
        relative = path.relative_to(anchor)
    except ValueError:
        return False
    if not relative.parts or ".." in relative.parts:
        return False

    current = anchor
    for part in relative.parts:
        try:
            mode = current.lstat().st_mode
        except FileNotFoundError:
            mode = 0
        except OSError:
            return False
        if mode and stat.S_ISLNK(mode):
            return False
        current /= part
    try:
        mode = current.lstat().st_mode
    except FileNotFoundError:
        return True
    except OSError:
        return False
    return not stat.S_ISLNK(mode)


_DIRECTORY_OPEN_FLAGS = (
    os.O_RDONLY
    | getattr(os, "O_CLOEXEC", 0)
    | getattr(os, "O_DIRECTORY", 0)
    | getattr(os, "O_NOFOLLOW", 0)
)
_FILE_READ_FLAGS = (
    os.O_RDONLY | getattr(os, "O_CLOEXEC", 0) | getattr(os, "O_NOFOLLOW", 0)
)


def _close_descriptors(descriptors: list[int]) -> None:
    for descriptor in reversed(descriptors):
        try:
            os.close(descriptor)
        except OSError:
            pass


def _append_uninstall_log(data: bytes) -> None:
    descriptors: list[int] = []
    try:
        relative = _UNINSTALL_LOG_PATH.relative_to(_UNINSTALL_LOG_ROOT)
        if len(relative.parts) != 2:
            return
        directory_name, file_name = relative.parts

        root_fd = os.open(_UNINSTALL_LOG_ROOT, _DIRECTORY_OPEN_FLAGS)
        descriptors.append(root_fd)
        try:
            os.mkdir(directory_name, 0o755, dir_fd=root_fd)
        except FileExistsError:
            pass

        directory_fd = os.open(
            directory_name,
            _DIRECTORY_OPEN_FLAGS,
            dir_fd=root_fd,
        )
        descriptors.append(directory_fd)
        directory_stat = os.fstat(directory_fd)
        if (
            directory_stat.st_uid != os.geteuid()
            or stat.S_IMODE(directory_stat.st_mode) & 0o022
        ):
            return

        file_fd = os.open(
            file_name,
            os.O_WRONLY
            | os.O_APPEND
            | os.O_CREAT
            | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0),
            0o640,
            dir_fd=directory_fd,
        )
        descriptors.append(file_fd)
        file_stat = os.fstat(file_fd)
        if (
            not stat.S_ISREG(file_stat.st_mode)
            or file_stat.st_uid != os.geteuid()
            or file_stat.st_nlink != 1
            or stat.S_IMODE(file_stat.st_mode) & 0o022
        ):
            return

        view = memoryview(data)
        written = 0
        while written < len(view):
            count = os.write(file_fd, view[written:])
            if count <= 0:
                return
            written += count
    except BaseException:
        pass
    finally:
        _close_descriptors(descriptors)


def _log_phase(name: str, ok: bool) -> None:
    safe_name = name.replace("\r", "\\r").replace("\n", "\\n")
    status = "ok" if ok else "failed"
    data = f"[aiwatch-uninstall] {safe_name}: {status}\n".encode()
    try:
        os.write(2, data)
    except BaseException:
        pass
    _append_uninstall_log(data)


def _attempt_phase(name: str, operation: Callable[[], Any]) -> Any:
    try:
        result = operation()
    except BaseException:
        _log_phase(name, False)
        return None
    if isinstance(result, bool):
        ok = result
    elif isinstance(result, dict) and isinstance(result.get("ok"), bool):
        ok = result["ok"]
    else:
        # Void phases return None; unknown shapes intentionally log success.
        ok = True
    _log_phase(name, ok)
    return result


def _open_anchored_parent(path: Path, anchor: Path) -> _ParentHandle | None:
    try:
        relative = path.relative_to(anchor)
    except ValueError:
        return None
    if not relative.parts or ".." in relative.parts:
        return None

    descriptors: list[int] = []
    try:
        descriptor = os.open(anchor, _DIRECTORY_OPEN_FLAGS)
        descriptors.append(descriptor)
        for part in relative.parts[:-1]:
            descriptor = os.open(
                part,
                _DIRECTORY_OPEN_FLAGS,
                dir_fd=descriptor,
            )
            descriptors.append(descriptor)
    except OSError:
        _close_descriptors(descriptors)
        return None
    return {
        "fds": descriptors,
        "parent_fd": descriptors[-1],
        "name": relative.parts[-1],
    }


def _read_regular_bytes(
    path: Path, *, anchor: Path | None = None
) -> _FileSnapshot | None:
    parent_handle: _ParentHandle | None = None
    if anchor is None:
        if not _path_is_safe(path, None):
            return None
        open_path: str | Path = path
        open_kwargs: dict[str, int] = {}
    else:
        parent_handle = _open_anchored_parent(path, anchor)
        if parent_handle is None:
            return None
        open_path = parent_handle["name"]
        open_kwargs = {"dir_fd": parent_handle["parent_fd"]}
    try:
        descriptor = os.open(open_path, _FILE_READ_FLAGS, **open_kwargs)
    except OSError:
        if parent_handle is not None:
            _close_descriptors(parent_handle["fds"])
        return None
    try:
        opened = os.fstat(descriptor)
        if not stat.S_ISREG(opened.st_mode) or opened.st_size > _MAX_CONFIG_BYTES:
            return None
        chunks: list[bytes] = []
        remaining = _MAX_CONFIG_BYTES + 1
        while remaining > 0:
            chunk = os.read(descriptor, min(65536, remaining))
            if not chunk:
                break
            chunks.append(chunk)
            remaining -= len(chunk)
        data = b"".join(chunks)
        if len(data) > _MAX_CONFIG_BYTES:
            return None
        return {
            "data": data,
            "mode": stat.S_IMODE(opened.st_mode),
            "uid": opened.st_uid,
            "gid": opened.st_gid,
            "device": opened.st_dev,
            "inode": opened.st_ino,
        }
    except OSError:
        return None
    finally:
        os.close(descriptor)
        if parent_handle is not None:
            _close_descriptors(parent_handle["fds"])


def _read_regular_text(
    path: Path, *, anchor: Path | None = None
) -> _TextFileSnapshot | None:
    snapshot = _read_regular_bytes(path, anchor=anchor)
    if snapshot is None:
        return None
    try:
        text = snapshot["data"].decode("utf-8")
    except UnicodeDecodeError:
        return None
    return {
        "data": snapshot["data"],
        "text": text,
        "mode": snapshot["mode"],
        "uid": snapshot["uid"],
        "gid": snapshot["gid"],
        "device": snapshot["device"],
        "inode": snapshot["inode"],
    }


def _load_plist_dict(snapshot: _FileSnapshot) -> dict[str, Any] | None:
    try:
        loaded = plistlib.load(io.BytesIO(snapshot["data"]))
    except (plistlib.InvalidFileException, ValueError, TypeError, OverflowError):
        return None
    return loaded if isinstance(loaded, dict) else None


def _snapshot_matches(path: Path, snapshot: _FileSnapshot) -> bool:
    try:
        current = path.lstat()
    except OSError:
        return False
    return (
        stat.S_ISREG(current.st_mode)
        and current.st_dev == snapshot["device"]
        and current.st_ino == snapshot["inode"]
    )


def _snapshot_matches_at(
    parent_fd: int,
    name: str,
    snapshot: _FileSnapshot,
) -> bool:
    try:
        current = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
    except OSError:
        return False
    return (
        stat.S_ISREG(current.st_mode)
        and current.st_dev == snapshot["device"]
        and current.st_ino == snapshot["inode"]
    )


def _atomic_replace(
    path: Path,
    data: bytes,
    snapshot: _FileSnapshot,
    *,
    anchor: Path | None = None,
) -> bool:
    parent_handle: _ParentHandle | None = None
    if anchor is None:
        if not _path_is_safe(path, None) or not _snapshot_matches(path, snapshot):
            return False
        try:
            directory_fd = os.open(path.parent, _DIRECTORY_OPEN_FLAGS)
        except OSError:
            return False
        target_name = path.name
        descriptors = [directory_fd]
    else:
        parent_handle = _open_anchored_parent(path, anchor)
        if parent_handle is None:
            return False
        directory_fd = parent_handle["parent_fd"]
        target_name = parent_handle["name"]
        descriptors = parent_handle["fds"]
        if not _snapshot_matches_at(directory_fd, target_name, snapshot):
            _close_descriptors(descriptors)
            return False

    temporary_name = (
        f".{path.name}.runlayer-uninstall-{os.getpid()}-{secrets.token_hex(6)}"
    )
    temporary_fd: int | None = None
    try:
        temporary_fd = os.open(
            temporary_name,
            os.O_WRONLY
            | os.O_CREAT
            | os.O_EXCL
            | getattr(os, "O_CLOEXEC", 0)
            | getattr(os, "O_NOFOLLOW", 0),
            snapshot["mode"],
            dir_fd=directory_fd,
        )
        os.fchmod(temporary_fd, snapshot["mode"])
        try:
            os.fchown(temporary_fd, snapshot["uid"], snapshot["gid"])
        except (AttributeError, PermissionError, OSError):
            pass
        view = memoryview(data)
        written = 0
        while written < len(view):
            count = os.write(temporary_fd, view[written:])
            if count <= 0:
                raise OSError("short write")
            written += count
        os.fsync(temporary_fd)
        os.close(temporary_fd)
        temporary_fd = None

        snapshot_matches = (
            _snapshot_matches(path, snapshot)
            if anchor is None
            else _snapshot_matches_at(directory_fd, target_name, snapshot)
        )
        if not snapshot_matches:
            return False
        os.replace(
            temporary_name,
            target_name,
            src_dir_fd=directory_fd,
            dst_dir_fd=directory_fd,
        )
        try:
            os.fsync(directory_fd)
        except OSError:
            pass
        return True
    except OSError:
        return False
    finally:
        if temporary_fd is not None:
            try:
                os.close(temporary_fd)
            except OSError:
                pass
        try:
            os.unlink(temporary_name, dir_fd=directory_fd)
        except OSError:
            pass
        _close_descriptors(descriptors)


def _unlink_snapshot(
    path: Path,
    snapshot: _FileSnapshot,
    *,
    anchor: Path | None = None,
) -> bool:
    if anchor is None:
        if not _path_is_safe(path, None) or not _snapshot_matches(path, snapshot):
            return False
        try:
            path.unlink()
        except OSError:
            return False
        return True

    parent_handle = _open_anchored_parent(path, anchor)
    if parent_handle is None:
        return False
    try:
        if not _snapshot_matches_at(
            parent_handle["parent_fd"],
            parent_handle["name"],
            snapshot,
        ):
            return False
        os.unlink(
            parent_handle["name"],
            dir_fd=parent_handle["parent_fd"],
        )
    except OSError:
        return False
    finally:
        _close_descriptors(parent_handle["fds"])
    return True


def _strip_json_line_comments(text: str) -> str:
    output: list[str] = []
    in_string = False
    index = 0
    while index < len(text):
        char = text[index]
        if in_string:
            output.append(char)
            if char == "\\" and index + 1 < len(text):
                index += 1
                output.append(text[index])
            elif char == '"':
                in_string = False
            index += 1
            continue
        if char == '"':
            in_string = True
            output.append(char)
            index += 1
            continue
        if char == "/" and index + 1 < len(text) and text[index + 1] == "/":
            newline = text.find("\n", index + 2)
            if newline < 0:
                break
            index = newline
            continue
        output.append(char)
        index += 1
    return "".join(output)


def _strip_json_trailing_commas(text: str) -> str:
    output: list[str] = []
    in_string = False
    index = 0
    while index < len(text):
        char = text[index]
        if in_string:
            output.append(char)
            if char == "\\" and index + 1 < len(text):
                index += 1
                output.append(text[index])
            elif char == '"':
                in_string = False
            index += 1
            continue
        if char == '"':
            in_string = True
            output.append(char)
            index += 1
            continue
        if char == ",":
            lookahead = index + 1
            while lookahead < len(text) and text[lookahead].isspace():
                lookahead += 1
            if lookahead < len(text) and text[lookahead] in "]}":
                index += 1
                continue
        output.append(char)
        index += 1
    return "".join(output)


def _load_jsonc_object(text: str) -> dict[str, Any] | None:
    try:
        loaded = json.loads(text)
    except json.JSONDecodeError:
        try:
            loaded = json.loads(
                _strip_json_trailing_commas(_strip_json_line_comments(text))
            )
        except json.JSONDecodeError:
            return None
    return loaded if isinstance(loaded, dict) else None


def _verified_json_bytes(value: dict[str, Any]) -> bytes | None:
    try:
        rendered = json.dumps(value, indent=2) + "\n"
        verified = json.loads(rendered)
    except (TypeError, ValueError, json.JSONDecodeError):
        return None
    if not isinstance(verified, dict) or verified != value:
        return None
    return rendered.encode("utf-8")


def _verified_plist_bytes(value: dict[str, Any]) -> bytes | None:
    try:
        rendered = plistlib.dumps(value, fmt=plistlib.FMT_XML, sort_keys=True)
        verified = plistlib.load(io.BytesIO(rendered))
    except (
        plistlib.InvalidFileException,
        TypeError,
        ValueError,
        OverflowError,
    ):
        return None
    if not isinstance(verified, dict) or verified != value:
        return None
    return rendered


def clean_json_hooks(
    path: Path,
    delete_when_empty: bool = False,
    *,
    _anchor: Path | None = None,
) -> bool:
    """Remove Runlayer entries from a JSON/JSONC ``hooks`` object."""
    path = Path(path)
    snapshot = _read_regular_text(path, anchor=_anchor)
    if snapshot is None:
        return False
    config = _load_jsonc_object(snapshot["text"])
    if config is None:
        return False
    hooks = config.get("hooks")
    if not isinstance(hooks, dict):
        return False

    filtered = without_runlayer_hooks(hooks)
    if filtered == hooks:
        return False

    updated = copy.deepcopy(config)
    if filtered:
        updated["hooks"] = filtered
    else:
        updated.pop("hooks", None)

    if delete_when_empty and not any(key != "version" for key in updated):
        return _unlink_snapshot(path, snapshot, anchor=_anchor)

    rendered = _verified_json_bytes(updated)
    if rendered is None:
        return False
    return _atomic_replace(path, rendered, snapshot, anchor=_anchor)


def _is_toml_table_header(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("[") and stripped.endswith("]")


def _toml_assignment(line: str, key: str) -> str | None:
    stripped = line.strip()
    if stripped.startswith("#"):
        return None
    name, separator, value = stripped.partition("=")
    # TOML allows quoted bare keys; a stale slot spelled that way still counts.
    if separator and name.strip().strip("\"'") == key:
        return value.strip()
    return None


def _toml_table_name(line: str) -> str:
    """Canonical header: TOML allows quoted segments and whitespace around dots."""
    segments: list[str] = []
    for raw in line.strip()[1:-1].split("."):
        segment = raw.strip()
        quoted = len(segment) >= 2 and segment[0] == segment[-1] and segment[0] in "\"'"
        segments.append(segment[1:-1] if quoted else segment)
    return "[" + ".".join(segments) + "]"


def _is_runlayer_toml_table(line: str) -> bool:
    name = _toml_table_name(line)
    return name == _CODEX_PROVIDER_TABLE or name.startswith(
        _CODEX_PROVIDER_TABLE[:-1] + "."
    )


def _without_runlayer_codex_config(content: str) -> str:
    """Strip the Runlayer routing from a Codex TOML config, preserving the rest.

    Dep-free port of ``hook_install.llm_routing._without_runlayer_codex_config``
    (unroute path): removes the top-level ``model_provider = "runlayer"`` assignment
    and the ``[model_providers.runlayer]`` / ``[model_providers.runlayer.*]`` table
    blocks, while preserving unrelated TOML (``approval_policy``, ``[features]``,
    foreign ``[model_providers.*]`` tables, etc.).
    """
    lines = content.splitlines()
    out: list[str] = []
    in_runlayer = False
    before_first_table = True
    for line in lines:
        if _is_toml_table_header(line):
            in_runlayer = _is_runlayer_toml_table(line)
            before_first_table = False
            if not in_runlayer:
                out.append(line)
            continue
        if in_runlayer:
            continue
        model_provider = _toml_assignment(line, "model_provider")
        if not (before_first_table and model_provider == '"runlayer"'):
            out.append(line)
    rendered = "\n".join(out)
    if content.endswith("\n") and rendered:
        rendered += "\n"
    return rendered


def clean_claude_routing(path: Path, *, _anchor: Path | None = None) -> bool:
    """Remove Runlayer LLM routing from a Claude Code JSON config.

    Strips the ``apiKeyHelper`` Runlayer credential helper and the eight routing
    ``env`` keys written by the install-side ``llm_routing._prepare_claude_route``,
    mirroring ``_prepare_claude_unroute`` while preserving foreign helpers and env
    keys. Does not delete the file: ``managed-settings.json`` is shared config.
    """
    path = Path(path)
    snapshot = _read_regular_text(path, anchor=_anchor)
    if snapshot is None:
        return False
    config = _load_jsonc_object(snapshot["text"])
    if config is None:
        return False

    changed = False
    if _is_runlayer_helper(config.get(_CLAUDE_HELPER_KEY)):
        del config[_CLAUDE_HELPER_KEY]
        changed = True
    env = config.get("env")
    if isinstance(env, dict):
        for name in _CLAUDE_ROUTING_ENV_KEYS:
            if name in env:
                del env[name]
                changed = True

    if not changed:
        return False
    rendered = _verified_json_bytes(config)
    if rendered is None:
        return False
    return _atomic_replace(path, rendered, snapshot, anchor=_anchor)


def clean_codex_routing(path: Path, *, _anchor: Path | None = None) -> bool:
    """Remove Runlayer LLM routing from a Codex TOML config.

    Strips the ``model_provider = "runlayer"`` assignment and the
    ``[model_providers.runlayer]`` / ``[model_providers.runlayer.auth]`` table
    blocks, mirroring ``llm_routing._prepare_codex_unroute`` while preserving
    unrelated TOML. Does not delete the file: ``managed_config.toml`` is shared
    config.
    """
    path = Path(path)
    snapshot = _read_regular_text(path, anchor=_anchor)
    if snapshot is None:
        return False
    stripped = _without_runlayer_codex_config(snapshot["text"])
    if stripped == snapshot["text"]:
        return False
    return _atomic_replace(path, stripped.encode("utf-8"), snapshot, anchor=_anchor)


def clean_vscode_settings(path: Path, *, _anchor: Path | None = None) -> bool:
    """Undo only VS Code hook-location values written by Runlayer."""
    path = Path(path)
    snapshot = _read_regular_text(path, anchor=_anchor)
    if snapshot is None:
        return False
    config = _load_jsonc_object(snapshot["text"])
    if config is None:
        return False
    locations = config.get("chat.hookFilesLocations")
    if not isinstance(locations, dict):
        return False

    updated_locations = copy.deepcopy(locations)
    changed = "~/.copilot/hooks" in updated_locations
    updated_locations.pop("~/.copilot/hooks", None)
    for location in (
        ".claude/settings.json",
        ".claude/settings.local.json",
        "~/.claude/settings.json",
    ):
        if updated_locations.get(location) is False:
            updated_locations.pop(location)
            changed = True
    if not changed:
        return False

    updated = copy.deepcopy(config)
    if updated_locations:
        updated["chat.hookFilesLocations"] = updated_locations
    else:
        updated.pop("chat.hookFilesLocations", None)
    rendered = _verified_json_bytes(updated)
    if rendered is None:
        return False
    return _atomic_replace(path, rendered, snapshot, anchor=_anchor)


def _without_line_ending(line: str) -> str:
    return line.rstrip("\r\n")


def _yaml_indent(line: str) -> int | None:
    body = _without_line_ending(line)
    prefix = body[: len(body) - len(body.lstrip(" \t"))]
    if "\t" in prefix:
        return None
    return len(prefix)


def _has_only_spaces_then_optional_comment(value: str) -> bool:
    remainder = value.lstrip(" ")
    return not remainder or remainder.startswith("#")


def _is_yaml_hooks_header(line: str) -> bool:
    prefix = "hooks:"
    return line.startswith(prefix) and _has_only_spaces_then_optional_comment(
        line[len(prefix) :]
    )


def _is_ascii_letter_or_underscore(char: str) -> bool:
    return char == "_" or "A" <= char <= "Z" or "a" <= char <= "z"


def _is_ascii_event_character(char: str) -> bool:
    return _is_ascii_letter_or_underscore(char) or "0" <= char <= "9" or char == "-"


def _yaml_event_indent(line: str) -> int | None:
    indent = len(line) - len(line.lstrip(" "))
    if indent == 0:
        return None
    remainder = line[indent:]
    key, separator, suffix = remainder.partition(":")
    if (
        not separator
        or not key
        or not _is_ascii_letter_or_underscore(key[0])
        or not all(_is_ascii_event_character(char) for char in key[1:])
        or not _has_only_spaces_then_optional_comment(suffix)
    ):
        return None
    return indent


def _yaml_command_suffix(line: str) -> str | None:
    prefix = "command"
    if not line.startswith(prefix):
        return None
    index = len(prefix)
    while index < len(line) and line[index] == " ":
        index += 1
    if index >= len(line) or line[index] != ":":
        return None
    index += 1
    while index < len(line) and line[index] == " ":
        index += 1
    return line[index:]


def _single_quoted_yaml_scalar(value: str) -> str | None:
    output: list[str] = []
    index = 1
    while index < len(value):
        char = value[index]
        if char != "'":
            output.append(char)
            index += 1
            continue
        if index + 1 < len(value) and value[index + 1] == "'":
            output.append("'")
            index += 2
            continue
        remainder = value[index + 1 :]
        if not remainder:
            return "".join(output)
        spaces = len(remainder) - len(remainder.lstrip(" "))
        if spaces > 0 and remainder[spaces:].startswith("#"):
            return "".join(output)
        return None
    return None


def _without_unquoted_inline_comment(value: str) -> str:
    for index, char in enumerate(value):
        if char != "#" or index == 0 or value[index - 1] != " ":
            continue
        comment_start = index
        while comment_start > 0 and value[comment_start - 1] == " ":
            comment_start -= 1
        return value[:comment_start]
    return value


def _yaml_scalar(value: str) -> str | None:
    value = value.strip()
    if not value or value[0] in "|>!&*[{":
        return None
    if value.startswith("'"):
        return _single_quoted_yaml_scalar(value)
    if value.startswith('"'):
        try:
            decoded, end = json.JSONDecoder().raw_decode(value)
        except json.JSONDecodeError:
            return None
        remainder = value[end:].strip()
        if not isinstance(decoded, str) or (
            remainder and not remainder.startswith("#")
        ):
            return None
        return decoded
    value = _without_unquoted_inline_comment(value).rstrip()
    return value or None


def _yaml_item_command(lines: list[str], start: int, end: int) -> str | None:
    candidates: list[str] = []
    for index in range(start, end):
        body = _without_line_ending(lines[index])
        stripped = body.lstrip(" ")
        if index == start:
            if not stripped.startswith("-"):
                return None
            stripped = stripped[1:].lstrip(" ")
        command_suffix = _yaml_command_suffix(stripped)
        if command_suffix is not None:
            scalar = _yaml_scalar(command_suffix)
            if scalar is None:
                return None
            candidates.append(scalar)
    return candidates[0] if len(candidates) == 1 else None


def _parse_yaml_hook_events(
    lines: list[str], section_start: int, section_end: int
) -> list[_YamlEvent] | None:
    substantive = [
        index
        for index in range(section_start + 1, section_end)
        if (body := _without_line_ending(lines[index]).strip())
        and not body.startswith("#")
    ]
    if not substantive:
        return []

    event_indent = _yaml_event_indent(_without_line_ending(lines[substantive[0]]))
    if event_indent is None:
        return None
    event_starts: list[int] = []
    for index in substantive:
        line = lines[index]
        indent = _yaml_indent(line)
        if indent is None or indent < event_indent:
            return None
        body = _without_line_ending(line)
        if indent == event_indent and not body.lstrip(" ").startswith("-"):
            if _yaml_event_indent(body) is None:
                return None
            event_starts.append(index)
    if not event_starts or event_starts[0] != substantive[0]:
        return None

    events: list[_YamlEvent] = []
    for event_index, start in enumerate(event_starts):
        end = (
            event_starts[event_index + 1]
            if event_index + 1 < len(event_starts)
            else section_end
        )
        item_starts: list[int] = []
        sequence_indent: int | None = None
        for index in range(start + 1, end):
            body = _without_line_ending(lines[index])
            stripped = body.strip()
            if not stripped or stripped.startswith("#"):
                continue
            indent = _yaml_indent(lines[index])
            if indent is None:
                return None
            is_item = body.lstrip(" ").startswith(("- ", "-\t")) or body.rstrip() == (
                " " * indent + "-"
            )
            if sequence_indent is None:
                if not is_item or indent < event_indent:
                    return None
                sequence_indent = indent
            if indent == sequence_indent:
                if not is_item:
                    return None
                item_starts.append(index)
            elif indent < sequence_indent:
                return None
        if sequence_indent is None:
            events.append({"start": start, "end": end, "items": []})
            continue
        items: list[_YamlItem] = []
        for item_index, item_start in enumerate(item_starts):
            item_end = (
                item_starts[item_index + 1]
                if item_index + 1 < len(item_starts)
                else end
            )
            command = _yaml_item_command(lines, item_start, item_end)
            items.append(
                {
                    "start": item_start,
                    "end": item_end,
                    "runlayer": (command is not None and is_runlayer_command(command)),
                }
            )
        events.append({"start": start, "end": end, "items": items})
    return events


def clean_hermes_yaml(path: Path, *, _anchor: Path | None = None) -> bool:
    """Conservatively remove Runlayer list items from top-level Hermes hooks."""
    path = Path(path)
    snapshot = _read_regular_text(path, anchor=_anchor)
    if snapshot is None:
        return False
    lines = snapshot["text"].splitlines(keepends=True)
    hook_headers = [
        index
        for index, line in enumerate(lines)
        if _is_yaml_hooks_header(_without_line_ending(line))
    ]
    if len(hook_headers) != 1:
        return False
    section_start = hook_headers[0]
    section_end = len(lines)
    for index in range(section_start + 1, len(lines)):
        body = _without_line_ending(lines[index])
        if not body.strip() or body.lstrip().startswith("#"):
            continue
        indent = _yaml_indent(lines[index])
        if indent is None:
            return False
        if indent == 0:
            section_end = index
            break

    events = _parse_yaml_hook_events(lines, section_start, section_end)
    if events is None:
        return False
    if not any(item["runlayer"] for event in events for item in event["items"]):
        return False

    removed: set[int] = set()
    kept_events = 0
    for event in events:
        removed_items = [item for item in event["items"] if item["runlayer"]]
        if not removed_items:
            kept_events += 1
            continue
        kept_items = [item for item in event["items"] if not item["runlayer"]]
        if kept_items:
            kept_events += 1
            for item in removed_items:
                removed.update(range(item["start"], item["end"]))
        else:
            removed.update(range(event["start"], event["end"]))

    if kept_events == 0:
        removed.update(range(section_start, section_end))
    rendered = "".join(
        line for index, line in enumerate(lines) if index not in removed
    ).encode("utf-8")
    return _atomic_replace(path, rendered, snapshot, anchor=_anchor)


def strip_managed_ignore_block(path: Path, *, _anchor: Path | None = None) -> bool:
    """Remove exactly one complete Runlayer-managed ignore block."""
    path = Path(path)
    snapshot = _read_regular_text(path, anchor=_anchor)
    if snapshot is None:
        return False
    lines = snapshot["text"].splitlines(keepends=True)
    starts = [
        index
        for index, line in enumerate(lines)
        if _without_line_ending(line) == _MANAGED_IGNORE_START
    ]
    ends = [
        index
        for index, line in enumerate(lines)
        if _without_line_ending(line) == _MANAGED_IGNORE_END
    ]
    if len(starts) != 1 or len(ends) != 1 or starts[0] >= ends[0]:
        return False

    before = "".join(lines[: starts[0]]).rstrip("\r\n")
    after = "".join(lines[ends[0] + 1 :]).lstrip("\r\n")
    newline = "\r\n" if "\r\n" in snapshot["text"] else "\n"
    if before and after:
        rendered_text = before + newline * 2 + after
    else:
        rendered_text = before or after
    if rendered_text and snapshot["text"].endswith(("\n", "\r")):
        rendered_text = rendered_text.rstrip("\r\n") + newline
    if not rendered_text:
        return _unlink_snapshot(path, snapshot, anchor=_anchor)
    return _atomic_replace(
        path,
        rendered_text.encode("utf-8"),
        snapshot,
        anchor=_anchor,
    )


def _cline_script_is_owned(text: str) -> bool:
    if _CLINE_MARKER in text:
        return True
    found_runlayer = False
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith(("#!", "#")):
            continue
        if (
            line.startswith(("export HOOK_EVENT_NAME=", "export RUNLAYER_HOOK_CLIENT="))
            or line.startswith(("$env:HOOK_EVENT_NAME", "$env:RUNLAYER_HOOK_CLIENT"))
            or line in {"set -e", "set -eu", "set -euo pipefail"}
        ):
            continue
        if is_runlayer_command(line):
            found_runlayer = True
            continue
        return False
    return found_runlayer


def clean_cline_scripts(hooks_dir: Path, *, _anchor: Path | None = None) -> int:
    """Delete only clearly Runlayer-owned scripts from a Cline hooks directory."""
    hooks_dir = Path(hooks_dir)
    if _anchor is None:
        if not _path_is_safe(hooks_dir, None):
            return 0
        try:
            entries = tuple(
                entry.name
                for entry in os.scandir(hooks_dir)
                if entry.is_file(follow_symlinks=False)
            )
        except OSError:
            return 0
    else:
        scan_handle = _open_anchored_parent(hooks_dir / ".scan", _anchor)
        if scan_handle is None:
            return 0
        try:
            entries = tuple(
                entry.name
                for entry in os.scandir(scan_handle["parent_fd"])
                if entry.is_file(follow_symlinks=False)
            )
        except OSError:
            return 0
        finally:
            _close_descriptors(scan_handle["fds"])
    removed = 0
    for entry_name in entries:
        path = hooks_dir / entry_name
        snapshot = _read_regular_text(path, anchor=_anchor)
        if snapshot is None or not _cline_script_is_owned(snapshot["text"]):
            continue
        if _unlink_snapshot(path, snapshot, anchor=_anchor):
            removed += 1
    return removed


def _is_runlayer_update_url(
    value: object,
    *,
    managed_host: str | None = None,
) -> bool:
    if not isinstance(value, str):
        return False
    try:
        parsed = urlparse(value)
        host = parsed.hostname or ""
    except ValueError:
        return False
    is_runlayer_host = (
        host == "runlayer.com"
        or host.endswith(".runlayer.com")
        or host.endswith(".runlayer.example")
    )
    try:
        configured_host = (
            urlparse(managed_host).hostname if isinstance(managed_host, str) else None
        )
    except ValueError:
        configured_host = None
    path = parsed.path.rstrip("/")
    tenant_manifest = path.removeprefix(_CHROME_TENANT_MANIFEST_PREFIX)
    tenant_token, separator, manifest_name = tenant_manifest.partition("/")
    is_tenant_manifest = (
        path.startswith(_CHROME_TENANT_MANIFEST_PREFIX)
        and bool(tenant_token)
        and separator == "/"
        and manifest_name == "update.xml"
    )
    is_runlayer_extension_manifest = path == "/extension/update_manifest.xml" or (
        is_tenant_manifest
    )
    is_legacy_aiwatch_manifest = "aiwatch" in path
    return parsed.scheme == "https" and (
        (
            is_runlayer_host
            and (is_runlayer_extension_manifest or is_legacy_aiwatch_manifest)
        )
        or (host == configured_host and is_runlayer_extension_manifest)
    )


def _is_chrome_extension_id(value: str) -> bool:
    return len(value) == 32 and all("a" <= char <= "p" for char in value)


def _without_runlayer_firefox_policy(
    current: dict[str, Any],
) -> dict[str, Any]:
    result = copy.deepcopy(current)

    extension_settings = result.get("ExtensionSettings")
    if isinstance(extension_settings, dict):
        extension_settings.pop(_RUNLAYER_FIREFOX_EXTENSION_ID, None)
        if not extension_settings:
            result.pop("ExtensionSettings", None)

    third_party = result.get("3rdparty")
    if isinstance(third_party, dict):
        extensions = third_party.get("Extensions")
        if isinstance(extensions, dict):
            extensions.pop(_RUNLAYER_FIREFOX_EXTENSION_ID, None)
            if not extensions:
                third_party.pop("Extensions", None)
        if not third_party:
            result.pop("3rdparty", None)

    return result


def clean_firefox_policy(
    path: Path,
    *,
    _anchor: Path | None = None,
) -> bool:
    """Remove only Runlayer-owned Firefox extension policy."""
    path = Path(path)
    snapshot = _read_regular_bytes(path, anchor=_anchor)
    if snapshot is None:
        return False
    current = _load_plist_dict(snapshot)
    if current is None:
        return False

    updated = _without_runlayer_firefox_policy(current)
    if updated == current:
        return False
    if len(updated) == 1 and updated.get("EnterprisePoliciesEnabled") is True:
        updated.pop("EnterprisePoliciesEnabled")
    if not updated:
        return _unlink_snapshot(path, snapshot, anchor=_anchor)

    rendered = _verified_plist_bytes(updated)
    if rendered is None:
        return False
    return _atomic_replace(path, rendered, snapshot, anchor=_anchor)


def _chrome_force_install_entry_parts(
    entry: object,
) -> tuple[str, str] | None:
    if not isinstance(entry, str):
        return None
    extension_id, separator, update_url = entry.partition(";")
    if not separator or not _is_chrome_extension_id(extension_id):
        return None
    return extension_id, update_url


def clean_chrome_force_install_policy(
    path: Path,
    *,
    _anchor: Path | None = None,
    managed_host: str | None = None,
) -> set[str]:
    """Remove Runlayer entries from Chrome's shared force-install policy."""
    path = Path(path)
    snapshot = _read_regular_bytes(path, anchor=_anchor)
    if snapshot is None:
        return set()
    current = _load_plist_dict(snapshot)
    if current is None:
        return set()
    force_list = current.get("ExtensionInstallForcelist")
    if not isinstance(force_list, list):
        return set()

    removed_ids: set[str] = set()
    kept_entries: list[Any] = []
    for entry in force_list:
        parts = _chrome_force_install_entry_parts(entry)
        if parts is not None and (
            parts[0] == _RUNLAYER_CHROME_EXTENSION_ID
            or _is_runlayer_update_url(parts[1], managed_host=managed_host)
        ):
            removed_ids.add(parts[0])
        else:
            kept_entries.append(copy.deepcopy(entry))
    if not removed_ids:
        return set()

    updated = copy.deepcopy(current)
    if kept_entries:
        updated["ExtensionInstallForcelist"] = kept_entries
    else:
        updated.pop("ExtensionInstallForcelist", None)
    if not updated:
        changed = _unlink_snapshot(path, snapshot, anchor=_anchor)
    else:
        rendered = _verified_plist_bytes(updated)
        changed = rendered is not None and _atomic_replace(
            path,
            rendered,
            snapshot,
            anchor=_anchor,
        )
    return removed_ids if changed else set()


def _unlink_regular(path: Path, *, anchor: Path | None = None) -> bool:
    if anchor is None:
        if not _path_is_safe(path, None):
            return False
        try:
            path_stat = path.lstat()
        except OSError:
            return False
        if not stat.S_ISREG(path_stat.st_mode):
            return False
        try:
            path.unlink()
        except OSError:
            return False
        return True

    parent_handle = _open_anchored_parent(path, anchor)
    if parent_handle is None:
        return False
    try:
        path_stat = os.stat(
            parent_handle["name"],
            dir_fd=parent_handle["parent_fd"],
            follow_symlinks=False,
        )
        if not stat.S_ISREG(path_stat.st_mode):
            return False
        os.unlink(
            parent_handle["name"],
            dir_fd=parent_handle["parent_fd"],
        )
    except OSError:
        return False
    finally:
        _close_descriptors(parent_handle["fds"])
    return True


def _unlink_owned_leaf(path: Path, *, anchor: Path | None = None) -> bool:
    if anchor is None:
        if not _path_is_safe(path, None):
            return False
        try:
            path_stat = path.lstat()
        except OSError:
            return False
        if stat.S_ISDIR(path_stat.st_mode) or stat.S_ISLNK(path_stat.st_mode):
            return False
        try:
            path.unlink()
        except OSError:
            return False
        return True

    parent_handle = _open_anchored_parent(path, anchor)
    if parent_handle is None:
        return False
    try:
        path_stat = os.stat(
            parent_handle["name"],
            dir_fd=parent_handle["parent_fd"],
            follow_symlinks=False,
        )
        if stat.S_ISDIR(path_stat.st_mode) or stat.S_ISLNK(path_stat.st_mode):
            return False
        os.unlink(
            parent_handle["name"],
            dir_fd=parent_handle["parent_fd"],
        )
    except OSError:
        return False
    finally:
        _close_descriptors(parent_handle["fds"])
    return True


def clean_browser_owned_artifacts(
    managed_preferences_dir: Path,
    external_extensions_dir: Path,
    *,
    extension_ids: set[str] | None = None,
    managed_host: str | None = None,
) -> int:
    """Delete owned Chrome external metadata and matching extension policies."""
    managed_preferences_dir = Path(managed_preferences_dir)
    external_extensions_dir = Path(external_extensions_dir)
    owned_extension_ids = {_RUNLAYER_CHROME_EXTENSION_ID}
    if extension_ids is not None:
        owned_extension_ids.update(
            extension_id
            for extension_id in extension_ids
            if isinstance(extension_id, str) and _is_chrome_extension_id(extension_id)
        )
    managed_dir_safe = _path_is_safe(managed_preferences_dir, None)
    external_dir_safe = _path_is_safe(external_extensions_dir, None)

    if external_dir_safe:
        try:
            entries = tuple(os.scandir(external_extensions_dir))
        except OSError:
            entries = ()
        for entry in entries:
            path = Path(entry.path)
            if not entry.name.endswith(".json") or not _is_chrome_extension_id(
                path.stem
            ):
                continue
            try:
                if not entry.is_file(follow_symlinks=False):
                    continue
            except OSError:
                continue
            snapshot = _read_regular_text(path)
            if snapshot is None:
                continue
            try:
                config = json.loads(snapshot["text"])
            except json.JSONDecodeError:
                continue
            update_url = (
                config.get("external_update_url") if isinstance(config, dict) else None
            )
            if _is_runlayer_update_url(update_url, managed_host=managed_host):
                owned_extension_ids.add(path.stem)

    removed = 0
    for extension_id in owned_extension_ids:
        external = external_extensions_dir / f"{extension_id}.json"
        policy = (
            managed_preferences_dir
            / f"com.google.Chrome.extensions.{extension_id}.plist"
        )
        if external_dir_safe and _unlink_regular(external):
            removed += 1
        if managed_dir_safe and _unlink_regular(policy):
            removed += 1
    return removed


def _remove_tree_at(parent_fd: int, name: str) -> bool:
    try:
        directory_fd = os.open(name, _DIRECTORY_OPEN_FLAGS, dir_fd=parent_fd)
    except OSError:
        return False
    try:
        opened = os.fstat(directory_fd)
        entries = tuple(os.scandir(directory_fd))
        for entry in entries:
            try:
                entry_stat = entry.stat(follow_symlinks=False)
                if stat.S_ISDIR(entry_stat.st_mode):
                    if not _remove_tree_at(directory_fd, entry.name):
                        return False
                else:
                    os.unlink(entry.name, dir_fd=directory_fd)
            except OSError:
                return False
        current = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
        if (
            not stat.S_ISDIR(current.st_mode)
            or current.st_dev != opened.st_dev
            or current.st_ino != opened.st_ino
        ):
            return False
    except OSError:
        return False
    finally:
        os.close(directory_fd)
    try:
        os.rmdir(name, dir_fd=parent_fd)
    except OSError:
        return False
    return True


def _remove_owned_tree(path: Path, *, anchor: Path | None = None) -> bool:
    if anchor is None:
        if not _path_is_safe(path, None):
            return False
        try:
            path_stat = path.lstat()
        except OSError:
            return False
        if not stat.S_ISDIR(path_stat.st_mode):
            return False
        try:
            shutil.rmtree(path)
        except OSError:
            return False
        return True

    parent_handle = _open_anchored_parent(path, anchor)
    if parent_handle is None:
        return False
    try:
        return _remove_tree_at(
            parent_handle["parent_fd"],
            parent_handle["name"],
        )
    finally:
        _close_descriptors(parent_handle["fds"])


def _clean_call(function: Callable[..., Any], *args: Any, **kwargs: Any) -> int:
    try:
        result = function(*args, **kwargs)
    except BaseException:
        return 0
    if isinstance(result, bool):
        return int(result)
    return result if isinstance(result, int) and result > 0 else 0


_USER_JSON_HOOK_PATHS: tuple[tuple[str, bool], ...] = (
    (".cursor/hooks.json", True),
    (".copilot/hooks/runlayer.json", True),
    (".claude/settings.json", False),
    (".codex/hooks.json", True),
    (".copilot/settings.json", True),
    (".codeium/windsurf/hooks.json", True),
    (".qwen/settings.json", False),
    (".gemini/settings.json", True),
    (".grok/hooks/runlayer.json", True),
    (".config/devin/config.json", False),
)
_LEGACY_SCRIPT_PATHS = (
    ".cursor/hooks/runlayer-hook.sh",
    ".cursor/hooks/runlayer-cursor-hook.sh",
    ".claude/hooks/runlayer-hook.sh",
    ".claude/hooks/runlayer-claude-hook.sh",
    ".codex/hooks/runlayer-hook.sh",
    ".hermes/agent-hooks/runlayer-hook.sh",
    ".copilot/hooks/runlayer-hook.sh",
    ".copilot/hooks/hooks/runlayer-hook.sh",
    ".codeium/windsurf/hooks/runlayer-hook.sh",
    ".gemini/hooks/runlayer-hook.sh",
    ".runlayer/hooks/runlayer-hook.sh",
)
_LEGACY_CONFIG_PATHS = (
    ".cursor/hooks/runlayer-config.json",
    ".claude/hooks/runlayer-config.json",
    ".codex/hooks/runlayer-config.json",
    ".hermes/agent-hooks/runlayer-config.json",
    ".copilot/hooks/runlayer-config.json",
    ".copilot/hooks/hooks/runlayer-config.json",
    ".codeium/windsurf/hooks/runlayer-config.json",
    ".gemini/hooks/runlayer-config.json",
    ".runlayer/hooks/runlayer-config.json",
)


def _resolve_managed_grok_home(home: Path, configured: str) -> Path | None:
    if not configured.strip():
        return None
    if configured == "~":
        candidate = home
    elif configured.startswith(("~/", "~\\")):
        candidate = home / configured[2:]
    elif configured.startswith("~"):
        return None
    else:
        configured_path = Path(configured)
        candidate = (
            configured_path if configured_path.is_absolute() else home / configured_path
        )

    normalized_home = Path(os.path.normpath(home))
    normalized_candidate = Path(os.path.normpath(candidate))
    try:
        normalized_candidate.relative_to(normalized_home)
    except ValueError:
        return None
    return normalized_candidate


def _read_managed_cleanup_config(
    paths: tuple[Path, ...] = _MACOS_MANAGED_CONFIG_PATHS,
) -> _ManagedCleanupConfig:
    result = _ManagedCleanupConfig(grok_home=None, host=None)
    for path in paths:
        snapshot = _read_regular_bytes(Path(path))
        if snapshot is None:
            continue
        config = _load_plist_dict(snapshot)
        if config is None:
            continue
        grok_home = config.get(_GROK_HOME_KEY)
        if (
            result["grok_home"] is None
            and isinstance(grok_home, str)
            and grok_home.strip()
        ):
            result["grok_home"] = grok_home
        host = config.get(_HOST_KEY)
        if result["host"] is None and isinstance(host, str) and host.strip():
            result["host"] = host
    return result


def clean_user_home(home: Path, *, grok_home: str | None = None) -> int:
    """Best-effort cleanup of all thirteen supported clients in one user home."""
    home = Path(home)
    if not _path_is_safe(home, None):
        return 0
    changed = 0

    for relative, delete_when_empty in _USER_JSON_HOOK_PATHS:
        changed += _clean_call(
            clean_json_hooks,
            home / relative,
            delete_when_empty=delete_when_empty,
            _anchor=home,
        )
    if grok_home is not None:
        managed_grok_home = _resolve_managed_grok_home(home, grok_home)
        if managed_grok_home is not None and managed_grok_home != home / ".grok":
            changed += _clean_call(
                clean_json_hooks,
                managed_grok_home / "hooks" / "runlayer.json",
                delete_when_empty=True,
                _anchor=home,
            )
    changed += _clean_call(
        clean_vscode_settings,
        home / "Library" / "Application Support" / "Code" / "User" / "settings.json",
        _anchor=home,
    )
    changed += _clean_call(
        clean_hermes_yaml,
        home / ".hermes" / "config.yaml",
        _anchor=home,
    )
    changed += _clean_call(
        strip_managed_ignore_block, home / ".cursorignore", _anchor=home
    )
    changed += _clean_call(
        strip_managed_ignore_block, home / ".claudeignore", _anchor=home
    )
    changed += _clean_call(clean_cline_scripts, home / ".cline" / "hooks", _anchor=home)
    changed += _clean_call(
        _remove_owned_tree,
        home / ".agents" / "plugins" / "runlayer-hooks",
        anchor=home,
    )

    for relative in _LEGACY_SCRIPT_PATHS:
        changed += int(_unlink_regular(home / relative, anchor=home))
    for relative in _LEGACY_CONFIG_PATHS:
        changed += int(_unlink_regular(home / relative, anchor=home))

    # Delete the per-user LLM routing credential written by MDM-scope route
    # (mirrors ``llm_routing._delete_credential``). ``_unlink_owned_leaf`` refuses
    # symlinks and directories so a planted link can't redirect the unlink.
    changed += int(
        _unlink_owned_leaf(home / _LLM_ROUTING_CREDENTIAL_RELATIVE_PATH, anchor=home)
    )

    for relative in (
        "Library/Application Support/Runlayer/aiwatch.sock",
        "Library/Application Support/Runlayer/aiwatch.sock.lock",
    ):
        changed += int(_unlink_owned_leaf(home / relative, anchor=home))
    changed += int(
        _unlink_regular(
            home / "Library/Preferences/com.runlayer.aiwatch.plist",
            anchor=home,
        )
    )
    return changed


def _run(
    command: tuple[str, ...], *, timeout: float = _SUBPROCESS_TIMEOUT_SECONDS
) -> bool:
    try:
        result = subprocess.run(
            command,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.SubprocessError):
        return False
    return result.returncode == 0


def _run_capture(
    command: tuple[str, ...], *, timeout: float = _SUBPROCESS_TIMEOUT_SECONDS
) -> str:
    try:
        result = subprocess.run(
            command,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
            timeout=timeout,
            text=True,
        )
    except (OSError, subprocess.SubprocessError):
        return ""
    return result.stdout if result.returncode == 0 else ""


def _parse_uid(value: str, *, minimum: int = 1) -> int | None:
    try:
        uid = int(value.strip())
    except ValueError:
        return None
    return uid if uid >= minimum else None


def _discover_local_homes_and_uids() -> _LocalUsers:
    homes: dict[str, Path] = {str(_ROOT_HOME): _ROOT_HOME}
    uids: set[int] = set()

    try:
        entries = tuple(os.scandir(_USERS_ROOT))
    except OSError:
        entries = ()
    for entry in entries:
        if entry.name == "Shared":
            continue
        home = Path(os.fsdecode(entry.path))
        homes.setdefault(str(home), home)

    console_uid = _parse_uid(
        _run_capture(("/usr/bin/stat", "-f", "%u", "/dev/console"))
    )
    if console_uid is not None:
        uids.add(console_uid)

    active_users = {
        line.split()[0]
        for line in _run_capture(("/usr/bin/who",)).splitlines()
        if line.split()
    }
    for username in active_users:
        uid = _parse_uid(_run_capture(("/usr/bin/id", "-u", username)))
        if uid is not None:
            uids.add(uid)

    local_users = _run_capture(("/usr/bin/dscl", ".", "-list", "/Users", "UniqueID"))
    for line in local_users.splitlines():
        fields = line.rsplit(None, 1)
        if len(fields) != 2:
            continue
        uid = _parse_uid(fields[1], minimum=500)
        if uid is not None:
            uids.add(uid)
    return {
        "homes": sorted(homes.values(), key=lambda path: path.as_posix()),
        "uids": uids,
    }


def _home_child_timeout_exit(_signum: int, _frame: object) -> None:
    os._exit(1)


def _clean_home_in_child(home: Path, grok_home: str | None = None) -> bool:
    fork = getattr(os, "fork", None)
    if fork is None:
        clean_user_home(home, grok_home=grok_home)
        return True
    try:
        child = fork()
    except OSError:
        return False
    if child == 0:
        exit_code = 0
        try:
            if hasattr(signal, "SIGALRM"):
                signal.signal(signal.SIGALRM, _home_child_timeout_exit)
                signal.alarm(max(1, int(_HOME_CHILD_TIMEOUT_SECONDS)))
            clean_user_home(home, grok_home=grok_home)
        except BaseException:
            exit_code = 1
        finally:
            os._exit(exit_code)

    deadline = time.monotonic() + _HOME_CHILD_TIMEOUT_SECONDS
    while time.monotonic() < deadline:
        try:
            waited, status = os.waitpid(child, os.WNOHANG)
        except (ChildProcessError, OSError):
            return False
        if waited == child:
            return os.WIFEXITED(status) and os.WEXITSTATUS(status) == 0
        time.sleep(0.05)
    try:
        os.kill(child, signal.SIGKILL)
    except OSError:
        pass
    try:
        os.waitpid(child, os.WNOHANG)
    except (ChildProcessError, OSError):
        pass
    return False


def _bootout_jobs(uids: set[int]) -> None:
    for uid in sorted(uids):
        for label in _AGENT_LABELS:
            _run(("/bin/launchctl", "bootout", f"gui/{uid}/{label}"))
    for label in _DAEMON_LABELS:
        _run(("/bin/launchctl", "bootout", f"system/{label}"))


def _kill_daemon_processes() -> None:
    pattern = (
        r"^(/usr/local/bin/aiwatch|"
        r"/usr/local/lib/runlayer/aiwatch/aiwatch) daemon( |$)"
    )
    _run(("/usr/bin/pkill", "-TERM", "-f", pattern))
    time.sleep(0.1)
    _run(("/usr/bin/pkill", "-KILL", "-f", pattern))


def _remove_package_path(path: Path) -> _RemovalResult:
    try:
        path_stat = path.lstat()
    except FileNotFoundError:
        return {"ok": True, "changed": False}
    except OSError:
        return {"ok": False, "changed": False}
    try:
        if stat.S_ISDIR(path_stat.st_mode) and not stat.S_ISLNK(path_stat.st_mode):
            shutil.rmtree(path)
        else:
            path.unlink()
    except FileNotFoundError:
        return {"ok": True, "changed": False}
    except OSError:
        return {"ok": False, "changed": False}
    return {"ok": True, "changed": True}


def _remove_package_artifacts() -> _PreferenceCleanupResult:
    ok = True
    preferences_changed = False
    for path in _PACKAGE_PATHS:
        removal = _remove_package_path(path)
        ok = removal["ok"] and ok
        try:
            under_preferences = bool(path.relative_to(_SYSTEM_PREFERENCES_DIR).parts)
        except ValueError:
            under_preferences = False
        preferences_changed = preferences_changed or (
            under_preferences and removal["changed"]
        )
    return {"ok": ok, "preferences_changed": preferences_changed}


def _map_system_path(path: Path, system_root: Path) -> Path | None:
    path = Path(path)
    system_root = Path(system_root)
    if (
        not path.is_absolute()
        or not system_root.is_absolute()
        or ".." in path.parts
        or ".." in system_root.parts
    ):
        return None
    relative = Path(*path.parts[1:])
    if not relative.parts:
        return None
    mapped = system_root / relative
    try:
        mapped_relative = mapped.relative_to(system_root)
    except ValueError:
        return None
    if not mapped_relative.parts or ".." in mapped_relative.parts:
        return None
    return mapped


_ENTERPRISE_ROUTING_PATHS: tuple[tuple[Path, Callable[..., bool]], ...] = (
    (
        Path("/Library/Application Support/ClaudeCode/managed-settings.json"),
        clean_claude_routing,
    ),
    (Path("/private/etc/codex/managed_config.toml"), clean_codex_routing),
)


def _clean_enterprise_hooks(system_root: Path = Path("/")) -> None:
    system_root = Path(system_root)
    for configured_path, delete_when_empty in _ENTERPRISE_JSON_HOOK_PATHS:
        path = _map_system_path(configured_path, system_root)
        if path is None:
            continue
        _clean_call(
            clean_json_hooks,
            path,
            delete_when_empty=delete_when_empty,
            _anchor=system_root,
        )
    for configured_path, cleaner in _ENTERPRISE_ROUTING_PATHS:
        path = _map_system_path(configured_path, system_root)
        if path is None:
            continue
        _clean_call(cleaner, path, _anchor=system_root)
    for configured_root, old_name in _ENTERPRISE_LEGACY_ROOTS:
        root = _map_system_path(configured_root, system_root)
        if root is None:
            continue
        legacy_paths = [
            Path("hooks") / "runlayer-hook.sh",
            Path("hooks") / "runlayer-config.json",
        ]
        if old_name is not None:
            legacy_paths.append(Path("hooks") / old_name)
        for relative in legacy_paths:
            _clean_call(
                _unlink_regular,
                root / relative,
                anchor=system_root,
            )


def _clean_browser_policies(
    system_root: Path = Path("/"),
    *,
    managed_host: str | None = None,
) -> _PreferenceCleanupResult:
    system_root = Path(system_root)
    result = _PreferenceCleanupResult(ok=True, preferences_changed=False)
    for configured_path in _FIREFOX_POLICY_PATHS:
        path = _map_system_path(configured_path, system_root)
        if path is not None:
            changed = bool(_clean_call(clean_firefox_policy, path, _anchor=system_root))
            if configured_path == _FIREFOX_CANONICAL_POLICY_PATH:
                # Only this plist needs cfprefsd eviction; Managed Preferences does not.
                result["preferences_changed"] = changed

    chrome_path = _map_system_path(
        _CHROME_FORCE_INSTALL_POLICY_PATH,
        system_root,
    )
    if chrome_path is None:
        return result
    try:
        extension_ids = clean_chrome_force_install_policy(
            chrome_path,
            _anchor=system_root,
            managed_host=managed_host,
        )
    except BaseException:
        extension_ids = set()
    if not extension_ids:
        return result

    managed_preferences_dir = _map_system_path(
        _CHROME_MANAGED_PREFERENCES_DIR,
        system_root,
    )
    external_extensions_dir = _map_system_path(
        _CHROME_EXTERNAL_EXTENSIONS_DIR,
        system_root,
    )
    if managed_preferences_dir is not None and external_extensions_dir is not None:
        _clean_call(
            clean_browser_owned_artifacts,
            managed_preferences_dir,
            external_extensions_dir,
            extension_ids=extension_ids,
            managed_host=managed_host,
        )
    return result


def _watchdog_exit_success(_signum: int, _frame: object) -> None:
    os._exit(0)


def main() -> int:
    """Run the complete macOS package teardown; always report success."""
    old_handler: Any = None
    watchdog_installed = False
    try:
        if hasattr(signal, "SIGALRM"):
            old_handler = signal.signal(signal.SIGALRM, _watchdog_exit_success)
            signal.alarm(_GLOBAL_WATCHDOG_SECONDS)
            watchdog_installed = True
    except (OSError, ValueError):
        pass

    try:
        homes: list[Path] = []
        uids: set[int] = set()
        local_users = _attempt_phase(
            "user discovery",
            _discover_local_homes_and_uids,
        )
        if isinstance(local_users, dict):
            homes = local_users["homes"]
            uids = local_users["uids"]
        _attempt_phase("launchd jobs", lambda: _bootout_jobs(uids))
        _attempt_phase("daemon processes", _kill_daemon_processes)
        managed_config = _attempt_phase(
            "managed config",
            _read_managed_cleanup_config,
        )
        managed_grok_home: str | None = None
        managed_host: str | None = None
        if isinstance(managed_config, dict):
            grok_home = managed_config.get("grok_home")
            host = managed_config.get("host")
            managed_grok_home = grok_home if isinstance(grok_home, str) else None
            managed_host = host if isinstance(host, str) else None
        package_cleanup = _attempt_phase(
            "package artifacts",
            _remove_package_artifacts,
        )
        package_preferences_changed = (
            isinstance(package_cleanup, dict)
            and package_cleanup.get("preferences_changed") is True
        )
        _attempt_phase(
            "TCC reset",
            lambda: _run(("/usr/bin/tccutil", "reset", "All", "com.runlayer.aiwatch")),
        )
        for receipt_id in _RECEIPT_IDS:
            _attempt_phase(
                f"receipt {receipt_id}",
                lambda receipt_id=receipt_id: _run(
                    ("/usr/sbin/pkgutil", "--forget", receipt_id)
                ),
            )
        _attempt_phase("enterprise hooks", _clean_enterprise_hooks)
        # Keep the canonical/external sweep independent: corrupt shared policy
        # must not block deleting wholly Runlayer-owned artifacts. The policy
        # phase repeats it only for additional ids recovered from the forcelist.
        _attempt_phase(
            "browser artifacts",
            lambda: clean_browser_owned_artifacts(
                _CHROME_MANAGED_PREFERENCES_DIR,
                _CHROME_EXTERNAL_EXTENSIONS_DIR,
                managed_host=managed_host,
            ),
        )
        browser_policy_cleanup = _attempt_phase(
            "browser policy",
            lambda: _clean_browser_policies(managed_host=managed_host),
        )
        firefox_preferences_changed = (
            isinstance(browser_policy_cleanup, dict)
            and browser_policy_cleanup.get("preferences_changed") is True
        )
        if package_preferences_changed or firefox_preferences_changed:
            # Direct preference plist edits need cfprefsd restarted to evict caches.
            _attempt_phase(
                "preference cache",
                lambda: _run(("/usr/bin/killall", "cfprefsd")),
            )
        for home in homes:
            _attempt_phase(
                f"user home {home}",
                lambda home=home: _clean_home_in_child(home, managed_grok_home),
            )
    except BaseException:
        try:
            _log_phase("uninstall", False)
        except BaseException:
            pass
    finally:
        if watchdog_installed:
            try:
                signal.alarm(0)
                signal.signal(signal.SIGALRM, old_handler)
            except (OSError, ValueError):
                pass
    return 0


__all__ = [
    "clean_browser_owned_artifacts",
    "clean_chrome_force_install_policy",
    "clean_claude_routing",
    "clean_cline_scripts",
    "clean_codex_routing",
    "clean_firefox_policy",
    "clean_hermes_yaml",
    "clean_json_hooks",
    "clean_user_home",
    "clean_vscode_settings",
    "is_runlayer_command",
    "main",
    "strip_managed_ignore_block",
    "without_runlayer_hooks",
]


if __name__ == "__main__":
    raise SystemExit(main())
