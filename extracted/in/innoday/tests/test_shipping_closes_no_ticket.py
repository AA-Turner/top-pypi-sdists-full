"""Nothing may promise that shipping closes tickets, because it does not.

`_bulk_close_tickets_for_release` set every ticket carrying a version to DONE
when the release shipped. It was removed deliberately: membership in a release
is a free-text string somebody typed or dragged, not evidence that work
happened, so a ticket nobody ever started was closed with a completion
timestamp exactly like one that shipped. That destroyed the only record it had
not been done, wrote nothing back to the external board, and could not be
undone. `_shipped_stamp` carries the full account.

The workflow launcher went on telling people the opposite for months --
"Tags every repo, publishes the release, closes its tickets" -- which is the
worse half of the bug: somebody reading it has every reason to leave finished
work open and wait for the release to tidy up.

A prose claim cannot be verified by running the code that contradicts it, so
this guards the two directions that are checkable: the removed function stays
removed, and no user-facing string re-promises what it did.
"""

from __future__ import annotations

import pathlib
import re

SRC = pathlib.Path(__file__).resolve().parents[1] / "src"

#: Wordings that assert closing tickets happens.
CLOSES = re.compile(
    r"(clos(e|es|ing)|complet(e|es|ing)|resolv(e|es|ing))\s+"
    r"(its|the|every|all)?\s*tickets?\b",
    re.IGNORECASE,
)

#: ...but only when the same string is talking about a release.
#:
#: `innoday tickets close` prints "Closing ticket 42" and is entirely correct:
#: closing one ticket on purpose is the supported way to do it. What must never
#: reappear is the claim that *shipping* does it for you, so both halves have
#: to be present before anything is flagged.
RELEASE = re.compile(r"\brelease|\bship|\btag(s|ging)?\b|blast\s*off", re.IGNORECASE)


def PROMISE(text: str):
    """A match only when a release is claimed to close tickets."""
    return CLOSES.search(text) and RELEASE.search(text)


def _user_facing_strings(path: pathlib.Path) -> list[tuple[int, str]]:
    """Quoted strings, minus the docstrings that explain the history.

    The explanation of *why* shipping no longer closes tickets necessarily
    contains the phrase it is warning about; flagging it would make the honest
    comment the thing that fails.
    """
    found: list[tuple[int, str]] = []
    text = path.read_text()
    in_doc = False
    for lineno, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith(('"""', 'r"""', "#:")) or stripped.startswith("#"):
            in_doc = stripped.startswith(('"""', 'r"""')) and stripped.count('"""') == 1
            continue
        if in_doc:
            if '"""' in stripped:
                in_doc = False
            continue
        for match in re.finditer(r'"([^"\n]{8,})"', line):
            found.append((lineno, match.group(1)))
    return found


class TestTheRemovalStaysRemoved:
    def test_the_bulk_close_function_is_gone(self):
        """Only the explanation of its removal may mention it."""
        offenders = [
            f"{path.relative_to(SRC)}:{lineno}"
            for path in SRC.rglob("*.py")
            for lineno, line in enumerate(path.read_text().splitlines(), 1)
            if "def _bulk_close_tickets_for_release" in line
        ]
        assert not offenders, f"the function came back: {offenders}"


class TestNothingPromisesItAgain:
    def test_no_user_facing_string_says_a_release_closes_tickets(self):
        offenders = [
            f"{path.relative_to(SRC)}:{lineno} — {text[:80]}"
            for path in SRC.rglob("*.py")
            for lineno, text in _user_facing_strings(path)
            if PROMISE(text)
        ]
        assert not offenders, (
            "shipping touches no ticket; closing finished work is a person's "
            "job through the board or `innoday tickets update`. Offending "
            "strings: " + "; ".join(offenders)
        )

    def test_the_pattern_would_catch_the_wording_that_shipped(self):
        """Guards the test above from passing because it matches nothing.

        This is the exact string the workflow launcher carried.
        """
        assert PROMISE("Tags every repo, publishes the release, closes its tickets.")

    def test_the_corrected_wording_is_allowed(self):
        """ "Closing them stays your call" is the fix, not a violation."""
        assert not PROMISE(
            "Tags every repo and publishes the release. Tickets are left alone "
            "— closing them stays your call."
        )
