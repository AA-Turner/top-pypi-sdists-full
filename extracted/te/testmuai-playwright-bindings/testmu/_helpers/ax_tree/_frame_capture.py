"""Per-frame accessibility capture for frame-aware AX tree capture.

Enumerates a page's iframes (Playwright ``page.frames``, skipping main),
classifies each as same-process (capturable via the page's own CDP session
+ ``Accessibility.getFullAXTree({frameId})``) or out-of-process (OOPIF,
capturable via Playwright's auto-attached per-frame CDP session,
``context.new_cdp_session(frame)``), applies a visibility filter and a
nesting-depth pathology backstop (see this module's
``FRAME_DEPTH_BACKSTOP``), and concurrently captures every eligible
frame's AX tree (``asyncio.gather`` — one broken frame never aborts the
rest; capture failures are noted, never raised).

The result (``FrameForest``) feeds ``ax_serializer.serialize_ax_tree``,
which inlines each captured frame's content directly under its owning
``iframe`` AX node, in one continuous ``e<N>`` ref space. This
module owns capture + classification only — grounding (resolving a ref
back to an actionable element inside its frame) is handled elsewhere
(``resolve_session_for_frame`` below).

## Frame attribution (fixed: positional pairing was unsafe)

Earlier revisions of this module (and ``ax_serializer.py``) paired an
iframe AX node to its captured content BY POSITION: Playwright's
``frame.child_frames`` (a set filled in frame-ATTACH order) zipped against
CDP ``Page.getFrameTree``'s ``childFrames`` array, and separately the
serializer consumed a ``FrameCapture`` list positionally as it visited
``iframe``-role AX nodes in document/render order. A live repro (real
Chromium, Playwright 1.57 driver) proved these two orders are NOT always
the same order: appending one iframe to the DOM before a sibling that was
inserted earlier via ``insertBefore`` produces an attach order that
diverges from the true document order — count stays equal, so neither
zip degrades safely; content gets silently swapped onto the WRONG iframe
line.

The fix replaces BOTH positional pairings with a single stable-identity
correlation, resolved directly off each iframe AX node's own OWNER
``backendDOMNodeId`` (already captured — no extra AX fetch):

    iframe AX node --(backendNodeId)--> DOM.describeNode --(frameId)-->
    the REAL CDP frame id this <iframe> element owns.

Verified live (Chromium, same session ``DOM.describeNode`` calls this
module already makes elsewhere): ``DOM.describeNode({backendNodeId})``
populates ``node.frameId`` for a frame-owner element REGARDLESS of
same-process/OOPIF boundaries (Chrome's DOM domain tracks frame ownership
centrally — the same property already established below for
``Page.getFrameTree``). This makes the AX-node -> content-frame-id mapping
100% independent of any Playwright or CDP list ORDER: ``FrameCapture``
entries are keyed by their owner's ``backendDOMNodeId`` (see
``owner_backend_node_id``), and ``ax_serializer`` looks each iframe node up
by that key — a dict lookup, never ``next()`` on an iterator. An iframe AX
node whose owner cannot be resolved to a real frame id (a
``DOM.describeNode`` failure, or an empty/missing ``frameId``) gets
``status="unresolved"`` — rendered as an honest
``[frame ? unresolved — not captured]`` note, NEVER a positional guess.

Playwright ``Frame`` objects are still needed for two things this module
cannot do via CDP alone: (1) OOPIF session acquisition
(``context.new_cdp_session(frame)`` — Playwright-only auto-attach
bookkeeping, no direct CDP equivalent) and (2) the visibility
check (``frame.frame_element().bounding_box()``, whose fail-open/fail-
closed distinction on check-failure-vs-determined-hidden is preserved
byte-for-byte). Matching a RESOLVED content frame id to the Playwright
``Frame`` object that captures/checks it is done two ways, never
positionally:

  - OOPIF frames self-identify EXACTLY: probe every ``page.frames`` entry
    for its own dedicated CDP session (the existing
    ``_NO_DEDICATED_SESSION_HINT`` test); a frame that has one is a genuine
    OOPIF root, and ``Page.getFrameTree`` sent on THAT frame's OWN session
    reports, as its own tree's root frame id, exactly that frame's real
    CDP id — self-reported, zero ambiguity, independent of enumeration
    order (``_probe_all_oopif_sessions``).
  - Same-process frames have no dedicated session to self-identify with,
    so they are matched by (url, name) against the already-fetched
    ``Page.getFrameTree`` record for the resolved content frame id
    (``_match_frame_by_identity``) — best-effort, and an ambiguous (>1
    matching candidate) or absent match is left unresolved rather than
    guessed: that frame's capture honestly downgrades to
    ``status="capture_failed"`` (the existing note), never a wrong-content
    swap, since ATTRIBUTION already succeeded independently via
    ``describeNode`` above and is not affected by a capture-side miss.

## Same-process capture via ancestor-session frameId (fix for a
live-proven capture failure)

Live repro: https://dom-setu.vercel.app/ecommerce/checkout?domComplexity=
iframe. The checkout ``<iframe>`` starts empty and is populated by
client-side JS after load. Playwright's own ``Frame.url`` for it stays
``"about:blank"`` (Playwright caches the URL from the frame's initial
commit and never re-polls it for a same-document-internal population),
while CDP's ``Page.getFrameTree`` reports that SAME frame's ``url`` as
its PARENT's url — verified live, a real Chrome quirk for dynamically-
populated same-process frames, not a Playwright bug. The frame-attribution
fix above (``_match_frame_by_identity``) resolves a content frame id to a
Playwright ``Frame`` object by comparing ``(url, name)`` between the two
sides; for this entire class of iframe (``srcdoc``, ``about:blank`` +
``document.write``, anything populated after the initial commit — all
ubiquitous) the two urls can never agree, so the match always comes back
empty and the frame was wrongly downgraded to ``capture_failed`` even
though ATTRIBUTION (which never depended on this match — see the section
above) had already succeeded, and CDP already had everything
needed to capture the frame's real content.

The fix: capture no longer needs a matched Playwright ``Frame`` at all
for the common (same-process) case. Once a content frame id is resolved
(unchanged — ``DOM.describeNode`` on the owner), it is captured DIRECTLY
via ``Accessibility.getFullAXTree({frameId: content_frame_id})`` sent on
the CURRENT ancestor CDP session (the session that owns the tree the
iframe node lives in) — zero Playwright objects involved. Verified live:
this succeeds and returns the frame's real, CURRENT content for every
same-process frame, completely independent of whatever Playwright's
cached ``Frame.url`` says.

Only when that call fails or returns zero nodes is the frame treated as
a possible OOPIF. Verified live: for a genuine cross-process iframe, the
identical ``getFullAXTree({frameId})`` call sent on the ancestor session
fails outright with a CDP protocol error ("Frame with the given frameId
is not found.") — a clean, unambiguous signal, never a false negative
for an actual same-process frame. (This also corrects an earlier
assumption in this module: a genuine OOPIF's frame id does NOT
appear anywhere in the ancestor's own ``Page.getFrameTree`` response —
verified live via ``Target.getTargets`` showing a separate ``type:
"iframe"`` target whose id is simply absent from the parent target's
``childFrames`` array. ``Page.getFrameTree`` was never actually a
reliable source for OOPIF identity; only ``DOM.describeNode``, used for
ATTRIBUTION, reaches across that boundary.)

Only on that failure does capture fall back to Playwright at all — and
even then, lazily, purely to locate an OOPIF's own dedicated CDP session
(``BrowserContext.new_cdp_session(frame)``, which succeeds only for a
frame that already has one). Candidate ``page.frames`` are probed ONE AT
A TIME and AT MOST ONCE per whole capture (``_LazyOopifResolver`` — a
capture-scoped cache shared across the entire recursive walk: a
candidate frame already probed, whether it matched or not, is never
probed again), self-identifying via ``Page.getFrameTree`` sent on ITS
OWN freshly-acquired session (unchanged from the pre-existing OOPIF
mechanism — still exact self-identification, still non-positional,
still zero ambiguity). A content frame id that no candidate
self-identifies as, after every candidate has been exhausted, is an
honest ``capture_failed`` — never a guess.

The visibility filter no longer needs a Playwright ``Frame``
either, for the identical reason: it now reads the iframe OWNER
element's own box model directly — ``DOM.getBoxModel({backendNodeId})``
sent on the PARENT session (the very session that already resolved this
owner's content frame id) — instead of
``frame.frame_element().bounding_box()``. Verified live: CDP does NOT
return a null/empty model for a genuinely unrendered node
(``display:none``, detached) the way Playwright's own API translates it
— it REJECTS the whole call ("Could not compute box model."). Since a
raw CDP exception can't reliably distinguish "genuinely not rendered"
from any other transient failure, both collapse to the same fail-open
default: a FAILED box-model query fails open (include, never exclude on
an inconclusive check); only a SUCCESSFUL query reporting an explicit
zero-area box is a *determined* "not visible" (skip).

``_match_frame_by_identity``/``_find_cdp_frame_node`` (the ``(url,
name)`` matcher) are retired from this module's CAPTURE path entirely —
they remain in use only by ``resolve_session_for_frame`` below (the
separate post-capture action-grounding routing problem: given an
already-known real frame id, find a live session to act on it — not
exercised by the live capture failure this fix addresses).

## OOPIF session mechanism (investigated against the pinned Playwright
1.57.0 driver — see ``playwright/driver/package/lib/server/chromium/
crBrowser.js: CRBrowserContext.newCDPSession``)

``BrowserContext.new_cdp_session()`` is a public, documented API that
accepts either a ``Page`` or a ``Frame``. Passing a ``Frame`` succeeds ONLY
when that frame already has its own dedicated CDP session — which
Playwright sets up automatically the moment it auto-attaches to an
out-of-process iframe's target (server-side:
``page.delegate._sessions.get(frame._id)``). For a same-process frame
there is no such dedicated session, and the call raises: "This frame does
not have a separate CDP session, it is a part of the parent frame's
session" (matched here via a lowercased substring, not the full message,
to tolerate driver wording drift across Playwright versions). This is
exactly the test Playwright's own ``Frame.frame_element()`` uses
internally to route across the same boundary (``crPage.js:
getFrameElement`` / ``_sessionForFrame``) — we reuse it rather than
inventing a parallel heuristic.

For a same-process frame we still need the real CDP ``frameId`` string to
pass to ``Accessibility.getFullAXTree({frameId: ...})`` (omitting it
always targets the *main* frame of whatever target the session is
attached to — it does not, by itself, reach into child frames). Playwright's
Python API exposes no such id on a ``Frame`` object: its channel ``guid``
is a random ``createGuid()`` value with no relation to the CDP frame id
(verified in the driver's ``frames.js`` / ``instrumentation.js``).
``Page.getFrameTree`` (CDP ``Page`` domain), called once from the page's
own top-level session, returns the *real* frame id — and, per frame, its
``url``/``name`` — for every SAME-PROCESS frame Chrome knows about.

CORRECTION (verified live via ``Target.getTargets``): an earlier
assumption in this module — that this same response also includes
out-of-process placeholders — does not hold. A genuine OOPIF is a
separate CDP target (``type: "iframe"``) and its frame id is simply
ABSENT from ``childFrames`` when ``Page.getFrameTree`` is sent on the
ancestor/main session; only same-process frames show up there. This
response is used purely as an ID -> (url, name) lookup table
(``_find_cdp_frame_node``) for ``_match_frame_by_identity`` — and that
matcher (and this lookup) no longer sit in this module's capture path at
all (see the section above); they remain only for
``resolve_session_for_frame``'s separate grounding problem.
"""

