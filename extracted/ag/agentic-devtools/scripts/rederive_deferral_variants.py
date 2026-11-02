#!/usr/bin/env python3
"""Re-derive the suppressed-deferral variant table for issue #3672.

Every headline figure in #3672 (162 PRs, 1,569 rounds, 38.6%) was produced by a
corpus simulation that loaded ``ccr_review_format.py`` from a working branch 28
commits behind ``main`` — the pre-#3638 parser — and never applied G2
(``declared == extracted``) as a gate.  The guardrail cost quoted alongside those
figures was measured on the *new* parser.  Savings from one parser and guardrail
cost from another is not a coherent model of the system that would ship.

This script re-derives the table on a single, consistent basis:

* the parser is **imported from the working tree** (``agentic_devtools.cli.github
  .ccr_review_format``) rather than vendored, so running it on a ``main`` checkout
  measures the ``main`` parser by construction and cannot drift;
* **G2 is applied as a gate** — a round whose declared suppressed count does not
  equal the number of entries the parser extracts can never be a cut round;
* suppressed entry paths are run through a **path-artefact detector**, because the
  executable-path carve-out is a ``startswith`` test that non-path strings
  (``get_issue_types()``, ``--dry-run``, ``Acceptance Scenarios``) pass silently;
* **condition 10** (the PR diff contains no executable file) is evaluated against
  the authoritative changed-file list from the PR API, never against parsed
  finding paths.

Two modes:

``fetch``
    Build the corpus from the GitHub API via ``gh`` and write it as JSONL — one
    object per merged PR, carrying every CCR review body, every inline review
    comment path, and the authoritative changed-file list.

``analyze``
    Consume that corpus and emit the variant table, G2's rejection rate on SP cut
    rounds, the non-path artefact rate, and net-of-follow-up at the 2.73-round
    band.

Usage:
    python scripts/rederive_deferral_variants.py fetch \\
        --owner swai-factory --repo agentic-devtools \\
        --first-pr 2875 --last-pr 3612 \\
        --merged-before 2026-08-11T09:00:00Z --out .agdt-temp/ccr-corpus.jsonl

    python scripts/rederive_deferral_variants.py analyze \\
        --corpus .agdt-temp/ccr-corpus.jsonl

``fetch`` requires the GitHub CLI (``gh``) authenticated with ``repo`` scope.
``analyze`` is offline and deterministic.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from agentic_devtools.cli.github.ccr_review_format import (  # noqa: E402
    UNKNOWN_FILE,
    extract_suppressed_comment_entries,
    parse_reported_comment_count,
    parse_suppressed_count,
)

#: Exact review-author logins (with the optional ``[bot]`` suffix stripped) that
#: identify a Copilot Code Review round.  A substring test would also capture
#: ``copilot-swe-agent[bot]`` — the cloud coding agent — and any login merely
#: containing "copilot", inflating the corpus and every derived metric.
CCR_AUTHOR_LOGINS = frozenset({"copilot-pull-request-reviewer"})

#: Mean number of rounds a deferral follow-up PR costs, measured in #3672.
FOLLOW_UP_ROUND_COST = 2.73

#: Consecutive-suppressed-only run length required by the N4 / S4 variants.
CONSECUTIVE_RUN_LENGTH = 4


# --------------------------------------------------------------------------------------
# Path classification
# --------------------------------------------------------------------------------------

#: Prefixes whose files are executable — a defect here ships as behaviour.
#: ``tests/**`` is deliberately absent: #3672 classifies it non-executable and
#: records that as a decision rather than an omission.
_EXECUTABLE_PREFIXES = ("scripts/", ".github/")

#: Trailing ``:12`` / ``:12-18`` line anchors CCR appends to a finding path.
_LINE_ANCHOR_RE = re.compile(r":\d+(?:-\d+)?$")

#: A path segment sequence with a file extension, e.g. ``specs/3672/spec.md``.
_PATH_SHAPE_RE = re.compile(r"^[\w.@+-]+(?:/[\w.@+ -]+)*\.[A-Za-z0-9]{1,10}$")


def normalize_finding_path(raw: str) -> str:
    """Strip decoration from a finding path so it can be classified.

    Removes surrounding whitespace, backticks, a leading ``./``, and a trailing
    ``:12`` / ``:12-18`` line anchor.  The result is *not* guaranteed to be a
    path — call :func:`looks_like_path` to decide that.

    Args:
        raw: Path string as extracted from a review body.

    Returns:
        The stripped path candidate.
    """
    candidate = raw.strip().strip("`").strip()
    candidate = _LINE_ANCHOR_RE.sub("", candidate)
    return candidate.removeprefix("./")


def looks_like_path(raw: str) -> bool:
    """Return ``True`` when *raw* is plausibly a repository file path.

    The executable carve-out (condition 6 of #3672) is a prefix test, so any
    string that is not a path passes it silently.  On the extraction the published
    simulation used, 7.6% of deferred entries carried such a string —
    ``get_issue_types()``, ``_is_copilot_review_actionable()``, ``--dry-run``,
    ``Acceptance Scenarios`` — and some were plainly findings about production
    Python.  This is the detector that rejects them.

    :data:`UNKNOWN_FILE` is rejected: an unattributed finding is not provably on a
    non-executable path.

    Args:
        raw: Path string as extracted from a review body.

    Returns:
        ``True`` when the string has the shape of a path with a file extension.
    """
    candidate = normalize_finding_path(raw)
    if not candidate or candidate == UNKNOWN_FILE:
        return False
    if candidate.startswith("-"):
        return False
    if "(" in candidate or ")" in candidate:
        return False
    if any(part in {".", ".."} for part in re.split(r"[\\/]", candidate)):
        return False
    return bool(_PATH_SHAPE_RE.match(candidate))


def _path_is_executable(candidate: str) -> bool:
    """Classify an already-normalised path against the executable union.

    Executable is ``agentic_devtools/**.py`` ∪ ``scripts/**`` ∪ ``.github/**``, per
    #3672.  *candidate* must already be normalised by :func:`normalize_finding_path`.
    """
    if candidate.startswith("agentic_devtools/") and candidate.endswith(".py"):
        return True
    return candidate.startswith(_EXECUTABLE_PREFIXES)


def is_executable_path(raw: str) -> bool:
    """Return ``True`` when a *parsed finding* path is on executable code.

    Fails closed: a string that is not path-shaped is treated as executable,
    because an unattributed finding extracted from a review body cannot be shown
    to be safe.  For authoritative paths from the PR API use
    :func:`is_executable_changed_file`, which must not fail closed.

    Args:
        raw: Path string as extracted from a review body.

    Returns:
        ``True`` when the path is executable or cannot be classified.
    """
    if not looks_like_path(raw):
        return True
    return _path_is_executable(normalize_finding_path(raw))


def is_executable_changed_file(raw: str) -> bool:
    """Return ``True`` when an API-provided changed file is on executable code.

    The changed-file list comes from ``GET /pulls/{n}/files``, so every entry is a
    real path and needs no heuristic validation.  Classifying it through
    :func:`is_executable_path` would fail closed on valid extensionless files such
    as ``LICENSE``, ``Dockerfile``, or a ``.../template`` — all outside the
    executable union — and wrongly disqualify SP candidates.  Classify directly.

    Args:
        raw: A changed-file path from the PR files API.

    Returns:
        ``True`` only when the path is in the executable union.
    """
    return _path_is_executable(normalize_finding_path(raw))


def is_executable_posted_path(raw: str) -> bool:
    """Return ``True`` when an API-provided posted path must count as executable.

    Posted inline-comment paths come from the review-comments API, so real file paths
    should use the direct executable-union classifier. ``UNKNOWN_FILE`` is the one
    exception: a pathless comment is unattributed, so ``UNKNOWN_FILE`` returns
    ``True`` and is counted as executable to fail closed.
    """
    return raw == UNKNOWN_FILE or is_executable_changed_file(raw)


# --------------------------------------------------------------------------------------
# Corpus model
# --------------------------------------------------------------------------------------


@dataclass(frozen=True)
class Round:
    """One CCR review on a pull request.

    Attributes:
        review_id: GitHub review id.
        submitted_at: ISO-8601 submission timestamp, used only for ordering.
        body: Full review body text, parsed with the working-tree parser.
        posted_paths: ``path`` of every inline review comment attached to this
            review — the authoritative posted-finding list.  Inline comments
            without a path are recorded as :data:`UNKNOWN_FILE`.
    """

    review_id: int
    submitted_at: str
    body: str
    posted_paths: tuple[str, ...] = ()


@dataclass(frozen=True)
class PullRequestRecord:
    """One merged pull request and every CCR round it ran.

    Attributes:
        number: Pull request number.
        changed_files: Authoritative changed-file list from the PR API.  Parsed
            finding paths are *not* a substitute — the two disagree, and only this
            list describes what CCR was able to see.
        rounds: CCR rounds in submission order.
    """

    number: int
    changed_files: tuple[str, ...]
    rounds: tuple[Round, ...]


@dataclass(frozen=True)
class RoundMetrics:
    """Parser output for a single round, on the working-tree parser.

    Attributes:
        declared_suppressed: Self-reported suppressed count from the body.
        extracted_paths: Path of every suppressed entry the parser recovered.
        posted_count: Number of inline comments posted in this round.
        posted_paths: Paths of those inline comments.
        body_comment_count: Self-reported posted count (``None`` when unparsed).
    """

    declared_suppressed: int
    extracted_paths: tuple[str, ...]
    posted_count: int
    posted_paths: tuple[str, ...]
    body_comment_count: int | None

    @property
    def g2_passes(self) -> bool:
        """Return ``True`` when declared and extracted suppressed counts agree."""
        return self.declared_suppressed == len(self.extracted_paths)

    @property
    def is_suppressed_only(self) -> bool:
        """Return ``True`` when the round has suppressed findings and no posted ones.

        The posted channel is checked twice, and the round must be clean on both.
        Inline comments are the artefact and the body count is only a claim, but a
        body that self-reports posted comments while the corpus carries no inline
        comment for that review is a *retrieval gap*, not a suppressed-only round.
        Trusting the inline list alone would silently manufacture cut rounds
        wherever the fetch was incomplete, inflating every saving in the table.

        An unparseable body count (``None``) is not a disagreement — legacy bodies
        do not carry the count at all — so it does not disqualify the round.
        """
        if self.declared_suppressed <= 0 or self.posted_count > 0:
            return False
        return not (self.body_comment_count or 0) > 0


def measure_round(round_: Round) -> RoundMetrics:
    """Parse *round_* with the working-tree CCR parser.

    The posted count is taken from the inline review comments rather than the
    body's self-report, because the body count is a claim and the comment list is
    the artefact.  The self-reported value is retained for reconciliation.

    Args:
        round_: The round to measure.

    Returns:
        The parsed metrics for that round.
    """
    entries = extract_suppressed_comment_entries(round_.body)
    return RoundMetrics(
        declared_suppressed=parse_suppressed_count(round_.body),
        extracted_paths=tuple(path for path, _ in entries),
        posted_count=len(round_.posted_paths),
        posted_paths=round_.posted_paths,
        body_comment_count=parse_reported_comment_count(round_.body),
    )


# --------------------------------------------------------------------------------------
# Variants
# --------------------------------------------------------------------------------------

#: The five variants re-derived here.  All of them additionally require G2.
#:
#: ``A``   any suppressed-only round cuts the PR.
#: ``S``   as ``A``, plus every suppressed entry in the cut round is on a
#:         path-shaped, non-executable path (G7, forward half).
#: ``SP``  as ``S``, plus the PR has produced no prior executable-path posted
#:         finding (condition 7) and its diff contains no executable file
#:         (condition 10) — the variant #3672 proposes.
#: ``N4``  as ``A``, but only at the 4th consecutive suppressed-only round.
#: ``S4``  as ``S``, but only at the 4th consecutive suppressed-only round.
VARIANTS = ("A", "S", "SP", "N4", "S4")


def _cut_round_is_deferrable(metrics: RoundMetrics) -> bool:
    """Return ``True`` when the cut round's suppressed entries are all safe.

    Every entry must be path-shaped and non-executable.  ``is_executable_path``
    already fails closed on non-path strings, so the artefact rejection is
    implied — it is asserted separately for clarity at the call site.
    """
    return bool(metrics.extracted_paths) and not any(is_executable_path(path) for path in metrics.extracted_paths)


def _has_prior_executable_posted(history: Sequence[RoundMetrics]) -> bool:
    """Return ``True`` when any earlier round posted a finding on executable code."""
    return any(is_executable_posted_path(path) for earlier in history for path in earlier.posted_paths)


def find_cut_index(
    record: PullRequestRecord,
    metrics: Sequence[RoundMetrics],
    variant: str,
) -> int | None:
    """Return the index of the round at which *variant* cuts *record*.

    The cut round itself is *not* saved — it is the round that runs, produces a
    suppressed-only verdict, and triggers the merge.  Rounds after it are the
    saving.

    Args:
        record: The pull request being evaluated.
        metrics: Parsed metrics for ``record.rounds``, in the same order.
        variant: One of :data:`VARIANTS`.

    Returns:
        The 0-based index of the cut round, or ``None`` when the variant never
        fires on this pull request.

    Raises:
        ValueError: When *variant* is not a known variant.
    """
    if variant not in VARIANTS:
        raise ValueError(f"Unknown variant: {variant!r} (expected one of {', '.join(VARIANTS)})")

    requires_safe_paths = variant in ("S", "SP", "S4")
    requires_run = variant in ("N4", "S4")
    diff_is_executable_free = not any(is_executable_changed_file(path) for path in record.changed_files)

    if variant == "SP" and not diff_is_executable_free:
        return None

    run_length = 0
    for index, current in enumerate(metrics):
        run_length = run_length + 1 if current.is_suppressed_only else 0
        if not current.is_suppressed_only:
            continue
        # G2 gates every variant: an unreconciled round can never be a cut round.
        if not current.g2_passes:
            continue
        if requires_run and run_length < CONSECUTIVE_RUN_LENGTH:
            continue
        if requires_safe_paths and not _cut_round_is_deferrable(current):
            continue
        if variant == "SP" and _has_prior_executable_posted(metrics[:index]):
            continue
        return index
    return None


@dataclass
class VariantResult:
    """Aggregate outcome of one variant across the corpus.

    Attributes:
        variant: The variant name.
        prs: Pull requests on which the variant fires.
        rounds_saved: Rounds after the cut, summed across those pull requests.
        findings_captured: Suppressed findings deferred at the cut rounds.
        posted_lost: Posted findings in rounds after the cut — never surfaced.
        executable_posted_lost: The subset of ``posted_lost`` on executable paths.
    """

    variant: str
    prs: int = 0
    rounds_saved: int = 0
    findings_captured: int = 0
    posted_lost: int = 0
    executable_posted_lost: int = 0

    def share_of_corpus(self, total_rounds: int) -> float:
        """Return ``rounds_saved`` as a fraction of *total_rounds* (0.0 when empty)."""
        return self.rounds_saved / total_rounds if total_rounds else 0.0

    def net_of_follow_up(self) -> float:
        """Return rounds saved net of one follow-up PR per deferring PR."""
        return self.rounds_saved - self.prs * FOLLOW_UP_ROUND_COST


#: A corpus record paired with the parsed metrics for each of its rounds.
MeasuredRecord = tuple[PullRequestRecord, list[RoundMetrics]]


def measure_corpus(records: Iterable[PullRequestRecord]) -> list[MeasuredRecord]:
    """Parse every round in *records* once.

    Parsing is the expensive step — the suppressed-block extraction masks fenced
    code and runs several multiline regexes over each body. Every variant and the
    diagnostics pass need the same parse, so it is done once here and shared,
    rather than six times over a corpus of thousands of long review bodies.

    Args:
        records: The corpus.

    Returns:
        Each record paired with its rounds' metrics, in round order.
    """
    return [(record, [measure_round(round_) for round_ in record.rounds]) for record in records]


def evaluate_variant(measured: Iterable[MeasuredRecord], variant: str) -> VariantResult:
    """Run *variant* across *measured* and aggregate the outcome.

    Args:
        measured: The corpus, as returned by :func:`measure_corpus`.
        variant: One of :data:`VARIANTS`.

    Returns:
        The aggregated result for that variant.
    """
    result = VariantResult(variant=variant)
    for record, metrics in measured:
        cut = find_cut_index(record, metrics, variant)
        if cut is None:
            continue
        result.prs += 1
        result.rounds_saved += len(metrics) - (cut + 1)
        result.findings_captured += len(metrics[cut].extracted_paths)
        for later in metrics[cut + 1 :]:
            if later.body_comment_count is not None and later.body_comment_count > later.posted_count:
                raise ValueError(
                    "retrieval gap: later round reports more posted comments than were retrieved "
                    f"({later.body_comment_count} > {later.posted_count})"
                )
            result.posted_lost += later.posted_count
            result.executable_posted_lost += sum(1 for path in later.posted_paths if is_executable_posted_path(path))
    return result


# --------------------------------------------------------------------------------------
# Diagnostics required by the acceptance criteria of #3683
# --------------------------------------------------------------------------------------


@dataclass
class Diagnostics:
    """Rates #3683 requires to be stated as numbers.

    Attributes:
        total_rounds: Every CCR round in the corpus.
        total_prs: Every merged pull request in the corpus.
        sp_candidate_rounds: Rounds that would be SP cut rounds if G2 were not
            applied — the denominator for G2's rejection rate.
        sp_g2_rejected: How many of those G2 rejects.
        deferred_entries: Suppressed entries across SP cut rounds.
        non_path_entries: The subset of those that are not path-shaped.
    """

    total_rounds: int = 0
    total_prs: int = 0
    sp_candidate_rounds: int = 0
    sp_g2_rejected: int = 0
    deferred_entries: int = 0
    non_path_entries: int = 0

    @property
    def g2_rejection_rate(self) -> float:
        """Return G2's rejection rate on SP cut rounds (0.0 when no candidates)."""
        return self.sp_g2_rejected / self.sp_candidate_rounds if self.sp_candidate_rounds else 0.0

    @property
    def non_path_artefact_rate(self) -> float:
        """Return the non-path artefact rate among deferred entries."""
        return self.non_path_entries / self.deferred_entries if self.deferred_entries else 0.0


def collect_diagnostics(measured: Iterable[MeasuredRecord]) -> Diagnostics:
    """Measure G2's rejection rate and the non-path artefact rate.

    The G2 denominator is every round that a G2-free SP would have cut on, so the
    rate answers "how much of the published saving does G2 remove", not "how often
    does the parser disagree with itself across the whole corpus".

    Args:
        measured: The corpus, as returned by :func:`measure_corpus`.

    Returns:
        The measured diagnostics.
    """
    diagnostics = Diagnostics()
    for record, metrics in measured:
        diagnostics.total_prs += 1
        diagnostics.total_rounds += len(metrics)

        diff_is_executable_free = not any(is_executable_changed_file(path) for path in record.changed_files)
        if diff_is_executable_free:
            for index, current in enumerate(metrics):
                if not current.is_suppressed_only:
                    continue
                if not _cut_round_is_deferrable(current):
                    continue
                if _has_prior_executable_posted(metrics[:index]):
                    continue
                diagnostics.sp_candidate_rounds += 1
                if not current.g2_passes:
                    diagnostics.sp_g2_rejected += 1
                break

        # Measure artefacts on the pre-path-detector SP candidate population.
        # Apply G2 and the SP executable conditions but omit _cut_round_is_deferrable,
        # so that non-path entries are visible.  Using find_cut_index("SP") would
        # silently pre-filter them away because _cut_round_is_deferrable rejects any
        # round whose entries are not all path-shaped.
        if diff_is_executable_free:
            for index, current in enumerate(metrics):
                if not current.is_suppressed_only:
                    continue
                if not current.g2_passes:
                    continue
                if _has_prior_executable_posted(metrics[:index]):
                    continue
                # SP's executable-path restriction still applies: a round with a
                # path-shaped executable entry is one SP would reject, so it is not
                # a cut round.  Non-path strings are retained — they are the
                # artefacts being measured.
                if any(is_executable_path(path) for path in current.extracted_paths if looks_like_path(path)):
                    continue
                for path in current.extracted_paths:
                    diagnostics.deferred_entries += 1
                    if not looks_like_path(path):
                        diagnostics.non_path_entries += 1
                break
    return diagnostics


# --------------------------------------------------------------------------------------
# Corpus I/O
# --------------------------------------------------------------------------------------


def _run_gh(args: list[str]) -> str:
    """Run a ``gh`` command and return stdout, raising on failure."""
    try:
        result = subprocess.run(  # noqa: S603 - shell=False, args passed as list
            ["gh", *args],
            capture_output=True,
            text=True,
            encoding="utf-8",
            check=True,
            shell=False,
        )
    except FileNotFoundError as exc:  # pragma: no cover - environment guard
        raise RuntimeError("GitHub CLI 'gh' not found on PATH.") from exc
    except subprocess.CalledProcessError as exc:
        detail = exc.stderr.strip() or exc.stdout.strip() or f"exit code {exc.returncode}"
        raise RuntimeError(f"gh command failed: {detail}") from exc
    return result.stdout


def _gh_json(args: list[str]) -> list[dict]:
    """Run a ``gh api --paginate`` call and merge its JSON array pages.

    ``gh api --paginate`` emits one JSON array per page, concatenated on stdout, so
    a single ``json.loads`` over the whole stream fails the moment a response spans
    more than one page — and a failed parse means ``fetch`` cannot rebuild the
    corpus.  Each page is decoded independently with :meth:`json.JSONDecoder.raw_decode`
    and the arrays are concatenated, mirroring the handling in
    ``agentic_devtools.cli.ci.github_provider``.
    """
    raw = _run_gh(args).strip()
    if not raw:
        return []
    merged: list[dict] = []
    decoder = json.JSONDecoder()
    idx = 0
    length = len(raw)
    while idx < length:
        while idx < length and raw[idx] in " \t\n\r":
            idx += 1
        if idx >= length:  # pragma: no cover - strip() removes trailing whitespace
            break
        try:
            page, idx = decoder.raw_decode(raw, idx)
        except json.JSONDecodeError as exc:
            snippet = raw[idx : idx + 200].replace("\n", " ")
            raise RuntimeError(f"gh returned non-JSON (truncated): {snippet!r}") from exc
        if not isinstance(page, list):
            raise RuntimeError(f"gh returned {type(page).__name__}, expected a JSON array")
        merged.extend(page)
    return merged


def is_ccr_review(review: dict) -> bool:
    """Return ``True`` when *review* was authored by Copilot Code Review.

    Matches the author login exactly against :data:`CCR_AUTHOR_LOGINS` after
    lower-casing and stripping the optional ``[bot]`` suffix.  A substring match
    would misclassify ``copilot-swe-agent[bot]`` and other ``copilot``-containing
    logins as CCR rounds, inflating the corpus and all derived metrics.
    """
    login = str((review.get("user") or {}).get("login", "")).lower().removesuffix("[bot]")
    return login in CCR_AUTHOR_LOGINS


def build_record(number: int, reviews: list[dict], comments: list[dict], files: list[dict]) -> PullRequestRecord:
    """Assemble one corpus record from raw GitHub API payloads.

    Args:
        number: Pull request number.
        reviews: ``GET /pulls/{n}/reviews`` payload.
        comments: ``GET /pulls/{n}/comments`` payload (inline review comments).
        files: ``GET /pulls/{n}/files`` payload.

    Returns:
        The assembled record, with rounds in submission order.
    """
    posted_by_review: dict[int, list[str]] = {}
    for comment in comments:
        review_id = comment.get("pull_request_review_id")
        if review_id is None:
            continue
        if comment.get("in_reply_to_id") is not None:
            continue
        posted_by_review.setdefault(int(review_id), []).append(str(comment.get("path") or UNKNOWN_FILE))

    changed_files: list[str] = []
    for entry in files:
        current = entry.get("filename")
        if current is not None:
            changed_files.append(str(current))
        previous = entry.get("previous_filename")
        if previous is not None:
            changed_files.append(str(previous))

    rounds = [
        Round(
            review_id=int(review["id"]),
            submitted_at=str(review.get("submitted_at") or ""),
            body=str(review.get("body") or ""),
            posted_paths=tuple(posted_by_review.get(int(review["id"]), ())),
        )
        for review in reviews
        if is_ccr_review(review)
    ]
    rounds.sort(key=lambda item: (item.submitted_at, item.review_id))
    return PullRequestRecord(
        number=number,
        changed_files=tuple(changed_files),
        rounds=tuple(rounds),
    )


def _highest_pull_request_number(slug: str) -> int:
    """Return the highest pull request number in *slug*, or 0 when there are none."""
    listed = json.loads(_run_gh(["pr", "list", "--repo", slug, "--state", "all", "--limit", "1", "--json", "number"]))
    return max((int(item["number"]) for item in listed), default=0)


def _parse_iso8601(value: str) -> datetime:
    """Parse a GitHub ISO-8601 UTC timestamp (``...Z``) to an aware ``datetime``."""
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def merged_numbers_in_range(
    slug: str,
    first_pr: int,
    last_pr: int,
    merged_before: str | None = None,
) -> list[int]:
    """Return every merged pull request number in ``[first_pr, last_pr]``, ascending.

    ``gh pr list`` returns the *most recent* N merged pull requests, so a limit
    sized to the requested range silently drops the oldest part of that range once
    newer pull requests exist — and a truncated corpus deflates every figure in the
    table without any visible error.  The limit is therefore sized to the number of
    pull requests that could possibly be newer than ``first_pr``, which is a
    guaranteed upper bound on how many merged ones there are.

    A numeric range alone does **not** freeze the corpus: a pull request whose
    number is in range but which merged *after* the original measurement is picked
    up on any later run, so re-derived figures drift against the published ones.
    *merged_before* pins the corpus to a fixed instant — pull requests merged at or
    after it are excluded, exactly as the measurement that produced #3672's table
    was frozen before those merges existed.

    Args:
        slug: ``owner/repo``.
        first_pr: Lowest pull request number to include (inclusive).
        last_pr: Highest pull request number to include (inclusive).
        merged_before: ISO-8601 UTC cutoff (``YYYY-MM-DDTHH:MM:SSZ``); when set,
            only pull requests merged strictly before it are included.

    Returns:
        The matching merged pull request numbers, ascending.

    Raises:
        ValueError: When the range is empty (``last_pr < first_pr``).
    """
    if last_pr < first_pr:
        raise ValueError(f"Empty pull request range: --first-pr {first_pr} > --last-pr {last_pr}")
    highest = _highest_pull_request_number(slug)
    limit = max(highest - first_pr + 1, 1)
    listed = json.loads(
        _run_gh(["pr", "list", "--repo", slug, "--state", "merged", "--limit", str(limit), "--json", "number,mergedAt"])
    )
    cutoff = _parse_iso8601(merged_before) if merged_before is not None else None
    numbers: list[int] = []
    for item in listed:
        number = int(item["number"])
        if not (first_pr <= number <= last_pr):
            continue
        if cutoff is not None:
            merged_at = item.get("mergedAt")
            if not merged_at or _parse_iso8601(str(merged_at)) >= cutoff:
                continue
        numbers.append(number)
    return sorted(numbers)


def fetch_corpus(
    owner: str,
    repo: str,
    first_pr: int,
    last_pr: int,
    out_path: Path,
    merged_before: str | None = None,
) -> int:
    """Fetch every merged PR in ``[first_pr, last_pr]`` and write the corpus JSONL.

    Args:
        owner: Repository owner.
        repo: Repository name.
        first_pr: Lowest pull request number to include (inclusive).
        last_pr: Highest pull request number to include (inclusive).
        out_path: Destination JSONL file; parent directories are created.
        merged_before: ISO-8601 UTC cutoff; when set, freezes the corpus to pull
            requests merged strictly before it (see :func:`merged_numbers_in_range`).

    Returns:
        The number of records written.
    """
    slug = f"{owner}/{repo}"
    numbers = merged_numbers_in_range(slug, first_pr, last_pr, merged_before=merged_before)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = out_path.with_name(f"{out_path.name}.tmp")
    written = 0
    try:
        with tmp_path.open("w", encoding="utf-8") as handle:
            for number in numbers:
                record = build_record(
                    number,
                    _gh_json(["api", "--paginate", f"repos/{slug}/pulls/{number}/reviews"]),
                    _gh_json(["api", "--paginate", f"repos/{slug}/pulls/{number}/comments"]),
                    _gh_json(["api", "--paginate", f"repos/{slug}/pulls/{number}/files"]),
                )
                handle.write(json.dumps(record_to_json(record)) + "\n")
                written += 1
                print(f"  fetched #{number} ({len(record.rounds)} rounds)", file=sys.stderr)
        tmp_path.replace(out_path)
    except BaseException:
        tmp_path.unlink(missing_ok=True)
        raise
    return written


def record_to_json(record: PullRequestRecord) -> dict:
    """Serialise *record* to a JSON-compatible dict."""
    return {
        "number": record.number,
        "changed_files": list(record.changed_files),
        "rounds": [
            {
                "review_id": round_.review_id,
                "submitted_at": round_.submitted_at,
                "body": round_.body,
                "posted_paths": list(round_.posted_paths),
            }
            for round_ in record.rounds
        ],
    }


def record_from_json(payload: dict) -> PullRequestRecord:
    """Deserialise a corpus record written by :func:`record_to_json`.

    Args:
        payload: One decoded JSONL line.

    Returns:
        The reconstructed record.

    Raises:
        ValueError: When *payload* is not a corpus record object.
    """
    if not isinstance(payload, dict) or "number" not in payload:
        raise ValueError("Corpus line is not a pull request record object")
    rounds = payload.get("rounds", [])
    if not isinstance(rounds, list):
        raise ValueError(f"PR #{payload['number']}: 'rounds' must be a list, got {type(rounds).__name__}")
    changed_files_raw = payload.get("changed_files")
    if not isinstance(changed_files_raw, list):
        raise ValueError(
            f"PR #{payload['number']}: 'changed_files' must be a list (got "
            f"{type(changed_files_raw).__name__}); omitting it silently bypasses condition 10"
        )
    changed_files = _validated_string_list(
        changed_files_raw,
        field_name="changed_files",
        pr_number=int(payload["number"]),
    )
    parsed_rounds = tuple(
        _round_from_json(item, pr_number=int(payload["number"]), round_index=index) for index, item in enumerate(rounds)
    )
    return PullRequestRecord(
        number=int(payload["number"]),
        changed_files=changed_files,
        rounds=parsed_rounds,
    )


def _validated_string_list(raw: list[object], *, field_name: str, pr_number: int) -> tuple[str, ...]:
    """Validate that *raw* is a list of path strings and return it as a tuple."""
    paths: list[str] = []
    for index, item in enumerate(raw):
        if not isinstance(item, str):
            raise ValueError(
                f"PR #{pr_number}: '{field_name}[{index}]' must be a string path, got {type(item).__name__}"
            )
        paths.append(item)
    return tuple(paths)


def _round_from_json(item: object, *, pr_number: int, round_index: int) -> Round:
    """Validate and deserialise one round object from a corpus record."""
    if not isinstance(item, dict):
        raise ValueError(f"PR #{pr_number}: 'rounds[{round_index}]' must be an object, got {type(item).__name__}")
    posted_paths_raw = item.get("posted_paths")
    if posted_paths_raw is None:
        posted_paths_raw = []
    if not isinstance(posted_paths_raw, list):
        raise ValueError(
            f"PR #{pr_number}: 'rounds[{round_index}].posted_paths' must be a list, got "
            f"{type(posted_paths_raw).__name__}"
        )
    return Round(
        review_id=int(item.get("review_id", 0)),
        submitted_at=str(item.get("submitted_at") or ""),
        body=str(item.get("body") or ""),
        posted_paths=_validated_string_list(
            posted_paths_raw,
            field_name=f"rounds[{round_index}].posted_paths",
            pr_number=pr_number,
        ),
    )


def load_corpus(path: Path) -> list[PullRequestRecord]:
    """Load a corpus JSONL file written by :func:`fetch_corpus`.

    Args:
        path: Path to the JSONL file.

    Returns:
        Every record in file order.
    """
    records = []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                records.append(record_from_json(json.loads(line)))
    return records


# --------------------------------------------------------------------------------------
# Reporting
# --------------------------------------------------------------------------------------


def render_report(results: Sequence[VariantResult], diagnostics: Diagnostics) -> str:
    """Render the corrected variant table and the two required rates as Markdown.

    Args:
        results: One result per variant, in report order.
        diagnostics: The measured diagnostics.

    Returns:
        The Markdown report.
    """
    total = diagnostics.total_rounds
    lines = [
        "# Re-derived deferral variant table (#3683)",
        "",
        f"Corpus: {diagnostics.total_prs} merged PRs, {total} CCR rounds.",
        "Parser: working-tree `agentic_devtools.cli.github.ccr_review_format`. G2 applied to every variant.",
        "",
        "| variant | PRs | rounds saved | % corpus | findings captured | posted lost | executable-path posted lost |",
        "|---|---:|---:|---:|---:|---:|---:|",
    ]
    lines.extend(
        f"| {result.variant} | {result.prs} | {result.rounds_saved} | "
        f"{result.share_of_corpus(total):.1%} | {result.findings_captured} | "
        f"{result.posted_lost} | {result.executable_posted_lost} |"
        for result in results
    )
    lines.extend(
        [
            "",
            f"**G2 rejection rate on SP cut rounds:** {diagnostics.g2_rejection_rate:.1%} "
            f"({diagnostics.sp_g2_rejected}/{diagnostics.sp_candidate_rounds})",
            f"**Non-path artefact rate among deferred entries:** {diagnostics.non_path_artefact_rate:.1%} "
            f"({diagnostics.non_path_entries}/{diagnostics.deferred_entries})",
            "",
            f"## Net of follow-up (at {FOLLOW_UP_ROUND_COST} rounds per deferring PR)",
            "",
            "| variant | rounds saved | follow-up cost | net | % corpus |",
            "|---|---:|---:|---:|---:|",
        ]
    )
    lines.extend(
        f"| {result.variant} | {result.rounds_saved} | "
        f"{result.prs * FOLLOW_UP_ROUND_COST:.0f} | {result.net_of_follow_up():.0f} | "
        f"{(result.net_of_follow_up() / total if total else 0.0):.1%} |"
        for result in results
    )
    return "\n".join(lines)


# --------------------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    """Build the command-line parser."""
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    fetch = sub.add_parser("fetch", help="Build the CCR corpus from the GitHub API")
    fetch.add_argument("--owner", default="swai-factory")
    fetch.add_argument("--repo", default="agentic-devtools")
    fetch.add_argument("--first-pr", type=int, required=True)
    fetch.add_argument("--last-pr", type=int, required=True)
    fetch.add_argument("--out", type=Path, required=True)
    fetch.add_argument(
        "--merged-before",
        default=None,
        help=(
            "ISO-8601 UTC cutoff (YYYY-MM-DDTHH:MM:SSZ). Freezes the corpus to pull "
            "requests merged strictly before this instant, so later merges cannot "
            "drift the re-derived figures against the published ones."
        ),
    )

    analyze = sub.add_parser("analyze", help="Re-derive the variant table from a corpus")
    analyze.add_argument("--corpus", type=Path, required=True)
    analyze.add_argument("--json", action="store_true", help="Emit machine-readable JSON instead of Markdown")
    return parser


def _analysis_payload(results: Sequence[VariantResult], diagnostics: Diagnostics) -> dict:
    """Build the machine-readable analysis payload."""
    return {
        "totalPrs": diagnostics.total_prs,
        "totalRounds": diagnostics.total_rounds,
        "g2RejectionRate": diagnostics.g2_rejection_rate,
        "nonPathArtefactRate": diagnostics.non_path_artefact_rate,
        "variants": [
            {
                "variant": result.variant,
                "prs": result.prs,
                "roundsSaved": result.rounds_saved,
                "shareOfCorpus": result.share_of_corpus(diagnostics.total_rounds),
                "findingsCaptured": result.findings_captured,
                "postedLost": result.posted_lost,
                "executablePostedLost": result.executable_posted_lost,
                "netOfFollowUp": result.net_of_follow_up(),
            }
            for result in results
        ],
    }


def main(argv: list[str] | None = None) -> int:
    """Entry point. Returns a process exit code."""
    args = build_parser().parse_args(argv)

    if args.command == "fetch":
        written = fetch_corpus(
            args.owner, args.repo, args.first_pr, args.last_pr, args.out, merged_before=args.merged_before
        )
        print(f"Wrote {written} record(s) to {args.out}")
        return 0

    if not args.corpus.is_file():
        print(f"Corpus not found: {args.corpus}", file=sys.stderr)
        return 1

    measured = measure_corpus(load_corpus(args.corpus))
    results = [evaluate_variant(measured, variant) for variant in VARIANTS]
    diagnostics = collect_diagnostics(measured)
    print(
        json.dumps(_analysis_payload(results, diagnostics), indent=2)
        if args.json
        else render_report(results, diagnostics)
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
