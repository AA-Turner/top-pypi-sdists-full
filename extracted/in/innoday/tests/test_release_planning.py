"""Which version a project is heading toward, and the shape its releases keep.

These rules were learned from BPAI's real data, and each test here is a thing that
actually went wrong on screen:

* a stale `v1.4.0` stuck IN_PROGRESS long after `v1.8.0` shipped, shown as the
  next launch -- a version four minor releases behind reality;
* forty-odd `v0.1.x-beta` rows from board sync, one of which then became "next"
  for a project already on v1.9.0;
* a literal `rancher-FINAL` tag that sorted above every real version and made
  everything else look already-shipped.
"""

import pytest

from src.domain.release import Release, ReleaseStatus
from src.services.release_planning import (
    _UPCOMING_STATUS_ORDER,
    BOOTSTRAP_VERSION,
    OUTSTANDING_STATUSES,
    bump,
    ensure_pipeline,
    is_semver,
    latest_release,
    next_release,
    outstanding_releases,
    pipeline_options,
    reconcile_statuses,
    release_being_cut,
    semver_key,
    suggest_next_version,
)


def _r_status(releases, version):
    return next(r.status for r in releases if r.version == version)


def _r(version: str, status: ReleaseStatus = ReleaseStatus.PLANNED) -> Release:
    return Release(
        organization_id="org", project_id="proj", version=version, status=status
    )


def test_semver_orders_numerically_not_as_strings():
    """v1.10.0 follows v1.9.0. A string compare says the opposite."""
    assert semver_key("v1.10.0") > semver_key("v1.9.0")
    assert semver_key("1.2.3") == semver_key("v1.2.3")


@pytest.mark.parametrize(
    "version,expected",
    [
        ("v1.2.3", True),
        ("1.2.3", True),
        ("v0.1.1-beta", True),
        ("rancher-FINAL", False),
        ("February 2025", False),
        ("", False),
    ],
)
def test_is_semver(version, expected):
    assert is_semver(version) is expected


def test_non_semver_tags_cannot_become_the_high_water_mark():
    """`rancher-FINAL` is a real tag in a BPAI repo. Giving unparseable versions a
    sentinel that sorted high made it the highest 'released' version, so every real
    version counted as already shipped and nothing was ever upcoming."""
    releases = [
        _r("v1.9.0", ReleaseStatus.RELEASED),
        _r("rancher-FINAL", ReleaseStatus.RELEASED),
        _r("v1.10.0", ReleaseStatus.PLANNED),
    ]
    assert latest_release(releases).version == "v1.9.0"
    assert next_release(releases).version == "v1.10.0"
    assert suggest_next_version(releases) == "v1.10.0"


def test_versions_at_or_below_what_shipped_are_never_next():
    """Board sync creates a PLANNED row per version-shaped ticket label and never
    closes them. Taking the lowest upcoming outright picked v0.1.1-beta as the next
    launch for a project already on v1.9.0."""
    releases = [
        _r("v1.9.0", ReleaseStatus.RELEASED),
        _r("v0.1.1-beta", ReleaseStatus.PLANNED),
        _r("v1.4.0", ReleaseStatus.IN_PROGRESS),
    ]
    assert next_release(releases) is None


def test_in_progress_outranks_a_lower_planned_version():
    releases = [
        _r("v1.9.0", ReleaseStatus.RELEASED),
        _r("v2.0.0", ReleaseStatus.IN_PROGRESS),
        _r("v1.10.0", ReleaseStatus.PLANNED),
    ]
    assert next_release(releases).version == "v2.0.0"


def test_suggestion_needs_something_to_have_shipped():
    """Inventing a first version for a project is a decision, not a default."""
    assert suggest_next_version([_r("v1.0.0", ReleaseStatus.PLANNED)]) is None
    assert suggest_next_version([]) is None


