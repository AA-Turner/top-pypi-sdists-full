from __future__ import annotations

from typing import TYPE_CHECKING, Any

from setuptools_git_versioning.git import (
    count_since,
    get_all_tags,
    get_branch,
    get_branches,
    get_latest_file_commit,
    get_sha,
    get_tag,
    get_tags,
    is_dirty,
)
from setuptools_git_versioning.setup import get_version, infer_version
from setuptools_git_versioning.version import version_from_git

if TYPE_CHECKING:
    from setuptools.dist import Distribution


def parse_config(dist: Distribution, attr: Any, value: Any) -> None:
    "Dummy function used only to register in distutils"
    return


__all__ = [
    "count_since",
    "get_all_tags",
    "get_branch",
    "get_branches",
    "get_latest_file_commit",
    "get_sha",
    "get_tag",
    "get_tags",
    "get_version",
    "infer_version",
    "is_dirty",
    "version_from_git",
]
