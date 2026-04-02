"""LinkedIn parameter enrichment — resolve LLM-generated names to LinkedIn codes.

Calls the Unipile search/parameters API to map ICP field values
(e.g., "Information Technology") to LinkedIn's internal codes.
Primary validation: LLM-based filtering (filter_candidates prompt).
Fallback: heuristic Jaccard similarity when LLM is unavailable.

Ported from the original AI in Charge IcpParamRetriever.
"""

from __future__ import annotations

import logging
import re
from typing import Any

from .icp_schemas import (
    EnrichedField,
    EnrichedIcpParams,
    EnrichedParam,
    SingleIcp,
)
from .json_repair import parse_json
from .prompt_loader import has_prompt, render_prompt, get_prompt_temperature

logger = logging.getLogger(__name__)

# Field name → Unipile search parameter type
_FIELD_TO_TYPE: dict[str, str] = {
    "job_titles": "JOB_TITLE",
    "industries": "INDUSTRY",
    "locations": "LOCATION",
    "company_locations": "LOCATION",
    "departments": "DEPARTMENT",
}

# Minimum Jaccard similarity for fuzzy matching
_JACCARD_THRESHOLD = 0.5

# Location aliases for common variants
_LOCATION_ALIASES: dict[str, set[str]] = {
    "united states": {"united states", "united states of america", "usa", "us", "u s a", "u s"},
    "united kingdom": {"united kingdom", "uk", "great britain", "gb"},
}

# Industry aliases — maps LLM-generated names to LinkedIn's canonical names.
# Keys are _norm()'d LinkedIn canonical names; values include common LLM variants.
_INDUSTRY_ALIASES: dict[str, set[str]] = {
    "hospital  health care": {
        "hospital  health care", "hospital and health care", "healthcare",
        "health care", "hospitals", "medical", "hospital health care",
    },
    "biotechnology": {"biotechnology", "biotech", "bio technology"},
    "pharmaceuticals": {"pharmaceuticals", "pharma", "pharmaceutical"},
    "financial services": {"financial services", "finserv", "finance"},
    "banking": {"banking", "banks", "bank"},
    "insurance": {"insurance", "insurtech"},
    "investment management": {
        "investment management", "investment", "asset management",
        "wealth management", "portfolio management",
    },
    "information technology and services": {
        "information technology and services", "information technology",
        "it services", "technology", "tech",
    },
    "computer software": {"computer software", "software", "saas"},
    "government administration": {
        "government administration", "government", "govt", "public sector",
        "public administration",
    },
    "defense  space": {
        "defense  space", "defense and space", "defense", "defence",
        "aerospace", "military", "defense space",
    },
    "consumer goods": {"consumer goods", "cpg", "fmcg", "consumer products"},
    "retail": {"retail", "ecommerce", "e commerce", "e-commerce"},
    "e-commerce": {"e-commerce", "ecommerce", "online retail", "retail"},
    "staffing and recruiting": {
        "staffing and recruiting", "staffing", "recruiting", "recruitment",
        "talent acquisition",
    },
    "management consulting": {
        "management consulting", "consulting", "consultancy",
        "professional services",
    },
    "marketing and advertising": {
        "marketing and advertising", "marketing", "advertising",
        "digital marketing",
    },
    "telecommunications": {"telecommunications", "telecom", "telco"},
    "oil  energy": {"oil  energy", "oil and energy", "oil", "energy", "oil energy"},
    "real estate": {"real estate", "property", "realty"},
    "education management": {
        "education management", "education", "edtech", "higher education",
    },
    "automotive": {"automotive", "auto", "cars", "vehicles"},
    "construction": {"construction", "building", "infrastructure"},
    "logistics and supply chain": {
        "logistics and supply chain", "logistics", "supply chain",
        "transportation",
    },
    "media production": {"media production", "media", "entertainment", "film"},
}


