"""Every DataForSEO domain-rank request carries a bare hostname as ``target``.

sec 6f24ab14 (seo_collection_failed, /seo/collections, 2026-11-20): a collection for
``labs.google.domain_rank_overview`` sent a URL target and DataForSEO answered
``Invalid Field: 'target'``. The host's tool path normalized it, but /seo/collections built the
request directly and skipped it. The normalization now lives on
``DataForSeoOperationRequest``, which every path constructs. RED before (target kept the URL),
GREEN after.
"""

from __future__ import annotations

from matrx_seo.providers.dataforseo.contracts import DataForSeoOperationRequest


def _request(operation: str, target: str) -> DataForSeoOperationRequest:
    return DataForSeoOperationRequest(
        operation=operation,
        tasks=[{"target": target, "location_code": 2840, "language_code": "en"}],
    )


def test_domain_rank_url_target_becomes_its_hostname() -> None:
    req = _request("labs.google.domain_rank_overview", "https://www.example.com/pricing?x=1")
    assert req.tasks[0]["target"] == "example.com"


def test_historical_rank_bare_domain_is_kept() -> None:
    req = _request("labs.google.historical_rank_overview", "example.org")
    assert req.tasks[0]["target"] == "example.org"


def test_other_operations_keep_a_url_target() -> None:
    req = _request("backlinks.core", "https://www.example.com/pricing")
    assert req.tasks[0]["target"] == "https://www.example.com/pricing"


def test_a_non_hostname_is_left_for_the_provider_to_refuse() -> None:
    req = _request("labs.google.domain_rank_overview", "not a domain")
    assert req.tasks[0]["target"] == "not a domain"
