"""user_data_writes.py — users 域双写 typed HTTP 客户端（dual-object-v1，isolated）v2。

Codex wire 定稿（wire-and-fetcher-codex-decisions-20261031.json）+
AP-B-REVIEW-20261031-0620 返修实现（P1×5+P2+temp/final 双向重叠契约）。

**本切片边界**：isolated client（不接 legacy 写入口）；A 未解恢复约束显式
unavailable 不伪造 committed；**真实 OSS 流式 adapter 与真实 transport 预算
测试归 D 线（user_data_upload.py）**——本模块默认 adapter 仅签名占位。

返修要点（编号=review findings）：
P1-1 SECRET-REPR：WriteTarget 四个凭据字段与 BeginWriteResult.fencing_token
  均 field(repr=False)（默认 repr 即安全）；map_user_data_write_error 不回显
  服务端 message/data（泛化 message+白名单键净化 data）。
P1-2 DESTINATION-BINDING：discovery 强制 canonical cn/sg 桶+OSS region
  精确登记；begin target endpoint 经结构化 HTTPS 校验（hostname/port/path/
  query/fragment）并归一化后必须与已验证 discovery endpoint 一致；两 target
  全部验证通过后才进入 IO。
P1-3 REQUEST-CONTENT-BINDING：BeginWriteResult 绑定 expected_sha256/
  expected_size/owner/relative_path/primary_region/idempotency_key；upload
  前（stat+流式 SHA）后（再校验防源变动）双重校验，不符拒绝；commit 回执
  比对 expected digest/size（不符→94108）。
P1-4 REGION-AND-AUTH：上传顺序=primary_region 先（both on full success）；
  auth 拒绝（401/403）/schema/digest 类终态即停不试 alternate 桶；仅明确
  网络类错误有界续 secondary；partial 保留 per-target 明细与首个 cause。
P1-5 OPERATION-STATE-BINDING：op_id 严格单段校验（拒 dot/dotdot/query/
  fragment/编码分隔符）复用于 begin 解析/status/commit URL/wait；status
  响应 op 必须等于请求 op、状态在 allowlist、protocol 必须为 dual-object-v1；
  同幂等 key begin 返回已终态（无 lease/短证）→ typed 解码为 BeginOutcome
  .status（不强制重传）。
P2-DEADLINE：_Budget 真实单调钟预算——耗尽后不再发起新网络调用；wait/
  upload/discovery 均接预算；RFC3339 用真实日历解析（fromisoformat+UTC
  偏移校验，拒绝 2026-13-45 等无效时间戳）。真实 transport 每请求超时穿透
  归 D 线（真实 HTTP 预算测试）。
契约澄清（返修版）：temp_key 与 final **前向/后向重叠均拒**（segment
  boundary——私有 staging 命名空间与 users/ap-tool final 物理隔离是总约束，
  等于/祖先只是最低检查，后代同样拒绝）。
"""
from __future__ import annotations

import hashlib
import os
import stat
import re
import time
import uuid as _uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import urlencode, urlsplit

from ..errors import (BizCodeError, RequestDeadlineExceeded,
                       SchemaError, TransportError)

#: 协议常量（定稿字符串）。
PROTOCOL = "dual-object-v1"

# ── ReplicasPolicy（0842 裁决定稿：trusted expected replica policy）──
#
# V3-PACKAGE-POLICY 正式闭合：删除拆字串常量——公共包源码**零内网业务
# 标识**（非混淆）；期望桶对经三个途径进入：
#   ① 显式构造参数（公共 SDK 可用——非 private build 许可证）；
#   ② ``_site_defaults.EXPECTED_REPLICA_POLICY_JSON``（内网构建注入，
#      源码恒为空串；无 envvar 通道）；
#   ③ 缺失 → 新客户端零 IO typed error（fail-closed，不猜）。
# 优先级：显式有效 > site 注入 > 缺失；**显式 invalid 不 fallback**。

from types import MappingProxyType
from typing import Mapping


class ReplicasPolicy:
    """typed 不可变期望 replica policy（构造即验证+deep copy/freeze）。

    - ``storage_id``：非空字符串；
    - ``buckets``/``oss_regions``：**恰 cn+sg 两键**全字段必填（部分=
      typed SchemaError）；值非空字符串；
    - 构造时 deep copy 入 ``MappingProxyType``（不可变快照——外部 dict
      后续修改不影响 policy）；
    - 错误消息**不含 raw values**（固定 field/region 名——防注入回显）；
    - JSON parser（site 注入值）用同一验证路径（严格解析/拒重复 keys/
      小配置有界）。

    用法（AP 私有 CLI）：用**已审私有 canonical constants**在 discovery
    **前**构造（不从同一未验证 discovery 响应造锚）。
    """

    __slots__ = ("_storage_id", "_buckets", "_oss_regions")

    def __init__(self, storage_id, buckets, oss_regions) -> None:
        # 修4：storage_id **严格 string 校验**——不做 str() 转换（任意
        # 对象不得被静默字符串化后通过）。
        if not isinstance(storage_id, str) or not storage_id:
            raise SchemaError(
                "ReplicasPolicy: storage_id must be a nonempty str")
        object.__setattr__(self, "_storage_id", storage_id)
        for name, src, attr in (("buckets", buckets, "_buckets"),
                                ("oss_regions", oss_regions,
                                 "_oss_regions")):
            # 修4：接受 **Mapping 协议**类型（dict/MappingProxyType 等
            # Mapping 实现），非仅 dict；非 Mapping 拒。
            if not isinstance(src, Mapping):
                raise SchemaError(
                    f"ReplicasPolicy: {name} must be a Mapping")
            if set(src) != set(_REGIONS):
                raise SchemaError(
                    f"ReplicasPolicy: {name} must contain exactly "
                    f"cn and sg keys (partial or extra keys rejected)")
            copied = {}
            for r in _REGIONS:
                v = src[r]
                if not isinstance(v, str) or not v:
                    raise SchemaError(
                        f"ReplicasPolicy: {name}[{r!r}] must be a "
                        "nonempty string")
                copied[r] = v
            object.__setattr__(self, attr,
                               MappingProxyType(copied))

    # frozen 语义：__setattr__ 拒绝（构造后不可变）。
    def __setattr__(self, name, value):
        raise SchemaError("ReplicasPolicy is immutable")

    def __delattr__(self, name):
        raise SchemaError("ReplicasPolicy is immutable")

    @property
    def storage_id(self) -> str:
        return self._storage_id

    @property
    def buckets(self):
        return self._buckets

    @property
    def oss_regions(self):
        return self._oss_regions

    def bucket(self, region: str) -> str:
        return self._buckets[region]

    def oss_region(self, region: str) -> str:
        return self._oss_regions[region]

    def __eq__(self, other) -> bool:
        if not isinstance(other, ReplicasPolicy):
            return NotImplemented
        return (self._storage_id == other._storage_id
                and dict(self._buckets) == dict(other._buckets)
                and dict(self._oss_regions) == dict(other._oss_regions))

    def __hash__(self):
        return hash((self._storage_id,
                     tuple(sorted(self._buckets.items())),
                     tuple(sorted(self._oss_regions.items()))))

    def __repr__(self) -> str:      # safe：无秘密字段（policy 本身公开）
        return (f"ReplicasPolicy(storage_id={self._storage_id!r}, "
                f"buckets=<cn/sg>, oss_regions=<cn/sg>)")


def _parse_replica_policy_json(raw: str) -> ReplicasPolicy:
    """site 注入 JSON → ReplicasPolicy（严格解析/拒重复 keys/小配置
    有界；错误不含 raw values）。"""
    if not isinstance(raw, str) or not raw:
        raise SchemaError(
            "expected replica policy JSON is empty (site default not "
            "injected and no explicit policy supplied)")
    if len(raw) > 4096:
        raise SchemaError(
            "expected replica policy JSON exceeds bounded size")
    import json
    # 修5：严格 JSON——parse_constant 拒 NaN/Infinity（json.loads 默认
    # 接受非标准常量）。
    def _reject_constants(value):
        raise SchemaError(
            "expected replica policy JSON: non-standard constant "
            "rejected")
    parsed = None
    invalid_json = False
    try:
        # object_pairs_hook：显式检测重复 keys（json.loads 默认静默
        # 覆盖——严格模式须拒绝）。修5：重复 key 的错误消息**不可回显
        # raw key**（固定文案，防把注入串带进异常/日志）。
        def _no_dupes(pairs):
            d = {}
            for k, val in pairs:
                if k in d:
                    raise SchemaError(
                        "expected replica policy JSON: duplicate key "
                        "rejected")
                d[k] = val
            return d
        parsed = json.loads(raw,
                            object_pairs_hook=_no_dupes,
                            parse_constant=_reject_constants)
    except SchemaError:
        raise
    except ValueError:
        invalid_json = True
    if invalid_json:
        raise SchemaError("expected replica policy JSON: invalid JSON")
    if not isinstance(parsed, dict):
        raise SchemaError("expected replica policy JSON: not an object")
    # 修5：未知顶层字段拒绝（严格 schema——只允许三键）。
    unknown = set(parsed) - {"storage_id", "buckets", "oss_regions"}
    if unknown:
        raise SchemaError(
            "expected replica policy JSON: unknown top-level field "
            "rejected")
    buckets = parsed.get("buckets")
    oss_regions = parsed.get("oss_regions")
    storage_id = parsed.get("storage_id")
    try:
        return ReplicasPolicy(storage_id, buckets, oss_regions)
    except SchemaError:
        raise


