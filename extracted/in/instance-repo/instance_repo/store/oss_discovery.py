"""store/oss_discovery.py -- OSS metadata discovery for unregistered datasets.

When a dataset is not registered in MongoDB but exists in OSS storage, this module
discovers the version/split/instance structure by probing the OSS directory layout
defined in :mod:`instance_repo.paths`.

Core entry point: :func:`parse_dataset_level` performs a 2-level LIST to derive
version and split information.  The ``build_synthetic_*`` helpers convert the raw
discovery result into the SDK's standard dataclass types (with ``registered=False``
to mark the OSS-only provenance).
"""
from __future__ import annotations

import json
import logging
from dataclasses import dataclass

from .. import paths as P
from ..errors import DatasetNotFound, PrivateNetworkRequired, TransportError
from ..models import (
    DatasetDetail,
    DatasetDetailStats,
    DatasetInstance,
    DatasetSplit,
    DatasetVersion,
    ManifestEntry,
    PagedResult,
    SplitManifest,
)

logger = logging.getLogger(__name__)

# Maximum size of a single metadata JSON object we are willing to read (10 MB).
# Larger objects are silently skipped to prevent OOM on malformed uploads.
_MAX_JSON_BYTES = 10 * 1024 * 1024


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class LevelGroup:
    """Grouped directory entries at a single OSS level (version or split).

    Names ending with ``-assets`` or ``-report`` are folded into the same
    group as their base name, with the corresponding flag set.
    """
    name: str
    has_dir: bool = False
    has_assets: bool = False
    has_report: bool = False


@dataclass
class OssVersionInfo:
    """Structural information about one version discovered from OSS."""
    version: str
    has_three_layer_content: bool
    splits: list[str]
    has_default_instances: bool
    instance_count: int
    # default split（3 层布局）的直接 .json 数，与 instance_count（含命名 split）区分
    default_instance_count: int = 0


@dataclass
class OssUnversionedSplit:
    """split_first 无版本布局：dataset 根下直接是 split 目录（无 version 层）。"""
    name: str
    has_assets: bool          # 同层 {name}-assets/ 存在（split 级 content）
    instance_count: int       # {name}/ 下直接 .json 数


@dataclass
class OssDatasetLevelInfo:
    """Overall dataset structure discovered from OSS directory layout."""
    dataset: str
    versions: list[OssVersionInfo]
    total_instance_count: int
    truncated: bool = False
    # split_first 无版本布局下的 split（version="" 语义）
    unversioned_splits: list[OssUnversionedSplit] = None  # type: ignore[assignment]

    def __post_init__(self):
        if self.unversioned_splits is None:
            self.unversioned_splits = []


# ---------------------------------------------------------------------------
# Helper functions
# ---------------------------------------------------------------------------

def _group_level_names(names: list[str]) -> dict[str, LevelGroup]:
    """Group same-level directory names by ``-assets`` / ``-report`` suffix.

    Names ending with ``-assets`` are folded into the base name with
    ``has_assets=True``; names ending with ``-report`` set ``has_report=True``;
    all other names set ``has_dir=True``.  Flags for the same base name are
    merged into a single :class:`LevelGroup`.

    When a suffixed name has no corresponding base-name directory, it is
    treated as a standalone entry (the full name including suffix becomes
    the group name).  This handles the edge case where a version name
    legitimately ends with ``-assets`` or ``-report``.
    """
    groups: dict[str, LevelGroup] = {}

    for name in names:
        if name.endswith("-assets"):
            base = name[:-7]  # len("-assets") == 7
            if base in groups:
                groups[base].has_assets = True
            else:
                # Standalone: no base dir seen (yet).
                groups[name] = LevelGroup(name=name, has_assets=True)
        elif name.endswith("-report"):
            base = name[:-7]  # len("-report") == 7
            if base in groups:
                groups[base].has_report = True
            else:
                groups[name] = LevelGroup(name=name, has_report=True)
        else:
            if name in groups:
                groups[name].has_dir = True
            else:
                # Check if standalone suffixed entries were created earlier
                # and consolidate them under this base name.
                merged = LevelGroup(name=name, has_dir=True)
                assets_key = name + "-assets"
                report_key = name + "-report"
                if assets_key in groups:
                    old = groups.pop(assets_key)
                    merged.has_assets = old.has_assets
                    merged.has_report = merged.has_report or old.has_report
                if report_key in groups:
                    old = groups.pop(report_key)
                    merged.has_report = old.has_report
                    merged.has_assets = merged.has_assets or old.has_assets
                groups[name] = merged

    return groups


