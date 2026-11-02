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
from .errors import SchemaError, TransportError, exc_for_biz_code, exc_for_code
from .models import PERMISSION_VALUES
from .retry import retry_transient

DEFAULT_TIMEOUT = 30.0

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

    仅当复用的连接失效（对端 idle 关闭 → 写入即失败，请求必未被处理）时，丢弃并
    重建、重试一次——这对任何方法都安全（不会重复提交非幂等请求）；全新连接的失败
    直接抛出原始异常（``socket.timeout`` / ``OSError`` 等），交由上层重试策略判定。
    用 http.client 以保 header 原大小写（X-API-Key 不被 title-case）。每线程独立连接，
    天然线程安全。整块为真实网络路径，单测走注入的 fake_send，不覆此分支。
    """

    def __init__(self) -> None:  # pragma: no cover - 真实网络
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

    def __call__(self, method, url, headers, body, timeout):
        import http.client
        from urllib.parse import urlsplit

        u = urlsplit(url)
        path = u.path + (("?" + u.query) if u.query else "")
        hdrs = dict(headers)
        hdrs.setdefault("Connection", "keep-alive")
        key = (u.scheme, u.hostname, u.port)
        for attempt in (1, 2):
            conn, reused = self._conn_for(u.scheme, u.hostname, u.port, timeout)
            # 发送阶段与接收阶段必须分开 try：只有 conn.request() 失败（请求**尚未送达**）
            # 才可在复用连接上安全重发；conn.getresponse() 失败时请求已完整发出、服务端
            # 可能已处理（非幂等 POST 如 ingest/:commit/feedback-append 会被重复提交），
            # 绝不能在这里静默重发——关连接后原样抛出，交给上层幂等感知的重试策略判定。
            try:
                conn.request(method, path, body=body, headers=hdrs)
            except (OSError, http.client.HTTPException):
                try:
                    conn.close()
                finally:
                    self._conns().pop(key, None)
                # 仅复用连接的首次发送失败才重试（stale keep-alive，请求未被处理）。
                if reused and attempt == 1:
                    continue
                raise
            try:
                resp = conn.getresponse()
                out = resp.status, resp.read().decode("utf-8", errors="replace")
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
                       body: bytes | None, timeout: float) -> tuple[int, str]:  # pragma: no cover
    """真实 HTTP（http.client，保 header 大小写）。单测走注入的 fake，不覆此分支。"""
    import http.client
    from urllib.parse import urlsplit

    u = urlsplit(url)
    path = u.path + (("?" + u.query) if u.query else "")
    Conn = (http.client.HTTPSConnection if u.scheme == "https"
            else http.client.HTTPConnection)
    conn = None
    try:
        conn = Conn(u.hostname, u.port, timeout=timeout)
        conn.request(method, path, body=body, headers=headers)
        resp = conn.getresponse()
        return resp.status, resp.read().decode("utf-8", errors="replace")
    finally:
        if conn is not None:
            conn.close()


class Transport:
    """apiserver 控制面 client。

    Parameters
    ----------
    base_url : apiserver 根地址
    token    : X-API-Key（身份 token）
    env      : Env 头，默认空串（不内置具体环境名；由调用方/apiserver 决定路由）
    http_send: 可注入的 HTTP 执行器（单测用 fake，默认真实 http.client）
    """

    def __init__(self, base_url: str, token: str, *, env: str = "",
                 http_send: HttpSend | None = None,
                 timeout: float = DEFAULT_TIMEOUT,
                 retry_attempts: int = 3,
                 cache_credentials: bool = True) -> None:
        self.base_url = base_url.rstrip("/")
        self.token = token
        self.env = env
        self.timeout = timeout
        self._send = http_send or _KeepAliveSender()
        # 自定义发送器身份参与缓存键（见 config._cluster_cache_key）：注入过 fake/代理的
        # transport 即使 base/env 相同也各自隔离，与 Go/Java 的 customSend 语义一致。
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
                headers: dict | None = None) -> dict:
        """发一次控制面请求，返回解析后的 data。非 2xx 或业务 success=false 抛异常。

        仅对**幂等**请求做瞬时故障重试（默认 GET 幂等，其余不重试），避免把 5xx/
        连接中断后重发导致 ingest/release/register/commit 等**非幂等**写重复提交。
        显式传 ``idempotent=True`` 可为幂等的写（如凭据签发）开启重试。
        """
        if not self.base_url:
            raise SchemaError(
                "apiserver 根地址未配置；请通过 AP_BASE_URL 提供"
                "（旧别名 INSTANCEREPO_API_BASE 仍兼容；SDK 不内置任何域名，见部署文档）")
        retry = True if idempotent is None else idempotent
        if not retry:
            return self._request_once(method, path, body, headers=headers)
        return retry_transient(
            lambda: self._request_once(method, path, body, headers=headers),
            attempts=self._retry_attempts)

    def request_with_meta(self, method: str, path: str) -> tuple[dict, dict | None]:
        """同 :meth:`request`，但额外返回分页元数据 ``pagination``（无则 None）。

        分页列表响应形如 ``{code,message,data,pagination}``；``request`` 解包后只回
        data，调用方拿不到 total 无法翻页。本方法把两者一并返回，供
        ``ApiMetadataRegistry.query`` 遍历全部页。仅幂等 GET 场景使用。
        """
        if not self.base_url:
            raise SchemaError(
                "apiserver 根地址未配置；请通过 AP_BASE_URL 提供"
                "（旧别名 INSTANCEREPO_API_BASE 仍兼容；SDK 不内置任何域名，见部署文档）")
        if method == "GET":
            return retry_transient(
                lambda: self._request_once_with_meta(method, path),
                attempts=self._retry_attempts)
        return self._request_once_with_meta(method, path)

    def _request_once(self, method: str, path: str,
                      body: dict | None = None, *,
                      headers: dict | None = None) -> dict:
        data, _ = self._request_once_with_meta(
            method, path, body, headers=headers)
        return data

    def _request_once_with_meta(self, method: str, path: str,
                                body: dict | None = None, *,
                                headers: dict | None = None
                                ) -> tuple[dict, dict | None]:
        url = self.base_url + path
        raw = json.dumps(body).encode("utf-8") if body is not None else None
        status, text = self._send(
            method, url, self._headers(headers), raw, self.timeout)
        try:
            parsed = json.loads(text) if text.strip() else {}
        except json.JSONDecodeError:
            parsed = {}
        if status < 200 or status >= 300:
            code = parsed.get("code") if isinstance(parsed, dict) else None
            msg = parsed.get("message") if isinstance(parsed, dict) else text[:300]
            # apiserver 业务错误码为字符串时映射；数字业务码经 BIZ_CODE_TO_EXC 映射为
            # 类型化异常（Dataset RBAC 等），未知数字码再回退 TransportError 并透传
            # biz_code（92001/92003 同为 404，语义不同，调用方需据此区分）。
            if isinstance(code, str):
                raise exc_for_code(code, msg or "")
            if isinstance(code, int):
                raise exc_for_biz_code(code, msg or "", status=status)
            raise TransportError(f"HTTP {status}: {msg or text[:300]}",
                                 status=status, biz_code=None)
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
    def get(self, path: str) -> dict:
        return self.request("GET", path)

    def post(self, path: str, body: dict, *, idempotent: bool = False,
             headers: dict | None = None) -> dict:
        return self.request(
            "POST", path, body, idempotent=idempotent, headers=headers)

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
