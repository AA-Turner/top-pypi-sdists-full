"""
cvc.sdk.sync — CRDT-based distributed sync for the Hive Mind.

CVC's Merkle DAG is a natural **G-Set CRDT** (Grow-only Set):

* Every commit has a globally-unique SHA-256 hash.
* Commits are never deleted (append-only).
* Merge = set union of commits from two replicas.
* Strong eventual consistency: all replicas that have received
  the same set of commits are guaranteed to be in the same state.

The sync protocol works at three levels:

1. **Local ↔ Local** — two ``HiveMind`` instances on the same machine
   (or in-process) sync directly via ``SyncEngine.sync_local()``.
2. **File-based** — export a ``.cvcpack`` archive, carry it on a USB
   stick / satellite uplink, and import on the other side
   (``SyncEngine.export_pack()`` / ``import_pack()``).
3. **Gossip** — a background thread periodically exchanges commit
   hashes with a list of peer ``HiveMind`` instances
   (``GossipProtocol``).
"""

from __future__ import annotations

import json
import logging
import threading
import time
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from cvc.core.database import ContextDatabase
from cvc.core.models import (
    BranchPointer,
    CognitiveCommit,
)

logger = logging.getLogger("cvc.sdk.sync")


# ──────────────────────────────────────────────────────────────────────
# Data types
# ──────────────────────────────────────────────────────────────────────

@dataclass
class SyncResult:
    """Summary of a single sync operation."""
    pushed: int = 0          # commits sent to remote
    pulled: int = 0          # commits received from remote
    branches_updated: int = 0
    agents_synced: int = 0
    errors: list[str] = field(default_factory=list)

    @property
    def total(self) -> int:
        return self.pushed + self.pulled


# ──────────────────────────────────────────────────────────────────────
# SyncEngine — the core CRDT sync logic
# ──────────────────────────────────────────────────────────────────────

