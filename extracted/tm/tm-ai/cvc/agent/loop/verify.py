"""Post-write verification for the CVC agent loop.

The dashboard log the team pasted contains the second-most-damaging
symptom after the read-cache pathology: the agent emits a ``patch``
or ``write_file`` call, the tool returns a success-shaped result, and
*the file on disk does not match the intent*. The model never re-reads,
so it thinks the change landed and moves on. The user later opens the
file and sees no diff — or worse, a partial diff.

This module is the verification step that upstream performs implicitly
via its per-tool-result framing: upstream re-reads any file it just
wrote and asserts the resulting content matches the expected delta.
CVC's analog (this module) makes that verification explicit, structured,
and testable.

Design
------
* :func:`verify_write` — after a full ``write_file``, re-read the file
  and check the SHA-256 matches the expected content's hash. Returns
  a structured :class:`VerifyResult` instead of a string so the
  caller can decide how to surface failure (return to the LLM as an
  error, raise a dashboard banner, etc.).

* :func:`verify_patch` — after a ``patch`` / ``edit_file``, re-read
  the file and check that the expected post-state substring is
  present. Catches the "I patched but the old_string didn't match,
  so nothing happened" silent failure class.

* :func:`verify_replace` — after a ``patch`` whose *old_string* had
  multiple matches, verify exactly one match was replaced. Catches
  the "patch landed in the wrong place" class.

All functions are pure — they take the path and a reader callable,
they never touch the filesystem directly. The gateway injects the
real reader (which itself can go through the read cache). This makes
the module trivially testable with a :class:`dict`-backed fake reader.

Why this is a loop primitive, not a tool
----------------------------------------
Verification happens *after* a tool call but *before* the tool result
is fed back to the LLM. It's the chat loop's responsibility, not the
executor or the tool. Putting it in ``loop/`` keeps the layering right
(``chat.py`` calls ``verify.verify_write``, never the executor).
"""
from __future__ import annotations

import hashlib
import os
import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, List, Optional

__all__ = [
    "VerifyStatus",
    "VerifyResult",
    "verify_write",
    "verify_patch",
    "verify_replace",
    "_sha256_text",
]


