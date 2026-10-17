"""A social link is stored as the account's own address: junk query parameters never ride along (2026-10-15)."""

from matrx_scraper.web_crawl.candidates import clean_social_url


def test_view_as_and_tracking_are_cut():
    assert (clean_social_url("https://www.youtube.com/channel/UCF4Ku_RBslqV3A36j6KddZQ?view_as=subscriber")
            == "https://www.youtube.com/channel/UCF4Ku_RBslqV3A36j6KddZQ")
    assert clean_social_url("https://www.instagram.com/acme/?utm_source=ig&igshid=x#top") == "https://www.instagram.com/acme/"


def test_identifying_params_stay():
    assert clean_social_url("https://www.facebook.com/profile.php?id=123&ref=bookmarks") == "https://www.facebook.com/profile.php?id=123"
    assert clean_social_url("https://www.youtube.com/watch?v=abc&si=zzz") == "https://www.youtube.com/watch?v=abc"