def test_reconcile_leaves_exactly_one_in_progress():
    """A project has at most one version in progress; the rest are planned (ahead)
    or released (behind). Nothing enforced it, and the records drifted."""
    releases = [
        _r("v1.8.0", ReleaseStatus.RELEASED),
        _r("v1.4.0", ReleaseStatus.IN_PROGRESS),  # shipped long ago
        _r("v1.10.0", ReleaseStatus.IN_PROGRESS),  # ahead, but not next
        _r("v1.9.0", ReleaseStatus.PLANNED),  # the real one in flight
        _r("rancher-FINAL", ReleaseStatus.PLANNED),
    ]
    changed = reconcile_statuses(releases)
    by_version = {r.version: r.status for r in releases}

    assert by_version["v1.4.0"] == ReleaseStatus.RELEASED, "below the high-water mark"
    assert by_version["v1.9.0"] == ReleaseStatus.IN_PROGRESS, "lowest ahead ships next"
    assert by_version["v1.10.0"] == ReleaseStatus.PLANNED
    assert by_version["v1.8.0"] == ReleaseStatus.RELEASED
    # Not a version: no position in the order, so no status to infer.
    assert by_version["rancher-FINAL"] == ReleaseStatus.PLANNED
    assert changed == 3

    in_progress = [r for r in releases if r.status == ReleaseStatus.IN_PROGRESS]
    assert len(in_progress) == 1


def test_reconcile_is_idempotent():
    releases = [
        _r("v1.8.0", ReleaseStatus.RELEASED),
        _r("v1.9.0", ReleaseStatus.PLANNED),
    ]
    reconcile_statuses(releases)
    assert reconcile_statuses(releases) == 0, "a settled project must not keep churning"


# --------------------------------------------------------------------------- #
# The two-slot pipeline
#
# A project keeps slot 1 (IN_PROGRESS, what blastoff cuts) and slot 2 (PLANNED,
# what tickets are planned into). These tests are the invariant: after
# `ensure_pipeline` plus the rows it asks for, both slots exist exactly once.
# --------------------------------------------------------------------------- #


@pytest.mark.parametrize(
    "version,part,expected",
    [
        ("v1.9.0", "minor", "v1.10.0"),
        ("v1.9.0", "major", "v2.0.0"),
        ("v1.9.0", "patch", "v1.9.1"),
        # A major bump zeroes what is below it; a minor bump zeroes the patch.
        ("v1.9.4", "major", "v2.0.0"),
        ("v1.9.4", "minor", "v1.10.0"),
        # The project's own prefix survives. The tag is matched against GitHub by
        # exact string, so acquiring a `v` would be a different tag.
        ("1.9.0", "minor", "1.10.0"),
        ("rancher-FINAL", "minor", None),
    ],
)
def test_bump(version, part, expected):
    assert bump(version, part) == expected


def test_bump_rejects_a_part_it_does_not_know():
    """Silently treating an unknown part as a minor bump would ship the wrong
    version off a typo'd query parameter."""
    with pytest.raises(ValueError):
        bump("v1.9.0", "mnior")


def _pipeline(releases):
    """Apply `ensure_pipeline` and return the resulting (version, status) pairs.

    The function reports rows to create rather than creating them, so a test that
    only read its return value would miss everything it did in place.
    """
    for version, status in ensure_pipeline(releases):
        releases.append(_r(version, status))
    # By semver, not by string -- sorting these as text puts v1.10.0 before
    # v1.9.0, which is the exact bug `semver_key` exists to avoid.
    upcoming = [r for r in releases if r.status in _UPCOMING_STATUS_ORDER]
    upcoming.sort(key=lambda r: semver_key(r.version))
    return [(r.version, r.status) for r in upcoming]


def test_a_project_with_nothing_at_all_bootstraps_both_slots():
    """v0.1.0 is what InnoDayVersionStore has always cut for such a project. This
    does not change that -- it makes it visible before the command runs."""
    releases = []
    assert _pipeline(releases) == [
        ("v0.1.0", ReleaseStatus.IN_PROGRESS),
        ("v0.2.0", ReleaseStatus.PLANNED),
    ]


