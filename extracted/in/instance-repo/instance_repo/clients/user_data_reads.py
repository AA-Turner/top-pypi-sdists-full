"""user_data_reads.py — users 域读取 typed HTTP 客户端（user-data-read-v1，isolated）。

Codex read wire 最终合同（read-shared-wire-final-codex-decisions-20261031-1215.json）
实现切片：resolve（union validator）+ download（流式）+ typed models + fixture tests。

**协议（canonical 域）**：
- GET /apis/v1/user-data/reads/resolve?owner=&relative_path=&cluster=；
- 响应必含：schema_version=1/protocol=user-data-read-v1/mode=canonical/
  cluster（echo）/storage_id=ap-userdata-v1/owner（echo）/relative_path
  （echo）/canonical_key（=owner+path 派生）/primary_region/anchor
  {op_id,generation>0,sha256,size>=0}/replicas 恰 cn+sg（bucket/region/
  endpoint 匹配 trusted ReplicasPolicy）/read_urls 恰 cn+sg
  {url,expires_at}/issued_at；
- **双 URL 同锚**：替代单 URL——cn/sg 双 URL 必须绑定同一冻结 anchor
  与 canonical key；网络故障切换一次不改锚；刷新后锚变更=新 resolution
  +丢弃部分下载，同一整体预算；
- **锚只从 Committed* 字段**（服务端 dual-verified commit 后的
  op_id/generation/sha256/size——非 begin 声明值）；无有效锚→
  integrity/notready 错误（**绝不 legacy 降级**）；
- size=0 有效（无 users 8GiB cap）；
- URL：HTTPS/精确 host:port+bucket/endpoint 绑定/对象 key 一次解码
  精确绑定；无 userinfo/fragment；redirect 禁；query 签名 opaque
  secret——URL 凭据 repr 脱敏（repr=False）；不受信 canonical echo
  单独采信；
- expires_at>issued_at 且 lifetime≤900s；dispatch 时未过期；下载
  分块/预算/tempfile 原子 rename；有限整体绝对预算（B 公共 deadline
  时长参数，None 旧语义）。

**协议（legacy 域）**：
- mode=legacy-unanchored：**无** canonical anchor/storage_id/replicas
  字段（空/伪造 canonical storage_id 拒；未知/跨 mode 多余字段拒）；
- 必含：legacy_profile（trusted 非空 ID）/legacy_key/size>=0（授权
  源 HEAD）/read_url/issued_at/expires_at；
- **trusted immutable LegacyReadProfile 表**（profile_id,cluster_names,
  bucket,endpoint,oss_region,owner_root_template）：私有 AP 注入
  LEGACY_READ_PROFILES 表初始为空（未核实的 debug/test/SH-TEST-1）；
  公共 SDK 默认空、无 env/用户配置覆盖、invalid 无 fallback；
  profile 须精确绑定请求逻辑 cluster+实际 verified root+owner+
  relative_path；每 profile 恰一 replica 元组；**服务器响应的
  profile 不自举信任**；
- legacy 无 SHA/generation 保证：size 预算/可选 ETag 是 opaque 源条件
  非 crypto 锚；原子 temp+读 size 校验+显式 unanchored 提示；不伪造
  digest；
- 下次 resolve 撤销生效，但已签发 URL/in-flight 不即时撤销（TTL 界+
  旧客户端过渡限制如实呈现）。

**错误码**（users 域 auth=94022/10003——**非 shared 94040**）：
unknown_cluster 404/94100；dependency 503/94101；invalid_query 400/
94102；pending_replication 409/94103；anchor/digest 422/94108；
not_found 404/94109；users auth 401/403（94022 或 10003）；裸 404=
endpoint unsupported（非 unknown cluster）。

**typed 合同**：本模块/构造/resolve/download 签名按 decision 原文；
frozen deep-immutable tagged union；URL repr=False；结果绑定 mode/
key/bytes（canonical 含 verified SHA/generation；legacy 显式
unanchored）；**缺 policy（canonical 模式）新 client 零 IO**。
"""
from __future__ import annotations

import hashlib
import math
import os
import queue
import re
import socket
import threading
import time
from types import MappingProxyType
from dataclasses import dataclass, field
from pathlib import Path
from typing import Mapping
from urllib.parse import urlencode, urlsplit

from ..errors import RequestDeadlineExceeded, SchemaError, TransportError
from .user_data_writes import (
    ERROR_FAMILY, ReplicasPolicy, UserDataStorageLayoutClient, _Budget,
    _call_with_budget, _derive_users_key, _resolve_replica_policy, validate_owner,
    validate_relative_path)

#: 读协议常量（定稿字符串）。
PROTOCOL = "user-data-read-v1"
STORAGE_ID = "ap-userdata-v1"
#: TTL 上限（秒）——read URL 生命周期（expires-issued ≤ 900）。
MAX_URL_TTL_SECONDS = 900.0
#: users 域 auth 错误码（**非** shared 94040）。
USERS_AUTH_CODES = (94022, 10003)

_RFC3339_RE = re.compile(
    r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})")
_SHA256_RE = re.compile(r"[0-9a-f]{64}")
_OP_ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,127}")
_REGIONS = ("cn", "sg")
_READ_CHUNK = 1024 * 1024