def _resolve_replica_policy(explicit
                            ) -> "ReplicasPolicy | None":
    """优先级：显式有效 > site 注入 > 缺失（None）。

    修2：**显式参数 IO 前 isinstance 校验**——非 ReplicasPolicy/None
    （如 int）立即 typed 拒（零网络调用、不 fallback、不做属性探测式
    延迟失败）。显式 ReplicasPolicy 本身在构造时已验证。
    """
    if explicit is not None and not isinstance(explicit, ReplicasPolicy):
        raise SchemaError(
            "expected_replica_policy must be a ReplicasPolicy instance "
            "or None")
    if explicit is not None:
        return explicit
    from .. import _site_defaults
    raw = getattr(_site_defaults, "EXPECTED_REPLICA_POLICY_JSON", "")
    if not isinstance(raw, str) or not raw:
        return None
    return _parse_replica_policy_json(raw)

ERROR_FAMILY = {
    94100: "storage_cluster_unknown",
    94101: "storage_dual_unavailable",
    94102: "user_data_write_invalid",
    94103: "user_data_write_pending",
    94104: "user_data_write_partial",
    94105: "user_data_write_conflict",
    94106: "user_data_upgrade_required",
    94107: "user_data_write_stale_fence",
    94108: "user_data_write_digest_mismatch",
    94109: "user_data_write_not_found",
}

#: 状态 allowlist（P1-5：未知状态拒绝——保守集，A 侧扩展须同步）。
STATUS_ALLOWLIST = ("active", "pending", "partial", "committed",
                    "conflict", "failed")

_UUID_RE = re.compile(
    r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")
_SHA256_RE = re.compile(r"[0-9a-f]{64}")
_RFC3339_RE = re.compile(
    r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})")
#: op_id：严格单段（拒 dot/dotdot/query/fragment/编码分隔符/斜杠）。
_OP_ID_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_-]{0,127}")
#: 错误 data 值校验用的 op_id 形态（更严：仅小写——防服务器在安全键
#: 下塞任意大小写 canary 串）。
_OP_ID_STRICT_RE = re.compile(r"[a-z0-9][a-z0-9_-]{0,127}")
_HOSTNAME_RE = re.compile(r"[a-z0-9][a-z0-9.-]*[a-z0-9]|[a-z0-9]")
_REGIONS = ("cn", "sg")

#: 流式分块（1MiB；无 8GiB 上限——users 域容量由服务端 begin 显式返回）。
_CHUNK_BYTES = 1024 * 1024


# ── typed 异常（94100..94109）─────────────────────────────────────────

class UserDataWriteError(BizCodeError):
    """users 域双写错误。str/repr 只含 code/error_code/status 与净化后
    data——**凭据、lease token、签名 URL、服务器敏感 message 永不出现**。"""
    code = "E_USERDATA_WRITE"
    error_code = "user_data_write_invalid"

    def __init__(self, message: str = "", *, status: int | None = None,
                 biz_code: int | None = None, error_code: str = "",
                 data: dict | None = None) -> None:
        super().__init__(message, status=status, biz_code=biz_code,
                         data=data)
        self.error_code = error_code or self.error_code


class StorageClusterUnknown(UserDataWriteError):
    code = "E_STORAGE_CLUSTER_UNKNOWN"; error_code = "storage_cluster_unknown"


class StorageDualUnavailable(UserDataWriteError):
    code = "E_STORAGE_DUAL_UNAVAILABLE"
    error_code = "storage_dual_unavailable"


class UserDataWriteUnauthorized(UserDataWriteError):
    """Known users-domain auth denial; exact numeric 94022/10003 only."""
    code = "E_USERDATA_WRITE_UNAUTHORIZED"
    error_code = "user_data_write_unauthorized"


class UserDataWriteInvalid(UserDataWriteError):
    code = "E_USERDATA_WRITE_INVALID"; error_code = "user_data_write_invalid"


class UserDataWritePending(UserDataWriteError):
    code = "E_USERDATA_WRITE_PENDING"; error_code = "user_data_write_pending"


class UserDataWritePartial(UserDataWriteError):
    code = "E_USERDATA_WRITE_PARTIAL"; error_code = "user_data_write_partial"


class UserDataWriteConflict(UserDataWriteError):
    code = "E_USERDATA_WRITE_CONFLICT"; error_code = "user_data_write_conflict"


class UserDataUpgradeRequired(UserDataWriteError):
    code = "E_USERDATA_UPGRADE_REQUIRED"
    error_code = "user_data_upgrade_required"


class UserDataWriteStaleFence(UserDataWriteError):
    code = "E_USERDATA_WRITE_STALE_FENCE"
    error_code = "user_data_write_stale_fence"


class UserDataWriteDigestMismatch(UserDataWriteError):
    code = "E_USERDATA_WRITE_DIGEST_MISMATCH"
    error_code = "user_data_write_digest_mismatch"


class UserDataWriteNotFound(UserDataWriteError):
    code = "E_USERDATA_WRITE_NOT_FOUND"; error_code = "user_data_write_not_found"


_ERROR_CODE_TO_EXC = {c.error_code: c for c in (
    StorageClusterUnknown, StorageDualUnavailable, UserDataWriteInvalid,
    UserDataWritePending, UserDataWritePartial, UserDataWriteConflict,
    UserDataUpgradeRequired, UserDataWriteStaleFence,
    UserDataWriteDigestMismatch, UserDataWriteNotFound)}



def _sanitize_error_data(data, *,
                         bound_op_id: str | None = None) -> dict:
    """项2（V5-ERRORS）：服务器 data **只保留请求已知绑定字段**——
    不再靠词表正则猜（"任意合法形状 op_id"也是不可信服务器串）。

    - ``op_id``：仅当与**本请求已知绑定**（bound_op_id，来自发起的
      请求 URL/op 绑定）逐字相等才保留；其余一律丢弃（含其它合法
      形状——非本 op 的 ID 对调用方无用且不可信）；
    - ``failed/succeeded_targets``：恰含 cn/sg（结构性枚举，无自由
      文本面）保留；
    - ``generation``：仅当与请求绑定 generation 相等才保留（未绑定
      不保留）；
    - ``status``/``error_code`` 等其余键：**删除**（服务器自报状态与
      码不是可信诊断面——权威分类已在异常类型上）。
    """
    if not isinstance(data, dict):
        return {}
    out = {}
    if bound_op_id is not None:
        v = data.get("op_id")
        if isinstance(v, str) and v == bound_op_id:
            out["op_id"] = v
    for key in ("failed_targets", "succeeded_targets"):
        v = data.get(key)
        if (isinstance(v, list) and v
                and all(isinstance(x, str) and x in _REGIONS for x in v)
                and len(set(v)) == len(v)):
            out[key] = list(v)
    return out


def map_user_data_write_error(exc: TransportError, *,
                              bound_op_id: str | None = None
                              ) -> TransportError:
    """941xx 信封→typed 异常。

    D3（B-V3-ERRORS）：
    - **数字 941xx 权威**：biz_code 可映射时以数字为准；服务器
      data.error_code 与之**矛盾**（非该数字族的词表成员）→ 视为不可信
      串，按数字族映射（矛盾 symbolic 不覆盖权威数字）；
    - message 用类固定 token；data 值词表校验；
    - **未知错误**（无 941xx 映射）：返回泛化 safe type（
      UserDataWriteInvalid 带 biz_code=None、message 不含服务器串）——
      不原样透传含 raw message/data 的原异常（调用方拿不到服务器
      message；诊断经结构化字段 request_id/code，由 transport 既有
      机制承载）；
    - 调用方**不得**再以 ``raise ... from exc`` 链回 raw（traceback
      披露面）——本模块各调用点已改为直接 raise。
    """
    biz = getattr(exc, "biz_code", None)
    # 修2（0925）：识别**共同** safe 本地类型 RequestDeadlineExceeded
    # （非仅客户端 subclass）——transport/retry 层抛的预算信号原样透传
    # （无服务器数据，勿泛化为 UserDataWriteInvalid、无 raw 透传面）。
    if isinstance(exc, RequestDeadlineExceeded):
        return exc
    # Users auth is a distinct numeric domain, never inferred from shared94040
    # or a server-controlled symbolic hint. Preserve old catchbase and status.
    if type(biz) is int and biz in (94022, 10003):
        return UserDataWriteUnauthorized(
            "user-data write authorization denied",
            status=getattr(exc, "status", None), biz_code=biz, data={})
    err_code = (exc.data or {}).get("error_code") if exc.data else None
    cls = None
    # 数字 941xx 权威：先按数字定类；symbolic 仅在数字不可映射或与
    # 数字族一致时采纳（矛盾 symbolic 不采纳）。
    if isinstance(biz, int):
        name = ERROR_FAMILY.get(biz)
        if name:
            cls = _ERROR_CODE_TO_EXC.get(name)
    if cls is None and isinstance(err_code, str):
        # 数字不可映射：symbolic 可用（但必须是词表成员——未知串
        # 不映射，走未知分支）。
        cls = _ERROR_CODE_TO_EXC.get(err_code)
    if cls is not None:
        status = getattr(exc, "status", None)
        fixed_token = cls.error_code
        message = f"user-data write error: {fixed_token}"
        if isinstance(status, int):
            message += f" (HTTP {status})"
        mapped = cls(message, status=status, biz_code=biz,
                     error_code=fixed_token,
                     data=_sanitize_error_data(exc.data,
                                        bound_op_id=bound_op_id))
        return mapped
    # 未知错误：泛化 safe type（不透传 raw message/data）。
    status = getattr(exc, "status", None)
    generic = UserDataWriteInvalid(
        "user-data write error: unclassified transport failure"
        + (f" (HTTP {status})" if isinstance(status, int) else ""),
        status=status, biz_code=None,
        error_code="user_data_write_invalid", data=None)
    return generic


# ── 本地输入校验（拒绝而非清洗；不二次解码）──────────────────────────

