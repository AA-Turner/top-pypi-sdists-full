"""user_data_upload.py — users 域真实 OSS 流式上传 adapter（D 切片，r3）。

Codex r2 复审 sdk-upload-D-r2-codex-review-20261031-0749 五项 P1 返修 +
两项代码审查落实（保留 r2 已修基础：planner 容量、不 DELETE key、
short-read 填充、AK repr、finally 关 session、redirect False、
postcheck——不重写）：

1. **D-R2-ACTUAL-BYTES（P1）**：回执摘要=**实际发送字节**的增量 SHA。
   所有传输路径统一为 `SizedStreamPart` 流式视图（每次 `read(amt)` 返回
   恰好 min(amt, remaining)——oss2 `_BytesAndFileAdapter` 按请求量跳
   offset，要求精确语义；内部短读补足+EOF 探测），总 SHA/计数在
   **每次实际 read** 时增量累计（我们自己的 hook——不是 vendor CRC）。
   二遍法删除：单 part > chunk 走 **单 part multipart**（init→1 个流式
   part→流式 hash 完成后 complete），源变异在 complete 前被流式摘要
   拦截。mismatch/short/extra 一律拒绝完成/回执。
2. **D-R2-BOUNDED-IO（P1）**：`SizedStreamPart.read(amt)` 内部按
   `io_chunk` 上限分段填满（**内存上界=io_chunk 与 part 尺寸无关**）。
   multipart 每逻辑 part 传该流式视图（非整 part bytes）。11GiB 规划
   2MiB part 时实际单次读 ≤1MiB（io_chunk）。测试：synthetic 大尺寸
   断言 max read ≤ 配置 bound（不分配大文件）。
3. **D-R2-VENDOR-LOG（P1）**：`_VENDOR_LOGGER_NAMES` 补 **oss2.auth**；
   Python logging 的 ancestor logger filter **不处理 propagated
   records**（callHandlers 源码证实）——故除名单外，同时挂 **root logger
   handler 级 filter 无法实现（Handler.addFilter 作用于 handler）**；
   采取方案：对名单+root 挂 logger filter 覆盖直接命名调用；对
   propagate 的子记录（如 oss2.auth 从真实 auth 代码发出），由于
   `oss2.auth` 已在名单中直接覆盖；**并额外 hook
   `logging.Logger.handle`**？——不（不改全局行为）。最终方案：
   名单覆盖 oss2 全部真实模块（http/api/utils/auth/exceptions/
   resumable/defaults）+ root logger filter（活跃 scope 线程的
   根级 direct 调用）。测试用 root DEBUG 实际 capture 走真实 upload
   （oss2.auth 签名期真实日志路径），断言 canary 不可见。
4. **D-R2-DEADLINE（P1）**：`_dispatch` 包装——**每次实际网络调用**
   （init/upload_part/put_object/complete/abort/delete）都经
   `_call_with_budget`：dispatch 前 timeout=min(cap, remaining)（每次
   重算），返回后 postcheck（deadline/cancel）；本地 scan/read 每
   chunk 检查 deadline/cancel；`_scan_stream` 有界
   （expected_size+1 停止——非读到 EOF）。模拟 elapsed 测试断言
   每请求 timeout ≤ 当时 remaining。
5. **D-R2-ERRORS（P1）**：分类修正——**只有已识别的网络瞬态**
   （oss2 RequestError/requests 网络异常超集、5xx）retryable；
   ValueError 等未知异常/源错误/schema/auth/cancel 一律**终态**
   （UploadOssError kind="unknown" retryable=False，非
   OutcomeUnknown——OutcomeUnknown 仅网络 ambiguous 语义）；
   ConnectionError（oss2 RequestError 包装）→ retryable=True（网络
   瞬态）。**traceback 脱敏**：`from exc` 保留原因链但消息层已
   脱敏；为防 raw canary 经 `__cause__` 全 traceback 回显，包装时
   对已知凭据异常消息做显式断链（`__suppress_context__`+cause 消息
   置换为类名）——实测完整 traceback 断言 canary 不可见。

代码审查项：
- `_make_bucket` 移入生命周期 guard（try/finally 覆盖构造——构造
  失败关 owned session）。
- `_scan_stream`/`_bounded_iter` 有界+每 chunk deadline/cancel 检查
  （后者已被 SizedStreamPart 统一取代，保留 scan 用于小对象? 不——
  统一流式，scan 删除）。

边界不变：输入=B 已验证 target；不做路由/成功裁决；仅两文件所有权；
零自有日志调用；零 checkpoint 落盘。
"""
from __future__ import annotations

import hashlib
import logging
import re
import threading
import time
from contextlib import closing, contextmanager
from dataclasses import dataclass, field

from ..errors import InstanceRepoError, SchemaError

