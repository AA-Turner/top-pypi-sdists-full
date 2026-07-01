from __future__ import annotations

import typing as t

from fsspec import AbstractFileSystem, register_implementation

from dreadnode.storage.providers import (
    AzureBlobCredentials,
    GCSCredentials,
    MinioCredentials,
    S3Credentials,
    StorageProvider,
    from_provider,
)
from dreadnode.storage.session_store import MessageSearchResult, SessionRecord, SessionStore
from dreadnode.storage.storage import Storage


class DreadnodeFS(AbstractFileSystem):
    protocol = ("dn", "dreadnode")


register_implementation("dreadnode", DreadnodeFS, clobber=True)
register_implementation("dn", DreadnodeFS, clobber=True)


def __getattr__(name: str) -> t.Any:
    if name == "BaseLoader":
        from dreadnode.packaging.loader import BaseLoader

        return BaseLoader
    if name == "Package":
        from dreadnode.packaging.package import Package

        return Package
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = [
    "AzureBlobCredentials",
    "GCSCredentials",
    "MessageSearchResult",
    "MinioCredentials",
    "S3Credentials",
    "SessionRecord",
    "SessionStore",
    "Storage",
    "StorageProvider",
    "from_provider",
]