def test_a_project_that_has_only_shipped_opens_both_slots_above_it():
    releases = [_r("v1.8.0", ReleaseStatus.RELEASED)]
    assert _pipeline(releases) == [
        ("v1.9.0", ReleaseStatus.IN_PROGRESS),
        ("v1.10.0", ReleaseStatus.PLANNED),
    ]


def test_one_upcoming_release_gets_a_second_slot_above_it():
    releases = [_r("v1.8.0", ReleaseStatus.RELEASED), _r("v1.9.0")]
    assert _pipeline(releases) == [
        ("v1.9.0", ReleaseStatus.IN_PROGRESS),
        ("v1.10.0", ReleaseStatus.PLANNED),
    ]


def test_a_full_pipeline_is_left_alone():
    releases = [
        _r("v1.8.0", ReleaseStatus.RELEASED),
        _r("v1.9.0", ReleaseStatus.IN_PROGRESS),
        _r("v1.10.0", ReleaseStatus.PLANNED),
    ]
    assert ensure_pipeline(releases) == []


def test_ensure_pipeline_is_idempotent():
    """It runs on every sync and after every release. Running it twice must not
    open a third slot, which is how a pipeline drifts deeper each sync."""
    releases = [_r("v1.8.0", ReleaseStatus.RELEASED)]
    _pipeline(releases)
    assert ensure_pipeline(releases) == []
    assert _pipeline(releases) == [
        ("v1.9.0", ReleaseStatus.IN_PROGRESS),
        ("v1.10.0", ReleaseStatus.PLANNED),
    ]


def test_only_two_versions_stay_open_and_the_rest_are_archived():
    """The invariant is a cap as well as a floor.

    A project carrying six open versions has no readable plan, which is exactly
    what board sync's old row-per-label behaviour produced. Archived rather than
    deleted: a third open version is usually residue but may be deliberate, and
    that is not knowable from here.
    """
    releases = [
        _r("v1.8.0", ReleaseStatus.RELEASED),
        _r("v1.9.0"),
        _r("v1.10.0"),
        _r("v2.0.0"),
        _r("v3.0.0"),
    ]
    assert ensure_pipeline(releases) == []

    assert _r_status(releases, "v1.9.0") == ReleaseStatus.IN_PROGRESS
    assert _r_status(releases, "v1.10.0") == ReleaseStatus.PLANNED
    assert _r_status(releases, "v2.0.0") == ReleaseStatus.ARCHIVED
    assert _r_status(releases, "v3.0.0") == ReleaseStatus.ARCHIVED
    # Nothing deleted, and shipped history untouched.
    assert len(releases) == 5
    assert _r_status(releases, "v1.8.0") == ReleaseStatus.RELEASED


def test_the_two_kept_are_the_existing_ones_not_the_minor_convention():
    """The convention governs what gets *created*, not what gets overruled.

    A project deliberately moved onto a major line must stay there rather than be
    dragged back to minor on the next sync.
    """
    releases = [
        _r("v1.8.0", ReleaseStatus.RELEASED),
        _r("v2.0.0", ReleaseStatus.IN_PROGRESS),
        _r("v2.1.0"),
    ]
    assert ensure_pipeline(releases) == []
    assert _r_status(releases, "v2.0.0") == ReleaseStatus.IN_PROGRESS
    assert _r_status(releases, "v2.1.0") == ReleaseStatus.PLANNED