from __future__ import annotations

import asyncio
import logging
from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import Any

from playwright.async_api import Frame, Page

from ._accessibility import (
    AxNode,
    _capture_ax_tree_via_session,
    capture_accessibility_tree,
)
from ._constants import FRAME_ROLE

logger = logging.getLogger(__name__)

# Not a semantic nesting limit — the merged AX doc is never sent to the
# model as-is (bounded windows into it are what matter), so limiting
# nesting protects nothing a real page needs. This is a pathology
# backstop: insurance against a runaway/cyclic frame chain, not a ceiling
# ordinary pages should ever approach. Frame depth 1 = a direct child of
# the main page; a frame at depth 11 (a child of a depth-10 frame) is
# noted, not captured.
FRAME_DEPTH_BACKSTOP = 10

_NO_DEDICATED_SESSION_HINT = "separate cdp session"


@dataclass
class FrameCapture:
    """Capture result for one iframe.

    ``status`` is one of ``"captured"``, ``"hidden"``, ``"capture_failed"``,
    ``"depth_exceeded"``, ``"unresolved"``. ``tree`` is populated only when
    ``status == "captured"``. ``children`` holds this frame's OWN nested
    ``FrameCapture``s (its child iframes) — always empty unless
    ``status == "captured"`` (there is nothing meaningful to recurse into
    otherwise).

    ``owner_backend_node_id`` is the iframe AX node's OWNER element's
    ``backendDOMNodeId`` in its PARENT frame's session/target namespace —
    the stable correlation key ``ax_serializer`` uses to find this
    entry (never positionally). Set even when ``status == "unresolved"``
    (the owner node itself was found; only ITS content frame id failed to
    resolve).

    No display frame number lives here: this dataclass
    is a discovery-time result, populated concurrently (``asyncio.gather``)
    across frames at the same nesting level — completion order is a race,
    not a document order. ``[frame fN]`` display numbers are minted by
    ``ax_serializer.serialize_ax_tree`` during its own deterministic,
    depth-first document-order walk instead, so the same forest always
    renders byte-identical numbering regardless of which frame's capture
    happened to finish first.
    """

    frame_id: str
    status: str
    tree: AxNode | None = None
    children: list[FrameCapture] = field(default_factory=list)
    owner_backend_node_id: int | None = None


