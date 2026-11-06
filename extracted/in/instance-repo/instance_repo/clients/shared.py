"""Shared release client using the actual AP wire and verified byte channels.

ap-tool supports only the registered tf-rewardkit / rewardkit pyz artifact on
linux-x86_64. Generic ap-share-data keeps its existing manifest/digest shape.
Trusted replica policy and (for generic downloads) explicit library root bind
signed URLs; neither endpoint responses nor caller filenames bootstrap trust.
Numeric94040..94050 classify safe shared errors; raw messages, URLs and fencing
values are never copied into errors or grant repr. No cloud calls occur on import.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import queue
import re
import socket
import threading
import time
from collections import OrderedDict
from dataclasses import dataclass, field
from pathlib import Path
from types import MappingProxyType
from urllib.parse import urlencode

from ..errors import BizCodeError, RequestDeadlineExceeded, SchemaError, TransportError
from .ap_tool import tool_object_key
from .user_data_writes import _Budget, _call_with_budget, _resolve_replica_policy
from .user_data_reads import _default_http_get, _parse_utc

#: shared 契约错误码（fixture error_codes；v2 数字码 94040+ 到位后扩表）。
SHARED_ERROR_CODES = (
    "shared_unauthorized",
    "shared_manifest_conflict",
    "shared_upload_lease_expired",
    "shared_stale_fencing_token",
    "shared_manifest_frozen",
    "shared_already_committed",
    "shared_not_ready",
    "shared_digest_mismatch",
    "shared_invalid_region",
    "shared_invalid_release_subject",
    "shared_upload_forbidden",
)

#: 正式双 region（固定 {cn, sg}；CanonicalizeRegions 乱序归一）。
SHARED_REGIONS = ("cn", "sg")

#: SHA256 规范：64 位小写十六进制。
_SHA256_LEN = 64
_SHA256_HEX = set("0123456789abcdef")

#: 路径规范：干净相对路径（上限 512 字节）。
_MAX_PATH_BYTES = 512

#: 流式 IO 常量（Codex r4 返修）：分块大小与单对象传输上限。
#: 分块读文件直写请求体，不整读入内存；超过上限拒绝（无界防护）。
_CHUNK_BYTES = 1024 * 1024                     # 1 MiB
MAX_TRANSFER_BYTES = 8 * 1024 * 1024 * 1024    # 8 GiB 单对象上限

#: 预签名 PUT 响应体（错误报文等）有界读取上限：读满即截断，防异常服务端
#: 无界响应拖垮客户端内存。
_MAX_RESP_BYTES = 1024 * 1024                  # 1 MiB


class SharedError(BizCodeError):
    """shared 域错误：``code`` 为字符串 error_code（fixture 词表）。

    Numeric shared biz_code and HTTP status are preserved. Error mapping
    discards remote messages/data, including contradictory symbolic codes.
    """

    code = "E_SHARED"

    def __init__(self, message: str = "", *, status: int | None = None,
                 error_code: str = "", data: dict | None = None,
                 biz_code: int | None = None) -> None:
        super().__init__(message, status=status, biz_code=biz_code, data=data)
        self.error_code = error_code or getattr(type(self), "error_code", "shared_unauthorized")


# error_code → 异常子类（懒构造，模块级注册）
class SharedUnauthorized(SharedError):
    code = "E_SHARED_UNAUTHORIZED"
    error_code = "shared_unauthorized"


class SharedManifestConflict(SharedError):
    code = "E_SHARED_MANIFEST_CONFLICT"
    error_code = "shared_manifest_conflict"


class SharedUploadLeaseExpired(SharedError):
    code = "E_SHARED_UPLOAD_LEASE_EXPIRED"
    error_code = "shared_upload_lease_expired"


class SharedStaleFencingToken(SharedError):
    code = "E_SHARED_STALE_FENCING_TOKEN"
    error_code = "shared_stale_fencing_token"


class SharedManifestFrozen(SharedError):
    code = "E_SHARED_MANIFEST_FROZEN"
    error_code = "shared_manifest_frozen"


class SharedAlreadyCommitted(SharedError):
    code = "E_SHARED_ALREADY_COMMITTED"
    error_code = "shared_already_committed"


class SharedNotReady(SharedError):
    code = "E_SHARED_NOT_READY"
    error_code = "shared_not_ready"


class SharedDigestMismatch(SharedError):
    code = "E_SHARED_DIGEST_MISMATCH"
    error_code = "shared_digest_mismatch"


class SharedInvalidRegion(SharedError):
    code = "E_SHARED_INVALID_REGION"
    error_code = "shared_invalid_region"


class SharedInvalidReleaseSubject(SharedError):
    code = "E_SHARED_INVALID_RELEASE_SUBJECT"
    error_code = "shared_invalid_release_subject"


class SharedUploadForbidden(SharedError):
    code = "E_SHARED_UPLOAD_FORBIDDEN"
    error_code = "shared_upload_forbidden"


ERROR_CODE_TO_EXC: dict[str, type[SharedError]] = {e.error_code: e for e in (
    SharedUnauthorized, SharedManifestConflict, SharedUploadLeaseExpired,
    SharedStaleFencingToken, SharedManifestFrozen, SharedAlreadyCommitted,
    SharedNotReady, SharedDigestMismatch, SharedInvalidRegion,
    SharedInvalidReleaseSubject, SharedUploadForbidden,
)}


def validate_shared_sha256(value: str) -> str:
    """校验 manifest sha256：恰好 64 位小写十六进制（fixture 规范）。"""
    v = value if isinstance(value, str) else ""
    if len(v) != _SHA256_LEN or not set(v) <= _SHA256_HEX:
        from ..errors import SchemaError
        raise SchemaError("shared manifest sha256 must be64lowercasehex")
    return v


def _utf8_size(value: str) -> int:
    """Reject malformed text without exporting UnicodeError.object."""
    encoded = None
    try:
        encoded = value.encode("utf-8")
    except UnicodeError:
        pass
    if encoded is None:
        raise SchemaError("shared text must be valid UTF-8")
    return len(encoded)


def validate_shared_path(path: str) -> str:
    """校验共享路径：干净相对路径（拒绝对/父/点段/空段/反斜杠/空白/控制符，≤512B）。"""
    from ..errors import SchemaError
    p = path if isinstance(path, str) else ""
    if not p:
        raise SchemaError("shared path must not be empty")
    if _utf8_size(p) > _MAX_PATH_BYTES:
        raise SchemaError(f"shared path exceeds {_MAX_PATH_BYTES} bytes")
    if p.startswith("/") or "\\" in p or any(ord(c) < 0x20 for c in p):
        raise SchemaError("invalid shared path")
    if any(c.isspace() for c in p):
        raise SchemaError("invalid shared path: whitespace not allowed")
    segs = p.split("/")
    if any(seg in ("", ".", "..") for seg in segs):
        raise SchemaError("invalid shared path: empty/dot/parent segment")
    if any(_utf8_size(segment) > 128 for segment in segs[:-1]):
        raise SchemaError("shared path component exceeds 128 bytes")
    return p


def canonicalize_regions(regions) -> list[str]:
    """region 集合归一化：必须恰好 {cn, sg}（乱序归一 [cn, sg]；单/重复/未知拒绝）。"""
    from ..errors import SchemaError
    rs = [str(r).strip() for r in (regions or [])]
    if not rs:
        rs = list(SHARED_REGIONS)
    if sorted(set(rs)) != ["cn", "sg"] or len(rs) != 2:
        raise SchemaError(
            f"invalid shared regions {regions!r}: must be exactly cn+sg")
    return ["cn", "sg"]


def canonical_manifest_digest(files) -> str:
    """canonical digest：按 path 排序 + 固定字段顺序 (path,size,sha256) 的
    JSON 数组做 SHA-256。FileID 不进摘要（服务器分配）。

    Go 参考实现 model.CanonicalManifestDigest 逐字节复现同值（fixture
    digest_vectors 三语言回归锚定）。
    """
    entries = []
    seen_paths = set()
    for f in files or []:
        path = validate_shared_path(f["path"])
        if path in seen_paths:
            from ..errors import SchemaError
            raise SchemaError(f"duplicate shared path {path!r}")
        seen_paths.add(path)
        size = f["size"]
        if not isinstance(size, int) or isinstance(size, bool) or size <= 0:
            from ..errors import SchemaError
            raise SchemaError(f"invalid shared file size {size!r} for {path!r}")
        entries.append({"path": path, "size": size,
                        "sha256": validate_shared_sha256(f["sha256"])})
    if not entries:
        from ..errors import SchemaError
        raise SchemaError("shared manifest must contain at least one file")
    entries.sort(key=lambda e: e["path"])
    # 固定 JSON 序列化：与 Go/Java 一致（紧凑分隔符、保持插入序）。
    canonical = json.dumps(entries, separators=(",", ":"), ensure_ascii=False)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


# Numeric protocol codes are authoritative over untrusted symbolic payloads.
_NUMERIC_SHARED_ERRORS = dict(zip(range(94040, 94051), SHARED_ERROR_CODES))
_SAFE_ID = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,127}")
_SHARED_IO_WORKERS = threading.BoundedSemaphore(4)


class SharedTransferError(TransportError):
    """Secret-safe byte IO failure; only explicit known network shapes retry."""
    def __init__(self, *, status=None, retryable=False):
        super().__init__("shared byte transfer failure", status=status, data={})
        self.retryable = bool(retryable)


class _SharedBudget(_Budget):
    def __init__(self, duration):
        if duration is not None and (isinstance(duration, bool)
                or not isinstance(duration, (int, float))
                or not math.isfinite(duration) or duration < 0):
            raise SchemaError("shared deadline must be finite nonnegative seconds or None")
        super().__init__(duration)

    def raise_if_exhausted(self):
        if self.exhausted:
            raise RequestDeadlineExceeded("shared operation deadline exhausted")


@dataclass(frozen=True)
class _FileBinding:
    release_id: str
    file_id: str
    key: str
    size: int
    sha256: str
    region: str
    expires_monotonic: float
    url: str = field(repr=False)
    generation: int = 0
    max_bytes: int = MAX_TRANSFER_BYTES
    space: str = ""
    cluster: str = ""


class _SafeResponse(dict):
    """Actual control response shape with a secret-safe default repr."""
    def __repr__(self):
        return "SharedControlResponse(<redacted>)"

    __str__ = __repr__


class _BoundGrant(dict):
    """Dict-compatible actual server wire with private immutable local binding.

    The binding is never serialized as a wire field or an authorization claim.
    Actual shared authorization remains fresh server-side on every endpoint.
    """
    def __init__(self, wire, binding, client):
        super().__init__(wire)
        self._original = MappingProxyType(dict(wire))
        self._binding = binding
        self._client = client

    def __repr__(self):
        return "SharedSignedGrant(<redacted>)"

    __str__ = __repr__


def _expiry(value):
    if not isinstance(value, str) or not re.fullmatch(
            r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})", value):
        raise SchemaError("shared expiry must be RFC3339 with explicit timezone")
    return _parse_utc(value)


def _identity(value, what):
    if (not isinstance(value, str) or not value or value != value.strip()
            or _utf8_size(value) > 128
            or any(c.isspace() or ord(c) < 32 or c in "/\\%?#" for c in value)
            or value in (".", "..")):
        raise SchemaError(f"invalid shared {what}")
    return value


def _token(value):
    if not isinstance(value, str) or not value or _utf8_size(value) > 4096:
        raise SchemaError("shared fencing token must be a nonempty bounded opaque string")
    return value


def _safe_id(value, what):
    if not isinstance(value, str) or not _SAFE_ID.fullmatch(value):
        raise SchemaError(f"invalid shared {what}")
    return value


def _size(value):
    if type(value) is not int or not 0 < value <= MAX_TRANSFER_BYTES:
        raise SchemaError("shared size must be a positive bounded integer")
    return value


def _tool_manifest(space, name, version, files):
    if space == "ap-tool":
        expected = tool_object_key(name, version)
        if len(files) != 1 or files[0]["path"] != expected:
            raise SchemaError("ap-tool manifest path does not match registered name/version/artifact")


def _signed_url(url, key, policy, *, expected_region=None):
    """Match one exact bucket/endpoint/key tuple, never independent sets."""
    from urllib.parse import unquote, urlsplit
    if policy is None:
        raise SchemaError("shared byte channel requires trusted expected_replica_policy")
    parsed = None
    try:
        parsed = urlsplit(url)
        port = parsed.port if parsed.port is not None else 443
    except (TypeError, ValueError):
        parsed = None
    if parsed is None:
        raise SchemaError("invalid shared signed URL")
    if (parsed.scheme != "https" or not parsed.hostname or parsed.username is not None
            or parsed.password is not None or parsed.fragment or port != 443
            or any(ord(c) <= 32 for c in url)
            or re.search(r"%(?![0-9a-fA-F]{2})", parsed.path)):
        raise SchemaError("invalid shared signed URL structure")
    path = None
    try:
        path = unquote(parsed.path, errors="strict")
    except UnicodeError:
        pass
    if path is None:
        raise SchemaError("invalid shared URL path encoding")
    regions = (expected_region,) if expected_region is not None else SHARED_REGIONS
    for region in regions:
        if region not in SHARED_REGIONS:
            raise SchemaError("invalid shared region")
        bucket, oss_region = policy.bucket(region), policy.oss_region(region)
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,61}[a-z0-9]", bucket):
            raise SchemaError("invalid trusted shared bucket")
        for endpoint in (f"oss-{oss_region}.aliyuncs.com", f"oss-{oss_region}-internal.aliyuncs.com"):
            if (parsed.hostname.lower() == f"{bucket}.{endpoint}" and path == "/" + key
                    or parsed.hostname.lower() == endpoint and path == "/" + bucket + "/" + key):
                return region
    raise SchemaError("shared URL does not bind trusted region/bucket/exact object key")


def _validate_upload_route_options(cluster, expected_region):
    if (not isinstance(cluster, str)
            or any(c.isspace() or ord(c) < 32 for c in cluster)):
        raise SchemaError("shared cluster must be an exact string without whitespace")
    if expected_region is not None and expected_region not in SHARED_REGIONS:
        raise SchemaError("shared expected_region must be cn or sg")


def _upload_route(space, cluster, expected_region):
    _validate_upload_route_options(cluster, expected_region)
    if space not in ('ap-tool', 'ap-share-data'):
        raise SchemaError("unsupported shared upload space")
    if space == 'ap-tool' or cluster:
        if not cluster:
            raise SchemaError("ap-tool upload requires explicit cluster")
        if expected_region is None:
            raise SchemaError("explicit shared cluster requires trusted expected_region")
        return cluster, expected_region
    # Only the approved old generic omitted-cluster path has a fixed default.
    if expected_region not in (None, 'cn'):
        raise SchemaError("omitted generic cluster requires legacy cn region")
    return '', 'cn'


class SharedReleaseClient:
    """Actual shared release wire, registered ap-tool binding and verified IO.

    Optional trusted policy is mandatory for byte/URL channels. Existing generic
    control methods remain usable without it. A generic ap-share-data download
    also needs explicit shared_library_id. Call lookup before download_file to
    bind reader identity without touching publisher-only Status.
    """
    _BASE = '/apis/v1/shared/releases'

    def __init__(self, transport, *, expected_replica_policy=None, shared_library_id=None):
        self._t = transport
        self._policy = _resolve_replica_policy(expected_replica_policy)
        self._library = None
        if shared_library_id is not None:
            self._library = validate_shared_path(shared_library_id)
        self._identities = OrderedDict()
        self._identity_lock = threading.RLock()

    def _request(self, method, path, body=None, *, budget):
        failure = None
        try:
            response = _call_with_budget(budget, self._t, method, path, body)
        except RequestDeadlineExceeded:
            failure = RequestDeadlineExceeded('shared operation deadline exhausted')
        except TransportError as exc:
            failure = map_shared_error(exc)
        if failure is not None:
            raise failure
        return _SafeResponse(response) if isinstance(response, dict) else response

    def _remember(self, response, *, expected=None, expected_digest=None):
        if not isinstance(response, dict):
            raise SchemaError('shared release response must be an object')
        fields = ('release_id', 'space', 'name', 'version')
        if expected_digest is not None:
            # create() already knows the exact submitted identity and manifest.
            # Old control projections may omit echoes, but cannot replace this
            # caller anchor with their first response. Keep it only locally;
            # never manufacture missing wire fields in the returned response.
            digest = validate_shared_sha256(expected_digest)
            if any(k in response and response[k] != value
                   for k, value in zip(fields[1:], expected)):
                raise SchemaError('shared release identity echo mismatch')
            if 'manifest_digest' in response and validate_shared_sha256(response['manifest_digest']) != digest:
                raise SchemaError('shared create manifest digest mismatch')
            if 'release_id' not in response:
                return
            release_id = _safe_id(response['release_id'], 'release_id')
            identity = expected
        else:
            if not all((k in response for k in fields)):
                return
            release_id = _safe_id(response['release_id'], 'release_id')
            identity = tuple((_identity(response[k], k) for k in fields[1:]))
            if expected is not None and identity != expected:
                raise SchemaError('shared release identity echo mismatch')
            digest = response.get('manifest_digest', '')
            if digest:
                validate_shared_sha256(digest)
        with self._identity_lock:
            previous = self._identities.get(release_id)
            if previous is not None:
                if previous[:3] != identity:
                    raise SchemaError('shared release identity changed for bound release ID')
                if previous[3] and digest and previous[3] != digest:
                    raise SchemaError('shared frozen manifest digest changed for bound release ID')
                # Older controls may omit the digest. Never erase a known
                # immutable binding; an initially empty digest may be learned.
                digest = digest or previous[3]
            self._identities[release_id] = (*identity, digest)
            self._identities.move_to_end(release_id)
            while len(self._identities) > 64:
                self._identities.popitem(last=False)

    def create(self, space, name, version, files, regions=None, *, deadline=None):
        canonicalize_regions(regions)
        identity = tuple((_identity(v, k) for v, k in ((space, 'space'), (name, 'name'), (version, 'version'))))
        manifest = self._build_manifest(files)
        _tool_manifest(*identity, manifest)
        expected_digest = canonical_manifest_digest(manifest)
        budget = _SharedBudget(deadline)
        result = self._request('POST', self._BASE, dict(zip(('space', 'name', 'version'), identity), files=manifest), budget=budget)
        if not isinstance(result, dict):
            raise SchemaError('shared create response must be an object')
        returned_manifest = result.get('manifest')
        if 'manifest' in result:
            if not isinstance(returned_manifest, dict) or 'files' not in returned_manifest:
                raise SchemaError('shared create manifest must contain files')
            if self._build_manifest(returned_manifest['files']) != manifest:
                raise SchemaError('shared create manifest differs from request')
            if 'digest' in returned_manifest:
                nested_digest = returned_manifest['digest']
                # Go exposes the unfrozen manifest's empty digest while the
                # submitted manifest is already anchored at the release level.
                unfrozen = (type(nested_digest) is str and nested_digest == ''
                    and result.get('status') == 'uploading'
                    and 'manifest_digest' in result
                    and validate_shared_sha256(result['manifest_digest']) == expected_digest)
                if not unfrozen and validate_shared_sha256(nested_digest) != expected_digest:
                    raise SchemaError('shared create nested manifest digest mismatch')
        if 'files' in result and self._build_manifest(result['files']) != manifest:
            raise SchemaError('shared create manifest differs from request')
        self._remember(result, expected=identity, expected_digest=expected_digest)
        return result

    def status(self, release_id, *, deadline=None):
        release_id = _safe_id(release_id, 'release_id')
        response = self._request('GET', f'{self._BASE}/{release_id}', budget=_SharedBudget(deadline))
        if not isinstance(response, dict) or response.get('release_id', release_id) != release_id:
            raise SchemaError('shared release ID mismatch')
        self._remember(response)
        return response

    def commit(self, release_id, generation=None, fencing_token='', files=None, *, deadline=None):
        release_id = _safe_id(release_id, 'release_id')
        if type(generation) is not int or generation <= 0:
            raise SchemaError('commit requires positive upload_lease.generation')
        if files is not None:
            self._build_manifest(files)
        return self._request('POST', f'{self._BASE}/{release_id}/commit', {'generation': generation, 'fencing_token': _token(fencing_token)}, budget=_SharedBudget(deadline))

    def retry(self, release_id, manifest_digest='', *, deadline=None):
        release_id = _safe_id(release_id, 'release_id')
        body = {}
        if manifest_digest:
            body['manifest_digest'] = validate_shared_sha256(manifest_digest)
        return self._request('POST', f'{self._BASE}/{release_id}/retry', body, budget=_SharedBudget(deadline))

    def lookup(self, space, name, version, *, deadline=None):
        identity = tuple((_identity(v, k) for v, k in ((space, 'space'), (name, 'name'), (version, 'version'))))
        query = urlencode(dict(zip(('space', 'name', 'version'), identity)))
        response = self._request('GET', '/apis/v1/shared/consume/lookup?' + query, budget=_SharedBudget(deadline))
        if not isinstance(response, dict):
            raise SchemaError('shared lookup response must be an object')
        if all((k in response for k in ('release_id', 'space', 'name', 'version'))):
            if response.get('status') != 'ready':
                raise SharedNotReady('shared lookup is not ready', biz_code=94046)
            validate_shared_sha256(response.get('manifest_digest'))
        self._remember(response, expected=identity)
        return response

    def files(self, release_id, *, deadline=None):
        response = self._request('GET', f"{self._BASE}/{_safe_id(release_id, 'release_id')}/files", budget=_SharedBudget(deadline))
        if not isinstance(response, dict):
            raise SchemaError('shared files response must be an object')
        return response.get('files') or []

    def files_projection(self, release_id, *, deadline=None):
        """Fresh reader projection, including frozen digest and ready_at.

        Existing files() keeps its list return type. Consumers that display or
        bind the full projection use this method, without publisher-only Status.
        """
        release_id = _safe_id(release_id, 'release_id')
        response = self._request('GET', f'{self._BASE}/{release_id}/files',
                                 budget=_SharedBudget(deadline))
        if not isinstance(response, dict) or not isinstance(response.get('files'), list):
            raise SchemaError('shared files projection must contain file array')
        manifest = self._build_manifest(response['files'])
        identifiers = [_safe_id(record.get('file_id'), 'file_id') for record in response['files']]
        if len(set(identifiers)) != len(identifiers):
            raise SchemaError('duplicate shared file_id')
        digest = validate_shared_sha256(response.get('manifest_digest'))
        if canonical_manifest_digest(manifest) != digest:
            raise SchemaError('shared files projection digest mismatch')
        with self._identity_lock:
            identity = self._identities.get(release_id)
        if identity is not None:
            _tool_manifest(*identity[:3], manifest)
            if identity[3] != digest:
                raise SchemaError('shared frozen manifest changed since lookup')
        return response

    def list(self, *, space='', name='', page_size=50, max_items=None, deadline=None):
        if type(page_size) is not int or page_size < 1:
            raise SchemaError('shared page_size must be a positive integer')
        if max_items is not None and (type(max_items) is not int or max_items < 1):
            raise SchemaError('shared max_items must be positive')
        page_size = min(page_size, 200)
        budget = _SharedBudget(deadline)
        output = []
        for page in range(1, 1001):
            budget.raise_if_exhausted()
            query = {'page_size': page_size}
            if page > 1:
                query['page'] = page
            if space:
                query['space'] = _identity(space, 'space')
            if name:
                query['name'] = _identity(name, 'name')
            import inspect
            fn = self._t.request_with_meta
            kwargs = {'timeout': budget.remaining_seconds()} if 'timeout' in inspect.signature(fn).parameters else {}
            failure = None
            try:
                path = '/apis/v1/shared/consume/releases?' + urlencode(query)
                from ..transport import Transport
                if budget.deadline() is not None and isinstance(self._t, Transport):
                    from ..retry import retry_transient

                    def attempt():
                        budget.raise_if_exhausted()
                        return self._t._request_once_with_meta('GET', path, timeout=budget.remaining_seconds(), deadline_monotonic=budget.deadline())
                    data, pagination = retry_transient(attempt, attempts=self._t._retry_attempts, deadline_monotonic=budget.deadline())
                else:
                    data, pagination = fn('GET', path, **kwargs)
            except RequestDeadlineExceeded:
                failure = RequestDeadlineExceeded('shared operation deadline exhausted')
            except TransportError as exc:
                failure = map_shared_error(exc)
            if failure is not None:
                raise failure
            budget.raise_if_exhausted()
            if not isinstance(data, list) or not all((isinstance(x, dict) for x in data)):
                raise SchemaError('shared list response must be an array of objects')
            if isinstance(pagination, dict) and pagination.get('page', page) != page:
                raise SchemaError('shared pagination echo mismatch')
            output.extend(data)
            if not data:
                return output
            if max_items is not None and len(output) >= max_items:
                return output[:max_items]
            total = pagination.get('total') if isinstance(pagination, dict) else None
            if type(total) is int and len(output) >= total:
                return output
        raise SchemaError('shared list page bound reached; refine filters')

    def _require_policy(self):
        if self._policy is None:
            raise SchemaError('shared byte channel requires expected_replica_policy')

    def _file(self, release_id, file_id, *, upload, budget):
        self._require_policy()
        release_id, file_id = (_safe_id(release_id, 'release_id'), _safe_id(file_id, 'file_id'))
        if upload:
            response = self._request('GET', f'{self._BASE}/{release_id}', budget=budget)
            if not isinstance(response, dict) or response.get('release_id') != release_id:
                raise SchemaError('shared status identity mismatch')
            if not all(k in response for k in ('space', 'name', 'version')):
                raise SchemaError('shared status lacks identity fields')
            self._remember(response)
            with self._identity_lock:
                identity = self._identities.get(release_id)
            if identity is None:
                raise SchemaError('shared upload metadata binding unavailable')
            files = self._files_of(response)
        else:
            with self._identity_lock:
                identity = self._identities.get(release_id)
            if identity is None:
                raise SchemaError('shared download requires prior lookup on this client')
            response = self._request('GET', f'{self._BASE}/{release_id}/files', budget=budget)
            if not isinstance(response, dict):
                raise SchemaError('invalid shared files response')
            files = response.get('files')
        if not isinstance(files, list):
            raise SchemaError('shared manifest files are missing')
        manifest = self._build_manifest(files)
        file_ids = [_safe_id(record.get('file_id'), 'file_id') for record in files]
        if len(set(file_ids)) != len(file_ids):
            raise SchemaError('duplicate shared file_id')
        _tool_manifest(*identity[:3], manifest)
        digest = canonical_manifest_digest(manifest)
        if not identity[3] or digest != identity[3]:
            raise SchemaError('shared frozen manifest digest mismatch')
        if not upload and response.get('manifest_digest') != identity[3]:
            raise SchemaError('shared frozen manifest digest mismatch')
        matches = [f for f in files if isinstance(f, dict) and f.get('file_id') == file_id]
        if len(matches) != 1:
            raise SchemaError('shared file_id not in manifest')
        target = matches[0]
        size, sha = (_size(target.get('size')), validate_shared_sha256(target.get('sha256')))
        if upload:
            lease = self._lease_of(response)
            if not lease or type(lease.get('generation')) is not int or lease.get('generation', 0) <= 0:
                raise SharedUploadLeaseExpired('shared upload lease unavailable', biz_code=94042)
            if response.get('status') != 'uploading':
                raise SharedNotReady('shared release not uploading', biz_code=94046)
        else:
            lease = None
        return (identity, target, size, sha, lease)

    def upload_credentials(self, release_id, *, generation, fencing_token, file_id,
                           cluster='', expected_region=None, deadline=None):
        _validate_upload_route_options(cluster, expected_region)
        release_id = _safe_id(release_id, 'release_id')
        with self._identity_lock:
            known = self._identities.get(release_id)
        if known is not None:
            _upload_route(known[0], cluster, expected_region)
        budget = _SharedBudget(deadline)
        identity, target, size, sha, lease = self._file(release_id, file_id, upload=True, budget=budget)
        cluster, expected_region = _upload_route(identity[0], cluster, expected_region)
        if type(generation) is not int or generation <= 0 or type(lease.get('generation')) is not int or (lease.get('generation') != generation) or (not isinstance(fencing_token, str)) or (not fencing_token) or (lease.get('fencing_token') != fencing_token):
            raise SharedStaleFencingToken('shared upload lease binding mismatch', biz_code=94043)
        lease_expiry = None
        try:
            if not isinstance(lease.get('expires_at'), str):
                raise SchemaError('shared upload lease expiry must be RFC3339 string')
            lease_expiry = _expiry(lease['expires_at'])
        except (KeyError, TypeError, ValueError):
            pass
        if lease_expiry is None:
            raise SchemaError('shared upload lease expiry missing or invalid')
        if lease_expiry <= time.time():
            raise SharedUploadLeaseExpired('shared upload lease expired', biz_code=94042)
        body = {'generation': generation, 'fencing_token': fencing_token, 'file_id': file_id}
        if cluster:
            body['cluster'] = cluster
        response = self._request('POST', f'{self._BASE}/{release_id}/upload-credentials', body, budget=budget)
        if not isinstance(response, dict) or response.get('file_id') != file_id or type(response.get('generation')) is not int or (response.get('generation') != generation) or (response.get('method') != 'PUT') or (response.get('expected_sha256') != sha):
            raise SchemaError('shared upload credential binding mismatch')
        if not isinstance(response.get('expires_at'), str):
            raise SchemaError('shared upload expiry must be RFC3339 string')
        expires = _expiry(response['expires_at'])
        ttl = expires - time.time()
        if not 0 < ttl <= 600 or expires > lease_expiry:
            raise SchemaError('shared upload grant expiry invalid')
        maximum = response.get('max_bytes')
        if type(maximum) is not int or maximum <= 0:
            raise SchemaError('shared upload max_bytes must be positive integer')
        maximum = min(maximum, MAX_TRANSFER_BYTES)
        if size > maximum:
            raise SchemaError('shared upload exceeds credential max_bytes')
        key = f'staging/{release_id}/{generation}/{file_id}/{sha}'
        region = _signed_url(response.get('url'), key, self._policy, expected_region=expected_region)
        if 'region' in response and response['region'] != region:
            raise SchemaError('shared upload region echo mismatch')
        binding = _FileBinding(release_id, file_id, key, size, sha, region, time.monotonic() + ttl, response['url'], generation, maximum, identity[0], cluster)
        return _BoundGrant(response, binding, self)

    def _grant(self, grant, release_id):
        if not isinstance(grant, _BoundGrant) or grant._client is not self or dict(grant) != dict(grant._original) or (grant._binding.release_id != release_id):
            raise SchemaError('shared byte channel requires unchanged server-bound grant')
        if time.monotonic() >= grant._binding.expires_monotonic:
            if grant._binding.generation > 0:
                raise SharedUploadLeaseExpired('shared signed upload grant expired', biz_code=94042)
            raise SchemaError('shared signed download URL expired; resolve again')
        return grant._binding

    def upload_file(self, release_id, upload, local_path, *, cluster='',
                    expected_region=None, deadline=None):
        _validate_upload_route_options(cluster, expected_region)
        budget = _SharedBudget(deadline)
        budget.raise_if_exhausted()
        binding = self._grant(upload, _safe_id(release_id, 'release_id'))
        cluster, expected_region = _upload_route(binding.space, cluster, expected_region)
        if cluster != binding.cluster or expected_region != binding.region:
            raise SchemaError('shared upload route differs from frozen grant')
        _signed_url(binding.url, binding.key, self._policy, expected_region=binding.region)
        size = os.stat(local_path).st_size
        if size != binding.size:
            raise SchemaError('shared upload size mismatch')
        if size > MAX_TRANSFER_BYTES:
            raise SchemaError('shared upload exceeds MAX_TRANSFER_BYTES')
        remaining = binding.expires_monotonic - time.monotonic()
        if budget.deadline() is None or binding.expires_monotonic < budget.deadline():
            budget = _SharedBudget(remaining)
        status, _ = self._put_streaming(binding.url, {}, str(local_path), size, budget=budget, expected_sha256=binding.sha256)
        budget.raise_if_exhausted()
        if not 200 <= status < 300:
            raise TransportError('shared upload HTTP failure', status=status)
        return {'ok': True, 'path': binding.key, 'file_id': binding.file_id, 'region': binding.region, 'generation': binding.generation, 'bytes_written': size, 'sha256': binding.sha256}

    def download_urls(self, release_id, *, file_id='', region='', deadline=None):
        return self._download_grant(release_id, file_id, region, _SharedBudget(deadline))

    def _download_grant(self, release_id, file_id, region, budget):
        if region not in ('', *SHARED_REGIONS):
            raise SchemaError('invalid shared region')
        identity, target, size, sha, _ = self._file(release_id, file_id, upload=False, budget=budget)
        space, name, version, _ = identity
        if space == 'ap-tool':
            key = tool_object_key(name, version)
        else:
            if self._library is None:
                raise SchemaError('generic shared download requires trusted shared_library_id')
            key = f'{self._library}/{space}/{name}/{version}/{file_id}/{sha}'
        query = {'file_id': file_id}
        if region:
            query['region'] = region
        issued_monotonic = time.monotonic()
        response = self._request('GET', f'{self._BASE}/{release_id}/download-urls?' + urlencode(query), budget=budget)
        if not isinstance(response, dict) or response.get('file_id') != file_id or response.get('expected_sha256') != sha or (type(response.get('expected_size')) is not int) or (response.get('expected_size') != size) or (response.get('region') not in SHARED_REGIONS):
            raise SchemaError('shared download metadata binding mismatch')
        ttl = response.get('expires_in')
        if type(ttl) is not int or not 0 < ttl <= 900:
            raise SchemaError('shared download TTL invalid')
        chosen = response['region']
        if region and chosen != region:
            raise SchemaError('shared requested region echo mismatch')
        _signed_url(response.get('url'), key, self._policy, expected_region=chosen)
        if 'canonical_key' in response and response['canonical_key'] != key:
            raise SchemaError('shared canonical key echo mismatch')
        return _BoundGrant(response, _FileBinding(release_id, file_id, key, size, sha, chosen, issued_monotonic + ttl, response['url']), self)

    def download_file(self, release_id, file_id, target, *, region='', overwrite=True, deadline=None):
        """Lookup first; return verified shared result dict without users anchors."""
        budget = _SharedBudget(deadline)
        if type(overwrite) is not bool:
            raise SchemaError('overwrite must be boolean')
        grant = self._download_grant(release_id, file_id, region, budget)
        binding = self._grant(grant, release_id)
        target = Path(target)
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists() and (not overwrite):
            raise SchemaError('shared target already exists')
        import tempfile
        tmp = tempfile.NamedTemporaryFile(dir=target.parent, prefix='.shared-read-', delete=False)
        digest = hashlib.sha256()
        count = 0
        source = None
        safe_error = None
        try:
            with tmp:
                source = iter(_default_http_get(binding.url, budget))
                for chunk in source:
                    budget.raise_if_exhausted()
                    if count + len(chunk) > binding.size:
                        raise SharedDigestMismatch('shared download exceeds frozen size', biz_code=94047)
                    count += len(chunk)
                    digest.update(chunk)
                    tmp.write(chunk)
            budget.raise_if_exhausted()
            if count != binding.size or digest.hexdigest() != binding.sha256:
                raise SharedDigestMismatch('shared downloaded bytes do not match frozen manifest', biz_code=94047)
            if overwrite:
                os.replace(tmp.name, target)
            else:
                try:
                    os.link(tmp.name, target)
                except FileExistsError:
                    raise SchemaError('shared target already exists') from None
                os.unlink(tmp.name)
            budget.raise_if_exhausted()
        except BaseException as exc:
            try:
                os.unlink(tmp.name)
            except OSError:
                pass
            if isinstance(exc, RequestDeadlineExceeded):
                safe_error = RequestDeadlineExceeded('shared download deadline exhausted')
            elif isinstance(exc, (TransportError, ConnectionError, TimeoutError)):
                status = getattr(exc, 'status', None)
                known_network = isinstance(exc, (ConnectionError, TimeoutError)) or (type(status) is int and 500 <= status < 600)
                safe_error = SharedTransferError(status=status, retryable=known_network)
            else:
                raise
        finally:
            closer = getattr(source, 'close', None)
            if closer is not None:
                try:
                    closer()
                except Exception:
                    pass
        if safe_error is not None:
            raise safe_error
        return {'ok': True, 'file_id': file_id, 'path': str(target), 'bytes_written': count, 'sha256_verified': binding.sha256, 'region': binding.region, 'canonical_key': binding.key}

    @staticmethod
    def _files_of(response):
        manifest = response.get('manifest') if isinstance(response, dict) else None
        return manifest.get('files', []) if isinstance(manifest, dict) else []

    @staticmethod
    def _lease_of(response):
        lease = response.get('upload_lease') if isinstance(response, dict) else None
        return dict(lease) if isinstance(lease, dict) else {}

    @staticmethod
    def _build_manifest(files):
        if not isinstance(files, (list, tuple)) or not files or len(files) > 1000:
            raise SchemaError('shared manifest requires1..1000files')
        manifest = []
        seen = set()
        for record in files:
            if not isinstance(record, dict):
                raise SchemaError('shared manifest entry must be object')
            path = validate_shared_path(record.get('path'))
            if path in seen:
                raise SchemaError('duplicate shared path')
            seen.add(path)
            manifest.append({'path': path, 'size': _size(record.get('size')), 'sha256': validate_shared_sha256(record.get('sha256'))})
        return sorted(manifest, key=lambda record: record['path'])

    @staticmethod
    def _require(value, what):
        return _identity(value, what)

    @staticmethod
    def _close_quietly(resource):
        if resource is not None:
            try:
                resource.close()
            except Exception:
                pass

    @staticmethod
    def _read_bounded(response):
        result = bytearray()
        while len(result) < _MAX_RESP_BYTES:
            block = response.read(min(_CHUNK_BYTES, _MAX_RESP_BYTES - len(result)))
            if not block:
                break
            result.extend(block)
        return bytes(result)

    def _put(self, url, headers, data):
        import tempfile
        with tempfile.NamedTemporaryFile() as tmp:
            tmp.write(data)
            tmp.flush()
            return self._put_streaming(url, headers, tmp.name, len(data), expected_sha256=hashlib.sha256(data).hexdigest())

    def _put_streaming(self, url, headers, local_path, size, *, budget=None, expected_sha256=None):
        import http.client
        from urllib.parse import urlsplit
        budget = budget or _SharedBudget(None)
        budget.raise_if_exhausted()
        if not _SHARED_IO_WORKERS.acquire(blocking=False):
            raise TransportError('shared upload capacity exhausted')
        cancel = threading.Event()
        lock = threading.Lock()
        state = {'conn': None, 'socket': None}
        events = queue.Queue(maxsize=1)

        def check():
            if cancel.is_set():
                raise RequestDeadlineExceeded('shared upload cancelled')
            budget.raise_if_exhausted()

        def chunks():
            total = 0
            digest = hashlib.sha256()
            with open(local_path, 'rb') as source:
                while True:
                    check()
                    block = source.read(_CHUNK_BYTES)
                    if not block:
                        break
                    if total + len(block) > size:
                        raise SharedDigestMismatch('shared upload source grew', biz_code=94047)
                    total += len(block)
                    digest.update(block)
                    yield block
            check()
            if total != size or (expected_sha256 is not None and digest.hexdigest() != expected_sha256):
                raise SharedDigestMismatch('shared upload bytes do not match declared manifest', biz_code=94047)

        def worker():
            conn = resp = None
            try:
                check()
                parsed = urlsplit(url)
                timeout = budget.remaining_seconds()
                conn = http.client.HTTPSConnection(parsed.hostname, parsed.port or 443, timeout=timeout if timeout is not None else 60)
                with lock:
                    state['conn'] = conn
                conn.connect()
                with lock:
                    state['socket'] = getattr(conn, 'sock', None)
                check()
                conn.request('PUT', parsed.path + ('?' + parsed.query if parsed.query else ''), body=chunks(), headers={'Content-Length': str(size)})
                check()
                resp = conn.getresponse()
                self._read_bounded(resp)
                check()
                events.put(('ok', (resp.status, '')))
            except BaseException as exc:
                if isinstance(exc, (SharedError, RequestDeadlineExceeded)):
                    safe = exc
                else:
                    safe = TransportError('shared upload transport failure', status=getattr(exc, 'status', None))
                events.put(('error', safe))
            finally:
                try:
                    self._close_quietly(resp)
                    self._close_quietly(conn)
                finally:
                    _SHARED_IO_WORKERS.release()
        try:
            threading.Thread(target=worker, name='shared-upload', daemon=True).start()
        except BaseException:
            _SHARED_IO_WORKERS.release()
            raise
        try:
            try:
                kind, result = events.get(timeout=budget.remaining_seconds())
            except queue.Empty:
                raise RequestDeadlineExceeded('shared upload deadline exhausted') from None
            budget.raise_if_exhausted()
            if kind == 'error':
                raise result from None
            return result
        finally:
            cancel.set()
            with lock:
                sock = state['socket'] or getattr(state['conn'], 'sock', None)
            if sock is not None:
                try:
                    sock.shutdown(socket.SHUT_RDWR)
                except OSError:
                    pass
                try:
                    sock.close()
                except OSError:
                    pass


def map_shared_error(exc):
    if isinstance(exc,RequestDeadlineExceeded):return exc
    numeric=getattr(exc,"biz_code",None)
    symbolic=_NUMERIC_SHARED_ERRORS.get(numeric) if type(numeric)is int else None
    if symbolic is None and numeric is None and isinstance(exc.data,dict):
        code=exc.data.get("error_code")
        if type(code) is str and code in ERROR_CODE_TO_EXC:symbolic=code
    if symbolic is not None:
        return ERROR_CODE_TO_EXC[symbolic]("shared error: "+symbolic,status=getattr(exc,"status",None),error_code=symbolic,biz_code=numeric,data={})
    return TransportError("shared unclassified transport failure",status=getattr(exc,"status",None),biz_code=numeric if type(numeric) is int else None,data={})
