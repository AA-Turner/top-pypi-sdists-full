"""Site rules — what the platform knows about a host before and after reading one of its pages.

The ``scrape_domain`` + ``scrape_path_pattern`` policy rows (migration 0037, category fields from 0101), read
through the shared :class:`~matrx_scraper.domain_config.PostgresDomainConfigStore` the scraper service already
keeps warm, merged path-over-host into ONE :class:`EffectivePolicy` per (host, path): the policy action, the
host's length floors, its main-text CSS selector, its category and notes.

Moved out of ``research/domain_policy.py`` (research/FEATURE.md § Actions a research workflow may run, lane L3, 2026-11-01) so the
``scraper.scrape`` Action can report a host's main text and rule facts without importing research. Research
keeps its callers: ``research.domain_policy`` re-exports these names, so ``domain_policy.resolve(url)`` is the
same function it always was.

Facts only: nothing here judges a page. :func:`main_text` runs the host's selector; what length counts as good
is a workflow step's rule, never this module's.

Path matching uses ``matrx_scraper.utils.url.match_path`` (``*`` = one segment, longest-specific match wins).
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING
from urllib.parse import urlparse

from matrx_scraper.utils.url import extract_domain, match_path

if TYPE_CHECKING:
    from matrx_scraper.domain_config import (
        DomainConfig,
        PathPatternConfig,
        PostgresDomainConfigStore,
    )


@dataclass(frozen=True, slots=True)
class EffectivePolicy:
    """Per-(host, path) policy after merging path overrides onto host defaults."""

    policy_action: str | None = None
    min_content_chars: int | None = None
    min_real_content_chars: int | None = None
    content_selector: str | None = None
    policy_notes: str | None = None
    category: str | None = None
    category_reason: str | None = None
    matched_pattern: str | None = None


_log = logging.getLogger(__name__)


def _try_get_store() -> PostgresDomainConfigStore | None:
    try:
        from matrx_scraper._ext import get_ext, has_ext
        from matrx_scraper.domain_config import PostgresDomainConfigStore

        if not has_ext("domain_config"):
            return None
        store = get_ext("domain_config")
        if isinstance(store, PostgresDomainConfigStore):
            return store
    except Exception:
        _log.debug("domain_config store unavailable for research policy", exc_info=True)
    return None


def _candidate_hosts(url: str) -> list[str]:
    raw = (extract_domain(url) or "").lower()
    candidates = [raw] if raw else []
    if raw.startswith("www."):
        candidates.append(raw[4:])
    return candidates


def _path_of(url: str) -> str:
    try:
        return urlparse(url).path or "/"
    except Exception:
        return "/"


def _domain_has_policy(config: DomainConfig) -> bool:
    if any(
        (
            config.policy_action,
            config.min_content_chars is not None,
            config.min_real_content_chars is not None,
            config.content_selector,
            config.category,
        )
    ):
        return True
    return any(_path_has_policy(pp) for pp in config.path_patterns)


def _path_has_policy(path_rule: PathPatternConfig) -> bool:
    return bool(
        path_rule.policy_action
        or path_rule.min_content_chars is not None
        or path_rule.min_real_content_chars is not None
        or path_rule.content_selector
        or path_rule.category
    )


def _lookup_domain(store: PostgresDomainConfigStore, url: str) -> DomainConfig | None:
    for host in _candidate_hosts(url):
        config = store.get_domain_by_host(host)
        if config is not None:
            return config
    return None


def _resolve_from_store(url: str, store: PostgresDomainConfigStore) -> EffectivePolicy:
    if not url:
        return EffectivePolicy()

    config = _lookup_domain(store, url)
    if config is None or not _domain_has_policy(config):
        return EffectivePolicy()

    path_rule: PathPatternConfig | None = None
    if config.path_patterns:
        matched = match_path(_path_of(url), [pp.pattern for pp in config.path_patterns])
        if matched is not None:
            for pp in config.path_patterns:
                if pp.pattern == matched:
                    path_rule = pp
                    break

    if path_rule is None:
        return EffectivePolicy(
            policy_action=config.policy_action,
            min_content_chars=config.min_content_chars,
            min_real_content_chars=config.min_real_content_chars,
            content_selector=config.content_selector,
            policy_notes=config.policy_notes,
            category=config.category,
            category_reason=config.category_reason,
            matched_pattern=config.url,
        )

    return EffectivePolicy(
        policy_action=path_rule.policy_action or config.policy_action,
        min_content_chars=(
            path_rule.min_content_chars
            if path_rule.min_content_chars is not None
            else config.min_content_chars
        ),
        min_real_content_chars=(
            path_rule.min_real_content_chars
            if path_rule.min_real_content_chars is not None
            else config.min_real_content_chars
        ),
        content_selector=path_rule.content_selector or config.content_selector,
        policy_notes=path_rule.policy_notes or config.policy_notes,
        category=path_rule.category or config.category,
        category_reason=path_rule.category_reason or config.category_reason,
        matched_pattern=f"{config.url}{path_rule.pattern}",
    )


async def resolve(url: str) -> EffectivePolicy:
    store = _try_get_store()
    if store is None:
        return EffectivePolicy()
    return _resolve_from_store(url, store)


def main_text(html: str | None, selector: str | None) -> str | None:
    """The host's main text: its CSS selector run over the page's HTML. ``None`` when the host has no selector or
    there is no HTML (nothing was measured); ``""`` when the selector matched nothing (measured, empty)."""
    if not selector or not html:
        return None
    from matrx_scraper.parser.core import extract_text_by_selector

    return extract_text_by_selector(html, selector)


__all__ = ["EffectivePolicy", "main_text", "resolve"]