@dataclass
class FrameForest:
    """Whole-page capture: the main tree + its (possibly empty) iframe forest."""

    main_tree: AxNode | None
    frame_captures: list[FrameCapture] = field(default_factory=list)


async def _is_owner_visible(session: Any, backend_node_id: int | None) -> bool:
    """Visibility filter: the iframe OWNER element's own
    box model, fetched directly via ``DOM.getBoxModel({backendNodeId})``
    on the PARENT session — the very session that already resolved this
    owner's content frame id via ``DOM.describeNode`` above. Replaces an
    earlier Playwright-``Frame``-based ``frame.frame_element().
    bounding_box()`` check: that required a matched PW ``Frame`` to
    even ask the question, exactly the dependency this fix retires (see
    module docstring, "Same-process capture via ancestor-session
    frameId"). No Playwright object is needed here at all — the owner
    element always lives in the PARENT frame's own DOM/session,
    regardless of whether its CONTENT frame turns out to be same-process
    or OOPIF.

    Verified live (real Chromium): CDP does NOT return a null/empty model
    for a genuinely unrendered node (``display:none``, detached) the way
    Playwright's own API translates it — it REJECTS the whole call
    ("Could not compute box model."). A raw CDP exception can't reliably
    distinguish that from any other transient failure, so both collapse
    to the same fail-open default: a FAILED query means "could not
    determine visibility" -> include, never exclude. Only a SUCCESSFUL
    query reporting an explicit zero-area box is a *determined* "not
    visible".
    """
    if backend_node_id is None:
        return True  # nothing to check — fail open
    try:
        result = await session.send(
            "DOM.getBoxModel", {"backendNodeId": backend_node_id}
        )
    except Exception:
        return True  # box-model failure — fail open, never exclude on a failed check
    model = (result or {}).get("model") or {}
    return bool(model.get("width", 0) > 0 and model.get("height", 0) > 0)


