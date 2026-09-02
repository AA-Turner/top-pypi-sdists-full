from __future__ import annotations

import hashlib
import uuid
from datetime import UTC, datetime

from matrx_ai.tools.vfs.paths import Inode, InodeType, split_components


def _now() -> datetime:
    return datetime.now(UTC)


class MemoryBackend:
    def __init__(self) -> None:
        # inode_id -> Inode
        self._inodes: dict[str, Inode] = {}
        # (workspace_id, parent_id_or_None_for_root, name) -> inode_id
        self._index: dict[tuple[str, str | None, str], str] = {}
        # workspace_id -> root inode_id
        self._roots: dict[str, str] = {}
        # blob_id -> bytes
        self._blobs: dict[str, bytes] = {}
        # sha256 -> blob_id (for dedupe)
        self._blob_by_sha: dict[str, str] = {}

    async def ensure_workspace_root(self, workspace_id: str) -> Inode:
        if workspace_id in self._roots:
            return self._inodes[self._roots[workspace_id]]
        now = _now()
        root = Inode(
            id=str(uuid.uuid4()),
            workspace_id=workspace_id,
            parent_id=None,
            name="/",
            type="dir",
            mode=0o755,
            ctime=now,
            mtime=now,
            atime=now,
        )
        self._inodes[root.id] = root
        self._index[(workspace_id, None, "/")] = root.id
        self._roots[workspace_id] = root.id
        return root

    async def get_inode(
        self,
        workspace_id: str,
        parent_id: str | None,
        name: str,
    ) -> Inode | None:
        key = (workspace_id, parent_id, name)
        inode_id = self._index.get(key)
        if inode_id is None:
            return None
        return self._inodes.get(inode_id)

    async def get_inode_by_path(self, workspace_id: str, path: str) -> Inode | None:
        root = await self.ensure_workspace_root(workspace_id)
        components = split_components(path)
        current = root
        for comp in components:
            child = await self.get_inode(workspace_id, current.id, comp)
            if child is None:
                return None
            current = child
        return current

    async def list_children(self, workspace_id: str, parent_id: str) -> list[Inode]:
        children: list[Inode] = []
        for (ws, pid, name), inode_id in self._index.items():
            if ws == workspace_id and pid == parent_id and name != "/":
                inode = self._inodes.get(inode_id)
                if inode is not None:
                    children.append(inode)
        return children

    async def create_inode(self, inode: Inode) -> Inode:
        if not inode.id:
            inode = inode.model_copy(update={"id": str(uuid.uuid4())})
        now = _now()
        if inode.ctime is None:
            inode = inode.model_copy(update={"ctime": now})
        if inode.mtime is None:
            inode = inode.model_copy(update={"mtime": now})
        if inode.atime is None:
            inode = inode.model_copy(update={"atime": now})
        key = (inode.workspace_id, inode.parent_id, inode.name)
        self._inodes[inode.id] = inode
        self._index[key] = inode.id
        return inode

    async def update_inode(self, inode_id: str, **fields) -> Inode:
        inode = self._inodes[inode_id]
        old_key = (inode.workspace_id, inode.parent_id, inode.name)
        updated = inode.model_copy(update={**fields, "mtime": fields.get("mtime") or _now()})
        new_key = (updated.workspace_id, updated.parent_id, updated.name)
        if old_key != new_key:
            del self._index[old_key]
            self._index[new_key] = updated.id
        self._inodes[updated.id] = updated
        return updated

    async def delete_inode(self, inode_id: str) -> None:
        inode = self._inodes.pop(inode_id, None)
        if inode is None:
            return
        key = (inode.workspace_id, inode.parent_id, inode.name)
        self._index.pop(key, None)

    async def get_blob(self, blob_id: str) -> bytes:
        return self._blobs[blob_id]

    async def put_blob(self, data: bytes) -> str:
        sha = hashlib.sha256(data).hexdigest()
        existing = self._blob_by_sha.get(sha)
        if existing is not None:
            return existing
        blob_id = str(uuid.uuid4())
        self._blobs[blob_id] = data
        self._blob_by_sha[sha] = blob_id
        return blob_id

    # Helpers for tests / introspection ---------------------------------------

    async def make_inode(
        self,
        workspace_id: str,
        parent_id: str | None,
        name: str,
        type: InodeType,
        *,
        mode: int | None = None,
        size: int = 0,
        symlink_target: str | None = None,
        content_id: str | None = None,
    ) -> Inode:
        if mode is None:
            mode = 0o755 if type == "dir" else 0o644
        inode = Inode(
            id=str(uuid.uuid4()),
            workspace_id=workspace_id,
            parent_id=parent_id,
            name=name,
            type=type,
            mode=mode,
            size=size,
            symlink_target=symlink_target,
            content_id=content_id,
        )
        return await self.create_inode(inode)
