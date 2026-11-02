"""content.py — 打包 Instance 目录为 content.tgz 并计算 sha-256。

内容可寻址：content_digest = "sha256:<hex>"；pull 时据此校验完整性。
打包用 stdlib tarfile（确定性排序，便于跨环境复现），可排除 image.tar.gz
（镜像已单独推 ACR，不进 content.tgz）。
"""
from __future__ import annotations

import gzip
import hashlib
import re
import tarfile
from pathlib import Path

_EXCLUDE_REL = "environment/image.tar.gz"

# 32 位 hex（无前缀）＝ apiserver ingest 扫描写入的 OSS ETag（简单上传即 md5）。
_MD5_HEX_RE = re.compile(r"^[0-9a-fA-F]{32}$")


def sha256_file(path: str | Path) -> str:
    """流式计算文件 sha-256，返回 'sha256:<hex>'。"""
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return "sha256:" + h.hexdigest()


def md5_file(path: str | Path) -> str:
    """流式计算文件 md5，返回 32 位小写 hex。"""
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def verify_file_digest(path: str | Path, expected: str | None) -> bool:
    """校验本地文件与 manifest ``content_digest`` 一致（两种生产者格式）。

    - SDK push/commit 路径写 ``sha256:<hex>`` → 按 sha256 比对；
    - apiserver ingest 扫描路径写 OSS ``ETag``（简单上传即 32 位 md5 hex，
      无前缀）→ 按 md5 比对（对齐服务端契约，避免 pull(verify=True) 误报）。
    空/缺失 digest（历史资产合并条目）视为跳过校验，返回 True。
    """
    if not expected:
        return True
    expected = expected.strip().strip('"')
    if not expected:
        return True
    if _MD5_HEX_RE.match(expected):
        return md5_file(path) == expected.lower()
    return sha256_file(path) == expected


def _normalize(ti: tarfile.TarInfo) -> tarfile.TarInfo:
    """归一化 tar 条目元数据，保证跨时间/机器可复现。"""
    ti.mtime = 0
    ti.uid = ti.gid = 0
    ti.uname = ti.gname = ""
    return ti


def pack(local_dir: str | Path, out_tgz: str | Path, *,
         exclude_image_tar: bool = True,
         compresslevel: int | None = None) -> str:
    """把 local_dir 打包成 out_tgz（gzip tar），返回 content_digest。

    确定性：条目按相对路径排序、元数据（mtime/uid/gid/uname/gname）归零、gzip
    header mtime=0，故同一目录内容恒得同一 digest（跨时间/机器可复现）。

    ``compresslevel``：gzip 压缩级别（1-9），默认 None 使用 gzip 库默认值（9）。
    较低级别（如 1）可显著减少 CPU 时间但产出稍大的文件。
    """
    src = Path(local_dir)
    out = Path(out_tgz)
    files = sorted(p for p in src.rglob("*") if p.is_file())
    gz_kw: dict = {"filename": "", "mode": "wb", "mtime": 0}
    if compresslevel is not None:
        gz_kw["compresslevel"] = compresslevel
    with open(out, "wb") as raw, \
            gzip.GzipFile(fileobj=raw, **gz_kw) as gz, \
            tarfile.open(fileobj=gz, mode="w") as tar:
        for p in files:
            rel = p.relative_to(src).as_posix()
            if exclude_image_tar and rel == _EXCLUDE_REL:
                continue
            tar.add(str(p), arcname="./" + rel, filter=_normalize)
    return sha256_file(out)


def compute_source_hash(local_dir: str | Path, *,
                        exclude_image_tar: bool = True) -> str:
    """快速计算源目录的内容哈希（不打包、不压缩）。

    遍历目录所有文件，按相对路径排序，对每个文件算 SHA-256，
    最终对所有 ``(path, sha256)`` 对再算一次 SHA-256。
    返回 ``"src-sha256:<hex>"``。

    与 :func:`pack` 的 digest 不同：本函数不做 tar+gzip，只做文件读取 + 哈希，
    CPU 开销大幅降低（省掉压缩），适合作为变更检测的快速指纹。

    ``exclude_image_tar`` 语义同 :func:`pack`。
    """
    src = Path(local_dir)
    files = sorted(p for p in src.rglob("*") if p.is_file())
    h = hashlib.sha256()
    for p in files:
        rel = p.relative_to(src).as_posix()
        if exclude_image_tar and rel == _EXCLUDE_REL:
            continue
        fh = hashlib.sha256()
        with open(p, "rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                fh.update(chunk)
        h.update(rel.encode("utf-8"))
        h.update(fh.digest())
    return "src-sha256:" + h.hexdigest()