def _in_memory_paged(items: list, page: int, page_size: int) -> PagedResult:
    """Create a :class:`PagedResult` from an in-memory list with client-side paging."""
    total = len(items)
    if page_size <= 0:
        page_size = 50
    start = (page - 1) * page_size
    end = start + page_size
    return PagedResult(
        items=items[start:end],
        total=total,
        page=page,
        page_size=page_size,
        has_more=end < total,
    )


def _empty_paged_result(page: int, page_size: int) -> PagedResult:
    """Return an empty :class:`PagedResult`."""
    if page_size <= 0:
        page_size = 50
    return PagedResult(
        items=[],
        total=0,
        page=page,
        page_size=page_size,
        has_more=False,
    )


def _direct_json_keys(all_keys: list[str], prefix: str) -> list[str]:
    """Filter *all_keys* for ``.json`` files directly under *prefix* (not nested)."""
    return [
        k for k in all_keys
        if k.endswith(".json") and "/" not in k[len(prefix):]
    ]


def _dataset_base(dataset: str, version: str, prefix: str) -> str:
    """Return a dataset/version base without a trailing slash."""
    root = P.DatasetName.parse(dataset).relative_root(prefix).removesuffix("/")
    return f"{root}/{version}" if version else root


# ---------------------------------------------------------------------------
# Core discovery
# ---------------------------------------------------------------------------

