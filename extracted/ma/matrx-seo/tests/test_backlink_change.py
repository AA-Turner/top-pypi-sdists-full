from __future__ import annotations

from datetime import UTC, datetime, timedelta

import pytest

from matrx_seo.backlink_change import (
    ALERT_SEVERITY_FLOOR,
    ObservationPoint,
    collapse_run,
    diff_chain,
    diff_pair,
    points_for_link,
    severity_for,
)

BASE = datetime(2026, 8, 1, tzinfo=UTC)


def point(
    *,
    n: int = 0,
    anchor: str | None = "best widgets",
    anchors: set[str] | None = None,
    dofollow: bool | None = True,
    state: str = "active",
    target: str | None = "https://mysite.com/widgets",
) -> ObservationPoint:
    resolved = anchors if anchors is not None else ({anchor} if anchor else set())
    return ObservationPoint(
        observation_id=f"obs-{n}",
        run_key=f"run-{n}",
        backlink_id="bl-1",
        site_id="site-1",
        source_url="https://publisher.com/post",
        source_domain="publisher.com",
        target_url=target,
        anchor_texts=frozenset(resolved),
        is_dofollow=dofollow,
        is_live=state != "lost",
        observed_at=BASE + timedelta(days=n),
    )


def row(
    *,
    run: str = "snap-1",
    n: int = 0,
    anchor: str | None = "best widgets",
    dofollow: bool | None = True,
    state: str = "active",
) -> dict:
    """A raw seo.backlink_observation row as the differ reads it."""
    return {
        "id": f"obs-{run}-{anchor}",
        "backlink_id": "bl-1",
        "snapshot_id": run,
        "site_id": "site-1",
        "source_url": "https://publisher.com/post",
        "source_domain": "publisher.com",
        "target_url": "https://mysite.com/widgets",
        "anchor_text": anchor,
        "is_dofollow": dofollow,
        "state": state,
        "first_seen_at": None,
        "last_seen_at": None,
        "lost_at": None,
        "created_at": BASE + timedelta(days=n),
    }


class TestLoss:
    def test_declared_loss_is_the_only_event_for_that_pair(self) -> None:
        # The publisher removed the link AND the anchor differs in the final
        # payload. "Your anchor changed" alongside "your link is gone" is noise.
        changes = diff_pair(
            point(n=0),
            point(n=1, state="lost", anchor="something else", dofollow=False),
        )
        assert [c.change_kind for c in changes] == ["lost"]

    def test_lost_dofollow_outranks_lost_nofollow_and_both_alert(self) -> None:
        lost_do = diff_pair(point(n=0, dofollow=True), point(n=1, state="lost"))[0]
        lost_no = diff_pair(point(n=0, dofollow=False), point(n=1, state="lost", dofollow=False))[0]
        assert lost_do.severity > lost_no.severity
        assert lost_do.is_alertable and lost_no.is_alertable

    def test_severity_is_read_from_what_the_link_WAS(self) -> None:
        # The provider reports the lost row with dofollow=False. The link we
        # lost was a dofollow one, and that is what the severity must reflect.
        lost = diff_pair(point(n=0, dofollow=True), point(n=1, state="lost", dofollow=False))[0]
        assert lost.severity == severity_for("lost", is_dofollow=True)

    def test_restored_link_is_reported(self) -> None:
        changes = diff_pair(point(n=0, state="lost"), point(n=1, state="active"))
        assert "restored" in [c.change_kind for c in changes]

    def test_new_and_active_are_both_live_so_no_event(self) -> None:
        # 'new' is the provider's discovery marker, not a transition of ours.
        assert diff_pair(point(n=0, state="new"), point(n=1, state="active")) == []