def validate_owner(owner: str) -> str:
    v = str(owner or "")
    if not v:
        raise SchemaError("owner must not be empty")
    if v in (".", ".."):
        raise SchemaError("owner must not be a dot segment")
    if v != v.strip() or any(ord(c) < 0x20 for c in v):
        raise SchemaError(f"invalid owner {owner!r}")
    if "/" in v or "\\" in v or any(c.isspace() for c in v):
        raise SchemaError(f"invalid owner {owner!r}")
    return v


def validate_relative_path(path: str) -> str:
    p = str(path or "")
    if not p:
        raise SchemaError("relative_path must not be empty")
    if p.startswith("/") or p.startswith("\\"):
        raise SchemaError(
            f"invalid relative_path {p!r}: leading slash/backslash")
    if any(ord(c) < 0x20 for c in p):
        raise SchemaError("invalid relative_path: control char")
    for seg in p.split("/"):
        if seg in ("", ".", ".."):
            raise SchemaError(
                f"invalid relative_path {p!r}: empty/dot/parent segment")
    return p


def validate_idempotency_key(key: str) -> str:
    v = str(key or "")
    if not _UUID_RE.fullmatch(v):
        raise SchemaError(
            "invalid idempotency_key: must be canonical lowercase UUID "
            "with hyphens (e.g. 550e8400-e29b-41d4-a716-446655440000)")
    return v


def new_idempotency_key() -> str:
    return str(_uuid.uuid4())


def _validate_op_id(op_id: str) -> str:
    """P1-5：严格单段 op_id——拒 dot（含 '.'/'..'）/query/fragment/编码
    分隔符/斜杠。复用于 begin 解析、status、commit URL、wait。"""
    v = str(op_id or "")
    if not _OP_ID_RE.fullmatch(v):
        raise SchemaError(
            f"invalid op_id {op_id!r}: must be a single safe segment "
            "(alphanumeric, '_', '-'; no dots, slashes, query, fragment "
            "or encoded separators)")
    return v


def _derive_users_key(owner: str, relative_path: str) -> str:
    return f"swe/user-data/users/{owner}/{relative_path}"


# ── 结构化校验 helpers ────────────────────────────────────────────────

def _validate_https_endpoint(endpoint: str, what: str) -> str:
    """P1-2：结构化 HTTPS 校验并归一化（返回 ``https://host[:port]``）。

    校验：scheme=https；hostname 非空且结构合法（无 userinfo）；port 合法
    （1..65535，443 归一省略）；**path 为空或 '/'**；无 query/fragment。
    拒绝：http、userinfo、任意 path、query、fragment、坏端口。"""
    u = None
    try:
        u = urlsplit(str(endpoint or ""))
        port = u.port
    except ValueError:
        u = None
    if u is None:
        raise SchemaError(f"{what}: invalid URL structure")
    if u.scheme != "https":
        raise SchemaError(f"{what} must be https, got {u.scheme!r}")
    host = (u.hostname or "").lower()
    if not host:
        raise SchemaError(f"{what}: missing hostname")
    if u.username is not None or u.password is not None:
        raise SchemaError(f"{what}: userinfo not allowed")
    if u.path not in ("", "/"):
        raise SchemaError(f"{what}: path component not allowed")
    if u.query or u.fragment:
        raise SchemaError(f"{what}: query/fragment not allowed")
    if port is not None and not (1 <= port <= 65535):
        raise SchemaError(f"{what}: invalid port {port}")
    if not _HOSTNAME_RE.fullmatch(host):
        raise SchemaError(f"{what}: invalid hostname structure")
    netloc = host if port in (None, 443) else f"{host}:{port}"
    return f"https://{netloc}"


def _validate_regional_oss_endpoint(endpoint: str, oss_region: str) -> str:
    """Bind credential destinations to the caller-trusted OSS region."""
    normalized = _validate_https_endpoint(endpoint, "replica endpoint")
    parsed = urlsplit(normalized)
    if parsed.hostname not in {
            f"oss-{oss_region}.aliyuncs.com",
            f"oss-{oss_region}-internal.aliyuncs.com"} or (parsed.port or 443) != 443:
        raise SchemaError("replica endpoint does not bind trusted OSS region")
    return normalized


def _validate_rfc3339_utc(value: str, what: str) -> str:
    """P2：RFC3339 **真实日历解析**（拒绝 2026-13-45T99:99:99Z 等无效
    时间戳）+ UTC 偏移强制（Z/+00:00；非零偏移拒绝）。"""
    v = str(value or "")
    if not _RFC3339_RE.fullmatch(v):
        raise SchemaError(f"{what} must be RFC3339 UTC")
    from ._rfc3339 import parse_utc
    dt = None
    try:
        dt = parse_utc(v)
    except ValueError:
        pass
    if dt is None:
        raise SchemaError(f"{what}: invalid calendar datetime")
    if dt.tzinfo is None or dt.utcoffset() != timedelta(0):
        raise SchemaError(f"{what} must carry UTC offset (Z or +00:00)")
    return v


def _refuse_temp_key_vs_final(temp_key: str, final_key: str) -> None:
    """契约澄清（返修版）：temp_key 与 final **前向/后向重叠均拒**
    （segment boundary）。

    wire 总约束=私有 op staging 命名空间与 users/ap-tool final 路径物理
    隔离——等于/祖先只是最低检查；**final 的后代同样拒绝**（撤销早先
    "后代不拒"的误判）。"""
    t, f = str(temp_key), str(final_key)
    for namespace in ("swe/user-data/users", "swe/user-data/ap-tool"):
        if t == namespace or t.startswith(namespace + "/"):
            raise SchemaError("temp_key must not target a final object namespace")
    if t == f:
        raise SchemaError("temp_key overlaps final key (equal)")
    t_p = t.rstrip("/") + "/"
    f_p = f.rstrip("/") + "/"
    if f.startswith(t_p) or t.startswith(f_p):
        raise SchemaError(
            "temp_key overlaps final key namespace (ancestor/descendant)")


@dataclass(frozen=True)
class _SourceIdentity:
    device: int
    inode: int
    size: int
    mtime_ns: int
    ctime_ns: int

    @classmethod
    def from_stat(cls, value):
        return cls(value.st_dev, value.st_ino, value.st_size,
                   value.st_mtime_ns, value.st_ctime_ns)


def _source_changed():
    return UserDataWriteDigestMismatch(
        "local upload source identity or content changed", biz_code=94108,
        error_code="user_data_write_digest_mismatch")


class _RegularSource:
    """Sequential bounded reads from a regular file, following regular symlinks.

    Cooperative guards cannot interrupt an arbitrary in-flight filesystem syscall.
    No executor is used; a late read is rejected before hashing or another IO.
    """
    def __init__(self, stream, identity, budget):
        self._stream, self.identity, self._budget = stream, identity, budget
        self._count = 0

    def read(self, count=-1):
        self._budget.raise_if_exhausted()
        amount = _CHUNK_BYTES if count is None or count < 0 else min(count, _CHUNK_BYTES)
        block = self._stream.read(amount)
        self._budget.raise_if_exhausted()
        self._count += len(block)
        if not block or self._count >= self.identity.size:
            if _SourceIdentity.from_stat(os.fstat(self._stream.fileno())) != self.identity:
                raise _source_changed()
        self._budget.raise_if_exhausted()
        return block

    def fileno(self):
        return self._stream.fileno()

    def close(self):
        self._stream.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()


def _open_regular(path, *, budget=None, identity=None):
    """Never blocking-open a FIFO before fstat. No O_NOFOLLOW: file symlinks work."""
    shared = budget if budget is not None else _Budget(None)
    shared.raise_if_exhausted()
    fd = None
    failed = False
    try:
        fd = os.open(path, os.O_RDONLY | os.O_NONBLOCK)
    except OSError:
        failed = True
    if failed:
        raise SchemaError("cannot open regular upload source")
    try:
        shared.raise_if_exhausted()
        value = os.fstat(fd)
        if not stat.S_ISREG(value.st_mode):
            raise SchemaError("upload source must be a regular file")
        actual = _SourceIdentity.from_stat(value)
        if identity is not None and actual != identity:
            raise _source_changed()
        shared.raise_if_exhausted()
        stream = os.fdopen(fd, "rb")
        fd = None  # stream owns the descriptor from here
        return _RegularSource(stream, actual, shared)
    finally:
        if fd is not None:
            os.close(fd)


def _sha256_file(path: Path, *, budget=None, identity=None) -> str:
    """SHA256 in <=1MiB reads, sharing the caller's absolute operation budget."""
    shared = budget if budget is not None else _Budget(None)
    h = hashlib.sha256()
    with _open_regular(path, budget=shared, identity=identity) as source:
        while True:
            shared.raise_if_exhausted()
            block = source.read(_CHUNK_BYTES)
            if not block:
                break
            h.update(block)
            shared.raise_if_exhausted()
    shared.raise_if_exhausted()
    return h.hexdigest()


class _DeadlineExhausted(RequestDeadlineExceeded):
    """预算耗尽信号（pre-IO 本地抛出，不携带任何服务器数据——不需要
    脱敏，且不得被 map_user_data_write_error 归为 unclassified 而掩盖
    语义）。

    0842：subclass 共同 safe ``RequestDeadlineExceeded``（errors.py，
    transport/retry 层共享）——**正向** import（client→errors，允许）；
    transport/retry 不 import client（方向纪律）。"""


