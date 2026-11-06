"""transport.py — apiserver 控制面客户端（鉴权 + 元数据 + STS 签发）。

数据面从不在此发生；本模块只与 apiserver 通信。HTTP 用 stdlib http.client（保
header 原大小写，X-API-Key 不被 title-case），并允许注入一个 ``http_send``
可调用以便单测无网络。apiserver 业务错误码经 errors.exc_for_code 映射为异常。
"""
from __future__ import annotations

import contextlib
import json
import threading
import time
from typing import Any, Callable

from .cache import TTLCache, parse_expiry
from .errors import (RequestDeadlineExceeded, SchemaError, TransportError,
                     exc_for_biz_code, exc_for_code)
from .models import PERMISSION_VALUES
from .retry import retry_transient

DEFAULT_TIMEOUT = 30.0
DEFAULT_MAX_RESPONSE_BYTES = 8 * 1024 * 1024
MAX_RESPONSE_BYTES = 64 * 1024 * 1024


class ResponseTooLarge(SchemaError):
    """Nonretryable successful/unknown-status limit; retains no body/URL/cause."""
    def __init__(self):
        super().__init__("control response size limit exceeded")


def _response_size_error(status=None):
    # Oversized error bodies cannot provide a trustworthy business code, but
    # received HTTP headers already determine auth/retry policy. Keep that
    # status without retaining/decoding the discarded body or guessing a code.
    if isinstance(status, int) and not isinstance(status, bool) and 100 <= status <= 999 and not 200 <= status < 300:
        return TransportError("HTTP %d: control response size limit exceeded" % status,
                              status=status, biz_code=None, data=None)
    return ResponseTooLarge()


def _validate_response_limit(value):
    if type(value) is not int or not 1 <= value <= MAX_RESPONSE_BYTES:
        raise SchemaError("max_response_bytes must be a positive int <= 64MiB")
    return value

#: 空闲多久就**不再复用** keep-alive 连接（秒）。必须**小于**服务端空闲回收阈值：
#: 实测 apiserver/LB 约 30s 回收（20s 存活、40s 已死）。取 15s 留足余量。
#: 见 _KeepAliveSender._conn_for 的说明——这是正确性而非性能取舍。
MAX_IDLE_REUSE_SECONDS = 15.0
# STS 时长 apiserver 夹到 [900,3600]；作为缺失 expiration 时的保守回退 TTL：
# 下限 MIN、上限 MAX（即便调用方传了超大 duration，回退也不超过真实令牌寿命上限，
# 避免缓存一份"以为还有效、实际已过期"的令牌导致持续 403 无法自愈）。
MIN_STS_DURATION = 900
MAX_STS_DURATION = 3600

# http_send 签名：(method, url, headers, body_bytes|None, timeout) -> (status:int, text:str)
HttpSend = Callable[[str, str, dict, "bytes | None", float], "tuple[int, str]"]


