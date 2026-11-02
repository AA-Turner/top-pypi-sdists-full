"""clients/versions.py — DatasetVersion 操作 + publish（→ apiserver benchmark-release）。"""
from __future__ import annotations

import time
import uuid
import warnings
from urllib.parse import quote

from ..models import (DatasetVersion, IngestReport, RUN_TYPE_VALUES,
                      STORAGE_TYPE_VALUES, VERSION_STATUS_VALUES)
from .. import paths as P
from .. import release as R
from ..errors import SchemaError, JobFailed, TransportError
from ..layout import Layout, MODEL_SPLIT_FIRST
from .config import (
    business_metadata_model, dataset_environment_for, fetch_repo_config,
    load_profile, normalize_storage_env,
)

_TERMINAL_OK = {"succeeded"}
_TERMINAL_BAD = {"failed", "canceled", "cancelled"}
_INGEST_OK = {"completed"}
_INGEST_BAD = {"failed", "canceled", "cancelled"}


def _job_error(job: dict) -> str:
    """从作业/工作流 dict 里尽力抽取失败原因文本（用于 JobFailed 消息）。"""
    if not isinstance(job, dict):
        return ""
    for k in ("error", "error_message", "message", "reason", "detail",
              "failure_reason", "status_message"):
        v = job.get(k)
        if v:
            return str(v)
    return str(job.get("status", ""))


def _ingest_job_id(job: dict | None) -> str:
    if not isinstance(job, dict):
        return ""
    value = job.get("ingest_id") or job.get("id")
    return value.strip() if isinstance(value, str) else ""


def _check_run_type(rt: str) -> None:
    if rt not in RUN_TYPE_VALUES:
        raise SchemaError(
            f"invalid run_type '{rt}'; valid values: {', '.join(RUN_TYPE_VALUES)}")


def _normalize_split_run_types(split_run_types) -> list[dict]:
    """把 split 级 run_type 打标归一成 apiserver 期望的 [{name, run_type}] 列表。

    入参可为 dict（``{"test": "eval"}``）或 [{"name","run_type"}] 列表；两种都校验
    每项 run_type 合法（train/eval）并要求 name 非空，避免打出无意义的空标签。
    """
    out: list[dict] = []
    if isinstance(split_run_types, dict):
        items = split_run_types.items()
    else:
        items = [((d.get("name") if isinstance(d, dict) else None),
                  (d.get("run_type") if isinstance(d, dict) else None))
                 for d in (split_run_types or [])]
    for name, rt in items:
        if not name:
            raise SchemaError("split_run_types entry requires a non-empty 'name'")
        if not rt:
            raise SchemaError(
                f"split_run_types['{name}'] requires 'run_type'")
        _check_run_type(rt)
        out.append({"name": name, "run_type": rt})
    return out


