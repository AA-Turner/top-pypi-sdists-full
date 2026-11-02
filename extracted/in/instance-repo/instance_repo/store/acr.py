"""ACR image store with private-first, pre-write skopeo routing."""
from __future__ import annotations

import base64
import contextlib
import json
import os
import re
import subprocess
import tempfile
import time
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Callable

from .._routing import _plan_acr_route
from ..errors import PrivateNetworkRequired, TransportError, WriteOutcomeUnknown
from .base import BaseImageStore

# Injected runners intentionally retain the historical one-argument signature.
Runner = Callable[[list], "tuple[int, str, str]"]

_DEFAULT_COMMAND_TIMEOUT_SECONDS = 120.0
_DEFAULT_OPERATION_DEADLINE_SECONDS = 300.0
_TIMEOUT_RETURN_CODE = 124

# Versioned, deliberately small stderr allowlists. Unknown skopeo output is never
# treated as either absence or a connectivity failure.
_MANIFEST_NOT_FOUND_MARKERS_V1 = (
    "manifest unknown",
    "manifest not found",
)
_MANIFEST_ERROR_MARKERS_V1 = (
    "unauthorized",
    "authentication required",
    "access denied",
    "permission denied",
    "forbidden",
    "x509",
    "certificate",
    "tls",
)
_CONNECTIVITY_MARKERS_V1 = (
    "no such host",
    "temporary failure in name resolution",
    "name or service not known",
    "nodename nor servname provided, or not known",
    "connection timed out",
    "i/o timeout",
    "context deadline exceeded",
    "connection refused",
    "connection reset by peer",
    "network is unreachable",
    "no route to host",
    "host is unreachable",
)
_NO_FALLBACK_MARKERS_V1 = (
    "unauthorized",
    "authentication required",
    "access denied",
    "permission denied",
    "forbidden",
    "x509",
    "certificate",
    "tls",
    "http status",
    "status code",
)
_HTTP_STATUS_RE = re.compile(
    r"\b(?:status\s*code|http(?:/\d(?:\.\d)?)?(?:\s+response)?"
    r"(?:\s+status(?:\s+code)?)?|response\s+status(?:\s+code)?)"
    r"\s*[:=]?\s*[1-5]\d{2}\b",
    re.IGNORECASE,
)
_DIGEST_RE = re.compile(r"^[a-z0-9_+.-]+:[0-9a-fA-F]+$")


class _InspectState(str, Enum):
    PRESENT = "present"
    ABSENT = "absent"
    ERROR = "error"


@dataclass(frozen=True)
class _InspectResult:
    state: _InspectState
    digest: str | None = None
    stderr: str = ""


@dataclass(frozen=True)
class _SelectedRoute:
    canonical_ref: str
    actual_ref: str
    inspect: _InspectResult


@dataclass(frozen=True)
class _CommandResult:
    returncode: int
    stdout: str
    stderr: str
    started: bool

    def as_runner_result(self) -> tuple[int, str, str]:
        return self.returncode, self.stdout, self.stderr


def _run_subprocess_result(argv: list, timeout: float) -> _CommandResult:
    try:
        result = subprocess.run(
            [str(part) for part in argv],
            capture_output=True,
            text=True,
            timeout=max(timeout, 0.001),
        )
        return _CommandResult(result.returncode, result.stdout, result.stderr, True)
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout.decode(errors="replace") if isinstance(exc.stdout, bytes) else (exc.stdout or "")
        stderr = exc.stderr.decode(errors="replace") if isinstance(exc.stderr, bytes) else (exc.stderr or "")
        if stderr and not stderr.endswith("\n"):
            stderr += "\n"
        stderr += "skopeo subprocess deadline exceeded"
        return _CommandResult(
            _TIMEOUT_RETURN_CODE,
            stdout,
            stderr,
            True,
        )
    except OSError as exc:
        return _CommandResult(127, "", str(exc), False)


def _run_subprocess(argv: list, timeout: float) -> tuple[int, str, str]:
    return _run_subprocess_result(argv, timeout).as_runner_result()


def _default_runner(argv: list) -> tuple[int, str, str]:  # pragma: no cover - real subprocess
    return _run_subprocess(argv, _DEFAULT_COMMAND_TIMEOUT_SECONDS)


def _has_http_status(stderr: str) -> bool:
    return _HTTP_STATUS_RE.search(stderr or "") is not None


