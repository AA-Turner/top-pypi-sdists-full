"""Which version a project is heading toward, and which it last shipped.

Lives in services rather than beside the dashboard that renders it: the GitHub
sync needs the same rules to decide whether to open the next planned release, and
a service importing from a router package points the dependency the wrong way.

Three ideas do the work here:

* **The high-water mark.** Board sync *used to* create a PLANNED release row every
  time a synced ticket carried a version-shaped label, and nothing ever closed
  them; projects accumulated dozens, often on versioning lines they had long
  left. That writer is gone, but the rows it left behind are not, and neither is
  the rule: anything at or below the highest *released* version is history
  someone forgot to close, not a plan, so it can never be "next".
* **Semver, numerically.** ``v1.10.0`` follows ``v1.9.0``; a string compare says
  the opposite, which is exactly the bug this ordering exists to avoid.
* **Exactly two slots, always full.** A project keeps two forward releases and
  no more -- IN_PROGRESS, the version being cut, and PLANNED, the version being
  filled, conventionally the next two minor versions. Shipping rotates them;
  anything open beyond them is archived. See ``ensure_pipeline``.
"""

import re
from typing import List, Optional, Tuple

from src.domain.release import Release, ReleaseStatus

# IN_PROGRESS before PLANNED: a release actively being cut is more "next" than one
# merely planned, whatever the version numbers say.
_UPCOMING_STATUS_ORDER = {
    ReleaseStatus.IN_PROGRESS: 0,
    ReleaseStatus.PLANNED: 1,
}

#: The statuses that make a release **outstanding** -- open, and therefore
#: something a ticket may still be planned into. Derived from the same mapping
#: ``next_release`` orders by, so a new ``ReleaseStatus`` member cannot silently
#: change one and not the other: a member that is pickable but never "current",
#: or current but not offered, would be a release the picker and the ``current``
#: sentinel disagree about.
OUTSTANDING_STATUSES: Tuple[ReleaseStatus, ...] = tuple(_UPCOMING_STATUS_ORDER)

_SEMVER = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)")

#: The parts of a version the pipeline can be bumped by.
BUMP_PARTS = ("major", "minor", "patch")

#: Where a project with **no releases at all** starts. Deliberately the same
#: value as ``InnoDayVersionStore.BOOTSTRAP_VERSION``: that store has always
#: bootstrapped to v0.1.0 without asking anyone, so adopting it here changes
#: nothing about what blastoff would cut -- it only makes the decision visible
#: on the page instead of implicit in a release command.
#:
#: A project that has shipped only *non-semver* tags is a different case and gets
#: nothing. It has plainly released things, so bootstrapping it to v0.1.0 would
#: be putting it on a versioning line nobody chose.
BOOTSTRAP_VERSION = "v0.1.0"

#: How many releases a project may have open at once. Exactly two: the one being
#: cut and the one being filled. This is a **cap as well as a floor** -- a project
#: that accumulates open versions is a project nobody can read a plan off, which
#: is what board sync's old row-per-label behaviour produced. Anything open beyond
#: these two is ARCHIVED rather than deleted, so a version someone opened
#: deliberately is recoverable rather than gone.
SLOT_COUNT = 2


def is_semver(version: str) -> bool:
    """Whether a version string can be compared numerically at all.

    Repos carry tags that are not versions -- BPAI has a literal `rancher-FINAL`.
    They must be excluded from any *maximum*, not merely sorted late: giving them a
    sentinel that sorts high made `rancher-FINAL` the high-water mark, so every
    real version counted as "already shipped" and nothing was ever upcoming.
    """
    return bool(_SEMVER.match(version.strip()))


def semver_key(version: str) -> Tuple[int, int, int, str]:
    """Sort key for a version string, numeric where it parses as semver.

    ``"v1.10.0"`` must sort after ``"v1.9.0"`` -- a plain string compare puts it
    before. Anything unparseable sorts last among its status group and falls back
    to a string compare, so a non-semver tag never crashes the page.
    """
    match = _SEMVER.match(version.strip())
    if not match:
        return (1, 0, 0, version)
    major, minor, patch = (int(part) for part in match.groups())
    return (0, major, minor, patch)  # type: ignore[return-value]


