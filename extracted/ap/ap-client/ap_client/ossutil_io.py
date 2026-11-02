"""Server-scoped OSS file operations. Dependencies load only when a command executes."""

from __future__ import annotations

import fnmatch
import hashlib
import json
import os
import re
import stat
import tempfile
import time
import unicodedata
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterator
from urllib.parse import unquote, urlsplit

COPY_MULTIPART_THRESHOLD = 100 * 1024 * 1024

#: 元数据注册表"dataset 未注册"的业务码(与 dataset_commands 的 dataset_get 同口径)。
_DATASET_NOT_FOUND_CODES = (92001, 94021)


class OssUsageError(ValueError):
    """Invalid local input; no OSS operation should be issued."""


class OssOperationError(RuntimeError):
    """A failed operation with a safe user-facing explanation."""


def _relative(value: str, *, allow_empty: bool = False) -> str:
    if not isinstance(value, str) or (not value and not allow_empty):
        raise OssUsageError("A non-empty remote path is required")
    if not value:
        return value
    if value.startswith("/") or "\\" in value or re.match(r"^[A-Za-z][\w+.-]*:", value):
        raise OssUsageError("Remote relative paths cannot be absolute paths or URLs")
    if any(unicodedata.category(c) == "Cc" for c in value) or any(c in value for c in "*?"):
        raise OssUsageError("Remote paths cannot contain control characters or wildcards")
    parts = value.rstrip("/").split("/")
    if any(p in ("", ".", "..") for p in parts):
        raise OssUsageError("Remote paths cannot contain empty, '.' or '..' segments")
    return value


def _endpoint(value: str) -> str:
    candidate = value if "://" in value else "https://" + value
    parsed = urlsplit(candidate)
    try:
        parsed.port
    except ValueError as exc:
        raise OssOperationError("repo-config provided an invalid OSS endpoint port") from exc
    if (
        parsed.scheme not in ("https", "http")
        or not parsed.hostname
        or parsed.username
        or parsed.password
        or parsed.query
        or parsed.fragment
        or parsed.path not in ("", "/")
    ):
        raise OssOperationError("repo-config provided an invalid OSS endpoint")
    # Both candidates come from the control plane. All data-plane requests use TLS.
    return "https://" + parsed.netloc


@dataclass(frozen=True)
class OssBinding:
    bucket: str
    prefix: str
    region: str
    endpoint: str
    public_endpoint: str = ""

    @classmethod
    def from_payload(cls, value: dict) -> "OssBinding":
        for key in ("bucket", "prefix", "region", "endpoint"):
            if not isinstance(value.get(key), str) or not value[key].strip():
                raise OssOperationError(f"repo-config OSS binding is missing {key}")
        prefix = value["prefix"].strip("/")
        _relative(prefix)
        return cls(
            bucket=value["bucket"].strip(),
            prefix=prefix + "/",
            region=value["region"].strip(),
            endpoint=_endpoint(value["endpoint"].strip()),
            public_endpoint=_endpoint(value["public_endpoint"].strip())
            if value.get("public_endpoint")
            else "",
        )

    def resolve(
        self,
        value: str,
        *,
        directory: bool = False,
        prefix: bool = False,
        encoding_type: str | None = None,
    ) -> "RemotePath":
        if value.startswith("oss://"):
            try:
                parsed = urlsplit(value)
                if (
                    parsed.username
                    or parsed.password
                    or parsed.port
                    or parsed.query
                    or parsed.fragment
                ):
                    raise OssUsageError("OSS URI cannot include userinfo, port, query or fragment")
                if parsed.netloc != self.bucket:
                    raise OssUsageError("OSS URI bucket does not match repo-config")
                raw = parsed.path.removeprefix("/")
                if encoding_type == "url" and re.search(r"%(?![0-9a-fA-F]{2})", raw):
                    raise OssUsageError("OSS URI has invalid percent encoding")
                key = unquote(raw, errors="strict") if encoding_type == "url" else raw
            except (ValueError, UnicodeError) as exc:
                raise OssUsageError(str(exc)) from exc
            if key == self.prefix.rstrip("/") and (directory or prefix):
                key = self.prefix
            if not key.startswith(self.prefix):
                raise OssUsageError("OSS URI prefix does not match repo-config")
            relative = key[len(self.prefix) :]
        else:
            relative = unquote(value, errors="strict") if encoding_type == "url" else value
            key = self.prefix + relative
        _relative(relative, allow_empty=directory or prefix)
        if directory and not key.endswith("/"):
            key += "/"
            relative += "/"
        if not directory and not prefix and (not relative or relative.endswith("/")):
            raise OssUsageError("This operation requires a file path")
        return RemotePath(self.bucket, key, relative)


@dataclass(frozen=True)
class RemotePath:
    bucket: str
    key: str
    path: str


def direction_for(src: str, dst: str) -> str:
    """Infer cp direction the way ossutil does: at least one operand is an OSS URI."""
    remote_src, remote_dst = src.startswith("oss://"), dst.startswith("oss://")
    if remote_src and remote_dst:
        return "copy"
    if remote_src:
        return "download"
    if remote_dst:
        return "upload"
    raise OssUsageError(
        "cp requires at least one operand starting with oss://; paths without it are local"
    )


def matches(path: str, include: tuple[str, ...], exclude: tuple[str, ...]) -> bool:
    def match(pattern):
        return fnmatch.fnmatchcase(path, pattern) or fnmatch.fnmatchcase(
            path.rsplit("/", 1)[-1], pattern
        )

    return (not include or any(match(p) for p in include)) and not any(match(p) for p in exclude)