__all__ = [
    "UploadTarget", "UploadReceipt", "UploadPartPlan", "plan_parts",
    "TempObjectUploader", "UserDataUploadError", "UploadSizeMismatch",
    "UploadDigestMismatch", "UploadDeadlineExceeded", "UploadCancelled",
    "UploadOssError", "UploadOutcomeUnknown", "UploadCapacityError",
    "scoped_vendor_log_sanitizer", "SizedStreamPart",
]

#: 流式分块默认 1MiB（IO 有界单位——内存上界，与 part 尺寸无关）。
CHUNK_BYTES = 1024 * 1024

#: OSS UploadPart 官方约束（不发明上限）。
OSS_MAX_PART_NUMBER = 10000
OSS_MIN_PART_BYTES = 100 * 1024
OSS_MAX_PART_BYTES = 5 * 1024 * 1024 * 1024

_SHA256_RE = re.compile(r"[0-9a-f]{64}")
_EMPTY_SHA256 = hashlib.sha256(b"").hexdigest()

#: vendor logger 名单（含 r2 漏掉的 oss2.auth）。
_VENDOR_LOGGER_NAMES = (
    "oss2.http", "oss2.api", "oss2.utils", "oss2.auth",
    "oss2.resumable", "oss2.exceptions", "oss2.defaults",
)


# ── typed 异常（safe kind/status/retryable 契约供 B 消费）──────────────

class UserDataUploadError(InstanceRepoError):
    """users 域上传执行错误基类。

    ``kind``：安全分类词表；``status``：真实 HTTP 状态码（int 或
    None——无响应网络失败）；``retryable``：**仅已识别网络瞬态**
    （RequestError/requests 网络异常/5xx）可 True；unknown/schema/
    source/auth/cancel/deadline 一律终态 False。消息只含
    类名/阶段/region/status——URL/body/凭据绝不可入；``__cause__``
    仅可为新建的安全类型诊断，不保留原 vendor 链或 traceback。
    """
    code = "E_USERDATA_UPLOAD"
    retryable = False

    def __init__(self, message: str = "", *, kind: str = "",
                 status: int | None = None, retryable: bool = False,
                 cause: BaseException | None = None) -> None:
        super().__init__(message, cause=self._sanitized(cause))
        self.kind = kind or self.code
        self.status = status if isinstance(status, int) else None
        self.retryable = bool(retryable)

    @staticmethod
    def _sanitized(cause: BaseException | None) -> BaseException | None:
        """Keep only a fresh diagnostic type/message, never vendor chains.

        Nested causes, custom attributes and traceback frames can all retain
        signed URLs or credentials even when the outer message is redacted.
        """
        if cause is None:
            return None
        try:
            proxy = type(cause)("redacted: " + type(cause).__name__)
            proxy.__cause__ = None
            proxy.__context__ = None
            proxy.__suppress_context__ = True
            proxy.__traceback__ = None
            return proxy
        except Exception:  # noqa: BLE001 - 构造兜底
            return None


class UploadSizeMismatch(UserDataUploadError):
    code = "E_UPLOAD_SIZE_MISMATCH"
    kind = "size_mismatch"


class UploadDigestMismatch(UserDataUploadError):
    code = "E_UPLOAD_DIGEST_MISMATCH"
    kind = "digest_mismatch"


class UploadDeadlineExceeded(UserDataUploadError):
    code = "E_UPLOAD_DEADLINE_EXCEEDED"
    kind = "deadline_exceeded"


class UploadCancelled(UserDataUploadError):
    code = "E_UPLOAD_CANCELLED"
    kind = "cancelled"


class UploadCapacityError(UserDataUploadError):
    """真实后端容量拒绝（10000 part × 5GiB 仍不足）——网络前显式。"""
    code = "E_UPLOAD_CAPACITY"
    kind = "capacity_exceeded"


class UploadOssError(UserDataUploadError):
    """oss2 协议/HTTP 错误或未知异常（**终态**——unknown 不可 retry）。"""
    code = "E_UPLOAD_OSS_ERROR"
    kind = "oss_error"


class UploadOutcomeUnknown(UserDataUploadError):
    """网络 ambiguous（无响应：超时/连接中断）——唯一 retryable=True
    语义（可重试上传，恢复协调交服务端）。"""
    code = "E_UPLOAD_OUTCOME_UNKNOWN"
    kind = "outcome_unknown"
    retryable = True


# ── 输入/输出结构 ──────────────────────────────────────────────────────

@dataclass(frozen=True)
class UploadTarget:
    """单 target 上传输入（B 已完成 canonical/discovery/HTTPS 校验）。

    全凭据字段（含 access_key_id）repr=False。
    """

    region: str
    bucket: str
    endpoint: str
    temp_key: str
    upload_attempt: str
    access_key_id: str = field(repr=False)
    access_key_secret: str = field(repr=False)
    security_token: str = field(repr=False)
    expiration: str = ""