def next_release(releases: List[Release]) -> Optional[Release]:
    """The release a project is heading toward, or ``None``.

    Ordered by status-then-version because there is no date to order by (see the
    module docstring), but **only across versions ahead of what has shipped**.

    That qualifier is load-bearing. A project accumulates PLANNED rows from board
    sync every time a ticket carries a version-shaped label, and those rows are
    never cleaned up -- BPAI has forty-odd, most of them `v0.1.x-beta` from a repo
    on an entirely different versioning line. Taking the lowest upcoming version
    outright picked `v0.1.1-beta` as the next launch for a project that has already
    shipped v1.9.0. A version below the high-water mark is history someone forgot
    to close, not a plan.
    """
    # Only semver-shaped releases define the high-water mark: a tag like
    # `rancher-FINAL` is not a version and cannot be "higher" than one.
    shipped_keys = [
        semver_key(r.version)
        for r in releases
        if r.status == ReleaseStatus.RELEASED and is_semver(r.version)
    ]
    highest_shipped = max(shipped_keys) if shipped_keys else None

    upcoming = [
        r
        for r in releases
        if r.status in _UPCOMING_STATUS_ORDER
        and is_semver(r.version)
        and (highest_shipped is None or semver_key(r.version) > highest_shipped)
    ]
    if not upcoming:
        return None
    return min(
        upcoming,
        key=lambda r: (_UPCOMING_STATUS_ORDER[r.status], semver_key(r.version)),
    )


def outstanding_releases(releases: List[Release]) -> List[Release]:
    """The project's open releases, best-first.

    IN_PROGRESS before PLANNED -- the version being cut is the more likely answer
    than the one being filled -- then semver-ascending within each.

    Unlike :func:`next_release` this **keeps non-semver rows**. That function needs
    a version it can compare against a high-water mark, so an uncomparable one has
    to be dropped; a picker has the opposite problem. `February 2025` is a real row
    that a real ticket may already point at, and a list that hides it makes such a
    ticket unassignable and unfixable. ``semver_key`` already sorts them last, so
    they never displace a real version.

    No high-water-mark filter either, for the same reason: a version below what has
    shipped is a row someone forgot to close, but it is still a row, and refusing
    to name it does not close it. ``reconcile_statuses`` is what fixes that.
    """
    return sorted(
        (release for release in releases if release.status in _UPCOMING_STATUS_ORDER),
        key=lambda release: (
            _UPCOMING_STATUS_ORDER[release.status],
            semver_key(release.version),
        ),
    )


def suggest_next_version(releases: List[Release]) -> Optional[str]:
    """The version a project would ship next, from what it has already shipped.

    Only offered when nothing is planned or in progress -- a project with a real
    upcoming release does not need a guess, and showing one beside it would invite
    creating a duplicate.

    A minor bump of the highest *released* semver, keeping the observed `v` prefix.
    Minor rather than patch because that is what these projects cut: BPAI went
    v1.5.0 -> v1.6.0 -> v1.7.0. Returns None when nothing semver-shaped has ever
    shipped, since inventing a first version for a project is a decision, not a
    default.

    "The highest released semver" is :func:`latest_release`'s entire question, so
    this asks it rather than re-deriving it. The RELEASED + ``is_semver`` filter,
    the ``semver_key`` ordering and the empty case were open-coded here
    identically -- one rule in two places, and so one rule that could be changed
    in only one of them.
    """
    newest = latest_release(releases)
    if newest is None:
        return None

    match = _SEMVER.match(newest.version.strip())
    if not match:
        return None
    major, minor, _patch = (int(part) for part in match.groups())
    prefix = "v" if newest.version.strip().startswith("v") else ""
    return f"{prefix}{major}.{minor + 1}.0"


def latest_release(releases: List[Release]) -> Optional[Release]:
    """The newest version this project has actually shipped, or ``None``.

    Ordered by semver rather than by ``released_at``: the dates come from GitHub
    publication timestamps and several repos publish the same cross-repo version
    minutes apart, so the highest version is the more stable answer than the most
    recent stamp.
    """
    shipped = [
        r
        for r in releases
        if r.status == ReleaseStatus.RELEASED and is_semver(r.version)
    ]
    if not shipped:
        return None
    return max(shipped, key=lambda r: semver_key(r.version))


