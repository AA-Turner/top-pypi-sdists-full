"""load_instances — 只读迭代（对齐 HF load_dataset 语义）。"""
from __future__ import annotations

from .repo import Repo


def load_instances(dataset: str, version: str, *, profile: str = "default",
                   split: str | None = None, repo: Repo | None = None):
    """迭代某 dataset/version 下的实例（走 apiserver 查 DB，不枚举 OSS）。"""
    r = repo or Repo(profile=profile)
    yield from r.instances.list(dataset, version, split)
