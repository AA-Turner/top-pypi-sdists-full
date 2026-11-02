"""clients/splits.py — split-first 记录管理（→ apiserver /apis/v1/datasets/splits）。

服务端契约（apiserver master 实测，recordsvc）：
* ``GET /datasets/splits``：dataset_name 必填；version 可选（无 version 时缺省
  version_scope=unversioned——只列无版本 split；跨全部版本须显式 version_scope=all）；
  status 过滤；environment（默认 online）；分页默认 page=1/page_size=50（上限 200）。
* ``GET /datasets/splits/detail``：dataset_name+split 必填、version 可选；裸记录。
* ``POST /datasets/splits``：dataset_name 必填、version 可选；body 为
  ``{"splits": [...]}``，响应兼容 DatasetVersion，需再 GET split 详情确认。
* ``PATCH /datasets/splits/detail``：dataset_split_id 或 dataset_name+split(+version)
  寻址；body 仅 run_type（必填，"train"/"eval"，空串=清除）；environment 与
  POST/GET 保持一致；返回更新后的记录。

设计决策（方案 D1，已评审）：``SplitsClient.list`` 在 version 为空且未显式传
version_scope 时**默认 all**（跨全部版本+无版本 split）。理由：SDK 的 list 语义
历来是"取全量"，服务端缺省 unversioned 只列无版本 split，对调用方是坑
（split_first 有版本布局下 list 出空却以为没有数据）。需要严格对齐服务端缺省
行为的调用方显式传 ``version_scope="unversioned"``。
"""
from __future__ import annotations

from urllib.parse import quote

from ..errors import SchemaError, TransportError, WriteOutcomeUnknown
from ..models import (DatasetSplit, PagedResult, RUN_TYPE_VALUES,
                      SPLIT_STATUS_VALUES)
from ..retry import retry_transient

# 服务端 ListSplits 认可的 version_scope 取值（recordsvc）。
VERSION_SCOPE_VALUES = ("unversioned", "exact", "all")


