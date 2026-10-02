"""AI answer-engine presence (ai_visibility) via DataForSEO's AI Optimization LLM Responses.

AI engines are ENGINES IN THE RANK PORTFOLIO — a `seo.rank_target` with
`engine` chat_gpt|claude|gemini|perplexity and `search_type='ai_answer'`,
whose "keyword" is the tracked prompt. Each check runs the prompt through the
engine with web search on and records:

- the SERP snapshot: every distinct CITATION the answer carried, in first-
  occurrence order (`SerpResultObservation.absolute_rank` = citation ordinal),
  plus the bounded answer text and run metadata in `serp_features`;
- the rank observation: `absolute_rank` = the ordinal of the first citation
  matching the target (result_type `ai_citation`), and `extras.mentioned` =
  whether the answer TEXT names the target (mention ≠ citation — the two
  axes every serious AI-visibility product measures). An unmatched check
  still persists an observation (`match_rule='no_match'`) — in AI share of
  voice, the MISSES are the data.

Wire shape verified live 2026-07-26 against `/v3/ai_optimization/chat_gpt/
llm_responses/live` (see tests/fixtures/dataforseo_llm_responses.json):
result[0] = {items[{type: reasoning|message, sections[{text, annotations
[{title,url}]}]}], model_name, money_spent, web_search, fan_out_queries, ...}.
"""

from __future__ import annotations

import re
from typing import Any
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

from ...contracts import (
    HostBindingRequest,
    NormalizationContext,
    ProviderResponse,
    RankObservation,
    SeoIdentityRequest,
    SeoObservation,
    SerpResultObservation,
    SerpSnapshotObservation,
)
from ...rank_matching import RankMatchTarget, canonicalize_domain, match_rank_url
from .contracts import DataForSeoOperationName

AI_ANSWER_SEARCH_TYPE = "ai_answer"

# Engine token (rank_target.engine / observation.engine) → DFS operation.
AI_ANSWER_OPERATIONS: dict[str, DataForSeoOperationName] = {
    "chat_gpt": DataForSeoOperationName.AI_CHAT_GPT_LLM_RESPONSES,
    "claude": DataForSeoOperationName.AI_CLAUDE_LLM_RESPONSES,
    "gemini": DataForSeoOperationName.AI_GEMINI_LLM_RESPONSES,
    "perplexity": DataForSeoOperationName.AI_PERPLEXITY_LLM_RESPONSES,
}
AI_ANSWER_ENGINES = tuple(AI_ANSWER_OPERATIONS)

# Default model per engine — mainstream + web_search_supported, verified
# against each platform's /models catalog 2026-07-26. Override per task via
# settings.tasks[0].model_name.
# gemini: every 3.x model returned persistent live 50301 rate_limit_exceeded
# from DFS's upstream (2026-08-12); gemini-2.5-flash answers with citations.
DEFAULT_AI_ANSWER_MODELS: dict[str, str] = {
    "chat_gpt": "gpt-5.5",
    "claude": "claude-sonnet-4-6",
    "gemini": "gemini-2.5-flash",
    "perplexity": "sonar",
}

ANSWER_TEXT_PERSIST_CAP = 20_000  # snapshot serp_features.answer_text bound
MAX_OUTPUT_TOKENS = 2_048

# Engines whose live endpoint accepts web-search location fields. Gemini's
# rejects them at task validation ("Invalid Field: 'web_search_country_iso_code'",
# live 2026-08-12) — its web_search has no location controls at all.
AI_ANSWER_LOCATION_ENGINES = frozenset({"chat_gpt", "claude", "perplexity"})


#: Below this many letters and digits an alias is SHORT ("W3C", "IBM", "HP", "3M").
#: A short alias is a real brand only as its owner writes it, so it is matched
#: case-sensitively; this is a classification boundary, not a quality floor.
SHORT_ALIAS_LENGTH = 4


def _is_short(value: str) -> bool:
    return len("".join(re.findall(r"[\w]+", value, flags=re.UNICODE))) < SHORT_ALIAS_LENGTH


