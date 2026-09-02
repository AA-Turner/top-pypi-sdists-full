from __future__ import annotations

import asyncio
from collections import OrderedDict
from dataclasses import dataclass, field
from typing import Any

from matrx_ai.tools.vfs.paths import Inode, split_components

# Cache key types
_InodeKey = tuple[str, str]  # (workspace_id, inode_id)
_NameKey = tuple[str, str | None, str]  # (workspace_id, parent_id|None, name)
_ListingKey = tuple[str, str]  # (workspace_id, parent_id)


@dataclass
class Stats:
    inode_hits: int = 0
    inode_misses: int = 0
    listing_hits: int = 0
    listing_misses: int = 0
    blob_hits: int = 0
    blob_misses: int = 0
    evictions: int = 0


@dataclass
class _BlobEntry:
    data: bytes
    size: int


@dataclass
class _InflightRegistry:
    # Concurrency strategy: in-flight future dedupe (one future per logical key).
    # We picked this over per-key locks because:
    #   * It's strictly cheaper than a Lock per key (no acquire/release ceremony).
    #   * Waiters await the same Future the leader resolves, so the second caller
    #     receives the result without re-entering the cache code path.
    #   * Cleanup is trivial: leader pops the entry on completion (success or failure).
    inode_by_name: dict[_NameKey, asyncio.Future[Inode | None]] = field(default_factory=dict)
    listing: dict[_ListingKey, asyncio.Future[list[Inode]]] = field(default_factory=dict)
    blob: dict[str, asyncio.Future[bytes]] = field(default_factory=dict)