# ── typed 错误（users read 域——沿 writes 941xx 族 + users auth 码）──

_READ_ERROR_CODES = dict(ERROR_FAMILY)
_READ_ERROR_CODES.update({
    94100: "storage_cluster_unknown",     # 404
    94101: "storage_dual_unavailable",    # 503
    94102: "user_data_read_invalid",      # 400（读域 invalid_query）
    94103: "user_data_read_pending",      # 409（pending_replication）
    94108: "user_data_read_anchor_invalid",  # 422
    94109: "user_data_read_not_found",    # 404
})
USERS_READ_ERROR_FAMILY = _READ_ERROR_CODES


def map_user_data_read_error(exc: TransportError, *,
                             bound_op_id: str | None = None
                             ) -> TransportError:
    """读域错误映射（与 writes 同 sanitizer；941xx+users auth 码）。"""
    from ..errors import RequestDeadlineExceeded
    if isinstance(exc, RequestDeadlineExceeded):
        return RequestDeadlineExceeded("user-data read deadline exhausted")
    biz = getattr(exc, "biz_code", None)
    err_code = (exc.data or {}).get("error_code") if exc.data else None
    cls_name = None
    # Preserve status/code, never remote message/data or signed URL causes.
    if type(biz) is int and biz in USERS_AUTH_CODES:
        return TransportError("user-data read authorization denied",
                              status=getattr(exc, "status", None),
                              biz_code=biz, data={})
    if isinstance(biz, int):
        cls_name = _READ_ERROR_CODES.get(biz)
    if cls_name is None and isinstance(err_code, str):
        cls_name = err_code if err_code in _READ_ERROR_CODES.values() \
            else None
    if cls_name is not None:
        status = getattr(exc, "status", None)
        from .user_data_writes import UserDataWriteError
        message = f"user-data read error: {cls_name}"
        if isinstance(status, int):
            message += f" (HTTP {status})"
        # 复用 writes 的 typed 异常族（同 941xx 数值语义）。
        from . import user_data_writes as _w
        wcls = _w._ERROR_CODE_TO_EXC.get(cls_name)
        if wcls is None:
            # 读域新码（94102 read_invalid 等）→ 泛化 UserDataWriteError
            # 子类形态。
            wcls = type("UserDataReadError", (UserDataWriteError,),
                        {"code": "E_USERDATA_READ",
                         "error_code": cls_name})
        return wcls(message, status=status, biz_code=biz,
                    error_code=cls_name, data={})
    # 未知 → 泛化 safe type（不含 raw message）。
    from .user_data_writes import UserDataWriteInvalid
    status = getattr(exc, "status", None)
    return UserDataWriteInvalid(
        "user-data read error: unclassified transport failure"
        + (f" (HTTP {status})" if isinstance(status, int) else ""),
        status=status, biz_code=None,
        error_code="user_data_write_invalid", data=None)


# ── typed models（frozen/deep-immutable；URL repr=False）─────────────

@dataclass(frozen=True)
class ReadAnchor:
    """冻结锚——只来自服务端 Committed* 字段（dual-verified commit 后）。

    客户端**不接受** begin 声明值/文件名推断的锚；无有效锚=integrity
    错误（不 legacy 降级）。"""
    op_id: str
    generation: int               # >0
    sha256: str                   # 64 lower hex
    size: int                     # >=0（0 有效）


@dataclass(frozen=True)
class ReadReplica:
    region: str
    bucket: str
    endpoint: str


@dataclass(frozen=True)
class ReadURL:
    """单地域预签名读 URL（secret——repr=False）。"""
    region: str
    url: str = field(repr=False)
    expires_at: str


@dataclass(frozen=True)
class CanonicalReadResolution:
    """canonical 读解析（tagged union: mode=canonical）。

    双 URL **同锚**（同 anchor+canonical_key）——网络故障切换一次不
    改锚；刷新后锚变更=新 resolution。"""
    cluster: str
    storage_id: str
    owner: str
    relative_path: str
    canonical_key: str
    primary_region: str
    anchor: ReadAnchor
    replicas: Mapping             # {"cn": ReadReplica, "sg": ReadReplica}
    read_urls: Mapping            # {"cn": ReadURL, "sg": ReadURL}
    issued_at: str
    mode: str = "canonical"
    schema_version: int = 1
    protocol: str = PROTOCOL

    def __post_init__(self):
        if (not isinstance(self.anchor, ReadAnchor)
                or not isinstance(self.replicas, Mapping)
                or not isinstance(self.read_urls, Mapping)
                or set(self.replicas) != set(_REGIONS)
                or set(self.read_urls) != set(_REGIONS)):
            raise SchemaError("canonical model requires typed anchor and cn/sg maps")
        for region in _REGIONS:
            if (type(self.replicas[region]) is not ReadReplica
                    or self.replicas[region].region != region
                    or type(self.read_urls[region]) is not ReadURL
                    or self.read_urls[region].region != region):
                raise SchemaError("canonical model region/type mismatch")
        object.__setattr__(self, "replicas", MappingProxyType(dict(self.replicas)))
        object.__setattr__(self, "read_urls", MappingProxyType(dict(self.read_urls)))