def parse_dataset_level(
    content_store,
    dataset: str,
    *,
    oss_prefix: str = "swe/datasets",
    max_versions: int = 500,
    metadata_model: str = "split_first",
) -> OssDatasetLevelInfo:
    """Discover version/split structure from OSS directory layout.

    Performs ``1 + min(N, max_versions)`` LIST calls where *N* is the number
    of Level 1 entries; the per-group probes run concurrently (16-way).

    语义消歧（``metadata_model``）：
    - ``split_first``（SDK 默认）：level-1 目录 `X/` 下**只有 .json、无子目录**
      时，`X` 是无版本 split（`{split}/{id}.json` 契约形态）；含子目录时是
      version（子目录为其 split）。
    - ``version_first``（显式切换）：level-1 目录一律视为 version（旧行为）。

    Args:
        content_store: :class:`~instance_repo.store.oss.OssContentStore` instance.
        dataset: Canonical dataset name with one or more segments.
        oss_prefix: Root prefix inside the bucket (default ``"swe/datasets"``).
        max_versions: Upper bound on the number of versions to probe.  When
            exceeded the result is truncated and ``truncated=True`` is set.
        metadata_model: ``split_first``（默认）or ``version_first``；决定
            level-1 目录的语义归属（见上）。

    Returns:
        :class:`OssDatasetLevelInfo` with the discovered version/split tree.

    Raises:
        DatasetNotFound: The OSS prefix contains no objects or no recognisable
            version/split structure.
    """
    from ..errors import SchemaError
    if type(max_versions) is not int or not 1 <= max_versions <= 500:
        raise SchemaError("max_versions must be an integer between 1 and 500")
    root = f"{_dataset_base(dataset, '', oss_prefix)}/"

    # -- Level 1: list immediate children under the dataset root -----------
    try:
        level1_names, level1_all_keys = content_store.list_level(
            root, list_only=True, dataset=dataset)
    except TransportError as e:
        if e.status == 403:
            # OSS fallback requires ListObjects permission, which is only granted
            # to system callers (admin API keys) or users with dataset RBAC roles.
            # For unregistered datasets, there's no RBAC record, so only system
            # callers can list. Non-admin users see a 403 here.
            raise DatasetNotFound(
                f"dataset {dataset!r} not found in MongoDB; OSS fallback requires "
                f"admin privileges (system_api_keys whitelist). Contact your "
                f"administrator to query unregistered datasets."
            ) from e
        raise
    level1_json_keys = _direct_json_keys(level1_all_keys, root)

    if not level1_names and not level1_json_keys:
        raise DatasetNotFound(
            f"dataset {dataset!r} not found in OSS under {root!r}"
        )

    # -- Group level 1 names into candidates -------------------------------
    l1_groups = _group_level_names(level1_names)

    if not l1_groups:
        if level1_json_keys:
            # 实例 .json 直接位于 dataset 根下（无 version/split 层）是**非法布局**：
            # paths.py 契约要求 metadata 至少带 version 层（version_first）或
            # split 层（split_first）。不兼容识别，明确报错引导上传方修正。
            raise DatasetNotFound(
                f"dataset {dataset!r} exists in OSS but has no recognizable "
                f"version/split structure: {len(level1_json_keys)} .json file(s) "
                f"directly under {root!r} (expected {root!r}{{version}}/[{{split}}/] "
                f"layout per paths.py contract)")
        raise DatasetNotFound(
            f"dataset {dataset!r} exists in OSS but has no recognizable "
            f"version/split structure under {root!r}"
        )

    # Sort for deterministic output.
    names = sorted(l1_groups.keys())

    # -- Truncation protection ---------------------------------------------
    truncated = False
    if len(names) > max_versions:
        names = names[:max_versions]
        truncated = True

    split_first = (metadata_model or "split_first") != "version_first"

    # -- Level 2: probe each candidate (concurrent) ------------------------
    # 每个 group 的完整分析（level-2 列举 + 逐 split 计数）都在 probe 内完成，
    # 使大 version 数数据集的探测全程并行，避免串行逐 split 计数拖慢整链。
    def probe(name: str):
        """分析单个 level-1 group，返回 OssVersionInfo / OssUnversionedSplit。"""
        grp = l1_groups[name]
        group_dir = f"{root}{name}/"
        level2_names, level2_keys = content_store.list_level(
            group_dir, list_only=True, dataset=dataset)
        l2_groups = _group_level_names(level2_names)
        direct_json = _direct_json_keys(level2_keys, group_dir)
        subdirs = [g for g in l2_groups.values() if g.has_dir or g.has_assets]

        # split_first 无版本布局：`{name}/` 下只有 .json、无子目录 →
        # 无版本 split（contract: {split}/{id}.json + {split}-assets/）。
        if split_first and grp.has_dir and not subdirs and direct_json:
            return OssUnversionedSplit(
                name=name,
                has_assets=grp.has_assets,
                instance_count=len(direct_json),
            )

        # version 路径（version_first 或含子目录的 split_first 形态）。
        splits: list[str] = sorted(g.name for g in subdirs)
        instance_count = len(direct_json)
        for s_name in splits:
            split_dir = f"{group_dir}{s_name}/"
            _s_dirs, s_keys = content_store.list_level(
                split_dir, list_only=True, dataset=dataset)
            instance_count += len(_direct_json_keys(s_keys, split_dir))
        return OssVersionInfo(
            version=name,
            has_three_layer_content=grp.has_assets,
            splits=splits,
            has_default_instances=len(direct_json) > 0,
            instance_count=instance_count,
            default_instance_count=len(direct_json),
        )

    # A failed probe is not an empty directory or zero instances. Propagate the
    # failure rather than replaying all probes or reporting a complete snapshot.
    from ..concurrency import map_concurrent
    results = map_concurrent(probe, names, concurrency=16)

    versions: list[OssVersionInfo] = []
    unversioned_splits: list[OssUnversionedSplit] = []
    total_instance_count = 0

    for entry in results:
        if isinstance(entry, OssUnversionedSplit):
            unversioned_splits.append(entry)
            total_instance_count += entry.instance_count
        else:
            versions.append(entry)
            total_instance_count += entry.instance_count

    return OssDatasetLevelInfo(
        dataset=dataset,
        versions=versions,
        total_instance_count=total_instance_count,
        truncated=truncated,
        unversioned_splits=unversioned_splits,
    )


def _warn_if_truncated(info: OssDatasetLevelInfo, dataset: str, max_versions: int) -> None:
    """Log a warning if parse_dataset_level results were truncated."""
    if info.truncated:
        import logging
        logging.getLogger(__name__).warning(
            "dataset %r has more than %d level-1 entries; OSS discovery results "
            "are truncated (showing %d of >%d)",
            dataset, max_versions,
            len(info.versions) + len(info.unversioned_splits), max_versions)


# ---------------------------------------------------------------------------
# JSON reading helper
# ---------------------------------------------------------------------------