@dataclass(frozen=True)
class UploadPartPlan:
    """分片规划：part 长度序列 + 计数（IO 时按 offset 分段流式读）。"""

    part_size: int
    total_size: int
    part_count: int
    final_part_size: int

    def part_length(self, index: int) -> int:
        if not 0 <= index < self.part_count:
            raise ValueError("part index out of range")
        if index == self.part_count - 1:
            return self.final_part_size
        return self.part_size


@dataclass(frozen=True)
class UploadReceipt:
    """上传执行回执：**实际发送字节**的计数与增量摘要（非预期值）。"""

    region: str
    bucket: str
    temp_key: str
    upload_attempt: str
    bytecount: int
    sha256: str
    multipart: bool
    part_count: int


def plan_parts(total_size: int, *, chunk_bytes: int = CHUNK_BYTES,
               max_part_number: int = OSS_MAX_PART_NUMBER,
               min_part_bytes: int = OSS_MIN_PART_BYTES,
               max_part_bytes: int = OSS_MAX_PART_BYTES) -> UploadPartPlan:
    """自适应分片规划（官方约束：count 1..10000、非末 ≥100KiB、
    每 part ≤5GiB、末可小；>10000×5GiB → CapacityError 网络前拒绝）。"""
    if isinstance(total_size, bool) or not isinstance(total_size, int) \
            or total_size < 0:
        raise SchemaError("total_size must be a nonnegative integer")
    if total_size == 0:
        return UploadPartPlan(part_size=0, total_size=0, part_count=0,
                              final_part_size=0)
    absolute_cap = max_part_number * max_part_bytes
    if total_size > absolute_cap:
        raise UploadCapacityError(
            "total size %d exceeds OSS multipart capacity "
            "(%d parts x %d bytes)" % (total_size, max_part_number,
                                       max_part_bytes))
    size = max(int(chunk_bytes), min_part_bytes)
    while True:
        size = min(size, max_part_bytes)
        count = (total_size + size - 1) // size
        if count <= max_part_number:
            if count == 1:
                return UploadPartPlan(
                    part_size=size, total_size=total_size, part_count=1,
                    final_part_size=total_size)
            final = total_size - size * (count - 1)
            return UploadPartPlan(part_size=size, total_size=total_size,
                                  part_count=count, final_part_size=final)
        if size >= max_part_bytes:
            raise UploadCapacityError(
                "cannot plan parts within OSS constraints")
        size *= 2


# ── scoped vendor 日志脱敏 ─────────────────────────────────────────────

class _VendorSecretScrubber(logging.Filter):
    """活跃 scope 线程发出的记录做凭据替换（线程 id 登记表——栈式，
    支持嵌套 scope：内层退出后外层 canaries 仍生效）。"""

    _active: dict[int, list[tuple[tuple[str, str], ...]]] = {}

    @classmethod
    def _register(cls, tid, canaries):
        stack = cls._active.setdefault(tid, [])
        stack.append(canaries)

    @classmethod
    def _unregister(cls, tid):
        stack = cls._active.get(tid)
        if stack:
            stack.pop()
            if not stack:
                del cls._active[tid]

    def filter(self, record: logging.LogRecord) -> bool:
        tid = threading.get_ident()
        stack = type(self)._active.get(tid)
        if not stack:
            return True
        # 顶层（最外层活跃 scope）canaries 生效（外层 secrets 覆盖面
        # 最广；内层叠加亦在外层 scope 内）。
        canaries = stack[0] + tuple(
            c for s in stack[1:] for c in s)
        base = record.msg if isinstance(record.msg, str) else \
            str(record.msg)
        rendered = base
        if record.args:
            try:
                rendered = base % record.args
            except (TypeError, ValueError):
                rendered = base
        changed = False
        for secret, placeholder in canaries:
            if secret and secret in rendered:
                rendered = rendered.replace(secret, placeholder)
                changed = True
        if changed:
            record.msg = rendered
            record.args = None
        return True


