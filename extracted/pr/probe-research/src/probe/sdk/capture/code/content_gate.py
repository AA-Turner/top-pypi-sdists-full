"""what every captured file passes: one read that hashes it and scans it (compressed members included) within the time budget."""

from __future__ import annotations
import hashlib
import os
import time
from typing import Any
from ... import secret_gate as _secret_gate

#: The largest file whose bytes a capture will upload: the credential gate's own
#: inspection limit (``secret_gate.ScanPolicy.max_bytes``, which is also the
#: server's upload ceiling). A file above it is not scanned, so its bytes never
#: leave; it is RECORDED instead (a file-path reference: path, host, sha256), the
#: same outcome as a file over ``reference_over_bytes``. Before this, such a file
#: was classified for upload and then refused by the transport or the server.
CONTENT_SCAN_MAX_BYTES = _secret_gate.ScanPolicy().max_bytes
#: Seconds ONE file may spend in the content scan, and seconds ONE snapshot may
#: spend scanning in total. The scanner reads text dense in its keywords at
#: ~4 MB/s -- an LLM training log printing `tokens/s` on every line is exactly
#: that, and 60 MB of it took 16-20 s at `probe.init()`. Capture stays broad (D7,
#: D12: every file up to 64 MiB); the budget is a safety stop, never a size rule.
#: A file whose scan runs past its budget, or a large (> FULL_SCAN_MAX_BYTES)
#: non-source file reached after the snapshot's budget is spent, is WITHHELD
#: with reason ``scan_budget``: recorded, never uploaded unscanned. Small files
#: and source files are always scanned, and the file budget holds for them too:
#: a big file's clock is read between chunks, a small file's between the
#: scanner's hits (``credential_rules``' ``deadline``; one regex pass cannot be
#: interrupted, so a small file can run a little past it). Override with the
#: env vars below; ``0`` removes a budget.
FILE_SCAN_BUDGET_SEC = 3.0
SNAPSHOT_SCAN_BUDGET_SEC = 15.0
FILE_SCAN_BUDGET_ENV = "PROBE_SNAPSHOT_FILE_SCAN_BUDGET_SEC"
SNAPSHOT_SCAN_BUDGET_ENV = "PROBE_SNAPSHOT_SCAN_BUDGET_SEC"
SCAN_BUDGET_REASON = "scan_budget"


def _budget_seconds(env: str, default: float) -> float:
    raw = os.environ.get(env, "").strip()
    try:
        value = float(raw) if raw else default
    except ValueError:
        return default
    if value != value or value < 0:  # NaN or negative: not a budget
        return default
    return float("inf") if value == 0 else value


#: Up to this size a file gets the scanner's full rule set WITH its decoding
#: layer -- base64, ``%xx`` and ``\\uXXXX`` escapes decoded and scanned again --
#: read next to each rule's keywords. Above it, the quick check (no decoding),
#: streamed in bounded chunks. Measured 2026-09-27 on 2,000 files / 35.7 MB of
#: this repo: quick 2.5 s, quick + decoding 4.0 s, un-windowed ``scan()`` 12.7 s,
#: ``secret_gate.inspect_bytes`` 31.7 s. Almost every file a repo holds is well
#: under 2 MiB, so almost every file gets the decoding pass.
FULL_SCAN_MAX_BYTES = 2 * 1024 * 1024

#: Chunks for the streamed quick scan of a big file, and how much of the previous
#: chunk each one re-reads: wider than the longest span a rule can match (a
#: private-key block, ~33K) plus a keyword's lead, so nothing is missed at a seam.
_SCAN_CHUNK = 1 << 20
_SCAN_OVERLAP = 40_000

#: A WITHHELD entry (a file left out for a credential) carries its sha256 only
#: from this size up. Below it the file is short enough that its hash could be
#: brute-forced back to a password offline, and the manifest is readable by the
#: whole team; path, mode and size still identify it.
WITHHELD_HASH_MIN_BYTES = 1024 * 1024


#: Notebooks up to this size are also read as their CODE (`_notebook_rules`).
#: The JSON of an `.ipynb` escapes every `"` inside a cell
#: (`OPENAI_API_KEY = \"...\"`), which hides a quoted literal from every rule
#: that reads quotes. Outputs (plots as base64) are what make a notebook big,
#: and parsing holds a few times the file, so there is a ceiling.
NOTEBOOK_DECODE_MAX_BYTES = 16 * 1024 * 1024


