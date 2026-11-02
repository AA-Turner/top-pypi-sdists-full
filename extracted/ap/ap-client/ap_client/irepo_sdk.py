"""InstanceRepo SDK 上下文构建与错误翻译(实现设计 §2 / §5.1 / §8.1)。

数据面命令(``ap instance push/pull``、``ap fs *``、
``ap dataset version create``)通过本模块拿到一个配好 AP 连接与认证的
``instance_repo.Repo``,并把 SDK 异常翻译成 AP CLI 统一的
``error:`` / ``hint:`` 两行文案 + 退出码。

对外只有三样东西:

* :class:`SdkMissing` —— 未安装 ``ap-client[dataset]`` extra;
* :func:`load_repo` —— 按 AP ``Config`` 构造 ``Repo``;
* :func:`sdk_error_exit` —— SDK 异常 → 可执行建议 + ``typer.Exit``。

控制面元数据命令(version create 除外),
以及 ``ap instance list/get`` **不得** import 本模块之外的 SDK 符号,也不应触发
``load_repo``:没装 extra 的用户必须仍能使用它们。

两个 SDK 版本的构造签名不同(设计 §8.1):

* ``release/v1.0.0``(1.0.0,目标版本)支持
  ``Repo(token=, api_base=, cluster=, storage_env=, api_env=)``;
* 已发布的 0.8.1 只有 ``Repo(profile, token=, api_env=, storage_env=)``,
  ``api_base`` 只能通过 ``INSTANCEREPO_API_BASE`` 环境变量提供,且完全没有
  cluster 概念。

因此 :func:`load_repo` 用 ``inspect.signature`` 做一次能力探测:签名支持的参数
显式传入,不支持的回退为进程内环境变量注入(不覆盖用户已设的值)。
"""

from __future__ import annotations

import hashlib
import inspect
import json
import math
import os
import platform
import re
import stat
import subprocess
import tempfile
import threading
import time
import weakref
from contextlib import contextmanager
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Iterator, NoReturn
from urllib.parse import urlsplit

import typer

from .config import _parse_bool, get_config

if TYPE_CHECKING:  # pragma: no cover - 仅供类型检查,运行时不 import SDK
    from instance_repo import Repo

__all__ = [
    "SdkMissing",
    "is_already_satisfied",
    "load_repo",
    "sdk_error_exit",
    "update_version_detail",
]

#: 数据集元数据的环境枚举(服务端 ``dataset environment``)。
#: ``auto`` 是 CLI 层取值:跟随集群绑定(读省略下发,写继承集群桶),不会下发给服务端。
DATASET_ENVIRONMENTS = ("online", "pre", "auto")

#: 缺 extra 时的安装提示(沿用 irepo_commands.py 的 ``_INSTALL_HINT`` 文案范式)。
_INSTALL_HINT = (
    "This command requires Dataset authoring support, which is not installed in "
    "this environment.\n"
    "Install it with: pip install 'ap-client[dataset]'"
)

# storage_env 解析顺序:显式参数 > 规范环境变量(1.0.0) > 旧别名(0.8.x)。
# **没有默认值**——猜一个 storage_env 会把数据写到错误的存储环境。
_STORAGE_ENV_VARS = ("INSTANCE_REPO_STORAGE_ENV", "IR_STORAGE_ENV")

# 旧 SDK 回退时注入的环境变量名(0.8.x 的契约)。
_LEGACY_API_BASE_VAR = "INSTANCEREPO_API_BASE"
_LEGACY_TOKEN_VAR = "INSTANCEREPO_TOKEN"
_LEGACY_STORAGE_ENV_VAR = "IR_STORAGE_ENV"


class SdkMissing(Exception):
    """``instance_repo`` 未安装。``str(exc)`` 就是给用户看的安装提示。

    数据面命令应捕获它,把消息打到 stderr 并以退出码 2 结束(缺依赖属于使用
    错误,不是业务失败)。
    """

    def __init__(self, message: str = _INSTALL_HINT) -> None:
        super().__init__(message)


_OSS_PROBE_CACHE_VERSION = 1
_OSS_PROBE_CACHE_TTL = 300.0
_OSS_PROBE_CACHE_MAX_BYTES = 64 * 1024
_OSS_PROBE_CACHE_MAX_ENTRIES = 128
_NETWORK_FINGERPRINT_UNSET = object()
_NETWORK_FINGERPRINT_TTL = 1.0
_now = time.time
_monotonic = time.monotonic


def _oss_probe_cache_path() -> Path:
    return Path.home() / ".ap" / ".cache" / "oss-probe.json"