@dataclass(frozen=True)
class LegacyReadProfile:
    """trusted 不可变 legacy 读 profile（显式表注入——服务器响应不
    自举信任）。

    profile 须精确绑定请求逻辑 cluster（cluster_names 含之）+实际
    verified root（owner_root_template）+owner+relative_path。每
    profile 恰一 replica 元组。"""
    profile_id: str
    cluster_names: tuple          # frozenset 形态（immutable）
    bucket: str
    endpoint: str
    oss_region: str
    owner_root_template: str      # 如 "swe/user-data/users/{owner}/"

    def __post_init__(self):
        if not isinstance(self.profile_id, str) or not self.profile_id:
            raise SchemaError("LegacyReadProfile: profile_id nonempty str")
        if not isinstance(self.cluster_names, (tuple, frozenset)) or \
                not self.cluster_names or not all(
                    isinstance(c, str) and c for c in self.cluster_names):
            raise SchemaError(
                "LegacyReadProfile: cluster_names nonempty str collection")
        for name in ("bucket", "endpoint", "oss_region",
                     "owner_root_template"):
            v = getattr(self, name)
            if not isinstance(v, str) or not v:
                raise SchemaError(
                    f"LegacyReadProfile: {name} nonempty str")
        # endpoint HTTPS 无 userinfo（同 canonical 纪律）。
        from .user_data_writes import _validate_https_endpoint
        endpoint = _validate_https_endpoint(self.endpoint, "profile.endpoint")
        object.__setattr__(self, "endpoint", endpoint)
        object.__setattr__(self, "cluster_names", tuple(self.cluster_names))
        if not re.fullmatch(r"[a-z0-9][a-z0-9.-]{0,61}[a-z0-9]", self.bucket):
            raise SchemaError("LegacyReadProfile: invalid bucket")
        if self.owner_root_template.count("{owner}") != 1:
            raise SchemaError("LegacyReadProfile: root must bind owner once")
        rest = self.owner_root_template.replace("{owner}", "owner")
        if "{" in rest or "}" in rest or not rest.endswith("/"):
            raise SchemaError("LegacyReadProfile: invalid owner root template")
        validate_relative_path(rest[:-1])

    def derive_legacy_key(self, owner: str, relative_path: str) -> str:
        root = self.owner_root_template.format(owner=owner)
        return root + relative_path


@dataclass(frozen=True)
class LegacyReadResolution:
    """legacy 读解析（tagged union: mode=legacy-unanchored）。

    **显式无锚**：无 SHA/generation 保证——size 是授权源 HEAD 的
    opaque 条件；结果 LegacyReadResult.unanchored=True。"""
    cluster: str
    owner: str
    relative_path: str
    legacy_profile: str           # trusted profile ID（echo 校验）
    legacy_key: str
    size: int                     # >=0（源 HEAD）
    read_url: str = field(repr=False)
    issued_at: str
    expires_at: str
    mode: str = "legacy-unanchored"
    schema_version: int = 1
    protocol: str = PROTOCOL


@dataclass(frozen=True)
class VerifiedReadResult:
    """canonical 下载结果（绑定 mode/key/bytes+verified SHA/generation）。"""
    canonical_key: str
    anchor: ReadAnchor
    bytes_written: int
    sha256_verified: str
    target: Path
    mode: str = "canonical"


@dataclass(frozen=True)
class LegacyReadResult:
    """legacy 下载结果（unanchored——无 crypto 锚；size 校验过）。"""
    legacy_key: str
    bytes_written: int
    target: Path
    mode: str = "legacy-unanchored"
    unanchored: bool = True


# ── 严格解码 helpers ──────────────────────────────────────────────────

def _req_str(d, key, what):
    v = d.get(key)
    if not isinstance(v, str) or not v:
        raise SchemaError(f"response missing nonempty {what!r}")
    return v


def _req_int(d, key, what, *, minimum=None):
    v = d.get(key)
    if isinstance(v, bool) or not isinstance(v, int):
        raise SchemaError(f"response field {what!r} must be an integer")
    if minimum is not None and v < minimum:
        raise SchemaError(f"response field {what!r} must be >= {minimum}")
    return v


def _req_rfc3339(d, key, what):
    v = _req_str(d, key, what)
    if not _RFC3339_RE.fullmatch(v):
        raise SchemaError(f"response field {what!r} must be RFC3339 UTC")
    return v


def _parse_utc(v: str) -> float:
    from ._rfc3339 import parse_utc
    parsed = None
    try:
        parsed = parse_utc(v, allow_offset=True)
    except ValueError:
        pass
    if parsed is None:
        raise SchemaError("invalid RFC3339 datetime")
    return parsed.timestamp()


def _read_budget(deadline):
    if deadline is not None and (isinstance(deadline, bool)
            or not isinstance(deadline, (int, float))
            or not math.isfinite(deadline) or deadline < 0):
        raise SchemaError("read deadline must be finite nonnegative seconds or None")
    return _Budget(deadline)


def _strict_fields(value, allowed, what):
    if not isinstance(value, dict) or set(value) != set(allowed):
        raise SchemaError(f"{what}: unexpected or missing fields")