class _Budget:
    """R4（B-DEADLINE-REMAINING）：**绝对单调 deadline**——公共时长参数
    一次派生，穿透每次真实控制面 HTTP（pre/post 检查+per-request 剩余量
    传参）与 sleep。**0 预算=零调用，无首调用豁免**。"""

    def __init__(self, total_seconds: float | None) -> None:
        self._deadline = (time.monotonic() + max(0.0, total_seconds)
                          if total_seconds is not None else None)

    @property
    def exhausted(self) -> bool:
        return (self._deadline is not None
                and time.monotonic() >= self._deadline)

    def raise_if_exhausted(self) -> None:
        if self.exhausted:
            raise _DeadlineExhausted(
                "user-data write deadline exhausted before network call")

    def remaining_seconds(self) -> float | None:
        """当前剩余量（无预算=None=不限制）；供 per-request timeout 传参。"""
        if self._deadline is None:
            return None
        return max(0.0, self._deadline - time.monotonic())

    def deadline(self) -> float | None:
        """绝对单调时刻（供 D 侧合同 budget_deadline 传参；None=不限）。"""
        return self._deadline

    def sleep_bound(self, backoff: float) -> None:
        if self._deadline is None:
            time.sleep(max(0.0, backoff))
            return
        remaining = self._deadline - time.monotonic()
        if remaining > 0:
            time.sleep(min(max(0.0, backoff), remaining))


def _transport_supports_timeout(transport, method: str) -> bool:
    """D2（B-V3-TYPEERROR）+ 0740 提示：**按实际方法**（GET/POST 各自）
    的可调用签名做 IO 前能力探测——绝不靠执行后 TypeError 重放（那会
    造成隐式重复控制面写+丢预算）。

    inspect 无 IO 无副作用；对应方法签名含 ``timeout`` 参数才传
    per-request 剩余量，否则该方法按原形态调用（预算边界仍由
    pre/post 检查保证）。"""
    import inspect
    fn = getattr(transport, method.lower(), None)
    if not callable(fn):
        return False
    try:
        sig = inspect.signature(fn)
    except (TypeError, ValueError):
        return False
    return "timeout" in sig.parameters


def _put_supports_budget(put_fn) -> bool:
    """项3：IO 前探测 D 注入面是否接受 ``budget_deadline``（V5 合同）——
    与 _transport_supports_timeout 同纪律（inspect 签名，无执行探测）。"""
    import inspect
    try:
        sig = inspect.signature(put_fn)
    except (TypeError, ValueError):
        return False
    return "budget_deadline" in sig.parameters


def _call_with_budget(budget: "_Budget", transport, method: str, path: str,
                      body=None):
    """D1/D2（0740 提示修正）：**执行一次→成功 postcheck→return**——
    不重放、不以 finally 错误覆盖原鉴权/传输错误；0 预算=零调用；
    per-request 剩余量作 timeout（IO 前能力探测，D2 无执行后 TypeError
    重放）。

    成功后 post-check：响应到达但总预算已耗尽（传输吃完了预算）——
    该响应仍按耗尽语义处理（raise _DeadlineExhausted），**不静默接受
    超预算成功**；传输中途错误（鉴权/网络原错误）原样上抛，post 检查
    不覆盖。"""
    budget.raise_if_exhausted()
    remaining = budget.remaining_seconds()
    if method == "GET":
        if _transport_supports_timeout(transport, method):
            resp = transport.get(path, timeout=remaining)
        else:
            resp = transport.get(path)
    else:
        if _transport_supports_timeout(transport, method):
            resp = transport.post(path, body, timeout=remaining)
        else:
            resp = transport.post(path, body)
    # 成功后 post-check（执行恰一次；不重放、不覆盖原错误路径）。
    budget.raise_if_exhausted()
    return resp


# ── typed dataclasses（secret 字段 repr=False——P1-1）─────────────────

@dataclass(frozen=True)
class StorageReplica:
    region: str
    bucket: str
    endpoint: str            # 归一化 https://host[:port]
    oss_region: str


@dataclass(frozen=True)
class StorageLayout:
    schema_version: int
    storage_id: str
    cluster: str
    root_prefix: str
    primary_region: str
    replicas: dict
    capabilities: tuple

    @property
    def write_ready(self) -> bool:
        return PROTOCOL in self.capabilities


@dataclass(frozen=True)
class WriteTarget:
    region: str
    bucket: str
    endpoint: str              # 归一化（已与 discovery 比对一致）
    region_id: str
    temp_key: str
    upload_attempt: str
    access_key_id: str = field(repr=False)
    access_key_secret: str = field(repr=False)
    security_token: str = field(repr=False)
    expiration: str = field(repr=False)


@dataclass(frozen=True)
class BeginWriteResult:
    op_id: str
    generation: int
    protocol: str
    storage_id: str
    canonical_key: str
    targets: dict
    fencing_token: str = field(repr=False)
    lease_expires_at: str
    # P1-3：请求内容绑定（handle 保留 begin 输入，不可变）。
    expected_sha256: str
    expected_size: int
    owner: str
    relative_path: str
    primary_region: str
    idempotency_key: str

    def target(self, region: str) -> WriteTarget:
        return self.targets[region]


@dataclass(frozen=True)
class StatusResult:
    op_id: str
    generation: int
    protocol: str
    storage_id: str
    canonical_key: str
    status: str

    @property
    def committed(self) -> bool:
        return self.status == "committed"


@dataclass(frozen=True)
class BeginOutcome:
    """begin 的结果形态：active 写（write）/幂等 committed 回执
    （receipt）/其它终态信息（status——非成功语义，仅决策参考）。

    R2：committed 回执=完整验证（digest/size/两 final 比对通过）才出现
    在 receipt；status 只是 A 侧 read-only 元数据的信息用途，不得当上传
    成功。"""
    write: BeginWriteResult | None = None
    receipt: CommitWriteResult | None = None
    status: StatusResult | None = None

    @property
    def active(self) -> bool:
        return self.write is not None

    @property
    def committed(self) -> bool:
        return self.receipt is not None


class _BeginTerminalStatus(Exception):
    """begin 幂等分支的非 committed 终态（内部信号→BeginOutcome.status）。"""
    def __init__(self, status: "StatusResult") -> None:
        super().__init__("terminal op status via idempotent begin")
        self.status = status


@dataclass(frozen=True)
class _RequestBinding:
    """R1：网络调用前从本地已验证实参构造的不可变请求绑定。

    parser 显式接收本对象——expected_* 的唯一权威来源是**本地输入**，
    服务端 echo 字段可选且出现即精确匹配。"""
    owner: str
    relative_path: str
    sha256: str
    size: int
    idempotency_key: str
    storage_id: str
    primary_region: str


@dataclass(frozen=True)
class CommitWriteResult:
    op_id: str
    generation: int
    protocol: str
    storage_id: str
    canonical_key: str
    sha256: str
    size: int
    final: dict
    status: str = "committed"


# ── 严格解码 helpers ──────────────────────────────────────────────────

def _req_str(d: dict, key: str, what: str) -> str:
    v = d.get(key)
    if not isinstance(v, str) or not v:
        raise SchemaError(f"response missing nonempty {what!r}")
    return v


def _req_int(d: dict, key: str, what: str, *, minimum: int | None = None,
             allow_zero: bool = False) -> int:
    v = d.get(key)
    if isinstance(v, bool) or not isinstance(v, int):
        raise SchemaError(f"response field {what!r} must be an integer")
    if minimum is not None and v < minimum:
        raise SchemaError(f"response field {what!r} must be >= {minimum}")
    if v < 0 or (v == 0 and not allow_zero):
        raise SchemaError(
            f"response field {what!r} must be a nonnegative integer")
    return v


def _req_rfc3339(d: dict, key: str, what: str) -> str:
    return _validate_rfc3339_utc(_req_str(d, key, what), what)


def _parse_status_fields(resp: dict) -> StatusResult:
    """status 形态解码（status/幂等 begin 终态共用）：op/generation/
    protocol/storage_id/canonical_key/status 全必填+校验。"""
    op_id = _validate_op_id(_req_str(resp, "op_id", "op_id"))
    generation = _req_int(resp, "generation", "generation", minimum=1)
    protocol = _req_str(resp, "protocol", "protocol")
    if protocol != PROTOCOL:
        raise SchemaError(f"unexpected protocol {protocol!r}")
    storage_id = _req_str(resp, "storage_id", "storage_id")
    canonical_key = _req_str(resp, "canonical_key", "canonical_key")
    status = _req_str(resp, "status", "status")
    if status not in STATUS_ALLOWLIST:
        raise SchemaError(f"unknown op status {status!r}")
    return StatusResult(op_id=op_id, generation=generation,
                        protocol=protocol, storage_id=storage_id,
                        canonical_key=canonical_key, status=status)


# ── discovery client ──────────────────────────────────────────────────

