"""store/oss.py — OSS content store（持 apiserver 签发的 STS 直连）。

所有公开 ContentStore 方法保持不变；网络意图由本模块内部按操作语义选择：正文下载与
下载探测只走可确认的标准私网 OSS 端点，其余操作私网优先，仅在明确连通失败时回退公网。
"""
from __future__ import annotations

import threading
from pathlib import Path
from typing import Any, Callable
from urllib.parse import urlsplit

from .. import paths as P
from .._routing import (
    _OperationIntent,
    _is_reachability_error,
    _plan_oss_route,
    _probe_private_endpoint,
)
from ..concurrency import ItemError, map_concurrent
from ..content import sha256_file, verify_file_digest
from ..errors import DigestMismatch, PrivateNetworkRequired, TransportError, SchemaError
from ..retry import retry_transient
from .base import BaseContentStore

def _next_listing_marker(result, seen: set[str]) -> str | None:
    """Fail closed on truncated/broken listings, without logging opaque markers."""
    if not result.is_truncated:
        return None
    marker = result.next_marker
    if not isinstance(marker, str) or not marker or marker in seen:
        raise SchemaError("OSS listing continuation did not advance")
    if len(seen) >= 1000:
        raise SchemaError("OSS listing exceeded its 1000-page budget")
    seen.add(marker)
    return marker


# bucket_factory 签名保持公开兼容：(sts:dict, bucket:str) -> bucket-like。
BucketFactory = Callable[[dict, str], Any]
# resumable_uploader 签名：(bucket, key, filename) -> None
ResumableUploader = Callable[[Any, str, str], None]

DEFAULT_MULTIPART_THRESHOLD = 100 * 1024 * 1024


def _instance_keys(layout, dataset: str, version: str, instance_id: str,
                   split: str) -> tuple[str, str, str]:
    """算 (sts_prefix, content_key, metadata_key)。

    ``layout`` 为 None 时回退 ``paths.*`` 的 version_first 语义——注入自定义 store 的
    调用方与旧用例不传 layout，必须保持逐字节不变。传入 ``Layout`` 时按其元数据模型
    （含 split_first 无版本布局）计算，这是修复「写侧仍走 version_first、split_first 下
    拼出 a/b//split/id.json 双斜杠畸形 key」的关键接缝。
    """
    if layout is None:
        return (P.sts_oss_prefix(dataset, version),
                P.content_key(dataset, version, instance_id, split),
                P.metadata_key(dataset, version, instance_id, split))
    return (layout.sts_prefix(dataset),
            layout.content_key(dataset, instance_id, version=version, split=split),
            layout.metadata_key(dataset, instance_id, version=version, split=split))


def _wrap_oss(exc: BaseException) -> BaseException:
    """把 oss2 异常归一成 SDK ``TransportError``，并由调用处保留 cause。"""
    from ..errors import InstanceRepoError
    if isinstance(exc, InstanceRepoError):
        return exc
    status = getattr(exc, "status", None)
    if not isinstance(status, int):
        return exc
    if not (hasattr(exc, "code") or hasattr(exc, "request_id")):
        return exc
    parts = [f"oss: status={status}"]
    for attr in ("code", "message", "request_id"):
        val = getattr(exc, attr, None)
        if val:
            parts.append(f"{attr}={val}")
    return TransportError(" ".join(parts), status=status)


def _https_endpoint(endpoint: str) -> str:
    value = endpoint.strip()
    if value.startswith("https://"):
        return value
    if value.startswith("http://"):
        return "https://" + value[len("http://"):]
    return "https://" + value


def _endpoint_host(endpoint: str) -> str:
    value = endpoint.strip()
    parsed = urlsplit(value if "://" in value else "//" + value)
    return parsed.netloc or parsed.path


def _private_endpoint_error(endpoint: str, cause: BaseException) -> PrivateNetworkRequired:
    host = _endpoint_host(endpoint)
    return PrivateNetworkRequired(
        "download requires private data-plane access; private endpoint "
        f"{host} is unreachable; public fallback is disabled",
        cause=cause,
    )


def _unconfirmed_private_endpoint_error(endpoint: str) -> PrivateNetworkRequired:
    host = _endpoint_host(endpoint)
    return PrivateNetworkRequired(
        "download requires private data-plane access; endpoint "
        f"{host} cannot be confirmed as a standard private OSS endpoint; "
        "public fallback is disabled"
    )


def _import_oss2():  # pragma: no cover - 真实 oss2
    """惰性 import oss2，屏蔽其编译期 SyntaxWarning。

    oss2 2.19.1 的 ``sign_url`` docstring 含非 raw 字符串里的 ``\\&``
    （示例 URL 的 OSSAccessKeyId=...&Expires=...），首次 import 时 Python
    编译器对其发出 ``SyntaxWarning: invalid escape sequence '\\&'``——纯第三方
    文档噪音，与请求拼接无关。仅抑制 SyntaxWarning（编译期），不影响运行时
    其他警告。
    """
    import warnings as _warnings
    with _warnings.catch_warnings():
        _warnings.simplefilter("ignore", SyntaxWarning)
        import oss2
    return oss2


