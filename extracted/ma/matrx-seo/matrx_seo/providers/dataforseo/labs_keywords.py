"""Normalizer for the DataForSEO Labs keyword operations (and Google Ads
``keywords_for_keywords``) into ``KeywordMarketObservation``.

OpenSEO Wave 1 Lane A owns this module (OPENSEO-TOOLS-SPEC §5.1). The core
registered it in ``DataForSeoAdapter``'s default normalizer map for every
operation in ``NORMALIZED_OPERATIONS``; this module never edits ``adapter.py``.

Two doors, one reading of the payload:

* :func:`parse_keyword_rows` — PURE. Reads a provider response body into
  :class:`ParsedKeywordRow` values: phrase, market, volume, CPC, competition,
  monthly searches, provider difficulty and provider intent. The keyword tool
  reads a run's stored raw payload through it, so what the agent is shown and
  what was persisted can never be two readings of the same bytes.
* :func:`normalize_labs_keywords` — the normalizer the collection service runs:
  the parsed rows become ``KeywordMarketObservation`` upserts (identity through
  the injected resolver, one ``seo.keyword_market`` row per (keyword, market)).

Field mapping (their method: ``research-data.ts`` at every-app/open-seo@0ffff93):

* Labs ``keyword_info.search_volume / cpc / monthly_searches / low|high_top_of_page_bid``
  map one to one. Labs ``competition`` is a 0-1 float and ``competition_level``
  a word; our columns are Google Ads' shape (``competition`` word,
  ``competition_index`` 0-100), so the float is scaled ×100 and rounded.
* ``keyword_properties.keyword_difficulty`` → ``difficulty`` (0-100). The
  repository writes it under its own newer-or-equal guard, so a later
  volume-only refresh never clears it (§4.1).
* ``search_intent_info.main_intent`` is provider evidence only: it rides in
  ``raw`` and is RETURNED beside our classifier's intent, never stored as ours
  (the classifier owns intent).
* ``related_keywords`` wraps each keyword one level deeper (``item.keyword_data``).
* ``bulk_keyword_difficulty`` items carry ONLY a difficulty; they become
  difficulty-only observations (every volume field ``None``).
* Google Ads ``keywords_for_keywords`` rows are already flat, carry no
  difficulty and no intent. The endpoint has no ``limit`` (it can return
  thousands of suggestions for one flat fee), so the request's
  ``settings.max_items`` — which the live client ignores below one page for a
  non-paginated endpoint — is the number of rows (in the provider's
  search-volume order) this normalizer persists. Unset means every row.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC
from decimal import Decimal, InvalidOperation
from typing import Any

from ...contracts import (
    KeywordMarketObservation,
    MonthlySearch,
    NormalizationContext,
    ProviderResponse,
    SeoIdentityRequest,
    SeoObservation,
)
from .contracts import DataForSeoOperationName

LABS_RELATED = DataForSeoOperationName.LABS_GOOGLE_RELATED_KEYWORDS.value
LABS_SUGGESTIONS = DataForSeoOperationName.LABS_GOOGLE_KEYWORD_SUGGESTIONS.value
LABS_IDEAS = DataForSeoOperationName.LABS_GOOGLE_KEYWORD_IDEAS.value
LABS_OVERVIEW = DataForSeoOperationName.LABS_GOOGLE_KEYWORD_OVERVIEW.value
LABS_BULK_DIFFICULTY = DataForSeoOperationName.LABS_GOOGLE_BULK_KEYWORD_DIFFICULTY.value
ADS_KEYWORDS_FOR_KEYWORDS = DataForSeoOperationName.KEYWORDS_GOOGLE_ADS_KEYWORDS_FOR_KEYWORDS.value
ADS_SEARCH_VOLUME = DataForSeoOperationName.KEYWORDS_GOOGLE_ADS_SEARCH_VOLUME.value

#: Operations whose normalized (KEYWORD_METRICS) collection routes here.
NORMALIZED_OPERATIONS: tuple[str, ...] = (
    LABS_OVERVIEW,
    LABS_IDEAS,
    LABS_SUGGESTIONS,
    LABS_RELATED,
    LABS_BULK_DIFFICULTY,
    ADS_KEYWORDS_FOR_KEYWORDS,
)

#: Operations :func:`parse_keyword_rows` reads. Google Ads ``search_volume`` has
#: its own normalizer (``adapter.normalize_google_ads_search_volume``); its rows
#: are the same flat shape as ``keywords_for_keywords``, so the keyword tool reads
#: a stored search-volume payload through this one parser too.
READABLE_OPERATIONS: tuple[str, ...] = (*NORMALIZED_OPERATIONS, ADS_SEARCH_VOLUME)

#: Labs operations whose ``result[*].items`` rows are keyword rows.
_LABS_ITEM_OPERATIONS = frozenset(
    {LABS_OVERVIEW, LABS_IDEAS, LABS_SUGGESTIONS, LABS_RELATED, LABS_BULK_DIFFICULTY}
)


@dataclass(frozen=True)
class ProviderIntent:
    """The provider's intent label for one keyword — evidence, never ours."""

    label: str
    probability: float | None = None
    foreign: tuple[str, ...] = ()


