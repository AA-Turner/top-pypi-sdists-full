"""layout.py — 元数据模型（version_first / split_first）与对象布局策略（唯一事实源）。

v0.8 默认 ``split_first``：**split 必填、version 选填**，空 version 表示「确实无版本」，
不再被解释为 latest 或 default。``version_first`` 作为显式逃生舱保留，行为与 v0.7.x
**逐字节一致**（含 ``split="default"`` 折叠为三层的历史约定），存量数据无需迁移。

对象布局三种形态（dataset root 可以是 ``{L1}`` 或 ``{L1}/{L2}``）::

    split_first  + 无 version   {prefix}/{dataset_root}/{split}/{id}.json
                                {prefix}/{dataset_root}/{split}-assets/{id}/content.tgz
                                {prefix}/{dataset_root}/{split}-report/{id}/report.jsonl
    split_first  + 有 version   {prefix}/{dataset_root}/{version}/{split}/{id}.json
                                {prefix}/{dataset_root}/{version}/{split}-assets/{id}/content.tgz
                                {prefix}/{dataset_root}/{version}/{split}-report/{id}/report.jsonl
    version_first（旧）          见 paths.py，原样保留

ACR 镜像 tag 随模型切换：``version_first`` 为 ``{version}-{id}``，``split_first`` 为
``{split}-{id}``；仓库名两者相同，均为 ``{ns}/{sanitize(dataset leaf)}``。

服务端契约要点（对接 codex/dataset-split-first-metadata，均已实测）：

* 服务端把空 ``metadata_model`` 归一为 ``version_first``，故 SDK **必须显式下发**
  ``split_first``，不能依赖默认；
* 服务端靠**相对深度**判别布局：深度 2 视作无版本、深度 3 视作有版本，两种形态在同一次
  扫描中共存时返回 92005 歧义错误；
* ``storage_path`` 必须指向 dataset 根（无版本）或 dataset 根加版本目录（有版本）。
  指向 ``{split}/`` 子目录会解析出零个 split 并以 92005 失败，故本模块只产出这两种形态。

纯函数、无 I/O，便于单测与跨语言 conformance 比对。
"""
from __future__ import annotations

import re

from . import paths as P
from .errors import SchemaError

MODEL_VERSION_FIRST = "version_first"
MODEL_SPLIT_FIRST = "split_first"
#: ``custom`` 是用户自定义格式的元数据模型：OSS 路径沿用 split_first 约定
#: （{split}/{id}.json 元数据 + {split}-assets/{id}/ 原样目录资产），SDK 不校验具体
#: 字段（仅强约束 instance_id），元数据 freeform。
MODEL_CUSTOM = "custom"
#: v0.8 起默认 split_first（v0.7.x 行为等价于显式传 version_first）。
DEFAULT_METADATA_MODEL = MODEL_SPLIT_FIRST
_MODELS = (MODEL_VERSION_FIRST, MODEL_SPLIT_FIRST, MODEL_CUSTOM)

# ACR tag 合法字符集与长度（OCI/Docker 约定）：首字符须为字母数字或下划线，
# 其余可含字母数字、下划线、点、连字符，总长 **< 105**（ACR tag 硬上限 128，
# 预留 {version}-{id} 拼接余量，超长片段由 sanitize 截断）。**大小写敏感**，
# 不做小写化——小写化会静默改变镜像身份，进而指向一个从未推送过的引用。
_TAG_RE = re.compile(r"^[A-Za-z0-9_][A-Za-z0-9_.\-]*$")
_TAG_MAX_LEN = 104
_TAG_BAD_CHARS = re.compile(r"[^A-Za-z0-9_.\-]+")
_TAG_BAD_HEAD = re.compile(r"^[^A-Za-z0-9_]+")


def normalize_metadata_model(model: str | None) -> str:
    """归一元数据模型：空值取 SDK 默认（``split_first``），非法值抛 SchemaError。

    注意与服务端的差异：服务端把空值归一为 ``version_first``，SDK 归一为 ``split_first``。
    这不是分歧，而是 SDK 必须**显式下发** ``split_first`` 的原因——不下发就会退回旧模型。
    """
    value = (model or "").strip()
    if not value:
        return DEFAULT_METADATA_MODEL
    if value not in _MODELS:
        raise SchemaError(
            f"invalid metadata_model {value!r}: must be one of {', '.join(_MODELS)}")
    return value


