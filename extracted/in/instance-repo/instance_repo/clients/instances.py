"""clients/instances.py — Instance 元数据 + 数据面（核心，写元数据先行）。

push 两种格式自动检测：目录→harbor（validate+pack+ACR+OSS），.json→swe（validate+upload json）。
harbor 两阶段：① 本地 validate + 打包 + owner_reference 校验 → ② 写元数据(pending)
拿 id → 取 STS 推 ACR/传 OSS → :commit(ready)。pull 取 STS + digest 校验。
"""
from __future__ import annotations

import hashlib
import json
import logging
import tempfile
from types import SimpleNamespace as NS
from pathlib import Path

from .. import paths as P
from ..concurrency import ItemError, map_concurrent, map_with_executor
from ..content import pack
from ..errors import DigestMismatch, ImageMissing, SchemaError, TransportError
from ..image import dockerfile_from, rewrite_dockerfile
from ..layout import Layout
from ..models import (
    DatasetInstance, Feedback, IngestReport, ManifestEntry, OwnerReference,
    PushManyReport, PushResult, RegistrationReport, InstanceDeleteResult,
    normalize_tag_values, _validate_tag_key, _normalize_tag_array,
)
from ..validate import (check_layout, check_swe_json, check_custom,
                        detect_format, validate_instance_id,
                        CUSTOM_SCHEMA_VERSION)
from .config import business_metadata_model, dataset_environment_for

logger = logging.getLogger(__name__)


def _registry_overrides(environment: str | None,
                        metadata_model: str | None,
                        profile_model: str | None = None, *,
                        allow_version_first: bool = False) -> dict:
    """Build explicit split-first registry parameters before any registry I/O."""
    overrides: dict = {
        "metadata_model": business_metadata_model(
            metadata_model if metadata_model is not None else profile_model,
            allow_version_first=allow_version_first),
    }
    if environment is not None:
        overrides["environment"] = environment
    return overrides


def _verify_native_write(data: dict | None, body: dict) -> None:
    if "tags" not in body or not isinstance(data, dict) or "tags" not in data:
        return
    requested, returned = body["tags"], data["tags"]
    confirmed = requested == returned
    if not confirmed and isinstance(returned, dict) and all(
            isinstance(key, str) and isinstance(value, str)
            for key, value in returned.items()):
        # The service trims keys and comma-separated members, removes duplicate
        # members in order, then joins them back into the legacy string protocol.
        # Empty strings remain valid legacy values. Compare that receipt contract
        # without rewriting the caller's valid tags input.
        normalized = {
            _validate_tag_key(key): ("" if not value.strip() else
                ",".join(dict.fromkeys(member.strip() for member in value.split(","))))
            for key, value in requested.items()
        }
        confirmed = normalized == returned
    if not confirmed:
        raise SchemaError(
            "The service did not confirm the requested tags. "
            "Check service support and read the instance before retrying.")


def _legacy_tags_query(tags: dict[str, str] | str | None) -> str:
    # Preserve master CSV encoding and key checks; never extend it with JSON.
    if tags is not None and not isinstance(tags, (dict, str)):
        raise SchemaError("tags must be a dict of strings or a CSV string")
    if not tags:
        return ""
    if isinstance(tags, dict):
        if not all(isinstance(k, str) and isinstance(v, str) for k, v in tags.items()):
            raise SchemaError("legacy tags must contain string keys and values")
        pairs = [f"{k}:{v}" for k, v in tags.items()]
    else:
        pairs = [p for p in tags.split(",") if p.strip()]
    for pair in pairs:
        key = pair.split(":", 1)[0]
        if not key or "." in key or "$" in key:
            raise SchemaError("legacy tag keys must not contain '.' or '$'")
    return ",".join(pairs)


def _validate_custom_asset_rel(rel: str) -> None:
    """白名单校验 custom 资产相对路径（防元数据被篡改造成 pull 路径穿越）。

    push 侧用 ``Path.relative_to`` 生成 ``assets`` 清单是安全的；pull 侧**不能**
    信任元数据：拒绝绝对路径、拒绝含 ``..`` 段、拒绝空。非法即抛 SchemaError，
    不静默跳过。
    """
    if not rel:
        raise SchemaError("custom 资产清单含空路径")
    if rel.startswith("/") or rel.startswith("\\"):
        raise SchemaError(f"custom 资产清单含绝对路径: {rel!r}")
    if ".." in rel.replace("\\", "/").split("/"):
        raise SchemaError(f"custom 资产清单含 '..' 段: {rel!r}")