@dataclass(frozen=True)
class ParsedKeywordRow:
    """One keyword row of one provider response, read and nothing more."""

    phrase: str
    language_code: str
    location_code: int | None
    search_volume: int | None = None
    cpc: Decimal | None = None
    competition: str | None = None
    competition_index: int | None = None
    low_top_of_page_bid: Decimal | None = None
    high_top_of_page_bid: Decimal | None = None
    monthly_searches: tuple[MonthlySearch, ...] = ()
    difficulty: int | None = None
    provider_intent: ProviderIntent | None = None
    task_id: str | None = None
    raw: dict[str, Any] = field(default_factory=dict)


def _decimal(value: Any) -> Decimal | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        return None


def _int(value: Any) -> int | None:
    if value is None or isinstance(value, bool):
        return None
    try:
        return int(round(float(value)))
    except (TypeError, ValueError):
        return None


def _difficulty(value: Any) -> int | None:
    score = _int(value)
    if score is None:
        return None
    return score if 0 <= score <= 100 else None


def _monthly(entries: Any) -> tuple[MonthlySearch, ...]:
    out: list[MonthlySearch] = []
    for entry in entries or []:
        if not isinstance(entry, dict) or not entry.get("year") or not entry.get("month"):
            continue
        out.append(
            MonthlySearch(
                year=int(entry["year"]),
                month=int(entry["month"]),
                search_volume=int(entry.get("search_volume") or 0),
            )
        )
    return tuple(out)


def _intent(info: Any) -> ProviderIntent | None:
    if not isinstance(info, dict):
        return None
    label = info.get("main_intent")
    if not isinstance(label, str) or not label.strip():
        return None
    probability = info.get("probability")
    foreign_raw = info.get("foreign_intent") or ()
    foreign = tuple(str(x) for x in foreign_raw if isinstance(x, str)) if isinstance(
        foreign_raw, list
    ) else ()
    return ProviderIntent(
        label=label.strip().lower(),
        probability=float(probability) if isinstance(probability, int | float) else None,
        foreign=foreign,
    )


def _tasks(raw: Any) -> list[dict[str, Any]]:
    tasks = raw.get("tasks") if isinstance(raw, dict) else None
    return [t for t in tasks or [] if isinstance(t, dict)]


def _labs_row(
    operation: str, item: dict[str, Any], task_data: dict[str, Any], task_id: str | None
) -> ParsedKeywordRow | None:
    if operation == LABS_RELATED:
        item = item.get("keyword_data") if isinstance(item.get("keyword_data"), dict) else {}
    phrase = str(item.get("keyword") or "").strip()
    if not phrase:
        return None
    language = str(item.get("language_code") or task_data.get("language_code") or "en")
    location = _int(item.get("location_code", task_data.get("location_code")))
    if operation == LABS_BULK_DIFFICULTY:
        return ParsedKeywordRow(
            phrase=phrase,
            language_code=language,
            location_code=location,
            difficulty=_difficulty(item.get("keyword_difficulty")),
            task_id=task_id,
            raw=item,
        )
    info = item.get("keyword_info") if isinstance(item.get("keyword_info"), dict) else {}
    props_raw = item.get("keyword_properties")
    props = props_raw if isinstance(props_raw, dict) else {}
    competition_float = info.get("competition")
    competition_index = (
        _int(float(competition_float) * 100)
        if isinstance(competition_float, int | float) and not isinstance(competition_float, bool)
        else None
    )
    level = info.get("competition_level")
    return ParsedKeywordRow(
        phrase=phrase,
        language_code=language,
        location_code=location,
        search_volume=_int(info.get("search_volume")),
        cpc=_decimal(info.get("cpc")),
        competition=str(level) if isinstance(level, str) and level else None,
        competition_index=competition_index,
        low_top_of_page_bid=_decimal(info.get("low_top_of_page_bid")),
        high_top_of_page_bid=_decimal(info.get("high_top_of_page_bid")),
        monthly_searches=_monthly(info.get("monthly_searches")),
        difficulty=_difficulty(props.get("keyword_difficulty")),
        provider_intent=_intent(item.get("search_intent_info")),
        task_id=task_id,
        raw=item,
    )


