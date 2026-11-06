"""repo.py — Repo Facade：组装 transport + store + 三资源客户端。"""
from __future__ import annotations

import logging
import os
import posixpath
import threading

logger = logging.getLogger(__name__)

from . import bootstrap
from . import paths as P
from .clients.config import (
    ENV_API_KEY,
    LEGACY_ENV_API_KEY,
    STORAGE_ENV_PROD,
    business_metadata_model,
    fetch_repo_config,
    fetch_user_data_config,
    load_profile,
    normalize_storage_env,
    resolve_config_value,
)
from .clients.benchmarks import BenchmarksClient
from .clients.datasets import DatasetsClient
from .clients.images import ImageClient
from .clients.instances import InstancesClient
from .clients.reports import ReportsClient
from .clients.scaffold import ScaffoldClient
from .clients.splits import SplitsClient
from .clients.versions import VersionsClient
from .clients.workflows import WorkflowsClient
from .concurrency import ItemError
from .errors import JobFailed, RegistrationFailed, SchemaError
from .store.acr import AcrImageStore
from .store.oss import OssContentStore
from .store.registry import ApiMetadataRegistry
from .transport import Transport


# Public canonical user-data values contain metadata only, never leases or URLs.
from dataclasses import dataclass, replace
from pathlib import Path
from types import MappingProxyType
from collections.abc import Mapping
import math

from .errors import RequestDeadlineExceeded, TransportError
from .clients.user_data_writes import (
    PROTOCOL as _WRITE_PROTOCOL, ReplicasPolicy, UserDataWritesClient,
    BeginOutcome, BeginWriteResult, CommitWriteResult, UserDataWriteError,
    UserDataWritePartial, UserDataWritePending, UserDataWriteNotFound, UserDataWriteConflict,
    UserDataUpgradeRequired, UserDataWriteUnauthorized, StatusResult, _Budget,
    _SourceIdentity, _open_regular, _sha256_file, _resolve_replica_policy, _derive_users_key,
    _SHA256_RE, _OP_ID_RE, _UUID_RE, _sanitize_error_data, new_idempotency_key, validate_idempotency_key,
)
from .clients.user_data_upload import UserDataUploadError as _UploadError
from .clients.user_data_reads import (
    UserDataReadsClient, CanonicalReadResolution, LegacyReadResolution,
    ReadAnchor, VerifiedReadResult, LegacyReadResult,
)
from .clients.user_data_entries import (
    UserDataEntriesClient, UserDataEntriesIncomplete, MAX_ROWS, MAX_BYTES, MAX_PAGES,
    _bound as _entries_bound,
)


def _facade_schema():
    return SchemaError("invalid canonical user-data input or result")


def _facade_budget(seconds):
    valid = False
    try:
        valid = (not isinstance(seconds, bool) and isinstance(seconds, (int, float))
                 and math.isfinite(seconds) and seconds >= 0)
    except (ValueError, OverflowError):
        pass
    if not valid:
        raise _facade_schema()
    budget = _Budget(seconds)
    budget.raise_if_exhausted()
    return budget


def _facade_call(function, *args, op_id=None, _bound_idempotency_key=None, **kwargs):
    """Preserve typed classification without retaining a remote exception object."""
    safe = None
    try:
        return function(*args, **kwargs)
    except RequestDeadlineExceeded:
        safe = RequestDeadlineExceeded("canonical user-data deadline exhausted")
    except UserDataWriteError as error:
        data = _sanitize_error_data(error.data, bound_op_id=op_id)
        if isinstance(op_id, str) and _OP_ID_RE.fullmatch(op_id):
            data["op_id"] = op_id
        safe = type(error)("canonical user-data operation failed", status=error.status,
            biz_code=error.biz_code, error_code=type(error).error_code, data=data)
    except TransportError as error:
        if type(error.biz_code) is int and error.biz_code in (94022, 10003):
            safe = UserDataWriteUnauthorized("canonical user-data authorization denied",
                status=error.status, biz_code=error.biz_code, data={})
        else:
            safe = TransportError("canonical user-data transport failed",
                status=error.status, biz_code=error.biz_code, data={})
        if op_id is not None:
            safe.data = {"op_id": op_id}
    except _UploadError as error:
        safe = type(error)("canonical user-data upload failed", kind=type(error).kind,
            status=error.status, retryable=error.retryable, cause=None)
        safe.data = {"op_id": op_id} if op_id is not None else {}
    except (TimeoutError, ConnectionError):
        safe = TransportError("canonical user-data network outcome unknown", status=None,
                              data={"op_id": op_id} if op_id is not None else {})
    except UserDataEntriesIncomplete:
        safe = UserDataEntriesIncomplete("canonical listing incomplete")
    except Exception:
        safe = _facade_schema()
    data = dict(getattr(safe, "data", None) or {})
    if isinstance(op_id, str) and _OP_ID_RE.fullmatch(op_id):
        data["op_id"] = op_id
    if isinstance(_bound_idempotency_key, str) and _UUID_RE.fullmatch(_bound_idempotency_key):
        data["idempotency_key"] = _bound_idempotency_key
    if data:
        safe.data = data
    # from None alone keeps __context__ and its raw remote payload reachable.
    raise safe


class _UserDataCallbackFailed(SchemaError):
    """Private fixed classification; never retain the callback's exception."""
    def __init__(self):
        super().__init__("canonical user-data metadata callback failed")


def _validate_metadata_callbacks(overwrite, on_existing, on_completed=None):
    if (type(overwrite) is not bool
            or (on_existing is not None and (not callable(on_existing) or overwrite))
            or (on_completed is not None and not callable(on_completed))):
        raise _facade_schema()


def _metadata_callback(budget, callback, *args):
    # Synchronous callbacks are cooperative: time counts against the operation,
    # but blocked prompt/display code cannot be forcibly interrupted here.
    budget.raise_if_exhausted()
    failed = False
    try:
        result = callback(*args)
    except Exception:
        failed = True
    if failed:
        # Raising outside except clears both __cause__ and __context__.
        raise _UserDataCallbackFailed()
    budget.raise_if_exhausted()
    return result


def _capture_source_identity(path, *, budget, identity=None):
    # This entire context (including __exit__/close) runs INSIDE _facade_call.
    # Wrapping only _open_regular would leave close errors outside the sanitizer.
    with _open_regular(path, budget=budget, identity=identity) as source:
        return source.identity


def _valid_anchor(anchor):
    return (type(anchor) is ReadAnchor and isinstance(anchor.op_id, str)
        and _OP_ID_RE.fullmatch(anchor.op_id) and type(anchor.generation) is int
        and anchor.generation > 0 and isinstance(anchor.sha256, str)
        and _SHA256_RE.fullmatch(anchor.sha256) and type(anchor.size) is int
        and 0 <= anchor.size <= 2**63 - 1)


@dataclass(frozen=True)
class ObservedUserDataObject:
    owner: str
    relative_path: str
    cluster: str
    storage_id: str
    canonical_key: str
    anchor: ReadAnchor

    def __post_init__(self):
        if (not all(isinstance(value, str) for value in
                (self.owner, self.relative_path, self.cluster, self.storage_id, self.canonical_key))
                or not _valid_anchor(self.anchor) or self.storage_id != "ap-userdata-v1"
                or self.canonical_key != _derive_users_key(self.owner, self.relative_path)):
            raise _facade_schema()


@dataclass(frozen=True)
class UserDataUploadOutcome:
    kind: str
    receipt: CommitWriteResult | None = None
    existing: ObservedUserDataObject | None = None

    def __post_init__(self):
        if self.kind == "skipped_existing":
            if self.receipt is not None or type(self.existing) is not ObservedUserDataObject:
                raise _facade_schema()
        elif self.kind == "committed":
            value = self.receipt
            if (self.existing is not None or type(value) is not CommitWriteResult
                    or value.status != "committed" or value.protocol != _WRITE_PROTOCOL
                    or value.storage_id != "ap-userdata-v1" or type(value.generation) is not int
                    or value.generation <= 0 or not isinstance(value.op_id, str)
                    or not _OP_ID_RE.fullmatch(value.op_id) or not isinstance(value.sha256, str)
                    or not _SHA256_RE.fullmatch(value.sha256) or type(value.size) is not int
                    or not 0 <= value.size <= 2**63 - 1 or not isinstance(value.final, Mapping)
                    or set(value.final) != {"cn", "sg"}):
                raise _facade_schema()
            copied = {}
            for region in ("cn", "sg"):
                row = value.final[region]
                if (not isinstance(row, Mapping) or set(row) != {"bucket", "key"}
                        or not isinstance(row["bucket"], str) or not row["bucket"]
                        or row["key"] != value.canonical_key):
                    raise _facade_schema()
                copied[region] = MappingProxyType(dict(row))
            object.__setattr__(self, "receipt", replace(value, final=MappingProxyType(copied)))
        else:
            raise _facade_schema()