async def enrich_icp_linkedin_params(
    icp: SingleIcp,
    get_params_fn: Any,
) -> EnrichedIcpParams:
    """Resolve ICP field values to LinkedIn search parameter codes.

    Args:
        icp: A SingleIcp with LLM-generated field values.
        get_params_fn: Async callable(type, keywords) -> list[{name, code}]
            Typically bound to BackendClient.get_search_params or
            UnipileClient equivalent.

    Returns:
        EnrichedIcpParams with validated LinkedIn codes.
    """
    result = EnrichedIcpParams()
    icp_name = icp.name or "Unknown ICP"

    # Industries
    if icp.industries and icp.industries.include:
        result.industries = await _enrich_field(
            "industries", icp.industries.include, icp.industries.exclude,
            get_params_fn, icp_name,
        )

    # Job titles
    if icp.job_titles and icp.job_titles.include:
        result.job_titles = await _enrich_field(
            "job_titles", icp.job_titles.include, icp.job_titles.exclude,
            get_params_fn, icp_name,
        )

    # Locations
    if icp.locations and icp.locations.include:
        result.locations = await _enrich_field(
            "locations", icp.locations.include, icp.locations.exclude,
            get_params_fn, icp_name,
        )

    # Company locations
    if icp.company_locations and icp.company_locations.include:
        result.company_locations = await _enrich_field(
            "company_locations", icp.company_locations.include,
            icp.company_locations.exclude, get_params_fn, icp_name,
        )

    # Departments
    if icp.departments and icp.departments.include:
        result.departments = await _enrich_field(
            "departments", icp.departments.include, icp.departments.exclude,
            get_params_fn, icp_name,
        )

    return result


async def _enrich_field(
    field_name: str,
    include_values: list[str],
    exclude_values: list[str],
    get_params_fn: Any,
    icp_name: str = "",
) -> EnrichedField:
    """Enrich a single include/exclude field."""
    param_type = _FIELD_TO_TYPE.get(field_name)
    if not param_type:
        return EnrichedField()

    include_params = await _resolve_values(
        param_type, include_values, field_name, get_params_fn, icp_name,
    )
    exclude_params = await _resolve_values(
        param_type, exclude_values, field_name, get_params_fn, icp_name,
    )

    # Remove overlaps: exclude wins
    exclude_codes = {p.code for p in exclude_params}
    include_params = [p for p in include_params if p.code not in exclude_codes]

    return EnrichedField(include=include_params, exclude=exclude_params)


async def _resolve_values(
    param_type: str,
    values: list[str],
    field_name: str,
    get_params_fn: Any,
    icp_name: str = "",
) -> list[EnrichedParam]:
    """Resolve a list of string values to EnrichedParam objects."""
    all_params: list[EnrichedParam] = []
    seen_codes: set[str] = set()

    for value in values:
        try:
            candidates = await get_params_fn(type=param_type, keywords=value)
        except Exception as e:
            logger.warning(f"Search params lookup failed for {param_type}/{value}: {e}")
            continue

        # If primary query returned nothing, retry with each alias (collect all)
        if not candidates:
            aliases = _get_aliases(value, field_name)
            all_alias_candidates: list[dict[str, str]] = []
            for alias in aliases:
                if alias.lower() == value.lower():
                    continue  # Skip the original value we already tried
                try:
                    alias_results = await get_params_fn(type=param_type, keywords=alias)
                    if alias_results:
                        logger.info(
                            f"Alias retry: {param_type}/{value} → "
                            f"'{alias}' returned {len(alias_results)} candidates"
                        )
                        all_alias_candidates.extend(alias_results)
                except Exception:
                    continue
            if all_alias_candidates:
                candidates = all_alias_candidates

        if not candidates:
            # Last resort: try individual words/parts from the value
            # e.g., "Marketing and Advertising" → try "Marketing", "Advertising" separately
            # Collect ALL results across parts (don't break on first hit)
            parts = [w.strip() for w in value.replace(" and ", ",").replace(" & ", ",").split(",") if w.strip()]
            if len(parts) == 1:
                # Single part — try splitting by space for multi-word queries
                parts = [w for w in value.split() if len(w) > 3 and w.lower() not in ("and", "the", "for", "with")]
            all_part_candidates: list[dict[str, str]] = []
            for part in parts:
                if part.lower() == value.lower():
                    continue
                try:
                    part_results = await get_params_fn(type=param_type, keywords=part)
                    if part_results:
                        logger.info(
                            f"Word-split retry: {param_type}/{value} → "
                            f"'{part}' returned {len(part_results)} candidates"
                        )
                        all_part_candidates.extend(part_results)
                except Exception:
                    continue
            if all_part_candidates:
                candidates = all_part_candidates

        if not candidates:
            logger.debug(f"No candidates found for {param_type}/{value} (including alias retries)")
            continue

        # Filter candidates: LLM primary, heuristic fallback
        filtered = await _filter_candidates_with_llm(
            value, candidates, field_name, icp_name,
        )

        for p in filtered:
            code = p.get("code", "")
            if code and code not in seen_codes:
                seen_codes.add(code)
                all_params.append(EnrichedParam(name=p.get("name", ""), code=code))

    return all_params


