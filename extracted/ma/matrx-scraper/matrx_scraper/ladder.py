"""The capture ladder: four rungs, in order, and never a silent skip.

`escalation.py` made rung 1 → rung 2 (scraper → server browser) an automatic
policy of `orchestrator.scrape()`. It stops there, and the server browser is not
the last thing we own. Arman, 2026-09-17:

    "for the most impossible sites to scrape or use in the cloud browser, the
    user can just open the extension and the extension then handles it like a
    human and if that doesn't work, then the user drives the browser for a few
    minutes, signs in and does whatever it takes"

So the ladder is four rungs, not two:

    http  →  browser  →  own_browser  →  human_drive

Rungs 3 and 4 do not run here. They run in the person's own Chrome, through
matrx-extend, hours later — and there is no outbound channel from this server
to that extension. What THIS module owns is the POLICY: what the trail is, which
rung could plausibly come next, why, and the one sentence a non-technical person
reads about it. The durable queue that carries a capture to rung 3 lives in
aidream (`aidream/services/capture_ladder/`), because it needs the database and
the organization's knobs, and this package has neither.

Three laws, the same three `escalation.py` states, one rung further:

1. **Never skip a rung.** A capture moves from rung *n* to rung *n+1* or it
   stops. `assert_no_skipped_rung()` is the guard, and it is called on every
   trail this module builds.
2. **Announce every stop.** A failed capture ALWAYS carries either `next_rung`
   (what comes next and why) or `stopped_because` (why nothing does). Both
   empty is the silent-failure defect, and `verdict_fields()` cannot produce it.
3. **A setting controls each rung**, resolved by the caller (organizations
   decide, not this module) and passed in.

Contract: `common-docs/projects/acquisition-frontier/extension-ladder/CONTRACT.md`.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any

#: The ladder, in order. The ONLY declaration of it anywhere; every other repo
#: imports these strings rather than re-listing them.
RUNGS: tuple[str, ...] = ("http", "browser", "own_browser", "human_drive")

#: Rungs this server can run itself. The rest need a person's machine.
SERVER_RUNGS: frozenset[str] = frozenset({"http", "browser"})

#: Rungs that need the person's own Chrome (matrx-extend).
CLIENT_RUNGS: frozenset[str] = frozenset({"own_browser", "human_drive"})

#: Residential egress — the person's OWN computer used as the internet exit,
#: after the server's own two rungs were blocked. It is NOT a fifth rung of the
#: ladder: it is the same `http`/`browser` work, run again from a different
#: address, and it is optional in every sense (a host that has not wired it
#: never records one). So it is an OPTIONAL entry: it may appear in a trail, it
#: never changes which rung may follow, and a trail without it is complete.
#: Contract: `common-docs/systems/platform/residential-egress/FEATURE.md`.
RESIDENTIAL_RUNG = "residential"

#: Entries a trail may carry that the ladder order does not reason about.
#: `assert_no_skipped_rung` steps over them and `decide()` asks the last
#: ORDERED rung what comes next — so adding one can never turn an existing,
#: legal trail (`http` -> `browser` -> `own_browser`) into a skipped rung.
OPTIONAL_RUNGS: frozenset[str] = frozenset({RESIDENTIAL_RUNG})

#: Why "stopped" — the closed vocabulary for a ladder that goes no further.
STOP_RUNG_DISABLED = "rung_disabled"
STOP_NOT_ESCALATABLE = "not_escalatable"
STOP_EXHAUSTED = "exhausted"


class LadderOrderError(AssertionError):
    """A trail skipped a rung. This is a defect, never a runtime condition."""


def rung_index(rung: str) -> int:
    """Where a rung sits in the ladder. An optional entry has no place in it."""
    if rung in OPTIONAL_RUNGS:
        raise LadderOrderError(f"{rung!r} is an optional entry, not a rung: {RUNGS}")
    try:
        return RUNGS.index(rung)
    except ValueError as exc:  # pragma: no cover — a typo'd rung is a defect
        raise LadderOrderError(f"{rung!r} is not a rung: {RUNGS}") from exc


def next_rung(current: str) -> str | None:
    """The one rung that may follow `current`, or None at the top."""
    index = rung_index(current)
    if index + 1 >= len(RUNGS):
        return None
    return RUNGS[index + 1]


def last_ordered_rung(trail: list[dict[str, Any]]) -> str | None:
    """The last ORDERED rung a trail actually reached, or None.

    THE ONE WAY to ask a trail "where did this get to". `trail[-1]["rung"]` is
    NOT that question and never was: an optional entry (`OPTIONAL_RUNGS` —
    residential egress) may sit anywhere in a trail, including last, and it is
    not a rung. Every caller that indexed the raw tail instead of calling this
    got a `ValueError` out of `RUNGS.index` the first time a host wired
    residential egress up — a 500 on a write door, for a trail the ladder law
    considers perfectly lawful.

    Returns None for an empty trail AND for a trail of nothing but optional
    entries; both mean "no rung has been reached", and a caller that must have
    one says so itself rather than being handed a rung nobody ran.
    """
    for entry in reversed(trail):
        rung = str(entry.get("rung") or "")
        if rung and rung not in OPTIONAL_RUNGS:
            return rung
    return None


def assert_no_skipped_rung(trail: list[dict[str, Any]]) -> None:
    """THE LADDER LAW, as a callable guard.

    A trail must start at `http` and step exactly one rung at a time. A trail
    that jumps (`http` → `own_browser`) means something escalated past a rung
    without that rung ever being tried or honestly declined — the class of
    defect this whole module exists to make impossible.

    Raises :class:`LadderOrderError`; never returns a bool, because a caller
    that can ignore the answer will.
    """
    if not trail:
        return
    rungs = [
        str(entry.get("rung") or "")
        for entry in trail
        if str(entry.get("rung") or "") not in OPTIONAL_RUNGS
    ]
    if not rungs:
        return
    if rungs[0] != RUNGS[0]:
        raise LadderOrderError(
            f"a capture trail must start at {RUNGS[0]!r}, this one starts at {rungs[0]!r}"
        )
    for previous, current in zip(rungs, rungs[1:]):
        expected = next_rung(previous)
        if current != expected:
            raise LadderOrderError(
                f"the ladder went {previous!r} → {current!r}; the only rung that may "
                f"follow {previous!r} is {expected!r}"
            )


def deepest_ladder_rung(trail: list[dict[str, Any]]) -> str | None:
    """How far up the ladder this trail actually got, or `None` for an empty one.

    "The deepest rung" is the LAST ORDERED rung in the trail. `residential` is an
    optional entry rather than a rung (it is the same `http` work asked again from a
    different address), so it is stepped over here exactly as `assert_no_skipped_rung`
    steps over it — answering `residential` to "how far did this get" would put a value
    in `platform.acquisition_block.rung` that the ledger's own `RUNGS` check refuses,
    and the whole row would be dropped.

    Written for the Block Ledger, which needs ONE rung name beside the full trail so a
    reader can sort and facet without parsing the trail on every row.
    """
    for entry in reversed(trail or []):
        rung = str(entry.get("rung") or "")
        if rung and rung not in OPTIONAL_RUNGS and rung in RUNGS:
            return rung
    return None


# ── What a person's own browser can beat that ours cannot ───────────────────
#
# Each entry is here because the failure is about WHO is asking, not about the
# page: the site is fine, it simply will not show it to a stranger. A 404 is a
# 404 in anybody's browser and is deliberately absent.
OWN_BROWSER_REASONS: frozenset[str] = frozenset(
    {
        "login_wall",
        "paywall",
        "bad_status",
        "cloudflare_block",
        "empty_content",
        "thin_content",
        "low_text_content",
        "wrong_resource",
    }
)

#: Path fragments that mean the site answered with its sign-in page. Narrow on
#: purpose: this is a fact about the response URL, not a guess about the site.
_LOGIN_PATH_MARKERS: tuple[str, ...] = (
    "/login",
    "/signin",
    "/sign-in",
    "/sign_in",
    "/accounts/login",
    "/auth/login",
    "/session/new",
    "/checkpoint",
    "/authwall",
)


def classify_login_wall(
    *,
    status_code: int | None,
    response_url: str | None,
    requested_url: str | None,
) -> bool:
    """Did the site answer "sign in first"?

    True only on evidence we actually hold: a 401/403, or a response address
    that is a sign-in page when a sign-in page is not what was asked for. No
    host list, no keyword sniffing of the body — a guess here would put pages in
    a person's queue that their own browser cannot read either.
    """
    if status_code in (401, 403):
        return True
    response = (response_url or "").lower()
    requested = (requested_url or "").lower()
    if not response:
        return False
    if any(marker in requested for marker in _LOGIN_PATH_MARKERS):
        return False
    return any(marker in response for marker in _LOGIN_PATH_MARKERS)


# ── The sentences. A screen renders these verbatim; nobody reads a code. ────

_WHY_YOUR_BROWSER: dict[str, str] = {
    "login_wall": (
        "This page only shows its content to someone signed in. Your own browser is "
        "already signed in, so it can read it."
    ),
    "paywall": (
        "This page is behind a subscription. Your own browser has your subscription, "
        "so it can read it."
    ),
    "bad_status": (
        "The site refused both our normal request and our server browser. It will "
        "answer an ordinary person's browser."
    ),
    "cloudflare_block": (
        "The site showed a bot check that our server browser could not pass. Your own "
        "browser passes it without noticing."
    ),
    "empty_content": (
        "The page came back empty for us, which usually means it only draws its "
        "content for a signed-in visitor. Your own browser is signed in."
    ),
    "thin_content": (
        "Almost nothing came back for us — usually a sign the site is holding the real "
        "content back from a stranger. Your own browser is not a stranger."
    ),
    "low_text_content": (
        "The page came back with almost no text for us. Your own browser will render "
        "it the way you normally see it."
    ),
    "wrong_resource": (
        "The site sent us to a different page than the one asked for, which it does to "
        "visitors it does not recognise. Your own browser will land on the real page."
    ),
}

_WHAT_TO_DO_DRIVING: dict[str, str] = {
    "login_wall": (
        "Sign in to the site as you normally would, get to the page, then press "
        "\"I'm done, capture it\"."
    ),
    "paywall": (
        "Open the page with your subscription, let it load fully, then press "
        "\"I'm done, capture it\"."
    ),
    "cloudflare_block": (
        "Click through the site's \"are you human\" check, wait for the page, then "
        "press \"I'm done, capture it\"."
    ),
}

_DEFAULT_WHY = (
    "Neither our scraper nor our server browser could read this page, and a browser "
    "that belongs to a real person usually can."
)
_DEFAULT_WHAT_TO_DO = (
    "Open the page, get it to show what you want kept, then press "
    "\"I'm done, capture it\"."
)

#: Honest, unglamorous estimates. A person deciding whether to spend the next
#: ten minutes deserves a number, and a number we can stand behind.
_ESTIMATED_SECONDS: dict[str, int] = {
    "login_wall": 60,
    "paywall": 45,
    "cloudflare_block": 30,
}
_DEFAULT_ESTIMATE_SECONDS = 45


def why_your_browser(reason: str | None) -> str:
    """One sentence: why this page needs a browser that belongs to a person."""
    return _WHY_YOUR_BROWSER.get(reason or "", _DEFAULT_WHY)


def what_to_do_driving(reason: str | None) -> str:
    """One sentence: what the person actually does, when they must do it."""
    return _WHAT_TO_DO_DRIVING.get(reason or "", _DEFAULT_WHAT_TO_DO)


def estimated_seconds(reason: str | None) -> int:
    return _ESTIMATED_SECONDS.get(reason or "", _DEFAULT_ESTIMATE_SECONDS)


def rung_disabled_note(rung: str) -> str:
    """Why nothing happens, when the reason is a setting. Named, never silent."""
    if rung == "own_browser":
        return (
            "This page could be read by your own browser, but sending pages to your "
            "browser is turned off for your organization."
        )
    if rung == "human_drive":
        return (
            "This page needs someone to open it by hand, but asking a person to drive "
            "is turned off for your organization."
        )
    if rung == "browser":
        return (
            "This page could be read by our server browser, but the server browser is "
            "turned off for this deployment."
        )
    return f"The {rung} step is turned off."


# ── The trail and the verdict ───────────────────────────────────────────────


def trail_entry(
    *,
    rung: str,
    ok: bool,
    reason: str | None = None,
    note: str | None = None,
    chars: int = 0,
) -> dict[str, Any]:
    """One rung's attempt, in the shape every repo reads."""
    if rung not in OPTIONAL_RUNGS:
        rung_index(rung)  # a typo'd rung fails here, not three systems later
    return {
        "rung": rung,
        "ok": bool(ok),
        "reason": reason,
        "note": note,
        "chars": int(chars),
        "at": datetime.now(timezone.utc).isoformat(),
    }


