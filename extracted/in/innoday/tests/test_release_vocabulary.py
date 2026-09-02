"""The verdict and recommendation vocabularies are closed, and enforced.

They were four hand-kept copies of one list: bare string literals at eight
assignment sites in `release_content`, a rendering table in `summary_line`, a
TypeScript union in the UI, and the release-review skill's prose. Nothing
reconciled them. `verdict_label` deliberately passes an unknown state through and
`SummaryItemPayload.state` was a bare `Optional[str]`, so the only thing that
would have refused a new value was a UI typecheck the API never consulted.

Two verdicts the skill described -- `release_candidate` and `unticketed_design`
-- existed in no code at all. That is the failure these tests exist to make
impossible: a closed set that only prose closes is not closed.
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest
from pydantic import ValidationError

from src.domain.release import Recommendation, ReleaseVerdict
from src.services.summary_line import _VERDICTS, verdict_label

#: Absolute, so the scan cannot silently cover nothing when pytest's rootdir is
#: not the working directory -- a relative path made this test's reach depend on
#: how it was invoked.
_ROOT = Path(__file__).resolve().parent.parent

#: Every module that names a verdict. The first version scanned only the service
#: and therefore never saw `src/cli/commands/releases.py`, which compared against
#: `"shipped_untagged"` directly -- a fifth copy of the vocabulary in the very
#: commit that claimed to have closed it.
SCANNED = (
    _ROOT / "src/services/release_content.py",
    _ROOT / "src/services/summary_line.py",
    _ROOT / "src/cli/commands/releases.py",
    _ROOT / "src/routers/webui/data.py",
)


def _reads_state(node: ast.AST) -> bool:
    """Whether this expression reads a `state` field, however it is spelled.

    `row["state"]`, `row.get("state")` and `row.state` are the three shapes in
    the tree today.
    """
    if isinstance(node, ast.Subscript):
        return isinstance(node.slice, ast.Constant) and node.slice.value == "state"
    if isinstance(node, ast.Attribute):
        return node.attr == "state"
    if isinstance(node, ast.Call):
        func = node.func
        if isinstance(func, ast.Attribute) and func.attr == "get" and node.args:
            first = node.args[0]
            return isinstance(first, ast.Constant) and first.value == "state"
    return False


class TestEveryVerdictIsRenderable:
    def test_every_verdict_has_words(self):
        """A member added to the enum and forgotten in `_VERDICTS` renders as its
        own key -- `on_shipped_release` instead of "left behind by a release" --
        which ships a raw schema token into a client-facing release note."""
        missing = sorted(v.value for v in ReleaseVerdict if v.value not in _VERDICTS)
        assert not missing, f"verdicts with no words: {missing}"

    def test_no_words_without_a_verdict(self):
        """The other direction: a label kept for a verdict that no longer exists
        is dead prose nobody will notice is unreachable."""
        known = {v.value for v in ReleaseVerdict}
        orphans = sorted(k for k in _VERDICTS if k not in known)
        assert not orphans, f"words for no verdict: {orphans}"

    def test_an_unknown_verdict_still_prints_itself(self):
        """`verdict_label` falls back to `key.replace("_", " ")` on purpose -- a
        verdict the renderer has not been taught is still a fact about the
        release, and blanking it is how a new state ships invisibly.

        This replaces a parametrised test that asserted the label was truthy and
        contained no underscore. Both hold for **any** string, including
        `totally_made_up_verdict`, so it passed for every input and certified
        nothing. `test_every_verdict_has_words` is the assertion that bites."""
        assert verdict_label("totally_made_up", icon=False) == "totally made up"
        assert verdict_label("", icon=False) == ""


class TestTheServiceEmitsNothingUndeclared:
    """Parsed from the source, not from a payload.

    A test that builds a release and inspects the result only covers the states
    that fixture happens to produce. Reading every `"state": <literal>` in the
    module covers the ones no fixture reaches -- which is where an invented
    verdict would actually hide.
    """

    @staticmethod
    def _strings_in(node: ast.AST) -> set[str]:
        """Every string constant reachable from `node`.

        Walked rather than type-matched. The first version of this test handled
        only a bare `ast.Constant`, so `"state": A if flag else B` and
        `entry["state"] = "shipped"` were both invisible -- and the conditional
        is precisely the shape the module uses. A mutation carrying four bare
        verdict literals passed all twenty-three tests.
        """
        return {
            n.value
            for n in ast.walk(node)
            if isinstance(n, ast.Constant) and isinstance(n.value, str)
        }

    def _emitted_states(self) -> set[str]:
        found: set[str] = set()
        for path in SCANNED:
            tree = ast.parse(path.read_text())
            for node in ast.walk(tree):
                # `{"state": <anything>}` -- including a conditional expression
                if isinstance(node, ast.Dict):
                    for key, value in zip(node.keys, node.values):
                        if isinstance(key, ast.Constant) and key.value == "state":
                            found |= self._strings_in(value)
                # `state = ...` and `entry["state"] = ...`, including conditionals
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        named = isinstance(target, ast.Name) and target.id == "state"
                        subscripted = (
                            isinstance(target, ast.Subscript)
                            and isinstance(target.slice, ast.Constant)
                            and target.slice.value == "state"
                        )
                        if named or subscripted:
                            found |= self._strings_in(node.value)
                # `row.get("state") == "shipped_untagged"` -- a comparison
                # against a literal is a copy of the vocabulary too, and the CLI
                # had one. Matched on AST shape, not on unparsed text: the first
                # attempt searched for `'"state"'` in `ast.unparse(...)`, which
                # normalises every string to single quotes, so it matched nothing
                # and passed while the CLI literal sat there.
                if isinstance(node, ast.Compare) and _reads_state(node.left):
                    for comparator in node.comparators:
                        found |= self._strings_in(comparator)
        return found

    def test_no_bare_verdict_literal_survives(self):
        """Every verdict now goes through the enum, so a string literal assigned
        to `state` is a copy that will drift."""
        known = {v.value for v in ReleaseVerdict}
        stray = sorted(s for s in self._emitted_states() if s in known)
        assert not stray, (
            "these verdicts are still written as bare strings rather than "
            f"through ReleaseVerdict: {stray}"
        )

    def test_every_verdict_is_produced_somewhere(self):
        """Guards the failure this PR was itself indicting: a member declared,
        rendered, documented -- and never assigned by any code path.

        `CONTESTED` shipped exactly that way. Three hand-picked members were
        checked before, which could not see it.
        """
        source = "\n".join(p.read_text() for p in SCANNED)
        unused = sorted(
            v.value for v in ReleaseVerdict if f"ReleaseVerdict.{v.name}" not in source
        )
        assert not unused, (
            "declared, rendered, and never produced by any code path -- the "
            f"failure a closed set exists to prevent: {unused}"
        )


class TestThePayloadRefusesAnInventedValue:
    def test_an_unknown_verdict_is_a_422(self):
        from src.routers.summaries import SummaryItemPayload

        with pytest.raises(ValidationError):
            SummaryItemPayload(state="probably_fine")

    def test_an_unknown_recommendation_is_a_422(self):
        from src.routers.summaries import SummaryItemPayload

        with pytest.raises(ValidationError):
            SummaryItemPayload(recommendation="have a think about it")

    def test_a_real_pair_is_accepted(self):
        from src.routers.summaries import SummaryItemPayload

        row = SummaryItemPayload(
            state=ReleaseVerdict.SHIPPED_UNTAGGED,
            recommendation=Recommendation.ATTACH_TICKET_TO_RELEASE,
        )
        assert row.state is ReleaseVerdict.SHIPPED_UNTAGGED
        assert row.recommendation is Recommendation.ATTACH_TICKET_TO_RELEASE

    def test_no_recommendation_is_a_real_answer(self):
        """`no_code` cannot be told from a design ticket awaiting its design pull
        requests, so it carries none rather than guessing at `drop_from_release`."""
        from src.routers.summaries import SummaryItemPayload
        from src.services.release_content import _recommend

        assert _recommend(ReleaseVerdict.NO_CODE.value) is None
        assert SummaryItemPayload(state=ReleaseVerdict.NO_CODE).recommendation is None


class TestTheImpliedMovesAreDeclared:
    def test_every_implied_recommendation_exists(self):
        from src.services.release_content import _IMPLIED

        known = {r.value for r in Recommendation}
        assert not sorted(v for v in _IMPLIED.values() if v not in known)

    def test_every_implied_verdict_exists(self):
        from src.services.release_content import _IMPLIED

        known = {v.value for v in ReleaseVerdict}
        assert not sorted(k for k in _IMPLIED if k not in known)

    def test_both_candidate_states_are_counted(self):
        """`release_candidate` split off `started_untagged` once open pull
        requests were attached. Every count over "candidates" has to span both,
        or it silently stops counting the half with code in flight."""
        from src.services.release_content import _CANDIDATE_STATES

        assert _CANDIDATE_STATES == {
            ReleaseVerdict.STARTED_UNTAGGED.value,
            ReleaseVerdict.RELEASE_CANDIDATE.value,
        }
