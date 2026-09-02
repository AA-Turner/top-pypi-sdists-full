"""The one thing about the `/innoday:summary` skill a test can honestly hold (#563).

Two of that issue's three defects were produced by `SKILL.md`, not by any code:
the narrator did what it was told, and what it was told was wrong. Defect 1 was
an instruction to close a client's work summary with InnoDay's own unmapped
assignee count, which the zero case was never scoped out of; defect 2 was the
*absence* of a rule, so a true sentence about a different project passed "never
invent a fact".

**Why this file is one assertion and not a checklist of phrases.** The version
of it that shipped with the first draft of #565 asserted eight substrings from
the corrected prose -- "InnoDay's own plumbing", "only about this project",
"footer", and so on. Review demonstrated both failure directions against it:

* Defect 1 was **re-added in paraphrase** ("Finish by reporting how many board
  names have no InnoDay user, every time, including when the answer is none")
  and all eight assertions stayed green. The file could hold the rule and its
  contradiction at once.
* Innocuous rewording **broke it**: `own plumbing` → `internal plumbing`, and
  `only about this project` → `about this project alone`.

Those are the two properties you want from a guard, both inverted. A guard that
green-lights the defect while failing on a synonym is not weak, it is
misleading -- it spends a reviewer's trust on nothing. So the phrase assertions
are gone rather than tightened.

**What is left, and exactly what it is worth.** The single test below pins the
*removed instruction* -- the concrete text that produced the observed sentence
-- rather than any of the prose that replaced it. A revert of that hunk cannot
dodge it, including a revert that reflows or recases the lines, because the
comparison is whitespace-normalised and lowercased. That is a real regression
this repo could plausibly suffer: somebody restores a deleted bullet.

**What no test here can do.** It cannot tell that the rule is *stated*, only
that its opposite is not literally present. Any paraphrase re-introduces defect
1 undetected -- the reviewer's own paraphrase contains neither "unmapped" nor
"close with", so there is no pattern to match on, and the set of ways to say
"tell me the count" in English is not enumerable. The same goes for defect 2 in
full: it was fixed by *adding* a rule, and "a rule to this effect is present and
means what it says" is not a substring question.

**So the real guard is a human reading `plugins/innoday/skills/summary/SKILL.md`
in the diff.** Step 4's two rules -- write only about this project from this
payload, and say nothing about InnoDay itself including the zero case -- are
prose, reviewed as prose. If you are changing them, the reviewer is the check;
this file will not stop you and does not claim to.

The server-side halves *are* pinned properly, by tests that read state rather
than words: `TestProjectIsolation` in `tests/test_summary_engine.py` (a sibling
project's tickets, live summary and code activity stay out of this project's
summary) and `TestReleaseScope` (the release predicate, the boundary counts, and
absence measured inside the scope).
"""

import re
from pathlib import Path

import pytest

SKILL = (
    Path(__file__).resolve().parents[1]
    / "plugins"
    / "innoday"
    / "skills"
    / "summary"
    / "SKILL.md"
)

#: The instruction that produced the observed sentence, verbatim from `main`:
#:
#:     - If `unmapped_assignees` is non-empty, close with the fix, once:
#:       "N assignees unmapped — map at /ui/<org>/profile".
#:
#: Two fragments rather than the whole bullet, so that restoring either line
#: alone still trips. Lowercase, and with runs of whitespace collapsed, because
#: markdown re-wrapping moves the newline inside the second fragment and an
#: exact-substring guard would silently stop matching -- passing while the
#: instruction is back.
REMOVED_DIRECTIVE_FRAGMENTS = (
    "close with the fix",
    "assignees unmapped — map at",
)


@pytest.fixture(scope="module")
def normalised_text() -> str:
    return re.sub(r"\s+", " ", SKILL.read_text()).lower()


def test_the_removed_unmapped_count_directive_has_not_come_back(normalised_text):
    """Defect 1 was this instruction executed in the case it never scoped.

    Reverting the hunk that deleted it is the failure this catches. A paraphrase
    of it is not caught -- see the module docstring; that is the reviewer's job,
    not this file's.
    """
    for fragment in REMOVED_DIRECTIVE_FRAGMENTS:
        assert re.sub(r"\s+", " ", fragment).lower() not in normalised_text, (
            f"{fragment!r} is back in SKILL.md — that instruction is what put "
            "InnoDay's unmapped assignee count into a client's work summary "
            "(#563, defect 1)"
        )
