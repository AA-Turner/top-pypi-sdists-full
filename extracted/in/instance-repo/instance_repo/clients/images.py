"""clients/images.py — 公开的独立镜像能力（v0.8 新增）。

v0.8 之前，镜像推送只作为「推实例」的内部副作用存在：没有实例目录就无法推镜像，也没有
任何拉取入口。本客户端把镜像能力提升为一等公民，四个动作可独立使用：

* :meth:`push`   本地 docker-archive tar → registry
* :meth:`pull`   registry → 本地 docker-archive tar
* :meth:`copy`   registry → registry（跨环境搬运，digest 固定）
* :meth:`exists` 存在性探测（带一致性重试）

命名不用调用方自己拼：正常业务固定 ``split_first``，:meth:`ref_for` 经
``DatasetName`` 解析后产出 ``{host}/{ns}/{sanitize(leaf)}:{split}-{id}``
（单段 L1 与两段 L1/L2 均支持）。旧布局仅由低层 ``Layout`` 读取存量数据。

网络策略沿用数据面统一口径：push / copy / exists 私网优先、连通性失败时受限回退公网；
**pull 归类为下载动作，强制私网**，公网回退被禁用，不可达即抛
``PrivateNetworkRequired``。
"""
from __future__ import annotations

from pathlib import Path

from .. import bootstrap
from .. import paths as P
from ..errors import SchemaError
from ..layout import Layout
from .config import business_metadata_model


class ImageClient:
    """独立的 ACR 镜像客户端（不依赖实例目录）。"""

    def __init__(self, transport, profile, image_store) -> None:
        self._t = transport
        self._p = profile
        self._image = image_store

    # ── 命名 ──
    def _layout(self, metadata_model: str | None = None) -> Layout:
        return Layout(metadata_model or self._p.metadata_model,
                      prefix=self._p.oss_prefix)

    def ref_for(self, dataset: str, instance_id: str, *,
                split: str | None = None, version: str | None = None,
                acr_host: str | None = None, namespace: str | None = None,
                metadata_model: str | None = None) -> str:
        """按当前元数据模型算某实例的 ACR 引用。

        ``acr_host`` / ``namespace`` 缺省取当前 profile（含自动发现结果）；显式传入可用于
        计算**目标环境**的引用，配合 :meth:`copy` 做跨环境搬运。
        """
        requested_model = metadata_model
        if requested_model is None:
            requested_model = self._p.metadata_model
        model = business_metadata_model(requested_model)
        host = acr_host or bootstrap.require(
            self._p, "effective_acr_host", action="拼 ACR 镜像引用")
        ns = namespace or bootstrap.require(
            self._p, "acr_namespace", action="拼 ACR 镜像引用")
        name = P.DatasetName.parse(dataset)
        return self._layout(model).image_ref(
            host, ns, name.canonical, instance_id,
            version=version, split=split)

    # ── 动作 ──
    def push(self, tar_path, ref: str, *, overwrite: bool = False) -> str:
        """把本地 docker-archive tar 推到 ``ref``；返回稳定的私网规范引用。

        ``overwrite=False``（默认）时目标已存在即跳过推送，直接返回引用——镜像 tag 承载
        实例身份，重复推送同一 tag 是可疑操作，默认不覆盖。
        """
        path = Path(tar_path)
        if not path.is_file():
            raise SchemaError(f"{path} 不是可读文件：push 需要 docker-archive tar")
        return self._image.push(path, _need_ref(ref), overwrite=overwrite)

    def pull(self, ref: str, tar_path, *, overwrite: bool = False) -> str:
        """把 ``ref`` 拉到本地 docker-archive tar；返回实际拉取的 digest 固定引用。

        返回值带 ``@sha256:...``：拉取前先 inspect 取不可变 digest 并以 digest 固定，
        因此返回的引用可用于复现同一份字节，而原始 tag 可能已被覆盖。
        """
        return self._image.pull(_need_ref(ref), Path(tar_path),
                                overwrite=overwrite)

    def copy(self, src_ref: str, dst_ref: str, *, overwrite: bool = False) -> str:
        """registry → registry 搬运；源以 digest 固定，返回目标规范引用。"""
        return self._image.copy(_need_ref(src_ref, "src_ref"),
                                _need_ref(dst_ref, "dst_ref"),
                                overwrite=overwrite)

    def exists(self, ref: str, *, retries: int = 0,
               retry_delay: float = 1.5) -> bool:
        """探测 ``ref`` 是否存在。

        刚推送完立即探测可能因 manifest 秒级一致性延迟而假 False，此时传
        ``retries=3`` 让探测带重试，避免把「已推成功」误报成失败。
        """
        if retries < 0:
            raise SchemaError("retries 必须 >= 0")
        return self._image.exists(_need_ref(ref), retries=retries,
                                  retry_delay=retry_delay)


def _need_ref(ref: str, name: str = "ref") -> str:
    value = (ref or "").strip()
    if not value:
        raise SchemaError(f"{name} must not be empty")
    if "/" not in value:
        raise SchemaError(
            f"invalid {name} {value!r}: expected '{{host}}/{{namespace}}/"
            f"{{repo}}:{{tag}}'")
    return value