def _run_network_command(command: tuple[str, ...]) -> bytes | None:
    if not command or not os.path.isabs(command[0]):
        return None
    environment = {
        key: value
        for key, value in os.environ.items()
        if key.upper() in {"LANG", "LC_ALL", "SYSTEMROOT", "WINDIR"}
    }
    environment.update({"LANG": "C", "LC_ALL": "C"})
    try:
        result = subprocess.run(
            command,
            check=False,
            capture_output=True,
            env=environment,
            timeout=1.0,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if result.returncode != 0 or not result.stdout.strip():
        return None
    return result.stdout[:32768]


def _read_network_file(path: str) -> bytes | None:
    try:
        with open(path, "rb") as handle:
            value = handle.read(32769)
    except OSError:
        return None
    if not value or len(value) > 32768:
        return None
    return value


def _network_context_parts(system: str) -> list[bytes]:
    if system == "darwin":
        primary = _run_network_command(("/usr/sbin/scutil", "--nwi"))
        if primary is None:
            return []
        route = _run_network_command(("/sbin/route", "-n", "get", "default"))
        return [primary, *([route] if route is not None else [])]
    if system == "linux":
        route = _read_network_file("/proc/net/route")
        if route is None:
            return []
        parts = [route]
        for path in ("/proc/net/ipv6_route", "/etc/resolv.conf"):
            value = _read_network_file(path)
            if value is not None:
                parts.append(value)
        try:
            parts.append(f"netns:{os.stat('/proc/self/ns/net').st_ino}".encode("ascii"))
        except OSError:
            pass
        try:
            interfaces = sorted(Path("/sys/class/net").glob("*/address"))
        except OSError:
            interfaces = []
        for address_path in interfaces:
            value = _read_network_file(str(address_path))
            if value is not None:
                parts.append(address_path.parent.name.encode("utf-8") + b"=" + value)
        return parts
    return []


def _network_fingerprint() -> str | None:
    system = platform.system().strip().lower()
    parts = _network_context_parts(system)
    if not parts:
        return None
    digest = hashlib.sha256()
    digest.update(system.encode("ascii", errors="replace"))
    for part in parts:
        digest.update(b"\0")
        digest.update(part)
    return f"{system}:{digest.hexdigest()}"


def _cache_endpoint(endpoint: str) -> str | None:
    value = str(endpoint or "").strip()
    if not value or len(value) > 2048:
        return None
    try:
        parsed = urlsplit(value if "://" in value else "//" + value)
        hostname = parsed.hostname
        port = parsed.port
    except ValueError:
        return None
    if not hostname:
        return None
    host = hostname.lower()
    if ":" in host:
        host = f"[{host}]"
    scheme = parsed.scheme.lower()
    authority = f"{host}:{port}" if port is not None else host
    return f"{scheme}://{authority}" if scheme else authority


def _validate_oss_probe_cache(value: Any) -> list[dict[str, Any]]:
    if (
        not isinstance(value, dict)
        or set(value) != {"version", "entries"}
        or type(value.get("version")) is not int
        or value["version"] != _OSS_PROBE_CACHE_VERSION
    ):
        raise ValueError("invalid OSS probe cache version")
    entries = value.get("entries")
    if not isinstance(entries, list) or len(entries) > _OSS_PROBE_CACHE_MAX_ENTRIES:
        raise ValueError("invalid OSS probe cache entries")
    validated = []
    required = {"endpoint", "network", "reachable", "timestamp"}
    for entry in entries:
        if not isinstance(entry, dict) or set(entry) != required:
            raise ValueError("invalid OSS probe cache entry")
        endpoint = entry["endpoint"]
        network = entry["network"]
        reachable = entry["reachable"]
        timestamp = entry["timestamp"]
        if (
            not isinstance(endpoint, str)
            or not endpoint
            or len(endpoint) > 2048
            or _cache_endpoint(endpoint) != endpoint
        ):
            raise ValueError("invalid OSS probe cache endpoint")
        if (
            not isinstance(network, str)
            or len(network) > 128
            or re.fullmatch(r"[a-z0-9_-]+:[0-9a-f]{64}", network) is None
        ):
            raise ValueError("invalid OSS probe cache network")
        if not isinstance(reachable, bool):
            raise ValueError("invalid OSS probe cache result")
        if (
            isinstance(timestamp, bool)
            or not isinstance(timestamp, (int, float))
            or not math.isfinite(timestamp)
            or timestamp < 0
        ):
            raise ValueError("invalid OSS probe cache timestamp")
        validated.append(entry)
    return validated


def _private_path_stat(path: Path) -> os.stat_result:
    path_stat = path.lstat()
    if not stat.S_ISREG(path_stat.st_mode):
        raise PermissionError(f"unsafe OSS probe cache path: {path}")
    getuid = getattr(os, "getuid", None)
    if callable(getuid) and path_stat.st_uid != getuid():
        raise PermissionError(f"OSS probe cache is not owned by current user: {path}")
    if stat.S_IMODE(path_stat.st_mode) & 0o077:
        raise PermissionError(f"OSS probe cache permissions are too broad: {path}")
    return path_stat


def _prepare_oss_probe_cache_dir(path: Path) -> None:
    path.mkdir(mode=0o700, parents=True, exist_ok=True)
    path_stat = path.lstat()
    if not stat.S_ISDIR(path_stat.st_mode):
        raise PermissionError(f"unsafe OSS probe cache directory: {path}")
    getuid = getattr(os, "getuid", None)
    if callable(getuid) and path_stat.st_uid != getuid():
        raise PermissionError(f"OSS probe cache directory is not owned by current user: {path}")
    os.chmod(path, 0o700)


@contextmanager
def _oss_probe_cache_lock(
    path: Path,
    *,
    name: str = ".oss-probe.lock",
    timeout: float = 1.0,
    verbose: bool = False,
) -> Iterator[bool]:
    fd = -1
    try:
        import fcntl

        _prepare_oss_probe_cache_dir(path.parent)
        flags = os.O_CREAT | os.O_RDWR
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        fd = os.open(path.parent / name, flags, 0o600)
        lock_stat = os.fstat(fd)
        getuid = getattr(os, "getuid", None)
        if not stat.S_ISREG(lock_stat.st_mode) or (
            callable(getuid) and lock_stat.st_uid != getuid()
        ):
            raise PermissionError("unsafe OSS probe cache lock")
        os.fchmod(fd, 0o600)
        deadline = time.monotonic() + timeout
        while True:
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                if time.monotonic() >= deadline:
                    raise TimeoutError("timed out waiting for OSS probe cache lock")
                time.sleep(0.01)
    except Exception as exc:
        _probe_cache_log(verbose, f"lock unavailable ({type(exc).__name__})", "cache")
        if fd >= 0:
            try:
                os.close(fd)
            except OSError:
                pass
        yield False
        return
    try:
        yield True
    finally:
        try:
            fcntl.flock(fd, fcntl.LOCK_UN)
        except OSError:
            _probe_cache_log(verbose, "unlock failed", "cache")
        finally:
            try:
                os.close(fd)
            except OSError:
                _probe_cache_log(verbose, "lock close failed", "cache")


def _oss_probe_endpoint_lock_name(endpoint: str) -> str:
    digest = hashlib.sha256(endpoint.encode("utf-8")).hexdigest()[:24]
    return f".oss-probe-{digest}.lock"


def _read_oss_probe_cache(path: Path) -> list[dict[str, Any]]:
    file_stat = _private_path_stat(path)
    if file_stat.st_size > _OSS_PROBE_CACHE_MAX_BYTES:
        raise ValueError("invalid OSS probe cache file")
    flags = os.O_RDONLY
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    fd = os.open(path, flags)
    try:
        rendered = os.read(fd, _OSS_PROBE_CACHE_MAX_BYTES + 1)
    finally:
        os.close(fd)
    if len(rendered) > _OSS_PROBE_CACHE_MAX_BYTES:
        raise ValueError("invalid OSS probe cache file")
    return _validate_oss_probe_cache(json.loads(rendered.decode("utf-8")))


def _write_oss_probe_cache(path: Path, entries: list[dict[str, Any]]) -> None:
    cache_dir = path.parent
    _prepare_oss_probe_cache_dir(cache_dir)
    fd, temporary = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=cache_dir)
    temporary_path = Path(temporary)
    try:
        os.fchmod(fd, 0o600)
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            fd = -1
            json.dump(
                {"version": _OSS_PROBE_CACHE_VERSION, "entries": entries},
                handle,
                separators=(",", ":"),
                sort_keys=True,
            )
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, path)
        os.chmod(path, 0o600)
    finally:
        if fd >= 0:
            os.close(fd)
        try:
            temporary_path.unlink()
        except FileNotFoundError:
            pass