def _is_manifest_not_found(stderr: str) -> bool:
    value = (stderr or "").lower()
    if _has_http_status(value):
        return False
    if any(marker in value for marker in _MANIFEST_ERROR_MARKERS_V1):
        return False
    return any(marker in value for marker in _MANIFEST_NOT_FOUND_MARKERS_V1)


def _is_skopeo_connectivity_error(stderr: str) -> bool:
    value = (stderr or "").lower()
    if _has_http_status(value):
        return False
    if any(marker in value for marker in _NO_FALLBACK_MARKERS_V1):
        return False
    return any(marker in value for marker in _CONNECTIVITY_MARKERS_V1)


def _registry_host(ref: str) -> str:
    return ref.split("/", 1)[0]


def _with_host(ref: str, host: str) -> str:
    _, separator, rest = ref.partition("/")
    return f"{host}/{rest}" if separator else host


def _inspect_digest(stdout: str) -> str | None:
    try:
        payload = json.loads(stdout or "{}")
    except (TypeError, json.JSONDecodeError):
        return None
    digest = payload.get("Digest") if isinstance(payload, dict) else None
    if isinstance(digest, str) and _DIGEST_RE.fullmatch(digest):
        return digest
    return None


def _pin_digest(ref: str, digest: str) -> str:
    name = ref.split("@", 1)[0]
    slash = name.rfind("/")
    colon = name.rfind(":")
    if colon > slash:
        name = name[:colon]
    return f"{name}@{digest}"