def _read_json_object(content_store, key: str) -> dict:
    """Best-effort read and parse of a JSON object from OSS.

    Performs a HEAD check first: if ``Content-Length`` exceeds 10 MB the object
    is skipped (returns ``{}``) to prevent OOM on malformed uploads.  Any other
    failure (network, parse error, missing key) also returns ``{}``.
    """
    try:
        # Use the internal _execute_oss to do a HEAD and check size.
        def _head_and_read(bucket):
            # HEAD to check size.
            head = bucket.head_object(key)
            content_length = getattr(head, "content_length", 0)
            if content_length and content_length > _MAX_JSON_BYTES:
                logger.warning(
                    "Skipping oversized JSON object %s (%d bytes)",
                    key, content_length,
                )
                return {}
            # Read body.
            result = bucket.get_object(key)
            body = result.read()
            return json.loads(body)

        from .._routing import _OperationIntent
        return content_store._execute_oss(
            _OperationIntent.DOWNLOAD, key, None, _head_and_read)
    except PrivateNetworkRequired:
        logger.warning(
            "Cannot read instance metadata JSON (private network required): %s",
            key)
        return {}
    except Exception:
        logger.debug("Failed to read JSON object %s", key, exc_info=True)
        return {}


# ---------------------------------------------------------------------------
# Synthetic builders
# ---------------------------------------------------------------------------

def build_synthetic_dataset_detail(
    dataset: str,
    info: OssDatasetLevelInfo,
    *,
    storage_env: str | None = None,
) -> DatasetDetail:
    """Build a :class:`DatasetDetail` from OSS discovery (``registered=False``)."""
    name = P.DatasetName.parse(dataset)
    all_splits: set[str] = set()
    total_instances = 0
    for v in info.versions:
        for s in v.splits:
            all_splits.add(s)
        if v.has_default_instances:
            all_splits.add("default")
        total_instances += v.instance_count
    # split_first 无版本布局：level-1 目录即 split
    for us in info.unversioned_splits:
        all_splits.add(us.name)
        total_instances += us.instance_count

    available_envs: list[str] = [storage_env] if storage_env else []

    return DatasetDetail(
        dataset_name=name.canonical,
        dataset_l1=name.l1,
        dataset_l2=name.l2,
        dataset_id="",
        version_count=len(info.versions),
        split_count=len(all_splits),
        latest_version=info.versions[-1].version if info.versions else None,
        stats=DatasetDetailStats(
            instance_count=total_instances,
            file_count=0,
            size_bytes=0,
        ),
        available_envs=available_envs,
        registered=False,
    )


def build_synthetic_version(
    dataset: str,
    v_info: OssVersionInfo,
) -> DatasetVersion:
    """Build a :class:`DatasetVersion` from OSS discovery (``registered=False``)."""
    splits_dicts: list[dict] = []
    for s in v_info.splits:
        splits_dicts.append({
            "name": s,
            "oss_prefix": f"{v_info.version}/{s}",
            "is_default": False,
        })
    if v_info.has_default_instances:
        splits_dicts.insert(0, {
            "name": "default",
            "oss_prefix": v_info.version,
            "is_default": True,
        })

    return DatasetVersion(
        version=v_info.version,
        dataset=dataset,
        status="draft",
        storage_path=f"{_dataset_base(dataset, v_info.version, P.DEFAULT_PREFIX)}/",
        split_count=len(splits_dicts),
        instance_count=v_info.instance_count,
        splits=splits_dicts,
        registered=False,
    )


def build_synthetic_split(
    dataset: str,
    version: str,
    split_name: str,
    *,
    has_assets: bool = False,
    instance_count: int = 0,
) -> DatasetSplit:
    """Build a :class:`DatasetSplit` from OSS discovery (``registered=False``)."""
    base = _dataset_base(dataset, version, P.DEFAULT_PREFIX)
    if split_name == "default":
        storage_path = f"{base}/"
    else:
        storage_path = f"{base}/{split_name}/"

    return DatasetSplit(
        dataset=dataset,
        version=version,
        name=split_name,
        status="draft",
        storage_type="oss",
        storage_path=storage_path,
        manifest=SplitManifest(instance_count=instance_count),
        projected=False,
        registered=False,
    )