class TestFieldFlips:
    def test_dofollow_lost_alerts_dofollow_gained_does_not(self) -> None:
        lost = diff_pair(point(n=0, dofollow=True), point(n=1, dofollow=False))[0]
        gained = diff_pair(point(n=0, dofollow=False), point(n=1, dofollow=True))[0]
        assert lost.change_kind == "dofollow_lost" and lost.is_alertable
        assert gained.change_kind == "dofollow_gained" and not gained.is_alertable

    def test_unknown_follow_state_never_manufactures_a_flip(self) -> None:
        assert diff_pair(point(n=0, dofollow=None), point(n=1, dofollow=True)) == []
        assert diff_pair(point(n=0, dofollow=True), point(n=1, dofollow=None)) == []

    def test_anchor_change_is_detected_and_carries_both_sides(self) -> None:
        change = diff_pair(point(n=0, anchor="best widgets"), point(n=1, anchor="click here"))[0]
        assert change.change_kind == "anchor_changed"
        assert change.previous_value["anchor_text"] == "best widgets"
        assert change.current_value["anchor_text"] == "click here"

    @pytest.mark.parametrize(
        ("before", "after"),
        [("best widgets", "  best   widgets  "), ("best widgets", "best widgets\n")],
    )
    def test_whitespace_noise_is_not_an_anchor_change(self, before: str, after: str) -> None:
        # Normalization happens where rows are read, so this goes through the
        # real path rather than a hand-built point.
        points = points_for_link(
            [row(run="snap-1", n=0, anchor=before), row(run="snap-2", n=1, anchor=after)]
        )
        assert diff_chain(points, first_is_baseline=True) == []

    def test_anchor_appearing_or_disappearing_counts(self) -> None:
        assert diff_pair(point(n=0, anchor=None), point(n=1, anchor="widgets"))
        assert diff_pair(point(n=0, anchor="widgets"), point(n=1, anchor=None))

    def test_casing_is_a_real_anchor_change(self) -> None:
        assert diff_pair(point(n=0, anchor="Widgets"), point(n=1, anchor="widgets"))

    def test_target_change_is_never_produced_from_provider_diffs(self) -> None:
        # A different target is a different seo.backlink identity, so this pair
        # cannot occur in real data; the differ must not invent the event.
        changes = diff_pair(point(n=0), point(n=1, target="https://mysite.com/other"))
        assert [c.change_kind for c in changes] == []

    def test_several_independent_flips_all_report(self) -> None:
        changes = diff_pair(
            point(n=0, dofollow=True, anchor="widgets"),
            point(n=1, dofollow=False, anchor="click here"),
        )
        assert sorted(c.change_kind for c in changes) == ["anchor_changed", "dofollow_lost"]


class TestChains:
    def test_first_ever_observation_is_an_appearance(self) -> None:
        changes = diff_chain([point(n=0)], first_is_baseline=False)
        assert [c.change_kind for c in changes] == ["appeared"]
        assert changes[0].previous_observation_id is None

    def test_a_baseline_is_a_comparison_point_not_an_event(self) -> None:
        changes = diff_chain([point(n=0), point(n=1)], first_is_baseline=True)
        assert changes == []

    def test_a_link_first_seen_as_lost_is_not_an_appearance(self) -> None:
        assert diff_chain([point(n=0, state="lost")], first_is_baseline=False) == []

    def test_every_step_of_a_multi_run_chain_reports(self) -> None:
        changes = diff_chain(
            [
                point(n=0, dofollow=True),
                point(n=1, dofollow=False),
                point(n=2, dofollow=False, state="lost"),
            ],
            first_is_baseline=True,
        )
        assert [c.change_kind for c in changes] == ["dofollow_lost", "lost"]

    def test_appearance_of_a_dofollow_link_does_not_interrupt_anyone(self) -> None:
        appeared = diff_chain([point(n=0, dofollow=True)], first_is_baseline=False)[0]
        assert appeared.severity < ALERT_SEVERITY_FLOOR

    def test_empty_chain_is_empty(self) -> None:
        assert diff_chain([], first_is_baseline=False) == []


class TestDedupe:
    def test_the_same_transition_always_produces_the_same_key(self) -> None:
        a = diff_pair(point(n=0), point(n=1, dofollow=False))[0]
        b = diff_pair(point(n=0), point(n=1, dofollow=False))[0]
        assert a.dedupe_key == b.dedupe_key

    def test_different_kinds_on_the_same_pair_do_not_collide(self) -> None:
        changes = diff_pair(
            point(n=0, dofollow=True, anchor="widgets"),
            point(n=1, dofollow=False, anchor="click here"),
        )
        assert len({c.dedupe_key for c in changes}) == len(changes)

    def test_a_later_observation_of_the_same_kind_is_a_new_event(self) -> None:
        first = diff_pair(point(n=0, dofollow=True), point(n=1, dofollow=False))[0]
        second = diff_pair(point(n=2, dofollow=True), point(n=3, dofollow=False))[0]
        assert first.dedupe_key != second.dedupe_key