def _endpoint_identity(endpoint):
    from .user_data_writes import _validate_https_endpoint
    invalid_endpoint = False
    try:
        normalized = _validate_https_endpoint(endpoint, "read endpoint")
    except SchemaError:
        invalid_endpoint = True
    if invalid_endpoint:
        raise SchemaError("read endpoint has invalid structure")
    parsed = urlsplit(normalized)
    return normalized, parsed.hostname, parsed.port or 443


def _validate_regional_endpoint(endpoint, bucket, oss_region):
    normalized, host, port = _endpoint_identity(endpoint)
    # Policy supplies the OSS region; response cannot choose another service.
    expected = {f"oss-{oss_region}.aliyuncs.com",
                f"oss-{oss_region}-internal.aliyuncs.com"}
    if host not in expected or port != 443:
        raise SchemaError("replica endpoint does not bind trusted OSS region")
    return normalized


def _validate_read_url(region, url, *, expires_at, issued_at,
                       bucket, endpoint, canonical_key):
    invalid_structure = False
    try:
        u = urlsplit(url)
        port = u.port or 443
    except ValueError:
        invalid_structure = True
    if invalid_structure:
        raise SchemaError("read URL has invalid structure")
    if (u.scheme != "https" or not u.hostname or u.username is not None
            or u.password is not None or u.fragment
            or any(ord(c) <= 32 for c in url)):
        raise SchemaError("read URL must be HTTPS without userinfo or fragment")
    _, ehost, eport = _endpoint_identity(endpoint)
    host = u.hostname.lower()
    if port != eport:
        raise SchemaError("read URL port does not bind trusted endpoint")
    from urllib.parse import unquote
    if re.search(r"%(?![0-9A-Fa-f]{2})", u.path):
        raise SchemaError("read URL has invalid path encoding")
    invalid_encoding = False
    try:
        decoded = unquote(u.path, errors="strict")
    except UnicodeError:
        invalid_encoding = True
    if invalid_encoding:
        raise SchemaError("read URL has invalid path encoding")
    if host == f"{bucket}.{ehost}":
        expected_path = "/" + canonical_key
    elif host == ehost:
        expected_path = "/" + bucket + "/" + canonical_key
    else:
        raise SchemaError("read URL host does not bind trusted bucket/endpoint")
    if decoded != expected_path:
        raise SchemaError("read URL path does not bind bucket and object key")
    issued, expires = _parse_utc(issued_at), _parse_utc(expires_at)
    if not 0 < expires - issued <= MAX_URL_TTL_SECONDS:
        raise SchemaError("read URL lifetime must be positive and at most 900s")
    return ReadURL(region=region, url=url, expires_at=expires_at)


# ── 客户端 ────────────────────────────────────────────────────────────

