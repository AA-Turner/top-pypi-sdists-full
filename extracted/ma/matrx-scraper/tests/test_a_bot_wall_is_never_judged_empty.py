"""A Cloudflare challenge is named a bot check, never "the page came back empty" (qz.com, 2026-11-06)."""

from pathlib import Path

from matrx_scraper.read_judge import CHALLENGE, judge_read

WALL = (Path(__file__).parent / "fixtures" / "cloudflare_managed_challenge.html").read_text()


def test_the_cf_mitigated_header_names_the_wall_even_with_no_body():
    v = judge_read(status=None, text="", html=None, title=None, headers={"CF-Mitigated": "challenge"})
    assert v.failed and v.reason == CHALLENGE


def test_a_challenge_page_with_a_200_and_no_title_is_a_challenge():
    v = judge_read(status=200, text="", html=WALL, title=None)
    assert v.reason == CHALLENGE


def test_a_403_challenge_page_is_a_challenge():
    assert judge_read(status=403, text="", html=WALL, title="Just a moment...").reason == CHALLENGE

