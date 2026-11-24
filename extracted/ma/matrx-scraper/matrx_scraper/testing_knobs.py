"""Test helpers shared by the scraper suite: crawler `crawl.*` knobs and the headless launch wrapper.

Importable on purpose; tests never `from conftest import` (path-dependent in CI)."""

from __future__ import annotations

#: Fast values for the crawler's `crawl.*` knobs (OPENSEO-TOOLS-SPEC §10) in tests
#: that are not about them: pacing opens at 1000 req/s (so the `_fast_pacing_knobs`
#: floor is not overridden by the 1 req/s registry default) and a 429 without
#: Retry-After pauses for 0 s. Tests ABOUT these behaviors bind their own values.
FAST_CRAWL_KNOBS: dict[str, object] = {
    "crawl.rate_limit_initial_interval_ms": 1,
    "crawl.rate_limit_max_interval_s": 0.001,
    "crawl.retry_after_default_s": 0,
    "crawl.max_consecutive_429": 3,
    "crawl.max_cooldown_minutes": 30,
    "crawl.max_retries_per_url": 3,
    "crawl.html_max_bytes": 1_048_576,
    "crawl.link_first": True,
    "crawl.item_lease_seconds": 600,
    # Not a crawl.* key, but CrawlKnobs.load_for asks for it, and a resolver answers every key asked.
    "respect_robots": False,
    # The app-shell test's knobs ride the same one-call-per-run resolution; their mirrors.
    "audit.js_shell_word_limit": 20,
    "audit.js_shell_root_text_words": 3,
}


def bind_crawl_knobs(values: dict[str, object]) -> None:
    """Bind the package knob reader to `values` for `crawl.*` keys; other keys
    (parser thresholds) raise, so they keep their mirrored defaults."""
    from matrx_scraper.parser.knobs import configure_parser_knobs

    def _read(key: str) -> object:
        if key in values:
            return values[key]
        raise KeyError(key)

    configure_parser_knobs(_read)


_HEADED_REQUESTS: list[str] = []


def _force_headless(method_name: str, original):
    import functools
    import inspect

    def _record(kwargs: dict) -> dict:
        if kwargs.get("headless") is False:
            _HEADED_REQUESTS.append(method_name)
        kwargs["headless"] = True
        args = [a for a in (kwargs.get("args") or []) if not str(a).startswith("--headless=")]
        if "args" in kwargs:
            kwargs["args"] = args
        return kwargs

    if inspect.iscoroutinefunction(original):

        @functools.wraps(original)
        async def _async_launch(self, *args, **kwargs):
            return await original(self, *args, **_record(kwargs))

        _async_launch._matrx_headless_guard = True  # type: ignore[attr-defined]
        return _async_launch

    @functools.wraps(original)
    def _sync_launch(self, *args, **kwargs):
        return original(self, *args, **_record(kwargs))

    _sync_launch._matrx_headless_guard = True  # type: ignore[attr-defined]
    return _sync_launch