def _iter_iframe_ax_nodes(node: AxNode) -> Iterator[AxNode]:
    """Depth-first walk yielding every ``iframe``-role AX node anywhere in
    ``node`` (one frame's OWN captured tree, pre-merge).

    This is the SOLE source of truth for "what child frames
    exist at this level" — driven entirely by the AX tree Chrome itself
    just rendered, never by a separate Playwright/CDP structure that could
    disagree with it on count or order. An ``iframe`` AX node has no AX
    children of its own to recurse into (its frame's content is a
    completely separate captured tree, merged in by ``ax_serializer``).
    """
    role = (node.role or "").strip().lower()
    if role == FRAME_ROLE:
        yield node
        return
    for child in node.children:
        yield from _iter_iframe_ax_nodes(child)


async def _resolve_owner_frame_id(session: Any, backend_node_id: int | None) -> str:
    """PRIMARY attribution mechanism: iframe AX node's OWNER
    ``backendDOMNodeId`` -> its CONTENT frame's real CDP frame id, via
    ``DOM.describeNode({backendNodeId})`` on the SAME session that captured
    the tree the owner node lives in (``node.frameId`` is scoped to that
    session's DOM namespace, exactly like ``backendDOMNodeId`` itself).

    Verified live (real Chromium): ``DOM.describeNode`` populates
    ``node.frameId`` for frame-owner elements — CDP's own protocol
    description for ``DOM.Node.frameId`` is simply "Frame ID for frame
    owner elements", with no same-process/OOPIF distinction, consistent
    with ``Page.getFrameTree`` already being known (see module docstring)
    to track frame identity centrally across that boundary.

    Never raises and never guesses: any failure (missing backend id, CDP
    error, empty/missing ``frameId`` in a well-formed response) returns
    ``""`` — the caller treats that as "owner resolution failed" and emits
    an honest ``unresolved`` note, never a positional fallback.
    """
    if backend_node_id is None:
        return ""
    try:
        described = await session.send(
            "DOM.describeNode", {"backendNodeId": backend_node_id}
        )
    except Exception:
        return ""
    node = (described or {}).get("node") or {}
    return node.get("frameId") or ""