def _mention_pattern(value: str) -> re.Pattern[str] | None:
    """Compile a conservative whole-token brand matcher.

    Provider prose is allowed to vary punctuation and whitespace (``A.I.
    Matrx`` versus ``AI Matrx``), but a short substring inside an unrelated
    word is never a mention.  This deliberately stays deterministic: aliases
    are user-owned identity data, not an LLM judgement.

    Long aliases match case-insensitively (the pattern is applied to casefolded
    text). SHORT aliases (fewer than ``SHORT_ALIAS_LENGTH`` letters and digits)
    are where case-insensitive matching produces false positives — "it", "hp",
    "ai" and "us" are ordinary words once case is thrown away — so a short
    alias matches ONLY as written: whole token, case-sensitive, applied to the
    original text. An all-lowercase short alias (typically a bare domain root
    such as "hp" from hp.com) is not how any brand writes its name and is
    refused; the brand's own name ("HP") and its full domain ("hp.com") carry
    the identity. Before 2026-09-28 every short alias was refused outright,
    which silently hid W3C, IBM, HP, AMD and 3M from every ai_visibility read.
    """
    tokens_as_written = re.findall(r"[\w]+", value, flags=re.UNICODE)
    if not tokens_as_written:
        return None
    separator = r"[^\w]*"
    if _is_short(value):
        if value == value.lower():
            return None
        return re.compile(
            r"(?<!\w)" + separator.join(map(re.escape, tokens_as_written)) + r"(?!\w)"
        )
    tokens = [t.casefold() for t in tokens_as_written]
    return re.compile(r"(?<!\w)" + separator.join(map(re.escape, tokens)) + r"(?!\w)")


def answer_mentions_target(answer_text: str, aliases: list[str]) -> tuple[bool, list[str]]:
    """Return whether provider prose names any canonical brand identity.

    The returned terms are the exact aliases considered and are persisted as
    evidence on the rank observation. Callers should supply the brand name,
    site name, explicit aliases, and domain forms.
    """
    accepted: list[str] = []
    seen: set[str] = set()
    for raw in aliases:
        alias = raw.strip()
        key = alias.casefold()
        if not alias or key in seen or _mention_pattern(alias) is None:
            continue
        seen.add(key)
        accepted.append(alias)
    normalized_answer = answer_text.casefold()
    compact_answer = re.sub(r"[^\w]", "", normalized_answer, flags=re.UNICODE)
    for alias in accepted:
        pattern = _mention_pattern(alias)
        # A short alias is matched case-sensitively against the text as written.
        haystack = answer_text if _is_short(alias) else normalized_answer
        if pattern is not None and pattern.search(haystack):
            return True, accepted
        # Initialisms are frequently punctuated ("A.I. Matrx"). Only enable
        # compact matching for multi-token identities; doing it for a single
        # word would turn "Table" into a match inside "injectable".
        tokens = re.findall(r"[\w]+", alias.casefold(), flags=re.UNICODE)
        if len(tokens) > 1 and not _is_short(alias) and "".join(tokens) in compact_answer:
            return True, accepted
    return False, accepted


def engine_for_operation(operation: str) -> str | None:
    for engine, op in AI_ANSWER_OPERATIONS.items():
        if op.value == operation:
            return engine
    return None


def build_ai_answer_task(
    *,
    prompt: str,
    engine: str,
    model_name: str | None = None,
    country_iso: str | None = "US",
    city: str | None = None,
    web_search: bool = True,
) -> dict[str, Any]:
    """One live-endpoint task dict. `force_web_search` is deliberately NOT
    sent — several models reject it (live 40501, 2026-07-26); `web_search`
    alone is honored by every web-search-capable model.

    ``web_search=False`` is the no-web lane (``closed_model``): the model answers
    from what it already knows. The ``web_search_*`` location fields only steer a
    search, so they are not sent when there is no search to steer.
    """
    if engine not in AI_ANSWER_OPERATIONS:
        raise ValueError(
            f"unsupported AI answer engine {engine!r} ({sorted(AI_ANSWER_OPERATIONS)})"
        )
    task: dict[str, Any] = {
        "user_prompt": prompt,
        "model_name": model_name or DEFAULT_AI_ANSWER_MODELS[engine],
        "web_search": bool(web_search),
        "max_output_tokens": MAX_OUTPUT_TOKENS,
    }
    if web_search and engine in AI_ANSWER_LOCATION_ENGINES:
        if country_iso:
            task["web_search_country_iso_code"] = country_iso.upper()
        if city:
            task["web_search_city"] = city
    return task