class _KeepAliveSender:
    """线程本地 keep-alive HTTP 执行器：每线程每 (scheme,host,port) 复用一条连接。

    仅对安全读取在复用连接发送失败时，丢弃并重建、重试一次；发送异常并不能
    证明服务端未执行写入，因此写请求的重试只能由上层显式幂等策略决定。全新连接的失败
    直接抛出原始异常（``socket.timeout`` / ``OSError`` 等），交由上层重试策略判定。
    用 http.client 以保 header 原大小写（X-API-Key 不被 title-case）。每线程独立连接，
    天然线程安全。整块为真实网络路径，单测走注入的 fake_send，不覆此分支。
    """

    def __init__(self, max_response_bytes=DEFAULT_MAX_RESPONSE_BYTES) -> None:
        self._max_response_bytes = _validate_response_limit(max_response_bytes)
        self._local = threading.local()

    def _conns(self) -> dict:  # pragma: no cover - 真实网络
        conns = getattr(self._local, "conns", None)
        if conns is None:
            conns = {}
            self._local.conns = conns
        return conns

    def _conn_for(self, scheme, host, port, timeout):
        """返回 (conn, reused)：reused=True 表示取自缓存。

        **空闲过久的连接不复用**：缓存条目记 (conn, last_used)，空闲超过
        ``MAX_IDLE_REUSE_SECONDS`` 就关掉重建。这不是性能优化，是正确性——
        apiserver/LB 约 30s 回收空闲 keep-alive（实测 20s 存活、40s 已死），
        而复用一条已死连接时失败点落在 ``getresponse()``：那时请求已发出、
        服务端**是否已处理无法判定**，非幂等 POST 绝不能重发（见 __call__），
        于是只能硬失败。组合能力必然踩中——push 段 skopeo 推镜像/传 OSS 要几十秒，
        期间控制面连接一直空闲，紧随其后的 ingest POST 正好打在死连接上。
        主动淘汰把失败点提前到"新建连接"，从根上消除这个不可重试窗口。
        """
        import http.client

        key = (scheme, host, port)
        conns = self._conns()
        cached = conns.get(key)
        if cached is not None:
            conn, last_used = cached
            if time.time() - last_used <= MAX_IDLE_REUSE_SECONDS:
                # D1（deadline 穿透）：复用连接的超时**每次更新**为本次
                # timeout——两个层面：
                # ① conn.timeout 属性：server 关闭 keep-alive 后（sock
                #   为 None）下次请求会走 conn.connect() 重建，而
                #   connect() 用构造时的 self.timeout——不更新属性会
                #   沿用首次的长超时；
                # ② conn.sock.settimeout：sock 仍存活时 read/write 的
                #   socket 超时。
                # 两者都更新，不改共享 self.timeout 状态。
                conn.timeout = timeout
                sock = getattr(conn, "sock", None)
                if sock is not None:
                    # 0740 提示：设置失败不得静默沿用旧的长超时——
                    # 失败即关闭该连接走重建（重建用本次 timeout），宁弃
                    # 连接不弃预算。
                    try:
                        sock.settimeout(timeout)
                    except OSError:
                        conns.pop(key, None)
                        with contextlib.suppress(Exception):
                            conn.close()
                        return self._conn_for(scheme, host, port, timeout)
                return conn, True
            with contextlib.suppress(Exception):   # 超时未用：主动关掉重建
                conn.close()
            conns.pop(key, None)
        Conn = (http.client.HTTPSConnection if scheme == "https"
                else http.client.HTTPConnection)
        conn = Conn(host, port, timeout=timeout)
        conns[key] = (conn, time.time())
        return conn, False

    def _touch(self, key) -> None:
        """请求成功后刷新该连接的最近使用时间。"""
        cached = self._conns().get(key)
        if cached is not None:
            self._conns()[key] = (cached[0], time.time())

    def _read_body_bounded(self, resp, conn, key, *,
                           deadline_monotonic: float | None = None
                           ) -> str:
        """0938 修1（trickle 根因版）：**绝对 deadline 有界取消**。

        根因（Codex 实证）：``resp.read(64KiB)`` 在**单次调用内持续
        recv 直到块完成**——块前 settimeout 无法中断该次 read（socket
        有数据可读时永不超时）；status line/headers 慢流与内部重连同病。

        修法：**请求级 watchdog**——每个带绝对 deadline 的请求起一条
        后台守护线程，到点**强制 close 本请求的 conn**（close 会以
        OSError 中断一切阻塞中的 recv/read/getresponse/status 解析/
        重连 attempt）；请求成功完成即 cancel watchdog（**防旧 timer
        误关后续复用请求**——watchdog 绑定请求而非连接）。conn 被关后
        从缓存 pop（半途连接不可复用）。

        No-deadline callers retain their timeout/watchdog behavior, but all
        native reads now have the same byte bound before decode/JSON parsing.
        """
        def discard_owned():
            # A request may have been superseded by a reentrant test/adapter.
            # Close this response/connection; never evict a newer owner's entry.
            with contextlib.suppress(Exception):
                resp.close()
            with contextlib.suppress(Exception):
                conn.close()
            cached = self._conns().get(key)
            if cached is not None and cached[0] is conn:
                self._conns().pop(key, None)

        def overflow():
            discard_owned()
            raise _response_size_error(getattr(resp, "status", None)) from None

        getheader = getattr(resp, "getheader", None)
        length = getheader("Content-Length") if callable(getheader) else None
        if isinstance(length, str) and length.isascii() and length.isdecimal():
            # Compare text lengths first: hostile million-digit headers must not
            # make int() allocate or raise Python's digit-limit diagnostics.
            digits = length.lstrip("0") or "0"
            cap = str(self._max_response_bytes)
            if len(digits) > len(cap) or (len(digits) == len(cap) and digits > cap):
                overflow()
        buf = bytearray()
        while True:
            block = resp.read(min(64 * 1024, self._max_response_bytes + 1 - len(buf)))
            if not block:
                break
            if len(block) > self._max_response_bytes - len(buf):
                overflow()
            buf.extend(block)
            if deadline_monotonic is not None and time.monotonic() >= deadline_monotonic:
                try:
                    conn.close()
                finally:
                    cached = self._conns().get(key)
                    if cached is not None and cached[0] is conn:
                        self._conns().pop(key, None)
                raise RequestDeadlineExceeded(
                    "request budget exhausted while reading response body")
        # Preserve legacy HTTP error status/retry classification for non-UTF8
        # HTML bodies. A successful JSON control object may never change keys
        # through replacement decoding. Raise outside except: no raw decoder
        # exception/body survives as the safe error's cause/context.
        text = None
        try:
            text = bytes(buf).decode("utf-8", errors=("strict" if 200 <= getattr(resp, "status", 200) < 300 else "replace"))
        except UnicodeDecodeError:
            pass
        if text is None:
            discard_owned()
            raise SchemaError("invalid UTF-8 in successful control response") from None
        return text

    _WATCHDOG_SENTINEL = object()

    def _call_with_request_watchdog(self, fn, key, deadline_monotonic):
        """1020 修①②：请求级有界取消（真实 socket/response 捕获+完整
        claim/cancel/generation 协议）。

        修①（HTTP/1.0 Connection:close）：``getresponse`` 会把
        ``conn.sock`` 置 None（response 持有 socket file——
        ``resp.fp.raw._sock``）——watchdog 不可只到点 ``getattr(conn,
        "sock")``。owner 在 rebind 时**捕获本请求真实 sock 引用**：
        优先 ``conn.sock``；getresponse 后由 ``_rebind_response`` 捕获
        ``resp.fp.raw._sock``（HTTP/1.0 close 场景）。

        修②（race 协议落码）：
        - watch 的 close/pop 前在**锁内重新核对 state+generation 快照**
          ——claim 与 close 之间 fn 可能已 cancel 并开始下一请求
          （新 rebind bump gen）——旧回调核对失败即退出（**不能删新
          conn 的缓存条目**）；
        - fn 正常返回的 **already-claimed 路径**：返回值到达但状态为
          claimed（过期响应）——不 pop 不返回成功语义，转
          RequestDeadlineExceeded（不能让过期 claim 的取消残留）；
        - fn 抛中断类异常且 claimed → 归一 RequestDeadlineExceeded。
        """
        import threading
        from .errors import RequestDeadlineExceeded

        # owner 线程捕获（watch 线程操作 owner 的 threadlocal 缓存）。
        owner_conns = self._conns()
        lock = threading.Lock()
        state = {"s": "active"}          # active | claimed | cancelled
        generation = {"g": 0}
        holder = {}

        def _rebind(conn):
            """owner 锁内更新当前 conn+bump gen（并捕获此刻 conn.sock）。
            """
            with lock:
                generation["g"] += 1
                holder["conn"] = conn
                holder["gen"] = generation["g"]
                # 修①：捕获**本请求真实 sock**（此刻 conn.sock 可能尚
                # 在；HTTP/1.0 close 下 getresponse 后置 None——由
                # rebind_response 补捕获）。
                sock = getattr(conn, "sock", None)
                if sock is not None:
                    holder["sock"] = sock

        def _rebind_response(resp):
            """owner 在 getresponse 后锁内捕获 response 的底层 sock
            （HTTP/1.0 Connection:close：conn.sock 已置 None，真实
            socket 在 resp.fp.raw._sock）。"""
            with lock:
                fp = getattr(resp, "fp", None)
                raw = getattr(fp, "raw", None)
                sock = getattr(raw, "_sock", None) if raw is not None \
                    else getattr(fp, "_sock", None)
                if sock is not None:
                    holder["sock"] = sock

        class _ClaimedEarly(RequestDeadlineExceeded):
            """1120 修：**源头归一**——直接 subclass 共同 typed
            ``RequestDeadlineExceeded``（clock expired 但 state active
            的早期拒绝形态）。即使任何调用路径漏过 except 映射，调用方
            看到的仍是共同 deadline 类型（绝不泄漏私有异常类型）。"""
            pass

        def _raise_if_expired():
            """1112 修（clock 门禁）：owner 线程为 **clock authority**——
            不依赖取消线程的调度及时性（取消线程若调度延迟，state 仍
            active 而时钟已过——受控延迟调度 probe 实证：过期后第二
            IO 在 .042 发出且 sender 返回 success）。

            每个内部 attempt/IO 前**硬检 monotonic**：
            - ``state == claimed``（取消线程已 claim）→ 拒；
            - ``time.monotonic() >= deadline_monotonic``（**硬时钟**
              过期，无论取消线程是否已被调度）→ 拒。
            """
            import time as _t
            with lock:
                if state["s"] == "claimed":
                    raise _ClaimedEarly()
            if _t.monotonic() >= deadline_monotonic:
                raise _ClaimedEarly()

        holder["rebind"] = _rebind
        holder["rebind_response"] = _rebind_response
        holder["check_claimed"] = _raise_if_expired

        def _watch():
            import socket as _socket
            import time as _time
            while _time.monotonic() < deadline_monotonic:
                with lock:
                    if state["s"] != "active":
                        return
                _time.sleep(min(0.01, max(0.0,
                                          deadline_monotonic
                                          - _time.monotonic())))
            # claim（锁内 active→claimed；已 cancel 则退出）。
            with lock:
                if state["s"] != "active":
                    return
                state["s"] = "claimed"
                # 锁内快照（claim 时刻的 state+gen+sock+conn）。
                claimed_gen = generation["g"]
                claimed_sock = holder.get("sock")
                claimed_conn = holder.get("conn")
            # 中断动作（锁外执行——shutdown/close 可能阻塞）：对
            # **claim 时刻捕获的真实 sock**执行（HTTP/1.0 close 场景
            # conn.sock=None 但 holder["sock"] 仍持真实 socket）。
            if claimed_sock is not None:
                try:
                    claimed_sock.shutdown(_socket.SHUT_RDWR)
                except OSError:
                    pass
                try:
                    claimed_sock.close()
                except OSError:
                    pass
            if claimed_conn is not None:
                try:
                    claimed_conn.close()
                except Exception:
                    pass
            # 1055 修①：**callback 不做任何缓存变更**——只取消 claim
            # 时刻捕获的 sock/conn。缓存清理**只由 owner 线程**执行（fn
            # 的异常/迟到拒绝路径在 owner 侧 pop）——旧回调晚到的任何
            # pop 都可能删掉新请求的缓存条目（每 helper 自己的 gen 守
            # 不了**另一请求**的条目；受控交错 probe 实证）。
            # （原"close 后锁内重核再 pop"已移除——即使重核通过，
            # owner 侧清理也足够且更安全。）

        th = threading.Thread(target=_watch, daemon=True)
        th.start()
        result = self._WATCHDOG_SENTINEL
        try:
            result = fn(holder)
        except (OSError, TimeoutError, AttributeError, ValueError,
                _ClaimedEarly):
            with lock:
                was_claimed = state["s"] == "claimed"
            # 1112：claimed 或 **硬时钟已过**（取消线程调度延迟）都归一
            # deadline——owner 是 clock authority。
            import time as _t
            clock_expired = _t.monotonic() >= deadline_monotonic
            if was_claimed or clock_expired:
                owner_conns.pop(key, None)
                raise RequestDeadlineExceeded(
                    "request budget exhausted (connection cancelled by "
                    "deadline watchdog or owner clock)") from None
            raise
        finally:
            with lock:
                final_state = state["s"]
                if final_state == "active":
                    state["s"] = "cancelled"
                holder.pop("sock", None)   # 释放 sock 引用
        # 1112 修：**成功完成 clock 后验**——返回值到达且 state 非
        # claimed（取消线程未及 claim——调度延迟），但**硬时钟已过**：
        # 仍不得当成功（owner 是 clock authority，不依赖取消线程）。
        if final_state == "claimed":
            owner_conns.pop(key, None)
            raise RequestDeadlineExceeded(
                "request budget exhausted (late response refused after "
                "deadline claim)")
        import time as _t
        if _t.monotonic() >= deadline_monotonic:
            owner_conns.pop(key, None)
            raise RequestDeadlineExceeded(
                "request budget exhausted (late success refused by "
                "owner clock authority)")
        return result

    def __call__(self, method, url, headers, body, timeout,
                 deadline_monotonic: float | None = None):
        import http.client
        from urllib.parse import urlsplit

        u = urlsplit(url)
        path = u.path + (("?" + u.query) if u.query else "")
        hdrs = dict(headers)
        hdrs.setdefault("Connection", "keep-alive")
        key = (u.scheme, u.hostname, u.port)

        if deadline_monotonic is None:
            return self._attempt_http(u, method, path, hdrs, body, timeout,
                                      key)
        # 0938 修1：**请求级 watchdog** 覆盖全部阻塞阶段（request/
        # getresponse/status/headers/body/内部重连）——绝对 deadline
        # 到点强制 close conn（真实中断）；正常完成即 cancel（旧 timer
        # 不影响后续复用请求——watchdog 绑定请求而非连接）。
        from .errors import RequestDeadlineExceeded

        def _guarded(holder):
            # holder["conn"] 在 _attempt_http 内每 attempt 更新，使
            # watchdog 总能 close 到**当前**连接。
            return self._attempt_http(u, method, path, hdrs, body, timeout,
                                      key, holder,
                                      deadline_monotonic=deadline_monotonic)

        try:
            return self._call_with_request_watchdog(
                _guarded, key, deadline_monotonic)
        except RequestDeadlineExceeded:
            self._conns().pop(key, None)
            raise

    def _attempt_http(self, u, method, path, hdrs, body, timeout, key,
                      holder=None, deadline_monotonic=None):
        import http.client
        for attempt in (1, 2):
            conn, reused = self._conn_for(u.scheme, u.hostname, u.port,
                                          timeout)
            if holder is not None:
                # 0953 修2：锁内 rebind（generation 递增——旧回调不能
                # close 新代次连接；内部重连 attempt 同预算同代次核对）。
                holder["rebind"](conn)
            # Either send or receive failure can have an unknown delivery
            # outcome. Never replay a write here, including on a reused
            # connection: conn.request() may fail after bytes reached the server.
            # Explicit idempotency/retry belongs to Transport.request().
            if holder is not None:
                # 1112 修：**IO 前**（连接后、请求发出前）state+monotonic
                # 双检——内部重连 attempt 不得在过期后发新 IO（硬时钟
                # 兜底：取消线程调度延迟时 state 尚未 claimed）。
                holder["check_claimed"]()
            try:
                conn.request(method, path, body=body, headers=hdrs)
            except (OSError, http.client.HTTPException):
                try:
                    conn.close()
                finally:
                    self._conns().pop(key, None)
                # Only safe reads may be replayed inside the native sender.
                if reused and attempt == 1 and method in ("GET", "HEAD"):
                    continue
                raise
            try:
                resp = conn.getresponse()
                if holder is not None:
                    # 1020 修①：getresponse 后捕获 response 的底层
                    # sock（HTTP/1.0 Connection:close——conn.sock 已置
                    # None，真实 socket 在 resp.fp.raw._sock）。
                    holder["rebind_response"](resp)
                out = (resp.status,
                       self._read_body_bounded(
                           resp, conn, key,
                           deadline_monotonic=deadline_monotonic))
                self._touch(key)      # 成功即刷新空闲计时
                return out
            except (OSError, http.client.HTTPException):
                try:
                    conn.close()
                finally:
                    self._conns().pop(key, None)
                raise   # 接收阶段失败：不重发（可能已处理），保留异常类型供上层判定
        raise AssertionError("unreachable")  # pragma: no cover - 防御：循环必已 return/raise


