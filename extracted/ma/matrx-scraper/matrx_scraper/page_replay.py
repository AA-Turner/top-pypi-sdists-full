"""Page fetch replay: a page's answer is a provider answer, recorded once and served again exactly.

A side-by-side proof runs the SAME read twice (the code path, then the workflow) against live websites; a page
that rotates its links, a site that answers a different block page per request, or a signed image URL made the
two copies differ for reasons that are the website's, not the engines' (L7i, 2026-11-09). Like an AI or search
answer, a page answer can be recorded on the first side and replayed to the second, so a replay pair compares
engines and not websites.

ONE seam for every reader: the two fetch entries both engines use — :func:`matrx_scraper.scraper.fetch_normally_with_proxy`
(``kind="http"``) and :func:`matrx_scraper.browser_lane.render_in_browser_lane` (``kind="browser"``) — pass through
:func:`replayed`, and so does a Brave search (:func:`matrx_scraper.search.search.async_brave_search`, ``kind="search"``,
the "url" being every search parameter as sent). The HOST decides when a fetch replays (this package never imports it): it registers the
``page_replay`` ext, an object with

* ``async lookup(kind, url) -> dict | None`` — the recorded answer, or None (= fetch live);
* ``async record(kind, url, answer) -> None`` — keep a live answer for the next identical fetch.

No ext registered (every normal server) ⇒ every fetch is live and nothing is recorded. A host failure is a live
fetch and a log line, never a broken read.
"""

from __future__ import annotations

import base64
import logging
from collections.abc import Awaitable, Callable
from typing import Any, TypeVar

from matrx_scraper._ext import get_ext, has_ext
from matrx_scraper.utils.proxy import redact_url_secrets

logger = logging.getLogger("matrx_scraper.page_replay")

PAGE_REPLAY_EXT = "page_replay"
T = TypeVar("T")


async def replayed(kind: str, url: str, live: Callable[[], Awaitable[T]], *,
                   to_answer: Callable[[T], Any], from_answer: Callable[[Any], T]) -> T:
    """``live()``'s answer, or the host's recorded answer for (kind, url); a live answer is offered for recording."""
    if not has_ext(PAGE_REPLAY_EXT):
        return await live()
    host = get_ext(PAGE_REPLAY_EXT)
    try:
        answer = await host.lookup(kind, url)
    except Exception as exc:  # noqa: BLE001 — a replay store miss is a live fetch, never a broken read
        logger.warning(
            "[PAGE REPLAY] lookup failed for %s %s (%s) — fetching live", kind, redact_url_secrets(url), redact_url_secrets(exc)
        )
        answer = None
    if answer is not None:
        return from_answer(answer)
    result = await live()
    try:
        await host.record(kind, url, to_answer(result))
    except Exception as exc:  # noqa: BLE001
        logger.warning("[PAGE REPLAY] record failed for %s %s (%s)", kind, redact_url_secrets(url), redact_url_secrets(exc))
    return result


# --- an HTTP fetch's answer (``matrx_scraper.scraper.Response``) ------------------------------------------------

_ENUM_FIELDS = ("request_type", "content_type", "failed_primary_reason", "cms_primary", "firewall")


def response_answer(response: Any) -> dict[str, Any] | None:
    """Everything the fetch answered (status, headers, body, content type, final url, the fetch's own reading of
    them), as JSON. The parsed soups are not answers: nothing downstream reads them."""
    import enum

    if response is None:
        return None

    def plain(value: Any) -> Any:
        return value.value if isinstance(value, enum.Enum) else value

    out: dict[str, Any] = {}
    for name, value in vars(response).items():
        if name in ("selectolax_soup", "soup"):
            continue
        if name == "content_bytes":
            out[name] = base64.b64encode(value).decode("ascii") if value else None
        elif name == "failed_reasons":
            out[name] = [[[plain(k), v] for k, v in r.items()] for r in value or []]
        elif name in ("cms_other",):
            out[name] = [plain(v) for v in value or []]
        else:
            out[name] = plain(value)
    return out


def answer_response(answer: dict[str, Any] | None) -> Any:
    """The ``Response`` a recorded answer was."""
    from matrx_scraper.scraper import CMS, ContentType, FailureReason, Firewall, RequestType, Response

    if answer is None:
        return None
    kinds = {"request_type": RequestType, "content_type": ContentType, "failed_primary_reason": FailureReason,
             "cms_primary": CMS, "firewall": Firewall}
    fields = dict(answer)
    for name, cls in kinds.items():
        if fields.get(name) is not None:
            fields[name] = cls(fields[name])
    fields["cms_other"] = [CMS(v) for v in fields.get("cms_other") or []]
    fields["failed_reasons"] = [{FailureReason(k): v for k, v in r} for r in fields.get("failed_reasons") or []]
    raw = fields.get("content_bytes")
    fields["content_bytes"] = base64.b64decode(raw) if raw else None
    known = set(Response.__dataclass_fields__)
    return Response(**{k: v for k, v in fields.items() if k in known})
