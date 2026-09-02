from __future__ import annotations

import re
import uuid
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any, Protocol, runtime_checkable

from fsspec.asyn import AsyncFileSystem
from wcmatch import glob as wcglob

from matrx_ai.tools.vfs.errors import (
    raise_eexist,
    raise_einval,
    raise_eisdir,
    raise_enoent,
    raise_enotdir,
    raise_enotempty,
    raise_exdev,
)
from matrx_ai.tools.vfs.paths import (
    Inode,
    basename,
    dirname,
    join,
    normalize,
    split_components,
)

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator


def _now() -> datetime:
    return datetime.now(UTC)


@runtime_checkable
class AbstractBackend(Protocol):
    async def get_inode(
        self,
        workspace_id: str,
        parent_id: str | None,
        name: str,
    ) -> Inode | None: ...

    async def get_inode_by_path(self, workspace_id: str, path: str) -> Inode | None: ...

    async def list_children(self, workspace_id: str, parent_id: str) -> list[Inode]: ...

    async def create_inode(self, inode: Inode) -> Inode: ...

    async def update_inode(self, inode_id: str, **fields: Any) -> Inode: ...

    async def delete_inode(self, inode_id: str) -> None: ...

    async def get_blob(self, blob_id: str) -> bytes: ...

    async def put_blob(self, data: bytes) -> str: ...

    async def ensure_workspace_root(self, workspace_id: str) -> Inode: ...


