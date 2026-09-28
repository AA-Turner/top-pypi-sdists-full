"""The landing hook — how a page this package scraped becomes a Source.

SOURCE-CONVERGENCE §3 (common-docs/projects/knowledge-system/SOURCE-CONVERGENCE.md). Every
acquired page becomes ONE ``docproc.processed_documents`` row through the host's landing door.
This package may not import that host (``scripts/check_package_boundaries.py``), so the door is
an injected extension point, the same mechanism as the page cache:

    from matrx_scraper._ext import configure_ext
    configure_ext(source_landing=<async (landing: dict) -> landed: dict>)

``landing`` is the door's wire shape (``SourceLanding``: ``source_kind``, ``canonical_identity``,
``portions``, ``structured``, ``provenance``, ``organization_id`` …) and ``landed`` is its answer
(``LandedSource``: ``processed_document_id``, ``source_id``, ``notices`` …). aidream wires an
in-process hook; the separately hosted scraper service wires an HTTP one
(``matrx_scraper.server.source_landing_http``).

🚨 THERE IS NO SILENT FALLBACK. :func:`land_result` RAISES :class:`SourceLandingNotConfigured`
when no hook is registered — a scraper that quietly stopped turning pages into Sources is the
failure this module exists to make impossible. A hook that is wired but FAILS for one page (the
door refused it, the host was unreachable) is announced on that page's result as a notice with
a remedy; the scrape itself still answers.

``cache.set`` never lands: landing happens at the RESULT BOUNDARY of each route, after the parse
succeeded and before the response, whether or not the cache was used.
"""

from __future__ import annotations

import base64
import json
import logging
from datetime import UTC, datetime
from typing import Any

from matrx_scraper._ext import get_ext, has_ext

logger = logging.getLogger("matrx_scraper.source_landing")

#: The ``configure_ext`` key.
SOURCE_LANDING_EXT = "source_landing"

#: What ``capture_method`` a scrape's engine/egress maps to (the door's closed set).
_ENGINE_METHOD = {"http": "http", "browser": "browser"}


class SourceLandingNotConfigured(RuntimeError):
    """No landing hook is registered — a wiring defect in the host, never a per-page failure."""

    def __init__(self) -> None:
        super().__init__(
            "matrx-scraper has no Source landing hook registered, so the page it just read cannot "
            "become a Source. Remedy: the host must call "
            "matrx_scraper.configure_ext(source_landing=<async (landing: dict) -> dict>) at "
            "startup — aidream wires it in package_integration._configure_matrx_scraper, the "
            "hosted scraper service in server/app.py's lifespan."
        )


class SourceLandingFailed(RuntimeError):
    """The hook ran and this one page did not land — a code, a sentence, and a remedy."""

    def __init__(self, code: str, message: str, *, remedy: str = "") -> None:
        self.code = code
        self.message = message
        self.remedy = remedy
        super().__init__(message)

    def as_notice(self) -> dict[str, str]:
        return {"code": self.code, "message": self.message, "remedy": self.remedy}


async def land_result(landing: dict[str, Any]) -> dict[str, Any]:
    """Hand one ``SourceLanding`` to the host's door and return its ``LandedSource``.

    Raises :class:`SourceLandingNotConfigured` when the host registered no hook.
    """
    if not has_ext(SOURCE_LANDING_EXT):
        raise SourceLandingNotConfigured()
    hook = get_ext(SOURCE_LANDING_EXT)
    landed = await hook(landing)
    if not isinstance(landed, dict) or not landed.get("processed_document_id"):
        raise SourceLandingFailed(
            "landing_answer_malformed",
            "The page was read, but the landing answered without a Source id, so it cannot be "
            "found in your Sources.",
            remedy="report_it",
        )
    return landed


def _get(result: Any, name: str) -> Any:
    if isinstance(result, dict):
        return result.get(name)
    return getattr(result, name, None)