@contextmanager
def scoped_vendor_log_sanitizer(secrets: tuple[str, ...] | list[str]):
    """对 vendor logger 名单（含 oss2.auth）+root 挂脱敏 Filter，退出恢复。

    并发安全（线程 id 登记）；不改 level/不删 handler/不改第三方源。
    注意 logging 语义：logger filter 只作用于该 logger 直接调用——
    名单覆盖 oss2 全部真实模块名即覆盖其直接日志；propagated 子名
    （未来新增 oss2.*）经 root 时也由 root filter 覆盖（root filter
    处理 root 直接调用；子名 propagate 到 root 的 handler 链不经
    root logger filter——故名单兜底 + 根 handler 层不做全局改动，
    已知 oss2 模块全覆盖即可）。
    """
    canaries = tuple((s, "<REDACTED>") for s in secrets if s)
    tid = threading.get_ident()
    scrubber = _VendorSecretScrubber()
    _VendorSecretScrubber._register(tid, canaries)
    attached: list[logging.Logger] = []
    try:
        targets = list(_VENDOR_LOGGER_NAMES) + [""]
        for name in targets:
            lg = logging.getLogger(name)
            lg.addFilter(scrubber)
            attached.append(lg)
        yield
    finally:
        for lg in attached:
            try:
                lg.removeFilter(scrubber)
            except Exception:  # noqa: BLE001
                pass
        _VendorSecretScrubber._unregister(tid)


# ── 有界读 helpers（短 read ≠ EOF）────────────────────────────────────

def read_exact(fh, n: int) -> bytes:
    """读满 n 字节或到 EOF（有界：≤ n；循环吸收短 read）。

    返回 < n = 真 EOF（非短 read 假象）。
    """
    if n <= 0:
        return b""
    buf = bytearray()
    while len(buf) < n:
        chunk = fh.read(n - len(buf))
        if not chunk:
            break
        buf.extend(chunk)
    return bytes(buf)


# ── 流式 sized part（实际字节绑定 + IO 有界）──────────────────────────

class SizedStreamPart:
    """单逻辑 part 的流式视图（D-R2-ACTUAL-BYTES + D-R2-BOUNDED-IO）。

    语义（与 oss2 `_BytesAndFileAdapter` 兼容——其 read(amt) 按请求量
    跳 offset，要求 read 返回**恰好** min(amt, remaining)）：
    - ``read(amt)``：内部按 ``io_chunk`` 上限**分段填充**至恰好
      min(amt, remaining)（内存上界=io_chunk，与 part 逻辑尺寸无关）；
      源短读循环补足；源 EOF 早于预期 → 置 error（UploadSizeMismatch
      语义，发送侧 read 返回已读内容后由 uploader 终检拒绝）。
    - ``__len__``：part 逻辑长度（供 oss2 Content-Length/CRC）。
    - 每次 read 的字节**同步增量累计**到 uploader 的总 SHA/计数
      （actual-bytes 绑定：摘要=实际发送字节，非预期）。
    - 每个 io_chunk 边界检查 deadline/cancel（D-R2-DEADLINE 长读检查）。
    """

    def __init__(self, fh, size: int, *, uploader, io_chunk: int,
                 deadline: float, label: str) -> None:
        self._fh = fh
        self._remaining = size
        self._total = size
        self._uploader = uploader
        self._io_chunk = max(1, int(io_chunk))
        self._deadline = deadline
        self._label = label
        self._error: BaseException | None = None

    def __len__(self) -> int:
        return self._total

    def read(self, amt: int = -1) -> bytes:
        if self._error is not None:
            raise self._error
        if self._remaining <= 0:
            return b""
        if amt is None or amt < 0:
            target = self._remaining
        else:
            target = min(amt, self._remaining)
        buf = bytearray()
        while len(buf) < target:
            # D-R2-DEADLINE：每个 IO 分段前检查 deadline/cancel。
            self._uploader._guard(self._deadline,
                                  "source read %s" % self._label)
            want = min(self._io_chunk, target - len(buf))
            chunk = self._fh.read(want)
            if not chunk:
                if len(buf) < target:
                    # 源 EOF 早于预期（短流）——记录错误，抛给发送链。
                    self._error = UploadSizeMismatch(
                        "source ended early during %s (read %d of %d)"
                        % (self._label, self._total - self._remaining,
                           self._total))
                    raise self._error
                break
            buf.extend(chunk)
            self._remaining -= len(chunk)
            # D-R2-ACTUAL-BYTES：实际消费字节增量累计（发送即计数）。
            self._uploader._hasher.update(chunk)
            self._uploader._actual_bytes += len(chunk)
        return bytes(buf)

    @property
    def remaining(self) -> int:
        return self._remaining


# ── 上传执行器 ─────────────────────────────────────────────────────────