class UserDataReadsClient:
    """users 域读客户端（resolve+download；isolated 单 writer）。

    构造（合同原文）：``UserDataReadsClient(transport, *, discovery=
    None, expected_replica_policy=None, legacy_profiles=None)``。
    """

    def __init__(self, transport, *,
                 discovery: UserDataStorageLayoutClient | None = None,
                 expected_replica_policy: ReplicasPolicy | None = None,
                 legacy_profiles=None) -> None:
        self._t = transport
        explicit = _resolve_replica_policy(expected_replica_policy)
        if discovery is not None:
            if not isinstance(discovery, UserDataStorageLayoutClient):
                raise SchemaError("discovery must be UserDataStorageLayoutClient")
            existing = discovery.replica_policy
            if explicit is not None and existing is not None and explicit != existing:
                raise SchemaError("conflicting read/discovery replica policies")
            self._policy = explicit if explicit is not None else existing
            if existing is None and self._policy is not None:
                discovery._policy = self._policy
            self._discovery = discovery
        else:
            self._discovery = UserDataStorageLayoutClient(
                transport, expected_replica_policy=explicit)
            self._policy = self._discovery.replica_policy
        profiles = {}
        if legacy_profiles is not None:
            if isinstance(legacy_profiles, Mapping):
                items = legacy_profiles.items()
            else:
                items = ((p.profile_id, p) for p in legacy_profiles)
            for pid, prof in items:
                if not isinstance(prof, LegacyReadProfile) or prof.profile_id != pid:
                    raise SchemaError("legacy_profiles must bind typed profile IDs")
                if pid in profiles:
                    raise SchemaError("duplicate legacy profile ID")
                profiles[pid] = prof
        self._legacy_profiles = MappingProxyType(profiles)
        if self._policy is not None:
            if self._policy.storage_id != STORAGE_ID:
                raise SchemaError("read policy storage_id must be ap-userdata-v1")
            for region in _REGIONS:
                if (not re.fullmatch(r"[a-z0-9][a-z0-9-]{1,61}[a-z0-9]", self._policy.bucket(region))
                        or not re.fullmatch(r"[a-z]+-[a-z]+-?[0-9]*", self._policy.oss_region(region))):
                    raise SchemaError("read policy has invalid OSS bucket/region identity")

    @property
    def replica_policy(self):
        return self._policy

    # ── resolve ──
    def resolve(self, *, owner: str, relative_path: str, cluster: str,
                deadline: float | None = None
                ) -> "CanonicalReadResolution | LegacyReadResolution":
        """GET /apis/v1/user-data/reads/resolve（union validator）。

        - 严格 echo（owner/path/cluster 与请求一致）；
        - mode 分派：canonical（须 policy+layout 校验）/legacy-
          unanchored（须 trusted profile 绑定校验）；
        - 未知/跨 mode 多余字段拒；错误按读域码表映射。
        """
        owner = validate_owner(owner)
        rel = validate_relative_path(relative_path)
        if not isinstance(cluster, str) or not cluster or cluster != cluster.strip():
            raise SchemaError("cluster must not be empty")
        budget = _read_budget(deadline)
        budget.raise_if_exhausted()
        # All modes require the trusted policy before any control/data IO.
        if self._policy is None:
            raise SchemaError(
                "read client requires expected replica policy: refusing any IO")
        path = ("/apis/v1/user-data/reads/resolve?"
                + urlencode({"owner": owner, "relative_path": rel,
                             "cluster": cluster}))
        safe_error = None
        try:
            resp = _call_with_budget(budget, self._t, "GET", path)
        except TransportError as exc:
            safe_error = map_user_data_read_error(exc)
        if safe_error is not None:
            raise safe_error
        if not isinstance(resp, dict):
            raise SchemaError("read resolve response must be an object")
        return self._parse_resolution(resp, owner=owner, rel=rel,
                                      cluster=cluster)

    def _parse_resolution(self, resp, *, owner, rel, cluster):
        sv = resp.get("schema_version")
        if isinstance(sv, bool) or not isinstance(sv, int) or sv != 1:
            raise SchemaError(
                "read resolve schema_version must be strict int 1")
        protocol = _req_str(resp, "protocol", "protocol")
        if protocol != PROTOCOL:
            raise SchemaError("unexpected read protocol")
        mode = _req_str(resp, "mode", "mode")
        echo_cluster = _req_str(resp, "cluster", "cluster")
        if echo_cluster != cluster:
            raise SchemaError("read resolve cluster echo mismatch")
        echo_owner = _req_str(resp, "owner", "owner")
        if echo_owner != owner:
            raise SchemaError("read resolve owner echo mismatch")
        echo_rel = _req_str(resp, "relative_path", "relative_path")
        if echo_rel != rel:
            raise SchemaError(
                "read resolve relative_path echo mismatch")
        if mode == "canonical":
            return self._parse_canonical(resp, owner=owner, rel=rel,
                                         cluster=cluster)
        if mode == "legacy-unanchored":
            return self._parse_legacy(resp, owner=owner, rel=rel,
                                      cluster=cluster)
        raise SchemaError("unknown read resolve mode")

    def _parse_canonical(self, resp, *, owner, rel, cluster):
        _strict_fields(resp, ("schema_version", "protocol", "mode", "cluster",
            "storage_id", "owner", "relative_path", "canonical_key",
            "primary_region", "anchor", "replicas", "read_urls", "issued_at"),
            "canonical response")
        policy = self._policy
        if policy is None:
            raise SchemaError(
                "canonical read requires expected replica policy "
                "(missing policy: refusing unverified layout)")
        storage_id = _req_str(resp, "storage_id", "storage_id")
        if storage_id != policy.storage_id:
            raise SchemaError(
                "canonical storage_id does not match policy")
        canonical_key = _req_str(resp, "canonical_key", "canonical_key")
        expected_key = _derive_users_key(owner, rel)
        if canonical_key != expected_key:
            raise SchemaError(
                "canonical_key does not match owner+relative_path")
        primary = _req_str(resp, "primary_region", "primary_region")
        if primary not in _REGIONS:
            raise SchemaError("invalid primary_region")
        # anchor（Committed* 字段语义——服务端 dual-verified）。
        a = resp.get("anchor")
        if not isinstance(a, dict):
            raise SchemaError("canonical anchor must be an object")
        _strict_fields(a, ("op_id", "generation", "sha256", "size"), "anchor")
        op_id = _req_str(a, "op_id", "anchor.op_id")
        if not _OP_ID_RE.fullmatch(op_id):
            raise SchemaError("anchor.op_id must be a safe segment")
        generation = _req_int(a, "generation", "anchor.generation",
                              minimum=1)
        sha = _req_str(a, "sha256", "anchor.sha256")
        if not _SHA256_RE.fullmatch(sha):
            raise SchemaError("anchor.sha256 must be 64 lowercase hex")
        size = _req_int(a, "size", "anchor.size", minimum=0)
        anchor = ReadAnchor(op_id=op_id, generation=generation,
                            sha256=sha, size=size)
        # replicas 恰 cn+sg 匹配 policy。
        reps = resp.get("replicas")
        if not isinstance(reps, dict) or set(reps) != set(_REGIONS):
            raise SchemaError("canonical replicas must be exactly cn+sg")
        parsed_reps = {}
        for r in _REGIONS:
            rec = reps[r]
            if not isinstance(rec, dict):
                raise SchemaError(f"replicas[{r!r}] must be an object")
            _strict_fields(rec, ("bucket", "endpoint", "region"), "replica")
            bucket = _req_str(rec, "bucket", f"replicas.{r}.bucket")
            endpoint = _req_str(rec, "endpoint", f"replicas.{r}.endpoint")
            region = _req_str(rec, "region", f"replicas.{r}.region")
            if bucket != policy.bucket(r):
                raise SchemaError(
                    f"replicas.{r}.bucket does not match policy")
            if region != policy.oss_region(r):
                raise SchemaError(
                    f"replicas.{r}.region does not match policy")
            endpoint = _validate_regional_endpoint(endpoint, bucket, region)
            parsed_reps[r] = ReadReplica(region=r, bucket=bucket,
                                         endpoint=endpoint)
        # read_urls 恰 cn+sg——双 URL 同锚（绑定 canonical_key 校验）。
        urls = resp.get("read_urls")
        if not isinstance(urls, dict) or set(urls) != set(_REGIONS):
            raise SchemaError("canonical read_urls must be exactly cn+sg")
        issued_at = _req_rfc3339(resp, "issued_at", "issued_at")
        parsed_urls = {}
        for r in _REGIONS:
            rec = urls[r]
            if not isinstance(rec, dict):
                raise SchemaError(f"read_urls[{r!r}] must be an object")
            _strict_fields(rec, ("url", "expires_at"), "read URL record")
            url = _req_str(rec, "url", f"read_urls.{r}.url")
            expires = _req_rfc3339(rec, "expires_at",
                                   f"read_urls.{r}.expires_at")
            parsed_urls[r] = _validate_read_url(
                r, url, expires_at=expires, issued_at=issued_at,
                bucket=parsed_reps[r].bucket, endpoint=parsed_reps[r].endpoint,
                canonical_key=canonical_key)
        return CanonicalReadResolution(
            cluster=cluster, storage_id=storage_id, owner=owner,
            relative_path=rel, canonical_key=canonical_key,
            primary_region=primary, anchor=anchor,
            replicas=parsed_reps, read_urls=parsed_urls,
            issued_at=issued_at)

    def _parse_legacy(self, resp, *, owner, rel, cluster):
        _strict_fields(resp, ("schema_version", "protocol", "mode", "cluster",
            "owner", "relative_path", "legacy_profile", "legacy_key", "size",
            "read_url", "issued_at", "expires_at"), "legacy response")
        profile_id = _req_str(resp, "legacy_profile", "legacy_profile")
        profile = self._legacy_profiles.get(profile_id)
        if profile is None:
            # 服务器响应 profile 不自举信任——无 trusted profile 即拒。
            raise SchemaError(
                "legacy_profile not in trusted legacy profile table")
        # cluster 绑定校验。
        if cluster not in tuple(profile.cluster_names):
            raise SchemaError(
                "legacy profile does not bind requested cluster")
        legacy_key = _req_str(resp, "legacy_key", "legacy_key")
        expected_key = profile.derive_legacy_key(owner, rel)
        if legacy_key != expected_key:
            raise SchemaError(
                "legacy_key does not match trusted profile root+owner"
                "+path")
        size = _req_int(resp, "size", "size", minimum=0)
        url = _req_str(resp, "read_url", "read_url")
        issued_at = _req_rfc3339(resp, "issued_at", "issued_at")
        expires_at = _req_rfc3339(resp, "expires_at", "expires_at")
        _validate_read_url("legacy", url, expires_at=expires_at,
            issued_at=issued_at, bucket=profile.bucket, endpoint=profile.endpoint,
            canonical_key=legacy_key)
        return LegacyReadResolution(
            cluster=cluster, owner=owner, relative_path=rel,
            legacy_profile=profile_id, legacy_key=legacy_key, size=size,
            read_url=url, issued_at=issued_at, expires_at=expires_at)

    # ── download ──
    def download(self, resolution, target: Path, *, overwrite: bool = True,
                 deadline: float | None = None
                 ) -> "VerifiedReadResult | LegacyReadResult":
        """流式下载（canonical=双 URL 同锚 failover 一次+SHA 校验；
        legacy=单 URL+size 校验+unanchored）。

        纪律：1MiB 分块不整读；tempfile 原子 rename；redirect 禁；
        dispatch 时 URL 未过期；有限整体绝对预算。
        """
        if type(overwrite) is not bool:
            raise SchemaError("overwrite must be a boolean")
        if self._policy is None:
            raise SchemaError("read client requires expected replica policy")
        budget = _read_budget(deadline)
        budget.raise_if_exhausted()
        # Revalidate even caller-constructed models; immutable dataclasses alone
        # are not evidence of trusted URL validation.
        resolution = self._validate_resolution_model(resolution)
        target = Path(target)
        if isinstance(resolution, CanonicalReadResolution):
            return self._download_canonical(resolution, target,
                                             overwrite=overwrite,
                                             budget=budget)
        if isinstance(resolution, LegacyReadResolution):
            return self._download_legacy(resolution, target,
                                         overwrite=overwrite,
                                         budget=budget)
        raise SchemaError("unknown resolution type")

    def _validate_resolution_model(self, res):
        from dataclasses import asdict
        common = ("schema_version", "protocol", "mode", "cluster", "owner", "relative_path")
        if type(res) is CanonicalReadResolution:
            wire = {k: getattr(res, k) for k in common}
            wire.update(storage_id=res.storage_id, canonical_key=res.canonical_key,
                primary_region=res.primary_region, anchor=asdict(res.anchor),
                replicas={r: {"bucket": v.bucket, "region": self._policy.oss_region(r),
                    "endpoint": v.endpoint} for r, v in res.replicas.items()},
                read_urls={r: {"url": v.url, "expires_at": v.expires_at}
                    for r, v in res.read_urls.items()}, issued_at=res.issued_at)
        elif type(res) is LegacyReadResolution:
            wire = {k: getattr(res, k) for k in common}
            wire.update(legacy_profile=res.legacy_profile, legacy_key=res.legacy_key,
                size=res.size, read_url=res.read_url, issued_at=res.issued_at,
                expires_at=res.expires_at)
        else:
            raise SchemaError("unknown resolution type")
        try:
            owner, rel = validate_owner(res.owner), validate_relative_path(res.relative_path)
            return self._parse_resolution(wire, owner=owner, rel=rel, cluster=res.cluster)
        except (KeyError, TypeError, AttributeError, ValueError):
            pass
        raise SchemaError("invalid typed read resolution")

    def _download_canonical(self, res, target, *, overwrite, budget):
        budget.raise_if_exhausted()
        if target.exists() and not overwrite:
            raise SchemaError(
                f"target exists and overwrite=False: {target}")
        target.parent.mkdir(parents=True, exist_ok=True)
        # 主 URL 优先（primary_region）；网络失败 failover 一次到
        # 另一 region URL——**同锚**（不改 anchor——URL 校验时已绑定）。
        order = [res.primary_region] + [
            r for r in _REGIONS if r != res.primary_region]
        last_exc = None
        for idx, region in enumerate(order):
            if idx > 0:
                budget.raise_if_exhausted()
            read_url = res.read_urls[region]
            # dispatch 时未过期。
            if _parse_utc(read_url.expires_at) <= time.time():
                raise SchemaError("read URL expired at dispatch; resolve again")
            try:
                return self._stream_download(
                    read_url.url, target,
                    expected_sha256=res.anchor.sha256,
                    expected_size=res.anchor.size, budget=budget,
                    canonical_key=res.canonical_key,
                    anchor=res.anchor, overwrite=overwrite)
            except (TransportError, ConnectionError, TimeoutError) as exc:
                if not _is_read_network_error(exc):
                    raise               # 终态（4xx/schema/auth）
                last_exc = _safe_read_io_error(exc)
                continue                # 同锚 failover 一次
        raise last_exc if last_exc else SchemaError(
            "no readable URL available")

    def _download_legacy(self, res, target, *, overwrite, budget):
        budget.raise_if_exhausted()
        if target.exists() and not overwrite:
            raise SchemaError(
                f"target exists and overwrite=False: {target}")
        target.parent.mkdir(parents=True, exist_ok=True)
        if _parse_utc(res.expires_at) <= time.time():
            raise SchemaError("legacy read_url expired at dispatch")
        return self._stream_download(
            res.read_url, target, expected_sha256=None,
            expected_size=res.size, budget=budget,
            canonical_key=None, anchor=None, legacy_mode=True,
            legacy_key=res.legacy_key, overwrite=overwrite)

    def _stream_download(self, url, target, *, expected_sha256,
                         expected_size, budget, canonical_key=None,
                         anchor=None, legacy_mode=False,
                         legacy_key=None, overwrite=True):
        """共享流式下载（1MiB 分块+tempfile 原子 rename+SHA/size 校验）。

        The default reader uses request-owned, bounded streaming HTTP IO.
        A private injected getter remains available for deterministic tests.
        """
        getter = getattr(self, "_http_get", None) or _default_http_get
        budget.raise_if_exhausted()
        h = hashlib.sha256() if expected_sha256 else None
        total = 0
        import tempfile
        tmp = tempfile.NamedTemporaryFile(
            dir=str(target.parent), delete=False,
            prefix=".read-", suffix=".tmp")
        source = None
        safe_error = None
        try:
            with tmp:
                source = iter(getter(url, budget))
                for chunk in source:
                    budget.raise_if_exhausted()
                    if not isinstance(chunk, bytes) or len(chunk) > _READ_CHUNK:
                        raise SchemaError("read source must yield bounded byte chunks")
                    if total + len(chunk) > expected_size:
                        raise SchemaError("downloaded size exceeds expected size")
                    total += len(chunk)
                    if h is not None:
                        h.update(chunk)
                    tmp.write(chunk)

            budget.raise_if_exhausted()   # including empty/late EOF
            # size 校验（canonical=锚 size；legacy=源 HEAD size）。
            if expected_size is not None and total != expected_size:
                raise SchemaError(
                    f"downloaded size {total} != expected "
                    f"{expected_size}")
            # SHA 校验（仅 canonical——legacy 不伪造 digest）。
            if h is not None and h.hexdigest() != expected_sha256:
                from .user_data_writes import UserDataWriteDigestMismatch
                raise UserDataWriteDigestMismatch(
                    "read SHA mismatch vs frozen anchor",
                    biz_code=94108,
                    error_code="user_data_write_digest_mismatch")
            budget.raise_if_exhausted()
            if overwrite:
                os.replace(tmp.name, str(target))
            else:
                # Same directory/filesystem: hardlink publication is an atomic
                # no-replace operation, unlike exists()+replace().
                try:
                    os.link(tmp.name, str(target))
                except FileExistsError:
                    raise SchemaError("target exists and overwrite=False") from None
                os.unlink(tmp.name)
            budget.raise_if_exhausted()
        except BaseException as exc:
            # 清理自己的 temp（失败路径——不动他人文件）。
            try:
                os.unlink(tmp.name)
            except OSError:
                pass
            if isinstance(exc, (TransportError, ConnectionError, TimeoutError)):
                safe_error = _safe_read_io_error(exc)
            else:
                raise
        finally:
            close = getattr(source, "close", None)
            if close is not None:
                try:
                    close()
                except Exception:
                    pass  # cleanup must not expose/mask the original failure
        if safe_error is not None:
            raise safe_error
        if legacy_mode:
            return LegacyReadResult(
                legacy_key=legacy_key, bytes_written=total,
                unanchored=True, target=target)
        return VerifiedReadResult(
            canonical_key=canonical_key, anchor=anchor,
            bytes_written=total, sha256_verified=expected_sha256,
            target=target)


