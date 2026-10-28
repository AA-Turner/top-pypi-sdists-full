"""Every ``scrape()`` honors the host's site rules, even when the caller passes none.

A host wires its per-site scrape rules (do-not-scrape, proxy type, selectors — the
domain-rules UI, ``scraper.scrape_domain``) as the ``domain_config`` ext. Only the
quick-scrape route and the site crawler passed them; the workflow steps
(``scraper.scrape`` / ``scraper.scrape_many``) and a dozen host services did not, so a
workflow read a site a person had blocked (found converting Deep Research,
2026-10-27). ``scrape()`` now falls back to the ext, as it does for the browser pool."""

from __future__ import annotations

import pytest

from matrx_scraper import _ext
from matrx_scraper.orchestrator import scrape


class BlockEverything:
    def __init__(self) -> None:
        self.asked: list[str] = []

    def is_scrape_allowed(self, url: str) -> bool:
        self.asked.append(url)
        return False

    def get_proxy_type(self, url: str) -> str:
        return "datacenter"


@pytest.fixture
def own_registry(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(_ext, "_registry", dict(_ext._registry))


@pytest.mark.asyncio
async def test_a_caller_that_passes_no_rules_still_gets_the_hosts(own_registry: None) -> None:
    rules = BlockEverything()
    _ext.configure_ext(domain_config=rules)
    result = await scrape("https://blocked.invalid/page", escalate=False)
    assert rules.asked == ["https://blocked.invalid/page"]
    assert result.failure_reason == "domain_blocked"


@pytest.mark.asyncio
async def test_rules_the_caller_injects_win_over_the_hosts(own_registry: None) -> None:
    host, injected = BlockEverything(), BlockEverything()
    _ext.configure_ext(domain_config=host)
    await scrape("https://blocked.invalid/page", escalate=False, domain_config=injected)
    assert injected.asked and not host.asked