class UserDataDirectoryPartial(UserDataWritePartial):
    """A bounded file batch stopped; completed outcomes are actual prior results."""
    def __init__(self, completed, failed_relative_path, failure):
        super().__init__("canonical user-data directory upload incomplete",
                         biz_code=94104, data={})
        self.completed = tuple(completed)
        self.failed_relative_path = failed_relative_path
        known = isinstance(failure, (UserDataWriteError, TransportError, RequestDeadlineExceeded, _UploadError))
        numeric = getattr(failure, "biz_code", None) if known else None
        status = getattr(failure, "status", None) if known else None
        recovery = getattr(failure, "data", None)
        if known and isinstance(recovery, dict):
            op = recovery.get("op_id")
            key = recovery.get("idempotency_key")
            if isinstance(op, str) and _OP_ID_RE.fullmatch(op):
                self.data["op_id"] = op
            if isinstance(key, str) and _UUID_RE.fullmatch(key):
                self.data["idempotency_key"] = key
        self.failure_biz_code = numeric if type(numeric) is int else None
        self.failure_status = status if type(status) is int and 100 <= status <= 599 else None
        self.failure_code = ("callback_failed" if isinstance(failure, _UserDataCallbackFailed)
            else "deadline_exhausted" if isinstance(failure, RequestDeadlineExceeded)
            else "authorization_denied" if self.failure_biz_code in (94022, 10003)
            else "upload_failed" if isinstance(failure, _UploadError)
            else "write_failed" if isinstance(failure, UserDataWriteError)
            else "transport_failed" if isinstance(failure, TransportError) else "local_failure")


_DIRECTORY_FD_CAPABLE = (os.open in os.supports_dir_fd and os.scandir in os.supports_fd)


class _CanonicalDirectoryScan:
    """Pinned no-follow directory: <=65 iterators + their <=65 original FDs."""
    def __init__(self, path, *, parent_fd=None):
        if (not all(hasattr(os, flag) for flag in ("O_DIRECTORY", "O_NOFOLLOW", "O_NONBLOCK"))
                or not _DIRECTORY_FD_CAPABLE):
            raise SchemaError("bounded no-follow directory traversal is unsupported")
        self.fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW | os.O_NONBLOCK,
                          dir_fd=parent_fd)
        self.closed = False
        try:
            self.iterator = os.scandir(self.fd)
        except BaseException:
            os.close(self.fd)
            raise

    def __next__(self):
        return next(self.iterator)

    def close(self):
        if not self.closed:
            self.closed = True
            try:
                self.iterator.close()
            finally:
                os.close(self.fd)


def _public_upload_dict(outcome):
    if outcome.kind == "skipped_existing":
        value = outcome.existing
        anchor = value.anchor
        return {"key": value.canonical_key, "skipped": True, "status": "skipped_existing",
            "existing_anchor": {"owner": value.owner, "relative_path": value.relative_path,
                "cluster": value.cluster, "storage_id": value.storage_id,
                "op_id": anchor.op_id, "generation": anchor.generation,
                "sha256": anchor.sha256, "size": anchor.size}}
    value = outcome.receipt
    return {"key": value.canonical_key, "skipped": False, "status": "committed",
        "receipt": {"op_id": value.op_id, "generation": value.generation,
            "protocol": value.protocol, "storage_id": value.storage_id,
            "canonical_key": value.canonical_key, "sha256": value.sha256, "size": value.size,
            "final": {r: dict(row) for r, row in value.final.items()}}}


