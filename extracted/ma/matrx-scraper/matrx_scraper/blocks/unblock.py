"""What would unblock it — one lawful route per error class, in plain English.

`HUNTER-RULES.md` law 3 says a block is recorded with "how a human would have experienced it"
and law 6 says the routes that cross DRM, a paywall, somebody else's login or a bot wall are
Arman's decision and never an agent's. So every sentence here is a LAWFUL route — the expert's
own purchased copy, an official export, an official API, OAuth as the account owner, the
person's own signed-in browser — and a class whose only route crosses one of those lines
answers with `decision`, which is what the screen shows and what the retry action refuses.

A class we have no route for answers with an empty note rather than an invented one. An empty
"what would unblock it" is honest; a guessed one sends somebody down a dead end.
"""

from __future__ import annotations

from dataclasses import dataclass

__all__ = ["Unblock", "unblock_for"]


@dataclass(frozen=True)
class Unblock:
    #: The machine key, so the screen can group and the retry action can decide.
    route: str | None
    #: The one sentence a non-technical person reads.
    note: str
    #: True when clearing this needs Arman, not an agent (HUNTER-RULES law 6).
    is_decision: bool = False


_NOTHING = Unblock(route=None, note="", is_decision=False)

#: Keyed by error class. The classes come from the engines themselves — the scraper's
#: failure reasons, the capture ladder's stop reasons, the export reader's codes, the ebook
#: reader's protection schemes, the connected-account refusals.
_ROUTES: dict[str, Unblock] = {
    # ── The page is readable, but not by a server ────────────────────────────
    "login_wall": Unblock(
        "own_browser",
        "This page only shows its content to someone signed in. Your own browser is already "
        "signed in, so send it there and it can read it.",
    ),
    "cloudflare_block": Unblock(
        "own_browser",
        "The site's bot protection refused our servers. Your own browser looks like a person "
        "to it, so send this one to your browser.",
    ),
    "bad_status": Unblock(
        "own_browser",
        "The site answered with an error for us. Try it in your own browser — if it opens "
        "there, we can capture it from there.",
    ),
    "empty_content": Unblock(
        "own_browser",
        "We reached the page but no text came back, which usually means it builds itself in "
        "the browser. Your own browser will have it on screen.",
    ),
    "thin_content": Unblock(
        "own_browser",
        "Almost no text came back. Opening it in your own browser and capturing what you see "
        "gets the whole page.",
    ),
    "low_text_content": Unblock(
        "own_browser",
        "The page is mostly not text for us. Your own browser sees it the way you do.",
    ),
    "wrong_resource": Unblock(
        "own_browser",
        "The site sent us somewhere other than the address we asked for. Open it yourself and "
        "capture the page you actually land on.",
    ),
    "proxy_error": Unblock(
        "retry",
        "Our proxy network refused to carry this request. It is usually temporary — retrying "
        "is the first thing to try.",
    ),
    "request_error": Unblock(
        "retry",
        "The request did not complete. Retrying is the first thing to try.",
    ),
    # ── The ladder itself stopped ────────────────────────────────────────────
    "rung_disabled": Unblock(
        "settings",
        "A step of the ladder is switched off for this organization, so nothing tried it. "
        "Turn that step back on in the Libraries settings and this will go further.",
    ),
    "exhausted": Unblock(
        None,
        "Every step of the ladder was tried, including your own browser. This one needs a "
        "different route into the content, not another attempt at the page.",
    ),
    "not_escalatable": Unblock(
        None,
        "This failure is not one a different browser can beat — the page genuinely is not "
        "there or is not what was asked for.",
    ),
    # ── Paywalls and protection — his call, never ours ───────────────────────
    "paywall": Unblock(
        "decision",
        "The content is behind a paid subscription. The lawful routes are the expert's own "
        "subscription opened in their own browser, a licence from the publisher, or a "
        "licensed data provider — which of those we use is a decision, not a fix.",
        is_decision=True,
    ),
    "drm_protected": Unblock(
        "decision",
        "The file is copy-protected and we will never strip a publisher's protection. What "
        "does work: the expert's own highlights and notes export, a DRM-free copy from the "
        "publisher, the audiobook, or the library's lending copy.",
        is_decision=True,
    ),
    "bot_wall": Unblock(
        "decision",
        "The site puts a human check in front of this page. We never answer one for you, so "
        "the route is you opening it yourself, or a partner arrangement with the site.",
        is_decision=True,
    ),
    # ── Files ────────────────────────────────────────────────────────────────
    "unsupported_format": Unblock(
        "convert",
        "We recognise this file but cannot read this format yet. Exporting or saving it as "
        "PDF, EPUB, DOCX or plain text gets it in today.",
    ),
    "export_format_not_readable": Unblock(
        "documented_route",
        "We recognise this export but cannot read it yet. The service's own documented export "
        "route produces a format we do read.",
    ),
    "export_unrecognised": Unblock(
        "re_export",
        "This does not look like any export we know. Re-exporting from the service itself, "
        "rather than a copy of it, usually produces the shape we expect.",
    ),
    "empty_file": Unblock(
        None,
        "The file opened but produced no readable words. It may be a scan — in which case the "
        "route is reading the images, not the text layer.",
    ),
    "ocr_binary_missing": Unblock(
        "settings",
        "This scan needs OCR to read, and the OCR engine is not installed on this server. "
        "That is an infrastructure gap, not something about this file — install Tesseract "
        "(or the configured OCR provider) on the host and reprocess.",
    ),
    # ── Connected accounts ───────────────────────────────────────────────────
    "scope_not_granted": Unblock(
        "reconnect",
        "The connected account has not granted us the permission this needs. Reconnecting it "
        "and approving that permission is the whole fix.",
    ),
    "scope_not_requested": Unblock(
        "decision",
        "This needs a permission our application does not ask for at all yet. Adding it is a "
        "consent decision with the provider, not a code change.",
        is_decision=True,
    ),
    "not_connected": Unblock(
        "connect",
        "No account of this kind is connected. Connecting one in Settings → Integrations opens "
        "everything in it at once.",
    ),
    "connection_needs_attention": Unblock(
        "reconnect",
        "The connection has expired or been revoked by the provider. Reconnecting it restores "
        "everything that depends on it.",
    ),
    "permission_denied": Unblock(
        "ask_owner",
        "The account is connected but the provider refused this particular item. Whoever owns "
        "it has to share it with the connected account.",
    ),
    "not_found": Unblock(
        None,
        "The provider says this does not exist for this account — usually a moved, deleted or "
        "differently-owned item.",
    ),
    "quota_exhausted": Unblock(
        "retry_later",
        "The provider's daily allowance for this account is used up. It resets, and retrying "
        "after it does will work.",
    ),
    # ── Catalog adapters ─────────────────────────────────────────────────────
    "input_unresolvable": Unblock(
        None,
        "We could not work out what this address points at. A direct link to the channel, "
        "show or profile page resolves it.",
    ),
    "feed_unreachable": Unblock(
        "retry",
        "The feed did not answer. Retrying is the first thing to try; a feed that stays down "
        "usually moved address.",
    ),
    "feed_unparseable": Unblock(
        None,
        "The feed answered but is not valid feed XML. The publisher's own feed page usually "
        "carries a second, working address.",
    ),
    "site_unreachable": Unblock(
        "retry",
        "The site did not answer at all. Retrying is the first thing to try.",
    ),
}


def unblock_for(error_class: str) -> Unblock:
    """The lawful route for a class, or an honest blank when we do not know one."""
    return _ROUTES.get(error_class, _NOTHING)
