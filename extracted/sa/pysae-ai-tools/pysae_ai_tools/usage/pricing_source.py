"""Fetch live Claude pricing from the official doc and cache it on disk.

There is no embedded table: ``load_pricing`` returns the cached rates, fetching
once synchronously on a cold cache. Thereafter the hook triggers a detached
background refresh whenever the cache is older than the TTL, so rates stay current
without a network call on the hot path.
"""

import json
import re
import subprocess
import time
from dataclasses import asdict

import httpx

from ..config import assistant_cache_dir
from .pricing import ModelPricing

PRICING_URL = "https://platform.claude.com/docs/en/about-claude/pricing.md"
CACHE_PATH = assistant_cache_dir("claude") / "pricing-cache.json"
DEFAULT_TTL = 7 * 24 * 3600.0

_PRICE_RE = re.compile(r"\$\s*([0-9]+(?:\.[0-9]+)?)\s*/\s*MTok")


def _name_to_id(name: str) -> str | None:
    """Map a doc display name (e.g. 'Claude Opus 4.8') to a model id ('claude-opus-4-8')."""
    n = name.split("(")[0].split("[")[0].strip().lower()
    if not n.startswith("claude "):
        return None
    n = n[len("claude ") :].strip()
    if not n:
        return None
    return "claude-" + n.replace(".", "-").replace(" ", "-")


def parse_pricing(markdown: str) -> dict[str, ModelPricing]:
    """Parse the standard per-MTok table: rows with 5 `$x / MTok` cells.

    Columns are (base input, 5m cache write, 1h cache write, cache read, output).
    Only the first occurrence of each model is kept, so the standard table (which
    precedes the long-context / batch tables) wins.
    """
    table: dict[str, ModelPricing] = {}
    for line in markdown.splitlines():
        if not line.lstrip().startswith("|") or "MTok" not in line:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        model_id = _name_to_id(cells[0])
        if model_id is None or model_id in table:
            continue
        prices = [float(m.group(1)) for c in cells[1:] for m in [_PRICE_RE.search(c)] if m]
        if len(prices) < 5:
            continue
        table[model_id] = ModelPricing(
            input=prices[0],
            cache_write_5m=prices[1],
            cache_write_1h=prices[2],
            cache_read=prices[3],
            output=prices[4],
        )
    return table


def fetch_pricing() -> dict[str, ModelPricing]:
    """Download and parse the pricing doc. Returns {} on any failure."""
    try:
        resp = httpx.get(PRICING_URL, timeout=15.0, follow_redirects=True)
        if resp.status_code != 200:
            return {}
        return parse_pricing(resp.text)
    except httpx.HTTPError:
        return {}


def _write_cache(table: dict[str, ModelPricing], fetched_at: float) -> None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "fetched_at": fetched_at,
        "url": PRICING_URL,
        "rates": {model: asdict(p) for model, p in table.items()},
    }
    CACHE_PATH.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _read_cache() -> tuple[dict[str, ModelPricing], float] | None:
    try:
        data = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    rates = data.get("rates")
    fetched_at = data.get("fetched_at")
    if not isinstance(rates, dict) or not isinstance(fetched_at, (int, float)):
        return None
    table: dict[str, ModelPricing] = {}
    for model, raw in rates.items():
        if isinstance(raw, dict) and isinstance(raw.get("input"), (int, float)):
            table[model] = ModelPricing(
                input=float(raw["input"]),
                output=float(raw.get("output", 0.0)),
                cache_read=raw.get("cache_read"),
                cache_write_5m=raw.get("cache_write_5m"),
                cache_write_1h=raw.get("cache_write_1h"),
            )
    return (table, float(fetched_at)) if table else None


def cache_age_seconds() -> float | None:
    """Seconds since the cache was last refreshed, or None if there is no cache."""
    cached = _read_cache()
    return time.time() - cached[1] if cached is not None else None


def refresh_cache(now: float) -> dict[str, ModelPricing] | None:
    """Fetch live rates and write the cache. Returns the parsed table, or None on failure."""
    table = fetch_pricing()
    if not table:
        return None
    _write_cache(table, now)
    return table


def load_pricing() -> dict[str, ModelPricing]:
    """Return cached live rates, fetching once synchronously on a cold cache.

    Returns {} only when there is no cache and the live fetch fails.
    """
    cached = _read_cache()
    if cached is not None:
        return cached[0]
    return refresh_cache(time.time()) or {}


def maybe_background_refresh(ttl: float = DEFAULT_TTL) -> None:
    """If the cache is missing or older than ``ttl``, spawn a detached refresh and return."""
    age = cache_age_seconds()
    if age is not None and age < ttl:
        return
    # Touch the cache time first so concurrent hooks don't all spawn a refresh.
    cached = _read_cache()
    if cached is not None:
        _write_cache(cached[0], time.time())
    try:
        subprocess.Popen(
            ["pysae-ai-tools", "usage", "pricing", "refresh"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            start_new_session=True,
        )
    except (OSError, ValueError):
        pass