class CachingBackend:
    def __init__(
        self,
        inner: Any,
        *,
        max_inodes: int = 4096,
        max_blob_bytes: int = 16_000_000,
    ) -> None:
        self._inner = inner
        self._max_inodes = max_inodes
        self._max_blob_bytes = max_blob_bytes

        self._inode_by_id: OrderedDict[_InodeKey, Inode] = OrderedDict()
        self._inode_by_parent_name: OrderedDict[_NameKey, str] = OrderedDict()
        self._children_listing: OrderedDict[_ListingKey, list[str]] = OrderedDict()

        self._blob_by_id: OrderedDict[str, _BlobEntry] = OrderedDict()
        self._blob_total_bytes: int = 0

        self._inflight = _InflightRegistry()
        self._stats = Stats()

    # ------------------------------------------------------------------
    # Stats
    # ------------------------------------------------------------------

    @property
    def stats(self) -> Stats:
        return self._stats

    def reset_stats(self) -> None:
        self._stats = Stats()

    # ------------------------------------------------------------------
    # Internal helpers — inode caches
    # ------------------------------------------------------------------

    def _store_inode(self, workspace_id: str, inode: Inode) -> None:
        id_key: _InodeKey = (workspace_id, inode.id)
        name_key: _NameKey = (workspace_id, inode.parent_id, inode.name)

        self._inode_by_id[id_key] = inode
        self._inode_by_id.move_to_end(id_key)
        self._inode_by_parent_name[name_key] = inode.id
        self._inode_by_parent_name.move_to_end(name_key)

        self._evict_inodes_if_needed()

    def _evict_inodes_if_needed(self) -> None:
        # Trim by-id index, then drop matching by-name entries that point to
        # evicted inode ids.
        while len(self._inode_by_id) > self._max_inodes:
            (ws_id, evicted_inode_id), evicted_inode = self._inode_by_id.popitem(last=False)
            self._stats.evictions += 1
            evicted_name_key: _NameKey = (
                ws_id,
                evicted_inode.parent_id,
                evicted_inode.name,
            )
            current_id = self._inode_by_parent_name.get(evicted_name_key)
            if current_id == evicted_inode_id:
                self._inode_by_parent_name.pop(evicted_name_key, None)

        # Mirror the same cap on the name index (defensive — stale entries can
        # exist when inodes are renamed without explicit invalidation).
        while len(self._inode_by_parent_name) > self._max_inodes:
            self._inode_by_parent_name.popitem(last=False)

    def _drop_inode_by_id(self, workspace_id: str, inode_id: str) -> Inode | None:
        return self._inode_by_id.pop((workspace_id, inode_id), None)

    def _drop_name(self, key: _NameKey) -> None:
        self._inode_by_parent_name.pop(key, None)

    def _drop_listing(self, key: _ListingKey) -> None:
        self._children_listing.pop(key, None)

    # ------------------------------------------------------------------
    # Internal helpers — blob cache
    # ------------------------------------------------------------------

    def _store_blob(self, blob_id: str, data: bytes) -> None:
        existing = self._blob_by_id.pop(blob_id, None)
        if existing is not None:
            self._blob_total_bytes -= existing.size
        entry = _BlobEntry(data=data, size=len(data))
        # If a single blob exceeds the budget on its own, refuse to cache it
        # (keeps the cap honest).
        if entry.size > self._max_blob_bytes:
            return
        self._blob_by_id[blob_id] = entry
        self._blob_total_bytes += entry.size
        self._evict_blobs_if_needed()

    def _evict_blobs_if_needed(self) -> None:
        while self._blob_total_bytes > self._max_blob_bytes and self._blob_by_id:
            _, evicted = self._blob_by_id.popitem(last=False)
            self._blob_total_bytes -= evicted.size
            self._stats.evictions += 1

    # ------------------------------------------------------------------
    # Read API
    # ------------------------------------------------------------------

    async def get_inode(
        self,
        workspace_id: str,
        parent_id: str | None,
        name: str,
    ) -> Inode | None:
        name_key: _NameKey = (workspace_id, parent_id, name)
        cached_id = self._inode_by_parent_name.get(name_key)
        if cached_id is not None:
            id_key: _InodeKey = (workspace_id, cached_id)
            cached_inode = self._inode_by_id.get(id_key)
            if cached_inode is not None:
                self._inode_by_id.move_to_end(id_key)
                self._inode_by_parent_name.move_to_end(name_key)
                self._stats.inode_hits += 1
                return cached_inode
            # Stale name entry — fall through to refetch.
            self._inode_by_parent_name.pop(name_key, None)

        self._stats.inode_misses += 1

        inflight = self._inflight.inode_by_name.get(name_key)
        if inflight is not None:
            return await inflight

        loop = asyncio.get_event_loop()
        future: asyncio.Future[Inode | None] = loop.create_future()
        self._inflight.inode_by_name[name_key] = future
        try:
            result = await self._inner.get_inode(workspace_id, parent_id, name)
            if result is not None:
                self._store_inode(workspace_id, result)
            future.set_result(result)
            return result
        except BaseException as exc:
            if not future.done():
                future.set_exception(exc)
            raise
        finally:
            self._inflight.inode_by_name.pop(name_key, None)

    async def get_inode_by_path(self, workspace_id: str, path: str) -> Inode | None:
        # Walk components using cached get_inode — no separate path index because
        # paths shift on rename.
        root = await self.ensure_workspace_root(workspace_id)
        components = split_components(path)
        current: Inode | None = root
        for comp in components:
            if current is None:
                return None
            current = await self.get_inode(workspace_id, current.id, comp)
        return current

    async def list_children(self, workspace_id: str, parent_id: str) -> list[Inode]:
        listing_key: _ListingKey = (workspace_id, parent_id)
        cached_ids = self._children_listing.get(listing_key)
        if cached_ids is not None:
            resolved: list[Inode] | None = []
            missing_ids: list[str] = []
            for child_id in cached_ids:
                inode = self._inode_by_id.get((workspace_id, child_id))
                if inode is None:
                    missing_ids.append(child_id)
                    resolved = None
                    break
                resolved.append(inode)  # type: ignore[union-attr]
            if resolved is not None and not missing_ids:
                self._children_listing.move_to_end(listing_key)
                for inode in resolved:
                    self._inode_by_id.move_to_end((workspace_id, inode.id))
                self._stats.listing_hits += 1
                return list(resolved)
            # Some children evicted from id cache — drop listing and refetch.
            self._children_listing.pop(listing_key, None)

        self._stats.listing_misses += 1

        inflight = self._inflight.listing.get(listing_key)
        if inflight is not None:
            return list(await inflight)

        loop = asyncio.get_event_loop()
        future: asyncio.Future[list[Inode]] = loop.create_future()
        self._inflight.listing[listing_key] = future
        try:
            children = await self._inner.list_children(workspace_id, parent_id)
            ids: list[str] = []
            for child in children:
                self._store_inode(workspace_id, child)
                ids.append(child.id)
            self._children_listing[listing_key] = ids
            self._children_listing.move_to_end(listing_key)
            # Bound the listing cache by the same inode cap (each listing entry
            # is far smaller than an inode, so reuse the limit conservatively).
            while len(self._children_listing) > self._max_inodes:
                self._children_listing.popitem(last=False)
                self._stats.evictions += 1
            future.set_result(children)
            return list(children)
        except BaseException as exc:
            if not future.done():
                future.set_exception(exc)
            raise
        finally:
            self._inflight.listing.pop(listing_key, None)

    async def get_blob(self, blob_id: str) -> bytes:
        cached = self._blob_by_id.get(blob_id)
        if cached is not None:
            self._blob_by_id.move_to_end(blob_id)
            self._stats.blob_hits += 1
            return cached.data

        self._stats.blob_misses += 1

        inflight = self._inflight.blob.get(blob_id)
        if inflight is not None:
            return await inflight

        loop = asyncio.get_event_loop()
        future: asyncio.Future[bytes] = loop.create_future()
        self._inflight.blob[blob_id] = future
        try:
            data = await self._inner.get_blob(blob_id)
            self._store_blob(blob_id, data)
            future.set_result(data)
            return data
        except BaseException as exc:
            if not future.done():
                future.set_exception(exc)
            raise
        finally:
            self._inflight.blob.pop(blob_id, None)

    # ------------------------------------------------------------------
    # Write API — invalidate, then write through, then cache result.
    # ------------------------------------------------------------------

    async def create_inode(self, inode: Inode) -> Inode:
        listing_key: _ListingKey | None = (
            (inode.workspace_id, inode.parent_id) if inode.parent_id is not None else None
        )
        if listing_key is not None:
            self._drop_listing(listing_key)
        result = await self._inner.create_inode(inode)
        self._store_inode(result.workspace_id, result)
        return result

    async def update_inode(self, inode_id: str, **fields: Any) -> Inode:
        # Locate cached entry (any workspace) so we know which name/listing keys
        # to invalidate. Inode IDs are unique across workspaces in practice, but
        # we walk to be safe.
        old_workspace_id: str | None = None
        old_inode: Inode | None = None
        for (ws_id, candidate_id), inode in self._inode_by_id.items():
            if candidate_id == inode_id:
                old_workspace_id = ws_id
                old_inode = inode
                break

        if old_inode is not None and old_workspace_id is not None:
            self._drop_inode_by_id(old_workspace_id, inode_id)
            self._drop_name((old_workspace_id, old_inode.parent_id, old_inode.name))
            self._drop_listing((old_workspace_id, old_inode.parent_id or ""))
            if old_inode.parent_id is not None:
                self._drop_listing((old_workspace_id, old_inode.parent_id))

            new_parent = fields.get("parent_id", old_inode.parent_id)
            if new_parent != old_inode.parent_id and new_parent is not None:
                self._drop_listing((old_workspace_id, new_parent))

        result = await self._inner.update_inode(inode_id, **fields)
        # If the new parent wasn't known to us pre-call, invalidate after.
        self._drop_listing((result.workspace_id, result.parent_id or ""))
        if result.parent_id is not None:
            self._drop_listing((result.workspace_id, result.parent_id))
        self._store_inode(result.workspace_id, result)
        return result

    async def delete_inode(self, inode_id: str) -> None:
        # Find cached parent so we can invalidate the right listing.
        target_workspace_id: str | None = None
        target_inode: Inode | None = None
        for (ws_id, candidate_id), inode in self._inode_by_id.items():
            if candidate_id == inode_id:
                target_workspace_id = ws_id
                target_inode = inode
                break

        if target_inode is not None and target_workspace_id is not None:
            self._drop_inode_by_id(target_workspace_id, inode_id)
            self._drop_name((target_workspace_id, target_inode.parent_id, target_inode.name))
            if target_inode.parent_id is not None:
                self._drop_listing((target_workspace_id, target_inode.parent_id))

        await self._inner.delete_inode(inode_id)

    async def put_blob(self, data: bytes) -> str:
        blob_id = await self._inner.put_blob(data)
        self._store_blob(blob_id, data)
        return blob_id

    async def ensure_workspace_root(self, workspace_id: str) -> Inode:
        # Cheap to look up cached root via name index keyed on (ws, None, "/").
        cached_id = self._inode_by_parent_name.get((workspace_id, None, "/"))
        if cached_id is not None:
            cached_inode = self._inode_by_id.get((workspace_id, cached_id))
            if cached_inode is not None:
                self._inode_by_id.move_to_end((workspace_id, cached_id))
                self._inode_by_parent_name.move_to_end((workspace_id, None, "/"))
                self._stats.inode_hits += 1
                return cached_inode

        self._stats.inode_misses += 1
        root = await self._inner.ensure_workspace_root(workspace_id)
        self._store_inode(workspace_id, root)
        return root