def _is_read_network_error(exc):
    if isinstance(exc, RequestDeadlineExceeded):
        return False
    if isinstance(exc, (ConnectionError, TimeoutError, socket.timeout)):
        return True
    status = getattr(exc, "status", None)
    return type(status) is int and 500 <= status <= 599


class ReadCapacityExceeded(TransportError):
    """All bounded read workers are occupied; no further IO started."""


def _safe_read_io_error(exc):
    if isinstance(exc, RequestDeadlineExceeded):
        return RequestDeadlineExceeded("user-data read deadline exhausted")
    if isinstance(exc, ReadCapacityExceeded):
        return ReadCapacityExceeded("read download capacity exhausted")
    if isinstance(exc, (ConnectionError, TimeoutError, socket.timeout)):
        return ConnectionError("user-data read network failure")
    status = getattr(exc, "status", None)
    return TransportError("user-data read HTTP failure",
                          status=status if type(status) is int else None)


# Bounded outstanding workers and queue: slow DNS may retain a daemon worker,
# but never an unbounded thread/buffer population or publish after cancellation.
_HTTP_WORKERS = threading.BoundedSemaphore(4)


def _default_http_get(url, budget):
    import http.client
    budget.raise_if_exhausted()
    if not _HTTP_WORKERS.acquire(blocking=False):
        raise ReadCapacityExceeded("read download capacity exhausted")
    events = queue.Queue(maxsize=1)
    cancelled = threading.Event()
    lock = threading.Lock()
    state = {"connection": None, "response": None, "socket": None}

    def cancel():
        cancelled.set()
        with lock:
            sock = state["socket"]
            conn = state["connection"]
        if sock is None and conn is not None:
            sock = getattr(conn, "sock", None)
        if sock is not None:
            try:
                sock.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            try:
                sock.close()
            except OSError:
                pass

    def emit(kind, value=None):
        while not cancelled.is_set():
            try:
                events.put((kind, value), timeout=.05)
                return
            except queue.Full:
                continue

    def check():
        if cancelled.is_set():
            raise RequestDeadlineExceeded("user-data read deadline exhausted")
        budget.raise_if_exhausted()

    def worker():
        connection = response = None
        try:
            check()
            parsed = urlsplit(url)
            timeout = budget.remaining_seconds()
            connection = http.client.HTTPSConnection(parsed.hostname,
                port=parsed.port or 443, timeout=timeout if timeout is not None else 30.)
            with lock:
                state["connection"] = connection
            # Explicit connect/check ensures delayed DNS/connect never sends
            # HTTP headers after owner cancellation.
            connection.connect()
            with lock:
                state["socket"] = connection.sock
            check()
            connection.request("GET", parsed.path + ("?" + parsed.query if parsed.query else ""))
            check()
            response = connection.getresponse()
            with lock:
                state["response"] = response
                # HTTP/1.0 closes conn.sock while the response still owns it.
                if state["socket"] is None:
                    state["socket"] = getattr(getattr(getattr(response, "fp", None), "raw", None), "_sock", None)
            check()
            if not 200 <= response.status < 300:
                raise TransportError("user-data read HTTP failure", status=response.status)
            while True:
                check()
                chunk = response.read1(_READ_CHUNK)
                check()
                if not chunk:
                    break
                emit("chunk", chunk)
            emit("eof")
        except BaseException as exc:
            emit("error", _safe_read_io_error(exc))
        finally:
            try:
                for resource in (response, connection):
                    if resource is not None:
                        try:
                            resource.close()
                        except Exception:
                            # Cleanup is best effort; never leak credentials via
                            # an unhandled daemon traceback or lose capacity.
                            pass
            finally:
                _HTTP_WORKERS.release()

    thread = threading.Thread(target=worker, name="userdata-read", daemon=True)
    try:
        thread.start()
    except BaseException:
        _HTTP_WORKERS.release()
        raise
    try:
        while True:
            budget.raise_if_exhausted()
            remaining = budget.remaining_seconds()
            try:
                kind, value = events.get(timeout=remaining)
            except queue.Empty:
                raise RequestDeadlineExceeded("user-data read deadline exhausted") from None
            budget.raise_if_exhausted()
            if kind == "eof":
                return
            if kind == "error":
                raise value from None
            yield value
    finally:
        cancel()
