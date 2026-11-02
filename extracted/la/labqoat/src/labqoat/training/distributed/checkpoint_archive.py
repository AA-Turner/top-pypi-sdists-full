"""Bounded deterministic group archives with per-rank integrity checks before restoration."""

import hashlib
import shutil
import tarfile
from collections.abc import Sequence
from dataclasses import replace
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Literal, cast

from labqoat.compute.checkpoint_group import CheckpointGroup
from labqoat.compute.checkpoint_rank import CheckpointRank
from labqoat.compute.checkpoint_recovery import CheckpointRecovery
from labqoat.storage.verified_file import VerifiedFile
from labqoat.training.distributed.rank_snapshot import RankSnapshot


class CheckpointArchive:
    """Keep all ranks in one pinned immutable payload and never deserialize framework bytes."""

    @classmethod
    def pack(
        cls,
        destination: Path,
        snapshots: Sequence[RankSnapshot],
        recovery: CheckpointRecovery,
        *,
        backend: Literal["gloo", "nccl"],
        max_bytes: int = 64 * 1024**3,
    ) -> CheckpointRecovery:
        """Publish only a complete common update boundary and reverify bytes after archive construction."""
        group = CheckpointGroup(backend=backend, ranks=tuple(snapshot.inventory() for snapshot in snapshots))
        coordinated = replace(recovery, group=group)
        coordinated.document(recovery.progress.update)
        cls._size(group, max_bytes)
        with tarfile.open(destination, "w", format=tarfile.USTAR_FORMAT) as archive:
            for snapshot, rank in zip(snapshots, group.ranks, strict=True):
                entry = tarfile.TarInfo(rank.path)
                entry.size = rank.byte_size
                with snapshot.payload.open("rb") as source:
                    archive.addfile(entry, source)
        with tarfile.open(destination, "r:") as archive:
            cls._verify(archive, group)
        return coordinated

    @classmethod
    def restore_rank(
        cls, payload: Path, group: CheckpointGroup, rank: int, destination: Path, *, max_bytes: int = 64 * 1024**3
    ) -> Path:
        """Verify the entire coordinated payload before exposing any selected rank to an adapter."""
        selected = cls._rank(group, rank)
        cls._size(group, max_bytes)
        destination.parent.mkdir(parents=True, exist_ok=True)
        with tarfile.open(payload, "r:") as archive, TemporaryDirectory(dir=destination.parent) as temporary:
            cls._verify(archive, group)
            captured = Path(temporary) / "rank"
            source = cast(tarfile.ExFileObject, archive.extractfile(selected.path))
            with source, captured.open("wb") as output:
                shutil.copyfileobj(source, output)
            VerifiedFile.validate(captured, selected.sha256.removeprefix("sha256:"), selected.byte_size)
            captured.replace(destination)
        return destination

    @staticmethod
    def _rank(group: CheckpointGroup, rank: int) -> CheckpointRank:
        """Reject ambiguous, oversized and missing group membership before opening an archive."""
        ids = tuple(item.rank for item in group.ranks)
        if not 2 <= len(ids) <= 256 or ids != tuple(range(len(ids))) or type(rank) is not int or rank not in ids:
            raise ValueError("Invalid coordinated rank membership")
        return group.ranks[rank]

    @staticmethod
    def _size(group: CheckpointGroup, maximum: int) -> None:
        """Bound total restored bytes before parsing archive entries or creating scratch files."""
        if type(maximum) is not int or maximum < 0:
            raise ValueError("Checkpoint byte limit must be a nonnegative integer")
        if any(type(rank.byte_size) is not int or rank.byte_size < 0 for rank in group.ranks):
            raise ValueError("Invalid checkpoint byte inventory")
        if sum(rank.byte_size for rank in group.ranks) > maximum:
            raise ValueError("Coordinated checkpoint exceeds the configured byte limit")

    @classmethod
    def _verify(cls, archive: tarfile.TarFile, group: CheckpointGroup) -> None:
        """Stop at the bounded member count; reject duplicates, extra entries, links and byte mismatches."""
        cls._rank(group, 0)
        expected = {rank.path: rank for rank in group.ranks}
        for entry in archive:
            rank = expected.pop(entry.name, None)
            if rank is None or not entry.isfile() or entry.size != rank.byte_size:
                raise ValueError("Archive does not match its coordinated rank inventory")
            source = cast(tarfile.ExFileObject, archive.extractfile(entry))
            with source:
                digest = hashlib.file_digest(source, "sha256").hexdigest()
            if f"sha256:{digest}" != rank.sha256:
                raise ValueError("Coordinated rank payload digest mismatch")
        if expected:
            raise ValueError("Coordinated checkpoint is missing ranks")