def _metadata_prefix(dataset: str, version: str, split: str | None,
                     oss_prefix: str) -> str:
    """拼接 metadata 列举前缀；version 为空时表示 split_first 无版本布局。"""
    base = _dataset_base(dataset, version, oss_prefix)
    if split and split != "default":
        return f"{base}/{split}/"
    return f"{base}/"


def build_synthetic_instances(
    content_store,
    dataset: str,
    version: str,
    split: str | None = None,
    *,
    oss_prefix: str = "swe/datasets",
    read_content: bool = False,
) -> list[DatasetInstance]:
    """List and build :class:`DatasetInstance` objects from OSS metadata JSONs.

    For each ``{instance_id}.json`` found directly under the target prefix, a
    ``DatasetInstance`` is constructed.  ``read_content=True`` 时尝试读 JSON
    回填 tags/difficulty/docker_image；默认 False——发现模式（list-only STS）
    无 GetObject，逐实例 GET 必然失败，跳过可省 N 次无谓的 STS 签发与下载。
    """
    metadata_prefix = _metadata_prefix(dataset, version, split, oss_prefix)

    all_keys = content_store.list_objects(
        metadata_prefix, list_only=True, dataset=dataset)
    json_keys = _direct_json_keys(all_keys, metadata_prefix)

    instances: list[DatasetInstance] = []
    for key in json_keys:
        instance_id = key.rsplit("/", 1)[-1].removesuffix(".json")
        inst = DatasetInstance(
            instance_id=instance_id,
            dataset=dataset,
            dataset_version=version,
            split=split or "default",
            registered=False,
        )
        if read_content:
            data = _read_json_object(content_store, key)
            if data:
                inst.tags = data.get("tags", {})
                inst.difficulty = data.get("difficulty")
                inst.docker_image = data.get("docker_image")
                inst.extend_meta = data.get("extend_meta", {})
        instances.append(inst)

    return instances


def _instance_dir(dataset: str, version: str, split: str | None,
                  instance_id: str, suffix: str, oss_prefix: str) -> str:
    """拼接实例的 -assets/-report 目录；version 为空表示无版本 split 布局。"""
    base = _dataset_base(dataset, version, oss_prefix)
    if split and split != "default":
        return f"{base}/{split}-{suffix}/{instance_id}/"
    return f"{base}-{suffix}/{instance_id}/"


def _format_from_key(key: str) -> str:
    if key.endswith(".jsonl"):
        return "jsonl"
    if key.endswith(".json"):
        return "json"
    if key.endswith((".tgz", ".tar.gz")):
        return "tgz"
    return ""


def discover_instance_file_tree(
    content_store,
    dataset: str,
    version: str,
    instance_id: str,
    split: str | None,
    *,
    oss_prefix: str,
) -> tuple[str, list[tuple[str, str]]] | None:
    """用 LIST 枚举实例的完整文件树（发现模式，list-only STS）。

    Returns ``(metadata_key, files)`` where *files* is a list of
    ``(oss_key, rel_path)`` tuples covering ``{split}-assets/{id}/`` 与
    ``{split}-report/{id}/`` 下的所有对象。*rel_path* 相对实例根（assets
    文件为原相对路径，report 文件加 ``report/`` 前缀避免与 assets 同名冲突）。

    实例不存在（metadata .json 的精确 key LIST 未命中）时返回 ``None``。
    """
    if version:
        metadata_key = P.metadata_key(
            dataset, version, instance_id, split, prefix=oss_prefix)
    else:
        base = _dataset_base(dataset, "", oss_prefix)
        metadata_key = (f"{base}/{split}/{instance_id}.json"
                        if split and split != "default"
                        else f"{base}/{instance_id}.json")

    # 存在性判定用 LIST（list-only STS 无 GetObject，不能 HEAD）。
    # 不能用「prefix=精确 key」的 LIST：OSS 的 prefix 过滤是字符串前缀语义，
    # 且 RAM 条件只放行 {parent}/*（精确 key 会带出同前缀兄弟对象，见 apiserver
    # sts/client.go），改为父目录 LIST + 客户端成员判断。
    parent = metadata_key.rsplit("/", 1)[0] + "/"
    try:
        if metadata_key not in content_store.list_objects(
                parent, list_only=True, dataset=dataset):
            return None
    except Exception:  # noqa: BLE001
        return None

    files: list[tuple[str, str]] = []
    for suffix, rel_prefix in (("assets", ""), ("report", "report/")):
        dir_prefix = _instance_dir(dataset, version, split, instance_id,
                                   suffix, oss_prefix)
        try:
            for k in content_store.list_objects(
                    dir_prefix, list_only=True, dataset=dataset):
                if k.endswith("/") or not k.startswith(dir_prefix):
                    continue  # 目录标记 / 异常 key
                rel = rel_prefix + k[len(dir_prefix):]
                files.append((k, rel))
        except Exception:  # noqa: BLE001, S110
            pass  # best-effort：无 assets/report 目录时忽略
    return metadata_key, files