def capture_method_of(result: Any) -> str:
    """How this page was obtained, in the door's vocabulary."""
    if _get(result, "egress") == "residential":
        return "residential"
    engine = str(_get(result, "engine") or "")
    if engine in _ENGINE_METHOD:
        return _ENGINE_METHOD[engine]
    # A cache hit: the rung that originally read it, else the plain reader.
    for step in reversed(list(_get(result, "rung_trail") or [])):
        rung = str((step or {}).get("rung") or "")
        if (step or {}).get("ok") and rung in _ENGINE_METHOD:
            return _ENGINE_METHOD[rung]
    return "http"


def _clean_title(value: Any) -> str:
    return " ".join(str(value).split()) if isinstance(value, str) else ""


def source_name_of(result: Any, url: str) -> str:
    """What a person reads as the Source's name: the page's title, else its host and path —
    never the raw URL (scheme, query string and tracking parameters are noise in a list).

    The title is looked for where each producer puts it: a ``ScrapeResult``'s ``title``, a raw
    ``parse_html`` dict's ``overview.page_title`` (the agent read path hands the parse through
    as-is) and the page's own metadata (``og:title``/``title``)."""
    overview = _get(result, "overview") or {}
    meta = overview.get("metadata") if isinstance(overview, dict) else None
    candidates = [
        _get(result, "title"),
        _get(result, "page_title"),
        overview.get("page_title") if isinstance(overview, dict) else None,
    ]
    if isinstance(meta, dict):
        candidates += [meta.get("title"), meta.get("og_title"), meta.get("og:title")]
    for candidate in candidates:
        title = _clean_title(candidate)
        if title:
            return title[:500]
    from urllib.parse import urlsplit

    parts = urlsplit(url if "//" in url else f"//{url}")
    host = (parts.hostname or "").removeprefix("www.")
    path = (parts.path or "").rstrip("/")
    return (f"{host}{path}" or url or "Untitled page")[:500]


#: What a scraper-landed Source's original file is: the scraper's own ``fetch_results`` envelope
#: (frontend ``ScrapedResultsEnvelope``) holding exactly this page's full result, so a saved Source
#: reopens as it looked when captured — organized data, text, structured data, markdown, images,
#: links, metadata, SEO, hashes — never as a plain-text dump. The page's raw HTML rides along in
#: ``metadata.raw_html`` when the scrape had it (a cache hit does not).
SCRAPER_ENVELOPE_SHAPE = "scraper_fetch_results.v1"


def scraper_page_envelope(result: Any) -> dict[str, Any]:
    """``{"__kind", "type": "fetch_results", "metadata": {...}, "results": [<the page>]}`` — the same
    envelope the scraper streams, for this one page, JSON-safe."""
    import json as _json

    if isinstance(result, dict):
        page = {k: v for k, v in result.items() if k not in ("raw_html", "raw_body")}
    elif hasattr(result, "to_dict"):
        page = result.to_dict()
    else:
        page = {k: v for k, v in vars(result).items() if k not in ("raw_html", "raw_body")}
    raw_html = _get(result, "raw_html")
    has_html = isinstance(raw_html, str) and bool(raw_html.strip())
    envelope: dict[str, Any] = {
        "__kind": SCRAPER_ENVELOPE_SHAPE,
        "type": "fetch_results",
        "metadata": {
            "shape": SCRAPER_ENVELOPE_SHAPE,
            "raw_html_kept": has_html,
            **({"raw_html": raw_html} if has_html else {}),
        },
        "results": [page],
    }
    return _json.loads(_json.dumps(envelope, default=str))