class InstancesClient:
    # registry 的 BASE 同值；此处独立声明使 list_paged/update 等纯控制面方法
    # 不依赖注入的 registry（直构客户端亦可调用）。
    _BASE = "/apis/v1/datasets/instances"

    def __init__(self, transport, profile, content_store, image_store,
                 registry, ingester=None) -> None:
        self._t = transport
        self._p = profile
        self._content = content_store
        self._image = image_store
        self._reg = registry
        # register=True 时经 ingest 写库（apiserver :commit 端点缺失，三段式
        # 收尾改为 ingest）。ingester 形如 (dataset, version) -> ingest job dict；
        # 由 Repo 注入 versions.ingest。直接构造未注入时 register=True 会报错。
        self._ingester = ingester
        # OSS 回退发现使用的 bucket 内根前缀（profile 可覆盖，缺省 swe/datasets）。
        self._oss_prefix = getattr(profile, 'oss_prefix', 'swe/datasets')

    def _check_split_not_locked(self, dataset: str, version: str,
                                split: str) -> None:
        """overwrite=True 时前置检查：dataset+version 下任何 split status 为
        published 则拒绝覆盖。

        published 表示数据已锁定（已发布），overwrite 语义与之冲突。检查范围是
        整个 dataset+version（不只目标 split），防止部分 split 已发布时误覆盖。
        所有 split 均非 published 或 dataset/version 不存在时放行。
        """
        from urllib.parse import quote
        q = f"dataset_name={quote(dataset, safe='')}"
        if (version or "").strip():
            q += f"&version={quote(version, safe='')}&version_scope=exact"
        else:
            q += "&version_scope=unversioned"
        profile = getattr(self, "_p", None)
        mm = business_metadata_model(
            getattr(profile, "metadata_model", None) if profile is not None else None)
        env = (getattr(profile, "dataset_environment", "") or "").strip()
        q += f"&metadata_model={quote(mm, safe='')}"
        if env:
            q += f"&environment={quote(env, safe='')}"
        # A published split on a later page must also fence overwrite. Keep a
        # finite request budget and fail closed on malformed/unbounded listings.
        for page in range(1, 1001):
            try:
                data = self._t.get(
                    f"/apis/v1/datasets/splits?{q}&page={page}&page_size=200")
            except TransportError as e:
                if e.biz_code == 92001:
                    return
                raise
            items = data.get("data") if isinstance(data, dict) else data
            if not isinstance(items, list) or any(not isinstance(s, dict) for s in items):
                raise SchemaError("invalid split listing while checking overwrite")
            locked = [s.get("name", s.get("split", "?"))
                      for s in items if s.get("status") == "published"]
            if locked:
                locked_str = ", ".join(f"'{n}'" for n in locked)
                raise SchemaError(
                    f"dataset '{dataset}' (version={version}) has locked splits: "
                    f"{locked_str}. overwrite=True is refused because published "
                    f"splits cannot be overwritten. Use "
                    f"splits.update(status='draft') to unlock first, or push to "
                    f"a different dataset/version.")
            if len(items) < 200:
                return
        raise SchemaError("split overwrite check exceeded its page budget")

    def _after_upload(self, register: bool, dataset: str,
                      version: str, instance_id: str,
                      split: str = "default") -> dict | None:
        """register=True：上传成功后触发一次 ingest 写库，返回 ingest job 摘要。

        register=False 返回 None（只传 OSS，由调用方决定何时 ingest）。

        ``split`` 必须透传给 ingest：split_first + 无 version 时服务端要求显式
        splits，否则 ingest 报 SchemaError——上传成功但 split 记录不落库，文件
        孤悬 OSS（真机锤实：``instance push --split abc`` 无 --version 场景）。
        """
        if not register:
            return None
        if self._ingester is None:
            raise SchemaError(
                "register=True 需要 ingest 回调：请通过 Repo() 构造客户端"
                "（已注入 versions.ingest），或显式传入 ingester=...；"
                "直接构造 InstancesClient 且未注入时请用 register=False 只传 OSS")
        result = self._ingester(
            dataset, version, split=split, instance_ids=[instance_id])
        return result.job if isinstance(result, IngestReport) else result

    def _layout(self, metadata_model: str | None = None) -> Layout:
        """按（显式或 profile 的）元数据模型构造布局策略。

        写侧一律经此拿 key，杜绝再直接调 ``paths.*``——后者是 version_first 语义，
        在 split_first 无版本时会拼出 ``a/b//split/id.json`` 双斜杠畸形 key。
        """
        requested_model = metadata_model
        if requested_model is None:
            requested_model = getattr(self._p, "metadata_model", None)
        model = business_metadata_model(requested_model)
        prefix = getattr(self._p, "oss_prefix", None) or P.DEFAULT_PREFIX
        return Layout(model, prefix=prefix)

    def _instance_assets_object_root(self, dataset: str, instance_id: str,
                                     version: str, split: str,
                                     metadata_model: str | None = None, *,
                                     environment: str | None = None) -> str:
        """资产目录相对于 object API 根的路径；注册的 object_path 优先。"""
        lay = self._layout(metadata_model)
        if version and self._reg is not None:
            # 非标准 Version storage_path 可能已经是 object API 根，不能
            # 无条件加版本名。服务端 object_path 已相对于它的真实根计算。
            env = environment
            if env is None:
                env = getattr(self._p, "dataset_environment", None) or None
            meta = self._reg.get(
                dataset, version, instance_id, split,
                **_registry_overrides(env, lay.model))
            if meta is not None:
                for entry in meta.manifest:
                    relative = (entry.object_path or "").rstrip("/")
                    if (entry.content_type == "directory" and relative
                            and relative.endswith("/" + instance_id)):
                        _validate_custom_asset_rel(relative)
                        return relative
                for entry in meta.manifest:
                    relative = entry.object_path or ""
                    if (entry.content_type == "file"
                            and relative.endswith("/" + instance_id + ".json")):
                        _validate_custom_asset_rel(relative)
                        metadata_dir = relative.rsplit("/", 1)[0]
                        if metadata_dir == split or metadata_dir.endswith("/" + split):
                            return f"{metadata_dir}-assets/{instance_id}"
        dataset_root = lay.dataset_root(dataset)
        assets_dir = lay.assets_dir(
            dataset, instance_id, version=version, split=split)
        return assets_dir[len(dataset_root):].rstrip("/")

    # ── 只读 ──
    def validate(self, local_path):
        """校验实例：自动检测格式（目录→harbor，dir-notask→custom，.json→swe）。"""
        fmt = detect_format(local_path)
        if fmt == "swe":
            return check_swe_json(local_path)
        if fmt == "custom":
            return check_custom(local_path)
        return check_layout(local_path)

    def get(self, dataset: str, version: str, instance_id: str,
            split: str | None = None, *,
            environment: str | None = None,
            metadata_model: str | None = None,
            fallback_to_oss: bool = True) -> DatasetInstance | None:
        """取单个实例；不存在返回 None。

        ``environment`` / ``metadata_model`` 传 None 用 profile 派生的值（默认行为
        不变）；显式传值可覆盖本次调用——CLI 需要读 online 集合时不必重建 Repo。

        **OSS 双触发回退**（设计文档 §4.4.4）：
        a. ``TransportError(biz_code=92001)``（dataset 不存在）→ OSS 回退。
        b. ``TransportError(biz_code=92023)``（split 不存在）→ OSS 回退。
        c. ``result is None``（registry 吞了 92003 instance 不存在）→ OSS 回退。
        """
        # 只在调用方显式指定时才下发覆盖参数:注册表是可注入实现,
        # 保持缺省调用形态与历史一致,避免破坏既有实现。
        overrides = _registry_overrides(
            environment, metadata_model,
            getattr(self._p, "metadata_model", None),
            allow_version_first=True)
        try:
            result = self._reg.get(
                dataset, version, instance_id, split, **overrides)
        except TransportError as e:
            # 路径 1: dataset 不存在(92001) 或 split 不存在(92023) → OSS 回退
            if (e.biz_code in (92001, 92023)
                    and fallback_to_oss and self._content is not None
                    and self._discovery_env_match(environment)):
                return self._discover_instance(
                    dataset, version, instance_id, split)
            raise
        # 路径 2: instance 不存在(None, registry 吞了 92003) → OSS 回退
        if result is None and fallback_to_oss and self._content is not None \
                and self._discovery_env_match(environment):
            return self._discover_instance(
                dataset, version, instance_id, split)
        return result

    def list(self, dataset: str, version: str,
             split: str | None = None, *,
             environment: str | None = None,
             metadata_model: str | None = None,
             fallback_to_oss: bool = True) -> list[DatasetInstance]:
        """自动翻页取全量；``environment`` / ``metadata_model`` 语义同 :meth:`get`。

        **OSS 回退**：当 ``TransportError(biz_code=92001)``（dataset 不存在）
        或 ``biz_code=92023``（split 不存在）时，
        若 ``fallback_to_oss=True`` 且 ``content_store`` 已注入，自动回退到 OSS
        存储层列举实例。
        """
        overrides = _registry_overrides(
            environment, metadata_model,
            getattr(self._p, "metadata_model", None))
        try:
            return self._reg.query(dataset, version, split, **overrides)
        except TransportError as e:
            if (e.biz_code in (92001, 92023)
                    and fallback_to_oss and self._content is not None
                    and self._discovery_env_match(environment)):
                return self._discover_instances(dataset, version, split)
            raise

    def list_paged(self, dataset: str, version: str = "", *,
                   split: str | None = None, q: str | None = None,
                   instance_id: str | None = None,
                   tags: dict[str, str] | str | None = None,
                   difficulty: str | None = None,
                   page: int = 1, page_size: int = 50,
                   environment: str | None = None,
                   metadata_model: str | None = None,
                   fallback_to_oss: bool = True) -> "PagedResult":
        """Single-page listing: tags use key:value CSV format.

        Only explicit dataset/split absence (92001/92023) allows OSS discovery.
        """
        from urllib.parse import quote
        from ..models import PagedResult
        if not (dataset or "").strip():
            raise SchemaError("dataset is required for instances.list_paged")
        if (difficulty or "").strip() and difficulty.strip() not in ("easy", "medium", "hard"):
            raise SchemaError(
                f"invalid difficulty {difficulty!r}; must be easy/medium/hard")
        tags_q = _legacy_tags_query(tags)
        params: list[tuple[str, str]] = [("dataset_name", dataset.strip())]
        if (version or "").strip():
            params.append(("version", version.strip()))
        if (split or "").strip():
            params.append(("split", split.strip()))
        if (q or "").strip():
            params.append(("q", q.strip()))
        if (instance_id or "").strip():
            params.append(("instance_id", instance_id.strip()))
        if tags_q:
            params.append(("tags", tags_q))
        if (difficulty or "").strip():
            params.append(("difficulty", difficulty.strip()))
        env = (environment or "").strip()
        if not env:
            env = (getattr(self._p, "dataset_environment", "") or "").strip()
        if env:
            params.append(("environment", env))
        requested_model = metadata_model
        if requested_model is None:
            requested_model = getattr(self._p, "metadata_model", None)
        mm = business_metadata_model(requested_model)
        params.append(("metadata_model", mm))
        params.append(("page", str(int(page))))
        params.append(("page_size", str(int(page_size))))
        query = "&".join(f"{k}={quote(v, safe='')}" for k, v in params)
        try:
            data, pagination = self._t.request_with_meta("GET", f"{self._BASE}?{query}")
        except TransportError as e:
            if (e.biz_code in (92001, 92023)
                    and fallback_to_oss and self._content is not None
                    and self._discovery_env_match(environment)):
                return self._discover_instances_paged(
                    dataset, version, split,
                    q=q, instance_id=instance_id,
                    tags=tags,
                    difficulty=difficulty,
                    page=page, page_size=page_size)
            raise
        rows = data.get("instances", data) if isinstance(data, dict) else data
        rows = rows if isinstance(rows, list) else []
        items = [DatasetInstance.from_dict(r) for r in rows if isinstance(r, dict)]
        return PagedResult.from_response(items, pagination, int(page), int(page_size))

    # ── OSS 回退发现（未注册 dataset 的 instance 合成） ──

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

    def _discover_instances(self, dataset: str, version: str,
                            split: str | None = None, *,
                            read_content: bool = False,
                            max_keys: int | None = None) -> list[DatasetInstance]:
        """OSS 回退的 instances.list — 从 OSS 列举指定 version/split 下的实例。

        ``max_keys`` 透传给 ``build_synthetic_instances`` 限制**有效实例**
        数上限（P1-1c）：无过滤的分页请求只需服务到请求页，避免首页请求
        的 LIST 开销随对象总量线性增长。有过滤（q/tags/difficulty）语义
        优先，调用方不传该值保持全量列举。
        """
        from ..store.oss_discovery import build_synthetic_instances
        return build_synthetic_instances(
            self._content, dataset, version, split,
            oss_prefix=getattr(self, '_oss_prefix', 'swe/datasets'),
            read_content=read_content, max_keys=max_keys)

    def _discover_instance(self, dataset: str, version: str,
                           instance_id: str,
                           split: str | None = None, *,
                           read_content: bool = False) -> DatasetInstance | None:
        """OSS 回退的 instances.get — 精确查找单个实例。"""
        from ..store.oss_discovery import build_synthetic_instance
        return build_synthetic_instance(
            self._content, dataset, version, instance_id, split,
            oss_prefix=getattr(self, '_oss_prefix', 'swe/datasets'),
            read_content=read_content)

    def _discover_instances_paged(
        self, dataset: str, version: str, split: str | None, *,
        q: str | None, instance_id: str | None,
        tags: dict[str, str] | str | None,
        difficulty: str | None,
        page: int, page_size: int,
    ) -> "PagedResult":
        """OSS 回退的 list_paged：全量列举 + 客户端过滤 + 内存分页。

        ``instance_id`` 精确匹配时直接 GET，不列举全量。
        """
        from ..store.oss_discovery import _in_memory_paged

        tags_dict = tags if isinstance(tags, dict) else self._parse_tags_csv(tags or "")
        if tags_dict:
            raise SchemaError(
                "tag filtering is not supported in unregistered OSS fallback mode; "
                "please register the dataset in AP first")
        normalized_difficulty = (difficulty or "").strip()
        # tags 过滤在 OSS 回退不支持；difficulty 过滤需要 GetObject；普通过滤/列表保持 list-only 零新增读取。
        read_content = bool(normalized_difficulty)
        # 优化：instance_id 精确匹配时直接 GET，不列举全量
        exhausted = True
        if instance_id:
            inst = self._discover_instance(
                dataset, version, instance_id, split, read_content=read_content)
            items: list[DatasetInstance] = [inst] if inst else []
        else:
            # P1-1c + 复审 P1：无任何过滤时按**有效实例数**推进列举到
            # 请求页（page*page_size 个有效实例），并用探针实例/OSS
            # 耗尽状态确定 has_more——无效 key 不再挤占页容量，恰满页
            # 且 OSS 耗尽时不再误报 has_more。有过滤时保持全量列举
            # （过滤正确性优先于列举开销）。
            unfiltered = not (q or normalized_difficulty)
            if unfiltered:
                from ..store.oss_discovery import build_synthetic_instances_paged
                want = page * page_size
                items, exhausted = build_synthetic_instances_paged(
                    self._content, dataset, version, split,
                    oss_prefix=getattr(self, '_oss_prefix', 'swe/datasets'),
                    want=want)
            else:
                items = self._discover_instances(
                    dataset, version, split, read_content=read_content)
                exhausted = True  # 全量列举 → 已耗尽

        # 客户端过滤
        if q:
            q_lower = q.lower()
            items = [i for i in items
                     if q_lower in i.instance_id.lower()]
        if normalized_difficulty:
            items = [i for i in items
                     if i.difficulty == normalized_difficulty]

        result = _in_memory_paged(items, int(page), int(page_size))
        if not exhausted:
            # OSS 未列举到底（探针实例证明还有更多有效实例）：真实总量
            # 未知（-1，与无分页信封语义一致），请求页之后仍可能有数据。
            result.total = -1
            result.has_more = True
        return result

    @staticmethod
    def _parse_tags_csv(tags_str: str) -> dict[str, str]:
        """The original master CSV parser (not the native-filter protocol)."""
        result: dict[str, str] = {}
        for pair in str(tags_str).split(","):
            pair = pair.strip()
            if not pair:
                continue
            parts = pair.split(":", 1)
            result[parts[0]] = parts[1] if len(parts) == 2 else ""
        return result

    # ── 实例目录/文件列举（GET /datasets/objects）──────────────────

    def list_objects(self, dataset: str, instance_id: str,
                     split: str | None = None, *,
                     version: str = "",
                     path: str | None = None,
                     page_size: int = 100,
                     max_pages: int = 50,
                     environment: str | None = None,
                     metadata_model: str | None = None,
                     dataset_split_id: str | None = None
                     ) -> "DatasetObjectListResult":
        """列举实例资产目录下的文件/子目录（自动翻页）。

        调用控制面 ``GET /apis/v1/datasets/objects``，返回指定实例的
        ``{version}/{split}-assets/{instance_id}/`` 路径下的目录和文件列表；
        无版本时省略 ``{version}/``。prefix 相对于 Dataset 根目录。
        自动翻页合并所有结果，直到 ``truncated=False`` 或达到 ``max_pages``。

        Parameters
        ----------
        dataset : str
            Dataset 名称（``L1/L2`` 格式）。
        instance_id : str
            实例 ID。
        split : str, optional
            Split 名称；为 None 时使用 ``"default"``。
        version : str
            版本号，默认空串（split_first 布局下可为空）。
        path : str, optional
            子目录路径过滤（相对于实例资产根目录）。
            为 None 或空串时列举实例根目录下全部内容；
            非空时仅列举该路径下的内容（如 ``"solution"`` 或 ``"tests/sealed"``）。
        page_size : int
            每页大小，默认 100。
        max_pages : int
            最大翻页数（安全阀，防无限循环），默认 50。
        environment : str, optional
            ``online`` / ``pre``，None 时用 profile 派生值。
        metadata_model : str, optional
            ``split_first`` / ``version_first``，None 时用 profile 派生值。
        dataset_split_id : str, optional
            Split ID，可直接指定以避免 split 名称解析。

        Returns
        -------
        DatasetObjectListResult
            合并后的完整结果。``truncated`` 为 True 表示因 ``max_pages`` 截断。
        """
        from urllib.parse import quote
        from ..models import DatasetObjectListResult
        if not (dataset or "").strip():
            raise SchemaError("dataset is required for instances.list_objects")
        if not (instance_id or "").strip():
            raise SchemaError(
                "instance_id is required for instances.list_objects")
        split = (split or "default").strip()
        # environment / metadata_model：优先显式值，其次 profile 派生
        env = (environment or "").strip()
        if not env:
            env = (getattr(self._p, "dataset_environment", "") or "").strip()
        requested_model = metadata_model
        if requested_model is None:
            requested_model = getattr(self._p, "metadata_model", None)
        mm = business_metadata_model(requested_model)
        # object API 的 prefix 相对于 Dataset 根，而非 Version 根。
        instance_asset_prefix = self._instance_assets_object_root(
            dataset.strip(), instance_id.strip(), version, split, mm,
            environment=env or None)
        if path:
            full_prefix = f"{instance_asset_prefix}/{path.strip().strip('/')}"
        else:
            full_prefix = instance_asset_prefix
        # 自动翻页
        all_dirs: list = []
        all_files: list = []
        tk: str | None = None
        result = DatasetObjectListResult()
        for _ in range(max_pages):
            params: list[tuple[str, str]] = [
                ("dataset_name", dataset.strip()),
                ("split", split),
                ("prefix", full_prefix),
                ("page_size", str(int(page_size))),
                ("version", (version or "").strip())]
            if (dataset_split_id or "").strip():
                params.append(("dataset_split_id", dataset_split_id.strip()))
            if tk:
                params.append(("token", tk))
            if env:
                params.append(("environment", env))
            if mm:
                params.append(("metadata_model", mm))
            qs = "&".join(f"{k}={quote(v, safe='')}" for k, v in params)
            data = self._t.get(f"/apis/v1/datasets/objects?{qs}")
            if not isinstance(data, dict):
                break
            page = DatasetObjectListResult.from_dict(data)
            all_dirs.extend(page.directories)
            all_files.extend(page.files)
            result = page  # 保留最后一页的 dataset/version/prefix 元信息
            if not page.truncated or not page.next_token:
                break
            tk = page.next_token
        result.directories = all_dirs
        result.files = all_files
        return result

    # ── 变更检测辅助 ────────────────────────────────────────────────

    def list_content_hashes(self, dataset: str, version: str = "",
                            split: str | None = None, *,
                            environment: str | None = None,
                            metadata_model: str | None = None
                            ) -> dict[str, str]:
        """批量查询远端实例的 ``source_hash``（存在 ``extend_meta`` 中）。

        返回 ``{instance_id: source_hash}`` 字典。用于 ``skip_unchanged``
        变更检测：与本地 ``compute_source_hash`` 或自定义哈希比对，
        匹配则跳过 pack + upload。
        """
        overrides = _registry_overrides(
            environment, metadata_model,
            getattr(self._p, "metadata_model", None))
        instances = self.list(dataset, version, split, **overrides)
        result: dict[str, str] = {}
        for inst in instances:
            h = (inst.extend_meta or {}).get("source_hash", "")
            if h:
                result[inst.instance_id] = h
        return result

    # ── 实例删除 ────────────────────────────────────────────────────

    def delete(self, dataset: str, version: str, instance_id: str, *,
               split: str | None = None,
               environment: str | None = None,
               metadata_model: str | None = None,
               delete_files: bool = False) -> InstanceDeleteResult:
        """删除单个实例；``delete_files=True`` 走服务端受限 STS 文件删除流程。

        纯元数据删除（默认）：``DELETE /datasets/instances/detail``，OSS 文件
        保留，后续 ingest 可能重建记录。

        ``delete_files=True``（Aone 88582969 新流程）：
        1. ``POST /apis/v1/credentials``（``purpose=instance_delete``，按
           instance 精确选择器）——服务端检查权限/存储布局/共享引用后返回
           ``operation_id``、``delete_scope``（精确 key + 前缀清单）与仅含
           ``oss:DeleteObject``/``ListObjects`` 的受限 STS（900s）；
        2. SDK 按 ``delete_scope`` 删除 OSS 文件（主 JSON、assets；report
           默认保留，``include_reports=True`` 才纳入）；
        3. ``DELETE /datasets/instances/detail`` 携 ``delete_operation_id``——
           服务端 HEAD/LIST 校验文件已清空后才在事务里删元数据。

        OSS 失败时保留数据库记录；数据库完成调用失败（如 409 文件残留）时
        文件可能已删，用**相同参数**重试即可收敛——幂等键相同则服务端返回
        同一 operation，不重复签发/扣统计。此操作不具备跨 OSS/数据库事务性，
        调用方必须先停止同实例的上传/ingest。非 canonical storage_path 不
        支持文件删除。删除凭据独立于读写凭据缓存，绝不复用普通 writer 令牌。
        """
        from urllib.parse import quote
        if not (dataset or "").strip():
            raise SchemaError("dataset is required for instances.delete")
        if not (instance_id or "").strip():
            raise SchemaError("instance_id is required for instances.delete")
        params: list[tuple[str, str]] = [
            ("dataset_name", dataset.strip()),
            ("instance_id", instance_id.strip())]
        if (version or "").strip():
            params.append(("version", version.strip()))
        if (split or "").strip():
            params.append(("split", (split or "").strip()))
        env = (environment or "").strip()
        if not env:
            env = (getattr(self._p, "dataset_environment", "") or "").strip()
        if env:
            params.append(("environment", env))
        requested_model = metadata_model
        if requested_model is None:
            requested_model = getattr(self._p, "metadata_model", None)
        params.append(("metadata_model",
                       business_metadata_model(requested_model)))
        if not isinstance(delete_files, bool):
            raise SchemaError("delete_files must be a bool")
        operation = None
        if delete_files:
            operation = self._prepare_instance_deletion(
                dataset.strip(), (version or "").strip(), instance_id.strip(),
                split=split, environment=env, metadata_model=requested_model)
            if operation.state != "completed":
                self._delete_instance_files(operation)
            params.append(("delete_operation_id", operation.operation_id))
        qs = "&".join(f"{k}={quote(v, safe='')}" for k, v in params)
        failure = None
        completed: dict | None = None
        try:
            completed = self._t.delete(f"/apis/v1/datasets/instances/detail?{qs}")
        except Exception as exc:
            if not delete_files:
                raise
            status = getattr(exc, "status", None)
            code = getattr(exc, "biz_code", None)
            failure = TransportError(
                "OSS files were removed but instance metadata deletion failed; "
                "retry the same deletion after resolving server authorization or availability",
                status=status if isinstance(status, int) else None,
                biz_code=code if isinstance(code, int) else None)
        if failure is not None:
            raise failure from None
        if not delete_files:
            return InstanceDeleteResult(instance_id=instance_id.strip())
        # 完成调用成功：服务端响应含 operation_id/state/stats_state。
        result = (completed or {}) if isinstance(completed, dict) else {}
        return InstanceDeleteResult(
            instance_id=instance_id.strip(),
            content_deleted=True,
            metadata_deleted=True,
            operation_id=str(result.get("operation_id") or operation.operation_id),
            state=str(result.get("state") or "completed"),
            stats_state=(str(result["stats_state"])
                         if isinstance(result.get("stats_state"), str)
                         and result.get("stats_state") else None))

    # ── 受限 STS 实例删除（Aone 88582969；服务端 113671c9 契约） ──

    def _prepare_instance_deletion(self, dataset: str, version: str,
                                   instance_id: str, *,
                                   split: str | None, environment: str,
                                   metadata_model: str | None):
        """申请 instance_delete 受限删除凭据；返回 operation 元信息。

        幂等键由 (dataset, version, split, instance_id, environment) 稳定派生
        ——失败重试复用同一 operation，服务端不重复签发、不重复扣统计。
        服务端仅接受 instance 精确选择器：oss_bucket/prefix/permission/
        list_only/dataset_source 一律不传（传了即 400）。
        """
        P.DatasetName.parse(dataset)
        validate_instance_id(instance_id)
        for name, value in (("version", version), ("split", split)):
            if name == "version" and not value:
                continue
            if not isinstance(value, str) or value != value.strip():
                raise SchemaError(f"{name} must be a canonical path segment")
            validate_instance_id(value)
        model = business_metadata_model(metadata_model if metadata_model is not None
                                        else getattr(self._p, "metadata_model", None))
        if model != "split_first":
            raise SchemaError(
                "instance file deletion requires split_first metadata model")
        digest = hashlib.sha256(
            "\x00".join(("instance-delete", dataset, (version or "").strip(),
                         split or "", instance_id, environment or "")).encode()
        ).hexdigest()
        body: dict = {
            "resource": "oss",
            "purpose": "instance_delete",
            "metadata_model": "split_first",
            "dataset_name": dataset,
            "instance_id": instance_id,
            "idempotency_key": f"sdk-{digest[:48]}",
        }
        if version:
            body["version"] = version
        if split:
            body["split"] = split
        if environment:
            body["environment"] = environment
        r = self._t.post("/apis/v1/credentials", body, idempotent=True)
        if not isinstance(r, dict):
            raise TransportError("instance deletion credential response invalid")
        op_id = r.get("operation_id")
        if not isinstance(op_id, str) or not op_id.strip():
            raise TransportError(
                "instance deletion credential response missing operation_id")
        state = r.get("state")
        if state not in ("issued", "completed"):
            raise TransportError(
                f"instance deletion operation state invalid: {state!r}")
        scope = r.get("delete_scope")
        if not isinstance(scope, dict):
            raise TransportError("instance deletion scope missing")
        keys = scope.get("keys")
        prefixes = scope.get("prefixes")
        bucket = scope.get("bucket")
        for value, label in ((keys, "keys"), (prefixes, "prefixes")):
            if not isinstance(value, list) or any(
                    not isinstance(k, str) or not k for k in value):
                raise TransportError(f"instance deletion scope {label} invalid")
        if state == "issued":
            for field in ("OSS_ACCESS_KEY_ID", "OSS_ACCESS_KEY_SECRET",
                          "OSS_SECURITY_TOKEN", "OSS_ENDPOINT"):
                if not isinstance(r.get(field), str) or not r.get(field):
                    # 只报字段名，绝不把密钥值带进异常（对齐 transport._require）。
                    raise TransportError(
                        f"instance deletion credential response missing {field}")
        return NS(operation_id=op_id.strip(), state=state, bucket=bucket,
                  keys=keys, prefixes=prefixes,
                  credentials=r if state == "issued" else None)

    def _delete_instance_files(self, operation) -> None:
        """按服务端返回的 delete_scope 删除 OSS 文件（受限 STS 直删）。

        列举与删除使用**同一张受限删除令牌**（服务端 policy 同时含
        oss:DeleteObject 与带 Prefix 条件的 ListObjects）。逐 key 直接删除；
        前缀按服务端返回的目录范围分页列举后删除。此流程独立签发删除凭据、
        独立开桶，不经读写凭据缓存——普通 writer 令牌不含 DeleteObject。
        """
        if not isinstance(operation.bucket, str) or not operation.bucket:
            raise TransportError("instance deletion scope bucket missing")
        delete_files = getattr(self._content, "delete_instance_files", None)
        if not callable(delete_files):
            raise SchemaError(
                "content store does not support instance file deletion")
        failure = None
        try:
            delete_files(operation)
        except Exception as exc:  # noqa: BLE001
            # 不透传含签名 URL/凭据的 OSS 原始异常。
            status = getattr(exc, "status", None)
            failure = TransportError(
                "instance file deletion failed; metadata was not deleted; "
                "retry with the same arguments to reuse the server operation; "
                "files may be partially removed; stop concurrent writers first",
                status=status if isinstance(status, int) else None)
        if failure is not None:
            raise failure from None

    def _read_tag_record(self, dataset: str, version: str, instance_id: str, *,
                         split: str | None, environment: str | None,
                         metadata_model: str | None) -> DatasetInstance:
        record = self.get(
            dataset, version, instance_id, split=split,
            environment=environment, metadata_model=metadata_model,
            fallback_to_oss=False)
        if record is None:
            raise SchemaError(f"instance {instance_id!r} not found")
        return record

    def _read_tags(self, dataset: str, version: str, instance_id: str, *,
                   split: str | None, environment: str | None,
                   metadata_model: str | None) -> dict[str, list[str]]:
        record = self._read_tag_record(
            dataset, version, instance_id, split=split, environment=environment,
            metadata_model=metadata_model)
        return normalize_tag_values(record.tag_values or {})

    def list_tags(self, dataset: str, version: str, instance_id: str, *,
                  split: str | None = None, environment: str | None = None,
                  metadata_model: str | None = None) -> dict[str, list[str]]:
        """Read a detached native map; legacy tags never supply missing values."""
        return self._read_tags(
            dataset, version, instance_id, split=split, environment=environment,
            metadata_model=metadata_model)

    def _mutate_tag_values(self, dataset, version, instance_id, tags, *,
                           operation, split, environment, metadata_model):
        normalized = normalize_tag_values(tags, keep_empty=True)
        record = self._read_tag_record(
            dataset, version, instance_id, split=split, environment=environment,
            metadata_model=metadata_model)
        current = normalize_tag_values(record.tag_values or {})
        merged = {key: list(values) for key, values in current.items()}
        for key, values in normalized.items():
            if not values:
                if operation == "set":
                    merged.pop(key, None)
            elif operation == "set":
                merged[key] = values
            elif operation == "append":
                existing = merged.setdefault(key, [])
                existing.extend(value for value in values if value not in existing)
            elif key in merged:
                remaining = [value for value in merged[key] if value not in values]
                if remaining:
                    merged[key] = remaining
                else:
                    merged.pop(key)
        merged = normalize_tag_values(merged)
        if merged == current:
            return record
        merged_tags = {key: ",".join(values) for key, values in merged.items() if values}
        return self.update(
            dataset, version, instance_id, split=split, tags=merged_tags,
            environment=environment, metadata_model=metadata_model)

    def set_tags(self, dataset: str, version: str, instance_id: str,
                 tags: dict[str, str | list[str]], *, split: str | None = None,
                 environment: str | None = None,
                 metadata_model: str | None = None) -> DatasetInstance:
        """Set native keys by non-atomic whole-map read-modify-write; [] deletes a key."""
        return self._mutate_tag_values(
            dataset, version, instance_id, tags, operation="set", split=split,
            environment=environment, metadata_model=metadata_model)

    def append_tags(self, dataset: str, version: str, instance_id: str,
                    tags: dict[str, str | list[str]], *, split: str | None = None,
                    environment: str | None = None,
                    metadata_model: str | None = None) -> DatasetInstance:
        """Append unique native values in order; duplicate-only calls do not PATCH."""
        return self._mutate_tag_values(
            dataset, version, instance_id, tags, operation="append", split=split,
            environment=environment, metadata_model=metadata_model)

    def remove_tags(self, dataset: str, version: str, instance_id: str,
                    tags: dict[str, str | list[str]], *, split: str | None = None,
                    environment: str | None = None,
                    metadata_model: str | None = None) -> DatasetInstance:
        """Remove native values, deleting empty keys; missing values are no-ops."""
        return self._mutate_tag_values(
            dataset, version, instance_id, tags, operation="remove", split=split,
            environment=environment, metadata_model=metadata_model)

    def clear_tags(self, dataset: str, version: str, instance_id: str,
                   keys: list[str], *, split: str | None = None,
                   environment: str | None = None,
                   metadata_model: str | None = None) -> DatasetInstance:
        """Delete selected native keys; clear the whole map with update(tag_values={})."""
        if isinstance(keys, (str, bytes)):
            raise SchemaError("clear_tags keys must be an iterable of strings")
        try:
            selected = {_validate_tag_key(key): [] for key in keys}
        except TypeError as exc:
            raise SchemaError("clear_tags keys must be an iterable of strings") from exc
        return self._mutate_tag_values(
            dataset, version, instance_id, selected, operation="set", split=split,
            environment=environment, metadata_model=metadata_model)

    def create(self, dataset: str, version: str, instance_id: str, *,
               split: str = "default", manifest: list[dict] | None = None,
               tags: dict[str, str] | None = None,
               tag_values: dict[str, str | list[str]] | None = None,
               difficulty: str | None = None, docker_image: str | None = None,
               extend_meta: dict | None = None,
               environment: str | None = None,
               metadata_model: str | None = None) -> DatasetInstance:
        """Create metadata with the strict POST DTO; native values never replace tags."""
        from urllib.parse import quote
        from ..store.registry import _unimplemented

        dataset = (dataset or "").strip()
        version = (version or "").strip()
        split = (split or "").strip()
        instance_id = (instance_id or "").strip()
        if not dataset or not instance_id:
            raise SchemaError("instances.create requires dataset and instance_id")
        if tags is not None and tag_values is not None:
            raise SchemaError("cannot provide both tags and tag_values")
        if tag_values is not None:
            normalized = normalize_tag_values(tag_values)
            tags = {k: ",".join(v) for k, v in normalized.items() if v}
        elif tags is not None and (not isinstance(tags, dict) or not all(
                isinstance(k, str) and isinstance(v, str) for k, v in tags.items())):
            raise SchemaError("legacy tags must contain strings")
        if difficulty is not None and difficulty not in ("", "easy", "medium", "hard"):
            raise SchemaError("invalid difficulty")
        body: dict = {"instance_id": instance_id, "split": split}
        for key, value in (("manifest", manifest), ("tags", tags),
                           ("difficulty", difficulty),
                           ("docker_image", docker_image), ("extend_meta", extend_meta)):
            if value is not None:
                body[key] = value
        overrides = _registry_overrides(
            environment, metadata_model, getattr(self._p, "metadata_model", None))
        env = (environment if environment is not None else
               getattr(self._p, "dataset_environment", "")) or ""
        env = env.strip()
        params = [("dataset_name", dataset), ("version", version),
                  ("split", split), ("metadata_model", overrides["metadata_model"])]
        if env:
            params.append(("environment", env))
        query = "&".join(f"{k}={quote(v, safe='')}" for k, v in params)
        with _unimplemented(
                "POST /apis/v1/datasets/instances",
                "Use an apiserver that supports instance metadata creation."):
            data = self._t.post(f"{self._BASE}?{query}", body)
        _verify_native_write(data, body)
        return DatasetInstance.from_dict(data)

    def update(self, dataset: str, version: str, instance_id: str, *,
               split: str | None = None, dataset_split_id: str | None = None,
               manifest: list[dict] | None = None,
               tags: dict[str, str] | None = None,
               tag_values: dict[str, str | list[str]] | None = None,
               difficulty: str | None = None,
               docker_image: str | None = None,
               extend_meta: dict | None = None,
               environment: str | None = None,
               metadata_model: str | None = None) -> DatasetInstance:
        """更新实例元数据（``PATCH /datasets/instances/detail``，不动 OSS 字节）。

        服务端 body 白名单（严格解析，未知字段 400）：``manifest``（整体替换，
        每项 {content_type, content_format, content_digest, file_path}）、
        ``tags``（字符串 map，多值按逗号拼接，整体替换）、
        ``difficulty``（"easy"/"medium"/"hard"，空串=清除）、
        ``docker_image``（空串=清除）、``extend_meta``（整体替换）。全部可选但
        **至少一项必填**（SDK 前置校验）。

        正常业务固定 split_first，使用 ``dataset_split_id`` 或
        dataset+version+split+instance_id 寻址。``metadata_model=None`` 保持
        split_first；显式 ``version_first`` 可读取并更新历史布局记录。
        """
        from urllib.parse import quote
        body: dict = {}
        if manifest is not None:
            body["manifest"] = manifest
        if tags is not None and tag_values is not None:
            raise SchemaError("cannot provide both tags and tag_values")
        if tag_values is not None:
            normalized = normalize_tag_values(tag_values)
            body["tags"] = {k: ",".join(v) for k, v in normalized.items() if v}
        elif tags is not None:
            if not isinstance(tags, dict) or not all(
                    isinstance(k, str) and isinstance(v, str) for k, v in tags.items()):
                raise SchemaError("legacy tags must contain strings")
            body["tags"] = dict(tags)
        if difficulty is not None:
            if difficulty not in ("", "easy", "medium", "hard"):
                raise SchemaError(
                    f"invalid difficulty {difficulty!r}; must be easy/medium/hard "
                    f"or '' to clear")
            body["difficulty"] = difficulty
        if docker_image is not None:
            body["docker_image"] = docker_image
        if extend_meta is not None:
            body["extend_meta"] = extend_meta
        if not body:
            raise SchemaError(
                "instances.update requires at least one field (manifest / tags / tag_values / "
                "difficulty / docker_image / extend_meta)")
        # 寻址：dataset_split_id 优先（split_first 精确记录）；否则三元组。
        model = business_metadata_model(
            metadata_model, allow_version_first=True)
        if dataset_split_id:
            q = (f"dataset_split_id={quote(dataset_split_id, safe='')}"
                 f"&instance_id={quote(instance_id, safe='')}")
        else:
            if not (dataset or "").strip() or not (instance_id or "").strip():
                raise SchemaError(
                    "instances.update requires dataset_split_id, or dataset + "
                    "instance_id (with optional version/split)")
            q = (f"dataset_name={quote(dataset, safe='')}"
                 f"&instance_id={quote(instance_id, safe='')}")
            if (version or "").strip():
                q += f"&version={quote(version.strip(), safe='')}"
            split_name = (split or "").strip()
            if split_name and (model == "split_first" or split_name != "default"):
                q += f"&split={quote(split_name, safe='')}"
        env = (environment or "").strip()
        if not env:
            env = (getattr(self._p, "dataset_environment", "") or "").strip()
        if env:
            q += f"&environment={quote(env, safe='')}"
        q += f"&metadata_model={quote(model, safe='')}"
        data = self._t.patch(f"{self._BASE}/detail?{q}", body)
        _verify_native_write(data, body)
        return DatasetInstance.from_dict(data) if isinstance(data, dict) else DatasetInstance(
            instance_id=instance_id, dataset=dataset, dataset_version=version or "")

    # ── 反馈回写（append） ──
    def add_feedback(self, dataset: str, version: str, instance_id: str,
                     feedback: Feedback | dict, split: str | None = None
                     ) -> DatasetInstance:
        fb = feedback if isinstance(feedback, Feedback) else Feedback(**feedback)
        fb.validate()
        return self._reg.feedback_append(dataset, version, instance_id,
                                         fb.to_dict(), split)

    # ── 写（元数据先行） ──
    def push(self, local_path, dataset: str, version: str, *,
             owner_reference: OwnerReference | str | None = None,
             split: str = "default", push_image: bool = True,
             overwrite: bool = False, register: bool = True,
             verify: bool = True,
             image_release_dst_acr: str | None = None,
             content_hash: str | None = None,
             skip_unchanged: bool = False,
             compress_level: int | None = None) -> PushResult:
        """推一个实例：自动检测格式（目录→harbor，.json→swe），validate → 上传。

        harbor: validate → (可选)推镜像 → 上传 OSS(content.tgz + {id}.json)。
        swe: validate JSON → 上传 OSS({id}.json only)，不推镜像。

        register=True（默认）：上传成功后自动触发一次 versions.ingest 把元数据写库
        （apiserver 的 :commit 端点缺失，三段式收尾由 ingest 替代；结果见
        ``PushResult.ingest``）。register=False：只传 OSS 不写库，之后由调用方
        自行 versions.ingest() 扫描入库。

        verify=True（默认）在真正发生上传后回读校验：确认 OSS 对象确实可 HEAD 到。

        image_release_dst_acr（可选）：目标（prod）ACR host（仅 harbor 格式有效）。

        content_hash（可选）：调用方提供的内容标识（如 git tree id），
        存入 ``extend_meta.source_hash``，供后续 ``skip_unchanged`` 比对。

        skip_unchanged（可选）：若为 True 且 content_hash 非空，先查远端
        ``extend_meta.source_hash``，匹配则跳过 pack + upload。

        compress_level（可选）：gzip 压缩级别（1-9），传 None 用默认值。
        """
        local_path = Path(local_path)
        if register and self._ingester is None:
            # fail-fast：register=True 需要 ingest 回调，先于任何打包/上传报错
            raise SchemaError(
                "register=True 需要 ingest 回调：请通过 Repo() 构造客户端"
                "（已注入 versions.ingest），或显式传入 ingester=...；"
                "直接构造 InstancesClient 且未注入时请用 register=False 只传 OSS")
        # overwrite=True 前置检查：split status=published 表示已锁定，禁止覆盖。
        # 在任何格式检测/打包/上传之前拦截，避免本地打包耗时后才发现不可写。
        if overwrite:
            self._check_split_not_locked(dataset, version, split)
        fmt = detect_format(local_path)
        if fmt == "swe":
            return self._push_swe(local_path, dataset, version, split=split,
                                  overwrite=overwrite, register=register,
                                  verify=verify)
        if fmt == "custom":
            return self._push_custom(local_path, dataset, version, split=split,
                                     push_image=push_image,
                                     overwrite=overwrite, register=register,
                                     verify=verify, content_hash=content_hash)
        # ── harbor 路径 ──
        report = check_layout(local_path)          # ① 本地校验（缺文件即抛）
        if report.config.get("steps"):
            from .._harbor import push_multi_step
            return push_multi_step(
                self, report, dataset, version, split=split,
                owner_reference=owner_reference, push_image=push_image,
                overwrite=overwrite, register=register, verify=verify,
                image_release_dst_acr=image_release_dst_acr,
                compress_level=compress_level)
        instance_id = report.instance_id
        lay = self._layout()                        # 写侧 key/镜像命名统一经 layout
        owner_ref = ("" if owner_reference is None
                     else owner_reference if isinstance(owner_reference, str)
                     else owner_reference.to_json())

        docker_ref = ""
        image_tar = local_path / "environment" / "image.tar.gz"
        dockerfile = local_path / "environment" / "Dockerfile"
        has_image = image_tar.is_file()
        if has_image:
            if push_image:
                # 自带 tar 且会推 ACR：docker_image 记它将被推到的 ACR 目标地址。
                # 仅在 push_image 时记——否则该 ACR 地址指向从未推送过的镜像，是假的。
                docker_ref = lay.image_ref(self._p.effective_acr_host, self._p.acr_namespace,
                                           dataset, instance_id,
                                           version=version, split=split)
        else:
            # 无 tar：复用 Dockerfile 现有 FROM（运行时构建的共享 base）。这是纯本地文本
            # 读取，与是否推送无关，故**不受 push_image 门控**——早先把它也挂在 push_image
            # 下，导致 push_image=False 时 docker_image 落空、ingest 落库为 None，下游
            # "落库优先"回落到从未推送的规则 ACR 地址、release 校验必败。
            docker_ref = dockerfile_from(dockerfile.read_text())
        # 生产交付硬失败：要求推镜像却既无 tar 也无可用 FROM —— 在写元数据前就报错，
        # 保证不留 orphan pending 记录（元数据先行 + 本地先校验）。
        if push_image and not has_image and not docker_ref:
            raise ImageMissing(f"{instance_id}: push_image but no image.tar.gz "
                               f"and no FROM in Dockerfile")

        # 「实例↔镜像」上架映射（可选）：给定目标 ACR 时写进 extend_meta，随 ingest 入库、
        # 随上架 copy 到 prod。复用 release.image_release_meta（与 build_image_distributions
        # 同口径），source==push 记录的 docker_ref，故 push 时算的与 publish 时完全一致。
        extend_meta: dict[str, str] = {}
        if image_release_dst_acr:
            from .. import release as _R  # 局部导入避免循环依赖
            extend_meta = _R.image_release_meta(
                docker_ref, self._p.effective_acr_host, image_release_dst_acr)

        # ② 写元数据(pending) → 拿稳定 id（register=False 时跳过，用本地 id）
        meta = DatasetInstance(
            instance_id=instance_id, dataset=dataset, dataset_version=version,
            owner_reference=owner_ref, split=split,
            difficulty=report.metadata.get("difficulty"),
            docker_image=docker_ref or None,
            tags=_tags(report.metadata),
            tag_values=(normalize_tag_values(report.metadata["tag_values"])
                        if report.metadata.get("tag_values") is not None else None),
            extend_meta=extend_meta,
            instance_status="draft",
        )
        uid = instance_id

        # 变更检测：skip_unchanged=True 时，若 content_hash 与远端一致，跳过 pack+upload。
        if skip_unchanged and content_hash:
            try:
                remote = self._reg.get(dataset, version, instance_id, split)
                if remote is not None:
                    remote_hash = (remote.extend_meta or {}).get("source_hash", "")
                    if remote_hash == content_hash:
                        logger.info("push %s: skip (source_hash match)", instance_id)
                        return PushResult(
                            instance_id=instance_id, uploaded=False,
                            skipped=True, image_pushed=False,
                            docker_image=docker_ref or None,
                            digests={}, ingest=None)
            except (TransportError, Exception):  # noqa: BLE001
                pass  # 查询失败不阻断，继续正常 push
        # 将 content_hash 存入 extend_meta，供下次 skip_unchanged 比对
        if content_hash:
            extend_meta["source_hash"] = content_hash
            meta.extend_meta = extend_meta

        # 打包 + 构造 manifest（本地）→ register(pending) → 推 ACR → 上传 OSS。
        # register 需要 manifest：apiserver 的 hasFile 校验要求至少一条
        # content_type=file 项，manifest 缺失时 register 被 92005 拒（曾导致
        # custom/harbor 主路径 push(register=True) 失败）。register 仍先于任何
        # 远程写（元数据先行），manifest 在本地打包时即可算出 digest。
        import time as _time
        _t0 = _time.monotonic()
        with tempfile.TemporaryDirectory(prefix="irepo_") as td:
            tgz = Path(td) / "content.tgz"
            digest = pack(local_path, tgz, exclude_image_tar=True,
                          compresslevel=compress_level)
            _pack_elapsed = _time.monotonic() - _t0
            meta.manifest = _manifest(self._p.oss_bucket, dataset, version,
                                      instance_id, split, digest, lay)

            image_pushed = False
            if push_image and has_image:
                # ③ 推 ACR（final 改写 Dockerfile）
                self._image.push(image_tar, docker_ref, overwrite=overwrite)
                rewrite_dockerfile(dockerfile, docker_ref, tar_role="final")
                image_pushed = True

            # ④ 上传 OSS（排除 image.tar.gz）；{id}.json 供 pull 校验 / ingest 扫描
            put = self._content.put(instance_id, dataset, version, split, tgz,
                                    meta.to_canonical_json(), overwrite=overwrite,
                                    layout=lay)
            _tgz_size = tgz.stat().st_size
        skipped = bool(put.get("skipped"))
        _upload_elapsed = _time.monotonic() - _t0 - _pack_elapsed
        if skipped:
            _tgz_size = 0
        logger.info("push %s: pack=%.1fs (%d bytes) upload=%.1fs skipped=%s",
                    instance_id, _pack_elapsed, _tgz_size,
                    _upload_elapsed, skipped)
        # 回读校验（防静默成功）：只在真正发生上传时校验对象已落库；镜像推送后校验可 inspect。
        if verify:
            if not skipped and not self._content.exists(
                    instance_id, dataset, version, split, layout=lay):
                raise TransportError(
                    f"{instance_id}: OSS 回读校验失败——上传后未在 OSS 找到 "
                    f"content.tgz/{{id}}.json")
            # ACR push 成功后 manifest 有秒级一致性延迟，立即 inspect 可能假 False，
            # 故回读校验带重试（retries=3），避免把"已推成功"误报成 push 失败。
            if image_pushed and not self._image.exists(docker_ref, retries=3):
                raise TransportError(
                    f"{instance_id}: ACR 回读校验失败——推送后未 inspect 到镜像 "
                    f"{docker_ref}")
        # ⑤ 写库：register=True 时经 ingest 扫描入库（替代缺失的 :commit 三段式收尾）。
        #    ingest 幂等（重扫 OSS），skip 与否都由服务端按 OSS 实际字节重算 digest，
        #    不再有「本地 digest 覆盖别家生产者」的 skip 分支歧义。
        ingest_result = self._after_upload(
            register, dataset, version, instance_id, split=split)
        digests = {"content.tgz": digest}
        return PushResult(instance_id=instance_id, uploaded=not skipped,
                          skipped=skipped, image_pushed=image_pushed,
                          docker_image=docker_ref or None,
                          digests=digests, ingest=ingest_result)

    def _push_swe(self, json_path: Path, dataset: str, version: str, *,
                  split: str = "default", overwrite: bool = False,
                  register: bool = False, verify: bool = True) -> PushResult:
        """推一个 SWE 格式实例：validate JSON → 上传 {id}.json → (可选)commit。

        SWE 格式的数据和元数据合一在单个 JSON 文件里，不打包 content.tgz，不推镜像。
        docker_image 是远端已存在的引用（由上游镜像构建流水线提前构建好）。
        推荐 register=False（默认）：只传 OSS，让 ingest 扫描入库。
        """
        report = check_swe_json(json_path)     # ① 校验（含 instance_id 安全检查）
        instance_id = report.instance_id
        docker_image = report.metadata.get("docker_image")

        # SWE JSON 内部的 split/dataset 与 push 参数冲突检测（参数优先，warn）
        json_split = report.raw_data.get("split")
        if json_split and json_split != split:
            logger.warning(
                "%s: JSON内部 split=%r 与 push 参数 split=%r 不一致，以参数为准",
                instance_id, json_split, split)
        json_dataset = report.raw_data.get("dataset")
        if json_dataset and json_dataset != dataset:
            logger.warning(
                "%s: JSON内部 dataset=%r 与 push 参数 dataset=%r 不一致，以参数为准",
                instance_id, json_dataset, dataset)

        # ② 上传 JSON 文件到 metadata_key 路径（SWE 只有这一个对象）
        lay = self._layout()
        idx_key = lay.metadata_key(dataset, instance_id, version=version, split=split)
        sts_prefix = lay.sts_prefix(dataset)
        raw_bytes = json_path.read_bytes()
        digest = "sha256:" + hashlib.sha256(raw_bytes).hexdigest()

        put = self._content.put_object(
            idx_key, raw_bytes, overwrite=overwrite,
            sts_prefix=sts_prefix, dataset=dataset)
        skipped = bool(put.get("skipped"))

        # ③ 回读校验
        if verify and not skipped:
            # dataset 必传：apiserver 按 dataset RBAC 签发 STS，缺了会 94020 拒签。
            # 这是真机踩到的缺陷——put_object 带了 dataset、回读却漏了，于是"上传成功但
            # 校验签不出凭据"，verify=True 必然失败。
            if not self._content.object_exists(idx_key, sts_prefix=sts_prefix,
                                               dataset=dataset):
                raise TransportError(
                    f"{instance_id}: OSS 回读校验失败——上传后未在 OSS 找到 {idx_key}")

        # ④ 写库：register=True 时经 ingest 扫描入库（替代缺失的 :commit 收尾）
        ingest_result = self._after_upload(
            register, dataset, version, instance_id, split=split)

        return PushResult(instance_id=instance_id, uploaded=not skipped,
                          skipped=skipped, image_pushed=False,
                          docker_image=docker_image or None,
                          digests={"instance.json": digest},
                          ingest=ingest_result)

    def _push_custom(self, local_path: Path, dataset: str, version: str, *,
                     split: str = "default", push_image: bool = True,
                     overwrite: bool = False, register: bool = True,
                     verify: bool = True,
                     content_hash: str | None = None) -> PushResult:
        """推一个 custom 格式实例：validate → (目录输入时) 上传资产 → 上传元数据 JSON。

        custom 格式的两种输入：

        - **目录**：SDK 生成最小元数据 JSON（``instance_id`` / ``metadata_model`` /
          ``schema_version`` / ``created_at`` / ``updated_at``）上传到 ``{split}/{id}.json``，
          目录内容**原样**逐文件上传到 ``{split}-assets/{id}/`` 前缀下（保持相对路径）。
        - **``.json`` 文件**：校验后**原样**上传到 ``{split}/{id}.json``（无资产）。

        custom 格式**不参与镜像流程**：``push_image=True`` 时告警并忽略（与 SWE 同口径）。
        """
        import datetime as _dt
        import warnings as _warnings

        if push_image:
            _warnings.warn(
                "custom 格式不支持 ACR 镜像推送（push_image=True 已忽略）；"
                "如需镜像请用 harbor 格式",
                UserWarning, stacklevel=3)

        report = check_custom(local_path)           # ① 校验（含 instance_id 安全检查）
        instance_id = report.instance_id
        lay = self._layout()
        idx_key = lay.metadata_key(dataset, instance_id, version=version, split=split)
        sts_prefix = lay.sts_prefix(dataset)

        if report.source == "json":
            # JSON 输入：原样上传
            raw_bytes = local_path.read_bytes()
            meta_digest = "sha256:" + hashlib.sha256(raw_bytes).hexdigest()
            put = self._content.put_object(
                idx_key, raw_bytes, overwrite=overwrite,
                sts_prefix=sts_prefix, dataset=dataset)
            skipped = bool(put.get("skipped"))
            asset_digests: dict[str, str] = {}
        else:
            # 目录输入：生成最小元数据 JSON + 原样上传资产
            now_iso = _dt.datetime.now(_dt.timezone.utc).isoformat(
                timespec="seconds").replace("+00:00", "Z")
            # 先枚举资产相对路径并写入元数据 ``assets`` 字段：pull 还原时据此逐对象
            # GetObject，免去 bucket LIST——普通用户的 dataset-RBAC STS 不含
            # oss:ListObjects，靠 LIST 枚举资产会 403/DatasetIdentifierRequired。
            asset_rels = sorted(
                child.relative_to(local_path).as_posix()
                for child in local_path.rglob("*") if child.is_file())
            meta_doc = {
                "instance_id": instance_id,
                "metadata_model": "custom",
                "schema_version": CUSTOM_SCHEMA_VERSION,
                "created_at": now_iso,
                "updated_at": now_iso,
                "assets": asset_rels,
            }
            if content_hash:
                meta_doc["extend_meta"] = {"source_hash": content_hash}
            raw_bytes = json.dumps(meta_doc, ensure_ascii=False).encode("utf-8")
            meta_digest = "sha256:" + hashlib.sha256(raw_bytes).hexdigest()

            # 原样上传目录内所有文件到资产目录（与 content.tgz 同层、同版本规则）
            asset_prefix = lay.assets_dir(dataset, instance_id,
                                          version=version, split=split)
            # 只有确实要发布新 source_hash（传了哈希且元数据将新写）时，才需要
            # 回读校验被跳过的资产；普通重复上传（无新哈希或元数据已存在）
            # 保持存在即跳过的行为，不引入额外下载。
            publish_new_hash = bool(content_hash) and (
                overwrite or not self._content.object_exists(
                    idx_key, sts_prefix=sts_prefix, dataset=dataset))
            asset_digests = {}
            assets_skipped = False
            for rel in asset_rels:
                child = local_path / rel
                key = asset_prefix + rel
                data = child.read_bytes()
                digest = "sha256:" + hashlib.sha256(data).hexdigest()
                asset_digests[rel] = digest
                aput = self._content.put_object(
                    key, data, overwrite=overwrite,
                    sts_prefix=sts_prefix, dataset=dataset)
                if bool(aput.get("skipped")):
                    assets_skipped = True  # 任一被 skip 即整体视为 skip
                    if not publish_new_hash:
                        continue
                    # skipped 只表示对象已存在，不代表内容一致（例如上次资产
                    # 上传失败留下的旧资产）。若与本地不一致却仍发布新
                    # source_hash，后续 skip_unchanged 会把旧资产误判为最新
                    # 内容，因此先回读校验，不一致即中止、不发布元数据。
                    with tempfile.TemporaryDirectory() as tmp:
                        try:
                            self._content.get_object(
                                key, Path(tmp) / "asset",
                                expected_digest=digest,
                                sts_prefix=sts_prefix, dataset=dataset)
                        except DigestMismatch as exc:
                            raise SchemaError(
                                f"{instance_id}: 资产 {rel} 远端内容与本地不一致，"
                                "overwrite=False 不能发布新的 source_hash；"
                                "请用 overwrite=True 重写整组内容"
                            ) from exc

            # 资产完整写入后才发布元数据：若先写带 source_hash 的 JSON 再传资产，
            # 资产失败会留下新哈希，ingest 收录后 skip_unchanged 会把缺资产的
            # 实例误判为未变化，跳过修复上传。
            put = self._content.put_object(
                idx_key, raw_bytes, overwrite=overwrite,
                sts_prefix=sts_prefix, dataset=dataset)
            skipped = bool(put.get("skipped")) or assets_skipped

        # ③ 回读校验（防静默成功）
        if verify and not skipped:
            if not self._content.object_exists(idx_key, sts_prefix=sts_prefix,
                                               dataset=dataset):
                raise TransportError(
                    f"{instance_id}: OSS 回读校验失败——上传后未在 OSS 找到 {idx_key}")

        # ④ 写库：register=True 时经 ingest 扫描入库（替代缺失的 :commit 收尾）
        ingest_result = self._after_upload(
            register, dataset, version, instance_id, split=split)

        return PushResult(instance_id=instance_id, uploaded=not skipped,
                          skipped=skipped, image_pushed=False,
                          docker_image=None,
                          digests={"instance.json": meta_digest},
                          ingest=ingest_result)

    # ── 上架前：把生产副本的 task.toml 指向生产镜像（本地重写，不触网）──────────
    def retarget_prod_content(self, local_dir, dataset: str, version: str,
                              split: str, target_ref: str, *,
                              tmp_root=None):
        """为上架生成「task.toml 指向 target_ref」的生产 content.tgz + {id}.json。

        运行期真正决定拉哪个镜像的是 ``content.tgz`` 里 ``task.toml`` 的
        ``[environment].docker_image``（不是元数据里的 ``docker_image`` 字段）。上架只逐字节
        复制 content.tgz，若不改写，生产副本的 task.toml 仍指向开发态 registry。这里在**上架
        阶段本地**改写并重打包，避免「先复制到生产再下载改写回传」的多一趟 I/O。

        步骤：复制目录 → 改写 task.toml → 重打包（排除 image.tar.gz）→ 重算 digest →
        重建带 target docker_image 与新 manifest 的 canonical ``{id}.json``。

        返回 ``(tgz_path, digest, meta_json, content_key, metadata_key)``。tgz_path 落在
        ``tmp_root`` 下（调用方负责在用完后清理该目录）。纯本地操作、不触网。
        """
        import shutil
        from ..tasktoml import set_docker_image

        src = Path(local_dir)
        report = check_layout(src)
        tag_values = (normalize_tag_values(report.metadata["tag_values"])
                      if report.metadata.get("tag_values") is not None else None)
        instance_id = report.instance_id
        lay = self._layout()

        work = Path(tempfile.mkdtemp(prefix="irepo_retarget_", dir=tmp_root))
        staged = work / instance_id
        shutil.copytree(src, staged)
        toml_path = staged / "task.toml"
        if not toml_path.is_file():
            raise TransportError(
                f"{instance_id}: 缺 task.toml，无法为上架改写镜像引用")
        new_text, _old = set_docker_image(toml_path.read_text(encoding="utf-8"),
                                          target_ref)
        toml_path.write_text(new_text, encoding="utf-8")

        tgz = work / "content.tgz"
        digest = pack(staged, tgz, exclude_image_tar=True)
        content_key = lay.content_key(dataset, instance_id,
                                      version=version, split=split)
        metadata_key = lay.metadata_key(dataset, instance_id,
                                        version=version, split=split)
        meta = DatasetInstance(
            instance_id=instance_id, dataset=dataset, dataset_version=version,
            split=split, docker_image=target_ref,
            difficulty=report.metadata.get("difficulty"),
            tags=_tags(report.metadata),
            tag_values=tag_values,
            manifest=_manifest(self._p.oss_bucket, dataset, version,
                               instance_id, split, digest, lay),
            instance_status="ready",
        )
        return (tgz, digest, meta.to_canonical_json(), content_key, metadata_key)

    @staticmethod
    def _normalize_batch_ids(instance_ids) -> list[str]:
        if isinstance(instance_ids, (str, bytes)):
            raise SchemaError("instance_ids must be a collection of strings")
        try:
            values = list(instance_ids)
        except TypeError as exc:
            raise SchemaError(
                "instance_ids must be a collection of strings") from exc
        normalized: list[str] = []
        for value in values:
            if not isinstance(value, str):
                raise SchemaError("instance_ids must contain only strings")
            iid = value.strip()
            if not iid:
                raise SchemaError("instance_ids must not contain empty IDs")
            validate_instance_id(iid, source="instances.ingest()")
            normalized.append(iid)
        return sorted(set(normalized))

    def ingest(self, dataset: str, version: str | None, instance_ids, *,
               split: str = "default", **ingest_kwargs) -> RegistrationReport:
        """Register selected IDs in sequential chunks of at most 100."""
        if ingest_kwargs.get("dry_run"):
            raise SchemaError(
                "incremental registration cannot use dry_run; "
                "registration must write metadata")
        selected = self._normalize_batch_ids(instance_ids)
        registration = RegistrationReport(selected_ids=selected)
        if not selected:
            return registration
        if self._ingester is None:
            raise SchemaError(
                "incremental ingest requires the Repo-injected ingest callback")

        def merge(report: IngestReport) -> None:
            registration.ingests.append(report)
            registration.job_status = report.job_status
            registration.completed.extend(report.completed)
            registration.pending.extend(report.pending)
            # A failed/canceled job cannot prove rollback. Keep report.failed only
            # as per-job diagnostics and never promote commit-unknown IDs into the
            # registration summary's definitive failed bucket.
            if not report.commit_unknown:
                registration.failed.extend(report.failed)
            registration.unknown.extend(report.unknown)
            registration.commit_unknown = (
                registration.commit_unknown or report.commit_unknown)

        callback_kwargs = dict(ingest_kwargs)
        callback_kwargs.pop("raise_on_failure", None)
        for offset in range(0, len(selected), 100):
            chunk = selected[offset:offset + 100]
            try:
                outcome = self._ingester(
                    dataset, version, split=split, instance_ids=chunk,
                    raise_on_failure=False, **callback_kwargs)
                report = (outcome if isinstance(outcome, IngestReport)
                          else IngestReport.from_job(outcome, chunk))
            except Exception as exc:
                from ..errors import JobFailed, RegistrationFailed
                authoritative = getattr(exc, "report", None)
                if isinstance(authoritative, IngestReport):
                    report = authoritative
                else:
                    raw_job = getattr(exc, "job", None)
                    if isinstance(exc, JobFailed):
                        status = (exc.status
                                  or ((raw_job or {}).get("status")
                                      if isinstance(raw_job, dict) else None)
                                  or "job_failed")
                    else:
                        status = "transport_error"
                    report = IngestReport(
                        job=raw_job, job_status=str(status).lower(),
                        selected_ids=list(chunk), unknown=list(chunk),
                        commit_unknown=True)
                merge(report)
                registration.not_submitted.extend(
                    selected[offset + len(chunk):])
                raise RegistrationFailed(
                    "incremental registration stopped; preserve the attached "
                    "report before retrying only unresolved IDs: "
                    f"{exc}", report=registration, cause=exc) from exc
            merge(report)
            if report.completed != chunk:
                registration.not_submitted.extend(selected[offset + len(chunk):])
                break
        return registration

    def _register_results(self, results, dataset: str, version: str,
                          split: str, **ingest_kwargs) -> RegistrationReport:
        successful = [r for r in results if isinstance(r, PushResult)]
        selected = [r.instance_id for r in successful]
        registration = self.ingest(
            dataset, version, selected, split=split, **ingest_kwargs)
        jobs_by_id = {
            iid: report.job
            for report in registration.ingests
            for iid in report.selected_ids
        }
        for result in successful:
            result.ingest = jobs_by_id.get(result.instance_id)
        return registration

    def push_many_with_report(self, local_dirs, dataset: str, version: str, *,
                              register: bool = False,
                              split: str = "default",
                              ingest_kwargs: dict | None = None,
                              **kwargs) -> PushManyReport:
        """Upload once and optionally register successful actual IDs by chunk."""
        results = self.push_many(
            local_dirs, dataset, version, register=False, split=split, **kwargs)
        registration = (self._register_results(
            results, dataset, version, split, **(ingest_kwargs or {}))
            if register else RegistrationReport())
        return PushManyReport(results=list(results), registration=registration)

    def push_many(self, local_dirs, dataset: str, version: str, *,
                  owner_reference: OwnerReference | str | None = None,
                  split: str = "default", push_image: bool = True,
                  overwrite: bool = False, register: bool = False,
                  verify: bool = True,
                  concurrency: int = 8, continue_on_error: bool = False,
                  image_release_dst_acr: str | None = None,
                  skip_unchanged: bool = False,
                  hash_func: "Callable | None" = None,
                  content_hashes: dict[str, str] | None = None,
                  progress_callback: "Callable | None" = None,
                  executor=None,
                  compress_level: int | None = None
                  ) -> list:
        """并发推一批实例（默认 register=False：只传 OSS，元数据随后由 ingest 扫描入库）。

        整批共用同一 ``sts_oss_prefix(dataset, version)`` 的 STS（先预热一次，
        后续线程命中缓存），把 N 次签发降到 ~1；线程池上限 ``concurrency`` 控并发。
        默认 ``continue_on_error=False``：任一实例失败即抛 ``ItemError``（fail-fast报告；
        已完成的远端写入不会回滚）；
        置 True 则不抛，返回列表中失败项以 ``ItemError`` 占位、成功项为 ``PushResult``，
        供上层（如 deliver）对成功子集继续 ingest 并单独汇报失败。结果按输入顺序。

        ``register=True``：整批上传后只选择完整成功（含skipped）的实际instance ID，
        去重后按最多100个分块串行注册；每个成功结果的 ``ingest`` 绑定所属chunk原始job。
        任一chunk非completed即停止，绝不退回全split扫描。

        ``owner_reference`` 整批共用同一来源引用（批量交付通常同源；需要逐实例不同来源时
        请自行循环 ``push``）。CLI 的 push / push-many / deliver 都把它设为必填——交付
        路径必须能追溯上游来源。

        ``skip_unchanged=True``：自动比对本地源文件哈希与远端 ``extend_meta.source_hash``，
        匹配则跳过 pack+upload。``hash_func`` 可自定义哈希函数（默认用
        ``content.compute_source_hash``）；``content_hashes`` 可直接提供
        ``{instance_id: hash}`` 映射跳过本地计算。

        ``progress_callback(completed, total, result_or_error)``：每个 case 完成时调用。

        ``executor``：外部 ``ThreadPoolExecutor``，传入时复用（不关闭）；
        为 None 时内部新建。

        ``compress_level``：gzip 压缩级别（1-9），透传给 ``pack()``。
        """
        input_dirs = list(local_dirs)
        dirs = list(input_dirs)
        result_slots: list[PushResult | ItemError | None] = [None] * len(input_dirs)
        active_indices = list(range(len(input_dirs)))

        # ── skip_unchanged：哈希比对 + 过滤 ──
        hashes_map: dict[str, str] = dict(content_hashes) if content_hashes else {}
        actual_ids: dict[str, str] = {}
        multi_step_paths: set[str] = set()
        if dirs and (skip_unchanged or hashes_map):
            # ID 必须来自与push相同的validate路径；Path.name对JSON输入会多出扩展名，
            # 对目录内容声明的ID也不具权威性。校验失败项留给push按原错误语义处理。
            # 显式 content_hashes 时即使 skip_unchanged=False 也要解析 ID，
            # 否则 _one 的 content_hash 会退化为 None。
            for d in dirs:
                try:
                    validated = self.validate(d)
                    actual_ids[str(Path(d))] = validated.instance_id
                    if getattr(validated, "config", {}).get("steps"):
                        multi_step_paths.add(str(Path(d)))
                except Exception:  # noqa: BLE001
                    continue
        if skip_unchanged and dirs:
            from ..content import compute_source_hash as _default_hash
            _hash_fn = hash_func or _default_hash
            # 1. 按实际ID计算本地哈希（未提供的）
            for d in dirs:
                iid = actual_ids.get(str(Path(d)))
                if iid and iid not in hashes_map:
                    try:
                        hashes_map[iid] = _hash_fn(str(d))
                    except Exception:  # noqa: BLE001
                        pass  # 哈希失败不阻断，视为"变化"
            # 2. 获取远端哈希
            try:
                remote_hashes = self.list_content_hashes(
                    dataset, version, split)
            except Exception:  # noqa: BLE001
                remote_hashes = {}
            # 3. 过滤：未变化结果直接写回原输入slot，其余项保留slot索引。
            remaining_dirs = []
            remaining_indices = []
            skipped_count = 0
            for index, d in enumerate(input_dirs):
                path_key = str(Path(d))
                iid = actual_ids.get(path_key)
                local_h = hashes_map.get(iid, "") if iid else ""
                remote_h = remote_hashes.get(iid, "") if iid else ""
                if path_key not in multi_step_paths and iid and local_h and local_h == remote_h:
                    result_slots[index] = PushResult(
                        instance_id=iid, uploaded=False, skipped=True,
                        image_pushed=False, docker_image=None,
                        digests={}, ingest=None)
                    skipped_count += 1
                else:
                    remaining_dirs.append(d)
                    remaining_indices.append(index)
            if skipped_count:
                logger.info("push_many: %d/%d unchanged (skipped)",
                            skipped_count, len(input_dirs))
            dirs = remaining_dirs
            active_indices = remaining_indices

        warm = getattr(self._content, "prewarm", None)
        if warm is not None:
            sts_prefix = self._layout().sts_prefix(dataset)
            try:
                warm(sts_prefix, dataset)
            except TypeError:
                warm(sts_prefix)
        if push_image and getattr(self._p, "acr_host", None):
            try:
                self._t.get_acr_credentials(self._p.acr_host)
            except Exception:  # noqa: BLE001
                pass

        def _one(d):
            iid = actual_ids.get(str(Path(d)))
            ch = hashes_map.get(iid) if iid else None
            return self.push(d, dataset, version,
                             owner_reference=owner_reference, split=split,
                             push_image=push_image, overwrite=overwrite,
                             register=False, verify=verify,
                             image_release_dst_acr=image_release_dst_acr,
                             content_hash=ch,
                             compress_level=compress_level)

        # ── 并发执行 + 进度回调 ──
        total = len(dirs)
        completed = [0]  # mutable counter for closure
        lock = __import__("threading").Lock()

        def _wrapped(d):
            result = _one(d)
            with lock:
                completed[0] += 1
                if progress_callback:
                    try:
                        progress_callback(completed[0], total, result)
                    except Exception:  # noqa: BLE001
                        pass
            return result

        if executor is not None:
            results = map_with_executor(
                _wrapped, dirs, executor=executor,
                return_exceptions=continue_on_error)
        else:
            results = map_concurrent(_wrapped, dirs, concurrency=concurrency,
                                     return_exceptions=continue_on_error)
        # Close retired OSS buckets after the batch to release connection pools.
        # Guard for non-OSS or mock stores that don't have close_retired.
        _close = getattr(self._content, "close_retired", None)
        if callable(_close):
            _close()
        for index, result in zip(active_indices, results):
            result_slots[index] = result
        combined = [result for result in result_slots if result is not None]
        # register=True 只选择完整成功的实际 instance_id；上传失败项不提交，
        # skipped 仍需补注册。分块、等待与逐项原始 job 绑定统一收敛在 _register_results。
        if register:
            self._register_results(combined, dataset, version, split)
        return combined

    def pull(self, dataset: str, version: str, instance_id: str, dest_dir,
             split: str = "default", *, verify: bool = True,
             fallback_to_oss: bool = True,
             path: str | None = None,
             environment: str | None = None) -> Path:
        """下载实例内容。自动检测格式：harbor 下载 content.tgz，swe 下载 {id}.json，
        custom 下载 {id}.json + assets 目录。

        格式判断优先级：
        1. verify=True 且 registry 有元数据 → 从 manifest 判断
           (有 tgz=harbor，仅 json=swe/custom，需进一步探测)
        2. 无元数据或 manifest 无法区分 swe/custom → 下载 metadata JSON 检查
           metadata_model 字段（custom → 下载 assets 目录；否则 swe）
        3. metadata JSON 不存在 → fallback 到 harbor（下载 content.tgz）
        4. dataset 未注册（92001）→ OSS 回退：list-only 枚举文件树 + 逐文件下载
           （仍走 DOWNLOAD 意图：仅私网，公网下载照旧禁止）

        ``environment`` selects metadata for this call: online/pre override the
        profile; None/auto retain it. Storage settings never change. OSS discovery
        fallback is disabled when an explicit online/pre environment does not
        match a known storage profile. None/auto (including an empty string)
        preserve the existing profile and fallback behavior. fallback_to_oss only
        controls registry-error discovery, not legacy content-format probing.

        ``path`` 参数用于部分下载（仅 custom 和 OSS 回退格式生效）：
        为空时下载全部内容；非空时只下载该路径前缀下的文件。
        harbor（content.tgz）和 swe（单 JSON）格式不支持部分下载，
        ``path`` 会被忽略。
        """
        # None/auto retain the profile's metadata environment and storage binding.
        # Explicit environments affect metadata reads only, including directory APIs.
        if environment is not None:
            if not isinstance(environment, str):
                raise SchemaError("environment must be online, pre or auto")
            environment = environment.strip().lower()
            if environment in ("", "auto"):
                environment = None
            elif environment not in ("online", "pre"):
                raise SchemaError("environment must be online, pre or auto")
        env = environment or getattr(self._p, "dataset_environment", None)
        bound_env = dataset_environment_for(getattr(self._p, "storage_env", None))
        # Explicit metadata selection may not silently discover bytes in another
        # (or unknown) store. The older registry-discovery switch is independent.
        scoped_storage_unavailable = environment is not None and environment != bound_env
        allow_fallback = fallback_to_oss and not scoped_storage_unavailable
        overrides = {"environment": environment} if environment is not None else {}

        def _ensure_oss_discovery_allowed() -> None:
            """Reject every unlocated OSS probe/LIST under the same environment gate."""
            if not scoped_storage_unavailable:
                return
            storage_env = getattr(self._p, "storage_env", None)
            storage_description = (
                f"{bound_env!r} (storage_env={storage_env!r})" if bound_env
                else f"unknown (storage_env={storage_env!r})")
            raise TransportError(
                f"OSS discovery is disabled for pull: requested metadata environment "
                f"{environment!r} does not match storage environment "
                f"{storage_description}; refusing format probing or object listing "
                f"without target-environment metadata")

        validate_instance_id(instance_id, source="pull()")
        expected = None
        fmt = None  # None = 未确定，需要探测
        dir_manifest = None  # manifest 中的 directory 条目（如有）
        lay = self._layout()
        # 已下载的元数据字节（探测阶段下载一次，swe/custom 路径复用，避免二次网络往返）。
        meta_bytes: bytes | None = None

        if verify:
            try:
                meta = self._reg.get(dataset, version, instance_id, split, **overrides)
            except TransportError as e:
                if (e.biz_code in (92001, 92023) and allow_fallback
                        and self._content is not None):
                    # 92001: dataset 未注册
                    # 92023: dataset 已注册但 split 在当前 environment 不存在
                    #        （如数据在 online 但 SDK 查了 pre）
                    # 两种情况均回退到 OSS 直接下载（私网 + 系统调用方语义）
                    return self._pull_unregistered(
                        dataset, version, instance_id, dest_dir, split,
                        path=path)
                raise
            if meta is None:
                _ensure_oss_discovery_allowed()
            if meta is not None and meta.manifest:
                has_tgz = False
                has_dir = False
                for m in meta.manifest:
                    if m.content_format == "tgz":
                        expected = m.content_digest
                        has_tgz = True
                        break
                    if m.content_type == "directory":
                        has_dir = True
                        dir_manifest = m
                if has_tgz:
                    fmt = "harbor"
                elif has_dir:
                    # manifest 同时有 json 和 directory 条目 → custom 格式
                    # （directory 条目指向 assets 目录，需逐文件下载）。
                    fmt = "custom"
                    for m in meta.manifest:
                        if m.content_format == "json":
                            expected = m.content_digest
                            break
                else:
                    # manifest 有 json entry 但无 tgz 也无 directory → swe 或 custom（需进一步探测）。
                    # custom 推的 manifest 由 ingest 扫描生成，与 swe 同形态；
                    # 唯一区分手段是读 metadata JSON 检查 metadata_model 字段。
                    for m in meta.manifest:
                        if m.content_format == "json":
                            fmt = "swe"  # 暂定 swe，后续探测可能修正为 custom
                            expected = m.content_digest
                            break

        # 无法从 manifest 确定 harbor → 探测 OSS 区分 swe/custom 或 fallback harbor。
        idx_key = lay.metadata_key(dataset, instance_id, version=version, split=split)
        sts_prefix = lay.sts_prefix(dataset)

        # ── 探测辅助：下载 metadata JSON 到临时文件并解析，区分 swe / custom ──
        def _probe_meta_json() -> bytes | None:
            """下载 metadata JSON 并返回字节；不存在或解析失败时返回 None。"""
            tmp_dest = Path(dest_dir) / f".{instance_id}.json.probe"
            tmp_dest.parent.mkdir(parents=True, exist_ok=True)
            try:
                self._content.get_object(
                    idx_key, tmp_dest, sts_prefix=sts_prefix, dataset=dataset)
                data = tmp_dest.read_bytes()
                return data
            except Exception:  # noqa: BLE001 — 下载失败视为不存在
                return None
            finally:
                tmp_dest.unlink(missing_ok=True)

        if fmt is None:
            # No target-environment locator: HEAD/GET format probing is discovery too.
            _ensure_oss_discovery_allowed()
            download_probe = getattr(self._content, "_download_probe", None)
            if download_probe is not None:
                exists = download_probe(
                    idx_key, sts_prefix=sts_prefix, dataset=dataset)
            else:
                exists = self._content.object_exists(
                    idx_key, sts_prefix=sts_prefix)
            if exists:
                # metadata JSON 存在 → 下载并解析以区分 swe / custom
                fmt = "swe"  # 默认；下载后可能修正为 custom
                probed = _probe_meta_json()
                if probed is not None:
                    meta_bytes = probed
                    try:
                        meta_doc = json.loads(meta_bytes)
                        if (isinstance(meta_doc, dict)
                                and meta_doc.get("metadata_model") == "custom"):
                            fmt = "custom"
                    except (json.JSONDecodeError, UnicodeDecodeError):
                        pass  # 无法解析 → 保持 swe
            else:
                fmt = "harbor"

        # 若 manifest 判定为 swe 但实际可能是 custom（两者 manifest 形态相同），
        # 下载 metadata JSON 做最终确认。
        if fmt == "swe" and meta_bytes is None:
            probed = _probe_meta_json()
            if probed is not None:
                meta_bytes = probed
                try:
                    meta_doc = json.loads(meta_bytes)
                    if (isinstance(meta_doc, dict)
                            and meta_doc.get("metadata_model") == "custom"):
                        fmt = "custom"
                except (json.JSONDecodeError, UnicodeDecodeError):
                    pass

        if fmt == "custom":
            dest = Path(dest_dir) / f"{instance_id}.json"
            if meta_bytes is not None:
                # 已在探测阶段下载，直接写入本地（避免二次网络往返）。
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(meta_bytes)
            else:
                self._content.get_object(
                    idx_key, dest, expected_digest=expected,
                    sts_prefix=sts_prefix, dataset=dataset)
                meta_bytes = dest.read_bytes()
            # 从元数据 ``assets`` 字段还原资产清单，逐对象 GetObject——普通用户的
            # dataset-RBAC STS 不含 oss:ListObjects，不能靠 LIST 枚举资产。
            # 旧数据无 ``assets`` 字段时 asset_rels=None，由下游回退到 LIST。
            asset_rels = None
            if meta_bytes is not None:
                try:
                    meta_doc = json.loads(meta_bytes)
                except (json.JSONDecodeError, UnicodeDecodeError):
                    meta_doc = None
                if isinstance(meta_doc, dict) and isinstance(
                        meta_doc.get("assets"), list):
                    asset_rels = [str(x) for x in meta_doc["assets"]]
            # manifest 有 directory 条目但 JSON 无 assets 字段时，
            # 用控制面 list_objects API 递归枚举目录下的全部文件作为 asset_rels。
            if asset_rels is None and dir_manifest is not None:
                try:
                    mm = getattr(self._p, "metadata_model", None)
                    # 递归列举：从根开始，遇到子目录继续深入
                    asset_rels = []
                    stack: list[str | None] = [None]  # None = 实例资产根
                    # 返回路径相对于 Dataset 根；去掉包含可选版本段的
                    # 实例资产前缀，才是相对于实例目录的下载路径。
                    split_str = (split or "default").strip()
                    assets_root = self._instance_assets_object_root(
                        dataset, instance_id, version, split_str, environment=env) + "/"
                    while stack:
                        cur_path = stack.pop()
                        objs = self.list_objects(
                            dataset, instance_id, split=split,
                            version=version, path=cur_path,
                            environment=env, metadata_model=mm)
                        for f in objs.files:
                            rel = f.path
                            if rel.startswith(assets_root):
                                rel = rel[len(assets_root):]
                            asset_rels.append(rel)
                        for d in objs.directories:
                            # directory path 也含完整前缀，去掉后入栈
                            d_path = d.path.rstrip("/")
                            if d_path.startswith(assets_root):
                                d_path = d_path[len(assets_root):]
                            stack.append(d_path)
                except Exception:  # noqa: BLE001
                    if scoped_storage_unavailable:
                        raise
                    asset_rels = None  # 枚举失败回退到 OSS LIST
            if asset_rels is None:
                # Legacy JSON without assets has no target-environment asset locator.
                _ensure_oss_discovery_allowed()
            self._download_custom_assets(
                dataset, instance_id, version, split, dest_dir, lay, sts_prefix,
                asset_rels=asset_rels, path=path)
            return dest

        if fmt == "swe":
            dest = Path(dest_dir) / f"{instance_id}.json"
            if meta_bytes is not None:
                # 已在探测阶段下载，直接写入本地。
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(meta_bytes)
            else:
                self._content.get_object(
                    idx_key, dest, expected_digest=expected,
                    sts_prefix=sts_prefix,
                    dataset=dataset)
            # swe 格式也可能附带 assets 目录（JSON + directory 混合格式）。
            # 尝试用 list_objects 检查并下载目录内容。
            try:
                objs = self.list_objects(
                    dataset, instance_id, split=split,
                    version=version,
                    environment=env,
                    metadata_model=getattr(self._p, "metadata_model", None))
                if objs.files or objs.directories:
                    # 有 assets 内容 → 递归枚举并下载
                    asset_rels: list[str] = []
                    stack: list[str | None] = [None]
                    split_str = (split or "default").strip()
                    assets_root = self._instance_assets_object_root(
                        dataset, instance_id, version, split_str, environment=env) + "/"
                    while stack:
                        cur = stack.pop()
                        page = self.list_objects(
                            dataset, instance_id, split=split,
                            version=version, path=cur,
                            environment=env,
                            metadata_model=getattr(self._p, "metadata_model", None))
                        for f in page.files:
                            rel = f.path
                            if rel.startswith(assets_root):
                                rel = rel[len(assets_root):]
                            asset_rels.append(rel)
                        for d in page.directories:
                            d_path = d.path.rstrip("/")
                            if d_path.startswith(assets_root):
                                d_path = d_path[len(assets_root):]
                            stack.append(d_path)
                    if asset_rels:
                        self._download_custom_assets(
                            dataset, instance_id, version, split,
                            dest_dir, lay, sts_prefix,
                            asset_rels=asset_rels, path=path)
            except Exception:  # noqa: BLE001
                if scoped_storage_unavailable:
                    raise
                pass  # assets 目录不存在或枚举失败 → 仅保留 JSON
            return dest

        # harbor：下载 content.tgz
        dest = Path(dest_dir) / instance_id / "content.tgz"
        return self._content.get(dataset, version, instance_id, split, dest,
                                 expected_digest=expected, layout=lay)

    def _download_custom_assets(self, dataset: str, instance_id: str,
                                version: str, split: str, dest_dir, lay,
                                sts_prefix: str,
                                asset_rels: list[str] | None = None,
                                path: str | None = None
                                ) -> list[Path]:
        """下载 custom 格式的资产目录（与 content.tgz 同层、同版本规则）。

        资产文件按相对路径还原到 ``{dest_dir}/{instance_id}/`` 下。返回已下载
        的本地文件路径列表。无资产时返回空列表（不报错）。

        ``asset_rels`` 为元数据 ``assets`` 字段记录的资产相对路径清单：非 None 时
        逐对象 GetObject 还原（普通用户的 dataset-RBAC STS 不含 oss:ListObjects，
        不能靠 LIST 枚举）；为 None（旧数据无该字段）时回退到 LIST 枚举。

        ``path`` 为子目录过滤（相对于资产根目录）：非空时仅下载该路径前缀下的文件。
        """
        asset_prefix = lay.assets_dir(dataset, instance_id,
                                       version=version, split=split)
        dest_root = Path(dest_dir) / instance_id
        downloaded: list[Path] = []
        # path 过滤：非空时只下载 rel 以 path 开头的文件
        path_prefix = ""
        if path:
            path_prefix = path.strip().strip("/") + "/"

        if asset_rels is not None:
            # 元数据记录了资产清单：逐对象下载，免 LIST。
            for rel in asset_rels:
                if rel.endswith("/"):
                    continue  # 目录占位符（push 侧不生成；兼容历史数据）
                if path_prefix and not rel.startswith(path_prefix):
                    continue  # path 过滤
                _validate_custom_asset_rel(rel)
                local_path = dest_root / rel
                local_path.parent.mkdir(parents=True, exist_ok=True)
                self._content.get_object(
                    asset_prefix + rel, local_path,
                    sts_prefix=sts_prefix, dataset=dataset)
                downloaded.append(local_path)
            return downloaded

        # 回退：旧数据无 assets 清单，用 LIST 枚举（仅 system 调用方有 LIST 权限）。
        list_fn = getattr(self._content, "list_objects", None)
        if list_fn is None:
            return []
        # path 非空时，LIST 直接用子前缀缩小范围
        list_prefix = asset_prefix + path_prefix if path_prefix else asset_prefix
        keys = list_fn(list_prefix, list_only=True, dataset=dataset)
        if not keys:
            return []
        for key in keys:
            rel = key[len(asset_prefix):]
            if rel.endswith("/"):
                continue  # 目录占位符（push 侧不生成；兼容历史数据）
            _validate_custom_asset_rel(rel)
            local_path = dest_root / rel
            local_path.parent.mkdir(parents=True, exist_ok=True)
            self._content.get_object(
                key, local_path,
                sts_prefix=sts_prefix, dataset=dataset)
            downloaded.append(local_path)
        return downloaded

    def _pull_unregistered(self, dataset: str, version: str,
                           instance_id: str, dest_dir, split: str,
                           path: str | None = None) -> Path:
        """未注册 dataset 的 pull 回退：list-only 枚举文件树 + 逐文件下载。

        下载仍走 :meth:`~instance_repo.store.oss.OssContentStore.get_object`
        的 DOWNLOAD 意图——**仅私网可用，公网下载照旧被拒**（与注册路径一致）。

        STS 语义：未注册 dataset 无 RBAC 记录，GetObject STS 仅 system 白名单
        调用方可签发（非 system 调用方在签发阶段收到明确错误），与历史行为一致。

        ``path`` 为子目录过滤（相对于实例资产根目录）：非空时仅下载该路径前缀下的文件。

        产物结构（harbor 同层，便于 CLI 整体搬移）::

            {dest_dir}/{instance_id}/{instance_id}.json     # metadata
            {dest_dir}/{instance_id}/<assets 相对路径>      # assets 文件
            {dest_dir}/{instance_id}/report/<report 相对路径>  # report 文件

        Returns the metadata JSON 本地路径。
        """
        from ..store.oss_discovery import discover_instance_file_tree

        tree = discover_instance_file_tree(
            self._content, dataset, version, instance_id, split,
            oss_prefix=self._oss_prefix)
        if tree is None:
            from ..errors import DatasetNotFound
            bucket = getattr(self._p, "oss_bucket", "") or ""
            from .config import dataset_environment_for
            env = dataset_environment_for(
                getattr(self._p, "storage_env", "")) or ""
            raise DatasetNotFound(
                f"instance {instance_id!r} not found in OSS bucket "
                f"{bucket!r} (environment={env or 'unknown'!r}) for "
                f"dataset {dataset!r}; the data may be registered in a "
                f"different storage environment — select a cluster whose "
                f"storage_env matches the dataset's environment")

        metadata_key, files = tree
        dest_root = Path(dest_dir) / instance_id
        dest_root.mkdir(parents=True, exist_ok=True)
        metadata_dest = dest_root / f"{instance_id}.json"

        self._content.get_object(metadata_key, metadata_dest, dataset=dataset)
        # path 过滤：非空时只下载 rel 以 path 开头的文件
        path_prefix = ""
        if path:
            path_prefix = path.strip().strip("/") + "/"
        for key, rel in files:
            if path_prefix and not rel.startswith(path_prefix):
                continue
            local_path = dest_root / rel
            local_path.parent.mkdir(parents=True, exist_ok=True)
            self._content.get_object(key, local_path, dataset=dataset)
        return metadata_dest

    def pull_many(self, instance_ids: list[str], dataset: str, version: str,
                  dest_dir, *, split: str = "default",
                  concurrency: int = 8, continue_on_error: bool = False,
                  verify: bool = True) -> list[Path]:
        """Batch-download instances concurrently (parallel counterpart of :meth:`pull`).

        Uses :func:`map_concurrent` to download up to *concurrency* instances in
        parallel.  Results preserve input order.

        Parameters
        ----------
        instance_ids:
            Instance IDs to download.
        dataset, version, split:
            Dataset coordinates (same semantics as :meth:`pull`).
        dest_dir:
            Root directory under which each instance is materialised.
        concurrency:
            Maximum number of parallel downloads (default 8).
        continue_on_error:
            ``False`` (default) — first failure raises ``ItemError``; completed downloads are retained.
            ``True`` — failures are captured as ``ItemError`` placeholders in the
            returned list; successful entries contain the downloaded :class:`Path`.
        verify:
            When ``True`` (default), validate content digest against registry
            metadata (see :meth:`pull`).

        Returns
        -------
        list[Path]
            Downloaded paths in the same order as *instance_ids*.
            When *continue_on_error* is ``True``, failed entries are
            ``ItemError`` instances instead of paths.
        """
        ids = list(instance_ids)
        if not ids:
            return []
        dest = Path(dest_dir)

        def _one(iid):
            return self.pull(dataset, version, iid, dest,
                             split=split, verify=verify)

        return map_concurrent(_one, ids, concurrency=concurrency,
                              return_exceptions=continue_on_error)


def _tags(metadata: dict) -> dict:
    t = metadata.get("tags", {})
    if isinstance(t, dict):
        return {str(k): str(v) for k, v in t.items()}
    if isinstance(t, list):
        return {str(v): "" for v in t}
    return {}


def _manifest(bucket, dataset, version, instance_id, split, digest, layout):
    return [
        ManifestEntry(
            file_path=P.oss_uri(bucket, layout.metadata_key(
                dataset, instance_id, version=version, split=split)),
            content_type="file", content_format="json"),
        ManifestEntry(
            file_path=P.oss_uri(bucket, layout.content_key(
                dataset, instance_id, version=version, split=split)),
            content_type="file", content_format="tgz", content_digest=digest),
    ]


def _manifest_without_digest(manifest):
    """返回去掉 content_digest 的 manifest 副本（不改原对象）。

    用于 put 被 skip 的分支：OSS 上是别的生产者写的字节，我们无权断言其 digest。
    必须做副本——原 manifest 已序列化进 OSS {id}.json，就地改会污染那份元数据。
    与 Go 的 manifestWithoutDigest 对齐。
    """
    import dataclasses
    return [dataclasses.replace(m, content_digest=None) for m in manifest]