def _probe_cache_log(verbose: bool, status: str, endpoint: str) -> None:
    if verbose:
        typer.echo(f"OSS probe cache {status}: {endpoint}", err=True)


def _cached_oss_probe(
    endpoint: str,
    probe: Any,
    *,
    verbose: bool,
    fingerprints: dict[str, str],
    state_lock: Any,
    fingerprint: Any = _NETWORK_FINGERPRINT_UNSET,
    checked_at: Callable[[float], None] | None = None,
) -> bool:
    def run_probe() -> bool:
        reachable = bool(probe(endpoint))
        if checked_at is not None:
            checked_at(_now())
        return reachable

    cache_endpoint = _cache_endpoint(endpoint)
    if fingerprint is _NETWORK_FINGERPRINT_UNSET:
        fingerprint = _network_fingerprint()
    if cache_endpoint is None or fingerprint is None:
        status = "bypass (network context unavailable)" if fingerprint is None else "bypass"
        _probe_cache_log(verbose, status, cache_endpoint or "invalid endpoint")
        return run_probe()

    with state_lock:
        fingerprints[cache_endpoint] = fingerprint
    path = _oss_probe_cache_path()
    endpoint_lock_name = _oss_probe_endpoint_lock_name(cache_endpoint)
    with _oss_probe_cache_lock(
        path, name=endpoint_lock_name, timeout=4.0, verbose=verbose
    ) as endpoint_locked:
        if not endpoint_locked:
            _probe_cache_log(verbose, "bypass (cache busy)", cache_endpoint)
            return run_probe()

        now = _now()
        status = "miss"
        with _oss_probe_cache_lock(path, verbose=verbose) as read_locked:
            if not read_locked:
                _probe_cache_log(verbose, "bypass (cache unavailable)", cache_endpoint)
                return run_probe()
            try:
                entries = _read_oss_probe_cache(path)
            except FileNotFoundError:
                entries = []
            except Exception:
                entries = []
                status = "invalid"

        for entry in entries:
            if entry["endpoint"] != cache_endpoint or entry["network"] != fingerprint:
                continue
            age = now - entry["timestamp"]
            if 0 <= age < _OSS_PROBE_CACHE_TTL:
                _probe_cache_log(verbose, "hit", cache_endpoint)
                if checked_at is not None:
                    checked_at(entry["timestamp"])
                return entry["reachable"]
            status = "stale"
            break

        _probe_cache_log(verbose, status, cache_endpoint)
        reachable = run_probe()
        with _oss_probe_cache_lock(path, verbose=verbose) as write_locked:
            if not write_locked:
                _probe_cache_log(verbose, "write skipped (cache busy)", cache_endpoint)
                return reachable
            try:
                latest_entries = _read_oss_probe_cache(path)
            except Exception:
                latest_entries = []
            now = _now()
            fresh_entries = [
                entry
                for entry in latest_entries
                if 0 <= now - entry["timestamp"] < _OSS_PROBE_CACHE_TTL
                and not (entry["endpoint"] == cache_endpoint and entry["network"] == fingerprint)
            ]
            fresh_entries.append(
                {
                    "endpoint": cache_endpoint,
                    "network": fingerprint,
                    "reachable": reachable,
                    "timestamp": now,
                }
            )
            try:
                _write_oss_probe_cache(path, fresh_entries[-_OSS_PROBE_CACHE_MAX_ENTRIES:])
            except Exception:
                _probe_cache_log(verbose, "write failed", cache_endpoint)
        return reachable


def _invalidate_oss_probe_cache(
    endpoint: str,
    fingerprint: str | None,
    *,
    verbose: bool,
) -> None:
    cache_endpoint = _cache_endpoint(endpoint)
    if cache_endpoint is None:
        return
    path = _oss_probe_cache_path()
    endpoint_lock_name = _oss_probe_endpoint_lock_name(cache_endpoint)
    with _oss_probe_cache_lock(
        path, name=endpoint_lock_name, timeout=4.0, verbose=verbose
    ) as endpoint_locked:
        if not endpoint_locked:
            return
        with _oss_probe_cache_lock(path, verbose=verbose) as locked:
            if not locked:
                return
            try:
                entries = _read_oss_probe_cache(path)
            except Exception:
                return
            remaining = [
                entry
                for entry in entries
                if not (
                    entry["endpoint"] == cache_endpoint
                    and (fingerprint is None or entry["network"] == fingerprint)
                )
            ]
            if len(remaining) == len(entries):
                return
            try:
                _write_oss_probe_cache(path, remaining)
            except Exception:
                return
    _probe_cache_log(verbose, "invalidated after connection error", cache_endpoint)


def _sdk_reachability_classifier() -> Callable[[BaseException], bool] | None:
    try:
        from instance_repo._routing import _is_reachability_error
    except (ImportError, AttributeError):
        return None
    return _is_reachability_error