def page_landing(
    result: Any,
    *,
    organization_id: str,
    user_id: str,
    origin_client: str,
    capture_method: str | None = None,
    keep: bool = False,
    visibility: str = "internal",
    attach_to: list[dict[str, Any]] | None = None,
) -> dict[str, Any] | None:
    """The door's ``SourceLanding`` for one successful server parse, or ``None`` when the parse
    produced no words (the caller announces that; the door would refuse it as
    ``nothing_captured``)."""
    from matrx_scraper.canonical import canonical_url
    from matrx_scraper.portions import from_parsed_page, structured_from_parsed_page

    portions = from_parsed_page(result)
    if not portions:
        return None
    url = str(_get(result, "response_url") or _get(result, "url") or "")
    envelope = scraper_page_envelope(result)
    original = {
        "bytes_b64": base64.b64encode(json.dumps(envelope, default=str).encode("utf-8")).decode("ascii"),
        "file_id": None,
        "mime_type": "application/json",
    }
    engine = str(_get(result, "engine") or "") or None
    return {
        "source_kind": "scrape_parsed_page",
        "source_id": None,
        "canonical_identity": canonical_url(url),
        "name": source_name_of(result, url),
        "mime_type": "text/html",
        "portions": portions,
        "original": original,
        "structured": {**structured_from_parsed_page(result), "original_shape": SCRAPER_ENVELOPE_SHAPE},
        "provenance": {
            "origin_client": origin_client,
            "capture_method": capture_method or capture_method_of(result),
            "captured_by_rung": engine if engine != "cache" else None,
            "rung_trail": list(_get(result, "rung_trail") or []),
            "captured_at": str(_get(result, "scraped_at") or datetime.now(UTC).isoformat()),
            "final_url": url or None,
            "user_id": user_id,
        },
        "attach_to": list(attach_to or []),
        "content_already_clean": False,
        "keep": bool(keep),
        "visibility": visibility,
        "organization_id": organization_id,
    }


def _notice(code: str, message: str, remedy: str) -> dict[str, str]:
    return {"code": code, "message": message, "remedy": remedy}


