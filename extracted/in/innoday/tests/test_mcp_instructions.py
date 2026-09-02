"""The server has to tell a host what it is for.

It offered 48 tools and no guidance. A model deciding how to answer "what
shipped in this release" saw a list of names and no reason to prefer them over
the shell it already had — so it reached for `gh`, which is right there, needs no
ids, and works. Twice in one day, and the second time it exported a personal
OAuth token to make a release command run.

**These tests cannot check that the wording persuades anyone.** Prose is not unit
testable, and asserting on substrings would fail on innocent rewording while
passing on a paraphrase that lost the point. What they can check is that the
field is *populated and reaching the host* — which is the failure that actually
happened — and that the two rules with a credential behind them are still named
somewhere in it.
"""

from __future__ import annotations

import pytest

from src.mcp.server import app


@pytest.fixture
def instructions() -> str:
    """Whitespace-collapsed, because the source is hard-wrapped prose.

    The first version of this matched raw text and failed on a phrase that
    happened to straddle a line break -- the exact brittleness the module
    docstring warns about, caught by the test rather than by review.
    """
    return " ".join((app.instructions or "").split())


class TestTheHostIsToldSomething:
    def test_the_server_ships_instructions_at_all(self, instructions):
        """The whole defect: this was empty, so a host got names and nothing
        else."""
        assert instructions.strip(), "FastMCP was constructed without instructions"

    def test_they_say_more_than_a_tagline(self, instructions):
        """A one-line description would satisfy 'not empty' and teach nothing."""
        assert len(instructions) > 500

    def test_innoday_is_named_as_the_source_of_truth(self, instructions):
        assert "source of truth" in instructions.lower()


class TestTheTwoRulesWithACredentialBehindThem:
    """Named explicitly because each one has already cost something real."""

    def test_the_personal_token_rule_is_stated(self, instructions):
        """`gh auth token` is a person's own login. A release must not be cut
        with it, and exporting one to make the command run also buries the
        defect that it was needed at all."""
        assert "GH_TOKEN" in instructions

    def test_a_failing_call_is_the_finding(self, instructions):
        """Routing around a broken InnoDay call yields a correct-looking answer
        assembled outside the product, so nobody learns it is broken."""
        lowered = instructions.lower()
        assert "failing innoday call is the finding" in lowered

    def test_verification_is_still_allowed(self, instructions):
        """A rule with no escape hatch gets ignored wholesale. Reading GitHub to
        check what InnoDay said must stay legitimate, or the rule reads as
        'never look', which nobody obeys while debugging."""
        assert "verif" in instructions.lower()


class TestTheSummaryWorkflowIsSpelledOut:
    def test_it_says_the_caller_narrates(self, instructions):
        """No route generates prose. A host that does not know this waits for a
        summary that is never coming."""
        assert "narrate" in instructions.lower()

    def test_the_ordered_steps_are_present(self, instructions):
        for tool in (
            "sync_board",
            "get_scrum_summary",
            "save_project_summary",
        ):
            assert tool in instructions, f"{tool} missing from the workflow"


class TestTheProjectAmbiguityIsCalledOut:
    def test_it_warns_that_the_default_is_the_launch_directory(self, instructions):
        """The server resolves from where it was started, which is usually not
        the project under discussion — a wrong-project answer that looks right."""
        lowered = instructions.lower()
        assert "project_id" in instructions
        assert "launch" in lowered or "launched" in lowered