def _install_connection_error_invalidation(
    content: Any,
    fingerprints: dict[str, str],
    *,
    verbose: bool,
    classifier: Callable[[BaseException], bool],
    state_lock: Any,
    reset_network: Callable[[], None],
    endpoint_lock: Callable[[str], Any],
) -> bool:
    open_bucket = getattr(content, "_open_bucket", None)
    execute = getattr(content, "_do", None)
    if not callable(open_bucket) or not callable(execute):
        return False
    try:
        open_signature = inspect.signature(open_bucket)
        if "endpoint" not in open_signature.parameters:
            return False
    except (TypeError, ValueError):
        return False

    active = threading.local()
    bucket_endpoints: weakref.WeakKeyDictionary[Any, str] = weakref.WeakKeyDictionary()

    def tracked_open_bucket(*args: Any, **kwargs: Any) -> Any:
        endpoint = open_signature.bind(*args, **kwargs).arguments.get("endpoint")
        active.endpoint = endpoint if isinstance(endpoint, str) else None
        try:
            bucket = open_bucket(*args, **kwargs)
            if active.endpoint:
                with state_lock:
                    try:
                        bucket_endpoints[bucket] = active.endpoint
                    except TypeError:  # Some custom bucket factories cannot be weak-referenced.
                        pass
            return bucket
        except Exception:
            active.endpoint = None
            raise

    def tracked_execute(*args: Any, **kwargs: Any) -> Any:
        endpoint = getattr(active, "endpoint", None)
        operation = args[0] if args else kwargs.get("fn")
        try:
            captured = list(inspect.getclosurevars(operation).nonlocals.values())
        except (TypeError, ValueError):
            captured = []
        captured.extend(getattr(operation, "args", ()))
        with state_lock:
            for value in captured:
                try:
                    selected = bucket_endpoints.get(value)
                except TypeError:
                    continue
                if selected:
                    endpoint = selected
                    break
        try:
            return execute(*args, **kwargs)
        except Exception as exc:
            if endpoint and classifier(exc):
                reset_network()
                cache_endpoint = _cache_endpoint(endpoint)
                with endpoint_lock(endpoint):
                    with state_lock:
                        fingerprint = fingerprints.get(cache_endpoint or "")
                        probe_cache = getattr(content, "_probe_cache", None)
                        if isinstance(probe_cache, dict):
                            probe_cache.pop(endpoint, None)
                    _invalidate_oss_probe_cache(endpoint, fingerprint, verbose=verbose)
            raise
        finally:
            active.endpoint = None

    try:
        content._open_bucket = tracked_open_bucket
        content._do = tracked_execute
    except (AttributeError, TypeError):
        try:
            content._open_bucket = open_bucket
            content._do = execute
        except (AttributeError, TypeError):
            pass
        return False
    return True


def _install_oss_probe_cache(repo: Any, *, verbose: bool) -> bool:
    content = getattr(repo, "_content", None)
    probe = getattr(content, "_probe_private_endpoint", None)
    sdk_cached_probe = getattr(content, "_probe_cached", None)
    probe_cache = getattr(content, "_probe_cache", None)
    open_bucket = getattr(content, "_open_bucket", None)
    execute = getattr(content, "_do", None)
    classifier = _sdk_reachability_classifier()
    if getattr(content, "_ap_probe_cache_installed", False):
        return True
    if (
        not callable(probe)
        or not callable(sdk_cached_probe)
        or not isinstance(probe_cache, dict)
        or not callable(open_bucket)
        or not callable(execute)
        or classifier is None
    ):
        _probe_cache_log(verbose, "unavailable (unsupported SDK hooks)", "SDK")
        return False

    fingerprints: dict[str, str] = {}
    fingerprint_context = threading.local()
    state_lock = threading.RLock()
    network_lock = threading.Lock()
    network_checked_at: float | None = None
    network_value: str | None = None

    def current_network() -> str | None:
        nonlocal network_checked_at, network_value
        with network_lock:
            now = _monotonic()
            if (
                network_checked_at is None
                or not 0 <= now - network_checked_at < _NETWORK_FINGERPRINT_TTL
            ):
                network_value = _network_fingerprint()
                network_checked_at = _monotonic()
            return network_value

    def reset_network() -> None:
        nonlocal network_checked_at
        with network_lock:
            network_checked_at = None

    def cached_probe(endpoint: str) -> bool:
        fingerprint = getattr(fingerprint_context, "value", _NETWORK_FINGERPRINT_UNSET)
        if fingerprint is _NETWORK_FINGERPRINT_UNSET:
            fingerprint = current_network()
        return _cached_oss_probe(
            endpoint,
            probe,
            verbose=verbose,
            fingerprints=fingerprints,
            state_lock=state_lock,
            fingerprint=fingerprint,
            checked_at=lambda timestamp: setattr(fingerprint_context, "checked_at", timestamp),
        )

    memory_networks: dict[str, str] = {}
    endpoint_locks: dict[str, Any] = {}

    def endpoint_lock(endpoint: str) -> Any:
        with state_lock:
            return endpoint_locks.setdefault(endpoint, threading.RLock())

    def network_aware_cached_probe(endpoint: str) -> bool:
        # Serialize only matching endpoints; no global state lock during SDK/file IO.
        with endpoint_lock(endpoint):
            fingerprint = current_network()
            with state_lock:
                if fingerprint is not None and memory_networks.get(endpoint) != fingerprint:
                    probe_cache.pop(endpoint, None)
                    memory_networks[endpoint] = fingerprint
            fingerprint_context.value = fingerprint
            fingerprint_context.checked_at = None
            try:
                reachable = bool(sdk_cached_probe(endpoint))
                # SDK timestamps newly acquired results. A disk-cache hit must
                # retain its original age instead of receiving another 300s.
                if fingerprint_context.checked_at is not None:
                    with state_lock:
                        cached = probe_cache.get(endpoint)
                        if (
                            isinstance(cached, tuple)
                            and len(cached) == 2
                            and isinstance(cached[0], bool)
                            and isinstance(cached[1], (int, float))
                            and not isinstance(cached[1], bool)
                            and math.isfinite(cached[1])
                            and cached[1] >= 0
                        ):
                            probe_cache[endpoint] = (reachable, fingerprint_context.checked_at)
                return reachable
            finally:
                del fingerprint_context.value
                del fingerprint_context.checked_at

    try:
        content._probe_private_endpoint = cached_probe
        content._probe_cached = network_aware_cached_probe
        content._ap_probe_cache_installed = True
    except (AttributeError, TypeError):
        _probe_cache_log(verbose, "unavailable (SDK hooks are read-only)", "SDK")
        try:
            content._probe_private_endpoint = probe
            content._probe_cached = sdk_cached_probe
            if hasattr(content, "_ap_probe_cache_installed"):
                del content._ap_probe_cache_installed
        except (AttributeError, TypeError):
            pass
        return False
    if not _install_connection_error_invalidation(
        content,
        fingerprints,
        verbose=verbose,
        classifier=classifier,
        state_lock=state_lock,
        reset_network=reset_network,
        endpoint_lock=endpoint_lock,
    ):
        _probe_cache_log(verbose, "unavailable (unsupported SDK bucket hook)", "SDK")
        try:
            content._probe_private_endpoint = probe
            content._probe_cached = sdk_cached_probe
            del content._ap_probe_cache_installed
        except (AttributeError, TypeError):
            pass
        return False
    return True