class SplitsClient:
    _BASE = "/apis/v1/datasets/splits"

    def __init__(self, transport, profile=None, *, content_store=None,
                 oss_prefix: str = "swe/datasets") -> None:
        self._t = transport
        self._p = profile
        self._content = content_store
        self._oss_prefix = oss_prefix

    # ── 读 ──

    def list(self, dataset: str, *, version: str | None = None,
             version_scope: str | None = None, status: str | None = None,
             page: int = 1, page_size: int = 50,
             environment: str | None = None,
             fallback_to_oss: bool = True) -> PagedResult:
        """列出 split 记录（单页，PagedResult）。

        参数:
          dataset        : dataset 名（必填）。
          version        : 可选。给定时按该 version 精确（scope=exact 语义）。
          version_scope  : 可选。``unversioned``/``exact``/``all``。**缺省规则**：
                           version 为空时默认 ``all``（SDK 取全量哲学，见模块
                           docstring）；version 非空时服务端只接受 exact 语义，
                           无需再传。
          status         : 可选，draft/published/deprecated/archived。
          page/page_size : 分页；服务端默认 50，上限 200。
          environment    : 可选，缺省由 profile 派生（pre/online）。
          fallback_to_oss: 可选（默认 True）。MongoDB 无结果时自动回退到 OSS
                           存储层探测（仅当 content_store 已注入时生效）。

        返回 :class:`~instance_repo.models.PagedResult`，items 为
        :class:`~instance_repo.models.DatasetSplit` 列表（当前页）。

        **三级回退优先级**（设计文档 §4.4.3）：
        1. MongoDB 查询 → 有结果直接返回。
        2. 404 异常 → 直接进入 OSS 回退。
        3. 空结果 → Legacy 回退（version_first 内嵌投影）→ 仍为空 → OSS 回退。
        """
        if not (dataset or "").strip():
            raise SchemaError("dataset is required for splits.list")
        scope = (version_scope or "").strip()
        if scope and scope not in VERSION_SCOPE_VALUES:
            raise SchemaError(
                f"invalid version_scope {scope!r}; must be one of "
                f"{', '.join(VERSION_SCOPE_VALUES)}")
        if not scope and not (version or "").strip():
            scope = "all"  # 见模块 docstring：SDK 默认跨全部版本
        if (status or "").strip():
            s = status.strip()
            if s not in SPLIT_STATUS_VALUES:
                raise SchemaError(
                    f"invalid status {s!r}; must be one of "
                    f"{', '.join(SPLIT_STATUS_VALUES)}")
        q = f"dataset_name={quote(dataset, safe='')}"
        if (version or "").strip():
            q += f"&version={quote(version, safe='')}"
        if scope:
            q += f"&version_scope={quote(scope, safe='')}"
        if (status or "").strip():
            q += f"&status={quote(status.strip(), safe='')}"
        q += f"&page={int(page)}&page_size={int(page_size)}"
        env = self._env(environment)
        if env:
            q += f"&environment={quote(env, safe='')}"
        # ── 1. MongoDB 查询 ──
        try:
            data, pagination = self._t.request_with_meta(
                "GET", f"{self._BASE}?{q}")
        except TransportError as e:
            # ── 2. 92001 异常 → 直接进入 OSS 回退 ──
            if (e.biz_code == 92001
                    and fallback_to_oss and self._content is not None
                    and self._discovery_env_match(environment)):
                return self._discover_splits(
                    dataset, version, scope, status, page, page_size)
            raise
        rows = data.get("splits", data) if isinstance(data, dict) else data
        rows = rows if isinstance(rows, list) else []
        items = [DatasetSplit.from_dict(r) for r in rows if isinstance(r, dict)]
        # ── 3. 空结果 → Legacy 回退（version_first 内嵌投影）──
        if not items and not (status or "").strip():
            items = self._legacy_list(dataset, version, self._env(environment))
        # ── 3b. 仍为空 → OSS 回退 ──
        if not items and fallback_to_oss and self._content is not None \
                and self._discovery_env_match(environment):
            return self._discover_splits(
                dataset, version, scope, status, page, page_size)
        return PagedResult.from_response(items, pagination, int(page), int(page_size))

    def get(self, dataset: str, split: str, *, version: str | None = None,
            environment: str | None = None,
            fallback_to_oss: bool = True) -> DatasetSplit | None:
        """取单个 split 记录；不存在返回 None（"没有"不是错误，与 instances.get 一致）。

        只吞 HTTP 404（服务端 split 不存在）；dataset 名拼错等服务端也按 404 报，
        此处不区分（split detail 端点无独立业务码可判——与 instances.get 的
        92003/92001 二分不同，这里统一 None，调用方拿不准时用 datasets.get 核对）。

        **存量数据回退（1.0.10 真机反馈）**：split 记录只存在于 split_first
        新数据（split-first 集合）；存量 version_first 数据的 split 内嵌在
        version 文档 ``splits[]`` 里，split detail 端点 404。此时回退到
        versions.get 的内嵌投影（``projected=True``，无 status/published_at，
        storage_path 取自 oss_prefix）；仍找不到才返回 None。

        **OSS 回退**：当 ``_legacy_get`` 返回 None 后，若 ``fallback_to_oss=True``
        且 ``content_store`` 已注入，尝试从 OSS 目录结构合成 split 记录。
        """
        if not (dataset or "").strip():
            raise SchemaError("dataset is required for splits.get")
        if not (split or "").strip():
            raise SchemaError("split is required for splits.get")
        q = (f"dataset_name={quote(dataset, safe='')}"
             f"&split={quote(split, safe='')}")
        if (version or "").strip():
            q += f"&version={quote(version, safe='')}"
        env = self._env(environment)
        if env:
            q += f"&environment={quote(env, safe='')}"
        try:
            data = self._t.get(f"{self._BASE}/detail?{q}")
        except TransportError as e:
            if e.status == 404:
                result = self._legacy_get(dataset, split, version, env)
                if result is not None:
                    return result
                # Legacy 回退无果 → OSS 回退
                if fallback_to_oss and self._content is not None \
                        and self._discovery_env_match(environment):
                    return self._discover_split(dataset, split, version)
                return None
            raise
        return DatasetSplit.from_dict(data) if isinstance(data, dict) else None

    # ── 存量数据兼容投影（version_first 的 split 内嵌在 version 文档里）──

    def _legacy_get(self, dataset: str, split: str, version: str | None,
                    env: str) -> DatasetSplit | None:
        """split detail 404 后的回退：读 version 内嵌 splits[] 投影。

        有 version 时单查该 version；无 version 时扫描全部 version（分页）
        直到命中。返回 projected=True 的 DatasetSplit；仍无则 None。
        TransportError 按 status 区分：404 重试/继续（version 不存在/实例
        未找到属正常），5xx 与连接错误重抛——不把网络故障伪装成"数据不存在"。
        """
        from .versions import VersionsClient
        vc = VersionsClient(self._t, self._p)
        if (version or "").strip():
            try:
                detail = vc.get(dataset, version, environment=env or None)
            except TransportError as e:
                if e.status == 404:
                    return None   # version 不存在 → 回退无果
                raise
            return _project_embedded_split(detail, split, version, dataset)
        # 无 version：扫描全部 version
        page = 1
        while True:
            try:
                res = vc.list_paged(dataset, page=page, page_size=200,
                                    environment=env or None)
            except TransportError as e:
                if e.status == 404:
                    return None   # dataset 不存在 → 终止扫描
                raise
            for item in res.items:
                try:
                    detail = vc.get(dataset, item.version,
                                    environment=env or None)
                except TransportError as e:
                    if e.status == 404:
                        continue  # 该 version 不存在，继续找下一个
                    raise
                found = _project_embedded_split(detail, split,
                                                item.version, dataset)
                if found is not None:
                    return found
            if not res.has_more or not res.items:
                break
            page += 1
        return None

    def _legacy_list(self, dataset: str, version: str | None, env: str
                     ) -> list[DatasetSplit]:
        """split 集合无记录时的回退：聚合全部 version 的内嵌 splits[] 投影。

        投影项无 status/published_at（内嵌字段集只有 name/run_type/oss_prefix/
        is_default/instance_count 等），因此 status 过滤对存量数据天然为空——
        如实返回空列表而非伪造状态。
        TransportError 按 status 区分：404→跳过/终止；其他重抛。
        """
        from .versions import VersionsClient
        vc = VersionsClient(self._t, self._p)
        out: list[DatasetSplit] = []
        if (version or "").strip():
            try:
                detail = vc.get(dataset, version, environment=env or None)
            except TransportError as e:
                if e.status == 404:
                    return out   # version 不存在，无数据可投影
                raise
            return _project_all_embedded_splits(detail, version, dataset)
        page = 1
        while True:
            try:
                res = vc.list_paged(dataset, page=page, page_size=200,
                                    environment=env or None)
            except TransportError as e:
                if e.status == 404:
                    break         # dataset 不存在，终止扫描
                raise
            for item in res.items:
                try:
                    detail = vc.get(dataset, item.version,
                                    environment=env or None)
                except TransportError as e:
                    if e.status == 404:
                        continue  # 该 version 不存在
                    raise
                out.extend(_project_all_embedded_splits(
                    detail, item.version, dataset))
            if not res.has_more or not res.items:
                break
            page += 1
        return out

    # ── OSS 回退发现（未注册 dataset 的 split 合成） ──

    def _discover_splits(self, dataset: str, version: str | None,
                         version_scope: str | None, status: str | None,
                         page: int, page_size: int) -> PagedResult:
        """OSS 回退的 splits.list — 处理 version_scope 和 status 过滤。

        split_first 模式下 OSS 探测可区分无版本 split（level-1 目录只有 .json）
        和有版本 split（level-1 目录含子目录），因此 ``version_scope`` 生效：

        - ``"unversioned"``: 只返回无版本 split
        - ``"versioned"``: 只返回有版本 split
        - ``"all"`` / None: 返回全部（SDK 默认行为）

        ``version`` 非空时仍精确匹配该 version。
        """
        from ..store.oss_discovery import (
            parse_dataset_level, build_synthetic_split,
            _in_memory_paged, _warn_if_truncated,
        )
        info = parse_dataset_level(
            self._content, dataset, oss_prefix=self._oss_prefix,
            metadata_model=self._discovery_mm())
        _warn_if_truncated(info, dataset, 500)
        splits: list[DatasetSplit] = []
        scope = (version_scope or "all").strip().lower()
        # split_first 无版本布局：dataset 根下直接是 split 目录
        if not version and scope in ("all", "unversioned"):
            for us in info.unversioned_splits:
                splits.append(build_synthetic_split(
                    dataset, "", us.name, instance_count=us.instance_count))
        if scope in ("all", "exact"):
            for v in info.versions:
                if version and v.version != version:
                    continue
                if v.has_default_instances:
                    splits.append(build_synthetic_split(
                        dataset, v.version, "default",
                        instance_count=v.default_instance_count))
                for s in v.splits:
                    splits.append(build_synthetic_split(
                        dataset, v.version, s))
        if (status or "").strip():
            splits = [s for s in splits if s.status == status.strip()]
        return _in_memory_paged(splits, int(page), int(page_size))

    def _discover_split(self, dataset: str, split_name: str,
                        version: str | None) -> DatasetSplit | None:
        """OSS 回退的 splits.get — 精确查找单个 split。"""
        from ..store.oss_discovery import (
            parse_dataset_level, build_synthetic_split, _warn_if_truncated,
        )
        info = parse_dataset_level(
            self._content, dataset, oss_prefix=self._oss_prefix,
            metadata_model=self._discovery_mm())
        _warn_if_truncated(info, dataset, 500)
        if not version:
            for us in info.unversioned_splits:
                if us.name == split_name:
                    return build_synthetic_split(
                        dataset, "", us.name, instance_count=us.instance_count)
        for v in info.versions:
            if version and v.version != version:
                continue
            if split_name == "default" and v.has_default_instances:
                return build_synthetic_split(
                    dataset, v.version, "default",
                    instance_count=v.default_instance_count)
            if split_name in v.splits:
                return build_synthetic_split(
                    dataset, v.version, split_name)
        return None

    def _discovery_mm(self) -> str:
        """OSS 回退探测的布局语义（split_first 默认；version_first 显式切换）。"""
        from ..layout import normalize_metadata_model
        return normalize_metadata_model(
            getattr(self._p, "metadata_model", None)
            if self._p is not None else None)

    def _discovery_env_match(self, environment: str | None) -> bool:
        """OSS 回退环境兼容性检查。

        请求的 ``environment`` 必须与 profile 的 storage_env 派生环境一致，
        否则 OSS 回退返回空——因为 bucket 是按 storage_env 绑定的，dev 桶里
        的数据不应作为 online 结果返回（反之亦然）。

        ``environment`` 为空时视为兼容（跟随 profile 默认环境）。
        """
        req = (environment or "").strip()
        if not req:
            return True
        if self._p is None:
            return True
        from .config import dataset_environment_for
        derived = dataset_environment_for(
            getattr(self._p, "storage_env", ""))
        if not derived:
            return True  # 无法派生时不做限制
        return req == derived

    # ── 写 ──

    def _post_create(self, dataset: str, split: str, version: str,
                     environment: str) -> None:
        """创建 split；POST 非幂等，响应是 DatasetVersion 兼容体，故不解析。"""
        q = f"dataset_name={quote(dataset, safe='')}"
        if version:
            q += f"&version={quote(version, safe='')}"
        if environment:
            q += f"&environment={quote(environment, safe='')}"
        self._t.post(f"{self._BASE}?{q}", {"splits": [split]},
                     idempotent=False)

    def create(self, dataset: str, split: str, *,
               version: str | None = None, run_type: str | None = None,
               storage_path: str | None = None,
               environment: str | None = None) -> DatasetSplit:
        """经独立 split API 创建记录并从详情端点权威读回。

        ``version`` 可选；空值表示 unversioned split。``storage_path`` 仅为 1.2.1
        源码兼容保留，独立端点不接受它，因此非空值会在网络调用前拒绝。
        POST 响应是 DatasetVersion 兼容体，不能当 DatasetSplit 解析；可选 run_type
        PATCH 完成后始终 GET 详情，并对创建后的短暂不可见做三次有界重试。
        """
        dataset_name = (dataset or "").strip()
        split_name = (split or "").strip()
        version_name = (version or "").strip()
        if not dataset_name:
            raise SchemaError("dataset is required for splits.create")
        if not split_name:
            raise SchemaError("split is required for splits.create")
        if (storage_path or "").strip():
            raise SchemaError(
                "storage_path is deprecated for splits.create: split creation now "
                "uses an independent endpoint that does not accept storage paths")
        rt = (run_type or "").strip()
        if rt and rt not in RUN_TYPE_VALUES:
            raise SchemaError(
                f"invalid run_type {rt!r}; must be one of "
                f"{', '.join(RUN_TYPE_VALUES)} or None")
        env = self._env(environment)

        try:
            self._post_create(dataset_name, split_name, version_name, env)
        except Exception as exc:
            raise TransportError(
                f"split create POST failed before creation was confirmed: {exc}",
                status=getattr(exc, "status", None),
                biz_code=getattr(exc, "biz_code", None)) from exc

        coordinates = _create_coordinates(
            dataset_name, version_name, split_name, env)
        if rt:
            try:
                self._update_with_environment(
                    dataset_name, split_name, version=version_name,
                    run_type=rt, status="", dataset_split_id=None,
                    environment=env)
            except Exception as exc:
                raise TransportError(
                    "split was created but run_type update failed; "
                    f"the split create is NOT rolled back; {coordinates}: {exc}",
                    status=getattr(exc, "status", None),
                    biz_code=getattr(exc, "biz_code", None)) from exc

        def readback() -> DatasetSplit:
            found = self._read_detail_once(
                dataset_name, split_name, version_name, env)
            if found is None or found.name != split_name:
                # A successful create can be briefly invisible to the detail read.
                # Mark only this post-write condition transient; retry_transient keeps
                # deterministic 4xx/schema failures single-shot.
                raise TransportError(
                    "created split is not yet visible in authoritative readback",
                    status=503)
            return found

        try:
            return retry_transient(readback, attempts=3)
        except Exception as exc:
            raise WriteOutcomeUnknown(
                "split create succeeded but authoritative readback could not be "
                f"confirmed; {coordinates}: {exc}",
                cause=exc) from exc

    def _read_detail_once(self, dataset: str, split: str, version: str,
                          environment: str) -> DatasetSplit | None:
        """Read only split detail once; never retry or project legacy version data."""
        q = (f"dataset_name={quote(dataset, safe='')}"
             f"&split={quote(split, safe='')}")
        if version:
            q += f"&version={quote(version, safe='')}"
        if environment:
            q += f"&environment={quote(environment, safe='')}"
        try:
            data = self._t._request_once("GET", f"{self._BASE}/detail?{q}")
        except TransportError as exc:
            if exc.status == 404:
                return None
            raise
        return DatasetSplit.from_dict(data) if isinstance(data, dict) and data else None

    def update(self, dataset: str, split: str | None = None, *,
               version: str | None = None, run_type: str = "",
               status: str = "",
               dataset_split_id: str | None = None,
               environment: str | None = None) -> DatasetSplit:
        """更新 split 记录（``PATCH /datasets/splits/detail``）。

        ``run_type``（**必填**："train"/"eval"，空串=清除）——服务端已支持。

        ``status``（可选）：split 生命周期状态（"draft"/"published"/"deprecated"/
        "archived"，空串=不变）。**SDK 侧先就绪**：参数随 PATCH body 下发，
        apiserver UpdateSplit handler 尚未接受 status 字段时会静默忽略；待
        apiserver 补 handler 后自动生效。客户端侧做枚举校验，非法值前置拒绝。
        典型用法：锁定 split（``status="published"``）后 push(overwrite=True)
        会被 instances 侧前置检查拒绝，解锁用 ``status="draft"``。

        ``environment`` 语义与 :meth:`get`/:meth:`list` 对齐：显式参数优先，
        缺省由 profile 派生。任何非空有效环境均拼入 query，使独立 create 的
        POST、可选 run_type PATCH 与权威 GET 始终访问同一集合；为空时沿用
        服务端默认环境。

        寻址二选一：``dataset_split_id``（优先，split-first 精确记录 id）或
        ``dataset``+``split``（+可选 ``version``）name 三元组。
        """
        return self._update_with_environment(
            dataset, split, version=version, run_type=run_type, status=status,
            dataset_split_id=dataset_split_id,
            environment=self._env(environment))

    def _update_with_environment(self, dataset: str, split: str | None, *,
                                 version: str | None, run_type: str, status: str,
                                 dataset_split_id: str | None,
                                 environment: str) -> DatasetSplit:
        """PATCH using an already-resolved environment, including frozen empty."""
        if dataset_split_id:
            q = f"dataset_split_id={quote(dataset_split_id, safe='')}"
        else:
            if not (dataset or "").strip() or not (split or "").strip():
                raise SchemaError(
                    "splits.update requires dataset_split_id, or dataset + split")
            q = (f"dataset_name={quote(dataset, safe='')}"
                 f"&split={quote(split, safe='')}")
            if (version or "").strip():
                q += f"&version={quote(version, safe='')}"
        if environment:
            q += f"&environment={quote(environment, safe='')}"
        rt = run_type or ""
        if rt and rt not in RUN_TYPE_VALUES:   # 空串=清除，合法
            raise SchemaError(
                f"invalid run_type {rt!r}; must be one of "
                f"{', '.join(RUN_TYPE_VALUES)} (empty string to clear)")
        st = status or ""
        if st and st not in SPLIT_STATUS_VALUES:
            raise SchemaError(
                f"invalid status {st!r}; must be one of "
                f"{', '.join(SPLIT_STATUS_VALUES)} (empty string to leave unchanged)")
        body: dict = {"run_type": rt}
        if st:
            body["status"] = st
        data = self._t.patch(f"{self._BASE}/detail?{q}", body)
        return DatasetSplit.from_dict(data) if isinstance(data, dict) else DatasetSplit()

    # ── 内部 ──

    def _env(self, environment: str | None) -> str:
        env = (environment or "").strip()
        if not env and self._p is not None:
            env = (getattr(self._p, "dataset_environment", "") or "").strip()
        return env


