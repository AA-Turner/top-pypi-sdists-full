"""Tier 2: sample scrubbed text heads within a byte and file budget, then enrich walked records."""

from __future__ import annotations
from pathlib import Path

from .....sdk.redaction import scrub_text
from probe.cli.imports.folder.walk.evidence import Evidence, FileEvidence, Tier, cluster_by_mtime
from probe.cli.imports.folder.walk.walk import WalkWarnings, walk

#: Head bytes sampled from ONE evidence file. Enough for a header, a docstring,
#: a config block or a table's columns; short enough that a few hundred of them
#: still fit a classification prompt.
SAMPLE_BYTES = 700

#: Total bytes Tier 2 may read across the whole folder. At SAMPLE_BYTES each
#: that is ~1500 files, comfortably above the few hundred a real research folder
#: carries and far below what would stall the import.
SAMPLE_BUDGET_BYTES = 3 * 1024 * 1024

#: Ceiling on sampled FILES, independent of bytes. A folder of ten thousand
#: tiny configs would satisfy the byte budget and still blow the prompt.
SAMPLE_BUDGET_FILES = 600

#: An evidence file at or above this size is sampled but flagged: its head is
#: unlikely to represent it, and a reader should know the sample is a corner of
#: something much larger rather than the whole thing.
LARGE_EVIDENCE_BYTES = 4 * 1024 * 1024


def read_head(path: str, *, limit: int = SAMPLE_BYTES) -> str | None:
    """A text head of `path`, SCRUBBED, or None when it is not usefully text.

    Decoded with ``errors="replace"`` rather than skipped on a decode error: a
    config with one stray byte is still a config, and losing it because of that
    byte is worse than a replacement character in a prompt. Binary is rejected
    by NUL sniffing instead, which is cheap and does not depend on the suffix
    list being complete.

    THE SCRUB IS THE CHOKEPOINT, and it is here rather than at the prompt
    because this is the one place every sample passes through. Filtering by
    FILENAME would not have worked: `.env` is already never sampled (`tier_for`
    calls it TAIL -- no `.env` suffix in EVIDENCE_SUFFIXES, no bare stem in
    EVIDENCE_NAMES), while the files that DO carry keys in an ML folder are
    ordinary sampled evidence -- `.hydra/config.yaml`, `overrides.yaml`, a
    plain `config.yaml` with `wandb_api_key:` in it. Those samples go into an
    agent prompt and into the captured transcript, neither of which passes the
    ingest redaction gate, so an unscrubbed head is a key in team memory.
    """
    try:
        with open(path, "rb") as fh:
            raw = fh.read(limit)
    except OSError:
        return None
    if b"\x00" in raw:
        return None
    text = scrub_text(raw.decode("utf-8", errors="replace")).strip()
    return text or None


def sample(
    files: list[FileEvidence],
    *,
    budget_bytes: int = SAMPLE_BUDGET_BYTES,
    budget_files: int = SAMPLE_BUDGET_FILES,
) -> tuple[list[FileEvidence], int, int, bool]:
    """Tier 2. Returns ``(files, sampled_count, sampled_bytes, budget_hit)``.

    Evidence files are sampled SMALLEST FIRST. That is not arbitrary: a folder's
    identity lives in its readmes and configs, which are small, while its big
    "evidence" files are usually logs whose head is boilerplate. Smallest-first
    spends a fixed budget on the most files, and the ones it drops are the ones
    that would have said least.
    """
    order = sorted(
        (i for i, f in enumerate(files) if f.tier is Tier.EVIDENCE),
        key=lambda i: files[i].size,
    )
    out = list(files)
    used_bytes = 0
    used_files = 0
    budget_hit = False
    for i in order:
        if used_files >= budget_files or used_bytes >= budget_bytes:
            budget_hit = True
            break
        f = files[i]
        head = read_head(f.path)
        if head is None:
            # Reads as binary despite its name. Reclassify rather than pretend:
            # the classifier must not be handed replacement characters as if
            # they meant something.
            out[i] = FileEvidence(
                path=f.path, size=f.size, mtime=f.mtime, tier=Tier.TAIL
            )
            continue
        # WHAT WAS READ, not what survived. `read_head` scrubs, so measuring
        # the returned string charged the budget for the leftovers: a config
        # whose body redacted down to `<redacted>` cost 10 bytes against a
        # budget that exists to bound how much of the folder gets opened. The
        # read is capped at SAMPLE_BYTES, so this is exact.
        used_bytes += min(f.size, SAMPLE_BYTES)
        used_files += 1
        out[i] = FileEvidence(
            path=f.path,
            size=f.size,
            mtime=f.mtime,
            tier=Tier.EVIDENCE,
            sample=head,
            # AGAINST WHAT WAS READ, not against the scrubbed head. `read_head`
            # redacts, so comparing the file size to `len(head)` marked a
            # 400-byte config as truncated because one `wandb_api_key` line
            # became `<redacted>` -- telling the classifier it saw a corner of
            # something larger when it saw the whole file.
            truncated=f.size > LARGE_EVIDENCE_BYTES or f.size > SAMPLE_BYTES,
        )
    return out, used_files, used_bytes, budget_hit


def enrich(root: Path, files: list[FileEvidence]) -> Evidence:
    """PHASE 2. Sample and cluster records phase 1 already walked.

    Split out from :func:`gather` so the caller can run phase 1, answer the
    cheap questions, and leave without paying for this. `sample` opens up to
    :data:`SAMPLE_BUDGET_FILES` files and `cluster_by_mtime` sorts every record
    -- on the filesystems this feature exists for, 600 opens is not free.

    The two callers that must never reach here are the already-imported and
    resume checks in `backfill_run`: both are answered by the census alone, and
    both used to run before the evidence walk happened at all. Folding the
    census into phase 1 without splitting this out would have made the fastest
    path in the flow slower.
    """
    files, n_files, n_bytes, hit = sample(files)
    return Evidence(
        root=str(Path(root).resolve()),
        files=files,
        clusters=cluster_by_mtime(files),
        sampled_files=n_files,
        sampled_bytes=n_bytes,
        sample_budget_hit=hit,
    )


def gather(root: Path, warn: WalkWarnings | None = None, *, include_hidden=()) -> Evidence:
    """Both phases, for callers that always want the whole thing.

    `backfill_run` does NOT use this -- it runs the phases separately so the
    early exits can skip phase 2. Kept because the phases are only separate for
    that one reason, and every other caller wants them together.
    """
    root = Path(root).resolve()
    return enrich(root, list(walk(root, warn, include_hidden=include_hidden)))
