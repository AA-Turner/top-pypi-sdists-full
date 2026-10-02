"""The ONE normalizer for DataForSEO ``serp.google.organic.advanced``.

Registered in ``DataForSeoAdapter``'s default normalizer map for
``SERP_ORGANIC_OPERATION``. Two payload shapes arrive on this operation:

* **prospect-tagged** tasks (``matrx_seo.serp_prospecting``) — routed to
  ``normalize_serp_prospect_payload`` exactly as the adapter did before this
  module existed, including the ``site_id`` requirement. SERP prospecting must
  keep working at every commit; ``tests/test_openseo_core_registration.py``
  pins it.
* **untagged** tasks — the organic rank snapshot (OPENSEO-TOOLS-SPEC §5.3,
  Lane B): one ``SerpSnapshotObservation`` per task, every item on the page
  kept in provider order with its ``absolute_rank``, and the ORGANIC rank
  **counted here, over organic items only**. The provider's own ``rank_group``
  is never trusted for it: ads, a featured snippet, a local pack or a
  People-also-ask box above the first blue link change ``rank_absolute`` and
  must never change the organic position a person is told.

The counting is a pure function (:func:`serp_rows`) so the reader of a stored
payload (``aidream/services/seo/serp_check.py``) gets exactly the ranks the
persisted snapshot carries — one computation, two readers.

A snapshot is keyword evidence, never tracking: its identity request carries
the engine, and ``OrmSeoIdentityResolver`` mints a ``rank_target`` only when
the REQUEST names a site. An ad-hoc ``serp_check`` sends no ``site_id``, so a
look never enrols a keyword in the paid tracking portfolio.
"""

from __future__ import annotations

from datetime import UTC
from typing import Any
from urllib.parse import urlparse

from ...contracts import (
    NormalizationContext,
    ProviderResponse,
    SeoIdentityRequest,
    SeoObservation,
    SerpResultObservation,
    SerpSnapshotObservation,
)
from .serp_prospect import is_prospect_payload, normalize_serp_prospect_payload

#: The one item type that is an organic listing. A featured snippet, a local
#: pack, a video carousel or an ad is not "a blue link", so it takes no organic
#: position (Google's own organic count, and Ahrefs'/Semrush's).
ORGANIC_TYPE = "organic"

#: "No Search Results." — the search RAN and returned nothing. A correct empty
#: answer (the target is not in the results), never a failure.
NO_RESULTS_STATUS = 40102
OK_STATUS = 20000


class SerpTaskFailedError(RuntimeError):
    """A SERP task the provider did not complete — the lookup failed, so the
    position is unknown. Carries the provider's own code and message."""

    def __init__(self, keyword: str, status_code: object, status_message: object) -> None:
        self.keyword = keyword
        self.status_code = status_code
        self.status_message = status_message
        super().__init__(
            f"DataForSEO SERP task for {keyword!r} failed: {status_code} {status_message}"
        )


def _domain_of(item: dict[str, Any]) -> str | None:
    domain = str(item.get("domain") or "").strip().lower()
    url = str(item.get("url") or "").strip()
    if not domain and url:
        domain = (urlparse(url).netloc or "").lower()
    domain = domain.split("@")[-1].split(":")[0].removeprefix("www.").rstrip(".")
    return domain or None