class UserDataStorageLayoutClient:
    """discovery（GET /apis/v1/user-data/storage-layout?cluster=…）。"""

    def __init__(self, transport, *,
                 expected_replica_policy: "ReplicasPolicy | None" = None
                 ) -> None:
        self._t = transport
        # 0842 定稿：显式有效 > site 注入 > 缺失；显式 invalid 已在调用
        # 方构造时抛（ReplicasPolicy 构造即验证，不 fallback）。
        self._policy = _resolve_replica_policy(expected_replica_policy)

    @property
    def replica_policy(self) -> "ReplicasPolicy | None":
        return self._policy

    def _require_policy(self) -> "ReplicasPolicy":
        if self._policy is None:
            # 缺失 policy：新客户端零 IO typed error（fail-closed 不猜）。
            raise UserDataUpgradeRequired(
                "no expected replica policy configured: pass "
                "expected_replica_policy (or inject site default); "
                "refusing to trust unverified discovery",
                status=None, biz_code=94106,
                error_code="user_data_upgrade_required", data=None)
        return self._policy

    def get_storage_layout(self, cluster: str, *,
                           deadline: float | None = None,
                           budget: "_Budget | None" = None
                           ) -> StorageLayout:
        """D1：接受共享 budget 对象（编排方一次派生穿透）或独立 deadline
        （直接调用）；0 预算=零调用（无豁免）。

        0842：**policy 缺失=零 IO typed error**（不信任未验证 discovery）。"""
        policy = self._require_policy()        # IO 前（零网络调用即拒）
        c = str(cluster or "")
        if not c:
            raise SchemaError("cluster must not be empty")
        shared = budget if budget is not None else _Budget(deadline)
        safe_error = None
        try:
            resp = _call_with_budget(
                shared, self._t, "GET",
                "/apis/v1/user-data/storage-layout?"
                + urlencode({"cluster": c}))
        except TransportError as exc:
            safe_error = map_user_data_write_error(exc)
        if safe_error is not None:
            raise safe_error
        return self._parse_layout(resp, requested_cluster=c,
                                   policy=policy)

    @staticmethod
    def _parse_layout(resp, *, requested_cluster: str,
                      policy: "ReplicasPolicy") -> StorageLayout:
        if not isinstance(resp, dict):
            raise SchemaError("storage-layout response must be an object")
        sv = resp.get("schema_version")
        if isinstance(sv, bool) or not isinstance(sv, int) or sv != 1:
            raise SchemaError(
                "storage-layout schema_version must be strict int 1")
        cluster = _req_str(resp, "cluster", "cluster")
        if cluster != requested_cluster:
            raise SchemaError(
                f"storage-layout cluster echo mismatch: requested "
                f"{requested_cluster!r}, echoed {cluster!r}")
        storage_id = _req_str(resp, "storage_id", "storage_id")
        # 修1：storage_id 与 expected policy **逐字校验**（"wrong-storage"
        # 即使桶/region 匹配也拒——probe 实证修正）。其后 begin/status/
        # final 的 storage_id 同源绑定（各自与本请求 policy 比对）。
        if storage_id != policy.storage_id:
            raise SchemaError(
                "storage-layout storage_id does not match expected "
                "replica policy")
        root = _req_str(resp, "root_prefix", "root_prefix")
        if root != "swe/user-data/":
            raise SchemaError(
                f"storage-layout root_prefix must be 'swe/user-data/', "
                f"got {root!r}")
        primary = _req_str(resp, "primary_region", "primary_region")
        if primary not in _REGIONS:
            raise SchemaError(f"invalid primary_region {primary!r}")
        reps = resp.get("replicas")
        if not isinstance(reps, dict) or set(reps) != set(_REGIONS):
            raise SchemaError(
                "storage-layout replicas must be exactly cn+sg records")
        parsed = {}
        for r in _REGIONS:
            rec = reps[r]
            if not isinstance(rec, dict):
                raise SchemaError(f"replicas[{r!r}] must be an object")
            bucket = _req_str(rec, "bucket", f"replicas.{r}.bucket")
            endpoint = _validate_https_endpoint(
                _req_str(rec, "endpoint", f"replicas.{r}.endpoint"),
                f"replicas.{r}.endpoint")
            reg = _req_str(rec, "region", f"replicas.{r}.region")
            # 0842：与 policy 精确匹配（错误不含 raw values——固定
            # field/region 名）。
            if bucket != policy.bucket(r):
                raise SchemaError(
                    f"replicas.{r}.bucket does not match expected "
                    "replica policy")
            if reg != policy.oss_region(r):
                raise SchemaError(
                    f"replicas.{r}.region does not match expected "
                    "replica policy")
            endpoint = _validate_regional_oss_endpoint(endpoint, policy.oss_region(r))
            parsed[r] = StorageReplica(region=r, bucket=bucket,
                                       endpoint=endpoint, oss_region=reg)
        caps = resp.get("capabilities", [])
        if not isinstance(caps, list) or not all(
                isinstance(x, str) for x in caps):
            raise SchemaError("capabilities must be a list of strings")
        return StorageLayout(
            schema_version=sv, storage_id=storage_id, cluster=cluster,
            root_prefix=root, primary_region=primary, replicas=parsed,
            capabilities=tuple(caps))


# ── writes client ─────────────────────────────────────────────────────

def _is_terminal_upload_error(exc: BaseException) -> bool:
    """R5/D4（B-V3-CLASSIFICATION）：**未知一律终态**——仅**明确识别**
    的 transport/network 类才续 secondary。

    续 secondary（非终态）的**正向白名单**：
    - ``ConnectionError``/``TimeoutError``/``socket.timeout``（注意
      ECONNRESET 的 OSError 会被自动子类化为 ConnectionResetError——
      已被 ConnectionError 分支覆盖，与 errno 分支并存不矛盾）；
    - ``OSError`` 且 errno 在网络族（ENETUNREACH/EHOSTUNREACH/
      ECONNRESET/ECONNABORTED/ECONNREFUSED/ETIMEDOUT/ENETRESET/EPIPE）；
    - ``TransportError`` 且 status 为 5xx/网关类（**无 status=终态**：
      schema/未知语义不可续）。
    终态：UserDataWriteError/SchemaError/ValueError/NotImplementedError/
    厂商异常/TransportError 4xx（401/403/404/409…）/本地 OSError
    （PermissionError/IsADirectoryError/FileNotFoundError——非网络 errno）。
    与 D 的合同：D 侧 put_object_fn 须以 typed 异常表达网络类（映射到
    本白名单的族），未分类 vendor 异常一律按终态。"""
    if isinstance(exc, (UserDataWriteError, SchemaError)):
        return True
    # 1155 修①：消费 **D typed 错误族**（exact kind/status/retryable
    # 词表——UserDataUploadError 是 D r5 的安全契约类）：
    # - retryable=True（D 已识别网络瞬态：OutcomeUnknown/5xx）→ 续
    #   secondary（非终态）；
    # - retryable=False（auth/schema/digest/cancel/deadline/capacity/
    #   unknown/4xx）→ 终态；
    # - 无 raw traceback 披露（D 侧 __cause__ 已脱敏；B 按类名+kind
    #   归类不触原始消息）。
    from .user_data_upload import UserDataUploadError as _DUploadError
    if isinstance(exc, _DUploadError):
        return not bool(getattr(exc, "retryable", False))
    if isinstance(exc, TransportError):
        status = getattr(exc, "status", None)
        # D4：无 status=终态（generic/unknown 语义不可续）；5xx/网关类
        # =显式已知可续；4xx（含 401/403）=终态。
        if not isinstance(status, int):
            return True
        return not (500 <= status <= 599)
    if isinstance(exc, (ConnectionError, TimeoutError)):
        return False
    import socket
    if isinstance(exc, socket.timeout):
        return False
    if isinstance(exc, OSError):
        import errno
        # D4：正向白名单网络 errno 族（非本族=终态：本地文件/权限语义）。
        return exc.errno not in (errno.ENETUNREACH, errno.EHOSTUNREACH,
                                 errno.ECONNRESET, errno.ECONNABORTED,
                                 errno.ECONNREFUSED, errno.ETIMEDOUT,
                                 errno.ENETRESET, errno.EPIPE)
    return True          # 未知（ValueError/NotImplementedError/…）=终态