def reconcile_statuses(releases: List[Release]) -> int:
    """Enforce the shape a project's releases are supposed to have.

    A project has **at most one** version in progress. Everything else is either
    planned (ahead of it) or released (behind it). Nothing enforced that, and the
    records drifted badly: BPAI carried a v1.4.0 stuck IN_PROGRESS long after
    v1.8.0 shipped, which the dashboard then showed as the next launch -- a
    version four minor releases behind reality.

    Two rules, applied in order:

    1. Anything upcoming at or below the highest released version has shipped.
       It is marked RELEASED, because the alternative is a "plan" to do something
       already done.
    2. Of what genuinely remains ahead, the *lowest* version is the one in
       progress -- you ship in order. Any other IN_PROGRESS is demoted to PLANNED.

    Non-semver tags are left alone entirely: `rancher-FINAL` is not a version, has
    no position in the order, and guessing at its status would be inventing.

    Returns the number of rows changed.
    """
    shipped_keys = [
        semver_key(r.version)
        for r in releases
        if r.status == ReleaseStatus.RELEASED and is_semver(r.version)
    ]
    high_water = max(shipped_keys) if shipped_keys else None

    changed = 0
    ahead: List[Release] = []
    for release in releases:
        if release.status not in _UPCOMING_STATUS_ORDER or not is_semver(
            release.version
        ):
            continue
        if high_water is not None and semver_key(release.version) <= high_water:
            release.status = ReleaseStatus.RELEASED
            changed += 1
            continue
        ahead.append(release)

    if not ahead:
        return changed

    ahead.sort(key=lambda r: semver_key(r.version))
    for position, release in enumerate(ahead):
        wanted = ReleaseStatus.IN_PROGRESS if position == 0 else ReleaseStatus.PLANNED
        if release.status != wanted:
            release.status = wanted
            changed += 1
    return changed


def bump(version: str, part: str = "minor") -> Optional[str]:
    """The version after ``version``, bumping one part and zeroing the rest.

    Distinct from ``suggest_next_version``, which answers a narrower question --
    "given what this project has *shipped*, what should it ship next" -- and is
    anchored to the highest RELEASED version. The pipeline needs neither of those
    properties: slot 2 is a bump of slot 1, which by definition has not shipped,
    and correcting a version needs major and patch as well as minor.

    ``None`` for anything not semver-shaped. `rancher-FINAL` has no successor,
    and inventing one is how a project ends up on a versioning line nobody chose.
    """
    if part not in BUMP_PARTS:
        raise ValueError(f"unknown version part {part!r}; expected one of {BUMP_PARTS}")

    text = version.strip()
    match = _SEMVER.match(text)
    if not match:
        return None

    major, minor, patch = (int(group) for group in match.groups())
    if part == "major":
        major, minor, patch = major + 1, 0, 0
    elif part == "minor":
        minor, patch = minor + 1, 0
    else:
        patch += 1

    # Keep the prefix the project actually uses. Tags here are overwhelmingly
    # `v`-prefixed, but a project that writes `1.4.0` must not silently acquire
    # a `v` -- the tag is matched against GitHub by exact string.
    prefix = "v" if text.startswith("v") else ""
    return f"{prefix}{major}.{minor}.{patch}"


#: The notional version a project with nothing released sits at, so one piece of
#: bump arithmetic serves a fresh project and an established one alike.
#: ``bump(_ZERO, "minor")`` is :data:`BOOTSTRAP_VERSION` -- the version
#: ``ensure_pipeline`` actually opens slot 1 with. A test pins that, because the
#: two drifting apart would mean the page offering a first version the pipeline
#: would not then create.
_ZERO = "v0.0.0"


def release_being_cut(releases: List[Release]) -> Optional[Release]:
    """The release actually in flight, or ``None``.

    ``next_release`` answers "what ships next", which includes a merely PLANNED
    version when nothing has been picked up yet. Two callers needed the narrower
    question -- *is this the release being cut right now* -- and each open-coded
    the same `next_release(...) is not None and .status == IN_PROGRESS` pair. The
    distinction matters: the rules that fire on the in-flight release must not
    fire on one still being planned.
    """
    upcoming = next_release(releases)
    if upcoming is None or upcoming.status != ReleaseStatus.IN_PROGRESS:
        return None
    return upcoming