@dataclass(frozen=True)
class LadderVerdict:
    """What happens after the last rung on the trail — and never nothing.

    Exactly one of `next_rung` / `stopped_because` is set. That is asserted in
    `__post_init__` rather than documented, because "documented" is how the
    silent-failure class comes back.
    """

    next_rung: str | None = None
    reason: str | None = None
    note: str = ""
    what_to_do: str = ""
    estimated_seconds: int | None = None
    stopped_because: str | None = None

    def __post_init__(self) -> None:
        if bool(self.next_rung) == bool(self.stopped_because):
            raise LadderOrderError(
                "a ladder verdict names exactly one of next_rung / stopped_because; "
                f"got next_rung={self.next_rung!r}, stopped_because={self.stopped_because!r}"
            )

    def as_fields(self) -> dict[str, Any]:
        """The flat fields a ScrapeResult and an API row both carry."""
        return {
            "next_rung": self.next_rung,
            "next_rung_reason": self.reason,
            "next_rung_note": self.note or None,
            "next_rung_what_to_do": self.what_to_do or None,
            "next_rung_estimated_seconds": self.estimated_seconds,
            "stopped_because": self.stopped_because,
        }


@dataclass
class LadderPolicy:
    """Which rungs are allowed to run. The ORGANIZATION decides; we obey.

    `aidream/services/capture_ladder/policy.py` builds this from the
    organization's resolved media settings. The defaults here are what an
    isolated `matrx-scraper` (no database, no tenant) assumes, and they are ON
    because a capability we built and then defaulted off is a capability nobody
    has.
    """

    own_browser_enabled: bool = True
    human_drive_enabled: bool = True

    def allows(self, rung: str) -> bool:
        if rung == "own_browser":
            return self.own_browser_enabled
        if rung == "human_drive":
            return self.human_drive_enabled
        return True