class SecureStore:
    """oss2-compatible resume store with private, atomic records."""

    def __init__(self, directory: Path, store_class: type):
        self.directory = directory
        self.make_store_key = store_class.make_store_key
        self.directory.mkdir(parents=True, exist_ok=True, mode=0o700)
        if self.directory.is_symlink():
            raise OssOperationError("Resume directory cannot be a symlink")
        self.directory.chmod(0o700)

    def _path(self, key: str) -> Path:
        if not key or Path(key).name != key or key in (".", ".."):
            raise OssOperationError("Invalid resume record name")
        path = self.directory / key
        if path.is_symlink():
            raise OssOperationError("Resume record cannot be a symlink")
        return path

    def get(self, key: str) -> dict | None:
        try:
            return json.loads(self._path(key).read_text())
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    def put(self, key: str, value: dict) -> None:
        path = self._path(key)
        fd, name = tempfile.mkstemp(dir=self.directory)
        try:
            with os.fdopen(fd, "w") as handle:
                json.dump(value, handle)
            os.replace(name, path)
        finally:
            Path(name).unlink(missing_ok=True)

    def delete(self, key: str) -> None:
        self._path(key).unlink(missing_ok=True)


class _WriteBucket:
    """Keep overwrite protection on CompleteMultipartUpload: oss2 filters headers."""

    def __init__(self, bucket: Any, overwrite: bool):
        self.bucket, self.overwrite = bucket, overwrite

    def __getattr__(self, name: str) -> Any:
        return getattr(self.bucket, name)

    def complete_multipart_upload(self, key, upload_id, parts, headers=None):
        headers = dict(headers or {})
        if not self.overwrite:
            headers["x-oss-forbid-overwrite"] = "true"
        return self.bucket.complete_multipart_upload(key, upload_id, parts, headers=headers)


class _RoutingBucket:
    """Invalidate reachability caches after a typed connection failure, without replaying."""

    def __init__(self, bucket: Any, owner: "OssFiles", endpoint: str):
        self.bucket, self.owner = bucket, owner
        self._ossutil_endpoint = endpoint

    def __getattr__(self, name: str) -> Any:
        value = getattr(self.bucket, name)
        if not callable(value):
            return value

        def call(*args, **kwargs):
            try:
                if self.owner.payer and name not in ("sign_url",):
                    headers = dict(kwargs.get("headers") or {})
                    headers["x-oss-request-payer"] = self.owner.payer
                    kwargs["headers"] = headers
                return value(*args, **kwargs)
            except Exception as exc:
                self.owner.invalidate_network(exc, self._ossutil_endpoint)
                raise

        return call


def safe_error(exc: Exception) -> str:
    if isinstance(exc, ImportError):
        # ImportError messages only name the missing module; nothing sensitive is included.
        return f"{type(exc).__name__}: {exc}"
    if isinstance(exc, (OssUsageError, OssOperationError, OSError)):
        return str(exc)
    # oss2 exceptions may stringify signed requests and arbitrary response payloads.
    code = getattr(exc, "code", None)
    status = getattr(exc, "status", None)
    request_id = getattr(exc, "request_id", None)
    if code or status:
        return f"OSS {code or type(exc).__name__} (status={status}, request_id={request_id or '-'})"
    return type(exc).__name__


