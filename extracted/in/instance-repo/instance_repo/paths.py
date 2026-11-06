"""paths.py — OSS/ACR 路径约定（唯一事实源，与 apiserver + RFC-0001 对齐）。

    oss://{bucket}/{dataset_root}/{version}/{instance_id}.json                 # Metadata (3层)
    oss://{bucket}/{dataset_root}/{version}/{split}/{instance_id}.json         # Metadata (4层)
    oss://{bucket}/{dataset_root}/{version}-assets/{instance_id}/content.tgz   # Content (3层)
    oss://{bucket}/{dataset_root}/{version}/{split}-assets/{instance_id}/content.tgz  # Content (4层)
    acr://{host}/{ns}/{sanitize(dataset_leaf)}:{version}-{instance_id}         # Image

``dataset_root`` 支持 ``{L1}`` 或 ``{L1}/{L2}``。路径规则：无 split 或
split="default" 时 -assets/-report 后缀跟 version（3层）；
有显式 split 时 -assets/-report 后缀跟 split（4层），version 独立占一层目录。

纯函数、无 I/O，便于单测与跨语言 conformance 比对。
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass

from .errors import SchemaError


def _dataset_name_parts(value: object) -> tuple[str, str, str, tuple[str, ...], str]:
    if not isinstance(value, str):
        raise SchemaError(f"dataset must be a string, got {type(value).__name__}")
    segments = tuple(value.split("/"))
    invalid_segment = any(
        not segment
        or segment in {".", ".."}
        or "\\" in segment
        or "*" in segment
        or "?" in segment
        or any(unicodedata.category(char) == "Cc" for char in segment)
        for segment in segments
    )
    if not segments or invalid_segment:
        raise SchemaError(
            f"dataset must contain one or more canonical segments, got {value!r}")
    l1 = segments[0]
    # 多段名（3+ 段）里 l2 是 l1 之下的完整后缀路径（含 "/"），保持
    # "l2 为空 ⇔ 根(L1)" 的不变量与 {l1,l2} 家族索引语义不变。
    l2 = "/".join(segments[1:])
    namespace = "/".join(segments[:-1])
    return l1, l2, namespace, segments, segments[-1]


@dataclass(frozen=True)
class DatasetName:
    """Canonical dataset name: one segment (L1) or more (L1/L2/...).

    Direct construction is supported only when every derived field matches
    ``canonical``; otherwise construction raises :class:`SchemaError`.
    """

    canonical: str
    l1: str
    l2: str
    namespace: str
    segments: tuple[str, ...]
    leaf: str

    def __post_init__(self) -> None:
        expected = _dataset_name_parts(self.canonical)
        actual = (self.l1, self.l2, self.namespace, self.segments, self.leaf)
        if actual != expected:
            raise SchemaError(
                "DatasetName fields must match canonical: expected "
                f"(l1, l2, namespace, segments, leaf)={expected!r}, got {actual!r}")

    @classmethod
    def parse(cls, value: str) -> DatasetName:
        l1, l2, namespace, segments, leaf = _dataset_name_parts(value)
        return cls(
            canonical=value,
            l1=l1,
            l2=l2,
            namespace=namespace,
            segments=segments,
            leaf=leaf,
        )

    def relative_root(self, prefix: str) -> str:
        """Return the dataset root with one trailing slash and no empty segments."""
        prefix_segments = tuple(segment for segment in prefix.split("/") if segment)
        return "/".join((*prefix_segments, *self.segments)) + "/"


def split_dataset(dataset: str) -> tuple[str, str]:
    """Return ``(L1, L2)``; single-segment datasets use an empty L2.

    For multi-level names (3+ segments) ``L2`` is the full suffix path under
    ``L1`` (segments joined by ``/``), e.g. ``"A/B/C"`` → ``("A", "B/C")``.
    """
    name = DatasetName.parse(dataset)
    return name.l1, name.l2


def sanitize_repo(name: str) -> str:
    """ACR repo 名规则：小写化 + 非 [a-z0-9._-] 转 '-'，去除首尾 '-._'。"""
    s = re.sub(r"[^a-z0-9._-]+", "-", name.lower()).strip("-._")
    return s or "dataset"


#: bucket 内的对象目录布局约定（与 apiserver 契约强绑定），非基础设施位置信息。
DEFAULT_PREFIX = "swe/datasets"
_DEFAULT_PREFIX = DEFAULT_PREFIX      # 向后兼容别名（旧调用点仍在用）


def _version_prefix(dataset: str, version: str, split: str | None,
                    prefix: str = _DEFAULT_PREFIX) -> str:
    root = DatasetName.parse(dataset).relative_root(prefix)
    base = f"{root}{version}"
    return f"{base}/{split}" if split and split != "default" else base


def metadata_key(dataset: str, version: str, instance_id: str,
                 split: str | None = None, *, prefix: str = _DEFAULT_PREFIX) -> str:
    """Instance metadata 的 OSS object key（不含 bucket）。"""
    return f"{_version_prefix(dataset, version, split, prefix)}/{instance_id}.json"


def content_key(dataset: str, version: str, instance_id: str,
                split: str | None = None, *, prefix: str = _DEFAULT_PREFIX) -> str:
    """Instance content.tgz 的 OSS object key（不含 bucket），走 -assets 后缀。

    3 层（无 split / split="default"）：{dataset_root}/{version}-assets/{id}/content.tgz
    4 层（有 split）：{dataset_root}/{version}/{split}-assets/{id}/content.tgz
    """
    root = DatasetName.parse(dataset).relative_root(prefix)
    if split and split != "default":
        return f"{root}{version}/{split}-assets/{instance_id}/content.tgz"
    return f"{root}{version}-assets/{instance_id}/content.tgz"


def report_key(dataset: str, version: str, instance_id: str,
               split: str | None = None, *, prefix: str = _DEFAULT_PREFIX) -> str:
    """Instance 质检 report 的 OSS object key（不含 bucket），走 -report 后缀。

    3 层（无 split / split="default"）：{dataset_root}/{version}-report/{id}/report.jsonl
    4 层（有 split）：{dataset_root}/{version}/{split}-report/{id}/report.jsonl
    """
    root = DatasetName.parse(dataset).relative_root(prefix)
    if split and split != "default":
        return f"{root}{version}/{split}-report/{instance_id}/report.jsonl"
    return f"{root}{version}-report/{instance_id}/report.jsonl"


def sts_oss_prefix(dataset: str, version: str | None = None, *,
                   prefix: str = _DEFAULT_PREFIX) -> str:
    """签发 OSS STS 时传给 apiserver 的 dataset 级 oss_prefix（带尾斜杠）。

    apiserver 的内联 policy 会收窄成 ``<bucket>/<prefix>/*``（仅 prefix 的
    直接子路径）。若只传 ``{version}``，则 ``{version}-assets/`` 与
    ``{version}-report/`` 这两个兄弟前缀无法命中，导致 content.tgz / report.jsonl 写入
    403。因此取 dataset 级前缀，一次签发覆盖该 dataset 下所有版本的
    metadata、content、report。``version`` 参数保留以兼容旧调用签名，但不再影响返回值。
    """
    return DatasetName.parse(dataset).relative_root(prefix)


def oss_uri(bucket: str, key: str) -> str:
    return f"oss://{bucket}/{key}"


def dataset_prefix(bucket: str, dataset: str, *,
                   prefix: str = _DEFAULT_PREFIX) -> str:
    """整个 dataset 的 OSS prefix（含所有 split/version）。"""
    root = DatasetName.parse(dataset).relative_root(prefix)
    return f"oss://{bucket}/{root}"


# ── ScaffoldPackage（仅存储、无元数据）─────────────────────────────────────
# scaffold 的目标 bucket 与根前缀（root）均由调用方提供（见 ScaffoldClient），
# 本模块不内置任何具体 bucket / 项目路径。布局：
#   {root}/{scaffold}/install.sh          安装脚本
#   {root}/{scaffold}/latest              指向当前版本的指针文件（内容=version 字符串）
#   {root}/{scaffold}/{version}/...       某版本的文件树


def _root(root: str) -> str:
    if not root:
        raise SchemaError(
            "scaffold root 未配置；请通过 IR_SCAFFOLD_ROOT 或 profile_overrides "
            "['scaffold_root'] 提供（见部署文档）")
    return root.strip("/")


def scaffold_prefix(root: str, scaffold: str) -> str:
    """某 scaffold 的对象前缀（不含 bucket，带尾斜杠）。"""
    return f"{_root(root)}/{scaffold}/"


def scaffold_install_key(root: str, scaffold: str) -> str:
    return f"{_root(root)}/{scaffold}/install.sh"


def scaffold_latest_key(root: str, scaffold: str) -> str:
    return f"{_root(root)}/{scaffold}/latest"


def scaffold_version_prefix(root: str, scaffold: str, version: str) -> str:
    """某 scaffold 某 version 的对象前缀（带尾斜杠）。"""
    return f"{_root(root)}/{scaffold}/{version}/"


def scaffold_object_key(root: str, scaffold: str, version: str, rel_path: str) -> str:
    """{root}/{scaffold}/{version}/{rel_path} 的完整对象 key（rel_path 用 posix 相对路径）。"""
    return f"{_root(root)}/{scaffold}/{version}/{rel_path.lstrip('/')}"


def image_ref(acr_host: str, namespace: str, dataset: str, version: str,
              instance_id: str) -> str:
    """ACR 镜像引用：{host}/{ns}/{sanitize(dataset leaf)}:{version}-{instance_id}。"""
    leaf = DatasetName.parse(dataset).leaf
    return f"{acr_host}/{namespace}/{sanitize_repo(leaf)}:{version}-{instance_id}"


def swap_image_host(source_image: str, src_host: str, dst_host: str) -> str:
    """把镜像引用的 registry host 从 src 换成 dst（namespace/repo/tag 保留）。"""
    if source_image.startswith(src_host + "/"):
        return dst_host + source_image[len(src_host):]
    _, _, rest = source_image.partition("/")
    return f"{dst_host}/{rest}" if rest else source_image


def retarget_image(source_image: str, src_host: str, dst_host: str,
                   dst_namespace: str = "") -> str:
    """算上架的目标镜像引用：host 必换，``dst_namespace`` 非空时同时换命名空间段。

    仓库名与 tag **一律保留**——tag 承载实例身份，改写会指向一个从未推送过的镜像。

    ``dst_namespace`` 为空时退化为 :func:`swap_image_host`（保留源命名空间），与
    v0.7.x 行为一致。v0.8 之前三语言 CLI 都解析了 ``--target-acr-namespace`` 却从未
    使用它，本函数是该缺陷的修复点。

    源引用形如 ``{host}/{ns}/{repo}:{tag}``；命名空间可含多段（``{ns_a}/{ns_b}/{repo}``），
    此时整段命名空间被替换为 ``dst_namespace``，只保留最后一段仓库名。
    """
    swapped = swap_image_host(source_image, src_host, dst_host)
    ns = (dst_namespace or "").strip().strip("/")
    if not ns:
        return swapped
    host, sep, rest = swapped.partition("/")
    if not sep or "/" not in rest:
        # 无命名空间段（形如 host/repo:tag）：插入目标命名空间。
        return f"{host}/{ns}/{rest}" if sep else swapped
    repo = rest.rsplit("/", 1)[1]
    return f"{host}/{ns}/{repo}"