async def land_page_result(
    result: Any,
    *,
    organization_id: str | None,
    user_id: str | None,
    origin_client: str,
    capture_method: str | None = None,
    keep: bool = False,
    visibility: str = "internal",
    attach_to: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    """Land one scrape result at a route's result boundary.

    Returns ``{"processed_document_id", "source_id", "notices"}`` — the id is ``None`` and the
    notices say why when the page did not land. Raises :class:`SourceLandingNotConfigured` when
    no hook is wired (never turned into a notice: it is the host's defect, not the page's).
    """
    if not has_ext(SOURCE_LANDING_EXT):
        raise SourceLandingNotConfigured()
    outcome: dict[str, Any] = {"processed_document_id": None, "source_id": None, "notices": []}
    if not _get(result, "success"):
        return outcome
    if not user_id:
        outcome["notices"].append(
            _notice(
                "source_needs_a_person",
                "This page was read but not saved as a Source: a Source always belongs to a person, "
                "and this request named nobody.",
                "call_it_signed_in_or_name_the_acting_user",
            )
        )
        return outcome
    if not organization_id:
        outcome["notices"].append(
            _notice(
                "source_needs_an_organization",
                "This page was read but not saved as a Source because the request named no "
                "organization.",
                "send_the_x_organization_id_header",
            )
        )
        return outcome
    landing = page_landing(
        result,
        organization_id=organization_id,
        user_id=user_id,
        origin_client=origin_client,
        capture_method=capture_method,
        keep=keep,
        visibility=visibility,
        attach_to=attach_to,
    )
    if landing is None:
        outcome["notices"].append(
            _notice(
                "nothing_captured",
                "This page was read but had no text to keep, so it was not saved as a Source.",
                "capture_the_page_again",
            )
        )
        return outcome
    try:
        landed = await land_result(landing)
    except SourceLandingNotConfigured:
        raise
    except SourceLandingFailed as exc:
        logger.warning("source landing refused for %s: %s", landing["canonical_identity"], exc.message)
        outcome["notices"].append(exc.as_notice())
        return outcome
    except Exception as exc:  # noqa: BLE001 — announced on the result, never swallowed
        logger.exception("source landing failed for %s", landing["canonical_identity"])
        outcome["notices"].append(
            _notice(
                "source_not_landed",
                "This page was read but could not be saved as a Source "
                f"({type(exc).__name__}: {str(exc)[:200]}).",
                "scrape_it_again",
            )
        )
        return outcome
    outcome["processed_document_id"] = landed.get("processed_document_id")
    outcome["source_id"] = landed.get("source_id")
    outcome["kept"] = bool(landed.get("kept"))
    outcome["notices"] = list(landed.get("notices") or [])
    return outcome


def crawl_snapshot_landing(
    *,
    markdown: str | None,
    url: str,
    title: str | None,
    page_id: str,
    body_file_id: str | None,
    body_mime_type: str | None,
    organization_id: str,
    user_id: str,
    captured_at: str | None = None,
    final_url: str | None = None,
    engine: str | None = None,
    snapshot_id: str | None = None,
    session_id: str | None = None,
    site_id: str | None = None,
    origin_client: str = "crawl",
) -> dict[str, Any] | None:
    """The door's ``SourceLanding`` for one marketing-crawl snapshot (SOURCE-CONVERGENCE §4.7).

    A ``web_page`` Source whose origin row is the ``web.page`` and whose text is the snapshot's
    markdown, portioned by :func:`matrx_scraper.portions.from_markdown`. The original is the
    snapshot's body file BY ID (``original.file_id``), so the door stores no second S3 copy.
    Always ``internal``: crawl output belongs to the organization, never one person (the same
    rule ``CanonicalBodyPersister._write_artifact`` enforces on the artifact itself). Never kept:
    a crawl is not a person's signal, so intelligence waits for one (``on_signal``).

    Filed under its ``web_site`` (``crawled_page``) with ``signal: False``: the edge is structural,
    never a Keep — a person's filing starts paid intelligence (§3.2 step 9), a crawl's does not.

    Returns ``None`` when the markdown has no words (nothing to land)."""
    from matrx_scraper.canonical import canonical_url
    from matrx_scraper.portions import from_markdown

    portions = from_markdown(markdown)
    if not portions:
        return None
    original = (
        {"bytes_b64": None, "file_id": str(body_file_id), "mime_type": body_mime_type or "text/html"}
        if body_file_id
        else None
    )
    structured = {
        k: v
        for k, v in {
            "web_page_id": page_id,
            "web_snapshot_id": snapshot_id,
            "crawl_session_id": session_id,
            "web_site_id": site_id,
        }.items()
        if v
    }
    return {
        "source_kind": "web_page",
        "source_id": str(page_id),
        "canonical_identity": canonical_url(url),
        "name": source_name_of({"title": title}, url),
        "mime_type": "text/markdown",
        "portions": portions,
        "original": original,
        "structured": structured or None,
        "provenance": {
            "origin_client": origin_client,
            "capture_method": "browser" if engine == "browser" else "http",
            "captured_by_rung": engine or None,
            "rung_trail": [],
            "captured_at": captured_at or datetime.now(UTC).isoformat(),
            "final_url": final_url or url or None,
            "user_id": user_id,
        },
        "attach_to": (
            [{"entity_type": "web_site", "entity_id": str(site_id), "label": "crawled_page", "signal": False}]
            if site_id
            else []
        ),
        "content_already_clean": False,
        "keep": False,
        "visibility": "internal",
        "organization_id": organization_id,
    }


def stamp_page(page: dict[str, Any], outcome: dict[str, Any]) -> dict[str, Any]:
    """Put a landing outcome on a result payload: ``processed_document_id``, ``source_id``,
    ``notices`` (appended to any the payload already carries)."""
    page["processed_document_id"] = outcome.get("processed_document_id")
    page["source_id"] = outcome.get("source_id")
    if "kept" in outcome:
        page["kept"] = bool(outcome["kept"])
    page["notices"] = [*list(page.get("notices") or []), *list(outcome.get("notices") or [])]
    return page


__all__ = [
    "SOURCE_LANDING_EXT",
    "SourceLandingFailed",
    "SourceLandingNotConfigured",
    "capture_method_of",
    "crawl_snapshot_landing",
    "land_page_result",
    "land_result",
    "page_landing",
    "source_name_of",
    "stamp_page",
]
