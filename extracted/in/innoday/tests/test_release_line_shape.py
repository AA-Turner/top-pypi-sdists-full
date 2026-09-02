"""A release line keeps all four of its parts: ticket, prose, people, verdict.

The line a person reads is `<ticket link> <human summary> <people> <verdict>`.
Three of the four survived being saved. The verdict did not -- it was computed
live from pull-request state and never written down -- and `people` was narrowed
to the single name the board carried.

Worse, the documented way to save a release summary did not work at all. The
skill says to post an `innoday releases content` item back through
`save_project_summary`; `SummaryItemPayload` forbids extra fields, so that call
failed with ten `extra_forbidden` errors at once. A release summary could only be
stored by stripping it to a stand-up line -- which is exactly where its verdict
and its second contributor were going.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from src.routers.summaries import SummaryItemPayload
from src.routers.webui.render import _people_line, _verdict_pill
from src.services.summary_service import SummaryService


def _release_item(**over):
    """An item shaped exactly as `innoday releases content` emits one."""
    item = {
        "ref": "BPAI-334",
        "ticket_id": 1130,
        "assignee_user_id": "u-unurbat",
        "is_design": False,
        "board_ref": "BPAI-334",
        "innoday_ref": "BPAI-41",
        "url": "https://linear.app/havilandsoftware/issue/BPAI-334",
        "title": "Implement Predict Reports",
        "status": "done",
        "state": "shipped",
        "people": ["Unurbat T.", "George M."],
        "prs": [{"repo": "bps-ui-v2", "number": 226, "merged": True}],
        "gaps": [],
        "body_markdown": "Property reports now run end to end.",
    }
    item.update(over)
    return item


class TestAReleaseItemCanBeSavedAtAll:
    def test_the_assembled_shape_is_accepted(self):
        """Ten `extra_forbidden` errors, on the one call the skill documents."""
        payload = SummaryItemPayload(**_release_item())
        assert payload.state == "shipped"
        assert payload.people == ["Unurbat T.", "George M."]

    def test_an_unknown_field_is_still_a_422(self):
        """Accepted, not un-forbidden. The next field added to the release
        payload has to name itself rather than vanish."""
        with pytest.raises(Exception):
            SummaryItemPayload(**_release_item(sentiment="upbeat"))


class TestTheVerdictIsStoredNotRecomputed:
    def _stored(self, **over):
        payload = SummaryItemPayload(**_release_item(**over)).model_dump()
        return SummaryService._summary_item("s-1", payload, default_rank=0)

    def test_state_lands_in_the_verdict_column(self):
        assert self._stored().verdict == "shipped"

    def test_verdict_may_also_be_named_directly(self):
        """One column, either spelling -- `releases content` says `state`, a
        narrator writing a line by hand says `verdict`."""
        assert self._stored(state=None, verdict="not_merged").verdict == "not_merged"

    def test_everyone_credited_is_kept(self):
        """A ticket two people delivered stored the first and lost the second."""
        assert self._stored().people == ["Unurbat T.", "George M."]

    def test_a_bare_string_is_wrapped_not_exploded(self):
        """Stored as a JSON list, a bare string becomes a list of characters.

        The HTTP boundary types this as a list and rejects a string outright,
        which is right. `_summary_item` is also reached directly -- from the MCP
        path and from service callers -- and has to be safe on its own.
        """
        stored = SummaryService._summary_item(
            "s-1", {"people": "Ken", "body_markdown": "x"}, default_rank=0
        )
        assert stored.people == ["Ken"]

    def test_the_http_boundary_insists_on_a_list(self):
        with pytest.raises(Exception):
            SummaryItemPayload(**_release_item(people="Ken"))

    def test_the_prose_still_survives(self):
        """The part with no other home anywhere."""
        assert self._stored().body_markdown == "Property reports now run end to end."

    def test_nobody_credited_is_none_not_an_empty_list(self):
        """ "Unattributed" and "credited to nobody" are different claims."""
        assert self._stored(people=[], assignee_display=None).people is None

    def test_the_board_name_backfills_when_people_is_absent(self):
        stored = self._stored(people=None, assignee_display="Jasminder pal singh")
        assert stored.people == ["Jasminder pal singh"]


class TestTheUiShowsTheVerdictItWasGiven:
    def test_a_shipped_verdict_reads_as_shipped(self):
        html = _verdict_pill("shipped")
        assert "shipped" in html and "sverdict" in html

    def test_underscores_do_not_reach_the_screen(self):
        assert "not merged" in _verdict_pill("not_merged")

    def test_missing_code_and_unmerged_code_share_a_colour(self):
        """Both need a decision before the release can claim the ticket."""
        assert "missing" in _verdict_pill("no_code")
        assert "missing" in _verdict_pill("not_merged")

    def test_no_verdict_renders_nothing_rather_than_a_guess(self):
        """Every row written before the column has none, and inventing one is
        the recomputation this whole change exists to stop."""
        assert _verdict_pill(None) == ""
        assert _verdict_pill("") == ""

    def test_an_unrecognised_verdict_still_renders(self):
        """The vocabulary can grow server-side without this dropping a value."""
        assert "brand new" in _verdict_pill("brand_new")

    def test_two_people_are_both_named(self):
        assert "George M." in _people_line(["Unurbat T.", "George M."], "Unurbat T.")

    def test_one_person_is_left_to_the_owner_bubble(self):
        """It is already on the row; repeating it underneath is noise."""
        assert _people_line(["Ken"], "Ken") == ""

    def test_nobody_renders_nothing(self):
        assert _people_line(None, None) == ""


class TestTheReleaseNoteBullet:
    """The prose was already right; what stood behind it was missing.

    A bullet said a property report now runs end to end and did not say which
    ticket, who built it, which pull requests delivered it, or how it was judged.
    """

    from src.services.summary_line import bullet, provenance

    PROSE = (
        "**New property report** — a per-property report is now available end "
        "to end,\n  from the underlying data through to the page a user opens."
    )

    def _full(self):
        return type(self).bullet(
            self.PROSE,
            ticket_ref="BPAI-334",
            people=["Unurbat T.", "George M."],
            # `merged` on both, because every pull request in a release's
            # `included` block has merged by definition -- a fixture without it
            # is not the shape the engine emits.
            prs=[
                {"repo": "bps-ui-v2", "number": 226, "merged": True},
                {"repo": "bps-api", "number": 587, "merged": True},
            ],
            verdict="shipped",
        )

    def test_the_prose_is_reproduced_byte_for_byte(self):
        """It is the one field a person wrote. Rewrapping it here would make the
        stored text and the rendered text two different things."""
        assert self.PROSE in self._full()

    def test_all_four_provenance_fields_are_present(self):
        out = self._full()
        assert "BPAI-334" in out
        assert "Unurbat T., George M." in out
        assert "bps-ui-v2#226, bps-api#587" in out
        assert "shipped" in out

    def test_provenance_sits_under_the_prose_not_beside_it(self):
        lines = self._full().split("\n")
        assert lines[0].startswith("- ")
        assert lines[-1].strip().startswith("BPAI-334")

    def test_the_verdict_reaches_the_reader_as_words(self):
        assert "partly merged" in type(self).provenance(verdict="partly_merged")

    def test_an_absent_field_is_omitted_not_dashed(self):
        """Prose with less provenance, never prose with a hole in it."""
        out = type(self).provenance(ticket_ref="BPAI-407", verdict="no_code")
        assert out == "BPAI-407 · no code"

    def test_nothing_known_renders_nothing(self):
        assert type(self).provenance() == ""

    def test_a_bullet_with_no_provenance_is_still_a_bullet(self):
        assert type(self).bullet("**Just prose**") == "- **Just prose**"

    def test_a_pull_request_without_a_number_still_names_its_repo(self):
        """A row recovered from a stand-up stores a URL and no number."""
        out = type(self).provenance(prs=[{"repo": "bps-api", "url": "https://x"}])
        assert out == "bps-api"

    def test_people_and_pull_requests_do_not_run_together(self):
        """Both are comma-separated internally, so the field separator cannot
        also be a comma -- 'Unurbat T., George M.' read as two fields."""
        out = type(self).provenance(
            people=["Unurbat T.", "George M."],
            prs=[{"repo": "r", "number": 1, "merged": True}],
        )
        assert out == "Unurbat T., George M. · r#1"


class TestPullRequestsSurviveTheSave:
    def _stored(self, **over):
        from src.routers.summaries import SummaryItemPayload

        payload = SummaryItemPayload(**_release_item(**over)).model_dump()
        return SummaryService._summary_item("s-1", payload, default_rank=0)

    def test_every_pull_request_is_kept(self):
        stored = self._stored(
            prs=[
                {"repo": "bps-ui-v2", "number": 226, "merged": True},
                {"repo": "bps-api", "number": 587, "merged": True},
            ]
        )
        assert [pr["repo"] for pr in stored.prs] == ["bps-ui-v2", "bps-api"]

    def test_only_the_rendered_fields_are_frozen(self):
        """An assembled pull request carries a description; storing GitHub prose
        inside a summary row means two copies of it drifting apart."""
        stored = self._stored(
            prs=[{"repo": "r", "number": 1, "merged": True, "title": "x", "body": "y"}]
        )
        assert set(stored.prs[0]) == {"repo", "number", "url", "merged"}

    def test_a_standup_row_still_yields_one_pull_request(self):
        """One shape out of the column, whichever door the row came in through."""
        stored = SummaryService._summary_item(
            "s-1",
            {"repo": "bps-api", "pr_url": "https://x/599", "pr_state": "merged"},
            default_rank=0,
        )
        assert stored.prs == [
            {"repo": "bps-api", "number": None, "url": "https://x/599", "merged": True}
        ]

    def test_no_code_stores_no_pull_requests(self):
        assert self._stored(prs=[], pr_url=None).prs is None


class TestEveryScopeHasAWord:
    """`--me`, `--scrum`, `--release`. One of the three, said out loud.

    A bare `innoday summary` has always meant your own work and still does, but
    the scope was the one thing a reader could not see in what they typed:
    `/innoday:summary` and `/innoday:summary --scrum` looked like one command with
    an option rather than two different questions.
    """

    @staticmethod
    def _parser():
        import argparse

        from src.cli.commands.summary import SummaryCommands

        parser = argparse.ArgumentParser()
        SummaryCommands.setup_parser(parser)
        return parser

    def test_each_scope_has_its_own_flag(self):
        parser = self._parser()
        assert parser.parse_args(["--me"]).summary_me is True
        assert parser.parse_args(["--scrum"]).scrum is True
        assert parser.parse_args(["--release"]).summary_release is True

    def test_naming_the_default_changes_nothing_about_it(self):
        """`--me` and no flag at all are the same request."""
        parser = self._parser()
        bare = parser.parse_args([])
        named = parser.parse_args(["--me"])
        assert bare.scrum is named.scrum is False
        assert bare.summary_release is named.summary_release is None

    def test_the_flags_are_still_optional(self):
        """Requiring one would break every existing call and every script."""
        assert self._parser().parse_args([]) is not None


class TestTheSaveablePayloadMatchesWhatIsEmitted:
    """Every key `releases content` emits, `save_project_summary` accepts.

    **Asserted against the emitter, never against a hand-written fixture.**
    `_release_item()` above claims to be shaped exactly as an emitted item and is
    typed out by hand -- so when the engine gained `narrative`, and `off_release`
    rows gained `release` and `remedy`, the fixture did not, every test stayed
    green, and echoing a real item back was still a 422. `extra="forbid"` refuses
    a key on *presence*, so even `narrative: None` failed.

    That is the trap `SummaryItemPayload`'s own docstring warns about, one level
    up: it compares its field set to `SummaryLine.to_dict()`, and nothing compared
    it to the release payload it had just been widened for.
    """

    @staticmethod
    def _emitted_shapes() -> list:
        """One key-set per row literal the module is written to return.

        Read out of the source rather than by calling them: they need a database,
        a project and a GitHub client, and the question here is about the *shape*
        they are written to return.

        **Per literal, not unioned.** Unioning first hides which shapes were
        matched, and the shapes are what this class is about: the union of two
        dicts can look complete while one of them was never seen at all.
        """
        import ast
        import inspect

        from src.services import release_content

        source = inspect.getsource(release_content)
        shapes: list = []
        for node in ast.walk(ast.parse(source)):
            if not isinstance(node, ast.Dict):
                continue
            literal = {
                k.value
                for k in node.keys
                if isinstance(k, ast.Constant) and isinstance(k.value, str)
            }
            # A row dict carries a ticket reference and either a verdict or the
            # command that fixes it; every other dict in the module is a pull
            # request, a gap or a totals block.
            #
            # **Two selectors, because there are two off-release shapes.** The
            # candidate row carries `state` inline; the mis-tagged row does not
            # -- `_off_release` adds its `state` afterwards -- so a guard keyed
            # only on `{ref, state}` never saw that literal at all. A key added
            # to it alone would have passed this test and 422'd on
            # `save_project_summary`, which is the failure this class exists to
            # prevent.
            if {"ref", "state"} <= literal or {"ref", "remedy"} <= literal:
                shapes.append(literal)
        return shapes

    @staticmethod
    def _emitted_keys() -> set:
        keys: set = set()
        for shape in TestTheSaveablePayloadMatchesWhatIsEmitted._emitted_shapes():
            keys |= shape
        return keys

    def test_the_emitter_returns_something_recognisable(self):
        """If this fails the introspection is broken, not the payload."""
        keys = self._emitted_keys()
        assert {"ref", "state", "title", "people", "prs"} <= keys

    def test_both_off_release_shapes_are_covered(self):
        """The mis-tagged row is a literal of its own, and it was invisible.

        **Asserting keys cannot show this.** Every key on the mis-tagged literal
        also appears on the candidate one, so the union is identical either way
        and a key assertion passes whether or not the selector reached it. What
        distinguishes them is that the mis-tagged row has no inline `state`, so
        the question is whether a matched *shape* exists without one.
        """
        shapes = self._emitted_shapes()
        assert [s for s in shapes if "state" in s], (
            "the item/candidate shape is unmatched"
        )
        assert [s for s in shapes if "state" not in s], (
            "no matched literal lacks `state`, so the mis-tagged off-release row "
            "is invisible to this guard -- a key added only to it would 422 on save"
        )

    def test_every_shape_is_accepted_on_its_own(self):
        """Per shape, not on the union -- for the same reason as above."""
        from src.routers.summaries import SummaryItemPayload

        declared = set(SummaryItemPayload.model_fields)
        for shape in self._emitted_shapes():
            missing = sorted(shape - declared)
            assert not missing, (
                f"this row shape emits keys `save_project_summary` refuses: {missing}"
            )

    def test_every_emitted_key_is_accepted(self):
        from src.routers.summaries import SummaryItemPayload

        declared = set(SummaryItemPayload.model_fields)
        missing = sorted(self._emitted_keys() - declared)
        assert not missing, (
            "release content emits keys `save_project_summary` refuses, so "
            f"echoing an item back is a 422: {missing}"
        )


class TestAnUnmergedPullRequestSaysSo:
    """The one thing a release line most needs to say about a pull request.

    A release's pull requests carry `merged` and nothing else -- no `state` -- so
    a lookup for `state` alone rendered an unmerged one byte-identical to a
    merged one, on every release line, live and stored.
    """

    from src.services.summary_line import pr_label, provenance

    def test_merged_needs_no_marker(self):
        """Every pull request in `included` merged by definition; marking each
        of them is noise on the common case."""
        assert type(self).pr_label({"repo": "r", "number": 1, "merged": True}) == "r#1"

    def test_not_merged_is_marked(self):
        assert (
            type(self).pr_label({"repo": "r", "number": 1, "merged": False})
            == "r#1 (open)"
        )

    def test_a_standup_row_uses_its_own_word(self):
        """`closed` and `open` are different, and the row knows which."""
        assert "(closed)" in type(self).pr_label(
            {"repo": "r", "url": "https://x/pull/9", "pr_state": "closed"}
        )

    def test_an_unknown_merge_state_claims_nothing(self):
        """Neither field present is genuinely unknown, and "(open)" would be an
        assertion rather than a reading."""
        assert type(self).pr_label({"repo": "r", "number": 1}) == "r#1"


class TestOneVerdictVocabulary:
    """`release_view` had its own words, and the two disagreed.

    `shipped_untagged` read "shipped, on no release" in `releases summarize` and
    "shipped untagged" in `summary --release` and on the dashboard -- the same
    verdict, two phrasings, across the surfaces this module exists to keep
    identical.
    """

    from src.cli.utils.release_view import verdict_label
    from src.services.summary_line import provenance

    @pytest.mark.parametrize(
        "verdict",
        [
            "shipped",
            "partly_merged",
            "not_merged",
            "not_started",
            "no_code",
            "shipped_untagged",
            "started_untagged",
        ],
    )
    def test_both_surfaces_say_the_same_words(self, verdict):
        assert type(self).provenance(verdict=verdict) == type(self).verdict_label(
            verdict, icon=False
        )

    def test_an_unknown_verdict_still_reads_as_words(self):
        assert type(self).provenance(verdict="brand_new") == "brand new"


class TestTheTwoRenderersAreOne:
    """A stand-up line and a release note are assembled by the same function.

    They were assembled by two: `release_view._evidence` joined the fields with
    `·` itself while `summary_line.provenance` did the same job for the stand-up,
    and the copies had already drifted on the two things they were most likely to
    -- what an absent field leaves behind, and what an unknown merge state
    claims. This class is what stops a third copy appearing.
    """

    ITEM = {
        "ref": "BPAI-402",
        "narrative": "Lumen now answers policy questions correctly.",
        "state": "partly_merged",
        "people": ["Alex Y."],
        "prs": [
            {"repo": "auditagent", "number": 124, "merged": True},
            {"repo": "bps-api", "number": 603, "merged": False},
        ],
    }

    def _standup_tail(self):
        from src.cli.commands import summary as standup
        from src.services import summary_line

        # The same facts, spelled the way a stored stand-up row spells them.
        line = {
            "ticket_ref": "BPAI-402",
            "body_markdown": "Lumen now answers policy questions correctly.",
            "verdict": "partly_merged",
            "people": ["Alex Y."],
            "prs": self.ITEM["prs"],
            "status": None,
            "occurred_at": None,
        }
        return summary_line.provenance(
            ticket_ref=standup._ref_for_line(line),
            people=standup._people_for_line(line, True),
            prs=standup._prs_for_line(line),
            verdict=standup._standing(line),
            icon=True,
        )

    def test_the_same_facts_render_the_same_tail(self):
        from rich.markup import render

        from src.cli.utils.release_view import _evidence

        # `_evidence` escapes for Rich; the stand-up escapes at its own call
        # site, so they are compared as the text a reader sees.
        release = str(render(_evidence(self.ITEM, icon=True)))
        assert release == self._standup_tail()
        assert (
            release
            == "BPAI-402 · Alex Y. · auditagent#124, bps-api#603 (open) · ◐ partly merged"
        )

    def test_the_release_view_no_longer_joins_the_line_itself(self):
        """Read from the source, because a second `·` join is exactly how the
        copies came back last time."""
        import inspect

        from src.cli.utils import release_view

        body = inspect.getsource(release_view._evidence)
        assert "summary_line.provenance" in body
        assert '" · ".join' not in body

    def test_a_release_pull_request_missing_its_number_is_not_repo_hash_none(self):
        """`pr_refs` built the reference itself and printed `repo#None` for a
        pull request whose number lives only in its URL."""
        from src.cli.utils.release_view import pr_refs

        assert pr_refs(
            [{"repo": "bps-api", "url": "https://g/x/pull/611", "merged": True}]
        ) == ("bps-api#611")


class TestWhereTheThingStandsIsOneField:
    """The stand-up's status chip and the release's verdict were two fields.

    One sat after the prose on the heading line and the other sat fourth in the
    provenance line, so the same question -- where does this stand? -- was
    answered in a different place depending on which summary you were reading.
    """

    def _line(self, **kw):
        base = {
            "ticket_ref": "PF-1",
            "body_markdown": "Something moved.",
            "status": "in_review",
            "verdict": None,
            "state": None,
        }
        base.update(kw)
        return base

    def test_a_judged_row_reports_its_verdict(self):
        from src.cli.commands.summary import _standing

        assert _standing(self._line(verdict="shipped")) == "shipped"

    def test_the_verdict_wins_over_the_board_column(self):
        """A release has looked at the code; the board column has not."""
        from src.cli.commands.summary import _standing

        assert (
            _standing(self._line(verdict="not_merged", status="done")) == "not_merged"
        )

    def test_an_unjudged_row_reports_the_board_column(self):
        from src.cli.commands.summary import _standing

        assert _standing(self._line()) == "🟢 In Review"

    def test_a_row_with_neither_reports_nothing(self):
        """Rather than an empty slot, which `provenance` would then have to drop
        anyway -- and a dash reads as a fact nobody has."""
        from src.cli.commands.summary import _standing

        assert _standing(self._line(status=None)) is None

    def test_the_heading_no_longer_carries_a_chip(self):
        import sys
        from pathlib import Path

        sys.path.insert(0, str(Path(__file__).parent))
        from test_cli_summary import line, payload

        from src.cli.commands.summary import render_summary

        out = render_summary(
            payload(active=[line()]), scrum=True, org_alias="hs", project_label="PF"
        )
        heading = next(row for row in out.splitlines() if row.startswith("▸"))
        assert "In Review" not in heading
        # Still on the page, one field of five, where a release puts its verdict.
        assert "🟢 In Review" in out


class TestTheSkillDescribesOneLine:
    """Two templates in one skill is why the team got different answers.

    The skill carried both: one saying the ticket leads the sentence and credit
    closes the item, another saying prose leads and the ticket sits in a
    provenance line underneath. Following either was following the skill.
    """

    # Anchored to this file, not to the working directory pytest was started in.
    SKILL = (
        Path(__file__).resolve().parents[1] / "plugins/innoday/skills/summary/SKILL.md"
    )

    def _text(self):
        return type(self).SKILL.read_text()

    def test_the_template_is_stated_before_any_scope(self):
        text = self._text()
        one_line = text.index("One line, whichever summary this is")
        release = text.index("### When the window is a release")
        assert one_line < release

    def test_the_competing_template_is_gone(self):
        text = self._text()
        assert "The ticket leads" not in text
        assert "Credit closes the item" not in text

    def test_the_release_section_adds_scope_and_not_a_second_shape(self):
        text = self._text()
        section = text[text.index("What the release scope adds") :]
        section = section[: section.index("#### Then the map")]
        assert "The line is the one above, unchanged." in section


class TestThereIsNoThirdCopy:
    """`releases summarize` rendered the same row two ways in one run.

    `_render_attention` built the line by hand -- unfiltered and un-bold -- so an
    off-release ticket whose pull-request authors did not resolve printed
    `BPAI-407 ·  · bps-api#611 · shipped, on no release` fifteen lines below the
    same row rendered correctly by `prose_lines`. The invariant test in
    `TestTheTwoRenderersAreOne` did not catch it because it reads only
    `_evidence`.
    """

    ROW = {
        "ref": "BPAI-407",
        "title": "Untagged but shipped",
        "narrative": None,
        "state": "shipped_untagged",
        # Reachable: `_off_release` builds this from PR authors it could resolve.
        "people": [],
        "prs": [{"repo": "bps-api", "number": 611, "merged": True}],
    }

    def _attention(self):
        from rich.console import Console

        from src.cli.commands import releases as releases_module

        console = Console(force_terminal=False, width=200, no_color=True)
        original = releases_module.console
        releases_module.console = console
        try:
            with console.capture() as captured:
                releases_module.ReleasesCommands._render_attention(
                    {"off_release": [type(self).ROW], "unticketed": []}
                )
            return captured.get()
        finally:
            releases_module.console = original

    def test_an_unattributed_row_leaves_no_dangling_separator(self):
        assert "·  ·" not in self._attention()

    def test_it_renders_the_same_line_prose_lines_would(self):
        from rich.console import Console

        from src.cli.utils.release_view import prose_lines

        console = Console(force_terminal=False, width=200, no_color=True)
        with console.capture() as captured:
            for line in prose_lines([type(self).ROW]):
                console.print(line)
        expected = [row for row in captured.get().splitlines() if row.strip()]
        got = [
            row
            for row in self._attention().splitlines()
            if row.strip() and row.strip() != "Needs attention"
        ]
        assert got == expected


class TestAReleaseScopedStandUpSaysWhatItsFourthFieldIs:
    """It has a board column and no verdict, and the two are not the same claim.

    `SummaryLine` carries `status` and `pr_state` and nothing that says whether
    the code landed, so this surface prints `🟢 In Review` where
    `releases summarize` prints `○ not merged`. Deriving one here would be a
    second answer to the question the line shape exists to answer once -- so the
    scope states which question it is answering.
    """

    def _boundary(self):
        from src.cli.commands.summary import _boundary

        return "\n".join(
            _boundary(
                {
                    "release": "v1.11.0",
                    "release_ticket_count": 10,
                    "tickets_without_release_count": 209,
                }
            )
        )

    def test_it_still_states_the_slice(self):
        assert "Covers only the 10 tickets" in self._boundary()

    def test_it_names_the_field_and_where_the_verdict_lives(self):
        text = self._boundary()
        assert "board column" in text
        assert "releases summarize" in text

    def test_a_windowed_stand_up_says_none_of_it(self):
        """There is no release, so there is no slice and no second question."""
        from src.cli.commands.summary import _boundary

        assert _boundary({"window_spec": "3d"}) == []


class TestTheSkillSaysWhichFieldsEachScopeHas:
    SKILL = (
        Path(__file__).resolve().parents[1] / "plugins/innoday/skills/summary/SKILL.md"
    )

    def _text(self):
        return type(self).SKILL.read_text()

    def test_personal_mode_is_documented_as_dropping_people(self):
        """It was attributed to `--scrum` only, so personal mode's five fields
        matched neither documented shape."""
        text = self._text()
        assert "personal (no flag)" in text
        assert "people is dropped" in text

    def test_the_mark_is_named_as_a_rendering_rather_than_a_field(self):
        """The template says `partly merged`; both commands emit
        `◐ partly merged`. Claude writes the words."""
        text = self._text()
        assert "the terminal adds the mark itself" in text
        assert "◐ partly merged" in text
