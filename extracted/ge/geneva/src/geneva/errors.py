# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Public Geneva exception types."""


class FatalWorkerError(RuntimeError):
    """Base exception for fatal worker termination during UDF execution."""


class FatalWorkerOOMError(FatalWorkerError):
    """Fatal worker termination caused by OOM."""


class FatalWorkerCrashError(FatalWorkerError):
    """Fatal worker termination caused by worker crash or segfault."""


class FatalWorkerTransientError(FatalWorkerError):
    """Fatal worker termination likely caused by transient infrastructure loss."""


class FatalWorkerExitError(FatalWorkerError):
    """Fatal worker termination with unknown or generic worker-exit cause."""


class ShortFragmentWriteError(FatalWorkerError):
    """A fragment data file was written with fewer rows than it should hold.

    The fragment writer must emit exactly the rows it was handed -- the aligned
    physical layout on the buffered path, or the input batch on the direct-write
    path. A short write would commit a data file whose row count disagrees with the
    fragment manifest, which makes the table unreadable on the next scan (a corrupt
    false success). Raised BEFORE the fragment's dedupe checkpoint is written and
    before commit, so the short file never lands and is not recorded as complete; the
    fragment is then a failed write, retryable on a re-run. Like the other
    ``FatalWorkerError`` subtypes it carries a single human-readable message so it
    round-trips through ``_picklable_remote_error`` across the Ray boundary.
    """


class CorruptCheckpointError(FatalWorkerError):
    """Non-retryable: a checkpoint file cannot be read back.

    Raised when reading a checkpoint triggers a Lance/pyo3 reader panic (e.g. the
    nullable-blob decode bug). Re-reading the same file reproduces the failure, so
    it is fatal and never retried: the affected fragment is isolated so the rest of
    the run still commits, and the job fails with attribution instead of the panic
    killing the worker and Ray crash-looping on the same file.
    """

    def __init__(
        self, key: str, *, path: str | None = None, cause: str | None = None
    ) -> None:
        self.key = key
        self.path = path
        self.cause = cause
        loc = f" at {path}" if path else ""
        detail = f" ({cause})" if cause else ""
        super().__init__(
            f"Checkpoint '{key}'{loc} is unreadable: the Lance reader panicked"
            f"{detail}. The checkpoint is corrupt or triggers a known Lance decode "
            "bug; re-running reproduces it. Remediation: delete this checkpoint and "
            "regenerate it (e.g. bump the UDF version)."
        )


class CheckpointCoverageError(FatalWorkerError):
    """Non-retryable: checkpoint coverage has a gap the writer refuses to null-fill.

    Raised by the fragment writer when a backfill is missing output for some
    of a fragment's live rows — a coverage gap at seal time, or fewer real
    rows than the fragment's live-row count during physical alignment.
    Writing the fragment anyway would silently commit null output for rows
    whose UDF may already have run, so the fragment is failed instead and the
    job fails with attribution. Re-running the backfill reuses the existing
    checkpoints and computes only the missing rows.
    """

    def __init__(
        self,
        frag_id: int,
        *,
        gap_start: int = 0,
        gap_end: int = 0,
        detail: str | None = None,
    ) -> None:
        self.frag_id = frag_id
        self.gap_start = gap_start
        self.gap_end = gap_end
        super().__init__(
            detail
            or (
                f"Fragment {frag_id} is missing output for rows "
                f"[{gap_start}, {gap_end}) in a full-table backfill; refusing "
                "to write null filler. Re-run the backfill to compute the "
                "missing rows."
            )
        )

    def __reduce__(
        self,
    ) -> tuple:  # type: ignore[override]
        # Default BaseException pickling would call cls(message), landing the
        # composed message in ``frag_id``. Rebuild with the real fields so the
        # error survives Ray's exception serialization intact.
        return (
            _rebuild_checkpoint_coverage_error,
            (self.frag_id, self.gap_start, self.gap_end, str(self)),
        )


def _rebuild_checkpoint_coverage_error(
    frag_id: int, gap_start: int, gap_end: int, detail: str
) -> "CheckpointCoverageError":
    """Unpickle helper for :class:`CheckpointCoverageError`."""
    return CheckpointCoverageError(
        frag_id, gap_start=gap_start, gap_end=gap_end, detail=detail
    )


class MergeFallbackTargetError(FatalWorkerError):
    """Non-retryable: a Merge fallback commit would drop an update target.

    The Merge fallback rebuilds the full fragment list from the dataset's
    current state on every conflict retry. An update target missing from that
    snapshot (removed or renumbered by a concurrent writer) would be silently
    omitted from the Merge: the commit would succeed without the fragment's
    new column file, orphaning the written data while the rows are recorded
    as committed. The commit is refused instead.
    """


__all__ = [
    "CheckpointCoverageError",
    "CorruptCheckpointError",
    "FatalWorkerCrashError",
    "FatalWorkerError",
    "FatalWorkerExitError",
    "FatalWorkerOOMError",
    "FatalWorkerTransientError",
    "MergeFallbackTargetError",
    "ShortFragmentWriteError",
]