class UserDataWritesClient:
    """users 域双写客户端（isolated）。begin→upload（两 temp 流式）→
    commit（服务端实流核验+双 final 回读；客户端零自报）。"""

    def __init__(self, transport, *,
                 discovery: UserDataStorageLayoutClient | None = None,
                 put_object_fn=None,
                 expected_replica_policy: "ReplicasPolicy | None" = None
                 ) -> None:
        self._t = transport
        # 0842：两 client 共用同一 resolved policy（frozen）。
        # 修3（0925）：**一致绑定**——传入 discovery(policy=None)+显式
        # valid policy 时，把同一 immutable policy 绑定到两者（discovery
        # 侧补绑定；无 silent 忽略、无"后续合法配置被拒为 missing"）；
        # discovery 已带 policy 且与显式**不一致** → 构造期拒绝（矛盾
        # 组合不 IO）。
        if discovery is not None:
            if expected_replica_policy is not None and not isinstance(
                    expected_replica_policy, ReplicasPolicy):
                raise SchemaError(
                    "expected_replica_policy must be a ReplicasPolicy "
                    "instance or None")
            disc_policy = discovery.replica_policy
            if (expected_replica_policy is not None
                    and disc_policy is not None
                    and disc_policy != expected_replica_policy):
                raise SchemaError(
                    "conflicting replica policies: explicit "
                    "expected_replica_policy does not match the policy "
                    "already resolved in the passed discovery client; "
                    "refusing to silently ignore either")
            self._discovery = discovery
            if expected_replica_policy is not None:
                # 修3 核心：显式有效 + discovery None → **同一 policy
                # 绑定到 discovery**（discovery 后续校验不再 missing）。
                if disc_policy is None:
                    discovery._policy = expected_replica_policy
                self._policy = expected_replica_policy
            else:
                self._policy = disc_policy
        else:
            self._discovery = UserDataStorageLayoutClient(
                transport,
                expected_replica_policy=expected_replica_policy)
            self._policy = self._discovery.replica_policy
        # 上传注入点：(target, local_path, expected_size) -> None。
        # 真实 oss2 adapter 归 D 线（user_data_upload.py）——此处默认仅占位。
        self._put_object_fn = put_object_fn or _default_put_object

    @property
    def replica_policy(self) -> "ReplicasPolicy | None":
        return self._policy

    # ── begin ──
    def begin(self, *, owner: str, relative_path: str, sha256: str,
              size: int, overwrite: bool = False,
              idempotency_key: str = "",
              cluster: str = "",
              deadline: float | None = None) -> BeginOutcome:
        # Explicit routing identity is not inferred from Env or transport headers.
        # Validate before discovery so malformed identities perform zero IO.
        if (not isinstance(cluster, str) or not cluster
                or any(c.isspace() or ord(c) < 32 for c in cluster)):
            raise SchemaError("cluster must be an explicit nonempty string without whitespace")
        owner = validate_owner(owner)
        rel = validate_relative_path(relative_path)
        if not _SHA256_RE.fullmatch(str(sha256 or "")):
            raise SchemaError("sha256 must be 64 lowercase hex chars")
        if isinstance(size, bool) or not isinstance(size, int) or size < 0:
            raise SchemaError("size must be a nonnegative integer (not bool)")
        if not isinstance(overwrite, bool):
            raise SchemaError("overwrite must be bool")
        key = validate_idempotency_key(
            idempotency_key or new_idempotency_key())

        # D1（B-V3-DEADLINE）：**单一绝对 budget** 一次派生，同一对象
        # 穿透 discovery 与 begin POST（0.75s+0.75s 在总 1s 下不再各自
        # 独立计时）；0 预算=零调用（无首调用豁免）。
        budget = _Budget(deadline)
        layout = self._discovery.get_storage_layout(cluster,
                                                    budget=budget)
        if not layout.write_ready:
            raise StorageDualUnavailable(
                "storage layout does not advertise dual-object-v1 write "
                "capability", biz_code=94101,
                error_code="storage_dual_unavailable")

        # R1（B-REQUEST-BINDING）：不可变请求绑定——网络调用前从**本地
        # 已验证实参**构造；expected_* 永不来自服务端响应字段。
        binding = _RequestBinding(
            owner=owner, relative_path=rel, sha256=sha256, size=size,
            idempotency_key=key, storage_id=layout.storage_id,
            primary_region=layout.primary_region)
        body = {
            "protocol": PROTOCOL,
            "cluster": cluster,
            "owner": owner,
            "relative_path": rel,
            "sha256": sha256,
            "size": size,
            "overwrite": overwrite,
            "idempotency_key": key,
        }
        # D1：同一 budget 对象（含 discovery 已消耗量）继续穿透 begin
        # POST；0 预算/已耗尽=零调用。
        safe_error = None
        try:
            resp = _call_with_budget(budget, self._t, "POST",
                                     "/apis/v1/user-data/writes/begin",
                                     body)
        except TransportError as exc:
            safe_error = map_user_data_write_error(exc)
        if safe_error is not None:
            raise safe_error
        if not isinstance(resp, dict):
            raise SchemaError("begin response must be an object")
        if "targets" not in resp:
            # R2（B-IDEMPOTENT-RECEIPT）：幂等/终态分支**全绑定校验**——
            # storage/key/request 一致；committed 走完整回执验证
            # （digest/size/两 final），非 committed 终态转信息形态。
            try:
                receipt = self._parse_receipt_like_begin(
                    resp, binding=binding)
            except _BeginTerminalStatus as term:
                return BeginOutcome(status=term.status)
            return BeginOutcome(receipt=receipt)
        result = self._parse_begin(resp, layout=layout, binding=binding)
        expected = _derive_users_key(owner, rel)
        if result.canonical_key != expected:
            raise SchemaError(
                f"canonical_key echo mismatch: expected {expected!r}, "
                f"got {result.canonical_key!r}")
        return BeginOutcome(write=result)

    @staticmethod
    def _parse_begin(resp, *, layout: StorageLayout,
                     binding: "_RequestBinding") -> BeginWriteResult:
        op_id = _validate_op_id(_req_str(resp, "op_id", "op_id"))
        generation = _req_int(resp, "generation", "generation", minimum=1)
        protocol = _req_str(resp, "protocol", "protocol")
        if protocol != PROTOCOL:
            raise SchemaError(f"unexpected protocol {protocol!r}")
        storage_id = _req_str(resp, "storage_id", "storage_id")
        if storage_id != layout.storage_id:
            raise SchemaError("begin storage_id does not match discovery")
        canonical_key = _req_str(resp, "canonical_key", "canonical_key")
        lease = resp.get("lease")
        if not isinstance(lease, dict):
            raise SchemaError("begin response missing lease object")
        fencing = _req_str(lease, "fencing_token", "lease.fencing_token")
        expires = _req_rfc3339(lease, "expires_at", "lease.expires_at")
        targets_raw = resp.get("targets")
        if not isinstance(targets_raw, dict) or set(targets_raw) != set(
                _REGIONS):
            raise SchemaError(
                "begin targets must be a map with exactly cn+sg")
        targets = {}
        for r in _REGIONS:
            t = _parse_target(targets_raw[r], r,
                              expected_bucket=layout.replicas[r].bucket,
                              expected_endpoint=layout.replicas[r].endpoint,
                              expected_region=layout.replicas[r].oss_region)
            _refuse_temp_key_vs_final(t.temp_key, canonical_key)
            targets[r] = t
        # R1：echo 字段**可选**——出现即与本地绑定精确匹配，缺失不报错
        # （不新增协议未规定的必填字段；A 旧最小 begin 响应可解析）。
        for field_name, echoed, local in (
                ("sha256", resp.get("sha256"), binding.sha256),
                ("size", resp.get("size"), binding.size),
                ("owner", resp.get("owner"), binding.owner),
                ("relative_path", resp.get("relative_path"),
                 binding.relative_path),
                ("idempotency_key", resp.get("idempotency_key"),
                 binding.idempotency_key)):
            if echoed is not None and echoed != local:
                raise SchemaError(
                    f"begin echoed {field_name!r} does not match request "
                    "binding")
        return BeginWriteResult(
            op_id=op_id, generation=generation, protocol=protocol,
            storage_id=storage_id, canonical_key=canonical_key,
            targets=targets, fencing_token=fencing,
            lease_expires_at=expires,
            expected_sha256=binding.sha256,
            expected_size=binding.size,
            owner=binding.owner,
            relative_path=binding.relative_path,
            primary_region=binding.primary_region,
            idempotency_key=binding.idempotency_key)

    def _parse_receipt_like_begin(self, resp: dict,
                                  *, binding: "_RequestBinding"
                                  ) -> CommitWriteResult:
        """R2：幂等 begin 已 committed 的完整回执验证。

        绑定：storage_id/canonical_key（=owner+path 派生）/request
        digest/size 全比对；final 恰 cn+sg、两 key 相等且等于 canonical、
        桶与 canonical 登记一致——**任意 status=committed 旗标不等于已
        验证上传成功**。非 committed 终态（conflict/failed 等）转
        BeginOutcome.status 信息形态（见 begin 调用处）。
        """
        st = _parse_status_fields(resp)
        if st.storage_id != binding.storage_id:
            raise SchemaError(
                "idempotent begin receipt storage_id does not match "
                "request binding")
        if st.canonical_key != _derive_users_key(
                binding.owner, binding.relative_path):
            raise SchemaError(
                "idempotent begin receipt canonical_key does not match "
                "request binding")
        if st.status != "committed":
            # 非 committed 终态：信息型 status（调用方可据此决策，不当成功）。
            raise _BeginTerminalStatus(st)
        # committed：必须携带完整回执字段（sha256/size/final）。
        if "sha256" not in resp or "size" not in resp or "final" not in resp:
            raise SchemaError(
                "idempotent begin committed receipt missing "
                "sha256/size/final (cannot validate upload success)")
        sha256 = _req_str(resp, "sha256", "sha256")
        if not _SHA256_RE.fullmatch(sha256):
            raise SchemaError("receipt sha256 must be 64 lowercase hex")
        size = _req_int(resp, "size", "size", allow_zero=True)
        if sha256 != binding.sha256 or size != binding.size:
            raise UserDataWriteDigestMismatch(
                "idempotent begin committed receipt digest/size does not "
                "match request binding", biz_code=94108,
                error_code="user_data_write_digest_mismatch")
        final_raw = resp.get("final")
        if not isinstance(final_raw, dict) or set(final_raw) != set(
                _REGIONS):
            raise SchemaError("receipt final must be exactly cn+sg")
        final = {}
        keys = set()
        for r in _REGIONS:
            rec = final_raw[r]
            if not isinstance(rec, dict):
                raise SchemaError(f"final[{r!r}] must be an object")
            bucket = _req_str(rec, "bucket", f"final.{r}.bucket")
            key = _req_str(rec, "key", f"final.{r}.key")
            if bucket != self._policy.bucket(r):
                raise SchemaError(
                    f"final.{r}.bucket does not match expected replica "
                    "policy")
            keys.add(key)
            final[r] = {"bucket": bucket, "key": key}
        if len(keys) != 1 or st.canonical_key not in keys:
            raise SchemaError(
                "receipt final keys must be identical and equal to "
                "canonical_key")
        return CommitWriteResult(
            op_id=st.op_id, generation=st.generation, protocol=st.protocol,
            storage_id=st.storage_id, canonical_key=st.canonical_key,
            sha256=sha256, size=size, final=final, status="committed")


