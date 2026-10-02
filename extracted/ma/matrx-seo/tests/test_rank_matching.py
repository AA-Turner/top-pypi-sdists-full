from matrx_seo.rank_matching import (
    RankMatchTarget,
    canonicalize_domain,
    canonicalize_rank_url,
    match_rank_url,
)


def test_domain_and_www_are_canonical_equivalents() -> None:
    target = RankMatchTarget(canonical_domain="https://www.Example.com/")

    match = match_rank_url("http://example.com/article", target)

    assert canonicalize_domain("WWW.Example.com.") == "example.com"
    assert match is not None
    assert match.match_rule == "domain"
    assert match.matched_domain == "example.com"


def test_subdomains_are_explicitly_included_or_excluded() -> None:
    included = RankMatchTarget(canonical_domain="example.com", include_subdomains=True)
    excluded = included.model_copy(update={"include_subdomains": False})

    assert match_rank_url("https://shop.example.com/product", included).match_rule == "subdomain"
    assert match_rank_url("https://shop.example.com/product", excluded) is None
    assert match_rank_url("https://notexample.com/product", included) is None


def test_page_and_alias_matches_precede_domain_match() -> None:
    target = RankMatchTarget(
        canonical_domain="example.com",
        canonical_url="https://example.com/new-page/",
        url_aliases=("http://www.example.com/old-page?b=2&a=1",),
    )

    exact = match_rank_url("http://www.example.com/new-page#result", target)
    alias = match_rank_url("https://example.com/old-page?a=1&b=2", target)

    assert exact is not None and exact.match_rule == "page_exact"
    assert alias is not None and alias.match_rule == "page_alias"
    assert canonicalize_rank_url(alias.matched_url) == alias.matched_url


def test_unicode_domains_are_compared_by_idna_identity() -> None:
    target = RankMatchTarget(canonical_domain="bücher.example")

    match = match_rank_url("https://xn--bcher-kva.example/catalog", target)

    assert match is not None
    assert match.matched_domain == "xn--bcher-kva.example"