#: Decompressed bytes one archive may yield to the scan; past it the archive is
#: withheld for the scan budget (a small gzip can expand to gigabytes).
ARCHIVE_EXPAND_MAX_BYTES = 256 * 1024 * 1024
_UNREADABLE_ARCHIVE = "unreadable-archive"
_NAME_IN_ARCHIVE = "credential-name-in-archive"


def _compressed_kind(head: bytes) -> str | None:
    """The compression wrapping a file, from its first bytes: its CONTENT is not
    in its raw bytes, so the raw scan cannot see it. A zip is listed here too;
    ``_archive_rules`` only opens its compressed members (a stored member -- a
    torch checkpoint, say -- is already plain in the raw bytes)."""
    if head[:2] == b"\x1f\x8b":
        return "gzip"
    if head[:3] == b"BZh":
        return "bz2"
    if head[:6] == b"\xfd7zXZ\x00":
        return "xz"
    if head[:4] in (b"PK\x03\x04", b"PK\x05\x06"):
        return "zip"
    return None


def _archive_streams(path: str, kind: str):
    """``(member name, readable)`` pairs to scan: the members of a compressed
    tar (their names checked too), the compressed members of a zip, or the one
    decompressed stream of a plain `.gz`/`.bz2`/`.xz`. One level deep."""
    import bz2
    import gzip
    import lzma
    import tarfile
    import zipfile

    if kind == "zip":
        with zipfile.ZipFile(path) as zf:
            for info in zf.infolist():
                if info.is_dir() or info.compress_type == zipfile.ZIP_STORED:
                    continue
                with zf.open(info) as member:
                    yield info.filename, member
        return
    opener = {"gzip": gzip.open, "bz2": bz2.open, "xz": lzma.open}[kind]
    tar_mode = {"gzip": "r|gz", "bz2": "r|bz2", "xz": "r|xz"}[kind]
    try:
        tar = tarfile.open(path, mode=tar_mode)
    except tarfile.ReadError:
        tar = None
    if tar is not None:
        with tar:
            for info in tar:
                if not info.isfile():
                    continue
                member = tar.extractfile(info)
                if member is not None:
                    yield info.name, member
        return
    with opener(path, "rb") as stream:
        yield os.path.basename(path).rsplit(".", 1)[0], stream


def _archive_rules(
    path: str, kind: str, allowed: float, spent: float
) -> tuple[set[str], float, bool]:
    """``(rules, seconds spent in total, out of budget)`` for what a compressed
    archive holds: each member's NAME against the credential-name rules and its
    decompressed bytes through the same chunked scan as a big file, under the
    same time budget. An archive that cannot be opened (corrupt, encrypted) is a
    finding: its bytes are not uploaded unread."""
    rules: set[str] = set()
    expanded = 0
    try:
        for member_name, stream in _archive_streams(path, kind):
            base = member_name.rsplit("/", 1)[-1]
            if _skip_reason(base) == "secret" or _in_secret_dir(member_name):
                rules.add(_NAME_IN_ARCHIVE)
            carry = b""
            codec: str | None = None
            while True:
                chunk = stream.read(_SCAN_CHUNK)
                if not chunk:
                    break
                if not carry:
                    codec = _utf16_codec(chunk)
                expanded += len(chunk)
                if expanded > ARCHIVE_EXPAND_MAX_BYTES:
                    return rules, spent, True
                window = carry + chunk
                started = time.monotonic()
                rules |= _chunk_rules(window, base, codec)
                spent += time.monotonic() - started
                carry = window[-_SCAN_OVERLAP:]
                if spent >= allowed:
                    return rules, spent, True
    except Exception:  # noqa: BLE001 -- corrupt, truncated, encrypted: not readable
        rules.add(_UNREADABLE_ARCHIVE)
    return rules, spent, False