class TestOneRunIsNotAChange:
    """The live bug this class exists to prevent (found 2026-08-15).

    `dannegroni.com/resources/tag/millennials/page/2/` links to one target twice,
    as "business coach" and as "Titanium Success", in the SAME snapshot. Read as
    a chain, those two rows manufacture an "anchor rewritten" event out of two
    links that coexist and never changed.
    """

    def test_two_links_on_one_page_in_one_run_collapse_to_one_point(self) -> None:
        points = points_for_link(
            [
                row(run="snap-1", anchor="business coach"),
                row(run="snap-1", anchor="Titanium Success"),
            ]
        )
        assert len(points) == 1
        assert points[0].anchor_texts == frozenset({"business coach", "Titanium Success"})
        assert points[0].instance_count == 2

    def test_two_links_in_one_run_produce_no_change_at_all(self) -> None:
        points = points_for_link(
            [
                row(run="snap-1", anchor="business coach"),
                row(run="snap-1", anchor="Titanium Success"),
            ]
        )
        assert diff_chain(points, first_is_baseline=True) == []

    def test_reporting_order_flipping_between_runs_is_not_a_rewrite(self) -> None:
        # The exact live shape: same two anchors, opposite order, two runs.
        points = points_for_link(
            [
                row(run="snap-1", n=0, anchor="business coach"),
                row(run="snap-1", n=0, anchor="Titanium Success"),
                row(run="snap-2", n=1, anchor="Titanium Success"),
                row(run="snap-2", n=1, anchor="business coach"),
            ]
        )
        assert len(points) == 2
        assert diff_chain(points, first_is_baseline=True) == []

    def test_one_of_two_anchors_actually_changing_IS_reported(self) -> None:
        points = points_for_link(
            [
                row(run="snap-1", n=0, anchor="business coach"),
                row(run="snap-1", n=0, anchor="Titanium Success"),
                row(run="snap-2", n=1, anchor="click here"),
                row(run="snap-2", n=1, anchor="Titanium Success"),
            ]
        )
        changes = diff_chain(points, first_is_baseline=True)
        assert [c.change_kind for c in changes] == ["anchor_changed"]
        assert changes[0].previous_value["anchor_texts"] == ["Titanium Success", "business coach"]
        assert changes[0].current_value["anchor_texts"] == ["Titanium Success", "click here"]

    def test_one_dofollow_instance_makes_the_link_dofollow(self) -> None:
        collapsed = collapse_run(
            [
                row(run="snap-1", anchor="a", dofollow=False),
                row(run="snap-1", anchor="b", dofollow=True),
            ]
        )
        assert collapsed is not None
        assert collapsed.is_dofollow is True

    def test_one_live_instance_means_the_link_is_still_there(self) -> None:
        collapsed = collapse_run(
            [
                row(run="snap-1", anchor="a", state="lost"),
                row(run="snap-1", anchor="b", state="active"),
            ]
        )
        assert collapsed is not None
        assert collapsed.is_live is True

    def test_all_instances_lost_means_lost(self) -> None:
        collapsed = collapse_run(
            [
                row(run="snap-1", anchor="a", state="lost"),
                row(run="snap-1", anchor="b", state="lost"),
            ]
        )
        assert collapsed is not None
        assert collapsed.is_live is False

    def test_runs_are_ordered_oldest_first_regardless_of_row_order(self) -> None:
        points = points_for_link(
            [row(run="snap-2", n=5, anchor="later"), row(run="snap-1", n=1, anchor="earlier")]
        )
        assert [p.anchor_text for p in points] == ["earlier", "later"]

    def test_a_page_dropping_to_a_single_link_is_a_real_anchor_change(self) -> None:
        points = points_for_link(
            [
                row(run="snap-1", n=0, anchor="business coach"),
                row(run="snap-1", n=0, anchor="Titanium Success"),
                row(run="snap-2", n=1, anchor="Titanium Success"),
            ]
        )
        changes = diff_chain(points, first_is_baseline=True)
        assert [c.change_kind for c in changes] == ["anchor_changed"]
        assert changes[0].current_value["instance_count"] == 1

    def test_rows_with_no_link_identity_are_dropped_not_guessed_at(self) -> None:
        broken = row(run="snap-1", anchor="x")
        broken["backlink_id"] = None
        assert points_for_link([broken]) == []