def _instance_manifest(
    content_store,
    dataset: str,
    version: str,
    instance_id: str,
    split: str | None,
    metadata_key: str,
    *,
    oss_prefix: str,
) -> list[ManifestEntry]:
    """用 LIST 枚举实例的文件结构（metadata + {split}-assets + {split}-report）。

    发现模式（list-only STS）无 GetObject，读不到 metadata JSON 内容，但目录
    结构可通过 LIST 完整呈现——恰好满足「查看实例的目录文件结构」需求。
    """
    tree = discover_instance_file_tree(
        content_store, dataset, version, instance_id, split,
        oss_prefix=oss_prefix)
    if tree is None:
        return []
    _meta_key, files = tree
    keys = [_meta_key] + [k for k, _ in files]
    bucket = getattr(content_store, "bucket_name", "") or ""
    return [
        ManifestEntry(
            file_path=f"oss://{bucket}/{k}" if bucket else k,
            content_type="file",
            content_format=_format_from_key(k),
            object_path=k,
        )
        for k in keys
    ]


def build_synthetic_instance(
    content_store,
    dataset: str,
    version: str,
    instance_id: str,
    split: str | None = None,
    *,
    oss_prefix: str = "swe/datasets",
    read_content: bool = False,
    include_files: bool = True,
) -> DatasetInstance | None:
    """Build a single :class:`DatasetInstance` by exact key lookup in OSS.

    Returns ``None`` if the metadata JSON does not exist.  ``read_content``
    语义同 :func:`build_synthetic_instances`（发现模式默认跳过 JSON 回填）。

    ``include_files``（默认 True）用 LIST 枚举实例文件结构（metadata + assets
    + report 目录）回填 ``manifest``——文件名为真实值，digest/大小留空
    （list-only STS 无 GetObject）。仅 instance get 单条路径开启，避免列表
    路径 N 倍 LIST 开销。
    """
    if version:
        key = P.metadata_key(
            dataset, version, instance_id, split, prefix=oss_prefix)
    else:
        # split_first 无版本布局：{split}/{id}.json（split=None/default 不合
        # 此形态，调用方须传真实 split 名）
        base = _dataset_base(dataset, "", oss_prefix)
        key = (f"{base}/{split}/{instance_id}.json"
               if split and split != "default"
               else f"{base}/{instance_id}.json")

    # 存在性判定用 LIST（list_only=True 仅需 ListObjects）而非 HEAD——
    # list-only STS 无 oss:GetObject，object_exists 的 HEAD 会在 STS 签发或
    # OSS 侧被拒，导致已存在的实例恒被误判为不存在。
    # 不能用「prefix=精确 key」的 LIST（OSS 字符串前缀语义会带出兄弟对象，
    # RAM 条件也只放行父目录形态），改父目录 LIST + 客户端成员判断。
    parent = key.rsplit("/", 1)[0] + "/"
    try:
        keys = content_store.list_objects(
            parent, list_only=True, dataset=dataset)
    except Exception:  # noqa: BLE001
        return None

    if key not in keys:
        return None

    inst = DatasetInstance(
        instance_id=instance_id,
        dataset=dataset,
        dataset_version=version,
        split=split or "default",
        registered=False,
    )
    if include_files:
        try:
            inst.manifest = _instance_manifest(
                content_store, dataset, version, instance_id, split, key,
                oss_prefix=oss_prefix)
        except Exception:  # noqa: BLE001, S110
            pass  # best-effort：manifest 枚举失败不阻断实例返回
    if read_content:
        data = _read_json_object(content_store, key)
        if data:
            inst.tags = data.get("tags", {})
            inst.difficulty = data.get("difficulty")
            inst.docker_image = data.get("docker_image")
            inst.extend_meta = data.get("extend_meta", {})

    return inst