def _default_bucket_factory(sts: dict, bucket: str, *,
                            private_download: bool = False):  # pragma: no cover - 真实 oss2
    """Build the default oss2 bucket, hardening private-download transport.

    Injected factories retain the historical two-argument signature and are deliberately outside
    this transport guarantee. The built-in private-download path forces HTTPS, ignores ambient
    proxy variables, and rejects redirects before requests can follow them.
    """
    oss2 = _import_oss2()

    endpoint = sts["endpoint"]
    session = None
    proxies = None
    if private_download:
        import requests

        endpoint = _https_endpoint(endpoint)
        session = oss2.Session()
        session.session.trust_env = False
        session.session.max_redirects = 0

        def reject_redirect(response, *args, **kwargs):
            if response.is_redirect or response.is_permanent_redirect:
                response.close()
                raise requests.TooManyRedirects(
                    "OSS redirects are disabled for private downloads",
                    response=response,
                )
            return response

        session.session.hooks.setdefault("response", []).append(reject_redirect)
        proxies = {}

    auth = oss2.StsAuth(sts["access_key_id"], sts["access_key_secret"],
                        sts["security_token"])
    return oss2.Bucket(auth, endpoint, bucket, session=session, proxies=proxies)


def _default_resumable_upload(bucket, key: str, filename: str):  # pragma: no cover - 真实 oss2
    oss2 = _import_oss2()
    oss2.resumable_upload(bucket, key, filename)