def _read_for_capture(
    path: str,
    name: str,
    *,
    scan: bool,
    limit: int,
    file_budget: float = float("inf"),
    total_left: float = float("inf"),
) -> tuple[str, int, tuple[str, ...], float, bool]:
    """``(sha256, size, credential rules, seconds scanning, budget ran out)`` from
    ONE read, so what is scanned is exactly what was hashed. Nothing past
    ``limit`` is scanned (the file is then too large to upload at all). A file up
    to FULL_SCAN_MAX_BYTES is scanned whole; a bigger one in overlapping chunks,
    so memory stays at a few MB whatever its size (a 60 MB keyword-dense log held
    ~530 MB before), UTF-16 included (the codec is read from the first chunk and
    windows stay on even offsets). The time budgets are checked between chunks:
    past ``file_budget`` seconds on this file -- or, for a non-source file, past
    what is ``total_left`` of the snapshot's budget -- the scan stops, hashing
    goes on, and the caller withholds the file. A whole-scanned file gets
    ``file_budget`` too, as ``credential_rules``' deadline. A compressed archive
    is then opened and its members scanned too (``_archive_rules``), and a
    notebook too big to scan whole has its code cells read up to
    NOTEBOOK_DECODE_MAX_BYTES (``_notebook_rules``)."""
    h = hashlib.sha256()
    rules: set[str] = set()
    n = 0
    spent = 0.0
    out_of_budget = False
    source = name.lower().endswith(_SOURCE_SUFFIXES)
    allowed = file_budget if source else min(file_budget, total_left)
    head = b""
    codec: str | None = None
    with open(path, "rb") as fh:
        size = os.fstat(fh.fileno()).st_size
        whole = scan and size <= FULL_SCAN_MAX_BYTES
        if scan and not whole and allowed <= 0:
            out_of_budget = True  # the snapshot's budget is spent: do not start
        small: bytearray | None = bytearray() if whole else None
        notebook: bytearray | None = (
            bytearray()
            if scan and not whole and size <= NOTEBOOK_DECODE_MAX_BYTES and name.lower().endswith(".ipynb")
            else None
        )
        carry = b""
        for chunk in iter(lambda: fh.read(_SCAN_CHUNK), b""):
            h.update(chunk)
            if n == 0:
                head = chunk[:4096]
                codec = _utf16_codec(head)
            n += len(chunk)
            if not scan or n > limit or out_of_budget:
                small = notebook = None
                continue
            if notebook is not None:
                notebook.extend(chunk)
                if len(notebook) > NOTEBOOK_DECODE_MAX_BYTES:
                    notebook = None  # grew while being read: the raw scan still covers it
            if small is not None:
                small.extend(chunk)
                if len(small) <= FULL_SCAN_MAX_BYTES:
                    continue
                # Grew past the full-scan size while being read: stream the rest.
                window, small = small, None
            else:
                window = carry + chunk
            started = time.monotonic()
            rules |= _chunk_rules(window, name, codec)
            spent += time.monotonic() - started
            carry = bytes(window[-_SCAN_OVERLAP:])
            if spent >= allowed:
                out_of_budget = True
    if small is not None and n <= limit and not out_of_budget:
        started = time.monotonic()
        try:
            rules |= set(credential_rules(small, name, deadline=started + file_budget))
        except _ScanOutOfTime:
            out_of_budget = True
        spent += time.monotonic() - started
    if notebook is not None and n <= limit and not out_of_budget:
        started = time.monotonic()
        try:
            rules |= _notebook_rules(notebook, deadline=started + max(0.0, allowed - spent))
        except _ScanOutOfTime:
            out_of_budget = True
        except Exception:  # noqa: BLE001 -- fail closed, as credential_rules does
            rules.add("inspection-failed")
        spent += time.monotonic() - started
    kind = _compressed_kind(head) if scan and n <= limit and not out_of_budget else None
    if kind is not None:
        archive_rules, spent, out_of_budget = _archive_rules(path, kind, allowed, spent)
        rules |= archive_rules
    return h.hexdigest(), n, tuple(sorted(rules)), spent, out_of_budget and n <= limit