def _find_cdp_frame_node(
    node: dict[str, Any], frame_id: str
) -> dict[str, Any] | None:
    """Recursive by-ID search over one ``Page.getFrameTree`` response node
    (``{"frame": {"id", "url", "name", ...}, "childFrames": [...]}``).
    Structural parent/child nesting is unambiguous (a real tree) — this
    never relies on sibling ORDER, only on ``frame.id`` identity."""
    frame_info = node.get("frame") or {}
    if frame_info.get("id") == frame_id:
        return node
    for child in node.get("childFrames") or []:
        found = _find_cdp_frame_node(child, frame_id)
        if found is not None:
            return found
    return None


def _match_frame_by_identity(
    frame_tree_root: dict[str, Any] | None,
    content_frame_id: str,
    candidates: list[Frame],
) -> Frame | None:
    """Best-effort, NEVER-positional Playwright ``Frame`` match for an
    already-resolved ``content_frame_id`` (capture-side session/
    visibility acquisition only; attribution itself does not depend on
    this succeeding, see module docstring).

    Looks up ``content_frame_id``'s own ``(url, name)`` from the
    already-fetched ``Page.getFrameTree`` structure (a structural by-id
    search, unambiguous), then finds the Playwright candidate reporting
    that SAME ``(url, name)``. Zero or more-than-one matching candidate is
    an honest "can't tell which one" — returns ``None`` rather than
    guessing; the caller downgrades that frame to ``capture_failed``.
    """
    if frame_tree_root is None:
        return None
    node = _find_cdp_frame_node(frame_tree_root, content_frame_id)
    if node is None:
        return None
    frame_info = node.get("frame") or {}
    target_url = frame_info.get("url")
    target_name = frame_info.get("name", "")
    matches: list[Frame] = []
    for frame in candidates:
        try:
            if frame.url == target_url and frame.name == target_name:
                matches.append(frame)
        except Exception:
            continue
    return matches[0] if len(matches) == 1 else None


async def _probe_oopif_session(page: Page, frame: Frame) -> tuple[Any, bool]:
    """Probe whether ``frame`` has its own dedicated CDP session (a genuine
    OOPIF root) — the EXACT test ``capture_frame_forest`` already uses
    (``new_cdp_session`` raises the ``_NO_DEDICATED_SESSION_HINT`` message
    for a same-process frame, matched via a lowercased substring to tolerate
    driver wording drift).

    Returns ``(session, True)`` on success — caller now owns and must
    ``.detach()`` that session. Returns ``(None, False)`` for a same-process
    frame (no session created, nothing to detach) or any OTHER unexpected
    probe failure (logged, treated the same as same-process — never raises).
    """
    try:
        session = await page.context.new_cdp_session(frame)
        return session, True
    except Exception as e:
        if _NO_DEDICATED_SESSION_HINT not in str(e).lower():
            logger.debug(
                "frame_capture: unexpected new_cdp_session error probing a "
                "frame for grounding — treating as same-process: %s", e,
            )
        return None, False