def test_closed_history_is_unbounded():
    """ "Only two open" caps the *queue*, not the record. Past versions accumulate
    freely -- you can create previous versions that are already closed."""
    releases = [_r(f"v1.{n}.0", ReleaseStatus.RELEASED) for n in range(9)]
    before = len(releases)
    for version, status in ensure_pipeline(releases):
        releases.append(_r(version, status))

    shipped = [r for r in releases if r.status == ReleaseStatus.RELEASED]
    assert len(shipped) == before, "no shipped release was archived or dropped"
    assert _pipeline(releases) == [
        ("v1.9.0", ReleaseStatus.IN_PROGRESS),
        ("v1.10.0", ReleaseStatus.PLANNED),
    ]


def test_open_non_semver_rows_are_closed():
    """BPAI's real data: `February 2025`, `March 2025`, `April 2025` left open by
    board sync's old row-per-label behaviour.

    A version that is not a version cannot be a slot -- `next_release` can never
    select it and blastoff can never bump from it -- so it would sit open forever
    making the count of open releases untrue.

    ARCHIVED rather than RELEASED: nothing says they shipped and there is no
    `released_at` to give them, so calling them released would invent history.
    """
    dated = [_r("February 2025"), _r("March 2025"), _r("April 2025")]
    releases = [_r("v1.9.0", ReleaseStatus.RELEASED), _r("v1.10.0"), *dated]
    for version, status in ensure_pipeline(releases):
        releases.append(_r(version, status))

    assert [r.status for r in dated] == [ReleaseStatus.ARCHIVED] * 3
    # Exactly two open, and they are the next two minor versions.
    assert _pipeline(releases) == [
        ("v1.10.0", ReleaseStatus.IN_PROGRESS),
        ("v1.11.0", ReleaseStatus.PLANNED),
    ]


def test_a_non_semver_release_that_already_shipped_is_history_and_stays():
    """ "Import the history, close it if it is in the past." A GitHub tag like
    `rancher-FINAL` is a real thing that shipped -- discovery records it RELEASED
    with its publication date, and nothing here touches it."""
    shipped = _r("rancher-FINAL", ReleaseStatus.RELEASED)
    releases = [_r("v1.9.0", ReleaseStatus.RELEASED), shipped]
    ensure_pipeline(releases)
    assert shipped.status == ReleaseStatus.RELEASED


def test_a_project_with_only_non_semver_releases_gets_nothing():
    """It has plainly shipped something, so bootstrapping it to v0.1.0 would put
    it on a versioning line nobody chose. `rancher-FINAL` has no successor."""
    releases = [_r("rancher-FINAL", ReleaseStatus.RELEASED)]
    assert ensure_pipeline(releases) == []
    assert len(releases) == 1


def test_an_archived_row_on_the_wanted_version_is_revived_not_duplicated():
    """Returning it for creation would hand the caller a row that violates
    uq_release_project_version -- an insert that fails at commit."""
    archived = _r("v1.9.0", ReleaseStatus.ARCHIVED)
    releases = [_r("v1.8.0", ReleaseStatus.RELEASED), archived]

    created = ensure_pipeline(releases)

    assert ("v1.9.0", ReleaseStatus.IN_PROGRESS) not in created
    assert archived.status == ReleaseStatus.IN_PROGRESS
    assert created == [("v1.10.0", ReleaseStatus.PLANNED)]


def test_a_stale_in_progress_below_the_high_water_mark_does_not_count_as_a_slot():
    """BPAI's original bug: v1.4.0 stuck IN_PROGRESS after v1.8.0 shipped. It is
    history someone forgot to close, so the pipeline must still open two slots."""
    stale = _r("v1.4.0", ReleaseStatus.IN_PROGRESS)
    releases = [_r("v1.8.0", ReleaseStatus.RELEASED), stale]

    assert _pipeline(releases) == [
        ("v1.9.0", ReleaseStatus.IN_PROGRESS),
        ("v1.10.0", ReleaseStatus.PLANNED),
    ]
    assert stale.status == ReleaseStatus.RELEASED