class _ContentGate:
    """What every captured file passes before it can be classified for upload.

    A snapshot stores EXACT bytes (restore verifies each sha256), so unlike
    ``log_artifact`` it cannot redact: a file with a credential is WITHHELD. It
    stays in the manifest as ``source: "withheld"`` with its size and reason (and
    its sha256 only from WITHHELD_HASH_MIN_BYTES up), so the tree's identity does
    not depend on whether a scan ran, and it is REPORTED in ``skipped`` (reason
    ``secret``, ``found_in: content``, the rule names). Live, before this
    existed: an untracked `.env` and a scratch file with a `probe_pat_` token
    were stored byte-identical from a git repo.

    Every upload path re-verifies the recorded sha256 on the descriptor it
    streams and pins it on the PUT, so nothing can change between this check
    and storage.

    ``scan`` switches the check. ``budget`` bounds it: the bytes that could be
    uploaded (``max_upload_bytes``); past it the capture would be refused as too
    large anyway, so it is refused HERE, before paying to scan what cannot ship.
    ``budget=None`` scans without a bound (a capture that will not upload).

    Time is bounded too (FILE_SCAN_BUDGET_SEC for every file,
    SNAPSHOT_SCAN_BUDGET_SEC for large non-source ones): a file the scan could
    not finish in time is withheld with reason ``scan_budget``, because
    unscanned bytes are never uploaded, and the run warns about it.
    """

    def __init__(self, *, scan: bool = True, budget: int | None = None) -> None:
        self.scan = scan
        self.budget = budget
        self.scanned = 0
        self.skipped: list[dict[str, Any]] = []
        self.file_budget = _budget_seconds(FILE_SCAN_BUDGET_ENV, FILE_SCAN_BUDGET_SEC)
        self.total_budget = _budget_seconds(SNAPSHOT_SCAN_BUDGET_ENV, SNAPSHOT_SCAN_BUDGET_SEC)
        self.seconds = 0.0

    def entry(
        self,
        full: str,
        rel: str,
        *,
        reference_over_bytes: int,
        tracked: bool = False,
        **extra: Any,
    ) -> dict[str, Any]:
        """The manifest entry for one regular file: ``blob``, ``reference``, or
        ``withheld`` when its content holds a credential (reason ``secret``) or
        its scan ran out of time (reason ``scan_budget``).

        The size limit does not depend on ``scan``: which files are copied, and so
        the tree's identity, must not change with whether a scan ran."""
        limit = min(reference_over_bytes, CONTENT_SCAN_MAX_BYTES)
        if self.scan and self.budget is not None:
            try:
                expected = os.path.getsize(full)
            except OSError:
                expected = 0
            if expected <= limit:
                self.scanned += expected
                if self.scanned > self.budget:
                    raise SnapshotTooLarge(
                        f"more than {self.budget / 1e6:.0f} MB of files would be uploaded, "
                        "over the cap; raise --max-upload-mb, or lower --reference-over-mb so "
                        "the large files are recorded where they live instead of copied"
                    )
        sha, size, rules, seconds, out_of_time = _read_for_capture(
            full,
            os.path.basename(rel),
            # scanning disabled: scan=self.scan,
            scan=False,
            limit=limit,
            file_budget=self.file_budget,
            total_left=self.total_budget - self.seconds,
        )
        self.seconds += seconds
        mode = "100755" if os.access(full, os.X_OK) else "100644"
        entry: dict[str, Any] = {"path": rel, "mode": mode, "sha256": sha, "size": size, **extra}
        _classify_by_size(entry, full, reference_over_bytes=limit)
        if entry["source"] != "blob" or not (rules or out_of_time):
            return entry
        # A finding decides; a scan cut short by the clock only when none was found.
        if not rules:
            reason = SCAN_BUDGET_REASON
        elif set(rules) <= {"inspection-failed", _UNREADABLE_ARCHIVE}:
            reason = "uninspectable"
        else:
            reason = "secret"
        self.skipped.append(
            {
                "path": rel,
                "reason": reason,
                "found_in": "content" if rules else "scan_time",
                **({"rules": list(rules)} if rules else {"seconds": round(seconds, 2)}),
                **({"tracked": True} if tracked else {}),
            }
        )
        withheld: dict[str, Any] = {
            "path": rel, "mode": mode, "size": size, "source": "withheld", "reason": reason, **extra,
        }
        if size >= WITHHELD_HASH_MIN_BYTES:
            withheld["sha256"] = sha
        return withheld
from probe.sdk.capture.code.code import SnapshotTooLarge, _classify_by_size, _in_secret_dir, _skip_reason  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.capture.code.scanners.source_code import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    _SOURCE_SUFFIXES,
    _ScanOutOfTime,
    _chunk_rules,
    _notebook_rules,
    _utf16_codec,
    credential_rules,
)