class AcrImageStore(BaseImageStore):
    def __init__(self, transport, *, runner: Runner | None = None,
                 prefer_public: bool = False) -> None:
        self._t = transport
        self._injected_runner = runner is not None
        self._run = runner or _default_runner
        # prefer_public：runner 不在 VPC 内网时置 True（对应 profile.prefer_public_registry）。
        # 连接优先公网 endpoint；凭据签名仍用 private canonical host（apiserver acr_profiles
        # 只登记 VPC host，GetAuthorizationToken 的 token 是实例级、对两个 endpoint 通用）。
        self._prefer_public = prefer_public

    def _deadline(self) -> float:
        return time.monotonic() + _DEFAULT_OPERATION_DEADLINE_SECONDS

    def _run_command(self, argv: list, deadline: float) -> _CommandResult:
        if self._injected_runner:
            # Injected runners retain their historical one-argument/three-tuple API.
            try:
                rc, stdout, stderr = self._run(argv)
            except OSError as exc:
                return _CommandResult(127, "", str(exc), False)
            return _CommandResult(rc, stdout, stderr, True)
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            return _CommandResult(
                _TIMEOUT_RETURN_CODE,
                "",
                "skopeo operation deadline exceeded before process start",
                False,
            )
        return _run_subprocess_result(
            argv,
            min(_DEFAULT_COMMAND_TIMEOUT_SECONDS, remaining),
        )

    def _route_refs(self, ref: str) -> tuple[str, tuple[str, ...]]:
        host = _registry_host(ref)
        route = _plan_acr_route(host)
        canonical = _with_host(ref, route.private_endpoint)
        if self._prefer_public and route.public_endpoint \
                and route.public_endpoint != route.private_endpoint:
            candidates = [_with_host(ref, route.public_endpoint), canonical]
        else:
            candidates = [canonical]
            if route.public_endpoint and route.public_endpoint != route.private_endpoint:
                candidates.append(_with_host(ref, route.public_endpoint))
        return canonical, tuple(candidates)

    def _net_ref(self, ref: str) -> str:
        """Return the stable canonical ref (private for standard ACR hosts)."""
        canonical, _ = self._route_refs(ref)
        return canonical

    def _authfile(self, *actual_refs: str, credentials: dict | None = None) -> str:
        """Write credentials keyed by the hosts skopeo will actually access."""
        credential_cache = credentials if credentials is not None else {}
        auths: dict[str, dict] = {}
        for actual_ref in actual_refs:
            actual_host = _registry_host(actual_ref)
            if actual_host in auths:
                continue
            canonical_ref, _ = self._route_refs(actual_ref)
            canonical_host = _registry_host(canonical_ref)
            cred = credential_cache.get(canonical_host)
            if cred is None:
                cred = self._t.get_acr_credentials(canonical_host)
                credential_cache[canonical_host] = cred
            pair = f"{cred['username']}:{cred['token']}".encode()
            auths[actual_host] = {"auth": base64.b64encode(pair).decode()}

        fd, path = tempfile.mkstemp(prefix="irepo_auth_", suffix=".json")
        try:
            with os.fdopen(fd, "w") as authfile:
                json.dump({"auths": auths}, authfile)
        except BaseException:
            self._cleanup(path)
            raise
        return path

    @staticmethod
    def _cleanup(authfile: str) -> None:
        with contextlib.suppress(OSError):
            os.unlink(authfile)

    def _inspect(self, ref: str, authfile: str, deadline: float) -> _InspectResult:
        command = self._run_command(
            ["skopeo", "inspect", "--authfile", authfile, f"docker://{ref}"],
            deadline,
        )
        if command.returncode == 0:
            return _InspectResult(
                _InspectState.PRESENT,
                _inspect_digest(command.stdout),
            )
        if _is_manifest_not_found(command.stderr):
            return _InspectResult(_InspectState.ABSENT, stderr=command.stderr)
        return _InspectResult(_InspectState.ERROR, stderr=command.stderr)

    @staticmethod
    def _inspect_error(ref: str, result: _InspectResult, authfile: str = "") -> TransportError:
        detail = result.stderr or "unknown skopeo inspect failure"
        if authfile:
            detail = detail.replace(authfile, "<authfile>")
        detail = detail[:300]
        return TransportError(f"skopeo inspect failed for {_registry_host(ref)}: {detail}")

    def _preflight(self, ref: str, credentials: dict, deadline: float) -> _SelectedRoute:
        canonical, candidates = self._route_refs(ref)
        private_failure: TransportError | None = None
        for index, candidate in enumerate(candidates):
            authfile = self._authfile(candidate, credentials=credentials)
            try:
                result = self._inspect(candidate, authfile, deadline)
            finally:
                self._cleanup(authfile)
            if result.state is not _InspectState.ERROR:
                return _SelectedRoute(canonical, candidate, result)

            error = self._inspect_error(candidate, result, authfile)
            if index == 0 and len(candidates) > 1 and _is_skopeo_connectivity_error(result.stderr):
                private_failure = error
                continue
            if private_failure is not None:
                error.__cause__ = private_failure
            raise error
        raise AssertionError("ACR route planner returned no candidates")

    @staticmethod
    def _copy_error(prefix: str, stderr: str, authfile: str) -> TransportError:
        detail = (stderr or "unknown skopeo copy failure").replace(authfile, "<authfile>")[:300]
        return TransportError(f"{prefix}: {detail}")

    def exists(self, ref: str, *, retries: int = 0, retry_delay: float = 1.5) -> bool:
        deadline = self._deadline()
        credentials: dict = {}
        selected = self._preflight(ref, credentials, deadline)
        if selected.inspect.state is _InspectState.PRESENT:
            return True

        for _ in range(retries):
            time.sleep(retry_delay)
            # Each consistency retry re-runs the full preflight so it keeps
            # routing through the one-time private→public connectivity fallback
            # (a bare private re-inspect would never recover from a transient
            # private outage). Hard inspect errors still raise (redacted).
            selected = self._preflight(ref, credentials, deadline)
            if selected.inspect.state is _InspectState.PRESENT:
                return True
        return False

    def push(self, tar_path: Path, ref: str, *, overwrite: bool) -> str:
        deadline = self._deadline()
        credentials: dict = {}
        destination = self._preflight(ref, credentials, deadline)
        if not overwrite and destination.inspect.state is _InspectState.PRESENT:
            return destination.canonical_ref

        authfile = self._authfile(destination.actual_ref, credentials=credentials)
        try:
            command = self._run_command(
                ["skopeo", "copy", "--dest-tls-verify=true",
                 "--authfile", authfile,
                 f"docker-archive:{tar_path}", f"docker://{destination.actual_ref}"],
                deadline,
            )
            if command.returncode != 0:
                cause = self._copy_error(
                    "skopeo copy failed",
                    command.stderr,
                    authfile,
                )
                if not command.started:
                    raise cause
                raise WriteOutcomeUnknown(
                    f"skopeo copy started; destination outcome is unknown for {destination.canonical_ref}",
                    cause=cause,
                )
        finally:
            self._cleanup(authfile)
        return destination.canonical_ref

    def copy(self, src_ref: str, dst_ref: str, *, overwrite: bool = False) -> str:
        deadline = self._deadline()
        credentials: dict = {}

        source = self._preflight(src_ref, credentials, deadline)
        if source.inspect.state is _InspectState.ABSENT:
            raise TransportError(f"source image manifest not found: {source.canonical_ref}")
        source_digest = source.inspect.digest
        if source_digest is None:
            raise TransportError(f"source inspect returned no immutable digest: {source.canonical_ref}")

        destination = self._preflight(dst_ref, credentials, deadline)
        if not overwrite and destination.inspect.state is _InspectState.PRESENT:
            return destination.canonical_ref

        pinned_source = _pin_digest(source.actual_ref, source_digest)
        authfile = self._authfile(pinned_source, destination.actual_ref, credentials=credentials)
        try:
            command = self._run_command(
                ["skopeo", "copy", "--src-tls-verify=true", "--dest-tls-verify=true",
                 "--authfile", authfile,
                 f"docker://{pinned_source}", f"docker://{destination.actual_ref}"],
                deadline,
            )
            if command.returncode == 0:
                return destination.canonical_ref

            cause = self._copy_error(
                "skopeo copy(reg→reg) failed",
                command.stderr,
                authfile,
            )
            if not command.started:
                raise cause
            # Reconcile only against the already-selected destination route. Never
            # switch hosts or issue a second copy after a write may have started.
            reconciled = self._inspect(destination.actual_ref, authfile, deadline)
            if (reconciled.state is _InspectState.PRESENT
                    and reconciled.digest == source_digest):
                return destination.canonical_ref
            raise WriteOutcomeUnknown(
                f"skopeo copy started; destination outcome is unknown for {destination.canonical_ref}",
                cause=cause,
            )
        finally:
            self._cleanup(authfile)

    def pull(self, ref: str, tar_path: Path, *, overwrite: bool = False) -> str:
        """把远端镜像拉到本地 docker-archive tar；返回实际拉取的 digest 固定引用。

        与 OSS 下载同口径：``pull`` 是**下载动作，默认强制私网**——只用私网候选，不做公网回退。
        私网端点无法确认为标准 ACR 私网地址（自定义 registry），或私网连通性失败时，抛
        ``PrivateNetworkRequired``，绝不静默走公网。

        例外：构造时 ``prefer_public=True``（IR_ACR_PREFER_PUBLIC=1，runner 不在 VPC 内网）
        时改走**公网 endpoint**（仍经标准 ACR 确认；凭据仍用 VPC host 签，token 实例级通用）。

        源引用先经 inspect 取得不可变 digest 并以 digest 固定后再拉，避免 tag 在
        inspect 与 copy 之间被覆盖、导致拉到非预期镜像。
        """
        deadline = self._deadline()
        credentials: dict = {}
        route = _plan_acr_route(_registry_host(ref))
        if not route.standard:
            raise PrivateNetworkRequired(
                "download requires private data-plane access; registry "
                f"{_registry_host(ref)} cannot be confirmed as a standard "
                "private ACR endpoint; public fallback is disabled")
        if self._prefer_public:
            data_ref = _with_host(ref, route.public_endpoint)
        else:
            data_ref = _with_host(ref, route.private_endpoint)

        authfile = self._authfile(data_ref, credentials=credentials)
        try:
            inspected = self._inspect(data_ref, authfile, deadline)
        finally:
            self._cleanup(authfile)
        if inspected.state is _InspectState.ERROR:
            error = self._inspect_error(data_ref, inspected, authfile)
            if _is_skopeo_connectivity_error(inspected.stderr):
                raise PrivateNetworkRequired(
                    "download data-plane access failed; registry "
                    f"{_registry_host(data_ref)} is unreachable; "
                    "public fallback is disabled", cause=error)
            raise error
        if inspected.state is _InspectState.ABSENT:
            raise TransportError(f"source image manifest not found: {data_ref}")
        if inspected.digest is None:
            raise TransportError(
                f"source inspect returned no immutable digest: {data_ref}")

        target = Path(tar_path)
        if target.exists() and not overwrite:
            raise TransportError(
                f"{target} already exists; pass overwrite=True to replace it")
        if target.parent and not target.parent.exists():
            target.parent.mkdir(parents=True, exist_ok=True)

        pinned = _pin_digest(data_ref, inspected.digest)
        authfile = self._authfile(pinned, credentials=credentials)
        try:
            command = self._run_command(
                ["skopeo", "copy", "--src-tls-verify=true",
                 "--authfile", authfile,
                 f"docker://{pinned}", f"docker-archive:{target}"],
                deadline,
            )
            if command.returncode != 0:
                cause = self._copy_error(
                    "skopeo copy(reg→archive) failed", command.stderr, authfile)
                if _is_skopeo_connectivity_error(command.stderr):
                    raise PrivateNetworkRequired(
                        "download data-plane access failed; registry "
                        f"{_registry_host(data_ref)} is unreachable; "
                        "public fallback is disabled", cause=cause)
                raise cause
        finally:
            self._cleanup(authfile)
        return pinned
