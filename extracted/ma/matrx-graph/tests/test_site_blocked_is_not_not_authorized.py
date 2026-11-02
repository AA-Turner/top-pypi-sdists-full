"""A website's bot wall is SITE_BLOCKED, never NOT_AUTHORIZED.

Live 2026-10-14, run ce04563a: a brand setup's crawl ended on rooterhero.com's
Cloudflare "Just a moment..." page (HTTP 403). The ladder read "403" and told
the person "This run isn't allowed to reach something it needs".
"""

from matrx_graph.failure import Cause, failure_from_text

LIVE = (
    "www.rooterhero.com: RemoteSiteCrawlError: crawl session c2de2325-2a89-4705-aa7d-770197ca0c63 "
    "ended failed: RuntimeError: Homepage fetch failed — cloudflare_block: cloudflare_block — "
    "cloudflare_block: Title indicates block: Just a moment...; bad_status: Status 403"
)


def test_the_live_cloudflare_message_is_site_blocked() -> None:
    assert failure_from_text(LIVE).cause == Cause.SITE_BLOCKED


def test_a_plain_permission_refusal_is_still_not_authorized() -> None:
    assert failure_from_text("PermissionError: 403 forbidden by row level security").cause == Cause.NOT_AUTHORIZED


def test_a_provider_rate_limit_is_still_rate_limited() -> None:
    assert failure_from_text("anthropic said: rate limit exceeded (429)").cause == Cause.RATE_LIMITED