def test_the_bootstrap_version_is_what_the_options_offer():
    """The page offers a first version and the pipeline creates one. If those two
    drifted, the control would propose something `ensure_pipeline` then would not
    make -- a guidance that lies about itself."""
    minor = next(o for o in pipeline_options([]) if o[0] == "minor")
    assert minor[1] == BOOTSTRAP_VERSION


def test_the_options_are_recomputed_from_what_shipped_not_from_the_slots():
    """This is what makes the control a toggle: a project already moved onto the
    major line still sees minor as an option leading back to where it began."""
    on_major = [
        _r("v1.8.0", ReleaseStatus.RELEASED),
        _r("v2.0.0", ReleaseStatus.IN_PROGRESS),
        _r("v2.1.0"),
    ]
    assert {(part, one) for part, one, _ in pipeline_options(on_major)} == {
        ("major", "v2.0.0"),
        ("minor", "v1.9.0"),
        ("patch", "v1.8.1"),
    }


def test_a_project_with_no_semver_high_water_mark_is_offered_nothing():
    """`latest_release` answers None both for a project with nothing and for one
    whose releases are all non-semver, and those are different situations. Only
    the first bootstraps -- offering v0.1.0 to a project that has plainly shipped
    `rancher-FINAL` would propose a version `ensure_pipeline` refuses to create.
    """
    assert pipeline_options([_r("rancher-FINAL", ReleaseStatus.RELEASED)]) == []
    # Nothing shipped, but something planned: still no stable base to toggle
    # against, so no options rather than options anchored on a moving value.
    assert pipeline_options([_r("v1.9.0", ReleaseStatus.IN_PROGRESS)]) == []
    assert pipeline_options([]) != []


def test_every_offered_option_is_one_ensure_pipeline_would_also_create():
    """The control and the invariant must agree about a project's first version,
    or the guidance proposes something the pipeline then declines to make."""
    for releases in ([], [_r("rancher-FINAL", ReleaseStatus.RELEASED)]):
        offered = pipeline_options(list(releases))
        created = [version for version, _status in ensure_pipeline(list(releases))]
        if offered:
            assert created and created[0] in {one for _p, one, _t in offered}
        else:
            assert not created


def test_bootstrapping_before_release_discovery_would_fabricate_history():
    """The ordering between discovery and the invariant is load-bearing.

    Seeding a fresh project's two slots at *creation* time is an obvious-looking
    improvement, and it silently invents releases. v0.1.0 and v0.2.0 land below
    the high-water mark the first repository sync then discovers, so
    `reconcile_statuses` rule 1 marks both RELEASED -- and the project claims to
    have shipped two versions that never existed, with no `released_at` on
    either.

    Every caller today runs `ensure_pipeline` *after* discovery, which is the only
    reason the bootstrap branch is safe. This test exists so that the next person
    who reaches for a seed-on-create sees why it is not one.
    """
    seeded = []
    for version, status in ensure_pipeline(seeded):
        seeded.append(_r(version, status))
    assert [r.version for r in seeded] == ["v0.1.0", "v0.2.0"]

    # The project's first repository sync finds real GitHub history.
    seeded.append(_r("v1.8.0", ReleaseStatus.RELEASED))
    reconcile_statuses(seeded)

    fabricated = [
        r.version
        for r in seeded
        if r.status == ReleaseStatus.RELEASED and r.version != "v1.8.0"
    ]
    assert fabricated == ["v0.1.0", "v0.2.0"], (
        "if this ever comes back empty the hazard is gone and this test can go; "
        "while it holds, nothing may call ensure_pipeline before discovery"
    )


def test_discovery_first_then_the_invariant_invents_nothing():
    """The order every caller actually uses: real releases exist by the time the
    pipeline is opened, so it bumps from them instead of bootstrapping."""
    discovered = [_r("v1.8.0", ReleaseStatus.RELEASED)]
    for version, status in ensure_pipeline(discovered):
        discovered.append(_r(version, status))

    assert {r.version for r in discovered if r.status == ReleaseStatus.RELEASED} == {
        "v1.8.0"
    }
    assert _pipeline(discovered) == [
        ("v1.9.0", ReleaseStatus.IN_PROGRESS),
        ("v1.10.0", ReleaseStatus.PLANNED),
    ]