def _sha256_text(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8", errors="replace")).hexdigest()


class VerifyStatus(str, Enum):
    """Outcome of a verification check."""

    OK = "ok"
    """The post-state matches the expected delta exactly."""

    MISMATCH = "mismatch"
    """The file's content differs from the expected post-state."""

    MISSING = "missing"
    """The file doesn't exist (e.g. a write was expected to create it)."""

    PARTIAL = "partial"
    """The expected substring is present, but the surrounding content
    doesn't match — typical of a patch that landed in the wrong place
    (e.g. ``old_string`` matched twice and only one was replaced)."""

    NO_DIFF = "no_diff"
    """The file's content is byte-identical to the pre-state — the
    patch must have failed silently. This is the worst class because
    the model thinks it succeeded."""


@dataclass
class VerifyResult:
    """Structured verification outcome — the loop feeds this back to the LLM."""

    status: VerifyStatus
    path: str
    expected_sha256: Optional[str] = None
    actual_sha256: Optional[str] = None
    pre_sha256: Optional[str] = None
    diff_summary: str = ""
    suggestion: str = ""

    @property
    def ok(self) -> bool:
        return self.status is VerifyStatus.OK

    def to_user_message(self) -> str:
        """One-line message the LLM can immediately act on.

        Designed to be the *value* of the tool_result message — not a
        human-facing string. Keep it terse and actionable.
        """
        if self.ok:
            return f"Verified: {self.path} content matches the intended patch."
        if self.status is VerifyStatus.MISSING:
            return (
                f"Verification FAILED: {self.path} does not exist on disk "
                f"after a write was expected to create it. "
                f"Check directory permissions and the parent path."
            )
        if self.status is VerifyStatus.NO_DIFF:
            return (
                f"Verification FAILED: {self.path} is byte-identical to its "
                f"pre-state — the patch did not modify the file. "
                f"Most likely cause: the old_string did not match exactly. "
                f"Re-read the file to see its current content and re-emit "
                f"the patch with the exact text."
            )
        if self.status is VerifyStatus.PARTIAL:
            return (
                f"Verification PARTIAL: {self.path} contains the expected "
                f"substring but the surrounding content is unexpected. "
                f"Likely cause: the old_string matched multiple times in "
                f"the file and only one was replaced. Re-read the file, "
                f"include more context lines to make the old_string unique, "
                f"and re-emit the patch. Diff: {self.diff_summary}"
            )
        # MISMATCH
        return (
            f"Verification FAILED: {self.path} content does not match the "
            f"expected post-state. Diff: {self.diff_summary}. "
            f"Re-read the file to see its current content and re-emit "
            f"the write with the exact intended content."
        )

    def to_dict(self) -> dict:
        return {
            "status": self.status.value,
            "path": self.path,
            "expected_sha256": self.expected_sha256,
            "actual_sha256": self.actual_sha256,
            "pre_sha256": self.pre_sha256,
            "diff_summary": self.diff_summary,
            "suggestion": self.suggestion,
            "ok": self.ok,
        }


# ── write verification ───────────────────────────────────────────────


def verify_write(
    path: str,
    expected_content: str,
    reader: Callable[[str], str],
) -> VerifyResult:
    """Confirm that *path* on disk matches *expected_content* byte-for-byte.

    *reader* must return the current file content (or raise
    ``FileNotFoundError``). The caller is responsible for routing the
    reader through any caching layer; this module never touches disk.
    """
    abs_path = os.path.realpath(os.path.expanduser(path))
    expected_sha = _sha256_text(expected_content)

    try:
        actual = reader(abs_path)
    except FileNotFoundError:
        return VerifyResult(
            status=VerifyStatus.MISSING,
            path=abs_path,
            expected_sha256=expected_sha,
            diff_summary="file not found",
            suggestion="check parent directory exists and is writable",
        )

    actual_sha = _sha256_text(actual)
    if actual_sha == expected_sha:
        return VerifyResult(
            status=VerifyStatus.OK,
            path=abs_path,
            expected_sha256=expected_sha,
            actual_sha256=actual_sha,
        )

    # Build a short, useful diff summary — not the full unified diff
    # (too noisy for the LLM context). We just show the first 200 chars
    # of expected vs actual so the model can see the shape of the gap.
    expected_head = expected_content[:200].replace("\n", "\\n")
    actual_head = actual[:200].replace("\n", "\\n")
    return VerifyResult(
        status=VerifyStatus.MISMATCH,
        path=abs_path,
        expected_sha256=expected_sha,
        actual_sha256=actual_sha,
        diff_summary=f"expected starts: {expected_head!r} | actual starts: {actual_head!r}",
    )


# ── patch verification ───────────────────────────────────────────────


def verify_patch(
    path: str,
    pre_content: Optional[str],
    expected_post_substring: str,
    reader: Callable[[str], str],
    *,
    full_expected: Optional[str] = None,
) -> VerifyResult:
    """Confirm that *path* on disk contains *expected_post_substring*.

    Use cases:

    * ``expected_post_substring`` = the *new_string* the model just
      patched in. If the file doesn't contain it, the patch failed.
    * ``full_expected`` = the entire file content the model expects
      after the patch. If provided, the check is stricter (catches
      partial-application: the substring is present but the surrounding
      file is wrong because the model patched the wrong location).

    *pre_content* is the file content captured *before* the patch — used
    to detect the silent ``NO_DIFF`` class (file is byte-identical to
    pre-state, meaning the patch did nothing). Pass ``None`` to skip
    that check (e.g. you don't have the pre-state handy).
    """
    abs_path = os.path.realpath(os.path.expanduser(path))
    try:
        actual = reader(abs_path)
    except FileNotFoundError:
        return VerifyResult(
            status=VerifyStatus.MISSING,
            path=abs_path,
            diff_summary="file not found after patch",
        )

    actual_sha = _sha256_text(actual)

    # NO_DIFF — patch landed but file is unchanged. Worst case.
    if pre_content is not None:
        pre_sha = _sha256_text(pre_content)
        if pre_sha == actual_sha:
            return VerifyResult(
                status=VerifyStatus.NO_DIFF,
                path=abs_path,
                pre_sha256=pre_sha,
                actual_sha256=actual_sha,
                expected_sha256=_sha256_text(expected_post_substring),
                diff_summary="file is byte-identical to pre-state",
            )

    # The expected substring must be present.
    if expected_post_substring and expected_post_substring not in actual:
        return VerifyResult(
            status=VerifyStatus.MISMATCH,
            path=abs_path,
            actual_sha256=actual_sha,
            expected_sha256=_sha256_text(expected_post_substring),
            diff_summary=(
                f"expected substring not present in {abs_path}; "
                f"file contains {len(actual)} chars; "
                f"expected substring was {len(expected_post_substring)} chars"
            ),
        )

    # Stricter check — full file content matches expectation.
    if full_expected is not None:
        full_sha = _sha256_text(full_expected)
        if full_sha != actual_sha:
            return VerifyResult(
                status=VerifyStatus.PARTIAL,
                path=abs_path,
                expected_sha256=full_sha,
                actual_sha256=actual_sha,
                diff_summary=(
                    f"substring present but full file content differs "
                    f"(expected {len(full_expected)} chars, got {len(actual)})"
                ),
            )

    return VerifyResult(
        status=VerifyStatus.OK,
        path=abs_path,
        actual_sha256=actual_sha,
        expected_sha256=_sha256_text(expected_post_substring) if expected_post_substring else None,
    )


# ── replace verification ─────────────────────────────────────────────


def verify_replace(
    path: str,
    old_string: str,
    new_string: str,
    reader: Callable[[str], str],
) -> VerifyResult:
    """Confirm that *path* contains *new_string* AND that *old_string*
    is no longer present (i.e. the replace was a 1:1 swap, not a 1:N
    fan-out where the new text was inserted without removing the old).

    This catches the subtle class where ``old_string`` matched multiple
    times, the model's patch tool replaced only the first match, and
    the rest of the file still has the old text. The new text is
    present (substring check passes) but the *intent* of the patch
    wasn't fully realised.
    """
    abs_path = os.path.realpath(os.path.expanduser(path))
    try:
        actual = reader(abs_path)
    except FileNotFoundError:
        return VerifyResult(
            status=VerifyStatus.MISSING,
            path=abs_path,
            diff_summary="file not found after replace",
        )

    actual_sha = _sha256_text(actual)
    new_present = new_string in actual if new_string else True
    old_absent = old_string not in actual if old_string else True

    if not new_present:
        return VerifyResult(
            status=VerifyStatus.MISMATCH,
            path=abs_path,
            actual_sha256=actual_sha,
            diff_summary=(
                f"new_string ({len(new_string)} chars) not found in {abs_path} "
                f"after the replace"
            ),
        )
    if not old_absent:
        # Count how many old_string occurrences remain — the message
        # is more useful if we tell the model the count.
        remaining = actual.count(old_string)
        return VerifyResult(
            status=VerifyStatus.PARTIAL,
            path=abs_path,
            actual_sha256=actual_sha,
            diff_summary=(
                f"old_string still present in {abs_path} after the replace "
                f"({remaining} occurrence{'s' if remaining != 1 else ''} remain). "
                f"Likely cause: old_string matched multiple times in the file. "
                f"Include more surrounding context to make the match unique."
            ),
        )

    return VerifyResult(
        status=VerifyStatus.OK,
        path=abs_path,
        actual_sha256=actual_sha,
    )