class MatrxAsyncFS(AsyncFileSystem):
    protocol = "matrx"
    root_marker = "/"
    async_impl = True

    def __init__(
        self,
        backend: AbstractBackend,
        workspace_id: str,
        *,
        asynchronous: bool = True,
        loop: Any = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(asynchronous=asynchronous, loop=loop, **kwargs)
        self.backend = backend
        self.workspace_id = workspace_id

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @classmethod
    def _strip_protocol(cls, path: Any) -> str:
        if isinstance(path, list):
            return [cls._strip_protocol(p) for p in path]
        s = str(path)
        if s.startswith(f"{cls.protocol}://"):
            s = s[len(cls.protocol) + 3 :]
        return normalize(s) if s else "/"

    def _to_info(self, inode: Inode, path: str) -> dict[str, Any]:
        if inode.type == "dir":
            kind = "directory"
        elif inode.type == "symlink":
            kind = "link"
        else:
            kind = "file"
        return {
            "name": path,
            "size": inode.size,
            "type": kind,
            "mode": inode.mode,
            "uid": inode.uid,
            "gid": inode.gid,
            "mtime": inode.mtime,
            "ctime": inode.ctime,
            "atime": inode.atime,
            "symlink_target": inode.symlink_target,
        }

    async def _resolve(self, path: str) -> Inode:
        norm = normalize(path)
        inode = await self.backend.get_inode_by_path(self.workspace_id, norm)
        if inode is None:
            raise_enoent(norm)
        return inode

    async def _resolve_or_none(self, path: str) -> Inode | None:
        norm = normalize(path)
        return await self.backend.get_inode_by_path(self.workspace_id, norm)

    async def _resolve_parent(self, path: str) -> Inode:
        norm = normalize(path)
        parent_path = dirname(norm)
        parent = await self.backend.get_inode_by_path(self.workspace_id, parent_path)
        if parent is None:
            raise_enoent(parent_path)
        if parent.type != "dir":
            raise_enotdir(parent_path)
        return parent

    async def _ensure_root(self) -> Inode:
        return await self.backend.ensure_workspace_root(self.workspace_id)

    # ------------------------------------------------------------------
    # Directory listing / stat
    # ------------------------------------------------------------------

    async def _ls(self, path: str, detail: bool = True, **kwargs: Any) -> list[Any]:
        norm = self._strip_protocol(path)
        await self._ensure_root()
        inode = await self._resolve_or_none(norm)
        if inode is None:
            raise_enoent(norm)
        if inode.type != "dir":
            raise_enotdir(norm)
        children = await self.backend.list_children(self.workspace_id, inode.id)
        children.sort(key=lambda c: c.name)
        if detail:
            return [self._to_info(c, join(norm, c.name)) for c in children]
        return [join(norm, c.name) for c in children]

    async def _info(self, path: str, **kwargs: Any) -> dict[str, Any]:
        norm = self._strip_protocol(path)
        await self._ensure_root()
        if norm == "/":
            root = await self._ensure_root()
            return self._to_info(root, "/")
        inode = await self._resolve_or_none(norm)
        if inode is None:
            raise_enoent(norm)
        return self._to_info(inode, norm)

    # ------------------------------------------------------------------
    # File read / write
    # ------------------------------------------------------------------

    async def _cat_file(
        self,
        path: str,
        start: int | None = None,
        end: int | None = None,
        **kwargs: Any,
    ) -> bytes:
        norm = self._strip_protocol(path)
        await self._ensure_root()
        inode = await self._resolve_or_none(norm)
        if inode is None:
            raise_enoent(norm)
        if inode.type == "dir":
            raise_eisdir(norm)
        if inode.type == "symlink":
            raise_einval(norm, "cannot cat a symlink without resolution")
        if inode.content_id is None:
            return b""[start:end] if (start or end) else b""
        data = await self.backend.get_blob(inode.content_id)
        if start is None and end is None:
            return data
        return data[start:end]

    async def _pipe_file(
        self,
        path: str,
        value: bytes,
        mode: str = "overwrite",
        **kwargs: Any,
    ) -> None:
        norm = self._strip_protocol(path)
        if norm == "/":
            raise_eisdir(norm)
        await self._ensure_root()
        parent = await self._resolve_parent(norm)
        name = basename(norm)
        existing = await self.backend.get_inode(self.workspace_id, parent.id, name)
        blob_id = await self.backend.put_blob(value)
        now = _now()
        if existing is None:
            new = Inode(
                id=str(uuid.uuid4()),
                workspace_id=self.workspace_id,
                parent_id=parent.id,
                name=name,
                type="file",
                mode=0o644,
                size=len(value),
                content_id=blob_id,
                ctime=now,
                mtime=now,
                atime=now,
            )
            await self.backend.create_inode(new)
        else:
            if existing.type == "dir":
                raise_eisdir(norm)
            await self.backend.update_inode(
                existing.id,
                content_id=blob_id,
                size=len(value),
                mtime=now,
                atime=now,
            )

    # ------------------------------------------------------------------
    # Directory creation
    # ------------------------------------------------------------------

    async def _mkdir(
        self,
        path: str,
        create_parents: bool = False,
        **kwargs: Any,
    ) -> None:
        norm = self._strip_protocol(path)
        if norm == "/":
            if create_parents:
                await self._ensure_root()
                return
            raise_eexist(norm)
        await self._ensure_root()
        existing = await self._resolve_or_none(norm)
        if existing is not None:
            raise_eexist(norm)
        parent_path = dirname(norm)
        parent = await self._resolve_or_none(parent_path)
        if parent is None:
            if create_parents:
                await self._makedirs(parent_path, exist_ok=True)
                parent = await self._resolve_or_none(parent_path)
                if parent is None:
                    raise_enoent(parent_path)
            else:
                raise_enoent(parent_path)
        if parent.type != "dir":
            raise_enotdir(parent_path)
        now = _now()
        new = Inode(
            id=str(uuid.uuid4()),
            workspace_id=self.workspace_id,
            parent_id=parent.id,
            name=basename(norm),
            type="dir",
            mode=0o755,
            ctime=now,
            mtime=now,
            atime=now,
        )
        await self.backend.create_inode(new)

    async def _makedirs(self, path: str, exist_ok: bool = False) -> None:
        norm = self._strip_protocol(path)
        await self._ensure_root()
        if norm == "/":
            if not exist_ok:
                raise_eexist(norm)
            return
        existing = await self._resolve_or_none(norm)
        if existing is not None:
            if existing.type != "dir":
                raise_enotdir(norm)
            if not exist_ok:
                raise_eexist(norm)
            return
        parts = split_components(norm)
        current_path = "/"
        current = await self._ensure_root()
        for part in parts:
            next_path = join(current_path, part)
            child = await self.backend.get_inode(self.workspace_id, current.id, part)
            if child is None:
                now = _now()
                new = Inode(
                    id=str(uuid.uuid4()),
                    workspace_id=self.workspace_id,
                    parent_id=current.id,
                    name=part,
                    type="dir",
                    mode=0o755,
                    ctime=now,
                    mtime=now,
                    atime=now,
                )
                current = await self.backend.create_inode(new)
            else:
                if child.type != "dir":
                    raise_enotdir(next_path)
                current = child
            current_path = next_path

    # ------------------------------------------------------------------
    # Removal
    # ------------------------------------------------------------------

    async def _rm_file(self, path: str, **kwargs: Any) -> Any:
        norm = self._strip_protocol(path)
        await self._ensure_root()
        inode = await self._resolve_or_none(norm)
        if inode is None:
            raise_enoent(norm)
        if inode.type == "dir":
            raise_eisdir(norm)
        await self.backend.delete_inode(inode.id)

    async def _rmdir(self, path: str) -> None:
        norm = self._strip_protocol(path)
        if norm == "/":
            raise_enotempty(norm)
        await self._ensure_root()
        inode = await self._resolve_or_none(norm)
        if inode is None:
            raise_enoent(norm)
        if inode.type != "dir":
            raise_enotdir(norm)
        children = await self.backend.list_children(self.workspace_id, inode.id)
        if children:
            raise_enotempty(norm)
        await self.backend.delete_inode(inode.id)

    async def _rm(
        self,
        path: str,
        recursive: bool = False,
        batch_size: int | None = None,
        **kwargs: Any,
    ) -> Any:
        if isinstance(path, list):
            for p in path:
                await self._rm(p, recursive=recursive, **kwargs)
            return
        norm = self._strip_protocol(path)
        await self._ensure_root()
        inode = await self._resolve_or_none(norm)
        if inode is None:
            raise_enoent(norm)
        if inode.type == "dir":
            if not recursive:
                raise_eisdir(norm)
            await self._rm_tree(inode)
        else:
            await self.backend.delete_inode(inode.id)

    async def _rm_tree(self, inode: Inode) -> None:
        if inode.type == "dir":
            children = await self.backend.list_children(self.workspace_id, inode.id)
            for c in children:
                await self._rm_tree(c)
        await self.backend.delete_inode(inode.id)

    # ------------------------------------------------------------------
    # Copy / move
    # ------------------------------------------------------------------

    async def _cp_file(self, path1: str, path2: str, **kwargs: Any) -> None:
        src = self._strip_protocol(path1)
        dst = self._strip_protocol(path2)
        await self._ensure_root()
        src_inode = await self._resolve_or_none(src)
        if src_inode is None:
            raise_enoent(src)
        if src_inode.type == "dir":
            raise_eisdir(src)
        data = b""
        if src_inode.content_id is not None:
            data = await self.backend.get_blob(src_inode.content_id)
        await self._pipe_file(dst, data)

    async def _mv_file(self, path1: str, path2: str) -> None:
        await self._mv(path1, path2)

    async def _mv(self, path1: str, path2: str, **kwargs: Any) -> None:
        src = self._strip_protocol(path1)
        dst = self._strip_protocol(path2)
        if src == "/" or dst == "/":
            raise_einval(src, "cannot move filesystem root")
        await self._ensure_root()
        src_inode = await self._resolve_or_none(src)
        if src_inode is None:
            raise_enoent(src)
        if src_inode.workspace_id != self.workspace_id:
            raise_exdev(src)
        dst_inode = await self._resolve_or_none(dst)
        if dst_inode is not None:
            if dst_inode.type == "dir" and src_inode.type != "dir":
                # POSIX: rename onto an existing directory of a non-dir is EISDIR
                raise_eisdir(dst)
            if dst_inode.type != "dir":
                # overwrite an existing file
                await self.backend.delete_inode(dst_inode.id)
            else:
                # both dirs: only allow when destination is empty
                children = await self.backend.list_children(self.workspace_id, dst_inode.id)
                if children:
                    raise_enotempty(dst)
                await self.backend.delete_inode(dst_inode.id)
        new_parent = await self._resolve_parent(dst)
        await self.backend.update_inode(
            src_inode.id,
            parent_id=new_parent.id,
            name=basename(dst),
        )

    # ------------------------------------------------------------------
    # Predicates
    # ------------------------------------------------------------------

    async def _exists(self, path: str, **kwargs: Any) -> bool:
        norm = self._strip_protocol(path)
        try:
            await self._ensure_root()
        except Exception:
            return False
        if norm == "/":
            return True
        inode = await self._resolve_or_none(norm)
        return inode is not None

    async def _isdir(self, path: str) -> bool:
        norm = self._strip_protocol(path)
        try:
            await self._ensure_root()
            if norm == "/":
                return True
            inode = await self._resolve_or_none(norm)
        except Exception:
            return False
        return inode is not None and inode.type == "dir"

    async def _isfile(self, path: str) -> bool:
        norm = self._strip_protocol(path)
        try:
            await self._ensure_root()
            if norm == "/":
                return False
            inode = await self._resolve_or_none(norm)
        except Exception:
            return False
        return inode is not None and inode.type == "file"

    # ------------------------------------------------------------------
    # Symlinks
    # ------------------------------------------------------------------

    async def _symlink(self, src: str, dst: str) -> None:
        # `src` is the target the link points to (may be absolute or relative).
        # `dst` is the path of the link itself.
        dst_norm = self._strip_protocol(dst)
        if dst_norm == "/":
            raise_eexist(dst_norm)
        await self._ensure_root()
        existing = await self._resolve_or_none(dst_norm)
        if existing is not None:
            raise_eexist(dst_norm)
        parent = await self._resolve_parent(dst_norm)
        now = _now()
        new = Inode(
            id=str(uuid.uuid4()),
            workspace_id=self.workspace_id,
            parent_id=parent.id,
            name=basename(dst_norm),
            type="symlink",
            mode=0o777,
            size=len(src),
            symlink_target=src,
            ctime=now,
            mtime=now,
            atime=now,
        )
        await self.backend.create_inode(new)

    # ------------------------------------------------------------------
    # touch
    # ------------------------------------------------------------------

    async def _touch(self, path: str, truncate: bool = True, **kwargs: Any) -> None:
        norm = self._strip_protocol(path)
        if norm == "/":
            raise_eisdir(norm)
        await self._ensure_root()
        existing = await self._resolve_or_none(norm)
        if existing is None:
            await self._pipe_file(norm, b"")
            return
        if existing.type == "dir":
            await self.backend.update_inode(existing.id, mtime=_now(), atime=_now())
            return
        if truncate:
            blob_id = await self.backend.put_blob(b"")
            await self.backend.update_inode(
                existing.id,
                content_id=blob_id,
                size=0,
                mtime=_now(),
                atime=_now(),
            )
        else:
            await self.backend.update_inode(existing.id, mtime=_now(), atime=_now())

    # ------------------------------------------------------------------
    # Walk / find / du / glob
    # ------------------------------------------------------------------

    async def _walk(
        self,
        path: str,
        maxdepth: int | None = None,
        on_error: str = "omit",
        **kwargs: Any,
    ) -> AsyncGenerator[tuple[str, list[str], list[str]]]:
        topdown = kwargs.pop("topdown", True)
        if maxdepth is not None and maxdepth < 1:
            raise ValueError("maxdepth must be at least 1")
        norm = self._strip_protocol(path)
        await self._ensure_root()
        try:
            entries = await self._ls(norm, detail=True)
        except (FileNotFoundError, OSError):
            if on_error == "raise":
                raise
            yield norm, [], []
            return
        dirs: list[str] = []
        files: list[str] = []
        sub_dirs: list[str] = []
        for entry in entries:
            name = basename(entry["name"])
            if entry["type"] == "directory":
                dirs.append(name)
                sub_dirs.append(entry["name"])
            else:
                files.append(name)
        if topdown:
            yield norm, dirs, files
        if maxdepth is None or maxdepth > 1:
            next_depth = None if maxdepth is None else maxdepth - 1
            for sub in sub_dirs:
                async for tup in self._walk(
                    sub, maxdepth=next_depth, topdown=topdown, on_error=on_error
                ):
                    yield tup
        if not topdown:
            yield norm, dirs, files

    async def _find(
        self,
        path: str,
        maxdepth: int | None = None,
        withdirs: bool = False,
        detail: bool = False,
        **kwargs: Any,
    ) -> Any:
        norm = self._strip_protocol(path)
        await self._ensure_root()
        results: list[str] = []
        info_map: dict[str, dict[str, Any]] = {}
        async for root, dirs, files in self._walk(norm, maxdepth=maxdepth, topdown=True):
            if withdirs and root != norm:
                results.append(root)
                if detail:
                    info_map[root] = await self._info(root)
            for f in files:
                full = join(root, f)
                results.append(full)
                if detail:
                    info_map[full] = await self._info(full)
        results.sort()
        if detail:
            return {p: info_map[p] for p in results}
        return results

    async def _du(
        self,
        path: str,
        total: bool = True,
        maxdepth: int | None = None,
        **kwargs: Any,
    ) -> Any:
        norm = self._strip_protocol(path)
        await self._ensure_root()
        sizes: dict[str, int] = {}
        async for root, _dirs, files in self._walk(norm, maxdepth=maxdepth, topdown=True):
            for f in files:
                full = join(root, f)
                info = await self._info(full)
                sizes[full] = info["size"]
        if total:
            return sum(sizes.values())
        return sizes

    async def _glob(self, path: str, maxdepth: int | None = None, **kwargs: Any) -> list[str]:
        if maxdepth is not None and maxdepth < 1:
            raise ValueError("maxdepth must be at least 1")
        norm = self._strip_protocol(path)
        await self._ensure_root()

        # Find the root directory to start walking from (everything before first wildcard).
        first_wild = len(norm)
        for ch in ("*", "?", "["):
            i = norm.find(ch)
            if i >= 0 and i < first_wild:
                first_wild = i
        if first_wild == len(norm):
            # No magic — behave like exists.
            if await self._exists(norm):
                return [norm]
            return []
        # Last "/" before first wildcard delimits the literal prefix root.
        prefix_root = norm[:first_wild].rsplit("/", 1)[0] or "/"

        # Build a regex from the full pattern using wcmatch.
        pattern_regexes, _ = wcglob.translate(
            norm,
            flags=wcglob.GLOBSTAR | wcglob.DOTGLOB,
        )
        compiled = [re.compile(rgx) for rgx in pattern_regexes]

        matches: list[str] = []

        async def _scan(start: str, depth_remaining: int | None) -> None:
            try:
                entries = await self._ls(start, detail=True)
            except (FileNotFoundError, OSError):
                return
            for entry in entries:
                full = entry["name"]
                if any(rgx.match(full) for rgx in compiled):
                    matches.append(full)
                if entry["type"] == "directory":
                    if depth_remaining is None or depth_remaining > 1:
                        next_depth = None if depth_remaining is None else depth_remaining - 1
                        await _scan(full, next_depth)

        await _scan(prefix_root, maxdepth)
        # De-dupe and sort for determinism.
        return sorted(set(matches))