# ---------------------------------------------------------------------------
# `outstanding_releases` -- the vocabulary a ticket's release may be set to
# ---------------------------------------------------------------------------


def test_outstanding_statuses_are_the_upcoming_ones_and_the_enum_has_not_grown():
    """One assertion, both halves, deliberately.

    A fifth `ReleaseStatus` member must fail *here* -- where someone is looking
    at what "outstanding" means -- rather than being silently excluded from every
    picker in the product. Asserting only the set would pass for a new member;
    asserting only the length would pass if the two swapped.
    """
    assert set(OUTSTANDING_STATUSES) == {
        ReleaseStatus.PLANNED,
        ReleaseStatus.IN_PROGRESS,
    }
    assert len(ReleaseStatus) == 4, (
        "ReleaseStatus gained a member -- decide explicitly whether it is "
        "outstanding before this test is updated"
    )


def test_outstanding_statuses_derive_from_the_ordering_next_release_uses():
    """The two must not be able to drift: one says what may be picked, the other
    what is picked by default, and a member in one but not the other is a release
    the picker offers and `current` can never resolve to (or vice versa)."""
    assert set(OUTSTANDING_STATUSES) == set(_UPCOMING_STATUS_ORDER)


def test_outstanding_puts_in_progress_before_planned():
    releases = [
        _r("v1.11.0", ReleaseStatus.PLANNED),
        _r("v1.10.0", ReleaseStatus.IN_PROGRESS),
    ]
    assert [r.version for r in outstanding_releases(releases)] == [
        "v1.10.0",
        "v1.11.0",
    ]


def test_outstanding_orders_numerically_within_a_status():
    """`v1.10.0` after `v1.9.0` -- the bug `semver_key` exists for, and the one
    the releases endpoint's `ORDER BY version DESC` (a string sort) still has."""
    releases = [_r("v1.10.0"), _r("v1.9.0"), _r("v1.2.0")]
    assert [r.version for r in outstanding_releases(releases)] == [
        "v1.2.0",
        "v1.9.0",
        "v1.10.0",
    ]


def test_outstanding_excludes_released_and_archived():
    releases = [
        _r("v1.0.0", ReleaseStatus.RELEASED),
        _r("v0.9.0", ReleaseStatus.ARCHIVED),
        _r("v1.1.0", ReleaseStatus.IN_PROGRESS),
    ]
    assert [r.version for r in outstanding_releases(releases)] == ["v1.1.0"]


def test_outstanding_keeps_non_semver_rows_and_sorts_them_last():
    """Unlike `next_release`, which needs a *comparable* version and so drops
    them: these are real rows an existing ticket may already point at, and a
    picker that hides them makes such a ticket unreachable. `semver_key` already
    sorts them last, so they never displace a real version."""
    releases = [_r("February 2025"), _r("v1.9.0")]
    assert [r.version for r in outstanding_releases(releases)] == [
        "v1.9.0",
        "February 2025",
    ]


def test_outstanding_is_empty_for_a_project_with_nothing_open():
    assert outstanding_releases([]) == []
    assert outstanding_releases([_r("v1.0.0", ReleaseStatus.RELEASED)]) == []


# ---------------------------------------------------------------------------
# `release_being_cut` -- narrower than `next_release` (came in with #559)
# ---------------------------------------------------------------------------