# ---------------------------------------------------------------------------
# Repo 构造
# ---------------------------------------------------------------------------


def _cluster_from_headers(headers: dict[str, str]) -> str:
    for key, value in headers.items():
        if key.lower() == "x-cluster":
            return value.strip()
    return ""


def _env_header(headers: dict[str, str]) -> str:
    """AP 注入的 ``Env`` 头值(config.py 按 cluster 推导 debug/test/product)。

    SDK 的 ``api_env`` 就是这个头的取值,读写两侧必须一致;不下发时 SDK 默认
    ``product``,在 test/debug 集群上会被网关路由到错误环境。
    """
    for key, value in headers.items():
        if key.lower() == "env":
            return value.strip()
    return ""


def _resolve_storage_env(storage_env: str | None) -> str:
    if storage_env is not None and storage_env.strip():
        return storage_env.strip()
    for name in _STORAGE_ENV_VARS:
        value = os.environ.get(name, "").strip()
        if value:
            return value
    return ""


def _setdefault_env(name: str, value: str) -> None:
    """只在用户没设过时注入,绝不覆盖显式设置的值。"""
    if value and not os.environ.get(name, "").strip():
        os.environ[name] = value


def _sdk_log_value(raw: bytes | str | None, cfg: Any) -> str:
    if raw is None:
        return ""
    text = raw.decode("utf-8", errors="replace") if isinstance(raw, bytes) else raw
    try:
        value = json.loads(text)
    except (TypeError, ValueError):
        if cfg.verbose_redaction:
            return "<non-JSON body omitted>"
        rendered = text
    else:
        from .api import _redact_sensitive_data, _safe_json

        value = _redact_sensitive_data(value, cfg.verbose_redaction)
        if cfg.verbose_redaction:
            value = _redact_sdk_tokens(value)
        rendered = _safe_json(value)
    if cfg.verbose_full_body or len(rendered) <= cfg.verbose_body_limit:
        return rendered
    return rendered[: cfg.verbose_body_limit] + "..."


def _redact_sdk_tokens(value: Any) -> Any:
    if isinstance(value, dict):
        redacted = {}
        for key, item in value.items():
            normalized = str(key).lower().replace("_", "").replace("-", "")
            redacted[key] = (
                "<redacted>" if normalized.endswith("token") else _redact_sdk_tokens(item)
            )
        return redacted
    if isinstance(value, list):
        return [_redact_sdk_tokens(item) for item in value]
    return value


def _instrument_sdk_transport(transport: Any, cfg: Any) -> bool:
    sender = getattr(transport, "_send", None)
    if not callable(sender):
        return False

    from .api import _redact_headers, _redact_url_query_secrets, _safe_json, _write_stderr

    def logged_send(method: str, url: str, headers: dict, body: bytes | None, timeout: float):
        shown_url = _redact_url_query_secrets(url) if cfg.verbose_redaction else url
        lines = [
            f">> Request {method} {shown_url}",
            f"   headers={_safe_json(_redact_headers(headers, cfg.verbose_redaction))}",
        ]
        if body is not None:
            lines.extend((f"   body_size={len(body)}", f"   body={_sdk_log_value(body, cfg)}"))
        _write_stderr(lines)
        started = time.perf_counter()
        try:
            status, text = sender(method, url, headers, body, timeout)
        except Exception as exc:
            duration_ms = (time.perf_counter() - started) * 1000
            _write_stderr(
                [
                    f"!! Error {method} {shown_url}",
                    f"   duration_ms={duration_ms:.1f}",
                    f"   error={type(exc).__name__}: {exc}",
                ]
            )
            raise
        duration_ms = (time.perf_counter() - started) * 1000
        encoded = text.encode("utf-8", errors="replace")
        response_lines = [
            f"<< Response {method} {shown_url}",
            f"   status={status}",
            f"   duration_ms={duration_ms:.1f}",
            f"   body_size={len(encoded)}",
        ]
        if text:
            response_lines.append(f"   body={_sdk_log_value(text, cfg)}")
        _write_stderr(response_lines)
        return status, text

    transport._send = logged_send
    return True


def _verbose_sdk_transport(cfg: Any, api_env: str) -> Any | None:
    try:
        from instance_repo.transport import Transport
    except ImportError:
        return None
    transport = Transport(cfg.base_url, cfg.token_key or "", env=api_env)
    return transport if _instrument_sdk_transport(transport, cfg) else None