class _LazyOopifResolver:
    """Capture-scoped, lazy OOPIF session lookup.

    Replaces an earlier eager, whole-page-upfront OOPIF probe: since
    same-process frames (the common case) are now captured directly via
    the ancestor session's own ``Accessibility.getFullAXTree({frameId})``
    (see module docstring) with no Playwright involvement at all,
    Playwright ``Frame`` candidates are only ever touched once THAT
    attempt has already failed/returned empty for a given content frame
    id. One instance is shared across the WHOLE recursive capture (every
    nesting level), so a candidate frame is probed AT MOST ONCE per
    capture regardless of how many separate lookups are made —
    ``_candidates`` is a shared list, drained by ``.pop(0)``, never
    re-scanned once a frame has been tried.

    A genuine OOPIF root SELF-IDENTIFIES its own TRUE CDP frame id by
    sending ``Page.getFrameTree`` on its OWN freshly-acquired dedicated
    session (unchanged from the earlier mechanism): that session's
    default root IS that frame, so ``frameTree.frame.id`` is, by
    construction, exactly this frame's real id — no ordering or
    positional assumption anywhere, no ambiguity even when several OOPIFs
    share a URL, and no dependency on ``Page.getFrameTree``
    reaching across the process boundary from the ANCESTOR side (it does
    not — see module docstring correction).

    ``_by_frame_id`` caches every self-identified OOPIF session found so
    far (even ones that did not match what THIS lookup was looking for —
    a bonus for a LATER lookup on the same page). A content frame id that
    no candidate self-identifies as, once every candidate is exhausted,
    resolves to ``None`` — the caller's honest ``capture_failed``, never
    a guess.
    """

    def __init__(self, page: Page) -> None:
        self._page = page
        self._by_frame_id: dict[str, Any] = {}
        self._candidates: list[Frame] | None = None

    async def resolve(self, content_frame_id: str) -> Any | None:
        cached = self._by_frame_id.get(content_frame_id)
        if cached is not None:
            return cached

        if self._candidates is None:
            try:
                self._candidates = [
                    f for f in self._page.frames if f is not self._page.main_frame
                ]
            except Exception:
                self._candidates = []

        while self._candidates:
            frame = self._candidates.pop(0)
            session, is_oopif = await _probe_oopif_session(self._page, frame)
            if not is_oopif:
                continue
            true_id: str | None = None
            try:
                tree_result = await session.send("Page.getFrameTree")
                true_id = ((tree_result or {}).get("frameTree") or {}).get(
                    "frame", {}
                ).get("id")
            except Exception:
                true_id = None
            if not true_id:
                try:
                    await session.detach()
                except Exception:
                    pass
                continue
            self._by_frame_id[true_id] = session
            if true_id == content_frame_id:
                return session
        return None

    def sessions(self) -> list[Any]:
        """Every OOPIF session discovered so far — caller owns detaching
        each of these (never detach one still in ``_by_frame_id`` early;
        a later ``.resolve()`` call may still return it from cache)."""
        return list(self._by_frame_id.values())