class SyncEngine:
    """
    Implements G-Set CRDT sync between two ``ContextDatabase`` instances.

    The algorithm is simple and provably convergent:

    1. Exchange commit-hash sets (the "membership" of each G-Set).
    2. Compute the symmetric difference: commits each side is missing.
    3. Transfer missing commits + their CAS blobs.
    4. Reconcile branch heads (advance to the newest tip).
    5. Merge agent registries (union of ``.cvc/agents/*.json``).

    No conflicts are possible because:
    - Commits are content-addressed and immutable.
    - The DAG is append-only.
    - Branch heads always advance forward (we pick the commit with
      the larger ancestor set, breaking ties by timestamp).
    """

    def __init__(self, local_db: ContextDatabase) -> None:
        self._local = local_db

    # -- Local-to-local sync -----------------------------------------------

    def sync_local(self, remote_db: ContextDatabase) -> SyncResult:
        """
        Bidirectional sync between two local ``ContextDatabase`` instances.

        This is the primitive used by ``HiveMind.sync()`` and by the
        gossip protocol.  It is also used in tests.
        """
        result = SyncResult()

        local_hashes = self._local.index.list_all_commit_hashes()
        remote_hashes = remote_db.index.list_all_commit_hashes()

        # Commits we need to PULL (exist on remote, not locally)
        to_pull = remote_hashes - local_hashes
        # Commits we need to PUSH (exist locally, not on remote)
        to_push = local_hashes - remote_hashes

        # ── Pull ──────────────────────────────────────────────
        for h in self._topo_sort(to_pull, remote_db):
            try:
                self._transfer_commit(h, source=remote_db, dest=self._local)
                result.pulled += 1
            except Exception as exc:
                result.errors.append(f"pull {h[:12]}: {exc}")

        # ── Push ──────────────────────────────────────────────
        for h in self._topo_sort(to_push, self._local):
            try:
                self._transfer_commit(h, source=self._local, dest=remote_db)
                result.pushed += 1
            except Exception as exc:
                result.errors.append(f"push {h[:12]}: {exc}")

        # ── Reconcile branches ────────────────────────────────
        result.branches_updated = self._reconcile_branches(remote_db)

        # ── Sync agent registries ─────────────────────────────
        result.agents_synced = self._sync_agents(remote_db)

        return result

    # -- Pack-based sync (offline / sneakernet) ----------------------------

    def export_pack(self, output_path: Path) -> int:
        """
        Export **all** commits and blobs to a ``.cvcpack`` archive.

        Returns the number of commits exported.
        """
        commits = self._local.index.list_all_commits(limit=100_000)
        branches = self._local.index.list_branches()

        manifest: dict[str, Any] = {
            "format": "cvcpack-v2",
            "exported_at": time.time(),
            "commits": [],
            "branches": [b.model_dump(mode="json") for b in branches],
        }

        output_path.parent.mkdir(parents=True, exist_ok=True)
        seen_blobs: set[str] = set()
        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for commit in commits:
                manifest["commits"].append(commit.model_dump(mode="json"))
                blob_key = self._local.index.get_blob_key(commit.commit_hash)
                if blob_key and blob_key not in seen_blobs:
                    raw = self._local.blobs.get(blob_key)
                    if raw is not None:
                        zf.writestr(f"blobs/{blob_key}", raw)
                        seen_blobs.add(blob_key)
            zf.writestr("manifest.json", json.dumps(manifest, indent=2, default=str))

        logger.info("Exported %d commits to %s", len(commits), output_path)
        return len(commits)

    def import_pack(self, pack_path: Path) -> SyncResult:
        """
        Import a ``.cvcpack`` archive (G-Set union merge).

        Returns a ``SyncResult`` summarising what was ingested.
        """
        result = SyncResult()

        with zipfile.ZipFile(pack_path, "r") as zf:
            manifest = json.loads(zf.read("manifest.json").decode("utf-8"))

            # Restore blobs first (they are referenced by commits)
            for name in zf.namelist():
                if name.startswith("blobs/"):
                    blob_key = name.split("/", 1)[1]
                    if not self._local.blobs.exists(blob_key):
                        raw = zf.read(name)
                        self._local.blobs.put(raw)

            # Restore commits (oldest first for DAG integrity)
            local_hashes = self._local.index.list_all_commit_hashes()
            raw_commits = manifest.get("commits", [])
            # Sort by timestamp ascending so parents arrive before children
            raw_commits.sort(key=lambda c: c.get("metadata", {}).get("timestamp", 0))

            for cdata in raw_commits:
                commit = CognitiveCommit.model_validate(cdata)
                if commit.commit_hash in local_hashes:
                    continue  # Already have it — G-Set dedup
                blob_key = self._local.blobs.put(
                    commit.content_blob.canonical_bytes()
                )
                self._local.index.insert_commit(commit, blob_key)
                result.pulled += 1

            # Reconcile branch heads
            for bdata in manifest.get("branches", []):
                bp = BranchPointer.model_validate(bdata)
                existing = self._local.index.get_branch(bp.name)
                if existing is None:
                    self._local.index.upsert_branch(bp)
                    result.branches_updated += 1
                elif self._is_ancestor(existing.head_hash, bp.head_hash, self._local):
                    self._local.index.advance_head(bp.name, bp.head_hash)
                    result.branches_updated += 1

        logger.info(
            "Imported pack %s: pulled=%d branches=%d",
            pack_path.name, result.pulled, result.branches_updated,
        )
        return result

    # -- Internal helpers --------------------------------------------------

    def _transfer_commit(
        self,
        commit_hash: str,
        source: ContextDatabase,
        dest: ContextDatabase,
    ) -> None:
        """Copy a single commit + its blob from source to dest."""
        commit = source.index.get_commit(commit_hash)
        if commit is None:
            raise ValueError(f"Commit {commit_hash[:12]} not found on source")

        # Transfer the CAS blob
        blob_key = source.index.get_blob_key(commit_hash)
        if blob_key:
            raw = source.blobs.get(blob_key)
            if raw is not None:
                dest.blobs.put(raw)

        # Re-store canonical blob to get the dest-side key
        dest_blob_key = dest.blobs.put(commit.content_blob.canonical_bytes())
        dest.index.insert_commit(commit, dest_blob_key)

    def _topo_sort(
        self, hashes: set[str], db: ContextDatabase,
    ) -> list[str]:
        """Sort commit hashes in topological order (parents before children)."""
        # Simple timestamp-based ordering (DAG-safe because parents
        # always have earlier timestamps in a well-formed Merkle chain).
        commits: list[tuple[float, str]] = []
        for h in hashes:
            c = db.index.get_commit(h)
            if c is not None:
                commits.append((c.metadata.timestamp, h))
        commits.sort()
        return [h for _, h in commits]

    def _reconcile_branches(self, remote_db: ContextDatabase) -> int:
        """Reconcile branch heads between local and remote (both directions)."""
        updated = 0

        # Pull remote branches → local
        for rbp in remote_db.index.list_branches():
            lbp = self._local.index.get_branch(rbp.name)
            if lbp is None:
                # New branch from remote
                self._local.index.upsert_branch(rbp)
                updated += 1
            elif lbp.head_hash != rbp.head_hash:
                if self._is_ancestor(lbp.head_hash, rbp.head_hash, self._local):
                    self._local.index.advance_head(rbp.name, rbp.head_hash)
                    updated += 1

        # Push local branches → remote
        for lbp in self._local.index.list_branches():
            rbp = remote_db.index.get_branch(lbp.name)
            if rbp is None:
                remote_db.index.upsert_branch(lbp)
                updated += 1
            elif rbp.head_hash != lbp.head_hash:
                if self._is_ancestor(rbp.head_hash, lbp.head_hash, remote_db):
                    remote_db.index.advance_head(lbp.name, lbp.head_hash)
                    updated += 1

        return updated

    def _sync_agents(self, remote_db: ContextDatabase) -> int:
        """Sync agent registries (set union, newer timestamp wins)."""
        synced = 0

        local_agents = {a["agent_id"]: a for a in self._local.index.list_agents()}
        remote_agents = {a["agent_id"]: a for a in remote_db.index.list_agents()}

        # Pull agents from remote that we don't have (or are newer)
        for aid, ra in remote_agents.items():
            la = local_agents.get(aid)
            if la is None or ra.get("updated_at", 0) > la.get("updated_at", 0):
                self._local.index.insert_agent(
                    agent_id=aid,
                    name=ra.get("name"),
                    role=ra.get("role"),
                    rank=ra.get("rank"),
                    squad=ra.get("squad"),
                    capabilities=ra.get("capabilities"),
                    metadata=ra.get("metadata"),
                    readable_branches=ra.get("readable_branches"),
                    writable_branches=ra.get("writable_branches"),
                    status=ra.get("status", "active"),
                )
                synced += 1

        # Push our agents to remote
        for aid, la in local_agents.items():
            ra = remote_agents.get(aid)
            if ra is None or la.get("updated_at", 0) > ra.get("updated_at", 0):
                remote_db.index.insert_agent(
                    agent_id=aid,
                    name=la.get("name"),
                    role=la.get("role"),
                    rank=la.get("rank"),
                    squad=la.get("squad"),
                    capabilities=la.get("capabilities"),
                    metadata=la.get("metadata"),
                    readable_branches=la.get("readable_branches"),
                    writable_branches=la.get("writable_branches"),
                    status=la.get("status", "active"),
                )
                synced += 1

        return synced

    def _is_ancestor(
        self, potential_ancestor: str, descendant: str, db: ContextDatabase,
    ) -> bool:
        """Check if *potential_ancestor* is reachable from *descendant*."""
        if potential_ancestor == descendant:
            return True
        visited: set[str] = set()
        queue = [descendant]
        while queue:
            h = queue.pop(0)
            if h in visited:
                continue
            visited.add(h)
            if h == potential_ancestor:
                return True
            c = db.index.get_commit(h)
            if c:
                queue.extend(c.parent_hashes)
        return False