def sanitize_tag(name: str) -> str:
    """把任意名字收敛成合法 ACR tag 片段（不改大小写）。"""
    s = _TAG_BAD_CHARS.sub("-", name or "")
    s = _TAG_BAD_HEAD.sub("", s)
    return s[:_TAG_MAX_LEN]


def check_tag(tag: str, *, source: str) -> str:
    """校验（不改写）一个完整 tag；非法即抛。用于 version_first 保持逐字节兼容。"""
    if not tag:
        raise SchemaError(f"{source}: empty image tag")
    if len(tag) > _TAG_MAX_LEN:
        raise SchemaError(
            f"{source}: image tag {tag!r} exceeds {_TAG_MAX_LEN} characters")
    if not _TAG_RE.match(tag):
        raise SchemaError(
            f"{source}: invalid image tag {tag!r}: must match "
            f"[A-Za-z0-9_][A-Za-z0-9_.-]*")
    return tag


def _clean_segment(value: str | None) -> str:
    return (value or "").strip().strip("/")


def check_locator(model: str, version: str | None, split: str | None
                  ) -> tuple[str, str]:
    """按模型校验并归一 ``(version, split)``；违约即抛 SchemaError。

    ``version_first``：version 必填，split 选填（空或 ``"default"`` 走三层折叠）。
    ``split_first``：split 必填且不得含 ``/``（含 ``/`` 会让服务端的相对深度判别把它
    误读成「版本 + split」两层），version 选填、空即无版本。
    """
    model = normalize_metadata_model(model)
    ver = _clean_segment(version)
    spl = _clean_segment(split)
    if model == MODEL_VERSION_FIRST:
        if not ver:
            raise SchemaError(
                "version is required when metadata_model=version_first")
        return ver, spl
    if not spl:
        raise SchemaError("split is required when metadata_model=split_first")
    if "/" in spl:
        raise SchemaError(
            f"invalid split {spl!r}: must not contain '/' when "
            f"metadata_model=split_first")
    return ver, spl