async def capture_frame_forest(
    page: Page,
    *,
    viewport_width: float = 1280,
    viewport_height: float = 800,
) -> FrameForest:
    """Capture the main frame plus every eligible iframe, merge-ready.

    Fast path: pages with no iframes at all (``len(page.frames) <= 1``)
    skip every frame-resolution CDP call and return an empty
    ``frame_captures`` — the byte-identical guarantee for plain pages holds
    without any extra round-trips (this is the common case).

    Never raises: any unrecoverable failure downgrades to
    ``FrameForest(main_tree, [])`` (main-frame capture only, unchanged from
    today) rather than propagating.

    Discovery is driven entirely by the ALREADY-CAPTURED AX
    tree's own ``iframe`` nodes (``_iter_iframe_ax_nodes``), not by walking
    Playwright's ``child_frames``: a frame's children cannot be discovered
    until ITS OWN tree has been captured, so recursion happens
    level-by-level (concurrent WITHIN a level via ``asyncio.gather`, same
    as before; sequential ACROSS levels, since level N+1 discovery depends
    on level N's tree) rather than in one flat, fully-upfront gather. Given
    the pathology backstop (``FRAME_DEPTH_BACKSTOP``), this trades a small
    amount of latency for correctness under attach/render-order divergence
    — see module docstring. Display frame numbers are NOT assigned here:
    concurrent, level-by-level discovery order is not
    a deterministic document order, so minting ``[frame fN]`` here would
    make output depend on real-time completion races.
    ``ax_serializer.serialize_ax_tree`` mints them during its own
    depth-first document-order walk instead — see that module.
    """
    main_tree = await capture_accessibility_tree(
        page,
        viewport_width=viewport_width,
        viewport_height=viewport_height,
        skip_bounding_boxes=True,
    )

    try:
        if len(page.frames) <= 1:
            return FrameForest(main_tree=main_tree, frame_captures=[])
    except Exception:
        return FrameForest(main_tree=main_tree, frame_captures=[])

    if main_tree is None:
        return FrameForest(main_tree=main_tree, frame_captures=[])

    try:
        main_session = await page.context.new_cdp_session(page)
    except Exception:
        return FrameForest(main_tree=main_tree, frame_captures=[])

    oopif_resolver = _LazyOopifResolver(page)
    try:

        async def capture_and_recurse(
            fc: FrameCapture,
            session: Any,
            content_frame_id: str,
            next_depth: int,
        ) -> None:
            """Ancestor-session frameId-first. ``session`` is
            whichever CDP session already owns the tree the iframe's
            OWNER node lives in — try capturing the CONTENT frame
            directly off that SAME session first (works for every
            same-process frame, regardless of what Playwright's own
            ``Frame.url`` reports — see module docstring). Only on
            failure/empty is this treated as a possible OOPIF and a
            Playwright-backed session looked up, lazily, via
            ``oopif_resolver`` — never by ``(url, name)`` matching.
            """
            try:
                tree = await _capture_ax_tree_via_session(
                    session,
                    frame_id=content_frame_id,
                    viewport_width=viewport_width,
                    viewport_height=viewport_height,
                    skip_bounding_boxes=True,
                )
            except Exception:
                tree = None

            child_session = session  # same-process: subtree stays on this session
            if tree is None:
                oopif_session = await oopif_resolver.resolve(content_frame_id)
                if oopif_session is None:
                    return  # fc.status stays "capture_failed" (set below)
                try:
                    tree = await _capture_ax_tree_via_session(
                        oopif_session,
                        frame_id=None,  # OOPIF's own dedicated session's default root
                        viewport_width=viewport_width,
                        viewport_height=viewport_height,
                        skip_bounding_boxes=True,
                    )
                except Exception:
                    tree = None
                if tree is None:
                    return  # fc.status stays "capture_failed"
                child_session = oopif_session

            fc.tree = tree
            fc.status = "captured"
            fc.children = await discover_children(tree, child_session, next_depth)

        async def discover_children(
            tree: AxNode,
            session: Any,
            depth: int,
        ) -> list[FrameCapture]:
            entries: list[tuple[FrameCapture, Any | None]] = []
            for ax_node in _iter_iframe_ax_nodes(tree):
                owner_id = ax_node.backend_dom_node_id

                content_frame_id = await _resolve_owner_frame_id(session, owner_id)
                if not content_frame_id:
                    entries.append((
                        FrameCapture(
                            "", "unresolved",
                            owner_backend_node_id=owner_id,
                        ),
                        None,
                    ))
                    continue

                if depth > FRAME_DEPTH_BACKSTOP:
                    entries.append((
                        FrameCapture(
                            content_frame_id, "depth_exceeded",
                            owner_backend_node_id=owner_id,
                        ),
                        None,
                    ))
                    continue

                try:
                    visible = await _is_owner_visible(session, owner_id)
                except Exception:
                    visible = True  # fail open (belt-and-suspenders)

                if not visible:
                    entries.append((
                        FrameCapture(
                            content_frame_id, "hidden",
                            owner_backend_node_id=owner_id,
                        ),
                        None,
                    ))
                    continue

                fc = FrameCapture(
                    content_frame_id, "capture_failed",
                    owner_backend_node_id=owner_id,
                )
                entries.append((
                    fc,
                    capture_and_recurse(fc, session, content_frame_id, depth + 1),
                ))

            coros = [coro for _fc, coro in entries if coro is not None]
            if coros:
                await asyncio.gather(*coros, return_exceptions=True)
            return [fc for fc, _coro in entries]

        frame_captures = await discover_children(main_tree, main_session, 1)
        return FrameForest(main_tree=main_tree, frame_captures=frame_captures)

    except Exception:
        return FrameForest(main_tree=main_tree, frame_captures=[])
    finally:
        for session in oopif_resolver.sessions():
            try:
                await session.detach()
            except Exception:
                pass
        try:
            await main_session.detach()
        except Exception:
            pass