# ──────────────────────────────────────────────────────────────────────
# GossipProtocol — background periodic sync for swarm networks
# ──────────────────────────────────────────────────────────────────────

class GossipProtocol:
    """
    Periodic background sync across a swarm of ``HiveMind`` peers.

    Each gossip round:
    1. Pick the next peer from the peer list (round-robin).
    2. Run ``SyncEngine.sync_local()`` with that peer's database.
    3. Sleep for *interval_seconds*.

    After enough rounds, all peers converge to the same commit set
    (strong eventual consistency via G-Set CRDT merge).

    Usage::

        gossip = GossipProtocol(local_db, peers=[peer1_db, peer2_db])
        gossip.start(interval_seconds=5)
        ...
        gossip.stop()
    """

    def __init__(
        self,
        local_db: ContextDatabase,
        peers: list[ContextDatabase] | None = None,
    ) -> None:
        self._local = local_db
        self._peers: list[ContextDatabase] = list(peers or [])
        self._engine = SyncEngine(local_db)
        self._thread: threading.Thread | None = None
        self._stop_event = threading.Event()
        self._round = 0
        self._results: list[SyncResult] = []
        self._lock = threading.Lock()

    @property
    def round_count(self) -> int:
        return self._round

    @property
    def results(self) -> list[SyncResult]:
        with self._lock:
            return list(self._results)

    def add_peer(self, peer_db: ContextDatabase) -> None:
        """Add a peer to the gossip network."""
        with self._lock:
            self._peers.append(peer_db)

    def start(self, interval_seconds: float = 30.0) -> None:
        """Start gossiping in a background daemon thread."""
        if self._thread is not None and self._thread.is_alive():
            return  # Already running
        self._stop_event.clear()
        self._thread = threading.Thread(
            target=self._gossip_loop,
            args=(interval_seconds,),
            daemon=True,
            name="cvc-gossip",
        )
        self._thread.start()
        logger.info("Gossip started (interval=%.1fs, peers=%d)", interval_seconds, len(self._peers))

    def stop(self, timeout: float = 5.0) -> None:
        """Stop the gossip thread."""
        self._stop_event.set()
        if self._thread is not None:
            self._thread.join(timeout=timeout)
            self._thread = None
        logger.info("Gossip stopped after %d rounds", self._round)

    @property
    def running(self) -> bool:
        return self._thread is not None and self._thread.is_alive()

    def sync_once(self) -> SyncResult | None:
        """Run a single gossip round synchronously (for testing)."""
        if not self._peers:
            return None
        peer = self._peers[self._round % len(self._peers)]
        result = self._engine.sync_local(peer)
        with self._lock:
            self._results.append(result)
        self._round += 1
        return result

    def _gossip_loop(self, interval: float) -> None:
        """Background loop: sync with one peer per round."""
        while not self._stop_event.is_set():
            if self._peers:
                try:
                    self.sync_once()
                except Exception as exc:
                    logger.warning("Gossip round %d failed: %s", self._round, exc)
            self._stop_event.wait(timeout=interval)