class Layout:
    """某个元数据模型下的对象/镜像布局策略。"""

    def __init__(self, model: str | None = None,
                 prefix: str = P.DEFAULT_PREFIX) -> None:
        self.model = normalize_metadata_model(model)
        self.prefix = (prefix or P.DEFAULT_PREFIX).strip("/")

    @property
    def split_first(self) -> bool:
        # custom 沿用 split_first 的路径约定（{split}/{id}.json +
        # {split}-assets/{id}/ 兄弟目录），故 path 构造上一视同仁。
        return self.model in (MODEL_SPLIT_FIRST, MODEL_CUSTOM)

    # ── 目录基座 ──
    def dataset_root(self, dataset: str) -> str:
        """dataset 级对象前缀（不含 bucket，带尾斜杠）。"""
        return P.DatasetName.parse(dataset).relative_root(self.prefix)

    def _base(self, dataset: str, version: str) -> str:
        """实例所在目录的父级（不含 bucket，带尾斜杠）：有版本时多一层 version。"""
        root = self.dataset_root(dataset)
        return f"{root}{version}/" if version else root

    def sts_prefix(self, dataset: str) -> str:
        """签发 OSS STS 用的 oss_prefix：取 dataset 级，一次覆盖 metadata/content/report。

        不能收到版本级：``{version}-assets/`` 与 ``{version}-report/`` 是 ``{version}/``
        的**兄弟**前缀，收到版本级会让这两类写入 403（v0.7.x 实测过的坑）。
        """
        return self.dataset_root(dataset)

    def ingest_storage_path(self, bucket: str, dataset: str,
                            version: str | None = None) -> str:
        """ingest 请求里下发的 ``storage_path``（含 bucket，带尾斜杠）。"""
        ver = _clean_segment(version)
        if not bucket:
            raise SchemaError(
                "oss_bucket 未配置：无法计算 ingest storage_path；请配置 "
                "IR_STORAGE_ENV 让 SDK 自动发现，或用 profile_overrides "
                "显式提供 oss_bucket")
        return f"oss://{bucket}/{self._base(dataset, ver)}"

    # ── 对象 key ──
    def metadata_key(self, dataset: str, instance_id: str, *,
                     version: str | None = None,
                     split: str | None = None) -> str:
        ver, spl = check_locator(self.model, version, split)
        if not self.split_first:
            return P.metadata_key(dataset, ver, instance_id, spl,
                                  prefix=self.prefix)
        return f"{self._base(dataset, ver)}{spl}/{instance_id}.json"

    def content_key(self, dataset: str, instance_id: str, *,
                    version: str | None = None,
                    split: str | None = None) -> str:
        ver, spl = check_locator(self.model, version, split)
        if not self.split_first:
            return P.content_key(dataset, ver, instance_id, spl,
                                 prefix=self.prefix)
        return (f"{self._base(dataset, ver)}{spl}-assets/"
                f"{instance_id}/content.tgz")

    def assets_dir(self, dataset: str, instance_id: str, *,
                   version: str | None = None,
                   split: str | None = None) -> str:
        """custom 资产目录（content_key 去 ``content.tgz``，含尾斜杠）。

        与 content.tgz 同层、同版本规则：3 层 ``{version}-assets/{id}/``、
        4 层 ``{version}/{split}-assets/{id}/``。custom push/pull 据此拼资产 key，
        避免历史缺陷把资产落到无 version 的 ``{split}-assets/{id}/``（与元数据层级错位）。
        """
        return self.content_key(dataset, instance_id,
                                version=version, split=split)[:-len("content.tgz")]

    def report_key(self, dataset: str, instance_id: str, *,
                   version: str | None = None,
                   split: str | None = None) -> str:
        ver, spl = check_locator(self.model, version, split)
        if not self.split_first:
            return P.report_key(dataset, ver, instance_id, spl,
                                prefix=self.prefix)
        return (f"{self._base(dataset, ver)}{spl}-report/"
                f"{instance_id}/report.jsonl")

    # ── ACR 镜像 ──
    def image_tag(self, instance_id: str, *, version: str | None = None,
                  split: str | None = None) -> str:
        """镜像 tag：``version_first`` 为 ``{version}-{id}``，``split_first`` 为 ``{split}-{id}``。

        ``version_first`` 走**校验不改写**（保持与 v0.7.x 逐字节一致，避免把已推送镜像的
        引用改成一个从未存在的地址）；``split_first`` 是新路径、无存量产物，故对 split 段
        做规范化后再拼，容忍 split 名里的越界字符。
        """
        ver, spl = check_locator(self.model, version, split)
        iid = (instance_id or "").strip()
        if not iid:
            raise SchemaError("instance_id must not be empty")
        if not self.split_first:
            return check_tag(f"{ver}-{iid}", source=iid)
        head = sanitize_tag(spl)
        if not head:
            raise SchemaError(
                f"split {spl!r} sanitizes to an empty image tag segment")
        return check_tag(sanitize_tag(f"{head}-{iid}"), source=iid)

    def image_ref(self, acr_host: str, namespace: str, dataset: str,
                  instance_id: str, *, version: str | None = None,
                  split: str | None = None) -> str:
        """完整 ACR 引用：``{host}/{ns}/{sanitize(dataset leaf)}:{tag}``。"""
        if not acr_host:
            raise SchemaError(
                "acr_host 未配置：无法拼 ACR 镜像引用；请配置 IR_STORAGE_ENV 让 SDK "
                "自动发现，或用 profile_overrides 显式提供 acr_host")
        if not namespace:
            raise SchemaError(
                "acr_namespace 未配置：无法拼 ACR 镜像引用；请配置 IR_STORAGE_ENV 让 "
                "SDK 自动发现，或用 profile_overrides 显式提供 acr_namespace")
        leaf = P.DatasetName.parse(dataset).leaf
        tag = self.image_tag(instance_id, version=version, split=split)
        return f"{acr_host}/{namespace}/{P.sanitize_repo(leaf)}:{tag}"