async def resolve_session_for_frame(page: Page, frame_id: str) -> Any:
    """Resolve a live CDP session whose DOM domain can act on ``frame_id``'s
    nodes — the grounding counterpart to this module's capture-time
    session routing. Used by ``PlaywrightBrowser.
    prepare_ref_action`` / ``scroll_node_into_view`` / ``get_node_viewport_
    status`` and ``flat_dom.enrich_element_by_node_id`` so every CDP call
    grounding a ref lands on the renderer that actually owns the node —
    the fix for a bare-backendNodeId collision across frames (two different
    frames can each report backendNodeId 42; calling DOM.* on the wrong
    session can resolve, or fail to resolve, the WRONG physical node).

    ``frame_id == ""`` (the main-frame convention) is the fast,
    common path — a fresh session on the page itself, IDENTICAL to what
    every grounding call site did before frame-scoped routing was added
    (zero extra CDP round trips — frame_id threading is fully backward
    compatible / byte-identical for main-frame refs).

    For a real frame id: one ``Page.getFrameTree`` call resolves
    ``frame_id``'s own ``(url, name)`` (a structural by-id lookup,
    ``_find_cdp_frame_node`` — never positional), then the owning
    Playwright ``Frame`` is found by matching that ``(url, name)`` against
    ``page.frames`` (best-effort, ``_match_frame_by_identity`` — an
    ambiguous or absent match falls through to the same main-session
    fallback as any other unresolvable id, below). Once found, classifies
    it exactly as capture does (``_probe_oopif_session``): a genuine
    OOPIF root's own dedicated session already has that frame as its
    default root — no ``frameId`` param is needed for any of
    ``DOM.resolveNode``, ``DOM.getBoxModel``, ``DOM.scrollIntoViewIfNeeded``,
    or ``Accessibility.getPartialAXTree`` (none of them take one; the
    SESSION is what scopes the call, since backendNodeId is unique within
    one CDP target's whole same-process render tree — see this module's
    docstring). On the same-process case, climbs ``parent_frame`` looking
    for the nearest OOPIF ancestor (repeating the same probe) or, failing
    that, the main page.

    ANY resolution failure — the frame id no longer maps to a live frame
    (a stale ref surviving a navigation, most likely), an ambiguous/absent
    Playwright-frame match, a detached frame, a probe error — falls back to
    a fresh main-page session: the caller's own CDP calls then fail cleanly
    against a now-wrong/stale backendNodeId exactly as they already do
    today (``ValueError`` "node not found" / the viewport-status "unknown
    geometry" safe default) rather than raising here.

    Caller always owns and must ``.detach()`` the returned session.
    """
    if not frame_id:
        return await page.context.new_cdp_session(page)

    main_session: Any = None
    frame_tree_root: dict[str, Any] | None = None
    try:
        main_session = await page.context.new_cdp_session(page)
        ft_result = await main_session.send("Page.getFrameTree")
        frame_tree_root = (ft_result or {}).get("frameTree")
    except Exception:
        frame_tree_root = None
    finally:
        if main_session is not None:
            try:
                await main_session.detach()
            except Exception:
                pass

    try:
        candidates = [f for f in page.frames if f is not page.main_frame]
    except Exception:
        candidates = []

    target_frame = _match_frame_by_identity(frame_tree_root, frame_id, candidates)
    if target_frame is None:
        # Stale/unresolvable/ambiguous frame id — let the caller's own CDP
        # calls fail cleanly against the main session rather than raising.
        return await page.context.new_cdp_session(page)

    session, is_oopif = await _probe_oopif_session(page, target_frame)
    if is_oopif:
        return session

    ancestor = target_frame.parent_frame
    while ancestor is not None and ancestor is not page.main_frame:
        session, is_oopif = await _probe_oopif_session(page, ancestor)
        if is_oopif:
            return session
        ancestor = ancestor.parent_frame

    return await page.context.new_cdp_session(page)
