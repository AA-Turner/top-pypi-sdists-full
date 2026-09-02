"""One release, two renderings, and the same five fields in both.

A release summary answers four questions -- what changed, who did it, which
pull requests carried it, did it land -- and it used to answer them in four
different places. A reader held a ticket reference in their head and scrolled
between sections to assemble one row.

These pin the two properties that make a line whole rather than a fragment:
every line carries its evidence, and the two views carry the *same* evidence.
A table that quietly showed less than the prose would be worse than not having
it, because the whole reason to offer a table is checking coverage.
"""

from __future__ import annotations

from src.cli.utils.release_view import (
    header_lines,
    people_names,
    pr_refs,
    prose_lines,
    summary_table,
    unnarrated_notice,
    verdict_label,
)

SHIPPED = {
    "ref": "BPAI-334",
    "title": "Implement Predict Reports",
    "narrative": "Property reports now run end to end.",
    "state": "shipped",
    "people": ["Unurbat T.", "George M."],
    "prs": [
        {"repo": "bps-ui-v2", "number": 226, "merged": True},
        {"repo": "bps-api", "number": 587, "merged": True},
    ],
}
PARTLY = {
    "ref": "BPAI-402",
    "title": "Fix Lumen's Policy Info",
    "narrative": "Lumen can now see which jurisdiction a building falls under.",
    "state": "partly_merged",
    "people": ["Alex Y."],
    "prs": [
        {"repo": "auditagent", "number": 124, "merged": True},
        {"repo": "bps-api", "number": 603, "merged": False},
    ],
}
NO_CODE = {
    "ref": "BPAI-407",
    "title": "Small UI Items",
    "narrative": None,
    "state": "no_code",
    "people": [],
    "prs": [],
}


class TestEveryLineCarriesItsEvidence:
    def test_the_prose_line_names_ticket_people_prs_and_verdict(self):
        text = "\n".join(prose_lines([PARTLY]))
        assert "Lumen can now see which jurisdiction" in text
        assert "BPAI-402" in text
        assert "Alex Y." in text
        assert "auditagent#124" in text
        assert "partly merged" in text

    def test_an_unmerged_pull_request_is_marked_in_the_reference(self):
        """Otherwise a list of references reads as a list of things that landed.

        This is the same claim `(Not Merged)` makes about a ticket, made about
        one pull request -- and on a partly-merged ticket it is the only place
        the distinction appears at all.
        """
        assert pr_refs(PARTLY["prs"]) == "auditagent#124, bps-api#603 (open)"

    def test_absent_fields_do_not_leave_dangling_separators(self):
        """`BPAI-407 · no code`, never `BPAI-407 ·  ·  · no code`.

        An empty slot is not information, and a row of separators around one
        reads as damage rather than as absence.
        """
        line = prose_lines([NO_CODE])[1]
        assert line == "  [dim]BPAI-407 · ⚠ no code[/dim]"


class TestTheTwoViewsAgree:
    def test_the_table_carries_the_same_five_fields_as_the_prose(self):
        """The table exists for checking coverage. One that shows less than the
        prose it sits beside cannot be used for that."""
        table = summary_table([SHIPPED, PARTLY, NO_CODE])

        assert [c.header for c in table.columns] == [
            "Ticket",
            "Human summary",
            "People",
            "PRs",
            "Verdict",
        ]
        cells = ["\n".join(str(c) for c in col._cells) for col in table.columns]
        for expected in ("BPAI-402", "Alex Y.", "auditagent#124", "partly merged"):
            assert expected in "\n".join(cells)

    def test_every_release_ticket_appears_in_both(self):
        rows = [SHIPPED, PARTLY, NO_CODE]
        table = summary_table(rows)
        prose = "\n".join(prose_lines(rows))
        refs = "\n".join(str(c) for c in table.columns[0]._cells)
        for row in rows:
            assert row["ref"] in refs
            assert row["ref"] in prose


class TestProseIsTheOnlyFieldWithNoOtherSource:
    def test_a_ticket_with_no_narrative_falls_back_to_its_title(self):
        assert "Small UI Items" in prose_lines([NO_CODE])[0]

    def test_and_the_fallback_is_said_rather_than_left_to_be_noticed(self):
        """A title reads like a summary. Without this line, a release nobody has
        narrated looks narrated and unusually terse."""
        notice = unnarrated_notice([SHIPPED, PARTLY, NO_CODE])
        assert notice is not None
        assert "1 ticket" in notice
        assert "/innoday:summary release" in notice

    def test_a_fully_narrated_release_says_nothing(self):
        assert unnarrated_notice([SHIPPED, PARTLY]) is None


class TestVerdictsReadAsEnglish:
    def test_the_payload_key_is_not_what_gets_printed(self):
        assert "partly merged" in verdict_label("partly_merged")
        assert "partly_merged" not in verdict_label("partly_merged")

    def test_an_unknown_verdict_prints_itself_rather_than_vanishing(self):
        """A state this renderer has not been taught is still a fact about the
        release. Dropping it is how a new verdict ships invisibly."""
        assert "something new" in verdict_label("something_new")


class TestTheHeaderSaysWhetherItShipped:
    def test_it_names_the_version_status_date_and_open_count(self):
        payload = {
            "release_record": {
                "version": "v1.11.0",
                "status": "released",
                "released_at": "2026-08-25T14:12:58+00:00",
                "tickets": 10,
                "open": 6,
            },
            "window": {"label": "since v1.10.0 (2026-08-12)"},
            "commit_count": 36,
        }
        text = "\n".join(header_lines(payload, "BPAI"))
        assert "BPAI v1.11.0" in text
        assert "released" in text
        assert "2026-08-25" in text and "T14:12" not in text
        assert "10 total, 6 open" in text
        assert "36 commits" in text


class TestPeopleArePrintedAsGiven:
    def test_an_unmapped_handle_is_shown_rather_than_replaced(self):
        """Inventing a name for a handle InnoDay cannot resolve is worse than
        showing the handle: one is missing data, the other is wrong data."""
        assert people_names([{"handle": "kengsc"}]) == "kengsc"

    def test_resolved_names_win_over_handles_on_the_same_person(self):
        assert people_names([{"name": "Ken S.", "handle": "kengsc"}]) == "Ken S."
