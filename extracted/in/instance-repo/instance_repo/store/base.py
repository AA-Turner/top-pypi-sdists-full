"""store/base.py — 三后端抽象（ABC）。SDK 依赖抽象、不绑定具体实现。"""
from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from ..models import DatasetInstance


class BaseContentStore(ABC):
    """通用 OSS 对象后端（持 STS 直连）：generic put_object/get_object/object_exists
    是深接口（隐藏换 STS + bucket + 校验）；put/get 是实例内容(content.tgz+{id}.json)
    的便捷封装，report 等其它对象走 generic 接口。"""

    # ── generic object ops（report/content 共用；STS 经 scope 换取） ──
    @abstractmethod
    def put_object(self, key: str, data, *, action: str, scope: dict,
                   overwrite: bool = False) -> dict: ...

    @abstractmethod
    def get_object(self, key: str, dest: Path, *, action: str, scope: dict,
                   expected_digest: str | None = None) -> Path: ...

    @abstractmethod
    def object_exists(self, key: str, *, action: str, scope: dict) -> bool: ...

    # ── 实例内容便捷封装 ──
    @abstractmethod
    def put(self, instance_id: str, dataset: str, version: str, split: str,
            tgz_path: Path, meta_json: str, *, overwrite: bool) -> dict: ...

    @abstractmethod
    def get(self, dataset: str, version: str, instance_id: str, split: str,
            dest: Path, *, expected_digest: str | None = None) -> Path: ...


class BaseImageStore(ABC):
    """ACR 镜像后端，持 STS/临时授权 skopeo 推拉。"""

    @abstractmethod
    def push(self, tar_path: Path, ref: str, *, overwrite: bool) -> str: ...

    @abstractmethod
    def copy(self, src_ref: str, dst_ref: str, *, overwrite: bool = False) -> str: ...

    @abstractmethod
    def exists(self, ref: str) -> bool: ...


class BaseMetadataRegistry(ABC):
    """元数据后端（调 apiserver）。published 版本 MUST 拒写。"""

    @abstractmethod
    def register(self, meta: DatasetInstance) -> DatasetInstance: ...

    @abstractmethod
    def commit(self, instance_uid: str, digests: dict,
               manifest: list | None = None) -> DatasetInstance: ...

    @abstractmethod
    def get(self, dataset: str, version: str, instance_id: str,
            split: str | None = None) -> DatasetInstance | None: ...

    @abstractmethod
    def query(self, dataset: str, version: str,
              split: str | None = None) -> list[DatasetInstance]: ...

    @abstractmethod
    def feedback_append(self, dataset: str, version: str, instance_id: str,
                        feedback: dict, split: str | None = None) -> DatasetInstance: ...