async def _filter_candidates_with_llm(
    original: str,
    candidates: list[dict[str, str]],
    field_name: str,
    icp_name: str = "",
) -> list[dict[str, str]]:
    """Filter candidates using LLM validation, falling back to heuristics.

    Primary: Uses the filter_candidates prompt for precise LLM-based validation.
    Routes through backend proxy when no local LLM key is available.
    Fallback: Jaccard + alias heuristic when LLM is unavailable or fails.
    """
    if not candidates:
        return []

    # Validate structure first
    valid = _validate_candidates(candidates)
    if not valid:
        return []

    # Try LLM-based filtering if prompt exists
    if has_prompt("filter_candidates"):
        try:
            candidates_str = "\n".join(
                f"- name: {c['name']} | code: {c['code']}" for c in valid
            )
            prompt = render_prompt("filter_candidates", {
                "icp_name": icp_name or "Unknown ICP",
                "field": field_name,
                "original": original,
                "candidates": candidates_str,
            })
            temperature = get_prompt_temperature("filter_candidates")

            # Try local LLM first; if no key, route through backend
            raw = await _llm_generate(
                prompt,
                system="You validate LinkedIn search parameters. Output ONLY JSON.",
                temperature=temperature,
                max_tokens=200,
            )

            if raw:
                result = parse_json(raw, fallback=None)
                keep_codes = result.get("param_codes", [])
                if isinstance(keep_codes, list) and all(isinstance(c, str) for c in keep_codes):
                    kept = [c for c in valid if c["code"] in set(keep_codes)]
                    if kept:
                        logger.info(
                            f"LLM filtered {field_name}/{original}: "
                            f"{len(valid)} → {len(kept)} candidates"
                        )
                        return _dedupe_by_code(kept)
                    # LLM returned empty — fall through to heuristic
                    logger.debug(f"LLM returned no matches for {field_name}/{original}")
        except Exception as e:
            logger.warning(f"LLM filtering failed for {field_name}/{original}: {e}")

    # Fallback to heuristic matching
    return _filter_candidates_heuristic(original, valid, field_name)


async def _llm_generate(
    prompt: str,
    system: str = "",
    temperature: float = 0.0,
    max_tokens: int = 200,
) -> str | None:
    """Generate LLM response via local key or backend proxy.

    Returns None if neither is available.
    """
    from ..config import has_local_llm_key, is_backend_mode

    # 1. Try local LLM key
    if has_local_llm_key():
        from .llm import LLMClient
        client = LLMClient()
        return await client.generate(
            prompt, system=system, temperature=temperature, max_tokens=max_tokens,
        )

    # 2. Route through backend proxy
    if is_backend_mode():
        try:
            from ..linkedin import get_linkedin_client
            from ..linkedin.backend_client import BackendClient

            client = get_linkedin_client()
            if isinstance(client, BackendClient):
                try:
                    result = await client.filter_candidates(prompt)
                    return result
                finally:
                    await client.close()
        except Exception as e:
            logger.debug(f"Backend LLM proxy for filter_candidates failed: {e}")
            return None

    return None


