"""A site address that forwards to somebody else's domain is not the brand's page (R2 #3 / Q4 #2, 2026-10-24).

CH-04: ``jmikes.co`` (Jersey Mike's branded Bitly domain) landed on ``bitly.com/pages/landing/...``; the homepage scrape
read that page's schema.org ``sameAs`` and filed Bitly's Facebook / Instagram / X as Jersey Mike's accounts, plus
Bitly's name, logos and customer-logo wall. Only where the address forwards may be recorded.
"""

from __future__ import annotations

from matrx_utils.source_guard import stable_source

from matrx_scraper.web_crawl import service
from matrx_scraper.events import PageSummary
from matrx_scraper.web_crawl.candidates import forwarded_candidates, landing_page_names, offsite_landing

BITLY = "https://bitly.com/pages/landing/branded-short-domains-powered-by-bitly?bsd=jmikes.co"


def test_a_vendor_landing_is_offsite() -> None:
    assert offsite_landing("https://jmikes.co", BITLY) == "vendor"
    # A vendor stays a vendor even when its page names the brand (a for-sale page names the address).
    assert offsite_landing("https://jmikes.co", BITLY, page_names=("jmikes",)) == "vendor"
    assert offsite_landing("https://joesbakery.com", "https://www.godaddy.com/forsale/joesbakery.com") == "vendor"
    assert offsite_landing("https://joesbakery.com", "https://dan.com/buy-domain/joesbakery.com",
                           page_names=("joesbakery.com is for sale | Dan.com",)) == "vendor"


def test_a_host_that_has_nothing_to_do_with_the_site_is_offsite() -> None:
    assert offsite_landing("https://pristinecarpets.com", "https://www.examplehosting.net/welcome") == "vendor"


# REVIEW12 I-4: a forward that stays the same brand must be read as the brand's page.
def test_the_brands_own_new_domain_is_not_offsite() -> None:
    assert offsite_landing("https://acmeplumbing.com", "https://www.acmeplumbingandair.com/") is None


def test_a_franchise_parents_location_page_is_not_offsite() -> None:
    assert offsite_landing("https://acmereno.com", "https://www.acmeplumbing.com/locations/reno") is None


def test_a_hosted_site_moving_to_its_own_domain_is_not_offsite() -> None:
    assert offsite_landing("https://acme.wixsite.com/home", "https://www.acme.com/") is None
    assert offsite_landing("https://www.acme.com/", "https://acme.wixsite.com/home") is None


def test_a_landing_page_titled_with_the_sites_name_is_not_offsite() -> None:
    names = landing_page_names(PageSummary(url="https://lsbakeshop.com", title="Joe's Bakery | Fresh bread in Reno"))
    assert offsite_landing("https://joesbakery.com", "https://lsbakeshop.com/", page_names=names) is None
    assert offsite_landing("https://joesbakery.com", "https://lsbakeshop.com/") == "vendor"


def test_a_forward_to_the_brands_facebook_page_becomes_its_account() -> None:
    landed = "https://www.facebook.com/joesbakery?fbclid=abc"
    assert offsite_landing("https://joesbakery.com", landed) == "social"
    out = forwarded_candidates(landed, root_url="https://joesbakery.com")
    assert [(c.category, c.guessed_kind, c.url) for c in out] == [
        ("social", "facebook", "https://www.facebook.com/joesbakery")
    ]
    # The platform's own front door names no account: nothing is recorded.
    assert forwarded_candidates("https://www.facebook.com/", root_url="https://joesbakery.com") == []


def test_a_forward_into_a_directory_records_the_listing_not_the_directory() -> None:
    landed = "https://www.yelp.com/biz/joes-bakery-reno"
    assert offsite_landing("https://joesbakery.com", landed) == "platform"
    out = forwarded_candidates(landed, root_url="https://joesbakery.com")
    assert [(c.category, c.guessed_kind, c.url) for c in out] == [("link", "website", landed)]


def test_the_sites_own_domain_is_never_offsite() -> None:
    assert offsite_landing("https://jerseymikes.com", "https://www.jerseymikes.com/menu") is None
    assert offsite_landing("http://www.jerseymikes.com/", "https://order.jerseymikes.com/") is None
    # The same name under another suffix is the same brand (a country site).
    assert offsite_landing("https://brand.com", "https://www.brand.co.uk/") is None


def test_a_forwarded_address_records_only_where_it_goes() -> None:
    out = forwarded_candidates(BITLY, root_url="https://jmikes.co")
    assert [(c.category, c.guessed_kind, c.url) for c in out] == [("link", "website", BITLY)]
    assert not any(c.category == "social" for c in out)
    assert out[0].context["forwarded_from"] == "https://jmikes.co"


def test_the_crawl_checks_the_landing_before_reading_the_page() -> None:
    source = stable_source(service)
    at_check = source.index("landed = offsite_landing(")
    at_extract = source.index("candidates = extract_homepage_candidates(")
    assert at_check < at_extract