def _parse_target(d, region: str, *, expected_bucket: str,
                  expected_endpoint: str,
                  expected_region: str) -> WriteTarget:
    """P1-2：单 target 严格校验（结构+canonical 桶+endpoint 与已验证
    discovery 归一化一致+凭据仅小写）；**两 target 都过此关才有 IO**。"""
    if not isinstance(d, dict):
        raise SchemaError(f"targets[{region!r}] must be an object")
    bucket = _req_str(d, "bucket", f"targets.{region}.bucket")
    endpoint = _validate_https_endpoint(
        _req_str(d, "endpoint", f"targets.{region}.endpoint"),
        f"targets.{region}.endpoint")
    if bucket != expected_bucket:
        raise SchemaError(
            f"targets.{region}.bucket {bucket!r} does not match discovery")
    # P1-2 核心：endpoint 归一化后必须与**已验证** discovery endpoint 一致
    # （防把 STS 交给 unexpected host）。
    endpoint = _validate_regional_oss_endpoint(endpoint, expected_region)
    if endpoint != expected_endpoint:
        raise SchemaError(
            f"targets.{region}.endpoint {endpoint!r} does not match "
            f"validated discovery endpoint {expected_endpoint!r}")
    reg = _req_str(d, "region", f"targets.{region}.region")
    if reg != expected_region:
        raise SchemaError(
            f"targets.{region}.region {reg!r} does not match discovery")
    temp_key = _req_str(d, "temp_key", f"targets.{region}.temp_key")
    attempt = _req_str(d, "upload_attempt",
                       f"targets.{region}.upload_attempt")
    cred = d.get("credentials")
    if not isinstance(cred, dict):
        raise SchemaError(f"targets.{region}.credentials must be an object")
    # P1-1/P1-2：凭据仅小写四字段（大写/多余形态拒绝）。
    if set(cred) != {"access_key_id", "access_key_secret",
                     "security_token", "expiration"}:
        raise SchemaError(
            f"targets.{region}.credentials must contain exactly "
            "lowercase access_key_id/access_key_secret/security_token/"
            "expiration")
    ak = _req_str(cred, "access_key_id", "credentials.access_key_id")
    sk = _req_str(cred, "access_key_secret",
                  "credentials.access_key_secret")
    tok = _req_str(cred, "security_token", "credentials.security_token")
    exp = _req_rfc3339(cred, "expiration", "credentials.expiration")
    return WriteTarget(region=region, bucket=bucket, endpoint=endpoint,
                       region_id=reg, temp_key=temp_key,
                       upload_attempt=attempt, access_key_id=ak,
                       access_key_secret=sk, security_token=tok,
                       expiration=exp)


# upload/status/wait/commit 编排（挂接为 UserDataWritesClient 方法，
# 保持单类定义可读）。
def _upload(self, result: BeginWriteResult, local_path,
            deadline: float | None = None, *,
            _budget: "_Budget | None" = None,
            _source_identity: "_SourceIdentity | None" = None) -> dict:
    """两 target 流式直传 temp_key（primary 先；auth/schema 终态即停）。

    D1：单一绝对 budget——**0 预算=零上传调用（无首调用豁免）**；
    secondary 前必检预算。OSS IO 内部预算归 D（put_object_fn 合同），
    本方法管编排边界。

    P1-3：上传前 stat+流式 SHA 校验（与 begin 输入不符→拒绝，零网络
    调用）；上传后复检（源变动→94108，绝不成功）。P1-4：按
    primary_region 定序；终态错误（auth 401/403、schema、digest）立即抛
    不试 alternate；仅**明确识别**网络类错误有界续 secondary。"""
    budget = _budget if _budget is not None else _Budget(deadline)
    budget.raise_if_exhausted()      # 0 预算：primary 也不发（无豁免）
    path = Path(local_path)
    # ── 前置校验（P1-3：零网络调用即拒绝）──
    with _open_regular(path, budget=budget, identity=_source_identity) as source:
        identity = source.identity
    st_size = identity.size
    if st_size != result.expected_size:
        raise SchemaError(
            f"local file size {st_size} != begin declared size "
            f"{result.expected_size}")
    if _sha256_file(path, budget=budget, identity=identity) != result.expected_sha256:
        raise SchemaError(
            "local file digest does not match begin declared sha256 "
            "(source changed or wrong file)")
    # ── 定序（P1-4：primary 先，secondary 后）──
    primary = result.primary_region
    order = [primary] + [r for r in _REGIONS if r != primary]
    outcomes: dict = {}
    errors: dict = {}
    first_error: BaseException | None = None
    for idx, r in enumerate(order):
        # 项3（V5 剩余）：**每个 target 的 IO 前都检查预算**——前置
        # stat+hash 校验耗时后预算可能已耗尽，primary 也不得 bypass
        # （firstidx bypass 已修：扫描后耗尽=零上传调用）。
        try:
            budget.raise_if_exhausted()
        except TransportError as exc:
            errors[r] = exc
            outcomes[r] = {"ok": False, "error_type": "deadline"}
            if first_error is None:
                first_error = exc
            continue
        t = result.targets[r]
        if not t.temp_key or not t.upload_attempt:
            raise SchemaError(
                f"target {r!r} missing temp_key/upload_attempt")
        _refuse_temp_key_vs_final(t.temp_key, result.canonical_key)
        try:
            if idx > 0:
                # Metadata timestamps can collide on a coarse filesystem. Bind
                # actual bytes again before any secondary-region IO, including
                # after an unknown primary network outcome. Same absolute
                # budget and regular-file identity guards apply to this scan.
                if _sha256_file(path, budget=budget, identity=identity) != result.expected_sha256:
                    raise _source_changed()
            # 1135 D bridge：消费已审 D r5 **真实接口**（不重写 D、
            # 不按 UploadRequest 注释重造）：
            # - 每 target **独立 uploader 实例**（不共享 mutable 实例
            #   并发）；
            # - expectedSHA/size/absolute budget（deadline_monotonic=
            #   budget.deadline() 绝对单调时刻）逐参数传入；
            # - typed receipt 校验：精确 target（region/bucket/temp_key/
            #   attempt）+ bytecount==expected + sha256==expected；
            # - D 的 typed error 族由 _is_terminal_upload_error 归类
            #   （网络类有界续 secondary；其余终态）。
            receipt = self._d_bridge_upload(
                t, path, result.expected_size, result.expected_sha256,
                budget.deadline(), _budget=budget, _source_identity=identity)
            budget.raise_if_exhausted()
            # Receipt 校验（精确 target/attempt/count/SHA）：
            if (receipt.region != t.region
                    or receipt.bucket != t.bucket
                    or receipt.temp_key != t.temp_key
                    or receipt.upload_attempt != t.upload_attempt):
                raise SchemaError(
                    "D receipt target mismatch (region/bucket/temp_key/"
                    "attempt) for region=%r" % r)
            if receipt.bytecount != result.expected_size:
                raise UserDataWriteDigestMismatch(
                    "D receipt bytecount != expected size",
                    biz_code=94108,
                    error_code="user_data_write_digest_mismatch")
            if receipt.sha256 != result.expected_sha256:
                raise UserDataWriteDigestMismatch(
                    "D receipt sha256 != expected digest",
                    biz_code=94108,
                    error_code="user_data_write_digest_mismatch")
        except Exception as exc:  # noqa: BLE001
            if _is_terminal_upload_error(exc):
                raise                      # auth/schema/digest：终态即停
            errors[r] = exc                # 网络类：有界续 secondary
            outcomes[r] = {"ok": False, "error_type": type(exc).__name__}
            if first_error is None:
                first_error = exc
            continue
        outcomes[r] = {"ok": True, "attempt": t.upload_attempt}
    # ── 后置复检（P1-3：源变动拒绝，绝不成功）──
    budget.raise_if_exhausted()
    if _sha256_file(path, budget=budget, identity=identity) != result.expected_sha256:
        raise UserDataWriteDigestMismatch(
            "local source changed during upload (digest/size mismatch "
            "after transfer)", biz_code=94108,
            error_code="user_data_write_digest_mismatch")
    if errors:
        partial = UserDataWritePartial(
            "upload failed for targets: " + ", ".join(sorted(errors)),
            biz_code=94104, error_code="user_data_write_partial",
            data={"failed_targets": sorted(errors),
                  "succeeded_targets": sorted(
                      k for k in outcomes if outcomes[k].get("ok"))})
        if first_error is not None:
            raise partial from first_error
        raise partial
    budget.raise_if_exhausted()
    return {"targets": outcomes}


def _status(self, op_id: str, *, budget: "_Budget | None" = None,
            deadline: float | None = None) -> StatusResult:
    op = _validate_op_id(op_id)
    shared = budget if budget is not None else _Budget(deadline)
    safe_error = None
    try:
        resp = _call_with_budget(shared, self._t, "GET",
                                 f"/apis/v1/user-data/writes/{op}")
    except TransportError as exc:
        safe_error = map_user_data_write_error(exc, bound_op_id=op)
    if safe_error is not None:
        raise safe_error
    if not isinstance(resp, dict):
        raise SchemaError("status response must be an object")
    st = _parse_status_fields(resp)
    if st.op_id != op:
        raise SchemaError(
            f"status op_id mismatch: requested {op!r}, echoed {st.op_id!r}")
    return st


def _wait(self, op_id: str, *, deadline_seconds: float = 60.0,
          backoff_seconds: float = 1.0,
          max_attempts: int = 10) -> StatusResult:
    """D1：单一绝对 budget 穿透每次 status 调用与 sleep；**0 预算=零
    调用（无首调用豁免）**；仅 pending 重试；耗尽 pending 终态返回。"""
    budget = _Budget(deadline_seconds)
    attempts = 0
    while True:
        budget.raise_if_exhausted()          # 首次也无豁免
        st = _status(self, op_id, budget=budget)
        attempts += 1
        if st.status != "pending":
            return st
        if attempts >= max_attempts:
            return st
        if budget.exhausted:
            return st                # 耗尽：pending 终态返回
        budget.sleep_bound(backoff_seconds)


