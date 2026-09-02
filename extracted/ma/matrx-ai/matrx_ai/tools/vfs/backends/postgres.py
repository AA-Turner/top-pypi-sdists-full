# Wired to be implemented against cxm — see migrations/0050_vfs_inode_blob.sql
#
# This backend defines the methods that will hit the Supabase tables
# vfs_inode and vfs_blob via the cxm singleton. Wiring is deferred to the
# integration phase; the schema migration is the source of truth for the
# columns these methods will read/write.
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from matrx_ai.tools.vfs.paths import Inode


class PostgresBackend:
    def __init__(self) -> None:
        # The cxm singleton will be obtained lazily inside each method to
        # avoid import-time database initialization during testing.
        pass

    async def ensure_workspace_root(self, workspace_id: str) -> Inode:
        raise NotImplementedError("PostgresBackend wiring deferred to integration phase")

    async def get_inode(
        self,
        workspace_id: str,
        parent_id: str | None,
        name: str,
    ) -> Inode | None:
        raise NotImplementedError("PostgresBackend wiring deferred to integration phase")

    async def get_inode_by_path(self, workspace_id: str, path: str) -> Inode | None:
        raise NotImplementedError("PostgresBackend wiring deferred to integration phase")

    async def list_children(self, workspace_id: str, parent_id: str) -> list[Inode]:
        raise NotImplementedError("PostgresBackend wiring deferred to integration phase")

    async def create_inode(self, inode: Inode) -> Inode:
        raise NotImplementedError("PostgresBackend wiring deferred to integration phase")

    async def update_inode(self, inode_id: str, **fields) -> Inode:
        raise NotImplementedError("PostgresBackend wiring deferred to integration phase")

    async def delete_inode(self, inode_id: str) -> None:
        raise NotImplementedError("PostgresBackend wiring deferred to integration phase")

    async def get_blob(self, blob_id: str) -> bytes:
        raise NotImplementedError("PostgresBackend wiring deferred to integration phase")

    async def put_blob(self, data: bytes) -> str:
        raise NotImplementedError("PostgresBackend wiring deferred to integration phase")
