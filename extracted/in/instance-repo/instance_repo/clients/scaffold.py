"""clients/scaffold.py — ScaffoldPackage 存储（仅 OSS，无元数据）。

目标 bucket 与根前缀（root）**均由调用方提供**（经 Repo 从 profile 传入：
``scaffold_bucket`` / ``scaffold_root``，来源 overrides 或环境变量
``IR_SCAFFOLD_BUCKET`` / ``IR_SCAFFOLD_ROOT``）。本模块不内置任何具体 bucket / 项目路径。

布局：
    {root}/{scaffold}/install.sh                     安装脚本
    {root}/{scaffold}/latest                         指针文件（内容=version）
    {root}/{scaffold}/{version}/...                  版本文件树

不写 apiserver 元数据；OSS 访问经 apiserver 签发的 STS。上传/下载在 STS 授权内；
list 需 STS 含 oss:ListObjects（当前读写 STS 默认不含，会 403，待 apiserver 放权）。
"""
from __future__ import annotations

import tempfile
from pathlib import Path

from .. import paths as P
from ..concurrency import map_concurrent
from ..errors import SchemaError
from ..store.oss import OssContentStore


class ScaffoldClient:
    def __init__(self, transport, *, bucket: str = "", root: str = "",
                 bucket_factory=None) -> None:
        # bucket / root 由调用方提供（无内置默认）；为空时构造不报错，
        # 真正做 scaffold 操作时才校验（惰性），避免未用到 scaffold 也被拦。
        self._bucket = bucket
        self._root = root
        self._store = OssContentStore(transport, bucket, bucket_factory=bucket_factory)

    @property
    def bucket(self) -> str:
        return self._bucket

    def _need_bucket(self) -> None:
        if not self._bucket:
            raise SchemaError(
                "scaffold bucket 未配置；请通过 IR_SCAFFOLD_BUCKET 或 "
                "profile_overrides['scaffold_bucket'] 提供（见部署文档）")

    # ── 上传 ──
    def upload_install(self, scaffold: str, local_path, *, overwrite: bool = True) -> dict:
        """上传 install.sh 到 {scaffold}/install.sh。"""
        self._need_bucket()
        return self._store.put_object(P.scaffold_install_key(self._root, scaffold),
                                      Path(local_path), overwrite=overwrite)

    def set_latest(self, scaffold: str, version: str) -> dict:
        """写 {scaffold}/latest 指针（内容=version 字符串）。恒覆盖。"""
        self._need_bucket()
        return self._store.put_object(P.scaffold_latest_key(self._root, scaffold),
                                      str(version).encode("utf-8"), overwrite=True)

    def upload_version(self, scaffold: str, version: str, local_dir, *,
                       overwrite: bool = True, concurrency: int = 8) -> list[str]:
        """递归上传 local_dir 到 {scaffold}/{version}/…（保留相对路径）。返回上传的 key 列表。

        同版本前缀共用一次 STS（sts_prefix），并发上传各文件；返回 key 保持排序。
        """
        self._need_bucket()
        local_dir = Path(local_dir)
        files = sorted(p for p in local_dir.rglob("*") if p.is_file())
        sts_prefix = P.scaffold_version_prefix(self._root, scaffold, version)
        # 预热一次共享 STS（否则首轮 concurrency 个 worker 会各签一次同前缀）
        self._store.prewarm(sts_prefix)

        def _one(f: Path) -> str:
            rel = f.relative_to(local_dir).as_posix()
            key = P.scaffold_object_key(self._root, scaffold, version, rel)
            self._store.put_object(key, f, overwrite=overwrite,
                                   sts_prefix=sts_prefix)
            return key

        return map_concurrent(_one, files, concurrency=concurrency)

    # ── 下载 ──
    def download(self, scaffold: str, rel_path: str, dest) -> Path:
        """下载单个对象；rel_path 相对 {scaffold}/ 前缀，如 install.sh / latest / {version}/x。"""
        self._need_bucket()
        key = P.scaffold_prefix(self._root, scaffold) + rel_path.lstrip("/")
        return self._store.get_object(key, Path(dest))

    def get_latest(self, scaffold: str) -> str:
        """读取 {scaffold}/latest 指针内容（version 字符串）。"""
        self._need_bucket()
        with tempfile.TemporaryDirectory(prefix="irepo_scaffold_") as td:
            dest = Path(td) / "latest"
            self._store.get_object(P.scaffold_latest_key(self._root, scaffold), dest)
            return dest.read_text(encoding="utf-8").strip()

    # ── list（需 STS 含 oss:ListObjects）──
    def list(self, scaffold: str | None = None, *, prefix: str | None = None) -> list[str]:
        """列举对象 key。prefix 显式优先；否则按 scaffold 前缀；都不给则整个 scaffold 根。"""
        self._need_bucket()
        if prefix is not None:
            pfx = prefix
        elif scaffold:
            pfx = P.scaffold_prefix(self._root, scaffold)
        else:
            pfx = P._root(self._root) + "/"
        return self._store.list_objects(pfx)
