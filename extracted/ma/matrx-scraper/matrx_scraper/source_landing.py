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


def page_landing(
    result: Any,
    *,
    organization_id: str,
    user_id: str,
    origin_client: str,
    capture_method: str | None = None,
    keep: bool = False,
    visibility: str = "personal",
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
    raw_html = _get(result, "raw_html")
    original = None
    if isinstance(raw_html, str) and raw_html.strip():
        original = {
            "bytes_b64": base64.b64encode(raw_html.encode("utf-8", errors="replace")).decode("ascii"),
            "file_id": None,
            "mime_type": "text/html",
        }
    engine = str(_get(result, "engine") or "") or None
    return {
        "source_kind": "scrape_parsed_page",
        "source_id": None,
        "canonical_identity": canonical_url(url),
        "name": str(_get(result, "title") or url)[:500],
        "mime_type": "text/html",
        "portions": portions,
        "original": original,
        "structured": structured_from_parsed_page(result),
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
    visibility: str = "personal",
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
    outcome["notices"] = list(landed.get("notices") or [])
    return outcome


def stamp_page(page: dict[str, Any], outcome: dict[str, Any]) -> dict[str, Any]:
    """Put a landing outcome on a result payload: ``processed_document_id``, ``source_id``,
    ``notices`` (appended to any the payload already carries)."""
    page["processed_document_id"] = outcome.get("processed_document_id")
    page["source_id"] = outcome.get("source_id")
    page["notices"] = [*list(page.get("notices") or []), *list(outcome.get("notices") or [])]
    return page


__all__ = [
    "SOURCE_LANDING_EXT",
    "SourceLandingFailed",
    "SourceLandingNotConfigured",
    "capture_method_of",
    "land_page_result",
    "land_result",
    "page_landing",
    "stamp_page",
]