def load_repo(
    *,
    cluster: str | None = None,
    storage_env: str | None = None,
    environment: str | None = None,
    request_timeout: float | None = None,
) -> "Repo":
    """按 AP ``Config`` 构造 ``instance_repo.Repo``。

    Args:
        cluster: 目标集群;``None`` 时沿用 ``--cluster`` / ``AP_CLUSTER`` 的解析结果。
        environment: 按 online/pre 选择数据面,覆盖 cluster 的存储绑定。
            ``"auto"`` 等价于 ``None``(不下发,完全跟随集群绑定)。
        storage_env: 数据面存储环境;``None`` 时取 ``INSTANCE_REPO_STORAGE_ENV``
            或旧别名 ``IR_STORAGE_ENV``。**不提供默认值**。

    Raises:
        SdkMissing: 未安装 ``ap-client[dataset]``。
        ConfigurationError: AP 认证/连接配置不可用(如 ``AP_API_KEYS`` 里放了
            多个逗号分隔的 key —— CLI 只接受单 key)。
    """
    try:
        from instance_repo import Repo as _Repo
    except ImportError as exc:
        raise SdkMissing() from exc

    from . import api as _api

    if environment == "auto":
        environment = None

    # 多 key 的 AP_API_KEYS 在这里直接抛 ConfigurationError:数据面要用这把 key 去
    # 换 STS,拿不到确定的单 key 就没法继续(与控制面同一口径)。
    cfg = get_config(
        verbose=_api._verbose_override,
        cluster=cluster if cluster is not None else _api._cluster_override,
    )

    effective_cluster = _cluster_from_headers(cfg.headers)
    effective_storage_env = _resolve_storage_env(storage_env)
    api_env = _env_header(cfg.headers)

    supported = _init_parameters(_Repo)
    kwargs: dict[str, Any] = {}
    if environment is not None:
        if "environment" not in supported:
            raise SdkMissing(
                "The installed instance-repo SDK does not support environment-scoped storage.\n"
                "Install it with: pip install 'ap-client[dataset]' --upgrade"
            )
        kwargs["environment"] = environment
    if "token" in supported and cfg.token_key:
        kwargs["token"] = cfg.token_key
    if "api_base" in supported:
        kwargs["api_base"] = cfg.base_url
    if "cluster" in supported and effective_cluster:
        kwargs["cluster"] = effective_cluster
    if "storage_env" in supported and effective_storage_env:
        kwargs["storage_env"] = effective_storage_env
    if "api_env" in supported and api_env:
        kwargs["api_env"] = api_env
    if cfg.verbose and "transport" in supported:
        transport = _verbose_sdk_transport(cfg, api_env)
        if transport is not None:
            if request_timeout is not None:
                transport.timeout = request_timeout
            kwargs["transport"] = transport
    if request_timeout is not None and "transport" in supported and "transport" not in kwargs:
        # Inject a pre-configured Transport so the custom timeout is effective
        # from the very first HTTP call inside Repo.__init__ / _bind_dataset_profile.
        try:
            from instance_repo.transport import Transport as _Transport
        except ImportError:
            _Transport = None
        if _Transport is not None:
            kwargs["transport"] = _Transport(
                cfg.base_url,
                cfg.token_key or "",
                env=api_env,
                timeout=request_timeout,
            )

    if "api_base" not in supported or "cluster" not in supported:
        # 0.8.x 兼容路径:构造参数缺位,只能退回环境变量契约。
        _setdefault_env(_LEGACY_API_BASE_VAR, cfg.base_url)
        _setdefault_env(_LEGACY_TOKEN_VAR, cfg.token_key or "")
        _setdefault_env(_LEGACY_STORAGE_ENV_VAR, effective_storage_env)

    repo = _Repo(**kwargs)
    _bind_dataset_profile(repo)
    _install_oss_probe_cache(repo, verbose=cfg.verbose)
    _install_user_data_directory_listing(repo)
    return repo


def _install_user_data_directory_listing(repo: Any) -> bool:
    """Keep the directory boundary lost by instance-repo 1.4.0 list_user_data.

    Use the SDK's path validation and content store so STS authorization,
    endpoint selection and pagination retain their normal behavior. Normalize
    here until the SDK dependency includes its directory-prefix fix.
    """
    content = getattr(repo, "_content", None)
    prefix_for = getattr(repo, "_user_data_prefix", None)
    clean = getattr(repo, "_clean_user_data_subpath", None)
    if not all(
        callable(fn)
        for fn in (
            getattr(repo, "list_user_data", None),
            prefix_for,
            clean,
            getattr(content, "list_objects", None),
        )
    ):
        return False

    def list_user_data(uid: str, subpath: str = "") -> list[str]:
        from instance_repo.errors import SchemaError

        if not str(uid).strip():
            raise SchemaError("uid must not be empty")
        prefix = prefix_for(uid)
        if str(subpath).strip():
            prefix += clean(subpath) + "/"
        return content.list_objects(prefix)

    repo.list_user_data = list_user_data
    return True


def _bind_dataset_profile(repo: Any) -> None:
    """Supply the configured context missing from SDK 1.3.5 dataset discovery.

    Its environment check reads ``_p``, but its constructor does not initialize
    that field. Bind only a missing field to this Repo's resolved profile;
    SDKs that initialize it retain their own context.
    """
    client = getattr(repo, "datasets", None)
    profile = getattr(repo, "profile", None)
    if (
        profile is not None
        and callable(getattr(client, "_discovery_env_match", None))
        and not hasattr(client, "_p")
    ):
        client._p = profile


def _init_parameters(repo_cls: type) -> frozenset[str]:
    """``Repo.__init__`` 接受的关键字参数名;签名不可读时返回空集合。"""
    try:
        signature = inspect.signature(repo_cls.__init__)
    except (TypeError, ValueError):  # pragma: no cover - 只在异常 SDK 打桩时触发
        return frozenset()
    names = set()
    for name, parameter in signature.parameters.items():
        if name == "self":
            continue
        if parameter.kind is inspect.Parameter.VAR_KEYWORD:
            # **kwargs 会吞下任何参数,当作全部支持(1.0.0 之后的宽松签名)。
            return frozenset(
                names
                | {
                    "token",
                    "api_base",
                    "cluster",
                    "storage_env",
                    "api_env",
                    "transport",
                    "environment",
                }
            )
        if parameter.kind is not inspect.Parameter.VAR_POSITIONAL:
            names.add(name)
    return frozenset(names)