def _text(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _int(value: Any) -> int | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def serp_rows(result: dict[str, Any]) -> list[SerpResultObservation]:
    """Every item of one SERP result, in page order, with the organic rank
    COUNTED over organic items only.

    Page order is ``rank_absolute`` (the provider's position on the whole page);
    items without it keep their payload order after the ranked ones. The first
    organic item is organic #1 whatever sits above it.
    """
    items = result.get("items") or []
    if not isinstance(items, list):
        raise ValueError("DataForSEO SERP result.items must be a list")
    indexed = [(index, item) for index, item in enumerate(items) if isinstance(item, dict)]
    indexed.sort(
        key=lambda pair: (
            _int(pair[1].get("rank_absolute")) is None,
            _int(pair[1].get("rank_absolute")) or 0,
            pair[0],
        )
    )
    rows: list[SerpResultObservation] = []
    organic = 0
    for position, (_index, item) in enumerate(indexed, start=1):
        result_type = str(item.get("type") or "unknown")
        organic_rank: int | None = None
        if result_type == ORGANIC_TYPE:
            organic += 1
            organic_rank = organic
        absolute = _int(item.get("rank_absolute"))
        rows.append(
            SerpResultObservation(
                result_type=result_type,
                organic_rank=organic_rank,
                absolute_rank=absolute if absolute is not None else position,
                url=_text(item.get("url")),
                domain=_domain_of(item),
                title=_text(item.get("title")),
                snippet=_text(item.get("description")),
                extras={
                    key: item[key]
                    for key in ("rank_group", "breadcrumb", "is_featured_snippet", "position")
                    if item.get(key) is not None
                },
            )
        )
    return rows


def task_outcome(task: dict[str, Any]) -> tuple[str, dict[str, Any] | None]:
    """``("ok", result)`` / ``("empty", None)`` for one provider task; raises
    :class:`SerpTaskFailedError` for a task the provider did not complete."""
    data = task.get("data") if isinstance(task.get("data"), dict) else {}
    keyword = str(data.get("keyword") or "").strip()
    status = task.get("status_code")
    if status == NO_RESULTS_STATUS:
        return "empty", None
    if status != OK_STATUS:
        raise SerpTaskFailedError(keyword, status, task.get("status_message"))
    results = task.get("result")
    if not isinstance(results, list):
        raise ValueError("DataForSEO SERP task.result must be a list")
    first = next((r for r in results if isinstance(r, dict)), None)
    if first is None:
        return "empty", None
    return "ok", first


def snapshot_rows_from_payload(raw: dict[str, Any]) -> list[SerpResultObservation]:
    """The rows of the FIRST task of a stored one-query payload (serp_check runs
    one query per run). Raises :class:`SerpTaskFailedError` when that task failed."""
    tasks = raw.get("tasks") if isinstance(raw, dict) else None
    if not isinstance(tasks, list) or not tasks or not isinstance(tasks[0], dict):
        raise ValueError("DataForSEO SERP payload tasks must be a non-empty list")
    outcome, result = task_outcome(tasks[0])
    return serp_rows(result) if outcome == "ok" and result is not None else []


async def _normalize_rank_snapshot(
    raw: dict[str, Any],
    response: ProviderResponse,
    context: NormalizationContext,
) -> list[SeoObservation]:
    tasks = raw.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        raise ValueError("DataForSEO SERP payload tasks must be a non-empty list")
    requested = context.request.settings.get("tasks") or []
    observed_at = response.fetched_at
    if observed_at.tzinfo is None:
        observed_at = observed_at.replace(tzinfo=UTC)
    observations: list[SeoObservation] = []
    for index, task in enumerate(tasks):
        if not isinstance(task, dict):
            raise ValueError("DataForSEO SERP tasks must contain objects")
        data = (
            dict(requested[index])
            if index < len(requested) and isinstance(requested[index], dict)
            else {}
        )
        if isinstance(task.get("data"), dict):
            data.update(task["data"])
        keyword = str(data.get("keyword") or "").strip()
        if not keyword:
            raise ValueError("DataForSEO SERP task carries no keyword")
        outcome, result = task_outcome(task)  # a failed task fails the run, loudly
        rows = serp_rows(result) if outcome == "ok" and result is not None else []
        language = str(data.get("language_code") or "en")
        device = str(data.get("device") or "desktop")
        identity = await context.resolve_identity(
            SeoIdentityRequest(
                keyword=keyword,
                language=language,
                engine="google",
                device=device,
                search_type="organic",
            )
        )
        type_counts: dict[str, int] = {}
        for row in rows:
            type_counts[row.result_type] = type_counts.get(row.result_type, 0) + 1
        observations.append(
            SerpSnapshotObservation(
                keyword_id=identity.keyword_id,
                rank_target_id=identity.rank_target_id,
                location_id=identity.location_id,
                engine="google",
                language=language,
                device=device,
                search_type="organic",
                observed_at=observed_at,
                query_settings={
                    "provider": "dataforseo",
                    "keyword": keyword,
                    "location_code": data.get("location_code"),
                    "language_code": language,
                    "depth": data.get("depth"),
                    "device": device,
                    "outcome": outcome,
                    "check_url": (result or {}).get("check_url"),
                    "provider_datetime": (result or {}).get("datetime"),
                    "se_results_count": (result or {}).get("se_results_count"),
                    "items_count": (result or {}).get("items_count"),
                    "organic_count": type_counts.get(ORGANIC_TYPE, 0),
                    "external_task_id": task.get("id"),
                },
                serp_features={
                    "item_types": (result or {}).get("item_types") or [],
                    "type_counts": type_counts,
                },
                results=rows,
            )
        )
    return observations


async def normalize_serp_organic(
    response: ProviderResponse,
    context: NormalizationContext,
) -> list[SeoObservation]:
    raw = response.raw
    if isinstance(raw, dict) and is_prospect_payload(raw):
        site_id = context.request.site_id
        if not site_id:
            raise ValueError("SERP prospecting collections must carry site_id")
        return list(
            normalize_serp_prospect_payload(
                raw=raw,
                site_id=site_id,
                fetched_at=response.fetched_at,
            )
        )
    if not isinstance(raw, dict):
        raise TypeError("DataForSEO SERP response must be an object")
    return await _normalize_rank_snapshot(raw, response, context)


__all__ = [
    "NO_RESULTS_STATUS",
    "ORGANIC_TYPE",
    "SerpTaskFailedError",
    "normalize_serp_organic",
    "serp_rows",
    "snapshot_rows_from_payload",
    "task_outcome",
]