class Repo:
    """SDK 入口。所有 OSS/ACR 操作经此，先向 apiserver 换 STS 再直连。

    为可测：transport 与两个数据面执行器（bucket_factory / runner）均可注入。
    """

    def __init__(self, profile: str = "default", *, token: str | None = None,
                 env: str | None = None, transport=None,
                 bucket_factory=None, runner=None,
                 profile_overrides: dict | None = None,
                 api_env: str | None = None,
                 api_base: str | None = None,
                 cluster: str | None = None,
                 storage_env: str | None = None,
                 metadata_model: str | None = None,
                 expected_replica_policy: ReplicasPolicy | None = None,
                 bootstrap_dataset: bool = True) -> None:
        # v0.8「三参数起步」：token + api_env（控制面）+ storage_env（数据面）。
        # 其余寻址字段（oss_bucket / acr_host / acr_namespace / oss_prefix）由 bootstrap
        # 向 apiserver 的 repo-config 自动拉取，用户无需手填。
        if type(bootstrap_dataset) is not bool:
            raise SchemaError("bootstrap_dataset must be a boolean")
        self._expected_replica_policy = _facade_call(_resolve_replica_policy, expected_replica_policy)
        self._canonical_constructor_cluster = cluster
        self.profile = load_profile(profile, overrides=profile_overrides,
                                    api_env=api_env, api_base=api_base,
                                    cluster=cluster, storage_env=storage_env,
                                    metadata_model=metadata_model)
        tok = resolve_config_value(
            token, ENV_API_KEY, LEGACY_ENV_API_KEY)
        # Env 头：显式 env 优先，否则跟随解析出的 api_env（参数 / IR_API_ENV）；二者都
        # 未提供时由配置解析器使用 "product"，与 load_profile 的运行时契约一致。
        env_header = env if env is not None else self.profile.api_env
        self.transport = transport or Transport(
            self.profile.api_base, tok, env=env_header)
        # 自动发现：只填空字段，显式 overrides 与遗留环境变量优先。**失败不抛**——纯控制面
        # 操作（list/get/create/claim/whoami）不需要数据面寻址，构造期硬失败会把它们一起
        # 阻断；真正缺字段的报错延迟到首次用到该字段时给出，那时才说得清缺什么、为什么。
        # Explicit canonical-only callers may defer Dataset discovery. This does
        # not declare Dataset configuration ready; all real clients still exist.
        if bootstrap_dataset:
            bootstrap.resolve_profile(self.transport, self.profile)
        self._bucket_factory = bucket_factory
        self._content = OssContentStore(
            self.transport, self.profile.oss_bucket,
            bucket_factory=bucket_factory)
        # user-data 独立上下文（F2-R1）：首次 user-data IO 时发现并缓存（独立
        # OssContentStore，bucket/prefix 来自 scope=user-data 配置或用户显式
        # user_data_bucket 覆盖）。惰性 + 单飞，与 Dataset 域 _content 完全隔离。
        self._ud_ctx = None
        self._ud_ctx_lock = threading.Lock()
        self._image = AcrImageStore(
            self.transport, runner=runner,
            prefer_public=self.profile.prefer_public_registry)
        # 读路径必须与写路径对称下发 environment 与 metadata_model：
        # ingest 按 storage_env 写 pre 集合、默认 split_first，读若不下发会查 online/
        # version_first 而闭环断裂（历史真实缺陷，见 store/registry.py）。
        self._registry = ApiMetadataRegistry(
            self.transport,
            environment=self.profile.dataset_environment,
            metadata_model=business_metadata_model(self.profile.metadata_model))
        self.datasets = DatasetsClient(
            self.transport,
            profile=self.profile,
            content_store=self._content,
            oss_prefix=self.profile.oss_prefix,
            metadata_model=self.profile.metadata_model)
        self.versions = VersionsClient(
            self.transport, self.profile,
            content_store=self._content,
            oss_prefix=self.profile.oss_prefix)
        # split 管理模块（1.0.10）：split-first 记录的 list/get/update，
        # dataset 级全量视角（version_scope=all 缺省）。
        self.splits = SplitsClient(
            self.transport, self.profile,
            content_store=self._content,
            oss_prefix=self.profile.oss_prefix)
        # benchmark 目录 / 发布工作流查询（1.0.10）：claim 候选与 publish 状态。
        self.benchmarks = BenchmarksClient(self.transport)
        self.workflows = WorkflowsClient(self.transport)
        # push(register=True) 的上传后写库经 ingest 完成（:commit 端点缺失），
        # 注入 versions.ingest 作为 ingester 回调。
        self.instances = InstancesClient(
            self.transport, self.profile, self._content, self._image,
            self._registry,
            ingester=lambda *args, **kwargs: self.versions.ingest(
                *args, **kwargs))
        self.reports = ReportsClient(self._content, self.profile)
        # 独立镜像能力（v0.8 新增）：push / pull / copy / exists 不再依赖实例目录。
        self.images = ImageClient(self.transport, self.profile, self._image)
        # AgentPlatformScaffoldPackage：仅存储（无元数据）；目标桶/根前缀由 profile 提供
        self.scaffold = ScaffoldClient(
            self.transport, bucket=self.profile.scaffold_bucket,
            root=self.profile.scaffold_root, bucket_factory=bucket_factory)

    def refresh_config(self) -> dict:
        """强制重新拉取数据面寻址（绕过缓存）并回填当前 profile。

        寻址配置变更频率极低，默认缓存一小时；改了服务端配置想立刻生效时调用本方法。
        返回本次解析出的寻址字段字典。
        """
        bootstrap.resolve_profile(self.transport, self.profile, refresh=True)
        return {f: getattr(self.profile, f)
                for f in bootstrap.DISCOVERABLE_FIELDS
                if getattr(self.profile, f, "")}

    # ── 高吞吐批量交付（并发 push(register=False) + 一次 ingest 入库）──
    def deliver(self, dataset: str, version: str, local_dirs, *,
                owner_reference=None,
                split: str = "default", push_image: bool = True,
                overwrite: bool = False, concurrency: int = 8,
                publish: bool = False, ingest: bool = True,
                continue_on_error: bool = False,
                image_release_dst_acr: str | None = None,
                skip_unchanged: bool = False,
                hash_func=None,
                content_hashes: dict | None = None,
                prune: bool = False,
                progress_callback=None,
                executor=None,
                compress_level: int | None = None,
                **ingest_kwargs) -> dict:
        """上传一批实例并只注册实际成功的 instance ID（增量，绝不回退整 split 扫描）。

        Registration includes uploaded and OSS-skipped results, is chunked by the
        instances client, and never widens to a whole-split scan. ``publish=True``
        is the explicit full-intent exception: after every selected chunk completes
        and no upload failed, one full reconcile runs with publish enabled.

        参数:
          owner_reference : 整批共用同一来源引用（批量交付通常同源；需要逐实例不同来源
            时自行循环 ``instances.push``）。CLI 的 push / push-many / deliver 都把它
            设为必填——交付路径必须能追溯上游来源。
          split           : push 与注册共用的 split 名（缺省 ``"default"``）。
          push_image      : 是否推送 harbor 镜像（缺省 True）。
          overwrite       : 覆盖已存在对象（published split 会被前置拒绝）。
          concurrency     : 并发上传线程数（缺省 8）。
          publish         : 显式整 split 发布意图（缺省 False）。True 时在增量注册
            全部完成后执行一次 full reconcile+publish；任一上传失败即抛
            ``RegistrationFailed``（report 为 ``RegistrationReport``），绝不部分发布。
          ingest          : 是否把上传成功的 ID 增量注册入库（缺省 True）。
          continue_on_error : True 时失败项以 ``ItemError`` 占位返回、不阻断成功子集
            注册（缺省 False=全或无）。
          image_release_dst_acr : 可选目标 ACR host，把「实例↔镜像」分发映射写进
            ``extend_meta`` 随本次 ingest 入库。
          skip_unchanged  : 按 ``source_hash`` 跳过未变化实例（配合 hash_func/content_hashes）。
          hash_func / content_hashes : skip_unchanged 的哈希函数 / 预计算映射。
          prune           : **不支持**（缺省 False）。True 在任何 I/O 前抛
            ``SchemaError``——破坏性删除必须先做显式远端/本地对账。
          progress_callback : 每实例完成回调 ``(completed, total, result)``。
          executor        : 外部 ``ThreadPoolExecutor``（复用，不关闭）。
          compress_level  : gzip 压缩级别（1-9），None 用默认。

        其余关键字原样透传给 ``versions.ingest``（full-only 选项在增量模式下前置拒绝；
        ``dry_run`` 不允许——注册必须写库）。返回
        ``{"pushed", "skipped", "failed", "ingest", "ingests", "registration"}``。
        """
        if prune:
            raise SchemaError(
                "prune=True is not supported by deliver; perform an explicit "
                "remote/local reconciliation before any destructive deletion")
        if publish and not ingest:
            raise SchemaError("publish=True requires ingest=True")
        full_only = {
            "storage_path", "splits", "allow_layout_inference",
            "run_type", "split_run_types",
        }
        provided_full_only = sorted(full_only.intersection(ingest_kwargs))
        if provided_full_only and not publish:
            raise SchemaError(
                "incremental deliver does not support full-ingest options: "
                + ", ".join(provided_full_only))
        if ingest_kwargs.get("dry_run"):
            raise SchemaError("deliver cannot use dry_run because registration must write")
        selected_ingest_kwargs = {
            key: value for key, value in ingest_kwargs.items()
            if key not in full_only and key not in {"publish", "dry_run"}
        }

        batch = self.instances.push_many_with_report(
            local_dirs, dataset, version, owner_reference=owner_reference,
            split=split, push_image=push_image,
            overwrite=overwrite, register=ingest, concurrency=concurrency,
            continue_on_error=continue_on_error,
            image_release_dst_acr=image_release_dst_acr,
            skip_unchanged=skip_unchanged,
            hash_func=hash_func,
            content_hashes=content_hashes,
            progress_callback=progress_callback,
            executor=executor,
            compress_level=compress_level,
            ingest_kwargs=selected_ingest_kwargs)
        results = list(batch.results)
        registration = batch.registration
        pushed = [r for r in results
                  if not isinstance(r, ItemError)
                  and not getattr(r, "skipped", False)]
        skipped = [r for r in results
                   if not isinstance(r, ItemError)
                   and getattr(r, "skipped", False)]
        failed = [r for r in results if isinstance(r, ItemError)]
        jobs = [report.job for report in registration.ingests if report.job]

        if publish and not pushed and not skipped and not failed:
            raise SchemaError(
                "publish requires at least one successful or skipped upload")
        if publish and registration.selected_ids:
            if failed:
                # report 统一为 RegistrationReport（与 instances.ingest 抛出的
                # RegistrationFailed 同型，调用方可按同一 schema 恢复）；失败上传项
                # 作为附带诊断挂在报告实例上，不并入注册字段语义。
                registration.failed_uploads = list(failed)
                raise RegistrationFailed(
                    "publish refused after partial upload; selected registration "
                    "is preserved and failed uploads must be reconciled explicitly",
                    report=registration)
            registration_unfinished = (
                registration.pending or registration.failed
                or registration.unknown or registration.not_submitted
                or registration.completed != registration.selected_ids)
            if registration_unfinished:
                last_report = (registration.ingests[-1]
                               if registration.ingests else None)
                raise JobFailed(
                    "selected registration did not complete; refusing full "
                    "reconcile and publish",
                    status=registration.job_status or None,
                    job=(last_report.job if last_report else None),
                    report=registration)
            full_kwargs = dict(ingest_kwargs)
            full_kwargs.pop("publish", None)
            if "splits" not in full_kwargs and "split" not in full_kwargs:
                full_kwargs["split"] = split
            full_job = self.versions.ingest(
                dataset, version, publish=True, **full_kwargs)
            full_status = ((full_job or {}).get("status") or "").lower()
            if full_status != "completed":
                raise JobFailed(
                    "full reconcile did not complete; refusing publish flow",
                    status=full_status or None, job=full_job)
            jobs.append(full_job)

        legacy_job = jobs[0] if len(jobs) == 1 else None
        return {"pushed": pushed, "skipped": skipped, "failed": failed,
                "ingest": legacy_job, "ingests": jobs,
                "registration": registration}

    # ── 源到目标交付：上传 → 元数据入库 → 发布 workflow ────────────────────────
    def deliver_to_prod(self, dataset: str, version: str, local_dirs, *,
                        owner_reference=None,
                        split: str = "default", push_image: bool = True,
                        overwrite: bool = False, concurrency: int = 8,
                        continue_on_error: bool = False,
                        target: str = "", target_overrides: dict | None = None,
                        granularity: str = "instance",
                        images: str | None = None,
                        approval_mode: str = "internal", backend: str = "acr",
                        description: str = "", wait_approval: bool = False,
                        rewrite_task_toml_image: bool = True,
                        raise_on_failure: bool = True,
                        poll_sec: float = 5.0, timeout_sec: float = 1800.0,
                        ingest_raise_on_failure: bool = True,
                        ingest_poll_sec: float = 5.0,
                        ingest_timeout_sec: float = 1800.0,
                        **ingest_kwargs) -> dict:
        """把一批实例从当前 Repo 的源数据面交付到运行时配置的目标数据面。

        尽管方法名保留 ``deliver_to_prod`` 以兼容现有调用，它不绑定 ``dev``、``prod``
        或 ``production`` profile。源 OSS/ACR 来自当前 Repo 的 ``profile_overrides``、
        环境变量或 ``repo-config`` 查询结果；目标 OSS/ACR 由 ``target_overrides`` 提供，
        也可直接使用另一目标的 ``repo-config`` 查询结果。``profile`` / ``target`` 只作标签，
        SDK 不内置任何环境到 bucket、registry 或权限策略的映射。

        调用顺序：

          ① ``push_many(register=False)``  → 写入运行时配置的源 OSS/ACR
          ② 增量注册（selected ingest）   → 只把本次实际成功（含 OSS skipped）的
             instance ID 分块注册入库；**不整 split 发布/锁定**——源侧绝不发送
             ``publish_after_validation``，也不执行 full reconcile
          ③ ``versions.publish``（workflow）→ prod 侧发布：按运行时源/目标寻址把
             对象与镜像分发到目标数据面（审批 / RBAC / 幂等等 workflow 语义原样保留）

        ② **不可跳过**：workflow 按 dataset/version 读取已入库元数据，数据集必须先可查、
        可被下游引用。源侧注册与目标侧发布是两件事：本次交付**不改变源 split 的
        published 状态**，源 split 的发布/锁定必须显式走 ``versions.ingest(publish=True)``
        或 ``splits.update(status='published')``。源与目标访问是否允许完全由运行时服务
        策略决定。

        失败即停（不静默走完后续阶段）：push 阶段按 ``continue_on_error`` 决定全或无；
        增量注册失败抛 ``RegistrationFailed``（附累计 ``RegistrationReport``），
        上架段到失败终态抛 ``JobFailed``。全部 push 失败时不会触发注册与上架
        （返回 ingest=None、release=None）。

        ``images`` 缺省跟随 ``push_image``（推了镜像就同步镜像）。上架只会分发**确实
        位于运行时源 ACR** 的镜像；复用公共/共享 base 的实例其 ``docker_image`` 指向别的
        registry，会被 ``build_image_distributions`` 跳过（见 ``skipped_images``），
        这些 base 由独立的镜像转储流程治理，不随数据集上架搬运。

        ``approval_mode="internal"``（默认）时 workflow 会停在人工审批：
        ``wait_approval=False`` 即在该状态返回，审批通过后由平台继续；置 True 则一直等到终态。
        合法值由 apiserver 定义为 ``internal`` | ``bpms``（其它值 400）。

        ``raise_on_failure`` / ``poll_sec`` / ``timeout_sec`` 作用于**上架段**；
        ingest 段用 ``ingest_raise_on_failure`` / ``ingest_poll_sec`` /
        ``ingest_timeout_sec``（同名具名参数会遮蔽 ``**ingest_kwargs``，故两段必须各有入口）。
        上架段置 ``raise_on_failure=False`` 时返回失败终态的 workflow 供诊断。

        **注册未到 ``completed`` 绝不上架**：增量注册还有"不报错但也没成功"的出口
        （``wait=False`` 提前返回、``raise_on_failure=False`` 时失败终态不抛），此时
        元数据并未真正入库，若继续上架会因源数据不可用而失败。这里显式拦一道并抛
        ``JobFailed``。``dry_run=True`` 与增量注册互斥，会更早地被 ``SchemaError``
        拒绝（见 ``versions.ingest``）。

        返回 ``{"pushed", "failed", "ingest", "release", "skipped_images"}``。
        """
        # 从运行时目标配置解析 ACR host：让 push 阶段就把「实例↔镜像」分发映射写进
        # extend_meta，随本次 ingest 入库（source==docker_ref，与 publish 的
        # image_distributions 同口径）。未提供目标 ACR 时不阻断交付，仅不写该映射。
        image_release_dst_acr = None
        want_images = (images is None and push_image) or (images == "on")
        if want_images:
            # 目标 ACR host 来自 target_overrides（SDK 不内置任何环境的仓地址）。
            image_release_dst_acr = (target_overrides or {}).get("acr_host") or None
        out = self.deliver(dataset, version, local_dirs,
                           owner_reference=owner_reference, split=split,
                           push_image=push_image, overwrite=overwrite,
                           concurrency=concurrency, ingest=True,
                           continue_on_error=continue_on_error,
                           image_release_dst_acr=image_release_dst_acr,
                           raise_on_failure=ingest_raise_on_failure,
                           poll_sec=ingest_poll_sec,
                           timeout_sec=ingest_timeout_sec, **ingest_kwargs)
        out["release"] = None
        out["skipped_images"] = []
        successful = out["pushed"] + out.get("skipped", [])
        if not successful:
            return out                      # 无一成功：不上架（deliver 也未 ingest）
        # deliver 只完成 selected 增量注册（源侧不整 split 发布/锁定、不发
        # publish_after_validation）；多 job 时旧 ingest 字段按契约为 None，
        # 因此必须检查完整 ingests 列表。
        ingest_jobs = out.get("ingests") or []
        ing_status = ((ingest_jobs[-1] if ingest_jobs else {}).get("status")
                      or "").lower()
        if ing_status != "completed":
            last_job = ingest_jobs[-1] if ingest_jobs else None
            raise JobFailed(
                f"ingest 未到 completed（当前 {ing_status or 'unknown'}），拒绝上架："
                f"元数据未入库时上架必然 source_path does not exist",
                status=ing_status or None, job=last_job)
        instances = [r.instance_id for r in successful]
        if not images:                      # None 或 "" 都跟随 push_image（对齐 Go）
            images = "on" if push_image else "off"

        # v0.8：把生产副本 task.toml 的 [environment].docker_image 改写为生产镜像引用。
        # 运行期真正决定拉哪个镜像的是 content.tgz 里的 task.toml，不是元数据里的
        # docker_image 字段；上架只逐字节复制 content.tgz，不改写则生产实例仍拉开发态
        # registry。这里在上架前本地改写并直传目标桶，避免「先复制再下载改回传」的多一趟。
        instance_objects = "all"
        retargeted: list[str] = []
        if rewrite_task_toml_image and images == "on":
            instance_objects, retargeted = self._retarget_prod_task_toml(
                dataset, version, split, local_dirs, out["pushed"],
                target=target, target_overrides=target_overrides,
                overwrite=overwrite)

        wf, skipped = self.versions.publish_with_report(
            dataset, version, instances=instances, target=target,
            target_overrides=target_overrides,
            granularity=granularity, images=images, overwrite=overwrite,
            split=split,          # 与 push 同一 split，否则上架源路径拼错（真机踩过）
            instance_objects=instance_objects,
            approval_mode=approval_mode, backend=backend,
            description=description or f"deliver_to_prod {dataset}/{version} "
                                       f"({len(instances)} instances)",
            wait_approval=wait_approval, raise_on_failure=raise_on_failure,
            poll_sec=poll_sec, timeout_sec=timeout_sec)
        out["release"] = wf
        out["skipped_images"] = skipped
        out["retargeted_task_toml"] = retargeted
        return out

    def _retarget_prod_task_toml(self, dataset, version, split, local_dirs,
                                 pushed, *, target, target_overrides, overwrite):
        """为上架把每个 harbor 实例的 task.toml 指向生产镜像并直传目标桶。

        仅处理 **harbor** 实例且其 ``docker_image`` 确实位于源 ACR（与
        ``build_image_distributions`` 同口径——只有这些镜像会随数据集搬到目标 ACR）。
        对每个这样的实例：本地重写 task.toml → 重打包 content.tgz → 重算 digest →
        重建 {id}.json，直传**目标桶**；随后 publish 用 ``instance_objects="report_only"``，
        workflow 只复制 report.jsonl，content.tgz 与 {id}.json 由本步骤直接写好。

        约束（保证正确性，宁可 fail-fast）：本批必须**全部**是可改写的 harbor 实例；
        若混入 SWE 实例或镜像不在源 ACR 上的实例，抛 SchemaError 说明为何不能整体
        report_only，并给出出路（设 rewrite_task_toml_image=False 接受生产 task.toml
        仍指向源 registry，或拆分批次）。

        重要限制：SDK 直传目标桶发生在 workflow 审批**之前/之外**，等于绕过审批门；
        被拒的上架会在目标桶留下未注册的孤儿对象。这是本能力的已知取舍，见使用指南。
        """
        from pathlib import Path as _Path
        import shutil as _shutil
        from .clients.config import load_profile
        from .validate import detect_format

        dst = load_profile(target or "target", overrides=target_overrides)
        if not dst.oss_bucket:
            raise SchemaError(
                "rewrite_task_toml_image 需要目标 oss_bucket（用 target_overrides 提供），"
                "否则无法把改写后的 content.tgz 直传目标桶")
        src_acr = self.profile.effective_acr_host
        dst_acr = dst.effective_acr_host
        dst_ns = dst.acr_namespace

        # instance_id → 本地目录（仅 harbor 目录；SWE 是 .json 文件，没有 task.toml）
        dir_by_id: dict[str, _Path] = {}
        for d in local_dirs:
            p = _Path(d)
            if detect_format(p) != "swe":
                dir_by_id[self.instances.validate(p).instance_id] = p

        # 落库镜像（权威源引用），与 build_image_distributions 同口径过滤
        recorded = self.versions._recorded_images(
            dataset, version, [r.instance_id for r in pushed], split)

        ineligible: list[str] = []
        plan: list[tuple[str, _Path, str]] = []   # (iid, dir, target_ref)
        for r in pushed:
            iid = r.instance_id
            src_ref = (recorded.get(iid) or r.docker_image or "").strip()
            if iid not in dir_by_id or not src_ref or not src_ref.startswith(src_acr + "/"):
                ineligible.append(iid)
                continue
            plan.append((iid, dir_by_id[iid],
                         P.retarget_image(src_ref, src_acr, dst_acr, dst_ns)))

        if ineligible:
            raise SchemaError(
                "rewrite_task_toml_image=True 需要本批实例全部是「镜像在源 ACR 上的 "
                f"harbor 实例」，但以下实例不满足：{ineligible}（SWE 实例无 task.toml，"
                "复用共享 base 的实例镜像不在源 ACR、不随数据集搬运）。出路：设 "
                "rewrite_task_toml_image=False 接受生产 task.toml 仍指向源 registry，"
                "或把可改写实例单独成批。")

        target_store = OssContentStore(
            self.transport, dst.oss_bucket, bucket_factory=self._bucket_factory)
        lay = self.instances._layout()
        for iid, d, target_ref in plan:
            tgz, digest, meta_json, _ck, _mk = self.instances.retarget_prod_content(
                d, dataset, version, split, target_ref)
            try:
                target_store.put(iid, dataset, version, split, tgz, meta_json,
                                 overwrite=True, layout=lay)
            finally:
                _shutil.rmtree(_Path(tgz).parent, ignore_errors=True)
        return "report_only", [iid for iid, _, _ in plan]

    # ── 用户输入数据（插件 / 数据合成输入）：swe/user-data/users/{uid}/ ─────────
    # users/ 这一层不能省：user-data 域根是 swe/user-data/，其下除 users/ 外还可能有
    # 别的子目录（如共享语料，仅系统白名单可只读）。apiserver 从 users/ 之后取 uid 段，
    # 把工号直接挂在域根下（swe/user-data/{uid}/）会被 94011 拒签。
    USER_DATA_ROOT = "swe/user-data/users/"

    @staticmethod
    def _user_data_prefix(uid: str) -> str:
        return Repo.USER_DATA_ROOT + (uid or "").strip().strip("/") + "/"

    @staticmethod
    def _clean_user_data_subpath(sub: str) -> str:
        """归一并校验用户子路径：去首尾 '/'、显式拒绝任何 '..' 段、禁止空。

        显式拒绝 '..'（而非依赖 normpath 静默消解）：'../x' 多为误用或恶意，
        直接失败比静默改写成 'x' 更可诊断、更安全。
        """
        sub = (sub or "").strip()
        if not sub:
            raise SchemaError("user-data subpath must not be empty")
        if any(seg == ".." for seg in sub.split("/")):
            raise SchemaError(f"invalid user-data subpath {sub!r}: '..' not allowed")
        cleaned = posixpath.normpath("/" + sub.lstrip("/")).lstrip("/")
        if not cleaned or cleaned == ".":
            raise SchemaError(f"invalid user-data subpath {sub!r}")
        return cleaned

    def whoami(self) -> str:
        """返回当前 apikey 对应的工号（user_id），供拼 user-data 前缀。

        工号可能带前导零（如 '0xxxxx'），须逐字符原样用于 prefix，切勿数字归一化。
        """
        resp = self.transport.get("/apis/v1/me/identity")
        uid = (resp or {}).get("user_id", "")
        if not str(uid).strip():
            raise SchemaError("empty user_id in /me/identity response")
        return str(uid)

    # ── 存储配置查询（从 apiserver 拉数据面寻址信息，无任何密钥）──
    def get_repo_config(self, *, cluster: str = "", storage_env: str = "") -> dict:
        """查询某 cluster/env 的数据面存储配置（oss_bucket/oss_prefix/acr_host/acr_namespace）。

        从 apiserver GET /apis/v1/repo-config 拉取，只含寻址信息、**不含 AK/SK/STS**。
        返回的 dict 可直接作为 profile_overrides 传给 Repo(...)，免去手工填桶名/仓库地址。
        cluster 与 storage_env 二选一，cluster 优先（apiserver 先由 cluster 解析出 storage_env）。
        """
        return fetch_repo_config(self.transport, cluster=cluster, storage_env=storage_env)

    def get_cluster_storage_env_map(self) -> dict:
        """查询 cluster → storage_env 的映射表（GET /apis/v1/repo-config/cluster-storage-env-map）。

        用于在不确定某执行集群对应哪个存储环境时先查映射，再用 storage_env 查 get_repo_config。
        """
        resp = self.transport.get("/apis/v1/repo-config/cluster-storage-env-map")
        if not isinstance(resp, dict):
            raise SchemaError("unexpected cluster-storage-env-map response shape")
        return resp

    def get_user_data_config(self, *, cluster: str = "", storage_env: str = "",
                             allow_fallback: bool = False):
        """查询 scope=user-data 的独立配置（schema1：OSS 寻址 + 生产读写能力声明）。

        从 apiserver ``GET /apis/v1/repo-config?…&scope=user-data`` 拉取，无密钥。
        cluster 与显式 storage_env 冲突直接拒绝（不静默换环境）；旧服务不认识
        scope 时仅当 ``allow_fallback=True`` 才走旧 repo-config 兼容（能力字段
        保持未知/关闭）。网络/认证/权限错误不当版本 fallback，原样抛出。

        返回的 :class:`~instance_repo.clients.config.UserDataConfig` 是 user-data
        **独立**上下文：``to_profile_overrides()`` 只含 OSS 寻址，勿并入 Dataset/
        artifact 的 profile（隔离防污染）；Repo 自身 profile 不受影响。
        """
        return fetch_user_data_config(self.transport, cluster=cluster,
                                      storage_env=storage_env,
                                      allow_fallback=allow_fallback)

    # ── F2-R1：user-data 独立数据面上下文（与 Dataset 域 _content 隔离）──

    def _user_data_context(self):
        """返回 user-data 独立数据面上下文（惰性发现 + 缓存 + 单飞）。

        优先级：
        1. 用户显式 ``profile.user_data_bucket``（profile_overrides 显式给
           user-data 寻址）——零网络发现，直接用显式值；
        2. ``get_user_data_config()``（scope=user-data schema1 发现，含
           production_read/write 能力声明）。

        独立性：返回的 OssContentStore 与 Dataset 域 ``_content`` 完全分离
        （独立 bucket、独立 bucket 缓存）；发现结果**不写回** self.profile
        （Dataset 寻址不受影响）。旧服务不认识 scope / 认证失败等异常原样
        抛出——绝不静默借用 Dataset bucket（那会把 user-data 数据写进错误
        的域，且绕过 apiserver 的 user-data 独立生产 gate）。

        production gate（F1 server 契约）：``production_write_enabled=False``
        时写入口（upload*）在客户端即拒绝（早失败）；``production_read_enabled``
        =False 时读入口（download/list）拒绝。注意这只是**声明对齐**：服务端
        每次仍按 RBAC 独立判定，客户端 gate 不构成授权。
        """
        if self._ud_ctx is not None:
            return self._ud_ctx
        with self._ud_ctx_lock:
            if self._ud_ctx is not None:
                return self._ud_ctx
            explicit_bucket = (getattr(self.profile, "user_data_bucket", "")
                               or "").strip()
            explicit_endpoint = (getattr(self.profile, "user_data_endpoint", "")
                                 or "").strip()
            if explicit_bucket:
                cfg = None            # 用户自填：零发现调用
            else:
                # 发现查询键：cluster（profile 已绑定）优先，否则 profile.storage_env；
                # 二者皆空时用 storage_env="dev" 兜底会静默退 dev——禁止。改为
                # cluster 查询（apiserver 从 X-Cluster/Env 头路由）仍需要键，
                # 空键即报清晰错误。
                cluster = (getattr(self.profile, "cluster", "") or "").strip()
                env = (getattr(self.profile, "storage_env", "") or "").strip()
                if not cluster and not env:
                    raise SchemaError(
                        "user-data 配置发现需要 cluster 或 storage_env："
                        "请配置 profile（cluster/storage_env）或显式 "
                        "user_data_bucket")
                # cluster 键优先且**不带** Dataset 域 env（独立环境语义：user-data
                # 环境由 cluster 解析，不受 Dataset profile env 影响；无 cluster
                # 时才用 storage_env 键——此键即用户为 user-data 选择的独立环境）。
                if cluster:
                    cfg = fetch_user_data_config(self.transport, cluster=cluster)
                else:
                    cfg = fetch_user_data_config(
                        self.transport, storage_env=env)
                explicit_bucket = cfg.oss_bucket
            if not explicit_bucket:
                raise SchemaError(
                    "user-data bucket 未配置：用户显式 user_data_bucket 或 "
                    "scope=user-data 发现均未给出 oss_bucket")
            # 显式 endpoint 覆盖：仅当用户显式给出 user_data_endpoint 时，把 STS
            # 签发响应里的 endpoint 替换为自填值（用户已知自己的数据面入口）。
            # 只包装独立 user-data 上下文的 transport，Dataset 域不受影响。
            ud_transport = self.transport
            if explicit_endpoint:
                ud_transport = _EndpointOverrideTransport(
                    self.transport, explicit_endpoint)
            store = OssContentStore(
                ud_transport, explicit_bucket,
                bucket_factory=self._bucket_factory)
            self._ud_ctx = _UserDataContext(cfg, store)
            return self._ud_ctx

    def _ud_is_production(self, ctx) -> bool:
        """user-data 上下文是否为 production 环境（gate 只对 production 生效）。

        判定来源（以树内契约为准）：``UserDataConfig.storage_env`` 为 scope
        发现响应的服务端权威值（P1-① 已核对与显式 env 一致）；用户显式
        ``user_data_bucket``（cfg=None 零发现）时退回 ``self.profile.storage_env``
        （Repo 构造时的数据面环境）。仅 ``storage_env == prod`` 视为
        production——dev/internal-dev/external-dev 等非 prod 环境的
        production_*_enabled 声明不构成 gate（服务端对非 prod scope 也返回
        默认 false，语义上仅是"生产开关"声明，不应阻断开发环境 IO）。
        未知/空 env（无法判定）**fail-closed 视为 production**——不因判定
        不了而放行 gate。
        """
        env = ""
        if ctx.config is not None:
            env = normalize_storage_env(getattr(ctx.config, "storage_env", ""))
        if not env:
            env = normalize_storage_env(getattr(self.profile, "storage_env", ""))
        if not env:
            return True  # 无法判定：fail-closed 按 production 对待
        return env == STORAGE_ENV_PROD

    def _require_ud_write(self, ctx) -> None:
        """写入口的客户端早失败：**production 环境**且发现结果声明 write 关闭即拒绝。

        gate 仅对 production（storage_env=prod）生效；dev 等非 prod 环境不受
        production_*_enabled 声明影响（服务端对非 prod 也返回默认 false）。
        production 语义原样保留——prod 下 write 关闭仍然拒绝。
        """
        if self._ud_is_production(ctx) and ctx.config is not None \
                and not ctx.config.production_write_enabled:
            raise SchemaError(
                "user-data production write is disabled (production_write_enabled=false)")

    def _require_ud_read(self, ctx) -> None:
        """读入口的客户端早失败：**production 环境**且发现结果声明 read 关闭即拒绝。

        同 :meth:`_require_ud_write`：仅 production 环境 gate；非 prod 不放
        生产语义，production gate 不放松。
        """
        if self._ud_is_production(ctx) and ctx.config is not None \
                and not ctx.config.production_read_enabled:
            raise SchemaError(
                "user-data production read is disabled (production_read_enabled=false)")

    def _canonical_inputs(self, uid, relative_path, cluster, *, root=False):
        policy = self._expected_replica_policy
        if policy is None:
            raise UserDataUpgradeRequired("canonical user-data requires trusted replica policy",
                biz_code=94106, data={})
        chosen = cluster if cluster is not None else self._canonical_constructor_cluster
        if chosen is None:
            chosen = self.profile.cluster
        if (not isinstance(chosen, str) or not chosen or any(c.isspace() for c in chosen)
                or any(c in chosen for c in "/\\%?#")):
            raise _facade_schema()
        entries = UserDataEntriesClient(self.transport, expected_replica_policy=policy)
        request = entries._request(uid, relative_path, chosen, False, 1, "")
        if not root and not request["relative_path"]:
            raise _facade_schema()
        key = _derive_users_key(request["owner"], request["relative_path"])
        if len(key.encode("utf-8")) > 1023:
            raise _facade_schema()
        return request, entries

    def _canonical_reader(self):
        return UserDataReadsClient(self.transport,
            expected_replica_policy=self._expected_replica_policy, legacy_profiles=())

    def _canonical_resolution(self, reader, request, budget):
        budget.raise_if_exhausted()
        resolution = _facade_call(reader.resolve, owner=request["owner"],
            relative_path=request["relative_path"], cluster=request["cluster"],
            deadline=budget.remaining_seconds())
        budget.raise_if_exhausted()
        if (type(resolution) is not CanonicalReadResolution or resolution.mode != "canonical"
                or resolution.owner != request["owner"] or resolution.relative_path != request["relative_path"]
                or resolution.cluster != request["cluster"]
                or resolution.storage_id != self._expected_replica_policy.storage_id
                or resolution.canonical_key != _derive_users_key(request["owner"], request["relative_path"])
                or not _valid_anchor(resolution.anchor)):
            raise _facade_schema()
        # Reuse the real SDK's validator; no facade URL parser or trust bootstrap.
        resolution = _facade_call(reader._validate_resolution_model, resolution)
        budget.raise_if_exhausted()
        return resolution

    def _canonical_upload(self, request, local_path, budget, *, overwrite,
                          skip_existing, idempotency_key, source_identity=None, on_existing=None):
        _validate_metadata_callbacks(overwrite, on_existing)
        if type(overwrite) is not bool or type(skip_existing) is not bool or (overwrite and skip_existing):
            raise _facade_schema()
        # Capture regular-file identity before any resolve/Begin, without hashing a skipped source.
        identity = _facade_call(_capture_source_identity, local_path,
                                budget=budget, identity=source_identity)
        budget.raise_if_exhausted()
        if skip_existing or on_existing is not None:
            reader = self._canonical_reader()
            missing = False
            try:
                resolution = self._canonical_resolution(reader, request, budget)
            except UserDataWriteError as error:
                if (type(error.biz_code) is int and error.biz_code == 94109
                        and error.error_code in ("user_data_read_not_found", "user_data_write_not_found")):
                    missing = True
                else:
                    raise
            if not missing:
                observed = ObservedUserDataObject(request["owner"], request["relative_path"],
                    request["cluster"], resolution.storage_id, resolution.canonical_key, resolution.anchor)
                budget.raise_if_exhausted()
                action = "skip" if on_existing is None else _metadata_callback(budget, on_existing, observed)
                if type(action) is not str or action not in ("skip", "overwrite", "error"):
                    raise _UserDataCallbackFailed()
                if action == "skip":
                    return UserDataUploadOutcome("skipped_existing", existing=observed)
                if action == "error":
                    raise UserDataWriteConflict("canonical user-data object already exists",
                        biz_code=94105, data={})
                overwrite = True
        key = idempotency_key if idempotency_key is not None else new_idempotency_key()
        _facade_call(validate_idempotency_key, key)
        digest = _facade_call(_sha256_file, local_path, budget=budget, identity=identity)
        budget.raise_if_exhausted()
        writes = UserDataWritesClient(self.transport, expected_replica_policy=self._expected_replica_policy)
        outcome = _facade_call(writes.begin, owner=request["owner"], relative_path=request["relative_path"],
            sha256=digest, size=identity.size, overwrite=overwrite, idempotency_key=key,
            cluster=request["cluster"], deadline=budget.remaining_seconds(), _bound_idempotency_key=key)
        _facade_call(budget.raise_if_exhausted, _bound_idempotency_key=key)
        if type(outcome) is not BeginOutcome or sum(x is not None for x in (outcome.write, outcome.receipt, outcome.status)) != 1:
            raise _facade_schema()
        if outcome.status is not None:
            if type(outcome.status) is not StatusResult:
                raise _facade_schema()
            op = outcome.status.op_id
            if not isinstance(op, str) or not _OP_ID_RE.fullmatch(op):
                raise _facade_schema()
            raise UserDataWritePending("canonical write requires reconciliation; no full receipt",
                biz_code=94103, data={"op_id": op, "idempotency_key": key})
        receipt = outcome.receipt
        if outcome.write is not None:
            handle = outcome.write
            if (type(handle) is not BeginWriteResult or handle.owner != request["owner"]
                    or handle.relative_path != request["relative_path"] or handle.expected_sha256 != digest
                    or handle.expected_size != identity.size
                    or handle.canonical_key != _derive_users_key(request["owner"], request["relative_path"])):
                raise _facade_schema()
            _facade_call(writes.upload, handle, local_path, _budget=budget,
                _source_identity=identity, op_id=handle.op_id, _bound_idempotency_key=key)
            _facade_call(budget.raise_if_exhausted, op_id=handle.op_id, _bound_idempotency_key=key)
            receipt = _facade_call(writes.commit, handle, deadline=budget.remaining_seconds(),
                op_id=handle.op_id, _bound_idempotency_key=key)
            _facade_call(budget.raise_if_exhausted, op_id=handle.op_id, _bound_idempotency_key=key)
        result = UserDataUploadOutcome("committed", receipt=receipt)
        receipt = result.receipt
        if (receipt.canonical_key != _derive_users_key(request["owner"], request["relative_path"])
                or receipt.storage_id != self._expected_replica_policy.storage_id
                or receipt.sha256 != digest or receipt.size != identity.size
                or any(receipt.final[r]["bucket"] != self._expected_replica_policy.bucket(r) for r in ("cn", "sg"))):
            raise _facade_schema()
        _facade_call(budget.raise_if_exhausted, op_id=receipt.op_id, _bound_idempotency_key=key)
        return result

    def upload_user_data_verified(self, uid, local_path, remote_subpath, *, overwrite=False,
            skip_existing=False, cluster=None, deadline=900.0, idempotency_key=None, on_existing=None):
        """Upload with an optional fresh metadata-only skip/overwrite/error decision."""
        budget = _facade_budget(deadline)
        request, _ = self._canonical_inputs(uid, remote_subpath, cluster)
        return self._canonical_upload(request, local_path, budget,
            overwrite=overwrite, skip_existing=skip_existing, idempotency_key=idempotency_key,
            on_existing=on_existing)

    def upload_user_data(self, uid, local_path, remote_subpath, *, overwrite=False,
                         cluster=None, deadline=900.0, on_existing=None):
        return _public_upload_dict(self.upload_user_data_verified(uid, local_path, remote_subpath,
            overwrite=overwrite, skip_existing=not overwrite, cluster=cluster, deadline=deadline,
            on_existing=on_existing))

    def download_user_data_verified(self, uid, remote_subpath, local_path, *, overwrite=True,
                                    cluster=None, deadline=900.0):
        budget = _facade_budget(deadline)
        request, _ = self._canonical_inputs(uid, remote_subpath, cluster)
        reader = self._canonical_reader()
        resolution = self._canonical_resolution(reader, request, budget)
        result = _facade_call(reader.download, resolution, local_path, overwrite=overwrite,
                              deadline=budget.remaining_seconds())
        budget.raise_if_exhausted()
        if (type(result) is not VerifiedReadResult or result.mode != "canonical"
                or result.canonical_key != resolution.canonical_key or result.anchor != resolution.anchor
                or result.sha256_verified != resolution.anchor.sha256
                or type(result.bytes_written) is not int or result.bytes_written != resolution.anchor.size
                or not isinstance(result.target, Path) or result.target != Path(local_path)):
            raise _facade_schema()
        return result

    def download_user_data(self, uid, remote_subpath, local_path, *, overwrite=True,
                           cluster=None, deadline=900.0):
        return str(self.download_user_data_verified(uid, remote_subpath, local_path,
            overwrite=overwrite, cluster=cluster, deadline=deadline).target)

    def user_data_entries_page(self, uid, subpath="", *, cluster=None, recursive=False,
                               limit=100, cursor="", deadline=30.0):
        budget = _facade_budget(deadline)
        request, entries = self._canonical_inputs(uid, subpath, cluster, root=True)
        request = entries._request(request["owner"], request["relative_path"], request["cluster"], recursive, limit, cursor)
        result = _facade_call(entries._fetch, request, budget)
        budget.raise_if_exhausted()
        return result

    @staticmethod
    def _canonical_pages(entries, request, budget, recursive, page_size, max_rows, max_bytes, max_pages):
        req = entries._request(request["owner"], request["relative_path"], request["cluster"], recursive, page_size, "")
        _entries_bound(max_rows, MAX_ROWS)
        _entries_bound(max_bytes, MAX_BYTES)
        _entries_bound(max_pages, MAX_PAGES)
        return entries._iterate_pages(req, budget, max_rows, max_bytes, max_pages)

    def iter_user_data_entries(self, uid, subpath="", *, cluster=None, recursive=False,
            page_size=200, deadline=60.0, max_rows=MAX_ROWS, max_bytes=MAX_BYTES, max_pages=MAX_PAGES):
        budget = _facade_budget(deadline)
        request, entries = self._canonical_inputs(uid, subpath, cluster, root=True)
        pages = self._canonical_pages(entries, request, budget, recursive, page_size, max_rows, max_bytes, max_pages)
        def iterate():
            while True:
                budget.raise_if_exhausted()
                page = _facade_call(next, pages, None)
                if page is None:
                    return
                for entry in page.entries:
                    budget.raise_if_exhausted()
                    yield entry
                    budget.raise_if_exhausted()
        return iterate()

    def list_user_data(self, uid, subpath="", *, cluster=None, deadline=60.0,
                       max_rows=MAX_ROWS, max_bytes=MAX_BYTES, max_pages=MAX_PAGES):
        budget = _facade_budget(deadline)
        request, entries = self._canonical_inputs(uid, subpath, cluster, root=True)
        pages = self._canonical_pages(entries, request, budget, True, 200, max_rows, max_bytes, max_pages)
        values, exists = [], False
        while True:
            page = _facade_call(next, pages, None)
            budget.raise_if_exhausted()
            if page is None:
                break
            values.extend(page.entries)
            exists = exists or page.directory_exists is True
        if values or exists or not request["relative_path"]:
            result = [entry.key for entry in values if entry.type == "file"]
            budget.raise_if_exhausted()
            return result
        missing = False
        try:
            resolution = self._canonical_resolution(self._canonical_reader(), request, budget)
        except UserDataWriteError as error:
            if (type(error.biz_code) is int and error.biz_code == 94109
                    and error.error_code in ("user_data_read_not_found", "user_data_write_not_found")):
                missing = True
            else:
                raise
        budget.raise_if_exhausted()
        return [] if missing else [resolution.canonical_key]

    def upload_user_data_dir(self, uid, local_dir, remote_subdir, *, overwrite=False,
            cluster=None, deadline=900.0, max_files=10000, max_metadata_bytes=32 * 1024 * 1024,
            on_existing=None, on_completed=None):
        """Sequential batch; completion callbacks receive actual metadata outcomes.

        on_completed(outcome, relative_path, done, total) runs after the outcome
        is recorded. A display error never erases a committed or observed result.
        """
        _validate_metadata_callbacks(overwrite, on_existing, on_completed)
        budget = _facade_budget(deadline)
        request, _ = self._canonical_inputs(uid, remote_subdir, cluster, root=True)
        if (type(overwrite) is not bool or type(max_files) is not int or not 1 <= max_files <= 10000
                or type(max_metadata_bytes) is not int or not 1 <= max_metadata_bytes <= 32 * 1024 * 1024):
            raise _facade_schema()
        plan = _facade_call(self._canonical_directory_plan, local_dir, request, budget, max_files, max_metadata_bytes)
        completed = []
        for path, item_request, identity in plan:
            failure = None
            try:
                outcome = self._canonical_upload(item_request, path, budget, overwrite=overwrite,
                    skip_existing=not overwrite, idempotency_key=None, source_identity=identity,
                    on_existing=on_existing)
            except (UserDataWriteError, TransportError, SchemaError, _UploadError) as error:
                failure = error
            if failure is not None:
                if not completed:
                    raise failure
                raise UserDataDirectoryPartial(completed, item_request["relative_path"], failure)
            completed.append(outcome)
            if on_completed is not None:
                failure = None
                try:
                    _metadata_callback(budget, on_completed, outcome,
                        item_request["relative_path"], len(completed), len(plan))
                except (TransportError, SchemaError) as error:
                    failure = error
                if failure is not None:
                    raise UserDataDirectoryPartial(completed, item_request["relative_path"], failure)
            self._canonical_batch_postcheck(budget, completed, item_request["relative_path"])
        result = [_public_upload_dict(outcome) for outcome in completed]
        self._canonical_batch_postcheck(budget, completed, plan[-1][1]["relative_path"] if plan else "")
        return result

    @staticmethod
    def _canonical_batch_postcheck(budget, completed, relative_path):
        failure = None
        try:
            budget.raise_if_exhausted()
        except RequestDeadlineExceeded as error:
            failure = error
        if failure is not None:
            if completed:
                raise UserDataDirectoryPartial(completed, relative_path, failure)
            raise failure

    def _canonical_directory_plan(self, local_dir, request, budget, max_files, max_bytes):
        base = Path(local_dir)
        stack, plan, total = [], [], 0
        try:
            stack.append((_CanonicalDirectoryScan(base), "", base))
            while stack:
                budget.raise_if_exhausted()
                iterator, parent, directory_path = stack[-1]
                entry = next(iterator, None)
                if entry is None:
                    iterator.close(); stack.pop(); continue
                relative = parent + entry.name
                remote = request["relative_path"] + "/" + relative if request["relative_path"] else relative
                full_path = directory_path / entry.name
                item, _ = self._canonical_inputs(request["owner"], remote, request["cluster"])
                total += len(os.fsencode(full_path)) + len(remote.encode("utf-8")) + 128
                if total > max_bytes:
                    raise UserDataEntriesIncomplete("directory plan bound exceeded")
                if entry.is_symlink():
                    if entry.is_dir(follow_symlinks=True):
                        continue
                elif entry.is_dir(follow_symlinks=False):
                    if len(stack) >= 65:
                        raise _facade_schema()
                    # Relative to the pinned parent, never a pathname check-then-follow.
                    budget.raise_if_exhausted()
                    child = _CanonicalDirectoryScan(entry.name, parent_fd=iterator.fd)
                    stack.append((child, relative + "/", full_path)); continue
                # DirEntry stat is relative to that same pinned directory. A renamed
                # ancestor or retargeted path must not substitute another source inode.
                expected = _SourceIdentity.from_stat(entry.stat(follow_symlinks=True))
                identity = _capture_source_identity(full_path, budget=budget, identity=expected)
                if len(plan) >= max_files:
                    raise UserDataEntriesIncomplete("directory plan bound exceeded")
                plan.append((full_path, item, identity))
            budget.raise_if_exhausted()
            plan.sort(key=lambda value: value[1]["relative_path"])
            return plan
        finally:
            # Attempt every owned close even if one close reports an OS failure.
            for iterator, _, _ in stack:
                try:
                    iterator.close()
                except OSError:
                    pass

    # ── Artifact 下载（AP HTTP 链接，由服务端执行权限校验）──

    def download_artifact(self, job_id: str, cluster: str | None = None,
                          output_dir: str = ".", *,
                          ap_endpoint: str | None = None,
                          include_files: list[str] | None = None,
                          exclude_files: list[str] | None = None,
                          extract: bool = False) -> str:
        """下载单个 job 的 artifact (result.tgz) 到本地。

        鉴权：由 AP artifact 接口执行，SDK 不再查询 Job 详情作预检查。
        并发模型：单 job = 单文件单线程。

        Args:
            job_id: AP job ID
            cluster: 数据面名（默认使用 SDK profile 绑定的 cluster）
            output_dir: 本地输出目录
            ap_endpoint: AP 控制面 URL（可选，默认从环境变量或内置常量取）

        Returns:
            下载文件的本地路径
        """
        from .artifacts import download_artifact as _dl
        cluster = cluster or self.profile.cluster or ""
        return _dl(self.transport, self.transport.token, job_id,
                   cluster, output_dir, ap_endpoint,
                   include_files=include_files, exclude_files=exclude_files, extract=extract)

    def download_artifacts(self, job_ids: list[str],
                           cluster: str | None = None,
                           output_dir: str = ".", *,
                           max_concurrent: int = 8,
                           ap_endpoint: str | None = None,
                           include_files: list[str] | None = None,
                           exclude_files: list[str] | None = None,
                           extract: bool = False,
                           ) -> dict[str, str | Exception]:
        """批量下载多个 job 的 artifact。

        并发粒度是跨 job（不是单文件内多线程）。下载使用 AP 返回的 HTTP 链接。

        Args:
            job_ids: AP job ID 列表
            cluster: 数据面名
            output_dir: 本地输出目录
            max_concurrent: 最大并发下载数（默认 8）
            ap_endpoint: AP 控制面 URL

        Returns:
            {job_id: 本地文件路径 或 Exception}
        """
        from .artifacts import download_artifacts as _dl_many
        cluster = cluster or self.profile.cluster or ""
        return _dl_many(self.transport, self.transport.token, job_ids,
                        cluster, output_dir, max_concurrent, ap_endpoint,
                        include_files=include_files, exclude_files=exclude_files, extract=extract)

    def download_artifacts_from_group(self, group_id: str,
                                      cluster: str | None = None,
                                      output_dir: str = ".", *,
                                      max_concurrent: int = 8,
                                      ap_endpoint: str | None = None,
                                      include_files: list[str] | None = None,
                                      exclude_files: list[str] | None = None,
                                      extract: bool = False,
                                      ) -> dict[str, str | Exception]:
        """下载某个 group 下全部 job 的 artifact。

        先调 AP GET /groups/{group_id}/jobs 分页收集 job_id，再批量下载。

        Args:
            group_id: AP group ID
            cluster: 数据面名
            output_dir: 本地输出目录
            max_concurrent: 最大并发下载数
            ap_endpoint: AP 控制面 URL

        Returns:
            {job_id: 本地文件路径 或 Exception}
        """
        from .artifacts import fetch_group_job_ids, download_artifacts as _dl_many
        cluster = cluster or self.profile.cluster or ""
        job_ids = fetch_group_job_ids(
            self.transport.token, group_id, cluster, ap_endpoint)
        if not job_ids:
            logger.warning("group %s has no jobs", group_id)
            return {}
        return _dl_many(self.transport, self.transport.token, job_ids,
                        cluster, output_dir, max_concurrent, ap_endpoint,
                        include_files=include_files, exclude_files=exclude_files, extract=extract)

    # ── 用户数据 ACL（role-bindings 接口，resource_type=user_data）──
    _USER_DATA_ROLE_MAP = {
        "reader": "built-in:user-data-reader",
        "writer": "built-in:user-data-writer",
        "admin": "built-in:user-data-admin",
    }

    def _user_data_acl_client(self, storage_env=""):
        from .clients.user_data_acl import UserDataACLClient, _UserDataACLControlClient
        if type(storage_env) is not str:
            raise SchemaError("invalid user-data ACL storage environment")
        if storage_env in ("", "prod"):
            return UserDataACLClient(self.transport)
        # Explicit legacy domain remains isolated. Never infer this from the
        # runtime Env header, profile, data discovery, or the Dataset bootstrap.
        return _UserDataACLControlClient(self.transport, storage_env=storage_env)

    def grant_user_data(self, uid: str, principal: str, role: str, *,
                        principal_type: str = "user", subpath: str = "",
                        storage_env: str = "", deadline=30.0) -> None:
        self._user_data_acl_client(storage_env).grant(owner=uid, principal=principal,
            role=role, principal_type=principal_type, subpath=subpath, deadline=deadline)

    def revoke_user_data(self, uid: str, principal: str, role: str = "", *,
                         principal_type: str = "user", subpath: str = "",
                         storage_env: str = "", deadline=30.0) -> None:
        # Full six-query identity; unknown mutation outcomes are not replayed.
        self._user_data_acl_client(storage_env).revoke(owner=uid, principal=principal,
            role="reader" if role == "" else role, principal_type=principal_type,
            subpath=subpath, deadline=deadline)

    def list_user_data_acl(self, uid: str, subpath: str = "",
                           storage_env: str = "", *, deadline=30.0) -> list[dict]:
        """Bounded complete observed traversal (<=1000), not a snapshot."""
        return [binding.to_dict() for binding in self._user_data_acl_client(storage_env).list_all(
            owner=uid, subpath=subpath, deadline=deadline)]

    def my_user_data_permissions(self, uid: str, subpath: str = "",
                                 storage_env: str = "", *, deadline=30.0) -> list[str]:
        """Fresh server actions mapped for display; never a local authority proof."""
        actions = self._user_data_acl_client(storage_env).permissions(owner=uid,
            subpath=subpath, deadline=deadline)
        return (["admin"] if "assign" in actions else ["writer"] if "use" in actions
            else ["reader"] if "get" in actions else [])