def slot_two(releases: List[Release], slot_one: Optional[Release]) -> Optional[Release]:
    """The lowest PLANNED release **above** slot 1, or ``None``.

    One sentence, one implementation. It had two, and they disagreed: the Releases
    tab required the version to be above slot 1, and ``release_pipeline.retarget``
    did not -- despite a comment directly above it claiming exactly that. So a
    PLANNED row *below* the version being cut was invisible on the page and yet was
    what the bump control moved: `_rename` rewrote its version and every ticket
    pointing at it. The page showed one row and the button changed another (#577).

    Reachable without anything unusual happening. ``POST /releases`` defaults to
    PLANNED and does not reconcile, and ``innoday releases create`` is a live
    command the CLI recommends -- so `innoday releases create v0.5.0` on a project
    cutting v1.9.0 is enough to arm it.

    Pure and session-free, like the rest of this module: ``release_pipeline`` is
    the half that writes, and a selection rule that needed a session could not be
    shared with the page that only reads.

    ``slot_one`` is ``Optional`` because a project can be mid-rotation with nothing
    in progress. With no slot 1 there is no "above" to test, so every PLANNED
    semver qualifies and the lowest wins -- which is what the page already did.
    """
    candidates = [
        release
        for release in releases
        if release.status == ReleaseStatus.PLANNED
        and is_semver(release.version)
        and (slot_one is None or release.id != slot_one.id)
        and (
            slot_one is None
            or not is_semver(slot_one.version)
            or semver_key(release.version) > semver_key(slot_one.version)
        )
    ]
    if not candidates:
        return None
    # By semver, not by string: sorting these as text puts v1.10.0 before v1.9.0,
    # which is the exact bug `semver_key` exists to avoid.
    return min(candidates, key=lambda release: semver_key(release.version))


def pipeline_options(releases: List[Release]) -> List[Tuple[str, str, str]]:
    """``(part, slot one, slot two)`` for each kind of bump this project could take.

    Always recomputed from the highest **released** version, never from whatever
    the slots currently hold. That is what makes a control built on this a
    *toggle* rather than a ratchet: choosing major and then minor lands exactly
    where it started, however many times it is flipped, and nothing has to store
    a previous value for "revert" to work.

    A project with **no releases at all** is offered v0.1.0 (minor) and v1.0.0
    (major) off the notional zero -- the same guidance ``ensure_pipeline``
    bootstraps with.

    Empty in every other case that has no semver high-water mark, and the
    distinction matters: ``latest_release`` answers ``None`` both for a project
    with nothing and for one whose releases are all non-semver, and those are
    different situations. A project that has shipped ``rancher-FINAL`` has
    plainly released something, so offering it v0.1.0 would propose a first
    version ``ensure_pipeline`` then refuses to create -- guidance that lies
    about itself. Without a shipped version to anchor to there is also no stable
    base, so the options would stop being a toggle.
    """
    newest = latest_release(releases)
    if newest is None and releases:
        return []
    base = newest.version if newest else _ZERO

    options: List[Tuple[str, str, str]] = []
    for part in BUMP_PARTS:
        slot_one = bump(base, part)
        if slot_one is None:
            continue
        slot_two = bump(slot_one, "minor")
        if slot_two is None:  # pragma: no cover - a bump of a bump always parses
            continue
        options.append((part, slot_one, slot_two))
    return options