class OssContentStore(BaseContentStore):
    def __init__(self, transport, bucket: str, *,
                 bucket_factory: BucketFactory | None = None,
                 cache_buckets: bool = True,
                 multipart_threshold: int = DEFAULT_MULTIPART_THRESHOLD,
                 resumable_uploader: ResumableUploader | None = None,
                 retry_attempts: int = 3) -> None:
        self._t = transport
        self._bucket = bucket
        self._uses_default_factory = bucket_factory is None
        self._factory = bucket_factory or _default_bucket_factory
        self._mp_threshold = multipart_threshold
        self._resumable = resumable_uploader or _default_resumable_upload
        self._retry_attempts = retry_attempts
        self._cache_buckets = cache_buckets
        # Shared bucket cache (not thread-local) — oss2.Bucket is thread-safe
        # (internal requests.Session is thread-safe), so sharing across threads
        # reduces connection pool count from N→1 and makes the lock effective.
        self._bucket_cache: dict = {}
        self._local = threading.local()
        # Lock for atomic bucket creation — prevents concurrent threads
        # racing to create oss2.Bucket instances that replace each other
        # and cause "Connection pool shut down" when the GC'd pool is still in use.
        self._bucket_lock = threading.Lock()
        # Track replaced buckets for deferred close — old buckets are closed
        # only after the current batch finishes, not while requests are in flight.
        self._retired_buckets: list = []
        # Injectable TCP probe for private endpoint reachability.  Defaults to
        # the real raw-TCP-connect probe; tests may replace it with a stub.
        self._probe_private_endpoint = _probe_private_endpoint
        # Per-store probe result cache: endpoint → (reachable, timestamp).
        # Avoids re-probing the same internal endpoint on every OSS operation
        # (3s per probe × N operations = minutes of waste in push_many).
        self._probe_cache: dict[str, tuple[bool, float]] = {}
        self._probe_cache_ttl: float = 300.0  # 5 minutes

    @property
    def bucket_name(self) -> str:
        return self._bucket

    def _do(self, fn):
        """Run one complete endpoint attempt with the existing bounded retry policy."""
        try:
            return retry_transient(fn, attempts=self._retry_attempts)
        except Exception as exc:  # noqa: BLE001
            wrapped = _wrap_oss(exc)
            if wrapped is exc:
                raise
            raise wrapped from exc

    def _thread_buckets(self) -> dict:
        buckets = getattr(self._local, "buckets", None)
        if buckets is None:
            buckets = {}
            self._local.buckets = buckets
        return buckets

    def _make_bucket(self, sts: dict, *, private_download: bool):
        if self._uses_default_factory:
            return self._factory(
                sts, self._bucket, private_download=private_download)
        return self._factory(sts, self._bucket)

    def _open_bucket(self, sts: dict, prefix: str, endpoint: str, *,
                     private_download: bool):
        """Open/cache a bucket by policy scope, actual endpoint, transport policy and token.

        Thread-safe via a lock: concurrent threads with the same cache key
        share one bucket instead of racing to create independent instances
        whose connection pools get GC'd while still in use.
        """
        actual_endpoint = (
            _https_endpoint(endpoint)
            if private_download and self._uses_default_factory
            else endpoint
        )
        selected_sts = dict(sts)
        selected_sts["endpoint"] = actual_endpoint
        token = selected_sts.get("security_token", "")
        policy = "private-download" if private_download else "default"
        cache_key = (prefix, actual_endpoint, policy)

        if not (self._cache_buckets and token):
            return self._make_bucket(selected_sts, private_download=private_download)

        cache = self._bucket_cache
        cached = cache.get(cache_key)
        if cached is not None and cached[0] == token:
            return cached[1]

        # Atomic creation under lock — prevents concurrent threads from
        # each creating a bucket and overwriting each other's entries.
        with self._bucket_lock:
            # Double-check under lock: another thread may have created it.
            cached = cache.get(cache_key)
            if cached is not None and cached[0] == token:
                return cached[1]
            # Retire the old bucket (if any) for deferred close instead of
            # silently dropping it — its connection pool may still be in use.
            if cached is not None:
                old_bucket = cached[1]
                self._retired_buckets.append(old_bucket)
            bucket = self._make_bucket(selected_sts, private_download=private_download)
            cache[cache_key] = (token, bucket)
        return bucket

    def _probe_cached(self, endpoint: str) -> bool:
        """Probe private endpoint reachability with per-store caching.

        Caches the result for self._probe_cache_ttl seconds (default 5 min).
        After the first probe fails, subsequent calls within the TTL skip the
        3-second TCP connect and return the cached False immediately — this
        eliminates minutes of redundant probing in push_many when private
        network is unreachable.
        """
        import time
        cached = self._probe_cache.get(endpoint)
        if cached is not None:
            reachable, ts = cached
            if time.time() - ts < self._probe_cache_ttl:
                return reachable
        reachable = self._probe_private_endpoint(endpoint)
        self._probe_cache[endpoint] = (reachable, time.time())
        return reachable

    def close_retired(self) -> None:
        """Release all retired buckets.

        In Python, oss2.Bucket has no explicit close() method — its underlying
        requests.Session connection pool is cleaned up by GC when the Bucket
        object is dereferenced.  This method pops retired buckets from the list
        so they become eligible for GC, but only after the batch completes
        (preventing premature GC while requests are in flight).

        In Java, the equivalent calls AliyunOssBucket.close() which shuts down
        the Apache connection pool explicitly.
        """
        while self._retired_buckets:
            self._retired_buckets.pop()

    def _credentials(self, prefix: str, dataset: str | None,
                     list_only: bool = False):
        return self._t.get_oss_credentials(
            self._bucket, prefix, dataset_name=dataset, list_only=list_only)

    def _open(self, prefix: str, dataset: str | None = None):
        """Compatibility helper used by prewarm and legacy private tests."""
        sts = self._credentials(prefix, dataset)
        route = _plan_oss_route(sts.get("endpoint", ""))
        return self._open_bucket(
            sts, prefix, route.private_endpoint, private_download=False)

    def _execute_oss(self, intent: _OperationIntent, prefix: str,
                     dataset: str | None, operation, *,
                     list_only: bool = False):
        """Execute one logical OSS operation using one STS acquisition.

        Non-download operations perform one complete bounded private attempt and only retry the
        complete operation on the public candidate after a typed connectivity failure. Downloads
        construct only a confirmed private bucket and translate connectivity failures to the
        stable private-network-required error.

        Args:
            list_only: Discovery-mode switch: True 时签发仅含 ListObjects 的令牌
                （OSS 回退发现专用）。Passed through to :meth:`_credentials`.
        """
        if intent is not _OperationIntent.DOWNLOAD and intent is not _OperationIntent.NON_DOWNLOAD:
            raise ValueError(f"unknown OSS operation intent: {intent!r}")

        sts = self._credentials(prefix, dataset, list_only=list_only)
        original_endpoint = sts.get("endpoint", "")
        route = _plan_oss_route(original_endpoint)

        if intent is _OperationIntent.DOWNLOAD:
            if not route.standard:
                raise _unconfirmed_private_endpoint_error(original_endpoint)
            endpoint = route.private_endpoint
            # Fail-fast: 3 秒探测私网可达性，不通立即报错，避免公网环境下
            # 傻等 TCP 超时（20s × 多轮重试 = 几分钟挂死）。下载仍不 fallback
            # 公网（安全约束），但能快速告知调用方需要私网环境。
            if not self._probe_cached(endpoint):
                raise _private_endpoint_error(
                    endpoint, ConnectionRefusedError(
                        f"TCP probe failed for {endpoint} within 3s"))
            try:
                bucket = self._open_bucket(
                    sts, prefix, endpoint, private_download=True)
                return self._do(lambda: operation(bucket))
            except Exception as exc:  # noqa: BLE001
                if _is_reachability_error(exc):
                    raise _private_endpoint_error(endpoint, exc) from exc
                raise

        private_endpoint = route.private_endpoint
        private_failure: BaseException | None = None

        # Quick TCP probe to decide whether to attempt the private endpoint.
        # If the route is standard (has a known public fallback) and the probe
        # fails, skip the private attempt entirely to save 60+ seconds of
        # waiting for a full timeout.  Downloads are NOT affected — they
        # always try private only (no public fallback).
        if route.standard and route.public_endpoint is not None:
            if not self._probe_cached(private_endpoint):
                private_failure = ConnectionRefusedError(
                    f"TCP probe failed for {private_endpoint}")
                try:
                    bucket = self._open_bucket(
                        sts, prefix, route.public_endpoint,
                        private_download=False)
                    return self._do(lambda: operation(bucket))
                except Exception as public_exc:  # noqa: BLE001
                    public_exc.private_route_failure = private_failure
                    raise

        try:
            bucket = self._open_bucket(
                sts, prefix, private_endpoint, private_download=False)
            return self._do(lambda: operation(bucket))
        except Exception as private_exc:  # noqa: BLE001
            if route.public_endpoint is None or not _is_reachability_error(private_exc):
                raise
            private_failure = private_exc

        try:
            bucket = self._open_bucket(
                sts, prefix, route.public_endpoint, private_download=False)
            return self._do(lambda: operation(bucket))
        except Exception as public_exc:  # noqa: BLE001
            public_exc.private_route_failure = private_failure
            raise

    def prewarm(self, prefix: str, dataset: str | None = None) -> None:
        self._open(prefix, dataset=dataset)

    def _upload_file(self, bucket, key: str, path) -> None:
        path = Path(path)
        if path.stat().st_size >= self._mp_threshold:
            self._resumable(bucket, key, str(path))
        else:
            bucket.put_object_from_file(key, str(path))

    # ── generic object ops（report/content 共用；默认按对象 key 收窄 STS）──
    def put_object(self, key: str, data, *, overwrite: bool = False,
                   sts_prefix: str | None = None,
                   dataset: str | None = None) -> dict:
        prefix = sts_prefix or key

        write_attempted = [False]

        def put(bucket):
            # The existence-based skip decision is only valid before any write
            # is attempted. If a write already started (a transient response
            # failure triggered a retry, or a private→public fallback re-run),
            # re-perform the write instead of mis-reporting a pre-existing skip.
            if not overwrite and not write_attempted[0] and bucket.object_exists(key):
                return {"skipped": True, "key": key}
            write_attempted[0] = True
            if isinstance(data, (bytes, bytearray)):
                bucket.put_object(key, bytes(data))
            else:
                self._upload_file(bucket, key, data)
            return {"skipped": False, "key": key}

        return self._execute_oss(
            _OperationIntent.NON_DOWNLOAD, prefix, dataset, put)

    def get_object(self, key: str, dest: Path, *,
                   expected_digest: str | None = None,
                   sts_prefix: str | None = None,
                   dataset: str | None = None) -> Path:
        dest = Path(dest)
        dest.parent.mkdir(parents=True, exist_ok=True)
        self._execute_oss(
            _OperationIntent.DOWNLOAD,
            sts_prefix or key,
            dataset,
            lambda bucket: bucket.get_object_to_file(key, str(dest)),
        )
        if expected_digest is not None and not verify_file_digest(dest, expected_digest):
            raise DigestMismatch(
                f"{key}: content digest mismatch "
                f"(expected {expected_digest}, got {sha256_file(dest)})")
        return dest

    def object_exists(self, key: str, *, sts_prefix: str | None = None,
                      dataset: str | None = None) -> bool:
        """HEAD 对象；已知 dataset 时透传给 STS 做 Dataset RBAC。

        ``dataset=None`` 保持通用对象探测的旧语义，不伪造 dataset 上下文；SWE push 的
        verify 回读会显式传 dataset，否则 apiserver 无法按 Dataset RBAC 签写后校验凭据。
        """
        return self._execute_oss(
            _OperationIntent.NON_DOWNLOAD,
            sts_prefix or key,
            dataset,
            lambda bucket: bucket.object_exists(key),
        )

    def _download_probe(self, key: str, *, sts_prefix: str | None = None,
                        dataset: str | None = None) -> bool:
        """Package-private HEAD probe for a subsequent body download."""
        return self._execute_oss(
            _OperationIntent.DOWNLOAD,
            sts_prefix or key,
            dataset,
            lambda bucket: bucket.object_exists(key),
        )

    def list_objects(self, prefix: str, *, list_only: bool = False,
                     dataset: str | None = None,
                     max_keys: int | None = None) -> list[str]:
        """List object keys under *prefix*.

        ``max_keys``（有限值时）在收集到该数量的键后提前停止翻页，
        不再拉取剩余 OSS 分页——分页发现路径（P1-1c）用它把首页
        请求的网络开销从“随对象总量线性”降为“随请求页数”。
        返回条数可能少于桶内实际对象数（截断语义由调用方处理）。
        """
        return self._list_objects_state(prefix, list_only=list_only,
                                        dataset=dataset, max_keys=max_keys)[0]

    def list_objects_with_exhausted(self, prefix: str, *, list_only: bool = False,
                                    dataset: str | None = None,
                                    max_keys: int | None = None,
                                    start_after: str = "") -> tuple[list[str], bool]:
        """Same as :meth:`list_objects` but also reports OSS exhaustion.

        Returns ``(keys, exhausted)``: *exhausted* is ``True`` when the OSS
        listing reached its natural end (no further pages under *prefix*),
        and ``False`` when it stopped early because *max_keys* keys were
        collected. ``start_after`` resumes the listing after that raw key
        (OSS marker semantics; only keys strictly greater are returned).
        Lets paged discovery advance by *valid* instances instead of raw
        keys and decide ``has_more`` without guessing.
        """
        return self._list_objects_state(prefix, list_only=list_only,
                                        dataset=dataset, max_keys=max_keys,
                                        start_after=start_after)

    def _list_objects_state(self, prefix: str, *, list_only: bool = False,
                            dataset: str | None = None,
                            max_keys: int | None = None,
                            start_after: str = "") -> tuple[list[str], bool]:
        bounded = isinstance(max_keys, int) and not isinstance(max_keys, bool) \
            and max_keys >= 0

        def list_all(bucket):
            keys: list[str] = []
            if bounded and max_keys == 0:
                return keys, False  # stopped by cap, OSS state unknown → not exhausted
            marker = start_after
            seen = {marker}
            while True:
                page_size = 1000
                if bounded:
                    page_size = min(1000, max(1, max_keys - len(keys)))
                result = bucket.list_objects(
                    prefix=prefix, marker=marker, max_keys=page_size)
                keys.extend(obj.key for obj in result.object_list)
                if bounded and len(keys) >= max_keys:
                    return keys[:max_keys], False  # stopped by cap
                marker = _next_listing_marker(result, seen)
                if marker is None:
                    return keys, True  # listing reached its natural end
            return keys, True  # unreachable

        return self._execute_oss(
            _OperationIntent.NON_DOWNLOAD, prefix, dataset, list_all,
            list_only=list_only)

    def delete_instance_files(self, operation) -> None:
        """Delete exactly the server-scoped objects of one instance deletion.

        ``operation`` carries the server-issued restricted credentials (policy
        bundles ``oss:DeleteObject`` for exact keys plus ``ListObjects``
        conditioned on the scope prefixes) and the ``delete_scope`` manifest:
        ``keys`` are exact objects, ``prefixes`` are directory subtrees. The
        restricted delete credentials are opened directly here — they never
        enter the read/write credential cache, and a normal writer token is
        never used for deletion (the server does not grant DeleteObject to
        read/write policies).

        Per subtree: at most 1000 pages of 200 objects, O(200) memory,
        sequential requests and existing bounded transport retries. Stop
        writers/ingesters before calling; this is not an atomic delete or a
        version-history purge.
        """
        from ..errors import SchemaError

        credentials = getattr(operation, "credentials", None)
        bucket_name = getattr(operation, "bucket", "")
        keys = list(getattr(operation, "keys", None) or [])
        prefixes = list(getattr(operation, "prefixes", None) or [])
        if not isinstance(credentials, dict) or not bucket_name:
            raise TransportError("instance deletion credentials missing")
        endpoint = credentials.get("OSS_ENDPOINT", "")
        route = _plan_oss_route(endpoint)
        if not route.standard:
            raise _unconfirmed_private_endpoint_error(endpoint)
        private_endpoint = route.private_endpoint
        # 与下载同一安全纪律：删除只走私网（受限 STS 900s，公网回退无意义且
        # 令牌作用域不应离开内网）。3s 探测快速失败，避免公网环境傻等 TCP 超时。
        if not self._probe_cached(private_endpoint):
            raise _private_endpoint_error(
                private_endpoint, ConnectionRefusedError(
                    f"TCP probe failed for {private_endpoint} within 3s"))
        # 独立开桶：不进 bucket 缓存（删除令牌 900s 短时效、单次使用；缓存
        # 会把它与读写令牌混入同一淘汰池）。factory 直收标准 STS dict。
        sts = {
            "access_key_id": credentials.get("OSS_ACCESS_KEY_ID", ""),
            "access_key_secret": credentials.get("OSS_ACCESS_KEY_SECRET", ""),
            "security_token": credentials.get("OSS_SECURITY_TOKEN", ""),
            "endpoint": private_endpoint,
            "bucket": bucket_name,
        }
        bucket = self._make_bucket(sts, private_download=True)

        def remove():
            for key in keys:
                self._do(lambda key=key: bucket.delete_object(key))
            for prefix in prefixes:
                marker = ""
                for _ in range(1000):
                    page = self._do(lambda: bucket.list_objects(
                        prefix=prefix, marker=marker, max_keys=200))
                    objects = list(page.object_list)
                    if len(objects) > 200:
                        raise SchemaError("OSS deletion page exceeds the requested limit")
                    page_keys = [obj.key for obj in objects]
                    if any(not isinstance(key, str) or not key.startswith(prefix)
                           or (marker and key <= marker) for key in page_keys):
                        raise SchemaError("OSS deletion listing escaped its instance subtree")
                    next_marker = page.next_marker
                    if page.is_truncated and (
                            not isinstance(next_marker, str)
                            or not next_marker.startswith(prefix)
                            or next_marker <= marker
                            or (page_keys and next_marker < max(page_keys))):
                        raise SchemaError("OSS deletion listing returned an invalid marker")
                    for key in page_keys:
                        self._do(lambda key=key: bucket.delete_object(key))
                    if not page.is_truncated:
                        break
                    marker = next_marker
                else:
                    raise SchemaError("OSS deletion page budget exceeded; retry after quiescing writers")

        remove()

    def list_prefixes(self, prefix: str, *, list_only: bool = False,
                       dataset: str | None = None) -> list[str]:
        """List immediate child *directories* under *prefix* using ``delimiter='/'``.

        Returns stripped directory names (without the parent prefix or trailing
        ``/``).  For example, if *prefix* is ``swe/datasets/a/b/`` and the bucket
        contains ``swe/datasets/a/b/v1/`` and ``swe/datasets/a/b/v1-assets/``,
        this returns ``["v1", "v1-assets"]``.

        Unlike :meth:`list_objects` which recursively enumerates all objects,
        this performs a single-level directory listing — ideal for version/split
        structure discovery without traversing potentially millions of instance
        keys.
        """
        def list_dirs(bucket):
            names: list[str] = []
            marker = ""
            seen = {marker}
            while True:
                result = bucket.list_objects(
                    prefix=prefix, marker=marker, delimiter="/", max_keys=1000)
                for p in result.prefix_list:
                    name = p[len(prefix):]
                    if name.endswith("/"):
                        name = name[:-1]
                    if name:
                        names.append(name)
                marker = _next_listing_marker(result, seen)
                if marker is None:
                    break
            return names

        return self._execute_oss(
            _OperationIntent.NON_DOWNLOAD, prefix, dataset, list_dirs,
            list_only=list_only)

    def list_level(self, prefix: str, *,
                   list_only: bool = False,
                   dataset: str | None = None) -> tuple[list[str], list[str]]:
        """Single-level listing with ``delimiter='/'``.

        Returns ``(dir_names, file_keys)`` where *dir_names* are stripped
        child-directory names (same as :meth:`list_prefixes`) and *file_keys*
        are the full keys of objects at the direct level (not in sub-dirs).

        This avoids two separate OSS calls when both directory structure and
        direct file presence are needed (e.g. version/split discovery).
        """
        def list_one_level(bucket):
            names: list[str] = []
            keys: list[str] = []
            marker = ""
            seen = {marker}
            while True:
                result = bucket.list_objects(
                    prefix=prefix, marker=marker, delimiter="/", max_keys=1000)
                for p in result.prefix_list:
                    name = p[len(prefix):]
                    if name.endswith("/"):
                        name = name[:-1]
                    if name:
                        names.append(name)
                keys.extend(obj.key for obj in result.object_list)
                marker = _next_listing_marker(result, seen)
                if marker is None:
                    break
            return names, keys

        return self._execute_oss(
            _OperationIntent.NON_DOWNLOAD, prefix, dataset, list_one_level,
            list_only=list_only)

    def list_direct_objects_paged(self, prefix: str, *,
                                  list_only: bool = False,
                                  dataset: str | None = None,
                                  max_keys: int | None = None,
                                  start_after: str = "") -> tuple[list[str], bool]:
        """Page over **direct-level** object keys using ``delimiter='/'``.

        Returns ``(direct_keys, exhausted)``:

        - *direct_keys*: object keys directly under *prefix* (sub-directory
          contents are skipped entirely — one subtree costs one prefix entry,
          not one entry per nested object). Marker ordering is preserved, so
          ``start_after`` (a raw direct key) resumes strictly after it.
        - *exhausted*: ``True`` when the single-level listing reached its
          natural end; ``False`` when it stopped early because *max_keys*
          direct keys were collected.

        Paged instance discovery uses this so a sparse directory (few direct
        JSONs beside huge nested subtrees) costs a handful of LISTs instead
        of one per two raw keys.
        """
        bounded = isinstance(max_keys, int) and not isinstance(max_keys, bool) \
            and max_keys >= 0

        def list_one_level(bucket):
            keys: list[str] = []
            if bounded and max_keys == 0:
                return keys, False
            marker = start_after
            seen = {marker}
            while True:
                # Request a full OSS page of *entries* (direct objects and
                # same-level sub-directory prefixes together): under the
                # delimiter the server folds each subtree into one entry, so
                # a full page is cheap regardless of subtree sizes. The
                # caller's cap applies to *direct keys* only — dense
                # directories stop after one page, directories dominated by
                # sibling sub-dirs page at O(entries/1000) which is bounded
                # by the listing's 1000-page budget.
                result = bucket.list_objects(
                    prefix=prefix, marker=marker, delimiter="/", max_keys=1000)
                keys.extend(obj.key for obj in result.object_list)
                if bounded and len(keys) >= max_keys:
                    return keys[:max_keys], False  # stopped by cap
                marker = _next_listing_marker(result, seen)
                if marker is None:
                    return keys, True  # listing reached its natural end
            return keys, True  # unreachable

        return self._execute_oss(
            _OperationIntent.NON_DOWNLOAD, prefix, dataset, list_one_level,
            list_only=list_only)

    # ── directory-level helpers（自定义格式实例 = 目录级上传/下载）──
    def put_directory(self, local_dir: Path, oss_prefix: str, *,
                      overwrite: bool = False,
                      sts_prefix: str | None = None,
                      dataset: str | None = None,
                      concurrency: int = 8) -> dict:
        """Upload all files under *local_dir* to OSS under *oss_prefix*.

        Each file is uploaded via :meth:`put_object` so every transfer gets
        proper STS credentials and endpoint routing.  Files are uploaded in
        parallel using :func:`~instance_repo.concurrency.map_concurrent`.

        Returns a summary dict::

            {"file_count": int, "total_bytes": int, "keys": list[str]}
        """
        local_dir = Path(local_dir)
        if not local_dir.is_dir():
            raise FileNotFoundError(f"local directory not found: {local_dir}")

        # Normalize prefix to always end with "/" so keys are proper children.
        if oss_prefix and not oss_prefix.endswith("/"):
            oss_prefix += "/"

        # Collect (local_path, oss_key) pairs — sorted for determinism.
        files: list[tuple[Path, str]] = sorted(
            ((p, oss_prefix + str(p.relative_to(local_dir)))
             for p in local_dir.rglob("*") if p.is_file()),
            key=lambda t: t[1],
        )

        total_bytes = sum(p.stat().st_size for p, _ in files)

        def _upload_one(item: tuple[Path, str]) -> str:
            path, key = item
            self.put_object(key, path, overwrite=overwrite,
                            sts_prefix=sts_prefix, dataset=dataset)
            return key

        try:
            keys = map_concurrent(_upload_one, files, concurrency=concurrency)
        except ItemError as exc:
            raise exc.error from exc
        return {
            "file_count": len(files),
            "total_bytes": total_bytes,
            "keys": keys,
        }

    def get_directory(self, oss_prefix: str, local_dir: Path, *,
                      expected_digests: dict[str, str] | None = None,
                      sts_prefix: str | None = None,
                      dataset: str | None = None,
                      concurrency: int = 8) -> Path:
        """Download all objects under *oss_prefix* to *local_dir*.

        Objects are listed via :meth:`list_objects` and then downloaded in
        parallel.  Each file is fetched via :meth:`get_object` so every
        transfer gets proper STS credentials and private-download routing.

        *expected_digests* optionally maps **relative paths** (e.g.
        ``"subdir/file.bin"``) to their expected content digest strings
        (``"sha256:<hex>"`` or bare md5).  Any mismatch raises
        :class:`~instance_repo.errors.DigestMismatch`.

        Returns the *local_dir* path.
        """
        local_dir = Path(local_dir)
        local_dir.mkdir(parents=True, exist_ok=True)

        # Normalize prefix for consistent key slicing.
        if oss_prefix and not oss_prefix.endswith("/"):
            oss_prefix += "/"

        keys = self.list_objects(oss_prefix, list_only=True, dataset=dataset)

        # Object names are untrusted even when listed under an authorized OSS
        # prefix. Validate every destination before starting any download.
        root = local_dir.resolve()
        for key in keys:
            if not isinstance(key, str) or not key.startswith(oss_prefix):
                raise SchemaError("directory listing returned an out-of-scope object")
            rel = key[len(oss_prefix):]
            if not rel:
                continue
            if (rel.startswith("/") or "\\" in rel or ":" in rel or "\0" in rel
                    or any(part in ("", ".", "..") for part in rel.split("/"))):
                raise SchemaError("unsafe object path in directory download")
            if not (root / rel).resolve().is_relative_to(root):
                raise SchemaError("directory download destination escapes its root")

        def _download_one(key: str) -> Path:
            rel = key[len(oss_prefix):]
            if not rel:  # skip the prefix "directory marker" itself
                return local_dir
            dest = local_dir / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            self._execute_oss(
                _OperationIntent.DOWNLOAD,
                sts_prefix or oss_prefix,
                dataset,
                lambda bucket: bucket.get_object_to_file(key, str(dest)),
            )
            # Per-file digest check.
            if expected_digests is not None:
                expected = expected_digests.get(rel)
                if expected is not None and not verify_file_digest(dest, expected):
                    raise DigestMismatch(
                        f"{key}: content digest mismatch "
                        f"(expected {expected}, got {sha256_file(dest)})")
            return dest

        try:
            map_concurrent(_download_one, keys, concurrency=concurrency)
        except ItemError as exc:
            raise exc.error from exc
        return local_dir

    # ── 实例内容便捷封装（content.tgz + {id}.json） ──
    def exists(self, instance_id: str, dataset: str, version: str,
               split: str = "default", *, layout=None) -> bool:
        prefix, tgz_key, idx_key = _instance_keys(
            layout, dataset, version, instance_id, split)

        def both_exist(bucket):
            return bucket.object_exists(tgz_key) and bucket.object_exists(idx_key)

        return self._execute_oss(
            _OperationIntent.NON_DOWNLOAD, prefix, dataset, both_exist)

    def put(self, instance_id: str, dataset: str, version: str, split: str,
            tgz_path: Path, meta_json: str, *, overwrite: bool,
            layout=None) -> dict:
        prefix, tgz_key, idx_key = _instance_keys(
            layout, dataset, version, instance_id, split)

        write_attempted = [False]

        def put_instance(bucket):
            # Only skip on pre-existing objects before any write is attempted;
            # a post-write transient retry (or public-fallback re-run) must
            # re-upload and return the digest, never a skip that drops it.
            if (not overwrite and not write_attempted[0]
                    and bucket.object_exists(tgz_key)
                    and bucket.object_exists(idx_key)):
                return {"skipped": True, "tgz_key": tgz_key, "idx_key": idx_key}
            write_attempted[0] = True
            self._upload_file(bucket, tgz_key, tgz_path)
            bucket.put_object(idx_key, meta_json.encode("utf-8"))
            return {"skipped": False, "tgz_key": tgz_key, "idx_key": idx_key,
                    "content_digest": sha256_file(tgz_path)}

        return self._execute_oss(
            _OperationIntent.NON_DOWNLOAD, prefix, dataset, put_instance)

    def verify_upload(self, dataset: str, version: str, instance_id: str, split: str,
                      local_archive: Path, *, expected_digest: str, layout=None) -> None:
        """Verify upload integrity, including pre-existing skipped bytes.

        Built-in buckets compare server CRC64/XZ and size without body downloads.
        Legacy injected buckets without HEAD use the existing private-only readback.
        Missing server checksums fail closed; caller can overwrite legacy objects.
        """
        from .._upload_integrity import crc64_file
        size, checksum, digest = crc64_file(local_archive)
        if digest != expected_digest:
            raise DigestMismatch("local multi-step archive changed before verification")
        prefix, tgz_key, idx_key = _instance_keys(
            layout, dataset, version, instance_id, split)

        def verify(bucket):
            head_object = getattr(bucket, "head_object", None)
            if not callable(head_object):
                return False  # Legacy injected buckets retain private readback.
            head = head_object(tgz_key)
            headers = {key.lower(): str(value) for key, value in head.headers.items()}
            crc = headers.get("x-oss-hash-crc64ecma", "")
            length = headers.get("content-length", "")
            if (len(crc) > 20 or not crc.isascii() or not crc.isdecimal() or int(crc) >= 1 << 64
                    or len(length) > 19 or not length.isascii() or not length.isdecimal()
                    or int(length) >= 1 << 63):
                raise TransportError("OSS upload verification requires server CRC64 and size; "
                                     "overwrite legacy objects or check the OSS backend")
            if int(crc) != checksum or int(length) != size:
                raise DigestMismatch("multi-step archive differs from local bytes (OSS CRC64/size)")
            if not bucket.object_exists(idx_key):
                raise TransportError("multi-step metadata is missing after delivery")
            return True

        if not self._execute_oss(_OperationIntent.NON_DOWNLOAD, prefix, dataset, verify):
            import tempfile
            with tempfile.TemporaryDirectory(prefix="irepo_verify_") as temporary:
                self.get(dataset, version, instance_id, split, Path(temporary) / "readback.tgz",
                         expected_digest=expected_digest, layout=layout)
            if not self.exists(instance_id, dataset, version, split, layout=layout):
                raise TransportError("multi-step metadata is missing after delivery")

    def get(self, dataset: str, version: str, instance_id: str, split: str,
            dest: Path, *, expected_digest: str | None = None,
            layout=None) -> Path:
        prefix, tgz_key, _ = _instance_keys(
            layout, dataset, version, instance_id, split)
        dest = Path(dest)
        dest.parent.mkdir(parents=True, exist_ok=True)
        self._execute_oss(
            _OperationIntent.DOWNLOAD,
            prefix,
            dataset,
            lambda bucket: bucket.get_object_to_file(tgz_key, str(dest)),
        )
        if expected_digest is not None and not verify_file_digest(dest, expected_digest):
            raise DigestMismatch(
                f"{instance_id}: content digest mismatch "
                f"(expected {expected_digest}, got {sha256_file(dest)})")
        return dest