def _ads_row(
    item: dict[str, Any], task_data: dict[str, Any], task_id: str | None
) -> ParsedKeywordRow | None:
    phrase = str(item.get("keyword") or "").strip()
    if not phrase:
        return None
    competition = item.get("competition")
    return ParsedKeywordRow(
        phrase=phrase,
        language_code=str(item.get("language_code") or task_data.get("language_code") or "en"),
        location_code=_int(item.get("location_code", task_data.get("location_code"))),
        search_volume=_int(item.get("search_volume")),
        cpc=_decimal(item.get("cpc")),
        competition=str(competition) if isinstance(competition, str) and competition else None,
        competition_index=_int(item.get("competition_index")),
        low_top_of_page_bid=_decimal(item.get("low_top_of_page_bid")),
        high_top_of_page_bid=_decimal(item.get("high_top_of_page_bid")),
        monthly_searches=_monthly(item.get("monthly_searches")),
        task_id=task_id,
        raw=item,
    )


def parse_keyword_rows(
    operation: str,
    raw: Any,
    *,
    requested_tasks: list[dict[str, Any]] | None = None,
    max_rows: int | None = None,
) -> list[ParsedKeywordRow]:
    """Every keyword row in one provider response body, in provider order.

    ``requested_tasks`` fills a market the provider echo leaves out (the task's
    own ``data`` wins). ``max_rows`` keeps the first N rows (Google Ads
    ``keywords_for_keywords`` only has no provider-side limit). Raises
    ``ValueError`` for an operation this module does not read."""
    if operation not in READABLE_OPERATIONS:
        raise ValueError(f"{operation} is not a keyword-row operation")
    rows: list[ParsedKeywordRow] = []
    for index, task in enumerate(_tasks(raw)):
        task_data = dict(requested_tasks[index]) if requested_tasks and index < len(
            requested_tasks
        ) and isinstance(requested_tasks[index], dict) else {}
        if isinstance(task.get("data"), dict):
            task_data = {**task_data, **task["data"]}
        task_id = str(task["id"]) if task.get("id") else None
        for result in task.get("result") or []:
            if not isinstance(result, dict):
                continue
            if operation in _LABS_ITEM_OPERATIONS:
                for item in result.get("items") or []:
                    if isinstance(item, dict):
                        row = _labs_row(operation, item, task_data, task_id)
                        if row is not None:
                            rows.append(row)
            else:
                row = _ads_row(result, task_data, task_id)
                if row is not None:
                    rows.append(row)
    if max_rows is not None:
        rows = rows[: max(max_rows, 0)]
    return rows


async def normalize_labs_keywords(
    response: ProviderResponse,
    context: NormalizationContext,
) -> list[SeoObservation]:
    """Labs / Google Ads keyword rows → ``KeywordMarketObservation`` upserts.

    A row with no market (``location_code``) is refused loudly, never guessed —
    the same rule as the Google Ads search-volume normalizer."""
    request = context.request
    settings = request.settings if isinstance(request.settings, dict) else {}
    requested = settings.get("tasks") if isinstance(settings.get("tasks"), list) else None
    max_rows = settings.get("max_items") if request.operation == ADS_KEYWORDS_FOR_KEYWORDS else None
    rows = parse_keyword_rows(
        request.operation,
        response.raw,
        requested_tasks=requested,
        max_rows=int(max_rows) if isinstance(max_rows, int) else None,
    )
    if not rows:
        return []
    for row in rows:
        if row.location_code is None:
            raise ValueError(
                f"DataForSEO {request.operation} row for {row.phrase!r} has no location_code "
                "— refusing to guess a market"
            )
    identities = await context.resolve_identities(
        [SeoIdentityRequest(keyword=row.phrase, language=row.language_code) for row in rows]
    )
    observed_at = response.fetched_at.astimezone(UTC)
    return [
        KeywordMarketObservation(
            keyword_id=identity.keyword_id,
            location_code=int(row.location_code),  # type: ignore[arg-type]
            search_volume=row.search_volume,
            competition=row.competition,
            competition_index=row.competition_index,
            cpc=row.cpc,
            low_top_of_page_bid=row.low_top_of_page_bid,
            high_top_of_page_bid=row.high_top_of_page_bid,
            monthly_searches=list(row.monthly_searches),
            metrics_task_id=row.task_id or response.external_task_id,
            difficulty=row.difficulty,
            raw=row.raw,
            observed_at=observed_at,
        )
        for row, identity in zip(rows, identities, strict=True)
    ]


__all__ = [
    "ADS_KEYWORDS_FOR_KEYWORDS",
    "ADS_SEARCH_VOLUME",
    "LABS_BULK_DIFFICULTY",
    "LABS_IDEAS",
    "LABS_OVERVIEW",
    "LABS_RELATED",
    "LABS_SUGGESTIONS",
    "NORMALIZED_OPERATIONS",
    "READABLE_OPERATIONS",
    "ParsedKeywordRow",
    "ProviderIntent",
    "normalize_labs_keywords",
    "parse_keyword_rows",
]