def decide(
    trail: list[dict[str, Any]],
    *,
    reason: str | None,
    policy: LadderPolicy | None = None,
) -> LadderVerdict:
    """What comes after this trail. The one decision point for rungs 3 and 4.

    `trail` must already satisfy the ladder law; it is re-checked here because
    this is the last place a skipped rung is cheap to catch.
    """
    assert_no_skipped_rung(trail)
    policy = policy or LadderPolicy()

    if not trail:
        raise LadderOrderError("a ladder verdict needs a trail; none was recorded")

    current = last_ordered_rung(trail)
    if current is None:
        raise LadderOrderError(
            "a ladder verdict needs at least one ladder rung; this trail has only "
            f"optional entries ({sorted(OPTIONAL_RUNGS)})"
        )
    candidate = next_rung(current)
    if candidate is None:
        return LadderVerdict(
            stopped_because=STOP_EXHAUSTED,
            reason=reason,
            note=(
                "Every step we have was tried, including opening the page yourself, "
                "and the page still did not give up its content."
            ),
        )

    if candidate == "own_browser" and reason not in OWN_BROWSER_REASONS:
        return LadderVerdict(
            stopped_because=STOP_NOT_ESCALATABLE,
            reason=reason,
            note=(
                "This is the site's real answer, not a wall — opening it in your own "
                "browser would get the same thing."
            ),
        )

    if not policy.allows(candidate):
        return LadderVerdict(
            stopped_because=STOP_RUNG_DISABLED,
            reason=reason,
            note=rung_disabled_note(candidate),
        )

    return LadderVerdict(
        next_rung=candidate,
        reason=reason,
        note=why_your_browser(reason),
        what_to_do=what_to_do_driving(reason) if candidate == "human_drive" else "",
        estimated_seconds=estimated_seconds(reason) if candidate == "human_drive" else None,
    )


@dataclass
class LadderTrail:
    """A mutable trail that cannot be built out of order.

    Used by `orchestrator.scrape()` (rungs 1–2) and by
    `aidream/services/capture_ladder` (rungs 3–4) so both halves of the ladder
    produce the identical shape.
    """

    entries: list[dict[str, Any]] = field(default_factory=list)

    def record(
        self,
        rung: str,
        *,
        ok: bool,
        reason: str | None = None,
        note: str | None = None,
        chars: int = 0,
    ) -> None:
        entry = trail_entry(rung=rung, ok=ok, reason=reason, note=note, chars=chars)
        candidate = [*self.entries, entry]
        assert_no_skipped_rung(candidate)  # refuses the skip at the moment it happens
        self.entries = candidate

    def verdict(
        self, *, reason: str | None, policy: LadderPolicy | None = None
    ) -> LadderVerdict:
        return decide(self.entries, reason=reason, policy=policy)