def _create_coordinates(dataset: str, version: str, split: str,
                        environment: str) -> str:
    """Stable recovery coordinates for post-write partial-completion errors."""
    return (f"dataset={dataset}, version={version or '<unversioned>'}, "
            f"split={split}, environment={environment or '<server-default>'}")


def normalize_split_version_scope(version: str | None,
                                  version_scope: str | None) -> str:
    """纯函数：供 conformance 跨语言比对 scope 缺省规则（version 空 → all）。"""
    scope = (version_scope or "").strip()
    if scope:
        if scope not in VERSION_SCOPE_VALUES:
            raise SchemaError(
                f"invalid version_scope {scope!r}; must be one of "
                f"{', '.join(VERSION_SCOPE_VALUES)}")
        return scope
    return "all" if not (version or "").strip() else "exact"


# ── 存量数据内嵌 splits[] 投影 ────────────────────────────────────────────────

def _embedded_splits_of(detail) -> list:
    """取 version 详情的内嵌 splits[]（兼容 dict 与 DatasetVersion 对象）。"""
    if detail is None:
        return []
    if isinstance(detail, dict):
        return detail.get("splits") or []
    return getattr(detail, "splits", None) or []


def _project_embedded_split(detail, split: str, version: str,
                            dataset: str) -> "DatasetSplit | None":
    """从 versions/detail 响应投影单个 split（projected=True）。

    内嵌字段集：{name, run_type?, oss_prefix, is_default, instance_count?,
    file_count?, size_bytes?}——无 status/published_at/storage_path。
    """
    for sp in _embedded_splits_of(detail):
        if not isinstance(sp, dict) or sp.get("name") != split:
            continue
        return _build_projected_split(sp, version, dataset)
    return None


def _project_all_embedded_splits(detail, version: str,
                                 dataset: str) -> list["DatasetSplit"]:
    """从 versions/detail 响应投影全部内嵌 split（projected=True）。"""
    return [_build_projected_split(sp, version, dataset)
            for sp in _embedded_splits_of(detail) if isinstance(sp, dict)]


def _build_projected_split(sp: dict, version: str,
                           dataset: str) -> "DatasetSplit":
    from ..models import SplitManifest
    manifest = SplitManifest(
        instance_count=sp.get("instance_count"),
        file_count=sp.get("file_count"),
        size_bytes=sp.get("size_bytes"))
    return DatasetSplit(
        dataset=dataset,
        dataset_id="",
        dataset_version_id=None,        # 内嵌投影拿不到 version 记录 id
        version=version,
        name=sp.get("name", ""),
        run_type=sp.get("run_type"),
        status="",                      # 内嵌无 status
        storage_path=sp.get("oss_prefix", ""),
        manifest=manifest,
        projected=True)