class TempObjectUploader:
    """单 target OSS 上传执行器。

    ``io_chunk``：IO 内存上界（每次底层 read ≤ io_chunk；与 part 尺寸
    无关——D-R2-BOUNDED-IO）。``request_timeout_cap``：单次 HTTP 上限
    （每次实际 timeout=min(cap, remaining)，每次重算——D-R2-DEADLINE）。
    """

    def __init__(self, target: UploadTarget, *,
                 io_chunk: int = CHUNK_BYTES,
                 request_timeout_cap: float = 30.0,
                 is_cname: bool = False,
                 abort_attempts: int = 3,
                 abort_backoff_seconds: float = 0.05,
                 oss2_module=None) -> None:
        for name in ("region", "bucket", "endpoint", "temp_key",
                     "upload_attempt", "access_key_id",
                     "access_key_secret", "security_token"):
            v = getattr(target, name)
            if not isinstance(v, str) or not v:
                raise SchemaError(f"target.{name} must be a nonempty string")
        if isinstance(io_chunk, bool) or not isinstance(io_chunk, int) \
                or io_chunk < 1:
            raise SchemaError("io_chunk must be a positive integer")
        self._target = target
        self._io_chunk = io_chunk
        self._timeout_cap = float(request_timeout_cap)
        self._is_cname = bool(is_cname)
        self._abort_attempts = int(abort_attempts)
        self._abort_backoff = float(abort_backoff_seconds)
        self._oss2 = oss2_module
        self._cancelled = threading.Event()
        self._closed = False
        self._session = None
        self._bucket_ref = None       # per-dispatch timeout 更新引用
        # cleanup best-effort 诊断（safe：类名/status；不掩盖原错）
        self._cleanup_diagnostic: str | None = None
        # actual-bytes 跟踪（每次 upload() 重置）：
        self._hasher = hashlib.sha256()
        self._actual_bytes = 0

    # ── 生命周期 ──
    def cancel(self) -> None:
        self._cancelled.set()

    def close(self) -> None:
        self._closed = True
        self._close_owned_session()

    def _close_owned_session(self) -> None:
        if self._session is not None:
            try:
                self._session.session.close()
            except Exception:  # noqa: BLE001
                pass
            self._session = None

    # ── 主入口 ──
    def upload(self, open_source, *, expected_size: int,
               expected_sha256: str,
               deadline_monotonic: float) -> UploadReceipt:
        if self._closed:
            raise UploadCancelled("uploader is closed")
        if isinstance(expected_size, bool) or not isinstance(expected_size, int) \
                or expected_size < 0:
            raise SchemaError(
                "expected_size must be a nonnegative integer (not bool)")
        if not _SHA256_RE.fullmatch(str(expected_sha256 or "")):
            raise SchemaError(
                "expected_sha256 must be 64 lowercase hex chars")
        self._guard(deadline_monotonic, "start")
        t = self._target

        # actual-bytes / cleanup 诊断重置（每次 upload 独立）。
        self._hasher = hashlib.sha256()
        self._actual_bytes = 0
        self._cleanup_diagnostic = None

        with scoped_vendor_log_sanitizer(
                (t.access_key_id, t.access_key_secret, t.security_token)):
            # D 代码审查项：构造纳入生命周期 guard（构造失败关 session）。
            bucket = None
            try:
                oss2 = self._load_oss2()
                bucket = self._make_bucket(oss2, deadline_monotonic)
                with closing(open_source()) as fh:
                    if expected_size == 0:
                        return self._upload_zero(bucket, fh, t,
                                                 expected_sha256,
                                                 deadline_monotonic)
                    # 性能快路径（PERF delta）：expected_size ≤ io_chunk
                    # → 有界整读（n+1 探测）+校验+不可变 bytes 一次 PUT。
                    # 此路径无二遍缺陷（actual bytes 一次性确定，无
                    # reopen）；较大文件继续已审的 sized stream multipart。
                    if expected_size <= self._io_chunk:
                        return self._upload_small_fast_put(
                            bucket, fh, t, expected_size,
                            expected_sha256, deadline_monotonic)
                    plan = plan_parts(expected_size,
                                      chunk_bytes=self._io_chunk)
                    return self._run_multipart(bucket, fh, t, plan,
                                               expected_sha256,
                                               deadline_monotonic)
            finally:
                self._close_owned_session()

    # ── 策略实现 ──
    def _upload_zero(self, bucket, fh, t, expected_sha256,
                     deadline) -> UploadReceipt:
        probe = fh.read(1)
        if probe:
            raise UploadSizeMismatch(
                "source is nonempty but expected_size is 0 (region=%s)"
                % t.region)
        if expected_sha256 != _EMPTY_SHA256:
            raise UploadDigestMismatch(
                "expected_sha256 does not match empty digest (region=%s)"
                % t.region)
        self._call_with_budget(
            lambda: bucket.put_object(t.temp_key, b""),
            deadline, "zero-byte put", t)
        return UploadReceipt(region=t.region, bucket=t.bucket,
                             temp_key=t.temp_key,
                             upload_attempt=t.upload_attempt,
                             bytecount=0, sha256=_EMPTY_SHA256,
                             multipart=False, part_count=0)

    def _upload_small_fast_put(self, bucket, fh, t, expected_size,
                               expected_sha256,
                               deadline) -> UploadReceipt:
        """小文件快路径（PERF delta）：expected_size ≤ io_chunk。

        有界整读（read_exact n+1 探测超长）→ 摘要/长度核对 →
        **不可变 bytes 一次 PUT**（每 target 1 次 HTTP——旧已验证安全
        路径，无二遍缺陷：bytes 一次性确定，actual=expected 无歧义，
        无 reopen）。零额外 init/complete 请求（避免小文件 3 调用退化）。
        """
        data = read_exact(fh, expected_size + 1)
        if len(data) > expected_size:
            raise UploadSizeMismatch(
                "source longer than expected_size (region=%s, "
                "expected=%d)" % (t.region, expected_size))
        if len(data) < expected_size:
            raise UploadSizeMismatch(
                "source shorter than expected_size (region=%s, "
                "expected=%d)" % (t.region, expected_size))
        digest = hashlib.sha256(data).hexdigest()
        if digest != expected_sha256:
            raise UploadDigestMismatch(
                "source sha256 does not match expected (region=%s)"
                % t.region)
        # actual-bytes 跟踪一致性（快路径 bytes 一次性确定）。
        self._hasher = hashlib.sha256(data)
        self._actual_bytes = len(data)
        self._call_with_budget(
            lambda: bucket.put_object(t.temp_key, data),
            deadline, "put_object", t)
        return UploadReceipt(region=t.region, bucket=t.bucket,
                             temp_key=t.temp_key,
                             upload_attempt=t.upload_attempt,
                             bytecount=expected_size, sha256=digest,
                             multipart=False, part_count=0)

    def _run_multipart(self, bucket, fh, t, plan, expected_sha256,
                       deadline) -> UploadReceipt:
        """统一 multipart 执行（1..10000 part，每 part SizedStreamPart）。

        实际字节绑定：总 SHA/计数=所有 part **实际 read**（发送）字节的
        增量累计；源 EOF 早退/extra 探测/摘要不符 → abort + 拒绝回执。
        """
        part_info_cls = self._load_oss2().models.PartInfo
        upload_id = None
        parts = []
        try:
            init = self._call_with_budget(
                lambda: bucket.init_multipart_upload(t.temp_key),
                deadline, "init_multipart_upload", t)
            upload_id = init.upload_id

            for idx in range(plan.part_count):
                plen = plan.part_length(idx)
                label = "part %d/%d" % (idx + 1, plan.part_count)
                # 防御：非末 part 官方 min（planner 保证）。
                if idx < plan.part_count - 1 and plen < OSS_MIN_PART_BYTES:
                    raise UploadSizeMismatch(
                        "nonfinal part below OSS minimum (region=%s)"
                        % t.region)
                stream = SizedStreamPart(
                    fh, plen, uploader=self, io_chunk=self._io_chunk,
                    deadline=deadline, label=label)
                resp = self._call_with_budget(
                    lambda s=stream: bucket.upload_part(
                        t.temp_key, upload_id, idx + 1, s),
                    deadline, "upload_part %d" % (idx + 1), t)
                # 传输后核对流完整性（短读会在 read 中抛——这里防御
                # remaining>0 且未抛的异常形态）。
                if stream.remaining > 0:
                    raise UploadSizeMismatch(
                        "part %d incomplete (%d bytes unsent)"
                        % (idx + 1, stream.remaining))
                etag = (resp.etag or "").strip('"')
                parts.append(part_info_cls(idx + 1, etag))

            # 源 extra 探测（EOF 后 1 字节）。
            if fh.read(1):
                raise UploadSizeMismatch(
                    "source longer than expected_size (region=%s, "
                    "expected=%d)" % (t.region, plan.total_size))

            # D-R2-ACTUAL-BYTES：实际发送字节摘要 vs expected。
            actual_digest = self._hasher.hexdigest()
            actual = self._actual_bytes
            if actual != plan.total_size:
                raise UploadSizeMismatch(
                    "actual transmitted bytes %d != expected %d "
                    "(region=%s)" % (actual, plan.total_size, t.region))
            if actual_digest != expected_sha256:
                raise UploadDigestMismatch(
                    "actual transmitted sha256 does not match expected "
                    "(region=%s)" % t.region)

            self._call_with_budget(
                lambda: bucket.complete_multipart_upload(
                    t.temp_key, upload_id, parts),
                deadline, "complete_multipart_upload", t)
        except (UploadCancelled, UploadSizeMismatch,
                UploadDigestMismatch, UploadOssError):
            self._abort_multipart(bucket, upload_id, deadline)
            raise
        # receipt 如实：所有非零路径都是真实 multipart（含单 part——
        # init/part/complete 协议实际发生）。
        return UploadReceipt(region=t.region, bucket=t.bucket,
                             temp_key=t.temp_key,
                             upload_attempt=t.upload_attempt,
                             bytecount=actual,
                             sha256=actual_digest,
                             multipart=True,
                             part_count=len(parts))

    # ── per-dispatch 预算（D-R2-DEADLINE 核心修正）─────────────────────
    def _call_with_budget(self, call, deadline, phase, t, *,
                          ignore_cancel: bool = False):
        """每次实际网络调用：guard（close/deadline；cancel 可豁免——
        abort 清理路径需要）→ 修 bucket timeout=min(cap, remaining)
        （每次重算）→ dispatch → 返回后 postcheck。"""
        if self._closed:
            raise UploadCancelled("uploader is closed")
        if not ignore_cancel and self._cancelled.is_set():
            raise UploadCancelled(
                "upload cancelled before %s (region=%s)"
                % (phase, self._target.region))
        if not self._deadline_ok(deadline):
            raise UploadDeadlineExceeded(
                "deadline exhausted before %s (region=%s)"
                % (phase, self._target.region))
        remaining = deadline - time.monotonic()
        timeout = min(self._timeout_cap, max(remaining, 0.0))
        if self._bucket_ref is not None and timeout > 0:
            try:
                self._bucket_ref.timeout = timeout
            except Exception:  # noqa: BLE001
                pass
        failure = None
        try:
            resp = call()
        except self._upload_error_types():
            raise
        except Exception as exc:  # noqa: BLE001
            failure = self._classify_error(exc, phase, t)
        # Raising in the handler retains raw vendor details in __context__,
        # even with "from None". Cross this boundary only after it has exited.
        if failure is not None:
            raise failure
        if not ignore_cancel:
            self._post_call_check(deadline, phase)
        elif not self._deadline_ok(deadline):
            # abort 豁免 cancel 但仍守 deadline（返回后超预算即停重试）。
            raise UploadDeadlineExceeded(
                "deadline exceeded after %s (region=%s)"
                % (phase, self._target.region))
        return resp

    def _upload_error_types(self):
        return (UploadCancelled, UploadDeadlineExceeded,
                UploadSizeMismatch, UploadDigestMismatch, UploadOssError,
                UploadOutcomeUnknown)

    # ── 清理（仅本 attempt upload_id；每次 dispatch 亦按 remaining）──
    def _abort_multipart(self, bucket, upload_id, deadline) -> bool:
        """best-effort scoped abort——**绝不掩盖原错**（D-R3
        CLEANUP-MASKS-ORIGINAL）：

        - 只 abort 本次 attempt 的已知 upload_id（不 DELETE key）；
        - 已分类的网络/unknown/HTTP 清理失败**有界吞回**（safe 诊断
          记到 self._cleanup_diagnostic，不抛出）；
        - 原错（digest/size/cancel/schema/deadline）在 _run_multipart
          的 except 分支 re-raise——本方法任何失败路径都不改变上抛的
          原异常类型/终态性。
        """
        if upload_id is None:
            return True
        for _ in range(max(1, self._abort_attempts)):
            if not self._deadline_ok(deadline):
                self._cleanup_diagnostic = \
                    "abort skipped: deadline exhausted"
                return False
            try:
                # abort 豁免 cancel（清理须发出——cancelled 不等于服务端
                # 知道本次失败）；仍守 deadline。
                self._call_with_budget(
                    lambda: bucket.abort_multipart_upload(
                        self._target.temp_key, upload_id),
                    deadline, "abort_multipart_upload", self._target,
                    ignore_cancel=True)
                return True
            except UploadOssError as exc:
                if exc.status == 404:
                    return True  # 已干净（视为成功清理）
                # HTTP 清理失败：safe 诊断（类名+status，无 URL/body），
                # 有界重试后吞回。
                self._cleanup_diagnostic = \
                    "abort failed: %s status=%s" % (exc.kind, exc.status)
            except UploadOutcomeUnknown as exc:
                # 网络 ambiguous 清理失败：safe 诊断吞回（**不得**上抛
                # 覆盖原错——cleanup probe 反例根因）。
                self._cleanup_diagnostic = \
                    "abort network failure: %s" % exc.kind
            except (UploadDeadlineExceeded, UploadCancelled):
                self._cleanup_diagnostic = \
                    "abort stopped: deadline/cancel"
                return False
            if self._cancelled.is_set():
                return False
            time.sleep(min(self._abort_backoff,
                           max(0.0, deadline - time.monotonic())))
        return False

    # ── helpers ──
    def _load_oss2(self):
        if self._oss2 is not None:
            return self._oss2
        failure = None
        try:
            import oss2
        except ImportError:
            failure = UploadOssError("oss2 is not importable")
        if failure is not None:
            raise failure
        return oss2

    def _make_bucket(self, oss2, deadline):
        remaining = deadline - time.monotonic()
        timeout = min(self._timeout_cap, max(remaining, 0.0))
        t = self._target
        failure = None
        try:
            auth = oss2.StsAuth(t.access_key_id, t.access_key_secret,
                                t.security_token)
            session = self._make_session(oss2)
            self._session = session
            bucket = oss2.Bucket(auth, t.endpoint, t.bucket,
                                 connect_timeout=timeout,
                                 is_cname=self._is_cname,
                                 session=session)
            self._bucket_ref = bucket
            return bucket
        except ImportError:
            failure = UploadOssError("oss2 is not importable")
        except Exception as exc:  # noqa: BLE001 - 构造失败（含注入异常）
            # 已建的 owned session 由 upload() finally 关闭（代码审查项）。
            failure = UploadOssError(
                "bucket construction failed (%s)" % type(exc).__name__,
                kind="unknown", status=None, retryable=False,
                cause=exc)
        if failure is not None:
            raise failure

    def _make_session(self, oss2):
        """自建 owned session：禁未验证 redirect；exit 时 close。"""
        session = oss2.http.Session()
        raw_request = session.session.request

        def no_redirect_request(method, url, **kw):
            kw.setdefault("allow_redirects", False)
            return raw_request(method, url, **kw)
        session.session.request = no_redirect_request
        return session

    @staticmethod
    def _deadline_ok(deadline) -> bool:
        return time.monotonic() < deadline

    def _guard(self, deadline, phase: str) -> None:
        if self._closed or self._cancelled.is_set():
            raise UploadCancelled(
                "upload cancelled before %s (region=%s)"
                % (phase, self._target.region))
        if not self._deadline_ok(deadline):
            raise UploadDeadlineExceeded(
                "deadline exhausted before %s (region=%s)"
                % (phase, self._target.region))

    def _post_call_check(self, deadline, phase: str) -> None:
        if self._cancelled.is_set():
            raise UploadCancelled(
                "cancelled during %s (region=%s)"
                % (phase, self._target.region))
        if not self._deadline_ok(deadline):
            raise UploadDeadlineExceeded(
                "deadline exceeded after %s (region=%s)"
                % (phase, self._target.region))

    # ── 错误分类（D-R2-ERRORS 方向修正）───────────────────────────────
    def _classify_error(self, exc: BaseException, phase: str,
                        t: UploadTarget) -> UserDataUploadError:
        """仅已识别网络瞬态/5xx retryable；unknown/schema/auth 终态。

        - oss2 RequestError（真实网络异常包装，status 哨兵-1/-2）→
          UploadOutcomeUnknown（retryable=True，网络 ambiguous——不碰 key）；
        - requests 网络异常超集（ConnectionError/Timeout 族，无 status）
          → UploadOutcomeUnknown；
        - 真实 HTTP status（100..599）→ UploadOssError（5xx retryable，
          其余终态）；
        - 其他未知异常（ValueError 等）→ UploadOssError kind="unknown"
          **终态**（不冒充 retryable 网络错）。
        映射只保留安全类型诊断；调用方退出 handler 后再抛出，防止
        原 vendor cause/context/traceback 经异常诊断回显。
        """
        status = self._safe_status(exc)
        if self._is_network_transient(exc):
            return UploadOutcomeUnknown(
                "oss2 %s during %s (region=%s, status=unknown)" %
                (type(exc).__name__, phase, t.region),
                kind="outcome_unknown", status=None, retryable=True,
                cause=exc)
        if status is not None:
            retryable = 500 <= status < 600
            return UploadOssError(
                "oss2 %s during %s (region=%s, status=%d)" %
                (type(exc).__name__, phase, t.region, status),
                kind=type(exc).__name__, status=status,
                retryable=retryable, cause=exc)
        return UploadOssError(
            "unexpected %s during %s (region=%s)" %
            (type(exc).__name__, phase, t.region),
            kind="unknown", status=None, retryable=False, cause=exc)

    @staticmethod
    def _is_network_transient(exc: BaseException) -> bool:
        """已识别的网络瞬态判定（未知异常不冒充）。"""
        # oss2 RequestError（网络层包装——status 哨兵）。
        if type(exc).__name__ == "RequestError":
            return True
        # requests 网络异常族。
        mod = type(exc).__module__ or ""
        if mod.startswith("requests.") or mod.startswith("urllib3."):
            name = type(exc).__name__
            if any(k in name for k in ("Timeout", "ConnectionError",
                                       "ConnectTimeout", "ReadTimeout",
                                       "RetryError", "ChunkedEncodingError",
                                       "ProtocolError")):
                return True
        return False

    @staticmethod
    def _safe_status(exc: BaseException) -> int | None:
        status = getattr(exc, "status", None)
        if isinstance(status, bool) or not isinstance(status, int):
            return None
        if 100 <= status <= 599:
            return status
        return None