def _default_http_send(method: str, url: str, headers: dict,
                       body: bytes | None, timeout: float) -> tuple[int, str]:
    """Legacy five-argument native helper; same bounded reader, one connection.

    Explicit injected senders own their allocation, but this library-provided
    helper must not retain an unbounded resp.read() path.
    """
    sender = _KeepAliveSender()
    try:
        return sender(method, url, headers, body, timeout)
    finally:
        for conn, _ in sender._conns().values():
            with contextlib.suppress(Exception):
                conn.close()


class Transport:
    """apiserver 控制面 client。

    Parameters
    ----------
    base_url : apiserver 根地址
    token    : X-API-Key（身份 token）
    env      : Env 头，默认空串（不内置具体环境名；由调用方/apiserver 决定路由）
    http_send: 可注入的 HTTP 执行器（单测用 fake，默认真实 http.client）。
        自定义 sender 自行保证读取期间的资源边界；本类仅在返回后、JSON前检查其文本。
    max_response_bytes: 控制面响应上限，默认8MiB，可显式设置为正整数至64MiB。
        原生HTTP在读入期间限制字节；成功JSON严格UTF8，错误HTTP分类保持原语义。
    """

    def __init__(self, base_url: str, token: str, *, env: str = "",
                 http_send: HttpSend | None = None,
                 timeout: float = DEFAULT_TIMEOUT,
                 retry_attempts: int = 3,
                 cache_credentials: bool = True,
                 max_response_bytes: int = DEFAULT_MAX_RESPONSE_BYTES) -> None:
        self.max_response_bytes = _validate_response_limit(max_response_bytes)
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.env = env
        self.timeout = timeout
        self._send = http_send or _KeepAliveSender(self.max_response_bytes)
        # 配置缓存始终按 transport 实例与主体隔离，不能跨身份共享发现结果。
        self._custom_send = http_send is not None
        self._retry_attempts = retry_attempts
        # STS 凭据缓存：key=("oss",bucket,prefix,duration) / ("acr",host,duration)，
        # 按签发返回的 Expiration 失效（留 60s 安全余量）。关缓存则每次现签。
        self._cred_cache = TTLCache() if cache_credentials else None
        # Single-flight lock for STS signing: ensures only one thread calls sign()
        # per cache miss; all concurrent waiters get the same cached result.
        # Without this, multiple threads each call sign() and get different STS
        # tokens, causing bucket cache token-mismatch → retire old bucket →
        # "Connection pool shut down" when GC closes the old pool mid-flight.
        self._cred_lock = threading.Lock()

    # ── 低层 ──
    def _headers(self, extra_headers: dict | None = None) -> dict:
        headers = {"X-API-Key": self.token, "Env": self.env,
                   "Content-Type": "application/json"}
        protected = {key.lower() for key in headers}
        for key, value in (extra_headers or {}).items():
            if not isinstance(key, str) or key.lower() in protected:
                raise SchemaError(
                    f"per-request header {key!r} may not override transport headers")
            headers[key] = value
        return headers

    def request(self, method: str, path: str, body: dict | None = None, *,
                idempotent: bool | None = None,
                headers: dict | None = None,
                timeout: float | None = None) -> dict:
        """发一次控制面请求，返回解析后的 data。非 2xx 或业务 success=false 抛异常。

        仅对**幂等**请求做瞬时故障重试（默认 GET 幂等，其余不重试），避免把 5xx/
        连接中断后重发导致 ingest/release/register/commit 等**非幂等**写重复提交。
        显式传 ``idempotent=True`` 可为幂等的写（如凭据签发）开启重试。

        ``timeout``（additive 可选，默认 None=沿用 ``self.timeout``，既有
        调用方语义零变化）：per-request 超时上限，供调用方按剩余 deadline
        逐请求收窄（双写客户端预算穿透用）。不改 ``self.timeout`` 状态、
        不改重试策略/连接复用。
        """
        if not self.base_url:
            raise SchemaError(
                "apiserver 根地址未配置；请通过 AP_BASE_URL 提供"
                "（旧别名 INSTANCEREPO_API_BASE 仍兼容；SDK 不内置任何域名，见部署文档）")
        retry = method in ("GET", "HEAD") if idempotent is None else idempotent
        # 0842 裁决（retry scope 放行）：``timeout=finite`` 时**一次派生
        # 绝对 monotonic deadline**，覆盖全部 attempt/退避——每次 attempt
        # 拿**当时剩余量**作 per-attempt timeout（不重置新全额预算）；
        # sleep 夹剩余（retry_transient 内实现）；耗尽零新 IO（首次也无
        # 豁免）；timeout=None 恒旧语义（不派生 deadline，不改共享
        # self.timeout）。成功后 postcheck 在 retry 外层做。
        deadline = None
        effective_timeout = timeout
        if timeout is not None:
            import math
            valid = False
            try:
                valid = type(timeout) in (int, float) and math.isfinite(timeout) and timeout >= 0
            except (ValueError, OverflowError):
                pass
            if not valid:
                raise SchemaError("invalid per-request timeout: must be finite and nonnegative")
            if timeout == 0:
                raise RequestDeadlineExceeded(
                    "request budget exhausted before any IO (timeout=0)")
            deadline = time.monotonic() + timeout
        if not retry:
            result = self._request_once(method, path, body,
                                        headers=headers,
                                        timeout=effective_timeout,
                                        deadline_monotonic=deadline)
            # 成功后 postcheck：非重试路径同样拒绝超预算成功。
            if deadline is not None and deadline - time.monotonic() <= 0:
                raise RequestDeadlineExceeded(
                    "request budget exhausted after response (late "
                    "success refused)")
            return result

        def _attempt():
            if deadline is not None:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise RequestDeadlineExceeded(
                        "request budget exhausted before attempt")
                return self._request_once(
                    method, path, body, headers=headers, timeout=remaining,
                    deadline_monotonic=deadline)
            return self._request_once(
                method, path, body, headers=headers,
                timeout=effective_timeout)

        result = retry_transient(
            _attempt, attempts=self._retry_attempts,
            deadline_monotonic=deadline)
        # 成功后 postcheck（仅正常返回路径——传输/鉴权原错误已在
        # retry_transient 内原样上抛，不被 deadline 信号覆盖）：响应到达
        # 但预算已耗尽 → 拒绝超预算成功。
        if deadline is not None and deadline - time.monotonic() <= 0:
            raise RequestDeadlineExceeded(
                "request budget exhausted after response (late success "
                "refused)")
        return result

    def request_with_meta(self, method: str, path: str, *,
                          timeout: float | None = None) -> tuple[dict, dict | None]:
        """Return actual data + pagination; optional timeout bounds all attempts.

        Omitted timeout preserves existing behavior. The native sender retains
        its existing body cap/connection owner; custom senders keep five args.
        """
        if not self.base_url:
            raise SchemaError("apiserver base URL is not configured")
        deadline = None
        if timeout is not None:
            import math
            valid = False
            try:
                valid = type(timeout) in (int, float) and math.isfinite(timeout) and timeout >= 0
            except (ValueError, OverflowError):
                pass
            if not valid:
                raise SchemaError("invalid metadata request timeout")
            if timeout == 0:
                raise RequestDeadlineExceeded("metadata request budget exhausted before IO")
            deadline = time.monotonic() + timeout

        def attempt():
            if deadline is None:
                return self._request_once_with_meta(method, path)
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise RequestDeadlineExceeded("metadata request budget exhausted before attempt")
            return self._request_once_with_meta(method, path, timeout=remaining,
                deadline_monotonic=deadline)

        result = (retry_transient(attempt, attempts=self._retry_attempts,
                  deadline_monotonic=deadline) if method == "GET" else attempt())
        if deadline is not None and time.monotonic() >= deadline:
            raise RequestDeadlineExceeded("metadata request exceeded budget")
        return result

    def _request_once(self, method: str, path: str,
                      body: dict | None = None, *,
                      headers: dict | None = None,
                      timeout: float | None = None,
                      deadline_monotonic: float | None = None) -> dict:
        data, _ = self._request_once_with_meta(
            method, path, body, headers=headers, timeout=timeout,
            deadline_monotonic=deadline_monotonic)
        return data

    def _request_once_with_meta(self, method: str, path: str,
                                body: dict | None = None, *,
                                headers: dict | None = None,
                                timeout: float | None = None,
                                deadline_monotonic: float | None = None
                                ) -> tuple[dict, dict | None]:
        url = self.base_url + path
        raw = json.dumps(body).encode("utf-8") if body is not None else None
        effective_timeout = self.timeout if timeout is None else timeout
        # 0925 修1：deadline 只传给**真实** _KeepAliveSender（支持
        # deadline_monotonic 参数；注入 fake_send 按原五参形态调用——
        # IO 前类型判定，无执行后 TypeError 重放）。
        if (deadline_monotonic is not None
                and isinstance(self._send, _KeepAliveSender)):
            status, text = self._send(
                method, url, self._headers(headers), raw, effective_timeout,
                deadline_monotonic=deadline_monotonic)
        else:
            status, text = self._send(
                method, url, self._headers(headers), raw, effective_timeout)
        # Custom senders keep their exact five-argument interface. They own
        # network/read allocation; this post-return guard bounds SDK JSON work,
        # and is not a claim about their internal read-time memory behavior.
        if not isinstance(self._send, _KeepAliveSender):
            if not isinstance(text, str):
                raise SchemaError("control sender must return response text")
            if len(text) > self.max_response_bytes or len(text.encode("utf-8", errors="surrogatepass")) > self.max_response_bytes:
                raise _response_size_error(status) from None
        try:
            parsed = json.loads(text) if text.strip() else {}
        except json.JSONDecodeError:
            parsed = {}
        if status < 200 or status >= 300:
            code = parsed.get("code") if isinstance(parsed, dict) else None
            msg = parsed.get("message") if isinstance(parsed, dict) else text[:300]
            # 可选结构化错误负载：仅 dict 透传（异常构造侧对非 dict/缺失安全回退
            # 空 dict），绝不拼进 message——凭据等秘密值不随异常 str/repr 进日志。
            data = parsed.get("data") if isinstance(parsed, dict) else None
            if not isinstance(data, dict):
                data = None
            # R1返修②：结构化 JSON 响应（parsed 为非空 dict，即真实含 code/message/
            # data 等键的 JSON）缺失/空 message 时，用不含 data 的通用 HTTP 信息
            # （"HTTP <status>"）做 message——否则 fallback 会把整段响应文本（可能
            # 含 data 里的秘密值）带进异常 str/repr。非 JSON（含解码失败得 {}）保留
            # base 截断行为（text[:300]）；正常 message 不隐藏、不加前缀覆盖。
            if not msg and isinstance(parsed, dict) and parsed:
                msg = f"HTTP {status}"
            # apiserver 业务错误码为字符串时映射；数字业务码经 BIZ_CODE_TO_EXC 映射为
            # 类型化异常（Dataset RBAC 等），未知数字码再回退 TransportError 并透传
            # biz_code（92001/92003 同为 404，语义不同，调用方需据此区分）。
            # R1返修①：字符串码路径不传 status——base 语义如此，且 retry.is_transient
            # 按 .status 判 5xx 重试，补 status 会让 503 等误触发重试、改变调用次数。
            if isinstance(code, str):
                raise exc_for_code(code, msg or "", data=data)
            if isinstance(code, int):
                raise exc_for_biz_code(code, msg or "", status=status, data=data)
            # 无 code：base 形态 "HTTP <status>: <msg|text[:300]>"；但 msg 为通用
            # 信息（"HTTP <status>"，无服务端 message 可拼）时不重复加前缀。
            if msg and msg != f"HTTP {status}":
                raise TransportError(f"HTTP {status}: {msg}",
                                     status=status, biz_code=None, data=data)
            raise TransportError(msg or f"HTTP {status}: {text[:300]}",
                                 status=status, biz_code=None, data=data)
        # 兼容 apiserver 统一信封：键集 ⊆ {code,message,data,pagination} 且含 data 时取 data。
        # **pagination 是关键豁免**——分页列表响应形如 {code,message,data,pagination}，早先
        # 白名单只有 {code,message,data}，多出的 pagination 使其被判为非信封→不解包，导致
        # versions.list/datasets 等分页列表把整个信封当业务对象、遍历出字符串键而崩（真机
        # 才暴露，fake 单测未带 pagination）。保留"额外未知键则不解包"的既有语义，仅新增
        # pagination 豁免，避免误伤 {data,total} 这类真实业务对象。
        if isinstance(parsed, dict) and "data" in parsed and set(parsed) <= {
                "code", "message", "data", "pagination"}:
            return parsed["data"], parsed.get("pagination")
        return parsed, None

    # ── 元数据实体 ──
    def get(self, path: str, *, timeout: float | None = None) -> dict:
        return self.request("GET", path, timeout=timeout)

    def post(self, path: str, body: dict, *, idempotent: bool = False,
             headers: dict | None = None,
             timeout: float | None = None) -> dict:
        return self.request(
            "POST", path, body, idempotent=idempotent, headers=headers,
            timeout=timeout)

    def patch(self, path: str, body: dict) -> dict:
        return self.request("PATCH", path, body)

    def delete(self, path: str) -> dict:
        # DELETE 无 body、幂等（重复删同键第二次 404，由调用方按语义处理）。
        return self.request("DELETE", path, idempotent=True)

    # ── STS 临时凭证（对齐 apiserver feat/credentials-sts 契约）──
    # POST /apis/v1/credentials，X-API-Key 鉴权。apiserver 按 resource 分别用
    # AssumeRole（OSS，收窄 bucket+prefix；list 仅授予系统白名单调用方）或 ACR GetAuthorizationToken
    # （返回 cr_temp_user + 短期 docker 令牌）签发。返回体为 SHOUTY_SNAKE_CASE，
    # 这里归一化成稳定小写 dict，屏蔽命名细节。全程无长期 AK/SK、无明文用户名密码。
    @staticmethod
    def _require(resp: dict, key: str) -> Any:
        """取签发响应里的必填字段；缺失/结构异常时抛清晰的 TransportError
        （而非裸 KeyError），保证契约破坏对调用方统一为 InstanceRepoError。

        安全：签发响应体本身是密钥材料（AK/SK、docker 令牌）。缺字段时**只**报
        存在的 key 名，绝不把 str(resp) 的**值**带进异常/日志（否则一份缺了某字段
        的部分响应会把 secret 泄进日志）。"""
        if not isinstance(resp, dict) or key not in resp:
            present = sorted(resp) if isinstance(resp, dict) else type(resp).__name__
            raise TransportError(
                f"credentials response missing {key!r}; present keys: {present}")
        return resp[key]

    def _cached_cred(self, key: tuple, sign, *, fallback_ttl: float):
        """通用凭据缓存：命中未过期直接返回；否则调用 ``sign`` 现签并入缓存。

        Single-flight: 多线程并发 miss 时只有一个线程调 sign()（网络请求），
        其余线程等待后拿缓存结果。确保同一 key 全线程拿到同一个 STS token，
        避免 bucket 缓存因 token 不一致而 retire 仍在用的 bucket。
        """
        if self._cred_cache is not None:
            hit = self._cred_cache.get(key)
            if hit is not None:
                return hit

        # Single-flight: 只有一个线程执行 sign()，其余等待后 double-check 缓存。
        with self._cred_lock:
            if self._cred_cache is not None:
                hit = self._cred_cache.get(key)
                if hit is not None:
                    return hit
            cred = sign()
            if self._cred_cache is not None:
                exp = parse_expiry(cred.get("expiration"))
                if exp is None:
                    exp = time.time() + fallback_ttl
                self._cred_cache.put(key, cred, exp)
        return cred

    def get_oss_credentials(self, bucket: str, prefix: str, *,
                            duration_seconds: int | None = None,
                            dataset_id: str | None = None,
                            dataset_name: str | None = None,
                            permission: str | None = None,
                            list_only: bool = False,
                            dataset_source: str | None = None) -> dict:
        """换 OSS STS 三元组（收窄到 bucket+prefix）。返回归一化小写字段。

        同 (bucket,prefix,duration,dataset,permission,list_only,dataset_source)
        在有效期内复用缓存，把 N 次签发降到 ~1 次。dataset_id / dataset_name
        至少传一个（细粒度授权场景），二者可并存，服务端校验一致性。

        ``permission``（可选，admin/writer/reader）是**权限封顶**：apiserver 取
        ``min(调用方真实角色, permission)``，**只能收窄不能提权**——传 admin 不会把
        reader 变成 admin。用途是最小权限原则（只读任务显式请求 reader，即便自己是
        admin），以及避免把可写令牌交给下游只读组件。admin 与 writer 在 STS 策略层等价，
        真正有区别的是 reader（只给 GetObject）。ACR 分支不支持该字段（镜像令牌是实例级的）。

        ``list_only`` 是**发现模式开关**（与 permission 封顶正交）：True 时签发仅含
        oss:ListObjects + oss:GetBucketInfo 的令牌，跳过 DatasetRBAC 检查，用于未注册
        dataset 的 OSS 回退目录探测。二者可并存（list_only 分支优先）。

        ``dataset_source``（可选，"db"/"oss"）指定数据集管理源：
        - 空/"db"（默认）：走 MongoDB 注册 + RBAC 授权流程
        - "oss"：纯 OSS 模式，跳过 RBAC，dataset_name/dataset_id 可不填，
          直接按 bucket+prefix 签发 STS
        """
        # 空串与 None 一律视为"不封顶"（与 Go 的 Permission == "" 语义对齐）。
        if permission and permission not in PERMISSION_VALUES:
            raise SchemaError(
                f"invalid permission '{permission}'; valid values: "
                f"{', '.join(PERMISSION_VALUES)}")
        if dataset_source and dataset_source not in ("db", "oss"):
            raise SchemaError(
                f"invalid dataset_source '{dataset_source}'; valid values: db, oss")

        def sign() -> dict:
            body: dict[str, Any] = {"resource": "oss",
                                    "oss_bucket": bucket, "oss_prefix": prefix}
            if duration_seconds is not None:
                body["duration_seconds"] = duration_seconds
            if dataset_id is not None:
                body["dataset_id"] = dataset_id
            if dataset_name is not None:
                body["dataset_name"] = dataset_name
            if permission:
                body["permission"] = permission
            if list_only:
                body["list_only"] = True
            if dataset_source:
                body["dataset_source"] = dataset_source
            r = self.post("/apis/v1/credentials", body, idempotent=True)
            return {
                "access_key_id": self._require(r, "OSS_ACCESS_KEY_ID"),
                "access_key_secret": self._require(r, "OSS_ACCESS_KEY_SECRET"),
                "security_token": self._require(r, "OSS_SECURITY_TOKEN"),
                "endpoint": self._require(r, "OSS_ENDPOINT"),
                "bucket": r.get("OSS_BUCKET", bucket),
                "region": r.get("OSS_REGION", ""),
                "prefix": r.get("OSS_Prefix", prefix),
                "expiration": r.get("OSS_Expiration", ""),
            }

        ttl = float(min(duration_seconds or MIN_STS_DURATION, MAX_STS_DURATION))
        # permission、list_only、dataset_source 都必须进缓存 key：否则请求 reader 封顶的调用方可能
        # 命中此前那份未封顶（可写）的缓存令牌，权限收窄被静默绕过；list-only 令牌
        # 也可能被普通请求复用（反之亦然），发现模式与读写模式互相污染；
        # oss 模式凭据不能被 db 模式复用（反之亦然）。
        cache_key = ("oss", bucket, prefix, duration_seconds,
                     dataset_id, dataset_name, permission or None, list_only,
                     dataset_source or None)
        return self._cached_cred(cache_key, sign, fallback_ttl=ttl)

    def get_acr_credentials(self, acr_registry_url: str, *,
                            duration_seconds: int | None = None) -> dict:
        """换 ACR 临时 docker 登录令牌（username=cr_temp_user + token）。

        用于写入 skopeo authfile 做私有仓推拉，替代长期用户名密码/AK-SK。返回
        归一化小写字段；同 registry 在有效期内复用缓存。"""
        def sign() -> dict:
            body: dict[str, Any] = {"resource": "acr",
                                    "acr_registry_url": acr_registry_url}
            if duration_seconds is not None:
                body["duration_seconds"] = duration_seconds
            r = self.post("/apis/v1/credentials", body, idempotent=True)
            return {
                "username": self._require(r, "ACR_USERNAME"),
                "token": self._require(r, "ACR_AUTHORIZATION_TOKEN"),
                "endpoint": r.get("ACR_ENDPOINT", ""),
                "instance_id": r.get("ACR_INSTANCE_ID", ""),
                "region": r.get("ACR_REGION", ""),
                "namespace": r.get("ACR_NAMESPACE", ""),
                "expiration": r.get("ACR_Expiration", ""),
            }

        ttl = float(min(duration_seconds or MIN_STS_DURATION, MAX_STS_DURATION))
        return self._cached_cred(("acr", acr_registry_url, duration_seconds), sign,
                                 fallback_ttl=ttl)