class VersionsClient:
    _BASE = "/apis/v1/datasets/versions"
    _WORKFLOWS = "/apis/v1/workflows"

    def __init__(self, transport, profile=None, *,
                 content_store=None,
                 oss_prefix: str = "swe/datasets") -> None:
        self._t = transport
        self._p = profile
        self._content = content_store
        self._oss_prefix = oss_prefix

    def _version_extra_q(self, environment: str | None = None,
                         metadata_model: str | None = None) -> str:
        """读/改路径对称下发 ``environment`` 与 ``metadata_model``。

        与 ``store/registry.py:_q`` 同一根因：写路径（ingest）由 storage_env 派生
        environment（dev→pre）写入 pre 集合；versions 的 list/status/update 等
        若不显式下发这两个字段，apiserver 缺省 ``online`` + ``version_first``，
        导致 dev 环境下找不到版本或查到错误模型。

        显式入参优先于 profile 派生（get/list_paged 的覆盖场景，如发布后查
        ``environment="online"``）。
        """
        requested_model = metadata_model
        if requested_model is None and self._p is not None:
            requested_model = self._p.metadata_model if self._p else None
        mm = business_metadata_model(requested_model)
        env = (environment or "").strip()
        if not env and self._p is not None:
            env = (getattr(self._p, "dataset_environment", "") or "").strip()
        parts: list[str] = []
        if mm:
            parts.append(f"metadata_model={quote(mm, safe='')}")
        if env:
            parts.append(f"environment={quote(env, safe='')}")
        return ("&" + "&".join(parts)) if parts else ""

    def _layout(self, metadata_model: str | None = None,
                oss_prefix: str | None = None) -> Layout:
        """Build the split-first layout used by normal business operations."""
        requested_model = metadata_model
        if requested_model is None and self._p is not None:
            requested_model = self._p.metadata_model
        model = business_metadata_model(requested_model)
        prefix = oss_prefix or getattr(self._p, "oss_prefix", None) \
            or P.DEFAULT_PREFIX
        return Layout(model, prefix=prefix)

    def _ingest_selectors(self, cluster: str | None
                          ) -> tuple[str, str, str, str]:
        """返回同源的 ``(cluster, storage_env, oss_bucket, oss_prefix)`` 绑定。

        必要时按 cluster 重新解析 repo-config。**bucket/prefix 与 selector 同源**：
        方法级 cluster 覆盖时用**同一次**响应里的 oss 块生成 storage_path，避免发出
        「cluster/storage_env 指向 A 数据面、storage_path 指向 B 桶」的错配请求；
        响应缺 bucket/prefix 时与 Go/Java 一样在 POST 前 fail-fast，不静默回退到
        共享 profile 的 OSS 路径。cluster 为空时沿用 profile 自身寻址。
        返回的 cluster 是 repo-config 响应回传的**规范 Name**（id/url_cluster 会被
        resolve_cluster 解析掉），ingest body 用它下发，服务端按 Name 精确匹配。
        """
        profile_cluster = (getattr(self._p, "cluster", "") or "").strip()
        method_cluster = (cluster or "").strip()
        effective_cluster = method_cluster or profile_cluster
        profile_storage_env = normalize_storage_env(
            getattr(self._p, "storage_env", ""))
        profile_bucket = getattr(self._p, "oss_bucket", "") or ""
        profile_prefix = getattr(self._p, "oss_prefix", "") or P.DEFAULT_PREFIX

        if not effective_cluster:
            return "", profile_storage_env, profile_bucket, profile_prefix

        bound_cluster = (
            getattr(self._p, "storage_env_cluster", "") or "").strip()
        # 已有同 cluster 的绑定证明且非方法级覆盖 → 直接复用，不再查询（对齐
        # Go/Java：方法级 cluster 显式给出时始终重新解析，保证 selector 同源）。
        if not method_cluster and profile_storage_env \
                and bound_cluster == effective_cluster:
            return (effective_cluster, profile_storage_env,
                    profile_bucket, profile_prefix)

        found = fetch_repo_config(self._t, cluster=effective_cluster)
        # fetch_repo_config 已把 cluster 入参（可能是 id/url_cluster）解析为规范 Name 并
        # 回传；ingest body 与 profile 绑定证明都用这个值，服务端按 Name 精确匹配。
        # 报错文案也统一用规范 Name（与 Go/Java 的 binding.cluster 一致）。
        resolved_cluster = (found.get("cluster") or effective_cluster).strip()
        resolved_storage_env = normalize_storage_env(found.get("storage_env"))
        if not resolved_storage_env:
            raise SchemaError(
                f"cluster={resolved_cluster!r} 的 repo-config 响应缺少非空 "
                "storage_env；已中止 ingest，避免发送未绑定的双 selector")

        storage_source = (getattr(self._p, "sources", {}) or {}).get(
            "storage_env")
        if profile_storage_env and storage_source != "discovery" \
                and profile_storage_env != resolved_storage_env:
            raise SchemaError(
                f"cluster={resolved_cluster!r} 与显式 profile storage_env="
                f"{profile_storage_env!r} 冲突：服务端解析为 "
                f"{resolved_storage_env!r}")

        bound_bucket = found.get("oss_bucket") or ""
        bound_prefix = found.get("oss_prefix") or ""
        if not bound_bucket or not bound_prefix:
            missing = "oss_bucket" if not bound_bucket else "oss_prefix"
            raise SchemaError(
                f"cluster={resolved_cluster!r} 的 repo-config 响应缺少非空 "
                f"{missing}；已中止 ingest，避免回退到其他数据面的 OSS 路径")

        # 只有解析的是 profile 自身 cluster 时才回填绑定；方法级覆盖不能篡改 profile
        # 原 selector，后续不带覆盖参数的 ingest 仍应使用原 profile cluster。
        if self._p is not None and effective_cluster == profile_cluster:
            if not profile_storage_env or storage_source == "discovery":
                self._p.storage_env = resolved_storage_env
                self._p.sources["storage_env"] = "discovery"
            self._p.storage_env_cluster = resolved_cluster

        return (resolved_cluster, resolved_storage_env,
                bound_bucket, bound_prefix)

    def _recorded_images(self, dataset: str, version: str,
                         instances: list[str],
                         split: str = "default") -> dict[str, str]:
        """查实例元数据里已落库的 ``docker_image``（上架时作为源镜像的权威值）。

        best-effort：查询失败（无该端点/无权限/网络问题）时返回空 dict，让
        ``build_image_distributions`` 回落到命名规则——保持与旧行为一致，不因为查询
        失败而中断上架。
        """
        try:
            from ..store.registry import ApiMetadataRegistry  # 局部导入避免循环依赖
            # 读路径对称下发 environment 与 metadata_model（见 store/registry.py）。
            reg = ApiMetadataRegistry(
                self._t,
                environment=(self._p.dataset_environment if self._p else ""),
                metadata_model=business_metadata_model(
                    self._p.metadata_model if self._p else None))
            # 必须带 split：省略会跨 split 匹配，而下面是 last-wins 覆盖——同 id 在别的
            # split 也存在时会取错那一份 docker_image（上架源镜像/跳过清单都会跟着错）。
            rows = reg.query(dataset, version, split)
        except Exception:
            return {}
        want = set(instances)
        out: dict[str, str] = {}
        for r in rows or []:
            iid = getattr(r, "instance_id", None)
            img = (getattr(r, "docker_image", None) or "").strip()
            if iid in want and img:
                out[iid] = img
        return out

    def list(self, dataset: str, *, environment: str | None = None,
             metadata_model: str | None = None,
             fallback_to_oss: bool = True) -> list[DatasetVersion]:
        try:
            extra = self._version_extra_q(environment, metadata_model)
            data = self._t.get(
                f"{self._BASE}?dataset_name={quote(dataset, safe='')}{extra}")
            rows = data.get("versions", data) if isinstance(data, dict) else data
            return [DatasetVersion(**_pick(r)) for r in (rows or [])]
        except TransportError as e:
            if (e.biz_code == 92001 and fallback_to_oss
                    and self._content is not None
                    and self._discovery_env_match(environment)):
                return self._discover_versions(dataset, metadata_model=metadata_model)
            raise

    def list_paged(self, dataset: str, *, status: str | None = None,
                   environment: str | None = None,
                   metadata_model: str | None = None,
                   page: int = 1, page_size: int = 20,
                   fallback_to_oss: bool = True) -> "PagedResult":
        """版本分页列表（单页，``GET /datasets/versions``）。

        服务端参数集仅 status + environment/metadata_model + 分页（**无 q 模糊
        搜索**——找数据集用 datasets.list_paged(q=)，两段式检索）。

        ``fallback_to_oss``: dataset 未注册（92001）时自动回退到 OSS 目录探测
        （与 :meth:`list` 一致），在内存中按 status 过滤 + 分页。
        """
        from ..models import PagedResult
        if not (dataset or "").strip():
            raise SchemaError("dataset is required for versions.list_paged")
        q = f"dataset_name={quote(dataset, safe='')}"
        if (status or "").strip():
            s = status.strip()
            if s not in VERSION_STATUS_VALUES:
                raise SchemaError(
                    f"invalid status '{s}'; valid values: "
                    f"{', '.join(VERSION_STATUS_VALUES)}")
            q += f"&status={quote(s, safe='')}"
        q += (f"&page={int(page)}&page_size={int(page_size)}"
              f"{self._version_extra_q(environment, metadata_model)}")
        try:
            data, pagination = self._t.request_with_meta("GET", f"{self._BASE}?{q}")
        except TransportError as e:
            if (e.biz_code == 92001 and fallback_to_oss
                    and self._content is not None
                    and self._discovery_env_match(environment)):
                return self._discover_versions_paged(
                    dataset, status, int(page), int(page_size),
                    metadata_model=metadata_model)
            raise
        rows = data.get("versions", data) if isinstance(data, dict) else data
        rows = rows if isinstance(rows, list) else []
        items = [DatasetVersion(**_pick(r)) for r in rows if isinstance(r, dict)]
        return PagedResult.from_response(items, pagination, int(page), int(page_size))

    def get(self, dataset: str, version: str, *,
            environment: str | None = None,
            metadata_model: str | None = None,
            fallback_to_oss: bool = True) -> DatasetVersion:
        """取版本完整详情（``GET /datasets/versions/detail``）。

        相比 :meth:`status` 只取状态：返回完整 DatasetVersion——含 ``splits``
        列表（每个 split 的 name/run_type/oss_prefix/is_default/instance_count/
        file_count/size_bytes，**无 per-split status/published_at/storage_path**，
        这些要走 ``repo.splits``）。split_first 分支时服务端聚合 legacy 投影。
        """
        if not (dataset or "").strip():
            raise SchemaError("dataset is required for versions.get")
        if not (version or "").strip():
            raise SchemaError("version is required for versions.get")
        try:
            q = (f"dataset_name={quote(dataset, safe='')}"
                 f"&version={quote(version, safe='')}"
                 f"{self._version_extra_q(environment, metadata_model)}")
            data = self._t.get(f"{self._BASE}/detail?{q}")
            return DatasetVersion.from_dict_full(data) if isinstance(data, dict) else DatasetVersion(version=version, dataset=dataset)
        except TransportError as e:
            if (e.biz_code == 92001 and fallback_to_oss
                    and self._content is not None
                    and self._discovery_env_match(environment)):
                return self._discover_version(dataset, version,
                                              metadata_model=metadata_model)
            raise

    def status(self, dataset: str, version: str, *,
               environment: str | None = None,
               metadata_model: str | None = None) -> str:
        extra = self._version_extra_q(environment, metadata_model)
        data = self._t.get(
            f"{self._BASE}/detail?dataset_name={quote(dataset, safe='')}"
            f"&version={quote(version, safe='')}{extra}")
        return data.get("status", "")

    # GET /apis/v1/datasets/splits/detail：split-first 叶详情（真实 split 记录）。
    _SPLITS = "/apis/v1/datasets/splits"

    def split_detail(self, dataset: str, version: str, split: str, *,
                     environment: str | None = None) -> dict:
        """split 级读 API（``GET /apis/v1/datasets/splits/detail``）。

        直接读 split-first 记录：``status``/``published_at``/``storage_path``
        都是真实值，不经过 version_first 兼容投影。版本级读接口
        （:meth:`list`/:meth:`status`）只保证 version_first 语义；要看
        split_first 的发布状态与目标路径请用本方法。

        ``environment`` 缺省由 profile 派生（与读路径对称）；显式传入可覆盖，
        例如发布后查 ``environment="online"`` 的 published 状态与目标路径。
        """
        if not (split or "").strip():
            raise SchemaError("split is required for split detail")
        mm = business_metadata_model(
            self._p.metadata_model if self._p is not None else None)
        env = (environment or "").strip()
        if not env and self._p is not None:
            env = (getattr(self._p, "dataset_environment", "") or "").strip()
        query = (f"dataset_name={quote(dataset, safe='')}"
                 f"&version={quote(version or '', safe='')}"
                 f"&split={quote(split, safe='')}"
                 f"&metadata_model={quote(mm, safe='')}")
        if env:
            query += f"&environment={quote(env, safe='')}"
        data = self._t.get(f"{self._SPLITS}/detail?{query}")
        return data if isinstance(data, dict) else {}

    def create(self, dataset: str, version: str, *,
               storage_path: str | None = None,
               splits: list[str] | None = None, status: str = "draft",
               storage_type: str = "oss",
               environment: str | None = None,
               metadata_model: str | None = None) -> DatasetVersion:
        """显式创建 DatasetVersion（``POST /apis/v1/datasets/versions``）。

        通常 version 由 ``ingest`` 扫描 OSS 时自动建；本方法用于需要**先建空版本壳**
        （例如先建再 PATCH run_type、或先建再单独 ingest）的场景。

        参数:
          storage_path : 可选。缺省时按 profile 自动计算
            （``oss://{bucket}/{prefix}/{L1}/{L2}/{version}/``，与 ingest 同源）。
            显式传入时原样下发（特殊桶/自定义布局场景覆盖）。
          splits       : 可选 split 名列表；缺省由 apiserver 按 storage_path 推导。
          status       : 版本状态，缺省 ``draft``（合法值见 VERSION_STATUS_VALUES）。
          storage_type : 存储类型，缺省 ``oss``（当前仅支持）。
          environment  : 可选。显式传入时原样下发；缺省时由 storage_env 派生
            （dev/internal-dev/external-dev→pre，prod→online）。profile 未显式配置
            storage_env 但配置了 cluster 时，会经 repo-config 解析出绑定的
            storage_env 再派生（与 ingest 对称）；显式 environment 与派生值冲突时
            前置拒绝。
          metadata_model: 源码兼容参数；只接受 None、空串或 ``split_first``，
            正常业务 I/O 不再允许 ``version_first``。

        run_type 不在建版本时设置（apiserver create 不收该字段）：建好后用
        ``set_run_type`` / ``update`` 打标，或走 ``ingest(run_type=...)``。
        """
        requested_model = metadata_model
        if requested_model is None and self._p is not None:
            requested_model = self._p.metadata_model if self._p else None
        mm = business_metadata_model(requested_model)
        if not version:
            raise SchemaError("version is required")
        # 与 ingest 对称（问题1 彻底修复）：storage_env 未在 profile 里显式配置时，
        # 经 repo-config 解析出与 cluster 绑定的 storage_env 再派生 environment；
        # 同时复用**同一次**响应里的 bucket/prefix 计算 storage_path，避免出现
        # 「create 落 online、push/ingest 落 pre」的读写环境撕裂。
        selected_storage_env = ""
        bound_bucket = bound_prefix = ""
        if self._p is not None:
            _, selected_storage_env, bound_bucket, bound_prefix = \
                self._ingest_selectors(None)
        env = (environment or "").strip()
        if not env and self._p is not None:
            env = (getattr(self._p, "dataset_environment", "") or "").strip()
        derived_env = dataset_environment_for(selected_storage_env)
        if env and derived_env and env != derived_env:
            raise SchemaError(
                f"environment={env!r} 与 storage_env="
                f"{selected_storage_env!r} 派生出的 {derived_env!r} 冲突："
                f"请只提供其中一个，或把 storage_env 改成与目标环境一致的值")
        if not env:
            env = derived_env
        if storage_path is None and self._p is not None:
            bucket = (getattr(self._p, "oss_bucket", "") or "") or bound_bucket
            if bucket:
                storage_path = self._layout(
                    oss_prefix=bound_prefix or None).ingest_storage_path(
                    bucket, dataset, version)
        if not storage_path or not storage_path.startswith("oss://"):
            raise SchemaError(
                f"storage_path must be an oss:// URL, got {storage_path!r}; "
                f"未显式提供且 profile 无 oss_bucket 时无法自动计算，"
                f"请配置 INSTANCE_REPO_STORAGE_ENV 或用 profile_overrides 提供")
        if status not in VERSION_STATUS_VALUES:
            raise SchemaError(
                f"invalid status '{status}'; valid values: "
                f"{', '.join(VERSION_STATUS_VALUES)}")
        if storage_type not in STORAGE_TYPE_VALUES:
            raise SchemaError(
                f"invalid storage_type '{storage_type}'; valid values: "
                f"{', '.join(STORAGE_TYPE_VALUES)}")
        body: dict = {"version": version, "storage_path": storage_path,
                      "storage_type": storage_type, "status": status}
        if splits:
            body["splits"] = splits
        # environment 必须放 query（apiserver createVersionRequest 无该字段，
        # 只从 datasetEnvironmentFromQuery 读）；放 body 会被静默丢弃导致
        # 版本落到默认 online 而 list/get/update 走 profile 派生的 pre。
        # metadata_model 已在任何 repo-config/HTTP 前固定为 split_first。
        q = f"dataset_name={quote(dataset, safe='')}"
        if env:
            q += f"&environment={quote(env, safe='')}"
        q += f"&metadata_model={quote(mm, safe='')}"
        data = self._t.post(f"{self._BASE}?{q}", body)
        return DatasetVersion(**_pick(data))

    def update(self, dataset: str, version: str, *, status: str | None = None,
               splits: list[str] | None = None, run_type: str | None = None,
               split_run_types=None,
               manifest: dict | None = None,
               environment: str | None = None,
               metadata_model: str | None = None) -> None:
        """通用版本更新（``PATCH /apis/v1/datasets/versions/detail``）。

        只发送非 None 字段。apiserver 侧 ``run_type`` / ``split_run_types`` / ``splits``
        三者**两两互斥**（version 级 run_type 与 split 级、与全量 splits 替换语义冲突），
        这里本地先拦，避免白跑一次 400。

        参数:
          status          : 版本状态流转（单向 draft→published→deprecated→archived，
                            回退由服务端 400）。
          splits          : 全量替换 split 名列表。
          run_type        : version 级用途标签（train/eval），仅适用于无 logical split 的版本。
          split_run_types : split 级打标，dict（``{"test":"eval"}``）或 [{name,run_type}]。
          manifest        : 版本 manifest 整体替换（``{instance_count, file_count,
                            size_bytes, validation_status, validation_message}``
                            子集均可）——服务端支持但此前 SDK 未暴露（1.0.10 补）。
          environment     : 显式 environment 覆盖 profile 派生值（如发布后操作 online）。
          metadata_model  : 显式 metadata_model 覆盖 profile 派生值。
        """
        norm_srt = _normalize_split_run_types(split_run_types) if split_run_types else None
        # 三选一互斥（对齐 apiserver：run_type / split_run_types / splits 两两互斥）。
        supplied = [k for k, v in (("run_type", run_type),
                                   ("split_run_types", norm_srt),
                                   ("splits", splits)) if v]
        if len(supplied) > 1:
            raise SchemaError(
                f"run_type / split_run_types / splits are mutually exclusive; "
                f"got {', '.join(supplied)}")
        if run_type is not None:
            _check_run_type(run_type)
        if status is not None and status not in VERSION_STATUS_VALUES:
            raise SchemaError(
                f"invalid status '{status}'; valid values: "
                f"{', '.join(VERSION_STATUS_VALUES)}")
        body: dict = {}
        if status is not None:
            body["status"] = status
        if splits is not None:
            body["splits"] = splits
        if run_type is not None:
            body["run_type"] = run_type
        if norm_srt is not None:
            body["split_run_types"] = norm_srt
        if manifest is not None:
            body["manifest"] = manifest
        if not body:
            raise SchemaError("update requires at least one field to change")
        self._patch_detail(dataset, version, body,
                           environment=environment, metadata_model=metadata_model)

    def set_run_type(self, dataset: str, version: str, *,
                     run_type: str | None = None, split_run_types=None,
                     environment: str | None = None,
                     metadata_model: str | None = None) -> None:
        """便捷入口：仅给 version/split 打 run_type 标签（train/eval）。

        version 级与 split 级二选一：传 ``run_type`` 打整个版本（无 logical split 的版本），
        或传 ``split_run_types`` 逐 split 打标。二者不能同时传（互斥）。
        """
        if not run_type and not split_run_types:
            raise SchemaError(
                "set_run_type requires run_type or split_run_types")
        self.update(dataset, version, run_type=run_type,
                    split_run_types=split_run_types,
                    environment=environment, metadata_model=metadata_model)

    def deprecate(self, dataset: str, version: str, *,
                  environment: str | None = None,
                  metadata_model: str | None = None) -> None:
        """把版本置为 deprecated（``update(status="deprecated")`` 的薄封装）。"""
        self.update(dataset, version, status="deprecated",
                    environment=environment, metadata_model=metadata_model)

    def _patch_detail(self, dataset: str, version: str, body: dict, *,
                      environment: str | None = None,
                      metadata_model: str | None = None) -> None:
        extra = self._version_extra_q(environment, metadata_model)
        self._t.patch(
            f"{self._BASE}/detail?dataset_name={quote(dataset, safe='')}"
            f"&version={quote(version, safe='')}{extra}",
            body)

    # ── ingest（临时元数据写入路径）───────────────────────────────────────────
    # apiserver 暂未实现 instance register/commit 端点；作为过渡，先用 STS 把
    # content.tgz + {id}.json 传到 OSS（instances.push(register=False)），再调
    # POST /apis/v1/dataset-ingests：apiserver 扫描 OSS 目录、自动建 series/version、
    # 从对象派生 instance 元数据并批量 upsert（异步，轮询 ingest_id 到终态）。
    _INGESTS = "/apis/v1/dataset-ingests"

    @staticmethod
    def _normalize_instance_ids(instance_ids) -> list[str]:
        if isinstance(instance_ids, (str, bytes)):
            raise SchemaError("instance_ids must be a collection of strings")
        try:
            raw = list(instance_ids)
        except TypeError as exc:
            raise SchemaError(
                "instance_ids must be a collection of strings") from exc
        if not raw:
            raise SchemaError("instance_ids must contain 1..100 IDs")
        normalized: list[str] = []
        for value in raw:
            if not isinstance(value, str):
                raise SchemaError("instance_ids must contain only strings")
            iid = value.strip()
            if not iid:
                raise SchemaError("instance_ids must not contain empty IDs")
            from ..validate import validate_instance_id
            validate_instance_id(iid, source="instance_ids")
            normalized.append(iid)
        selected = sorted(set(normalized))
        if len(selected) > 100:
            raise SchemaError("instance_ids must contain 1..100 unique IDs")
        return selected

    def _post_ingest(self, path: str, body: dict, *,
                     idempotency_key: str | None = None) -> dict:
        """POST once with the operation-scoped idempotency header.

        Transport adapters must implement ``post(..., headers=...)``. Silently
        dropping the header would make a non-retryable write look protected when
        it is not.
        """
        headers = ({"Idempotency-Key": idempotency_key}
                   if idempotency_key else None)
        return self._t.post(path, body, headers=headers)

    def ingest(self, dataset: str, version: str | None = None, *,
               storage_path: str | None = None, splits: list[str] | None = None,
               split: str | None = None,
               instance_ids=None,
               metadata_model: str | None = None,
               environment: str | None = None,
               allow_layout_inference: bool = False,
               publish: bool = False, dry_run: bool = False,
               wait: bool = True, poll_sec: float = 5.0,
               timeout_sec: float = 1800.0, raise_on_failure: bool = True,
               run_type: str | None = None, split_run_types=None,
               cluster: str | None = None,
               sleep=time.sleep) -> dict | IngestReport:
        """发起 dataset-ingest 并（默认）轮询到终态；返回 job 或所选实例报告。

        正常业务入口固定 ``split_first``（split 必填、version 选填）并显式下发模型；
        ``metadata_model`` 兼容参数只接受 None、空串或 ``split_first``，VF在任何I/O前拒绝。

        **环境选择**：方法参数 ``cluster`` 优先于 profile cluster；没有方法参数时沿用 profile
        cluster。cluster 仅用于经 repo-config 解析同源 ``storage_env`` 与存储路径，绝不进入
        dataset-ingest 请求体（严格服务端不接受该字段）。显式 ``environment`` 与派生值冲突时
        前置拒绝。

        ``storage_path`` 缺省由 SDK 计算：无 version 取 dataset 根，有 version 取
        dataset 根加版本目录。**不要指向 ``{split}/`` 子目录**——服务端会解析出零个 split
        并以 92005 失败（真机锤实）。显式传入的 ``storage_path`` 原样下发，由调用方自负。

        **split_first 且 version 为空时必须提供 ``splits``（或 ``split``）**，否则抛
        ``SchemaError``。原因是服务端靠相对深度推断布局：深度 2 视作无版本、深度 3 视作
        有版本，两者共存即报 92005 歧义。而 dataset 根下天然存在两类深度 3 的对象——质检
        报告 ``{split}-report/{id}/report.jsonl``（``-report`` 不属于服务端识别的资产目录
        后缀，会被当成"有版本"的证据）以及存量的版本目录——都会污染推断。显式给出 splits
        时服务端只列举 ``{split}/`` 与 ``{split}-assets/`` 两个前缀，推断被完全绕过。
        确需让服务端推断时传 ``allow_layout_inference=True``。

        dry_run=True 仅预览不落库、不轮询；wait=False 立即返回已建 job。
        publish=True 时 ingest 完成后把 version 置 published。
        raise_on_failure=True（默认）时，轮询到 failed/canceled 终态即抛 JobFailed
        （避免"调用返回正常、实际 ingest 失败"的静默成功）；置 False 则返回失败终态 job。

        run_type / split_run_types（可选）：ingest 会先创建 version+split，故在 ingest
        **到达 completed 后**自动 PATCH 打用途标签（train/eval）。因打标依赖 version 已建
        且 ingest 已成功，与 ``dry_run=True`` / ``wait=False`` **冲突**（此时无从确认版本已就绪、
        会静默丢标），传了即抛 SchemaError。若 ingest 成功但打标 PATCH 失败，抛 TransportError
        且**不回滚 ingest**（ingest 已成功，打标是补充动作），消息提示可稍后 set_run_type 重试。
        """
        requested_model = metadata_model
        if requested_model is None and self._p is not None:
            requested_model = self._p.metadata_model
        model = business_metadata_model(requested_model)
        selected_ids = (self._normalize_instance_ids(instance_ids)
                        if instance_ids is not None else None)
        if selected_ids is not None:
            if publish:
                raise SchemaError(
                    "incremental instance ingest cannot publish the whole split")
            if allow_layout_inference:
                raise SchemaError(
                    "incremental instance ingest cannot use layout inference")
            if dry_run:
                raise SchemaError(
                    "incremental instance ingest cannot use dry_run; "
                    "registration must write metadata")
        ver = (version or "").strip()
        # 逐项 strip 后丢空：纯空白项若原样发出，服务端会以
        # "ingest resolved an empty split name" / 92005 拒绝——不如在这里就当它不存在，
        # 让"必须提供 splits"的前置检查如实生效。
        want_splits = [s.strip() for s in (splits or []) if str(s).strip()]
        if split and split.strip():
            if want_splits:
                raise SchemaError("split 与 splits 互斥（对齐服务端校验）")
            want_splits = [split.strip()]

        if selected_ids is not None and len(want_splits) != 1:
            raise SchemaError(
                "incremental instance ingest requires exactly one split")

        norm_srt = (_normalize_split_run_types(split_run_types)
                    if split_run_types else None)
        tag_run_type = run_type is not None
        tag_split = norm_srt is not None
        if selected_ids is not None and (tag_run_type or tag_split):
            raise SchemaError(
                "incremental instance ingest does not support run_type tagging; "
                "complete registration first, then call versions.set_run_type()")
        if tag_run_type:
            _check_run_type(run_type)
        if tag_run_type and tag_split:
            raise SchemaError(
                "run_type and split_run_types are mutually exclusive")
        if (tag_run_type or tag_split) and (dry_run or not wait):
            raise SchemaError(
                "run_type/split_run_types tagging needs the version created and "
                "ingest completed; it is incompatible with dry_run=True or wait=False")
        if (tag_run_type or tag_split) and not ver:
            raise SchemaError("run_type tagging requires an explicit version")

        if not ver and not want_splits and not allow_layout_inference:
            raise SchemaError(
                "metadata_model=split_first 且未指定 version 时必须提供 splits："
                "服务端按对象相对深度推断布局，dataset 根下的质检报告目录 "
                "'{split}-report/{id}/report.jsonl' 与存量版本目录都会被当成"
                "「有版本」的证据，与真实的无版本实例共存即报 92005 ambiguous。"
                "两条出路：① 传 splits=['<你的 split>']（推荐，服务端只列 "
                "'{split}/' 与 '{split}-assets/'，完全绕过推断）；"
                "② 确需服务端推断时传 allow_layout_inference=True。")

        selected_cluster, selected_storage_env, bound_bucket, bound_prefix = \
            self._ingest_selectors(cluster)
        derived_env = dataset_environment_for(selected_storage_env)
        env = (environment or "").strip()
        if env and derived_env and env != derived_env:
            raise SchemaError(
                f"environment={env!r} 与 storage_env="
                f"{selected_storage_env!r} 派生出的 {derived_env!r} 冲突："
                f"请只提供其中一个，或把 storage_env 改成与目标环境一致的值")
        env = env or derived_env

        if storage_path is None and self._p is not None:
            # storage_path 用**绑定**的 bucket/prefix（与 selector 同源）：方法级
            # cluster 覆盖时指向重新解析出的数据面，而不是共享 profile 的旧 bucket。
            storage_path = self._layout(
                model, oss_prefix=bound_prefix).ingest_storage_path(
                bound_bucket, dataset, ver)

        body: dict = {"dataset": dataset, "metadata_model": model}
        if ver:
            body["version"] = ver
        if storage_path:
            body["storage_path"] = storage_path
        if want_splits:
            body["splits"] = want_splits
        if env:
            body["environment"] = env
        if selected_storage_env:
            body["storage_env"] = selected_storage_env
        # selected_cluster is only a repo-config selector. The strict ingest
        # request schema does not accept a cluster field for either mode.
        if selected_ids is not None:
            body["instance_ids"] = selected_ids
        if publish:
            body["publish_after_validation"] = True
        if dry_run:
            body["dry_run"] = True

        operation_key = str(uuid.uuid4())
        job = self._post_ingest(
            self._INGESTS, body, idempotency_key=operation_key)
        if dry_run:
            return job
        ingest_id = _ingest_job_id(job)
        if not ingest_id:
            raise TransportError(
                "dataset-ingest response missing ingest_id/id", report=job)
        if not wait:
            return (IngestReport.from_job(job, selected_ids)
                    if selected_ids is not None else job)
        deadline = time.monotonic() + timeout_sec
        last = job
        while time.monotonic() < deadline:
            last = self._t.get(f"{self._INGESTS}/{ingest_id}")
            polled_id = _ingest_job_id(last)
            if not polled_id:
                raise TransportError(
                    "dataset-ingest poll response missing ingest_id/id",
                    report=last)
            if polled_id != ingest_id:
                raise TransportError(
                    "dataset-ingest poll response ingest_id mismatch: "
                    f"expected {ingest_id!r}, got {polled_id!r}",
                    report=last)
            st = (last.get("status") or "").lower()
            if st in _INGEST_OK:
                completed_report = IngestReport.from_job(last, selected_ids)
                try:
                    self._tag_after_ingest(dataset, ver, run_type, norm_srt)
                except TransportError as exc:
                    exc.report = completed_report
                    raise
                return completed_report if selected_ids is not None else last
            if st in _INGEST_BAD:
                report = (IngestReport.from_job(last, selected_ids)
                          if selected_ids is not None else None)
                if raise_on_failure:
                    raise JobFailed(
                        f"dataset-ingest {ingest_id} {st}: {_job_error(last)}",
                        status=st, job=last, report=report)
                return report if report is not None else last
            sleep(poll_sec)
        report = (IngestReport.from_job(last, selected_ids)
                  if selected_ids is not None else None)
        raise JobFailed(
            f"dataset-ingest {ingest_id} timeout after {timeout_sec}s; "
            f"last status={(last.get('status') or 'unknown')}",
            status="timeout", job=last, report=report)

    def cancel_ingest(self, ingest_id: str, *, instance_ids=None) -> IngestReport:
        """Cancel an ingest job; cancellation does not prove a DB rollback."""
        iid = (ingest_id or "").strip()
        if not iid:
            raise SchemaError("ingest_id is required")
        selected = (self._normalize_instance_ids(instance_ids)
                    if instance_ids is not None else [])
        job = self._post_ingest(
            f"{self._INGESTS}/{iid}/cancel", {},
            idempotency_key=str(uuid.uuid4()))
        response_id = _ingest_job_id(job)
        if not response_id:
            raise TransportError(
                "dataset-ingest cancel response missing ingest_id/id", report=job)
        if response_id != iid:
            raise TransportError(
                "dataset-ingest cancel response ingest_id mismatch: "
                f"expected {iid!r}, got {response_id!r}", report=job)
        report = IngestReport.from_job(job, selected)
        report.commit_unknown = True
        if selected and not report.unknown:
            report.unknown = list(selected)
            report.completed = []
            report.pending = []
            report.failed = []
        return report

    def _tag_after_ingest(self, dataset: str, version, run_type, norm_srt) -> None:
        """ingest completed 后打 run_type 标签；失败抛 TransportError，不回滚 ingest。"""
        if run_type is None and norm_srt is None:
            return
        if not version:
            # 无 version 无从 PATCH（dataset 级 ingest 不该带 run_type，前置已基本挡住）。
            raise SchemaError(
                "run_type tagging requires an explicit version")
        try:
            self.update(dataset, version, run_type=run_type,
                        split_run_types=norm_srt)
        except JobFailed:
            raise
        except Exception as e:
            raise TransportError(
                f"ingest succeeded but run_type tagging failed: {e}; "
                f"the ingest is NOT rolled back — retry with "
                f"versions.set_run_type('{dataset}', '{version}', ...)",
                status=getattr(e, "status", None),
                biz_code=getattr(e, "biz_code", None), cause=e)

    def publish_with_report(self, dataset: str, version: str, *,
                            instances: list[str] | None = None,
                            images: str = "off", **kw) -> tuple[dict, list[dict]]:
        """同 :meth:`publish`，但**额外返回被跳过的镜像清单**。

        上架只分发确实位于源 ACR 的镜像；落库 ``docker_image`` 指向别的 registry
        （公共/共享 base 或另一运行时地址）的实例会被 ``build_image_distributions``
        直接跳过。跳过本身是对的（见其文档），但**不能静默**——否则调用方以为"镜像也
        一起上架了"。这里把跳过项显式返回：``[{"instance_id","image","reason"}, …]``。

        为什么能在不改 release 的前提下推导：命名规则回落值恒以 ``src_acr/`` 开头、
        永远不会被跳过，故**只有落库值**可能被跳过，比对一遍 recorded 即可。

        .. deprecated:: 同 :meth:`publish`，版本级发布正在废弃。
        """
        warnings.warn(
            "versions.publish_with_report() is deprecated: version-level publishing "
            "is being phased out. For split-first datasets, use "
            "versions.ingest(..., publish=True) or splits.update(status='published') "
            "instead. This method will be removed in a future release.",
            DeprecationWarning, stacklevel=2)
        skipped: list[dict] = []
        # 只在 typed 路径下推导（request_body 逃生舱会忽略 instances/images，报跳过是误导）。
        typed = kw.get("request_body") is None
        if typed and images == "on" and instances and self._p is not None:
            # **只查一次**并把快照下传给 publish：两次独立 best-effort 查询可能不一致，
            # 导致"报了跳过实际却分发了"或更糟的"该报却报空"（正是本能力要消灭的静默）。
            recorded = self._recorded_images(dataset, version, instances,
                                             kw.get("split", "default"))
            kw["recorded_images"] = recorded
            for iid, img in sorted(recorded.items()):
                if img and not img.startswith(self._p.effective_acr_host + "/"):
                    skipped.append({
                        "instance_id": iid, "image": img,
                        "reason": f"not on source ACR {self._p.effective_acr_host}; "
                                  f"base/共享镜像不随数据集上架搬运",
                    })
        wf = self.publish(dataset, version, instances=instances, images=images, **kw)
        return wf, skipped

    def publish(self, dataset: str, version: str = "", *,
                instances: list[str] | None = None,
                target: str = "",
                target_overrides: dict | None = None,
                granularity: str = "dataset",
                images: str = "off",
                overwrite: bool = False,
                approval_mode: str = "internal",
                backend: str = "acr",
                description: str = "",
                request_body: dict | None = None,
                split: str = "",
                metadata_model: str | None = None,
                instance_objects: str = "all",
                recorded_images: dict[str, str] | None = None,
                wait_approval: bool = False, raise_on_failure: bool = True,
                poll_sec: float = 5.0, timeout_sec: float = 1800.0,
                sleep=time.sleep) -> dict:
        """提交 benchmark-release workflow（运行时源地址→目标地址）并轮询到终态。

        .. deprecated::
            版本级发布正在废弃。split-first 数据集请使用
            ``versions.ingest(..., publish=True)`` 或
            ``splits.update(status='published')`` 管理 split 生命周期。
            此方法暂不阻断执行，后续版本将移除。

        按元数据模型选择发布协议（v1.0.5 起）：

        * **split_first 且给了 split**（granularity≠instance）：走 apiserver master 的
          ``dataset_distributions`` 发布协议。split 必填、version 可选——无 version 即
          无版本 split 发布，有 version 即版本化 split 发布；目标路径由服务端从 online
          Dataset base 派生，发布成功后服务端只 ingest 该 split 并置 published。
        * **其余情况**（version_first / 未给 split / granularity=instance）：保留旧
          ``oss_distributions`` 纯前缀拷贝语义，行为与 v0.8~v1.0.4 一致。

        默认按业务意图构造请求体（SDK 内部拼 workflow body，隐藏 distributions/幂等 key/
        registry host 改写）。源 OSS/ACR 地址来自当前 Repo 的运行时环境或构造参数；目标
        OSS/ACR 地址必须通过 ``target_overrides`` 显式提供。若地址来自 repo-config，调用方
        须用明确的 cluster 或 storage_env 查询，并分别把查询结果传给源 Repo 的
        ``profile_overrides`` 或本方法的 ``target_overrides``。``target`` 只是标签，不选择
        环境，也没有隐式目标地址。``request_body`` 为直接透传自定义 workflow body 的逃生舱。

        参数:
          dataset         : {L1}/{L2}
          version         : 版本号。dataset_distributions 协议下可选（split_first 无版本
                            split 发布）；旧协议下必填
          instances       : KEEP 实例 id；granularity='instance' 或 images='on' 时必填
          target          : 目标标签；只用于标识，不解析或选择数据面地址
          target_overrides: 目标 oss_bucket/acr_host/acr_namespace 等运行时地址
          granularity     : 旧协议专用（'dataset' 整前缀一条 | 'instance' 逐实例枚举）；
                            dataset_distributions 协议恒为整 split 目录
          images          : 'off'(仅 OSS) | 'on'(按实例枚举 ACR 镜像分发，可与
                            dataset_distributions 同单下发)
          split           : **必须与 push 时一致**；split_first 协议下必填
          approval_mode   : 'internal' 时 workflow 停在 awaiting_approval;wait_approval=False
                            即在该状态返回(交人工审批),True 则继续等到 succeeded/failed
        """
        requested_model = metadata_model
        if requested_model is None and self._p is not None:
            requested_model = self._p.metadata_model
        model = business_metadata_model(requested_model)
        warnings.warn(
            "versions.publish() is deprecated: version-level publishing is being "
            "phased out. For split-first datasets, use versions.ingest(..., publish=True) "
            "or splits.update(status='published') instead. "
            "This method will be removed in a future release.",
            DeprecationWarning, stacklevel=2)
        if request_body is None:
            if self._p is None:
                raise SchemaError("typed publish 需要源 profile（用 Repo().versions，"
                                  "或改用 request_body 逃生舱）")
            use_dataset_protocol = (model == MODEL_SPLIT_FIRST
                                    and bool(split.strip())
                                    and granularity != "instance")
            dst = load_profile(target or "target", overrides=target_overrides)
            lay = self._layout(model)
            dataset_dists: list[dict] = []
            oss_dists: list[dict] = []
            if use_dataset_protocol:
                if not dst.oss_bucket:
                    raise SchemaError(
                        "publish 需要目标 oss_bucket；SDK 不内置任何环境的桶地址，请通过 "
                        "target_overrides={'oss_bucket': ..., 'acr_host': ...} 提供（见文档）")
                dataset_dists = R.build_dataset_distributions(
                    dataset, split=split, version=version,
                    metadata_model=model,
                    src_bucket=self._p.oss_bucket,
                    overwrite=overwrite, layout=lay)
            else:
                if not version:
                    raise SchemaError(
                        f"version is required when metadata_model={model!r} "
                        f"且未指定 split；split_first 的 split 发布请显式传 split")
                if not dst.oss_bucket:
                    raise SchemaError(
                        "publish 需要目标 oss_bucket；SDK 不内置任何环境的桶地址，请通过 "
                        "target_overrides={'oss_bucket': ..., 'acr_host': ...} 提供（见文档）")
                oss_dists = R.build_oss_distributions(
                    dataset, version, instances or [],
                    src_bucket=self._p.oss_bucket, dst_bucket=dst.oss_bucket,
                    granularity=granularity, overwrite=overwrite, split=split,
                    instance_objects=instance_objects, layout=lay)
            image_dists: list[dict] = []
            if images == "on":
                if not instances:
                    raise SchemaError("images='on' 需要 instances 列表（镜像按实例枚举）")
                image_dists = R.build_image_distributions(
                    dataset, version, instances,
                    src_acr=self._p.effective_acr_host, src_namespace=self._p.acr_namespace,
                    dst_acr=dst.effective_acr_host,
                    # 目标命名空间：v0.8 之前解析了 --target-acr-namespace 却只换 host，
                    # 该参数从未生效；这里真正把它传下去。为空则保留源命名空间（旧行为）。
                    dst_namespace=dst.acr_namespace,
                    recorded_images=(recorded_images if recorded_images is not None
                                     else self._recorded_images(
                                         dataset, version, instances, split)),
                    layout=lay, split=split)
            elif images != "off":
                raise SchemaError(f"unknown images {images!r} (use 'off'|'on')")
            scope = ("split" if dataset_dists
                     else "dataset" if granularity == "dataset"
                     else f"n{len(instances or [])}")
            idem = R.make_idempotency_key(dataset, version, scope,
                                          oss_dists, image_dists, dataset_dists)
            request_body = R.build_release_request(
                idempotency_key=idem,
                description=description or f"release {dataset}/{version} ({scope})",
                oss_dists=oss_dists, image_dists=image_dists,
                dataset_dists=dataset_dists,
                approval_mode=approval_mode, backend=backend)

        wf = self._t.post(self._WORKFLOWS, request_body)
        wid = wf.get("id", "")
        deadline = time.monotonic() + timeout_sec
        last = wf
        while time.monotonic() < deadline:
            last = self._t.get(f"{self._WORKFLOWS}/{wid}")
            st = (last.get("status") or "").lower()
            if st in _TERMINAL_OK:
                return last
            if st in _TERMINAL_BAD:
                if raise_on_failure:
                    raise JobFailed(
                        f"benchmark-release {wid} {st}: {_job_error(last)}",
                        status=st, job=last)
                return last
            if st == R.AWAITING_APPROVAL and not wait_approval:
                return last   # 停在人工审批，交由 ops-BPMS 审批后自动继续
            sleep(poll_sec)
        return last

    # ── OSS fallback discovery (private) ─────────────────────────────────

    def _discover_versions(self, dataset: str,
                           metadata_model: str | None = None) -> list:
        from ..store.oss_discovery import (
            parse_dataset_level, build_synthetic_version, _warn_if_truncated)
        info = parse_dataset_level(
            self._content, dataset, oss_prefix=self._oss_prefix,
            metadata_model=metadata_model or self._discovery_mm())
        _warn_if_truncated(info, dataset, 500)
        # split_first 无版本布局（只有 split）也是发现成功，只是没有版本可列
        if not info.versions and not info.unversioned_splits:
            from ..errors import DatasetNotFound
            raise DatasetNotFound(f"dataset {dataset!r} not found in OSS")
        return [build_synthetic_version(dataset, v) for v in info.versions]

    def _discover_versions_paged(self, dataset: str, status: str | None,
                                 page: int, page_size: int,
                                 metadata_model: str | None = None):
        """OSS 回退的 list_paged：全量探测后按 status 过滤 + 内存分页。"""
        from ..store.oss_discovery import _in_memory_paged
        items = self._discover_versions(dataset, metadata_model=metadata_model)
        if (status or "").strip():
            items = [v for v in items if v.status == status.strip()]
        return _in_memory_paged(items, int(page), int(page_size))

    def _discover_version(self, dataset: str, version: str,
                          metadata_model: str | None = None):
        from ..store.oss_discovery import (
            parse_dataset_level, build_synthetic_version, _warn_if_truncated)
        info = parse_dataset_level(
            self._content, dataset, oss_prefix=self._oss_prefix,
            metadata_model=metadata_model or self._discovery_mm())
        _warn_if_truncated(info, dataset, 500)
        for v in info.versions:
            if v.version == version:
                return build_synthetic_version(dataset, v)
        from ..errors import DatasetNotFound
        raise DatasetNotFound(
            f"version {version!r} not found in OSS for dataset {dataset!r}")

    def _discovery_mm(self) -> str:
        """OSS 回退探测的布局语义（split_first 默认；version_first 显式切换）。"""
        from ..layout import normalize_metadata_model
        return normalize_metadata_model(
            getattr(self._p, "metadata_model", None)
            if self._p is not None else None)

    def _discovery_env_match(self, environment: str | None) -> bool:
        """OSS 回退环境兼容性检查：请求的 environment 须与 profile storage_env 派生环境一致。"""
        req = (environment or "").strip()
        if not req:
            return True
        if self._p is None:
            return True
        from .config import dataset_environment_for
        derived = dataset_environment_for(
            getattr(self._p, "storage_env", ""))
        if not derived:
            return True
        return req == derived


# 与 apiserver `DatasetVersionListItem`（pkg/server/dataset_service.go:315）对齐:
# 列表项带 instance_count/split_count/updated_at/last_ingested_at,详情接口才带
# splits/manifest/run_type/created_by/published_at —— 两者都收进模型。
_FIELDS = ("version", "dataset", "status", "dataset_version_id",

           "storage_path", "published_at",
           "instance_count", "split_count", "last_ingested_at", "updated_at")



def _pick(d: dict) -> dict:
    out = {k: d[k] for k in _FIELDS if k in d}
    out.setdefault("version", d.get("version", ""))
    out.setdefault("dataset", d.get("dataset", ""))
    out.setdefault("status", d.get("status", "draft"))
    # 列表项**不带** storage_type，「缺省即 oss」的模型默认值会让调用方以为服务端
    # 返回了它（CLI 原样透出服务端响应，凭空多字段就是契约变更）。这里显式给 None。
    out.setdefault("storage_type", d.get("storage_type"))
    return out