def load_ossutil_repo() -> tuple[Any, dict]:
    """Read the complete OSS binding through SDK transport, with server-owned addressing."""
    from dataclasses import replace

    from . import api as _api
    from .config import ConfigurationError

    try:
        from instance_repo import Repo as RepoClass
        from instance_repo.clients.config import resolve_cluster
        from instance_repo.transport import Transport
    except ImportError as exc:
        raise SdkMissing() from exc

    cfg = get_config(verbose=_api._verbose_override, cluster=_api._cluster_override)
    cluster = _cluster_from_headers(cfg.headers)
    if not cluster:
        raise ConfigurationError("Set --cluster / AP_CLUSTER before using ap dfs")
    if not cfg.token_key:
        raise ConfigurationError("Set AP_API_KEY before using ap dfs")
    transport = Transport(cfg.base_url, cfg.token_key, env=_env_header(cfg.headers))
    if cfg.verbose:
        # STS material must stay redacted even when general HTTP redaction is disabled.
        _instrument_sdk_transport(transport, replace(cfg, verbose_redaction=True))
    from urllib.parse import urlencode

    canonical_cluster = resolve_cluster(transport, cluster)
    payload = transport.get("/apis/v1/repo-config?" + urlencode({"cluster": canonical_cluster}))
    if not isinstance(payload, dict) or not isinstance(payload.get("oss"), dict):
        raise ConfigurationError("repo-config did not provide an OSS storage binding")
    oss = payload["oss"]
    for field in ("bucket", "prefix", "region", "endpoint"):
        if not isinstance(oss.get(field), str) or not oss[field].strip():
            raise ConfigurationError(f"repo-config OSS binding is missing {field}")
    storage_env = payload.get("storage_env")
    if not isinstance(storage_env, str) or not storage_env.strip():
        raise ConfigurationError("repo-config did not provide storage_env")
    repo = RepoClass(
        token=cfg.token_key,
        api_base=cfg.base_url,
        api_env=_env_header(cfg.headers),
        cluster=canonical_cluster,
        storage_env=storage_env,
        transport=transport,
        profile_overrides={"oss_bucket": oss["bucket"], "oss_prefix": oss["prefix"]},
    )
    _install_oss_probe_cache(repo, verbose=cfg.verbose)
    return repo, dict(oss)


# ---------------------------------------------------------------------------
# 错误翻译
# ---------------------------------------------------------------------------

# 数字业务码 → (hint, 退出码)。按 ``getattr(exc, "biz_code", None)`` 分派,
# **不 import 数值异常类**:release/v1.0.0 上并不存在 24401/24402/24404/94022/94023
# 对应的类(它们只在 feat/sdk-user-data-acl 分支)。
_BIZ_CODE_RULES: dict[int, tuple[str, int]] = {
    94016: (
        "Ask the dataset admin to run: ap dataset access grant <dataset> "
        "--user <your-id> --role writer",
        1,
    ),
    94017: (
        "This dataset is not claimed yet; run: ap dataset claim <dataset> --workspace <ws> --benchmark <b>",
        1,
    ),
    94018: (
        "Current role is read-only; writes need the writer role. Ask an admin to run ap dataset access grant",
        1,
    ),
    94019: (
        "Dataset identity conflict: check whether --dataset collides with an existing dataset name",
        1,
    ),
    94020: (
        "Request carried no dataset identity (SDK too old); upgrade: pip install -U 'instance-repo[oss]>=1.1.2'",
        1,
    ),
    94021: ("This dataset does not exist; run: ap dataset create <dataset> --benchmark <b>", 1),
    92024: (
        "Dataset namespace conflict: a root (L1) and child (L1/L2) dataset cannot share "
        "a namespace. Rename the new dataset, or register the data as a split of the "
        "existing dataset: ap dataset register <existing> --unversioned --split <name>",
        1,
    ),
    94022: (
        "No access grant on this user storage space; ask the owner to run: ap fs access grant --user <your-id> --role reader",
        1,
    ),
    94023: (
        "No write grant on this user storage space; ask the owner to run: ap fs access grant --user <your-id> --role writer",
        1,
    ),
    24401: ("Binding does not exist; already in the desired state, nothing to do", 0),
    24402: ("Check the user/group id; make sure AP_CLUSTER points to a dataset-enabled cluster", 2),
    24404: ("Binding already exists; already in the desired state, nothing to do", 0),
    92005: (
        "Check that --benchmark exists; for ingest layout ambiguity, pass splits explicitly or set --version",
        1,
    ),
}

# 字符串 ``code`` → (hint, 退出码)。SDK 的 ``InstanceRepoError.code``。
_CODE_RULES: dict[str, tuple[str, int]] = {
    "E_PRIVATE_NETWORK_REQUIRED": (
        "This operation requires private-network access; run inside an AP dev cluster / ROCK VPC",
        1,
    ),
    "E_DIGEST_MISMATCH": ("Content digest check failed; pull or repack the instance again", 1),
    "E_IMMUTABLE": ("Published versions are immutable; create a new version instead", 1),
    "E_FORBIDDEN": ("Current identity is not authorized; check AP_API_KEY and dataset role", 1),
    "E_OWNER_REF_MISSING": (
        "Missing upstream source reference; upgrade: pip install -U 'instance-repo[oss]>=1.1.2'",
        1,
    ),
    "E_LAYOUT": (
        "Instance directory layout is invalid; run ap instance validate <path> to locate the problem",
        1,
    ),
    "E_SCHEMA": (
        "Instance metadata does not match the schema; run ap instance validate <path> to locate the problem",
        1,
    ),
    "E_CRED_EXPIRED": ("Temporary credentials expired; rerun the command to fetch new ones", 1),
    "E_NETWORK_DENIED": (
        "Network access denied; make sure this environment can reach the OSS endpoint",
        1,
    ),
    "E_JOB_FAILED": (
        "Remote job failed; use ap dataset version get to see the version status and failure reason",
        1,
    ),
    "E_WRITE_OUTCOME_UNKNOWN": (
        "Write outcome unknown; verify the actual state with the corresponding get/list command before retrying",
        1,
    ),
}

