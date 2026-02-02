"""Corvic system client protocol."""

import sqlalchemy as sa
from typing_extensions import Protocol

from corvic.system._embedder import ImageEmbedder, TextEmbedder
from corvic.system.op_graph_executor import OpGraphExecutor
from corvic.system.staging import StagingDB
from corvic.system.storage import StorageManager


class Client(Protocol):
    """A Client holds objects that provide access to the platform."""

    @property
    def storage_manager(self) -> StorageManager: ...

    @property
    def sa_engine(self) -> sa.Engine: ...

    @property
    def staging_db(self) -> StagingDB: ...

    @property
    def executor(self) -> OpGraphExecutor: ...

    @property
    def text_embedder(self) -> TextEmbedder: ...

    @property
    def image_embedder(self) -> ImageEmbedder: ...