def _strip_tracking_params(url: str) -> str:
    """Engines append attribution params (`utm_source=openai`) — strip utm_*
    so citation URLs dedupe and match stored page URLs."""
    try:
        parts = urlparse(url)
        query = [(k, v) for k, v in parse_qsl(parts.query) if not k.lower().startswith("utm_")]
        return urlunparse(parts._replace(query=urlencode(query)))
    except ValueError:
        return url


def _domain(url: str | None) -> str | None:
    if not url:
        return None
    try:
        host = urlparse(url).netloc.lower()
    except ValueError:
        return None
    return host.removeprefix("www.") or None


def _extract_answer(raw: Any) -> tuple[str, list[dict[str, str]], dict[str, Any]]:
    """(answer_text, ordered distinct citations [{url,title}], run_meta)."""
    tasks = raw.get("tasks", []) if isinstance(raw, dict) else []
    text_parts: list[str] = []
    citations: list[dict[str, str]] = []
    seen: set[str] = set()
    meta: dict[str, Any] = {}
    for task in tasks:
        if not isinstance(task, dict):
            continue
        for result in task.get("result") or []:
            if not isinstance(result, dict):
                continue
            for key in (
                "model_name",
                "money_spent",
                "web_search",
                "fan_out_queries",
                "input_tokens",
                "output_tokens",
                "datetime",
            ):
                if result.get(key) is not None:
                    meta.setdefault(key, result[key])
            for item in result.get("items") or []:
                if not isinstance(item, dict) or item.get("type") != "message":
                    continue
                for section in item.get("sections") or []:
                    if not isinstance(section, dict):
                        continue
                    if isinstance(section.get("text"), str):
                        text_parts.append(section["text"])
                    for annotation in section.get("annotations") or []:
                        if not isinstance(annotation, dict):
                            continue
                        url = _strip_tracking_params(str(annotation.get("url") or ""))
                        if not url or url in seen:
                            continue
                        seen.add(url)
                        citations.append({"url": url, "title": str(annotation.get("title") or "")})
    return "\n".join(text_parts), citations, meta


async def _resolve_match_target(
    context: NormalizationContext,
) -> tuple[RankMatchTarget | None, str | None]:
    """Match target from the collection's host bindings (site_id / page_id on
    the CollectionRequest) — the same canonical resolution the Brave/SerpAPI
    adapters perform. A site-less collection is observation-only (DEF-25)."""
    request = context.request
    domain: str | None = None
    page_url: str | None = None
    page_id: str | None = None
    if request.site_id:
        site = await context.resolve_host_binding(
            HostBindingRequest(resource_kind="web_site", resource_id=request.site_id)
        )
        domain = canonicalize_domain(site.canonical_url)
    if request.page_id:
        page = await context.resolve_host_binding(
            HostBindingRequest(resource_kind="web_page", resource_id=request.page_id)
        )
        page_domain = canonicalize_domain(page.canonical_url)
        domain = domain or page_domain
        page_url = page.canonical_url
        page_id = page.page_id
    if not domain:
        return None, None
    return (
        RankMatchTarget(canonical_domain=domain, canonical_url=page_url, include_subdomains=True),
        page_id,
    )