def test_release_being_cut_is_narrower_than_next_release():
    """`next_release` includes a merely PLANNED version when nothing is in flight.
    Two callers needed the narrower question and each open-coded the same pair --
    and the distinction matters, because rules that fire on the in-flight release
    must not fire on one still being planned."""
    only_planned = [_r("v1.8.0", ReleaseStatus.RELEASED), _r("v1.9.0")]
    # `reconcile_statuses` promotes the lowest ahead, so read it before that runs.
    assert next_release(only_planned).version == "v1.9.0"
    assert release_being_cut(only_planned) is None

    in_flight = [
        _r("v1.8.0", ReleaseStatus.RELEASED),
        _r("v1.9.0", ReleaseStatus.IN_PROGRESS),
    ]
    assert release_being_cut(in_flight).version == "v1.9.0"


def test_nothing_upcoming_is_not_being_cut():
    assert release_being_cut([]) is None
    assert release_being_cut([_r("v1.0.0", ReleaseStatus.RELEASED)]) is None


# --------------------------------------------------------------------------- #
# Slot 2 has one definition (#577)
# --------------------------------------------------------------------------- #


def test_slot_two_ignores_a_planned_release_below_slot_one():
    """The bug this closes: the page and the bump control disagreed.

    `retarget`'s predicate had a comment saying "above slot 1" and no such
    condition, so `min(PLANNED)` could select a version *below* the one being cut.
    The Releases tab filtered it out and showed the correct slot 2 — while the
    bump control moved the stale low row and `_rename` rewrote its version and
    every ticket pointing at it. The page showed one row and the button changed
    another.

    Reachable without anything unusual: `POST /releases` defaults to PLANNED and
    does not reconcile, and `innoday releases create` is a live command.
    """
    from src.services.release_planning import slot_two

    cutting = _r("v1.9.0", ReleaseStatus.IN_PROGRESS)
    above = _r("v1.10.0", ReleaseStatus.PLANNED)
    stale_below = _r("v0.5.0", ReleaseStatus.PLANNED)

    assert slot_two([cutting, above, stale_below], cutting) is above
    # Order of the list must not decide it.
    assert slot_two([stale_below, above, cutting], cutting) is above
    # By semver, not by string: "v1.10.0" sorts before "v1.9.0" as text.
    higher = _r("v1.11.0", ReleaseStatus.PLANNED)
    assert slot_two([cutting, higher, above], cutting) is above


def test_slot_two_edge_cases_that_the_two_implementations_handled_differently():
    """Nothing above, no slot 1 at all, and a non-semver slot 1."""
    from src.services.release_planning import slot_two

    cutting = _r("v1.9.0", ReleaseStatus.IN_PROGRESS)
    assert slot_two([cutting], cutting) is None, "nothing planned above it"
    assert slot_two([cutting, _r("v0.5.0", ReleaseStatus.PLANNED)], cutting) is None

    # Mid-rotation, nothing in progress: there is no "above" to test, so the
    # lowest planned wins -- which is what the page already did.
    low = _r("v0.5.0", ReleaseStatus.PLANNED)
    high = _r("v2.0.0", ReleaseStatus.PLANNED)
    assert slot_two([high, low], None) is low

    # A slot 1 that is not a version cannot be compared against, so it cannot
    # exclude anything -- the same rule `next_release` applies to the high-water
    # mark.
    odd = _r("nightly-FINAL", ReleaseStatus.IN_PROGRESS)
    assert slot_two([odd, low, high], odd) is low

    # RELEASED and IN_PROGRESS rows are never slot 2, whatever their version.
    shipped = _r("v3.0.0", ReleaseStatus.RELEASED)
    assert slot_two([cutting, shipped], cutting) is None


def test_the_page_and_retarget_choose_the_same_slot_two():
    """The assertion that is the whole point: one sentence, one answer.

    Stated as the two callers agreeing rather than as either one being correct,
    because the defect was never that one of them was wrong on its own.
    """
    from src.routers.webui import data as webui_data
    from src.services import release_pipeline
    from src.services.release_planning import slot_two

    # Both modules must reach the *same* function, not two copies of it.
    assert webui_data.slot_two is slot_two
    assert release_pipeline.slot_two is slot_two