class OssFiles:
    def __init__(
        self,
        repo: Any,
        binding: OssBinding,
        *,
        oss_module: Any = None,
        state_dir: Path | None = None,
    ):
        self.repo, self.binding = repo, binding
        self.encoding_type = None
        self.payer = None
        self.disable_crc64 = False
        self.multipart_threshold = COPY_MULTIPART_THRESHOLD
        self.part_size = None
        self.write_headers: dict[str, str] = {}
        self.byte_range = None
        self.disable_all_symlink = False
        self.verbose = False
        if oss_module is None:
            from instance_repo.store.oss import _import_oss2

            oss_module = _import_oss2()
        self.oss = oss_module
        self.state_dir = state_dir or Path.home() / ".ap" / ".cache" / "ossutil"
        self._endpoint: str | None = None
        #: 相对路径 → 解析出的 dataset 名;``None`` 也进缓存(用键存在性判断命中,
        #: 区分"无 dataset"与"尚未解析")。缓存只在本命令生命周期内有效。
        self._dataset_cache: dict[str, str | None] = {}

    def resolve(self, value: str, **kwargs) -> RemotePath:
        return self.binding.resolve(value, encoding_type=self.encoding_type, **kwargs)

    def _dataset_for_scope(self, scope: str) -> str | None:
        """解析覆盖 ``scope``(完整对象 key)的已注册 dataset 名。

        凭据请求携带 ``dataset_name``:普通调用方在控制面按它走 dataset RBAC(旧 prod
        构建也要求显式上下文)。ans:// 路径是 dataset 相对的,dataset 名就是最长前缀
        (任意深度的最长已注册前缀优先);由于 ``A``(L1)与 ``A/B`` 可能同时是合法布局,
        这里以**注册表为准**:候选按"最长优先"查注册,第一个命中者胜出;都未注册时退回
        原有最多两段上下文(系统身份的 raw 路径与服务端的 list-only 发现都会校验
        claimed 命名空间,写操作仍由服务端拒绝)。结果按相对路径缓存,一次命令内多次
        签发只查一次。
        """
        prefix = self.binding.prefix
        if not scope.startswith(prefix):
            return None
        relative = scope[len(prefix) :].rstrip("/")
        if relative in self._dataset_cache:
            return self._dataset_cache[relative]
        name = self._resolve_dataset_name(relative)
        self._dataset_cache[relative] = name
        return name

    def _resolve_dataset_name(self, relative: str) -> str | None:
        from .dataset_name import DatasetNameError, parse_dataset_name

        segments = [segment for segment in relative.split("/") if segment]
        if not segments:
            return None
        # Validate each segment with the SDK. Older SDKs only parse one or two
        # levels at a time; that limit must not truncate registry lookup paths.
        valid: list[str] = []
        for index, segment in enumerate(segments):
            try:
                parse_dataset_name(segment)
            except DatasetNameError:
                break
            valid.append("/".join(segments[: index + 1]))
        valid.reverse()
        if not valid:
            return None
        for candidate in valid:
            try:
                self.repo.datasets.get(candidate, fallback_to_oss=False)
            except Exception as exc:  # noqa: BLE001 - 只吞"未注册",其余必须上抛
                if getattr(exc, "biz_code", None) not in _DATASET_NOT_FOUND_CODES:
                    raise
                continue
            return candidate
        # 未注册路径的 list-only 发现与写操作仍由服务端授权。
        # Preserve the legacy raw-OSS discovery namespace when none is registered.
        return valid[-2] if len(valid) >= 2 else valid[0]

    def _credentials(self, scope: str, permission: str, list_only: bool) -> dict:
        kwargs: dict[str, Any] = {}
        dataset = self._dataset_for_scope(scope)
        if dataset:
            kwargs["dataset_name"] = dataset
        # 双参数齐发:``dataset_source=oss`` 对系统白名单/平台管理员是跳过 RBAC 的
        # raw 快速路径(ossutil 式,与数据集注册无关);普通调用方在新 apiserver 上会
        # 忽略该参数并回落 dataset RBAC(用上面的 dataset_name),老 prod 构建本就
        # 不认该参数。两者并存才能同时保住"系统身份无注册直读"与"普通用户受控"。
        kwargs["dataset_source"] = "oss"
        cred = dict(
            self.repo.transport.get_oss_credentials(
                self.binding.bucket,
                scope,
                permission=permission,
                list_only=list_only,
                **kwargs,
            )
        )
        # The SDK treats OSS_REGION as optional; repo-config supplies the signing region.
        cred["region"] = cred.get("region") or self.binding.region
        if cred.get("bucket") != self.binding.bucket or cred.get("region") != self.binding.region:
            raise OssOperationError(
                "STS storage binding differs from repo-config; rerun after refreshing config"
            )
        granted = cred.get("prefix")
        if not isinstance(granted, str) or not (
            scope == granted or granted.endswith("/") and scope.startswith(granted)
        ):
            raise OssOperationError("STS prefix does not cover the requested operation")
        for field in ("access_key_id", "access_key_secret", "security_token"):
            if not isinstance(cred.get(field), str) or not cred[field]:
                raise OssOperationError(f"STS response is missing {field}")
        return cred

    def _require_private_endpoint(self) -> None:
        from instance_repo._routing import _plan_oss_route

        route = _plan_oss_route(self.binding.endpoint)
        if (
            not route.standard
            or _endpoint(route.private_endpoint).lower() != self.binding.endpoint.lower()
        ):
            raise OssOperationError(
                "E_PRIVATE_NETWORK_REQUIRED: repo-config endpoint is not a confirmed private OSS endpoint"
            )

    def bucket(
        self, scope: str, permission: str, *, list_only: bool = False, private_only: bool = False
    ):
        if private_only:
            self._require_private_endpoint()
        initial = self._credentials(scope, permission, list_only)
        provider_class = self.oss.credentials.CredentialsProvider
        owner = self

        class Provider(provider_class):
            def get_credentials(self):
                fresh = owner._credentials(scope, permission, list_only)
                if any(
                    fresh.get(k) != initial.get(k)
                    for k in ("bucket", "region", "prefix", "endpoint")
                ):
                    raise OssOperationError(
                        "STS binding changed during transfer; rerun the command"
                    )
                return owner.oss.credentials.Credentials(
                    fresh["access_key_id"], fresh["access_key_secret"], fresh["security_token"]
                )

        probe = getattr(getattr(self.repo, "_content", None), "_probe_cached", None)
        if not callable(probe):
            raise OssOperationError(
                "Installed instance-repo SDK has no compatible network probe; upgrade ap-client[dataset]"
            )
        if private_only:
            # Availability caching is delegated to SDK; a previously selected public
            # endpoint is never a valid route for content downloads.
            if not probe(self.binding.endpoint):
                raise OssOperationError(
                    "E_PRIVATE_NETWORK_REQUIRED: private OSS endpoint is unreachable; "
                    "run with private-network access"
                )
            endpoint = self.binding.endpoint
        elif self._endpoint is None:
            if probe(self.binding.endpoint):
                self._endpoint = self.binding.endpoint
            elif self.binding.public_endpoint and probe(self.binding.public_endpoint):
                self._endpoint = self.binding.public_endpoint
            else:
                raise OssOperationError(
                    "OSS network unavailable: configured private and public endpoints are unreachable"
                )
            endpoint = self._endpoint
        else:
            endpoint = self._endpoint
        session = self.oss.Session()
        session.session.trust_env = False
        session.session.max_redirects = 0
        bucket = self.oss.Bucket(
            self.oss.ProviderAuthV4(Provider()),
            endpoint,
            self.binding.bucket,
            region=self.binding.region,
            session=session,
            proxies={},
            connect_timeout=30,
            enable_crc=not self.disable_crc64,
        )
        return _RoutingBucket(bucket, self, endpoint)

    def invalidate_network(self, exc: Exception, endpoint: str | None = None) -> None:
        from .irepo_sdk import _invalidate_oss_probe_cache, _sdk_reachability_classifier

        classify = _sdk_reachability_classifier()
        endpoint = endpoint or self._endpoint
        if not endpoint or not classify or not classify(exc):
            return
        content = getattr(self.repo, "_content", None)
        cache = getattr(content, "_probe_cache", None)
        if isinstance(cache, dict):
            cache.pop(endpoint, None)
        if self._endpoint == endpoint:
            self._endpoint = None
        try:
            _invalidate_oss_probe_cache(endpoint, None, verbose=False)
        except Exception:
            # Cache maintenance cannot hide the actual transport failure.
            pass

    def list(
        self,
        remote: RemotePath,
        *,
        recursive: bool = False,
        limit: int | None = None,
        marker: str = "",
        include: tuple[str, ...] = (),
        exclude: tuple[str, ...] = (),
    ) -> dict:
        # 目录意图必须由调用方显式表达(resolve(directory=True) 或尾斜杠):不再把
        # "恰好两段"当作 Dataset root 的隐式目录启发(单段 L1 与两段 L1/L2 都是合法
        # root,段数与目录性无关)。未显式收目录时,remote.key 即前缀语义。
        if marker:
            marker = self.resolve(marker, prefix=True).key
            if not marker.startswith(remote.key):
                raise OssUsageError("--marker must be within the listed prefix")
        bucket = self.bucket(remote.key, "reader", list_only=True)
        entries = []
        while limit is None or len(entries) < limit:
            result = bucket.list_objects(
                prefix=remote.key,
                delimiter="" if recursive else "/",
                marker=marker,
                max_keys=min(1000, limit - len(entries)) if limit is not None else 1000,
            )
            for item in result.object_list:
                path = self._listed_path(item.key, remote.key)
                if not matches(path, include, exclude):
                    continue
                entries.append(
                    {
                        "path": path,
                        "type": "file",
                        "size": item.size,
                        "etag": item.etag,
                        "last_modified": item.last_modified,
                    }
                )
            for key in result.prefix_list:
                path = self._listed_path(key, remote.key)
                if matches(path, include, exclude):
                    entries.append({"path": path, "type": "directory"})
            if not result.is_truncated:
                return {"entries": entries, "is_truncated": False, "next_marker": ""}
            next_marker = result.next_marker
            if not next_marker or next_marker == marker:
                raise OssOperationError("OSS returned an invalid pagination marker")
            marker = next_marker
        return {
            "entries": entries,
            "is_truncated": True,
            "next_marker": marker[len(self.binding.prefix) :],
        }

    def _listed_path(self, key: str, prefix: str) -> str:
        if not key.startswith(prefix) or not key.startswith(self.binding.prefix):
            raise OssOperationError("OSS listing returned an object outside the requested prefix")
        path = key[len(self.binding.prefix) :]
        _relative(path, allow_empty=True)
        return path

    def stat(self, remote: RemotePath) -> dict:
        bucket = self.bucket(remote.key, "reader")
        result = bucket.head_object(remote.key)
        acl = bucket.get_object_acl(remote.key)
        return {
            "path": remote.path,
            "size": result.content_length,
            "etag": result.etag,
            "last_modified": result.last_modified,
            "content_type": result.headers.get("Content-Type"),
            "acl": acl.acl,
            "metadata": {
                k: v for k, v in result.headers.items() if k.lower().startswith("x-oss-meta-")
            },
            "crc64": getattr(result, "crc", None),
        }

    def cat(self, remote: RemotePath, output: Any) -> None:
        result = self.bucket(remote.key, "reader", private_only=True).get_object(remote.key)
        try:
            from .ossutil_hash import _stored_content_stream

            stream = _stored_content_stream(result)
            while data := stream.read(1024 * 1024):
                output.write(data)
        finally:
            result.resp.response.close()

    @contextmanager
    def _lock(self, name: str):
        import fcntl

        self.state_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
        if self.state_dir.is_symlink():
            raise OssOperationError("Transfer state directory cannot be a symlink")
        self.state_dir.chmod(0o700)
        directory = self.state_dir / "locks"
        directory.mkdir(parents=True, exist_ok=True, mode=0o700)
        if directory.is_symlink():
            raise OssOperationError("Transfer lock directory cannot be a symlink")
        directory.chmod(0o700)
        path = directory / hashlib.sha256(name.encode()).hexdigest()
        fd = os.open(path, os.O_CREAT | os.O_RDWR | getattr(os, "O_NOFOLLOW", 0), 0o600)
        try:
            os.fchmod(fd, 0o600)
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError as exc:
                raise OssOperationError("Another transfer is using this target") from exc
            yield
        finally:
            os.close(fd)

    def _store(self, kind: str) -> SecureStore:
        cls = self.oss.ResumableStore if kind != "download" else self.oss.ResumableDownloadStore
        return SecureStore(self.state_dir / kind, cls)

    def _progress(self, path: str, callback: Callable | None):
        last = [0.0]

        def report(done, total):
            now = time.monotonic()
            if callback and (done == total or now - last[0] >= 1):
                last[0] = now
                callback(path, done, total)

        return report

    def upload(
        self,
        bucket,
        local: Path,
        remote: RemotePath,
        *,
        overwrite: bool,
        jobs: int,
        progress: Callable | None,
    ) -> None:
        if not local.is_file() or local.is_symlink():
            raise OssUsageError("Upload source must be a regular file, not a symlink")
        headers = dict(self.write_headers)
        if not overwrite:
            headers["x-oss-forbid-overwrite"] = "true"
        with self._lock("write:" + remote.bucket + "/" + remote.key):
            self.oss.resumable_upload(
                _WriteBucket(bucket, overwrite),
                remote.key,
                str(local),
                store=self._store("upload"),
                headers=headers,
                num_threads=jobs,
                multipart_threshold=self.multipart_threshold,
                part_size=self.part_size,
                progress_callback=self._progress(remote.path, progress),
            )

    def download(
        self,
        bucket,
        remote: RemotePath,
        target: Path,
        *,
        overwrite: bool,
        jobs: int,
        progress: Callable | None,
    ) -> None:
        self._require_private_endpoint()
        if getattr(bucket, "_ossutil_endpoint", None) != self.binding.endpoint:
            raise OssOperationError(
                "E_PRIVATE_NETWORK_REQUIRED: file downloads require the configured private endpoint"
            )
        self._check_local_path(target)
        target.parent.mkdir(parents=True, exist_ok=True)
        with self._lock("download:" + str(target.absolute())):
            self._check_local_path(target)
            if target.exists() and not overwrite:
                raise OssOperationError(f"Local target already exists: {target}; use --force")
            suffix = hashlib.sha256((remote.bucket + remote.key).encode()).hexdigest()[:16]
            # oss2 creates random .tmp-* siblings, so protect their directory
            # throughout the download, including interruptions and retries.
            staging = target.with_name(f".ap-{target.name}-{suffix}.download")
            staging.mkdir(mode=0o700, exist_ok=True)
            directory_fd = os.open(
                staging, os.O_RDONLY | os.O_DIRECTORY | getattr(os, "O_NOFOLLOW", 0)
            )
            try:
                if os.fstat(directory_fd).st_uid != os.getuid():
                    raise OssOperationError("Download staging directory must belong to this user")
                os.fchmod(directory_fd, 0o700)
            finally:
                os.close(directory_fd)
            partial = staging / "content.part"
            fd = os.open(partial, os.O_CREAT | os.O_WRONLY | getattr(os, "O_NOFOLLOW", 0), 0o600)
            try:
                os.fchmod(fd, 0o600)
            finally:
                os.close(fd)
            if self.byte_range is not None:
                result = bucket.get_object(
                    remote.key,
                    byte_range=self.byte_range,
                    progress_callback=self._progress(remote.path, progress),
                )
                try:
                    with partial.open("wb") as output:
                        while data := result.read(1024 * 1024):
                            output.write(data)
                finally:
                    result.resp.response.close()
            else:
                self.oss.resumable_download(
                    bucket,
                    remote.key,
                    str(partial),
                    store=self._store("download"),
                    num_threads=jobs,
                    multiget_threshold=self.multipart_threshold,
                    part_size=self.part_size,
                    progress_callback=self._progress(remote.path, progress),
                )
            fd = os.open(partial, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
            try:
                if not stat.S_ISREG(os.fstat(fd).st_mode):
                    raise OssOperationError("Download staging content must be a regular file")
                os.fchmod(fd, 0o600)
            finally:
                os.close(fd)
            self._check_local_path(target)
            if overwrite:
                os.replace(partial, target)
            else:
                os.link(partial, target)
                partial.unlink()
            staging.rmdir()

    @staticmethod
    def _check_local_path(path: Path) -> None:
        for item in (path, *path.parents):
            if item.is_symlink():
                raise OssUsageError("Download target cannot contain symlinks")
        if path.exists() and not path.is_file():
            raise OssUsageError("Download target must be a file")

    def copy_object(
        self,
        bucket,
        src: RemotePath,
        dst: RemotePath,
        *,
        overwrite: bool,
        jobs: int,
        progress: Callable | None,
    ) -> None:
        if src.key == dst.key:
            raise OssUsageError("OSS copy source and destination must differ")
        source = bucket.head_object(src.key)
        headers = {"x-oss-copy-source-if-match": source.etag, **self.write_headers}
        if self.write_headers:
            headers["x-oss-metadata-directive"] = "REPLACE"
        if not overwrite:
            headers["x-oss-forbid-overwrite"] = "true"
        with self._lock("write:" + dst.bucket + "/" + dst.key):
            if source.content_length < self.multipart_threshold:
                bucket.copy_object(src.bucket, src.key, dst.key, headers=headers)
                if progress:
                    progress(dst.path, source.content_length, source.content_length)
                return
            store = self._store("copy")
            record_key = hashlib.sha256(
                (src.bucket + src.key + "\0" + dst.key).encode()
            ).hexdigest()
            record = store.get(record_key)
            if record and (
                record.get("etag") != source.etag or record.get("size") != source.content_length
            ):
                bucket.abort_multipart_upload(dst.key, record["upload_id"])
                store.delete(record_key)
                record = None
            if not record:
                part_size = self.oss.determine_part_size(
                    source.content_length, preferred_size=self.part_size or 8 * 1024 * 1024
                )
                record = {
                    "etag": source.etag,
                    "size": source.content_length,
                    "part_size": part_size,
                    "upload_id": bucket.init_multipart_upload(
                        dst.key, headers=self.write_headers
                    ).upload_id,
                }
                store.put(record_key, record)
            upload_id, part_size = record["upload_id"], record["part_size"]
            parts, marker = {}, ""
            try:
                while True:
                    result = bucket.list_parts(dst.key, upload_id, marker=marker)
                    parts.update({part.part_number: part for part in result.parts})
                    if not result.is_truncated:
                        break
                    if not result.next_marker or result.next_marker == marker:
                        raise OssOperationError("Invalid multipart pagination marker")
                    marker = result.next_marker
            except Exception as exc:
                if getattr(exc, "code", None) == "NoSuchUpload":
                    store.delete(record_key)
                    raise OssOperationError(
                        "Saved OSS copy upload no longer exists; rerun to start again"
                    ) from exc
                raise
            # Copy parts in a bounded queue; source ETag is checked for every part.
            count = (source.content_length + part_size - 1) // part_size
            done_bytes = sum(
                min(part_size, source.content_length - (n - 1) * part_size) for n in parts
            )

            def transfer(number):
                start = (number - 1) * part_size
                end = min(source.content_length, start + part_size) - 1
                result = bucket.upload_part_copy(
                    src.bucket,
                    src.key,
                    (start, end),
                    dst.key,
                    upload_id,
                    number,
                    headers={"x-oss-copy-source-if-match": source.etag},
                )
                return self.oss.models.PartInfo(number, result.etag)

            for _, part, error in self._bounded(
                ((str(n), n) for n in range(1, count + 1) if n not in parts), transfer, jobs
            ):
                if error:
                    raise error
                parts[part.part_number] = part
                done_bytes += min(
                    part_size, source.content_length - (part.part_number - 1) * part_size
                )
                if progress:
                    progress(dst.path, done_bytes, source.content_length)
            completion = _WriteBucket(bucket, overwrite).complete_multipart_upload(
                dst.key, upload_id, [parts[n] for n in range(1, count + 1)]
            )
            if (
                not self.disable_crc64
                and getattr(source, "crc", None) is not None
                and getattr(completion, "crc", None) is not None
            ):
                if source.crc != completion.crc:
                    raise OssOperationError("OSS copy CRC64 mismatch")
            store.delete(record_key)
            if progress:
                progress(dst.path, source.content_length, source.content_length)

    @staticmethod
    def _bounded(items: Iterator, operation: Callable, jobs: int, stop_on_error: bool = False):
        with ThreadPoolExecutor(max_workers=jobs) as executor:
            pending = {}
            done_reading = False
            while pending or not done_reading:
                while not done_reading and len(pending) < jobs * 2:
                    try:
                        name, value = next(items)
                    except StopIteration:
                        done_reading = True
                        break
                    except Exception as exc:
                        done_reading = True
                        yield "enumeration", None, exc
                        break
                    pending[executor.submit(operation, value)] = name
                if not pending:
                    continue
                finished, _ = wait(pending, return_when=FIRST_COMPLETED)
                for future in finished:
                    name = pending.pop(future)
                    if future.cancelled():
                        continue
                    try:
                        yield name, future.result(), None
                    except Exception as exc:
                        yield name, None, exc
                        if stop_on_error:
                            done_reading = True
                            for queued in pending:
                                queued.cancel()

    def _objects(self, bucket, prefix: str):
        token = ""
        while True:
            result = bucket.list_objects_v2(prefix=prefix, continuation_token=token, max_keys=1000)
            for item in result.object_list:
                self._listed_path(item.key, prefix)
                if item.key != prefix and not item.key.endswith("/"):
                    yield item.key
            if not result.is_truncated:
                break
            new_token = result.next_continuation_token
            if not new_token or new_token == token:
                raise OssOperationError("OSS returned an invalid pagination token")
            token = new_token

    def cp(
        self,
        src: str,
        dst: str,
        *,
        direction: str | None = None,
        recursive: bool,
        overwrite: bool,
        jobs: int,
        progress: Callable | None = None,
        parallel: int = 4,
        update: bool = False,
        include: tuple[str, ...] = (),
        exclude: tuple[str, ...] = (),
        only_current_dir: bool = False,
        stop_on_error: bool = False,
        confirm: Callable | None = None,
        start_time: int | None = None,
        end_time: int | None = None,
    ) -> dict:
        if direction is None:
            # Library convenience for direct callers; the CLI commands pass the
            # direction explicitly so relative remote paths stay unambiguous.
            direction = direction_for(src, dst)
        elif direction not in ("upload", "download", "copy"):
            raise OssUsageError("direction must be upload, download or copy")
        remote_src = self.resolve(src, directory=recursive) if direction != "upload" else None
        remote_dst = None
        if direction != "download":
            target_directory = recursive or dst.endswith("/")
            remote_dst = self.resolve(dst, directory=target_directory)
            if target_directory and not recursive:
                name = Path(src).name if direction == "upload" else remote_src.key.rsplit("/", 1)[1]
                remote_dst = self.binding.resolve(remote_dst.path + name)
        if direction == "copy" and recursive and remote_dst.key.startswith(remote_src.key):
            raise OssUsageError(
                "Recursive OSS copy destination cannot be inside the source directory"
            )
        if direction == "upload":
            local = Path(src)
            if local.is_symlink() or not (local.is_dir() if recursive else local.is_file()):
                raise OssUsageError("Upload source must be a regular file or a directory with -r")
        if self.byte_range is not None and (direction != "download" or recursive):
            raise OssUsageError("--range requires a single-object download")
        if self.write_headers and direction == "download":
            raise OssUsageError("--meta is only supported for upload or OSS copy")
        if direction == "download" and not recursive and (Path(dst).is_dir() or dst.endswith("/")):
            dst = str(Path(dst) / remote_src.key.rsplit("/", 1)[1])
        if direction == "copy":
            parent = os.path.commonpath(
                [remote_src.key.rsplit("/", 1)[0], remote_dst.key.rsplit("/", 1)[0]]
            )
            scope = parent.rstrip("/") + "/"
            if not scope.startswith(self.binding.prefix):
                raise OssUsageError("OSS copy scope is outside repo-config prefix")
        else:
            scope = (remote_dst or remote_src).key
        bucket = self.bucket(
            scope,
            "reader" if direction == "download" else "writer",
            private_only=direction == "download",
        )
        if direction != "download" and not overwrite and not update and confirm is None:
            # OSS ignores forbid-overwrite when versioning is enabled or suspended.
            # A HEAD-then-write check cannot provide atomic protection.
            versioning = bucket.get_bucket_info().versioning_status
            if versioning not in (None, "", "Disabled"):
                raise OssOperationError(
                    "Bucket versioning prevents atomic no-overwrite writes; "
                    "use --force explicitly or an unversioned storage binding"
                )
        if direction == "upload":

            def items():
                if not recursive:
                    yield remote_dst.path, (local, remote_dst)
                    return
                for root, dirs, files in os.walk(local, followlinks=False):
                    if self.disable_all_symlink:
                        dirs[:] = [name for name in dirs if not (Path(root) / name).is_symlink()]
                        files = [name for name in files if not (Path(root) / name).is_symlink()]
                    if any((Path(root) / name).is_symlink() for name in dirs + files):
                        raise OssUsageError("Recursive upload cannot include symlinks")
                    if only_current_dir:
                        dirs[:] = []
                    for filename in files:
                        path = Path(root) / filename
                        relative = path.relative_to(local).as_posix()
                        remote = self.binding.resolve(remote_dst.path + relative)
                        yield remote.path, (path, remote)

            def transfer(value):
                path, remote = value
                self.upload(
                    bucket,
                    path,
                    remote,
                    overwrite=overwrite,
                    jobs=parallel,
                    progress=progress,
                )
        else:

            def items():
                keys = (
                    self._objects(bucket, remote_src.key) if recursive else iter([remote_src.key])
                )
                for key in keys:
                    remote = self.binding.resolve(key[len(self.binding.prefix) :])
                    relative = key[len(remote_src.key) :] if recursive else ""
                    if direction == "download":
                        target = Path(dst) / relative if recursive else Path(dst)
                        if recursive and not target.absolute().is_relative_to(Path(dst).absolute()):
                            raise OssUsageError("Download path is outside the target directory")
                        yield remote.path, (remote, target)
                    else:
                        target = (
                            self.binding.resolve(remote_dst.path + relative)
                            if recursive
                            else remote_dst
                        )
                        yield target.path, (remote, target)

            def transfer(value):
                remote, target = value
                if direction == "download":
                    self.download(
                        bucket,
                        remote,
                        target,
                        overwrite=overwrite,
                        jobs=parallel,
                        progress=progress,
                    )
                else:
                    self.copy_object(
                        bucket,
                        remote,
                        target,
                        overwrite=overwrite,
                        jobs=parallel,
                        progress=progress,
                    )

        force_overwrite = overwrite
        transfer_file = transfer
        skipped = []

        def transfer(value):
            source, target = value
            path = (
                source.relative_to(local).as_posix()
                if direction == "upload" and recursive
                else (source.name if direction == "upload" else source.path)
            )
            if (
                only_current_dir
                and direction != "upload"
                and recursive
                and "/" in source.key[len(remote_src.key) :]
            ):
                return False
            if not matches(path, include, exclude):
                return False
            modified = (
                source.stat().st_mtime
                if direction == "upload"
                else bucket.head_object(source.key).last_modified
            )
            if (
                start_time is not None
                and modified < start_time
                or end_time is not None
                and modified > end_time
            ):
                return False
            exists, target_modified = False, 0
            if direction == "download":
                self._check_local_path(target)
                exists = target.exists()
                if exists:
                    target_modified = target.stat().st_mtime
            elif update or confirm:
                try:
                    target_modified = bucket.head_object(target.key).last_modified
                    exists = True
                except Exception as exc:
                    if getattr(exc, "code", None) != "NoSuchKey":
                        raise
            if update and exists and modified <= target_modified:
                return False
            if (
                exists
                and not force_overwrite
                and not update
                and confirm
                and not confirm(target.path if direction != "download" else str(target))
            ):
                return False
            transfer_file(value)
            if direction == "download":
                os.utime(target, (modified, modified))
            return True

        # update and an accepted overwrite prompt use ordinary ossutil replacement semantics.
        overwrite = overwrite or update or confirm is not None
        completed, failed = [], []
        for name, copied, error in self._bounded(
            iter(items()), transfer, jobs if recursive else 1, stop_on_error
        ):
            if error:
                if self.verbose:
                    # Frames only: exception text may embed signed URLs or STS material.
                    import sys
                    import traceback

                    sys.stderr.write("Traceback (most recent call last):\n")
                    sys.stderr.writelines(traceback.format_tb(error.__traceback__))
                    sys.stderr.write(f"error: {safe_error(error)}\n")
                failed.append({"path": name, "error": safe_error(error)})
            elif copied:
                completed.append(name)
            else:
                skipped.append(name)
        return {
            "direction": direction,
            "completed": completed,
            "failed": failed,
            "skipped": skipped,
            "completed_count": len(completed),
            "failed_count": len(failed),
            "skipped_count": len(skipped),
        }

    def _mkdir_marker_exists(self, bucket, remote: RemotePath) -> bool:
        from .ossutil_hash import _close_result

        try:
            result = bucket.head_object(remote.key)
        except Exception as exc:
            if getattr(exc, "code", None) == "NoSuchKey":
                return False
            raise
        try:
            if result.content_length != 0:
                raise OssOperationError("mkdir refuses an existing non-empty directory marker")
            return True
        finally:
            _close_result(result)

    def mkdir(self, remote: RemotePath) -> dict:
        """Create a zero-byte directory marker; no-overwrite is best-effort.

        - 未版本化桶:forbid-overwrite 由 OSS 强制执行,HEAD→PUT 原子拒绝并发
          非空 marker(FileAlreadyExists 时回退幂等检查);
        - 版本化/版本状态未知的桶:OSS 忽略 forbid-overwrite,并发写入的非空
          marker 可能被本操作的新空版本遮蔽(旧内容仍作为历史版本保留)。
          这是版本化语义下的已知局限——mkdir 用于目录占位,不保证跨版本强一致。
        """
        from .ossutil_hash import _close_result

        if (
            not isinstance(remote, RemotePath)
            or not remote.key.endswith("/")
            or remote != self.binding.resolve(remote.path, directory=True)
        ):
            raise OssUsageError("mkdir requires a directory within the configured OSS binding")
        bucket = self.bucket(remote.key, "writer")
        if self._mkdir_marker_exists(bucket, remote):
            return {"path": remote.path, "created": False}
        # 版本控制探测是尽力而为：旧构建的 dataset STS 缺 GetBucketInfo
        # （AccessDenied 403），或桶开启/暂停版本控制时 forbid-overwrite 会被
        # OSS 忽略。对 zero-byte 目录 marker 这两者都无害——重复 mkdir 至多
        # 多出一个空 marker 版本，"非空 marker 拒绝"仍由上面的 HEAD 保证；
        # 因此不再因无法确认版本状态而硬拒，写入保持 forbid-overwrite 尽力语义。
        try:
            info = bucket.get_bucket_info()
        except Exception as exc:
            if getattr(exc, "code", None) != "AccessDenied":
                raise
        else:
            _close_result(info)
        try:
            result = bucket.put_object(remote.key, b"", headers={"x-oss-forbid-overwrite": "true"})
        except Exception as exc:
            if getattr(exc, "code", None) != "FileAlreadyExists":
                raise
            if self._mkdir_marker_exists(bucket, remote):
                return {"path": remote.path, "created": False}
            raise OssOperationError(
                "Concurrent mkdir conflict; rerun after checking the marker"
            ) from exc
        _close_result(result)
        return {"path": remote.path, "created": True}

    def _hash_object(
        self,
        remote: RemotePath,
        algorithm: str,
        download: bool,
        base64_output: bool,
    ) -> dict:
        from .ossutil_hash import (
            _close_result,
            _hash_request,
            _hash_stream,
            _metadata_hash,
            _stored_content_stream,
        )

        reader = self.bucket(remote.key, "reader")
        head = _hash_request(reader, "head_object", remote.key)
        try:
            value = None if download else _metadata_hash(head.headers, algorithm, base64_output)
            size = getattr(head, "content_length", None)
            if value is not None:
                result = {
                    "path": remote.path,
                    "algorithm": algorithm,
                    "hash": value,
                    "source": "metadata",
                }
                if size is not None:
                    result["size"] = size
                return result
            content_encoded = any(
                key.lower() == "content-encoding" and bool(header_value)
                for key, header_value in head.headers.items()
            )
            etag = getattr(head, "etag", None)
            if not isinstance(etag, str) or not etag or etag.startswith("W/"):
                raise OssOperationError("HEAD returned no valid ETag for a conditional hash read")
            # oss2 strips quotes from ETags; HTTP If-Match uses a quoted strong tag.
            if not etag.startswith('"'):
                etag = '"' + etag + '"'
            if not re.fullmatch(r'"[\x21\x23-\x7e\x80-\xff]+"', etag):
                raise OssOperationError("HEAD returned no valid ETag for a conditional hash read")
            expected_size = size
        finally:
            _close_result(head)
        reader = self.bucket(remote.key, "reader", private_only=True)
        content = _hash_request(reader, "get_object", remote.key, headers={"If-Match": etag})
        try:
            stored_stream = _stored_content_stream(content, content_encoded=content_encoded)
            value, size = _hash_stream(stored_stream, algorithm, base64_output)
            if expected_size is not None and size != expected_size:
                raise OssOperationError(
                    "Hash content length differs from HEAD; possible truncated read"
                )
        finally:
            _close_result(content)
        return {
            "path": remote.path,
            "algorithm": algorithm,
            "hash": value,
            "source": "content",
            "size": size,
        }

    def hash(
        self,
        path: str,
        algorithm: str,
        *,
        download: bool = False,
        base64_output: bool = False,
        recursive: bool = False,
    ) -> dict:
        """Prefer validated HEAD hashes; read missing hashes only over private OSS."""
        from .ossutil_hash import _validate_options

        _validate_options(algorithm, base64_output)
        remote = self.resolve(path, directory=recursive)
        if not recursive:
            return self._hash_object(remote, algorithm, download, base64_output)
        entries, failed = [], []
        try:
            listing = self.bucket(remote.key, "reader", list_only=True)
            for key in self._objects(listing, remote.key):
                # Listed keys are already decoded. Do not apply encoding_type twice.
                item = self.binding.resolve(key[len(self.binding.prefix) :])
                try:
                    entries.append(self._hash_object(item, algorithm, download, base64_output))
                except Exception as exc:
                    failed.append({"path": item.path, "error": safe_error(exc)})
        except Exception as exc:
            failed.append({"path": remote.path, "error": safe_error(exc)})
        return {"entries": entries, "failed": failed, "failed_count": len(failed)}