async def normalize_ai_answer_response(
    response: ProviderResponse, context: NormalizationContext
) -> list[SeoObservation]:
    request = context.request
    engine = engine_for_operation(request.operation)
    if engine is None:
        raise ValueError(f"{request.operation} is not an AI answer operation")
    tasks = list(request.settings.get("tasks") or [])
    if not tasks or not isinstance(tasks[0], dict):
        raise ValueError("AI answer collections require settings.tasks[0]")
    task = tasks[0]
    prompt = str(task.get("user_prompt") or "").strip()
    if not prompt:
        raise ValueError("AI answer task has no user_prompt")
    country = str(task.get("web_search_country_iso_code") or "") or None
    city = str(task.get("web_search_city") or "") or None

    target, target_page_id = await _resolve_match_target(context)
    identity = await context.resolve_identity(
        SeoIdentityRequest(
            keyword=prompt,
            language="en",
            target_page_id=target_page_id,
            country_code=country,
            city=city,
            engine=engine,
            device="desktop",
            search_type=AI_ANSWER_SEARCH_TYPE,
            target_domain=target.canonical_domain if target else None,
            settings={"model_name": task.get("model_name")},
        )
    )

    answer_text, citations, meta = _extract_answer(response.raw)
    results = [
        SerpResultObservation(
            absolute_rank=ordinal,
            organic_rank=None,
            url=citation["url"],
            domain=_domain(citation["url"]),
            title=citation["title"] or None,
            snippet=None,
            extras={"result_type": "ai_citation"},
        )
        for ordinal, citation in enumerate(citations, start=1)
    ]
    snapshot = SerpSnapshotObservation(
        keyword_id=identity.keyword_id,
        rank_target_id=identity.rank_target_id,
        location_id=identity.location_id,
        engine=engine,
        language="en",
        device="desktop",
        search_type=AI_ANSWER_SEARCH_TYPE,
        observed_at=response.fetched_at,
        query_settings={
            "user_prompt": prompt,
            "model_name": str(meta.get("model_name") or task.get("model_name") or ""),
            "web_search_country_iso_code": country,
            "web_search_city": city,
        },
        serp_features={
            "answer_text": answer_text[:ANSWER_TEXT_PERSIST_CAP],
            "answer_chars": len(answer_text),
            "citation_count": len(citations),
            "fan_out_queries": meta.get("fan_out_queries"),
            "money_spent": meta.get("money_spent"),
            "input_tokens": meta.get("input_tokens"),
            "output_tokens": meta.get("output_tokens"),
        },
        results=results,
    )
    observations: list[SeoObservation] = [snapshot]
    if identity.rank_target_id is None or target is None:
        return observations

    matched_result = None
    matched = None
    for result in results:
        candidate = match_rank_url(result.url, target)
        if candidate is not None:
            matched_result = result
            matched = candidate
            break
    # Mention ≠ citation. Identity aliases come from the host-owned brand
    # profile; domain forms remain a useful baseline for older callers.
    bare_name = target.canonical_domain.rsplit(".", 1)[0].replace("-", " ")
    configured_aliases = request.settings.get("target_aliases")
    aliases = (
        [str(value) for value in configured_aliases] if isinstance(configured_aliases, list) else []
    )
    mentioned, mention_terms = answer_mentions_target(
        answer_text,
        aliases + [target.canonical_domain, bare_name],
    )

    observations.append(
        RankObservation(
            keyword_id=identity.keyword_id,
            rank_target_id=identity.rank_target_id,
            location_id=identity.location_id,
            engine=engine,
            locale=country or "US",
            language="en",
            device="desktop",
            search_type=AI_ANSWER_SEARCH_TYPE,
            matched_domain=matched_result.domain if matched_result else None,
            matched_url=matched_result.url if matched_result else None,
            organic_rank=None,
            absolute_rank=matched_result.absolute_rank if matched_result else None,
            result_type="ai_citation",
            match_rule=(
                matched.match_rule if matched else ("mention_only" if mentioned else "no_match")
            ),
            observed_at=response.fetched_at,
            query_settings=snapshot.query_settings,
            serp_features={"citation_count": len(citations)},
            title=matched_result.title if matched_result else None,
            snippet=None,
            extras={
                "mentioned": mentioned,
                "cited": matched_result is not None,
                "mention_terms": mention_terms,
                "model_name": snapshot.query_settings.get("model_name"),
            },
        )
    )
    return observations


__all__ = [
    "AI_ANSWER_ENGINES",
    "AI_ANSWER_OPERATIONS",
    "AI_ANSWER_SEARCH_TYPE",
    "DEFAULT_AI_ANSWER_MODELS",
    "answer_mentions_target",
    "build_ai_answer_task",
    "normalize_ai_answer_response",
]