def ensure_pipeline(
    releases: List[Release], *, bootstrap: str = BOOTSTRAP_VERSION
) -> List[Tuple[str, ReleaseStatus]]:
    """Keep two forward releases open, and report which rows are missing.

    A project runs on a two-slot pipeline: **slot 1** is IN_PROGRESS, the version
    blastoff cuts next, and **slot 2** is PLANNED, the version tickets are being
    planned into. Shipping slot 1 rotates the pipeline -- slot 2 is promoted and
    a new slot 2 opens above it -- so both are always there to point at.

    **Exactly two, not at least two.** New slots are opened as the next *minor*
    version, and anything open beyond the two is archived. A release record is
    meant to be stable enough to plan against: a project carrying six open
    versions has no readable plan, and that is precisely what board sync's old
    row-per-version-label behaviour produced. Closed history below the high-water
    mark is untouched and unbounded -- past versions are a record, not a queue.

    Two slots rather than one because they answer different questions and a
    single "next release" had to be both. What is closing out and what is being
    filled are not the same version, and a planning surface with nothing to drop
    onto until someone remembers to create a release is a planning surface that
    does not work on a Monday morning.

    Statuses are reconciled first, in place, so the caller never has to decide
    whether to run both. What is *returned* is only the rows that must be created
    -- everything else in this module is a pure function over a list of releases,
    and the caller is the one that owns the session and knows the organization
    and project ids.

    **Never call this before a project's existing releases have been discovered.**
    The bootstrap branch fires only when a project has no releases at all, and
    every caller today runs *after* GitHub release discovery has created rows for
    whatever the repos already shipped -- which is the only reason bootstrapping
    is safe. Seed a fresh project at creation time instead and the two slots
    (v0.1.0, v0.2.0) sit below the high-water mark the first sync then discovers,
    so ``reconcile_statuses`` rule 1 marks both **RELEASED**: the project ends up
    claiming to have shipped two versions that never existed, with no
    ``released_at`` on either. `tests/test_release_planning.py` pins this.

    Deliberately adds nothing in two cases:

    * **Only non-semver releases.** See ``bump``. A project that has shipped
      `rancher-FINAL` and nothing else has no computable next version.
    * **A version that already exists.** An ARCHIVED row sitting on the version
      the pipeline wants is revived into the slot rather than returned for
      creation, because returning it would hand the caller a row that violates
      ``uq_release_project_version``.
    """
    reconcile_statuses(releases)

    # A version that is not a version cannot be a slot. `February 2025` has no
    # position in the order, so `next_release` can never select it and blastoff
    # can never bump from it -- it would sit open forever, doing nothing except
    # making the count of open releases untrue.
    #
    # Closing these is safe *because nothing creates them any more*. Board sync
    # was the only writer that ever did, and it no longer creates releases at all
    # (a version label lands on `ticket.release` and stops there); GitHub release
    # discovery only ever creates RELEASED rows, which is history and is left
    # alone. So an open non-semver row is residue by construction.
    #
    # ARCHIVED, not RELEASED: there is no evidence any of them shipped, and no
    # `released_at` to give them. Marking them released would invent history --
    # see the ordering warning above.
    for release in releases:
        if release.status in _UPCOMING_STATUS_ORDER and not is_semver(release.version):
            release.status = ReleaseStatus.ARCHIVED

    by_version = {release.version.strip(): release for release in releases}
    newest_shipped = latest_release(releases)
    high_water = semver_key(newest_shipped.version) if newest_shipped else None

    ahead = sorted(
        (
            release
            for release in releases
            if release.status in _UPCOMING_STATUS_ORDER
            and is_semver(release.version)
            and (high_water is None or semver_key(release.version) > high_water)
        ),
        key=lambda release: semver_key(release.version),
    )
    # Exactly two stay open. `reconcile_statuses` has already made ahead[0]
    # IN_PROGRESS and the rest PLANNED, so the first two are filled and correctly
    # labelled; everything above them is closed out.
    #
    # ARCHIVED, not deleted -- a third open version is usually board-sync residue
    # but may be something a person opened on purpose, and the difference is not
    # knowable from here. Archiving keeps it readable and reversible.
    #
    # The two kept are the *existing* lowest two, not recomputed from the
    # high-water mark: a project deliberately moved onto a major line (see
    # `pipeline_options`) must stay there rather than be dragged back to the
    # minor convention on the next sync. The convention governs what gets
    # **created**, not what gets overruled.
    for extra in ahead[SLOT_COUNT:]:
        extra.status = ReleaseStatus.ARCHIVED
    ahead = ahead[:SLOT_COUNT]

    if len(ahead) >= SLOT_COUNT:
        return []

    if ahead:
        cursor: Optional[str] = ahead[-1].version
    elif newest_shipped is not None:
        cursor = newest_shipped.version
    elif not releases:
        cursor = None  # Nothing at all: bootstrap rather than bump.
    else:
        return []

    slots = (ReleaseStatus.IN_PROGRESS, ReleaseStatus.PLANNED)
    created: List[Tuple[str, ReleaseStatus]] = []
    for position in range(len(ahead), SLOT_COUNT):
        candidate = bootstrap.strip() if cursor is None else bump(cursor, "minor")
        if candidate is None:
            break
        cursor = candidate

        existing = by_version.get(candidate)
        if existing is None:
            created.append((candidate, slots[position]))
            continue
        if existing.status != ReleaseStatus.RELEASED:
            existing.status = slots[position]

    return created