def _commit(self, result: BeginWriteResult,
            deadline: float | None = None) -> CommitWriteResult:
    """commit（body=protocol/generation/upload_attempt/fencing_token——
    零客户端自报）；回执比对 expected digest/size（P1-3，不符→94108）。
    D1：公共预算入口（0 预算=零调用）。"""
    op_id = _validate_op_id(result.op_id)
    attempts = {r: result.targets[r].upload_attempt for r in _REGIONS}
    if len(set(attempts.values())) != 1:
        raise SchemaError(
            "begin targets carry different upload_attempt values")
    body = {
        "protocol": PROTOCOL,
        "generation": result.generation,
        "upload_attempt": attempts["cn"],
        "fencing_token": result.fencing_token,
    }
    safe_error = None
    try:
        resp = _call_with_budget(_Budget(deadline), self._t, "POST",
                                 f"/apis/v1/user-data/writes/{op_id}/commit",
                                 body)
    except TransportError as exc:
        safe_error = map_user_data_write_error(exc, bound_op_id=op_id)
    if safe_error is not None:
        raise safe_error
    if not isinstance(resp, dict):
        raise SchemaError("commit response must be an object")
    status = _req_str(resp, "status", "status")
    if status != "committed":
        raise UserDataWritePending(
            f"commit response status {status!r} is not committed",
            biz_code=94103, error_code="user_data_write_pending")
    op_r = _validate_op_id(_req_str(resp, "op_id", "op_id"))
    generation = _req_int(resp, "generation", "generation", minimum=1)
    protocol = _req_str(resp, "protocol", "protocol")
    if protocol != PROTOCOL:
        raise SchemaError(f"unexpected protocol {protocol!r}")
    storage_id = _req_str(resp, "storage_id", "storage_id")
    if op_r != result.op_id:
        raise SchemaError("commit op_id does not match begin")
    if generation != result.generation:
        raise UserDataWriteStaleFence(
            "commit generation does not match begin", biz_code=94107,
            error_code="user_data_write_stale_fence")
    if storage_id != result.storage_id:
        raise SchemaError("commit storage_id does not match begin")
    canonical_key = _req_str(resp, "canonical_key", "canonical_key")
    if canonical_key != result.canonical_key:
        raise SchemaError("commit canonical_key does not match begin")
    sha256 = _req_str(resp, "sha256", "sha256")
    if not _SHA256_RE.fullmatch(sha256):
        raise SchemaError("commit sha256 must be 64 lowercase hex")
    size = _req_int(resp, "size", "size", allow_zero=True)
    # P1-3：回执比对 expected digest/size（不符→94108，绝不成功）。
    if sha256 != result.expected_sha256 or size != result.expected_size:
        raise UserDataWriteDigestMismatch(
            "commit receipt digest/size does not match begin request",
            biz_code=94108,
            error_code="user_data_write_digest_mismatch")
    final_raw = resp.get("final")
    if not isinstance(final_raw, dict) or set(final_raw) != set(_REGIONS):
        raise SchemaError("commit final must be exactly cn+sg")
    final = {}
    keys = set()
    for r in _REGIONS:
        rec = final_raw[r]
        if not isinstance(rec, dict):
            raise SchemaError(f"final[{r!r}] must be an object")
        bucket = _req_str(rec, "bucket", f"final.{r}.bucket")
        key = _req_str(rec, "key", f"final.{r}.key")
        if bucket != result.targets[r].bucket:
            raise SchemaError(
                f"final.{r}.bucket does not match begin target")
        keys.add(key)
        final[r] = {"bucket": bucket, "key": key}
    if len(keys) != 1:
        raise SchemaError("final keys must be identical across cn+sg")
    if canonical_key not in keys:
        raise SchemaError(
            "final key must equal canonical_key (no extra hierarchy)")
    return CommitWriteResult(op_id=op_r, generation=generation,
                             protocol=protocol, storage_id=storage_id,
                             canonical_key=canonical_key, sha256=sha256,
                             size=size, final=final)


# 挂接方法（保持类定义集中）。
# ── 1135 D bridge：消费已审 D r5 TempObjectUploader（真实接口）──


def _d_bridge_upload(self, t: "WriteTarget", path: Path,
                     expected_size: int, expected_sha256: str,
                     budget_deadline: float | None, *,
                     _budget: "_Budget | None" = None,
                     _source_identity: "_SourceIdentity | None" = None):
    """单 target 上传经 D r5 真实 uploader。

    优先级：
    1. ``put_object_fn`` 注入（测试 fake——签名含 budget_deadline 时
       传绝对预算）；
    2. D r5 ``TempObjectUploader``（每 target 独立实例、close 释放；
       expected/absolute deadline 逐参数；返回 typed UploadReceipt）。
    """
    shared = _budget if _budget is not None else _Budget(None)
    if _budget is None:
        shared._deadline = budget_deadline
    # Bind again before every target, including legacy injected adapters. Their
    # own read allocation/interruption remains the trusted caller's responsibility.
    with _open_regular(path, budget=shared, identity=_source_identity) as source:
        identity = source.identity
    # 测试注入路径（三参/budget 形态）——返回轻量 receipt 形态。
    if self._put_object_fn is not _default_put_object:
        put = self._put_object_fn
        if _put_supports_budget(put):
            put(t, path, expected_size,
                budget_deadline=budget_deadline)
        else:
            put(t, path, expected_size)
        from .user_data_upload import UploadReceipt as _DReceipt
        return _DReceipt(
            region=t.region, bucket=t.bucket, temp_key=t.temp_key,
            upload_attempt=t.upload_attempt, bytecount=expected_size,
            sha256=expected_sha256, multipart=False, part_count=0)
    # 真实 D r5 路径：每 target 独立 uploader（close 释放 session）。
    # ``oss2_module``：测试注入 vendor fake（D 真实代码路径不换——
    # 只替底层 oss2 实现）；生产 None=D 内部 lazy import 真实 oss2。
    from .user_data_upload import TempObjectUploader
    oss2_module = getattr(self, "_test_oss2_module", None)
    uploader = TempObjectUploader(t, oss2_module=oss2_module)
    try:
        # D r5 契约：deadline_monotonic 必传（绝对单调时刻）。B 侧
        # 无预算（None）时给一个"无限远"值（D 内部 guard 恒过——与
        # B 无预算语义一致，单请求 cap 仍由 D request_timeout_cap 管）。
        import math
        deadline_value = (budget_deadline
                          if budget_deadline is not None else math.inf)
        return uploader.upload(
            lambda: _open_regular(path, budget=shared, identity=identity),
            expected_size=expected_size,
            expected_sha256=expected_sha256,
            deadline_monotonic=deadline_value)
    finally:
        uploader.close()


UserDataWritesClient._d_bridge_upload = _d_bridge_upload
UserDataWritesClient.upload = _upload
UserDataWritesClient.status = _status
UserDataWritesClient.wait = _wait
UserDataWritesClient.commit = _commit


def _default_put_object(target: "WriteTarget", local_path: Path,
                        expected_size: int) -> None:  # pragma: no cover
    """真实 OSS 直传归 **D 线**（user_data_upload.py）：真实 oss2 adapter、
    流式分块、OSS IO 预算测试都在 D 实现/补测。

    **B/D 接口约定（待 D 落地后协调冻结）**：
    - D 的 put_object_fn 签名=本模块注入点 ``(target: WriteTarget,
      local_path: Path, expected_size: int) -> None``；
    - D 须以 **typed 异常**表达失败类别：网络类（可续 secondary——本模块
      ``_is_terminal_upload_error`` 白名单：ConnectionError/TimeoutError/
      socket.timeout/网络 errno 族）、鉴权/数据/编程类（终态）；
    - 厂商 OSS 异常（oss2 ServerError 等）在 D 侧转 typed 后进本模块；
      **未分类异常一律终态**（R5 契约）；
    - D 只管 OSS IO 预算；控制面 HTTP 预算归 B（本模块 ``_Budget``）。
    本占位仅在无注入时拒绝（fail-closed，防误用未审实现）。"""
    raise NotImplementedError(
        "real OSS upload adapter is owned by the D slice "
        "(user_data_upload.py); inject put_object_fn for tests")


# ── B/D 接线合同（项3：接口规格化——**不接 D 实现**，D 过审冻结后由
#    本模块单 writer 整合；D 未冻结前 put_object_fn 注入面保持现状）──

@dataclass(frozen=True)
class UploadRequest:
    """B→D 上传请求（V5 剩余项3：显式 expectedSHA/size/绝对剩余预算/
    typed 回执合同——替代三参 placeholder）。

    D 侧约定（待 D 过审后按本规格实现 user_data_upload.py）：
    - **绝对剩余预算**：``budget_deadline`` 为**绝对单调时刻**（不是
      时长——B 侧 ``_Budget`` 一次派生后传入 ``deadline`` 值）；D 在
      每次 OSS IO 前/后检查（含 hash 扫描后、primary IO 前——B 不再
      有 firstidx bypass 面，见 _upload）；
    - **expected_sha256/expected_size**：来自 begin 本地绑定（P1-3），
      D 侧流式上传/校验以二者为准（客户端不自报成功）；
    - **typed 回执**：成功返回 ``UploadReceipt``；失败必须以可分类
      异常表达（网络 errno 族/ConnectionError/TimeoutError——可续
      secondary；其余终态），未知异常 B 侧按终态（_is_terminal_upload_
      error 契约）；
    - **safe error**：D 不得在异常 message/repr 放凭据/签名 URL。
    """
    target: "WriteTarget"
    local_path: Path
    expected_sha256: str
    expected_size: int
    budget_deadline: float | None      # 绝对 monotonic 时刻（None=不限）


@dataclass(frozen=True)
class UploadReceipt:
    """D→B 上传回执（typed——B 侧不再从异常侧猜测结果）。"""
    region: str                        # "cn" | "sg"
    upload_attempt: str
    bytes_sent: int                    # == expected_size（D 校验）
    etag: str = ""                     # 可选（OSS 返回时）


def _bridge_put_adapter(put_fn):
    """三参 legacy 注入面→V5 合同适配（过渡期：既有 fake 与 D 旧形态
    继续可用；D 冻结后切换 put_fn 直接收 UploadRequest）。"""
    def adapted(request: "UploadRequest") -> "UploadReceipt":
        put_fn(request.target, request.local_path, request.expected_size)
        return UploadReceipt(region=request.target.region,
                             upload_attempt=request.target.upload_attempt,
                             bytes_sent=request.expected_size)
    return adapted