#: 无法归类时的兜底文案。
_FALLBACK_HINT = (
    "Rerun with -v/--verbose for the full traceback; contact the Agent Platform on-call if needed"
)

# 数据面寻址字段:``/apis/v1/repo-config`` 在当前 apiserver 里不存在(设计 §8.3),SDK 的
# 自动发现是 best-effort、构造期不抛错,真正用到某字段时才由 ``bootstrap.require`` 抛
# ``SchemaError``(code ``E_SCHEMA``)。裸 ``E_SCHEMA`` 的文案("先跑 ap instance validate")
# 对这类失败是错的,所以先按 message 里出现的寻址字段名单独识别。
_ADDRESSING_FIELDS = (
    "oss_bucket",
    "oss_prefix",
    "scaffold_bucket",
    "scaffold_root",
    "storage_path",
)
_ADDRESSING_HINT = (
    "The current AP cluster does not provide data-plane storage config; make sure "
    "AP_CLUSTER points to a dataset-enabled cluster, or contact the Dataset admin"
)


def _is_addressing_failure(exc: Exception) -> bool:
    if getattr(exc, "code", None) != "E_SCHEMA":
        return False
    text = _reason(exc)
    return "repo-config" in text or any(field in text for field in _ADDRESSING_FIELDS)


def is_already_satisfied(exc: Exception) -> bool:
    """该异常是否属于设计 §5.1 的幂等码(已达目标态,退出 0)。

    ``fs access grant/revoke`` 这类命令在拿到 24401/24404 时仍要按 ``--format``
    输出正常结果,不能走 :func:`sdk_error_exit` 的 ``raise typer.Exit(0)`` —— 那会
    在打印 stdout 之前就结束进程。它们用本函数分派,码表仍只有这一份。
    """
    return _resolve_rule(exc)[1] == 0


def _is_verbose() -> bool:
    from . import api as _api

    if _api._verbose_override is not None:
        return bool(_api._verbose_override)
    return _parse_bool(os.environ.get("AP_VERBOSE"))


#: 集群绑定存储 → 环境侧(dev 三个变体都是 pre 侧),与 dataset_commands._STORAGE_SIDES 同口径。
_STORAGE_SIDES = {
    "dev": "pre",
    "internal-dev": "pre",
    "external-dev": "pre",
    "prod": "online",
}


def _derive_environment(repo: Any) -> str:
    """``auto`` 的实际取值:按 repo profile 的集群存储绑定派生,未知回退 online。"""
    profile = getattr(repo, "profile", None)
    storage_env = str(getattr(profile, "storage_env", "") or "").strip().lower()
    return _STORAGE_SIDES.get(storage_env, "online")


def update_version_detail(
    repo: Any,
    dataset: str,
    version: str,
    body: dict,
    *,
    environment: str,
    metadata_model: str = "",
) -> None:
    """``PATCH /apis/v1/datasets/versions/detail`` with explicit routing selectors."""
    if environment == "auto":
        # auto 是 CLI 层取值(跟随集群绑定),服务端契约只有 online/pre。直连
        # transport 的兼容分支必须显式带上派生值——只删 query 会落到服务端
        # 缺省 online,在 dev 集群上造成读写撕裂;SDK 分支传派生值与 SDK 自行
        # 按 profile 派生等价,两条路径口径一致。
        environment = _derive_environment(repo)
    update = repo.versions.update
    try:
        accepted = inspect.signature(update).parameters
    except (TypeError, ValueError):  # pragma: no cover - 内建/装饰过的可调用
        accepted = {}
    if "environment" in accepted and "metadata_model" in accepted:
        kwargs = dict(body)
        if environment:
            kwargs["environment"] = environment
        if metadata_model:
            kwargs["metadata_model"] = metadata_model
        update(dataset, version, **kwargs)
        return

    from urllib.parse import quote

    query = f"dataset_name={quote(dataset, safe='')}&version={quote(version, safe='')}"
    if environment:
        query += f"&environment={quote(environment, safe='')}"
    if metadata_model:
        query += f"&metadata_model={quote(metadata_model, safe='')}"
    repo.transport.patch(f"/apis/v1/datasets/versions/detail?{query}", dict(body))


def _reason(exc: Exception) -> str:
    message = getattr(exc, "message", None)
    text = str(message or "").strip() or str(exc).strip()
    return text or type(exc).__name__


def _resolve_rule(exc: Exception) -> tuple[str, int]:
    biz_code = getattr(exc, "biz_code", None)
    if isinstance(biz_code, int) and not isinstance(biz_code, bool):
        rule = _BIZ_CODE_RULES.get(biz_code)
        if rule is not None:
            return rule
    code = getattr(exc, "code", None)
    if _is_addressing_failure(exc):
        return _ADDRESSING_HINT, 1
    if isinstance(code, str):
        rule = _CODE_RULES.get(code)
        if rule is not None:
            return rule
    return _FALLBACK_HINT, 1


def sdk_error_exit(exc: Exception, *, what: str, stage: str) -> NoReturn:
    """把 SDK 异常翻译成 ``error:`` / ``hint:`` 文案与 ``typer.Exit``。

    设计 §5.1 里判定为幂等的 24401/24404 直接以 0 退出；非零失败输出固定
    ``error: <what> <stage>失败:<reason>`` 与可执行 ``hint:``。
    """
    hint, exit_code = _resolve_rule(exc)
    if exit_code != 0:
        typer.echo(f"error: {what} {stage} failed: {_reason(exc)}", err=True)
        typer.echo(f"hint: {hint}", err=True)
        if _is_verbose():
            import traceback

            traceback.print_exception(type(exc), exc, exc.__traceback__)
    raise typer.Exit(exit_code)