class _EndpointOverrideTransport:
    """包装 transport：把 OSS STS 签发响应的 endpoint 替换为显式自填值。

    仅用于 user-data 独立上下文（用户显式 user_data_endpoint 时）——用户已知
    自己的数据面入口，覆盖服务端下发值；其余请求原样透传（repo-config/ACL 等
    不受影响）。只改 GET/POST 透传方法与 get_oss_credentials 返回。
    """

    def __init__(self, transport, endpoint: str) -> None:
        self._t = transport
        self._endpoint = endpoint
        # 缓存键身份兼容：transport 相同即视为同一缓存身份
        self.base_url = getattr(transport, "base_url", "")
        self.env = getattr(transport, "env", "")
        self._custom_send = getattr(transport, "_custom_send", False)

    def get_oss_credentials(self, *args, **kwargs):
        cred = self._t.get_oss_credentials(*args, **kwargs)
        if isinstance(cred, dict):
            cred = dict(cred)
            cred["endpoint"] = self._endpoint
        return cred

    def __getattr__(self, name):
        return getattr(self._t, name)


class _UserDataContext:
    """user-data 独立数据面上下文：配置（可 None=用户显式）+ 独立 content store。"""

    __slots__ = ("config", "store")

    def __init__(self, config, store) -> None:
        self.config = config
        self.store = store