def _filter_candidates_heuristic(
    original: str,
    candidates: list[dict[str, str]],
    field_name: str,
) -> list[dict[str, str]]:
    """Filter Unipile search parameter candidates using heuristic matching.

    Uses exact match → alias match → Jaccard similarity fallback.
    Candidates are expected to be pre-validated.
    """
    if not candidates:
        return []

    o_norm = _norm(original)

    # 1. Exact match (including location + industry aliases)
    aliases = _get_aliases(o_norm, field_name)
    exact = [c for c in candidates if _norm(c["name"]) in aliases]
    if exact:
        return _dedupe_by_code(exact)

    # 2. Reverse alias check: does any candidate's name alias-match our original?
    if field_name == "industries":
        for c in candidates:
            c_norm = _norm(c["name"])
            c_aliases = _get_aliases(c_norm, field_name)
            if o_norm in c_aliases:
                return _dedupe_by_code([c])

    # 3. For locations, only accept exact matches (already checked via aliases)
    if field_name in ("locations", "company_locations"):
        return _dedupe_by_code(
            [c for c in candidates if _norm(c["name"]) == o_norm]
        )

    # 4. Jaccard similarity for other fields
    if field_name in ("job_titles", "industries", "departments"):
        o_tokens = _tokens(o_norm)
        scored: list[tuple[float, dict[str, str]]] = []
        for c in candidates:
            c_tokens = _tokens(_norm(c["name"]))
            jacc = _jaccard(o_tokens, c_tokens)
            if jacc >= _JACCARD_THRESHOLD:
                scored.append((jacc, c))
        scored.sort(key=lambda x: x[0], reverse=True)
        return _dedupe_by_code([c for _, c in scored])

    return []


# ──────────────────────────────────────────────
# Helpers
# ──────────────────────────────────────────────

def _validate_candidates(candidates: list[dict]) -> list[dict[str, str]]:
    """Validate candidate structure, returning only well-formed entries."""
    valid: list[dict[str, str]] = []
    seen: set[str] = set()
    for c in candidates:
        if not isinstance(c, dict):
            continue
        name = c.get("name")
        code = c.get("code")
        if not isinstance(name, str) or not name.strip():
            continue
        if not isinstance(code, str) or not code.strip():
            continue
        code = code.strip()
        if code in seen:
            continue
        seen.add(code)
        valid.append({"name": name.strip(), "code": code})
    return valid


def _dedupe_by_code(items: list[dict[str, str]]) -> list[dict[str, str]]:
    """Deduplicate by code, preserving order."""
    seen: set[str] = set()
    out: list[dict[str, str]] = []
    for c in items:
        if c["code"] in seen:
            continue
        seen.add(c["code"])
        out.append(c)
    return out


def _norm(s: str) -> str:
    """Normalize text for comparison."""
    return re.sub(r"[^a-z0-9 ]+", "", s.lower()).strip()


def _tokens(s: str) -> set[str]:
    """Split normalized text into token set."""
    return {t for t in s.split() if t}


def _jaccard(a: set[str], b: set[str]) -> float:
    """Jaccard similarity between two token sets."""
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def _get_aliases(norm: str, field_name: str = "") -> set[str]:
    """Get known aliases for a normalized string.

    Checks location aliases for location fields, industry aliases
    for industry fields, or both if field_name is empty.
    Case-insensitive matching against alias sets.
    """
    norm_lower = norm.lower()

    # Location aliases
    if not field_name or field_name in ("locations", "company_locations"):
        for canonical, alias_set in _LOCATION_ALIASES.items():
            if norm_lower in {a.lower() for a in alias_set}:
                return alias_set

    # Industry aliases
    if not field_name or field_name == "industries":
        for canonical, alias_set in _INDUSTRY_ALIASES.items():
            if norm_lower in {a.lower() for a in alias_set}:
                return alias_set

    return {norm}
