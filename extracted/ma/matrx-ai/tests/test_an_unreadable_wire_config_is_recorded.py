"""A provider config the cache guard cannot read is recorded, never only printed (real-tests closeout, 2026-11-09).

When ``wire_json`` cannot turn a provider's ``config`` into a dict, the guard compares no system text and no tools
for that round: a blind spot. It used to print one red console line and nothing else, so a guard that stopped
seeing would never reach an operator. It is now captured once per config type (kind ``prompt_cache_guard_blind``).
"""

from __future__ import annotations

import asyncio


class _Opaque:
    pass


def test_an_unreadable_config_is_captured_once_per_type() -> None:
    from matrx_ai import _ext
    from matrx_ai.providers import cache_guard

    rows: list[dict] = []

    async def record_error(exc: BaseException, **fields: object) -> None:
        rows.append(fields)

    saved = dict(_ext._registry)
    seen_set = getattr(cache_guard, "_UNREADABLE_CONFIG_SEEN", None)
    seen = set(seen_set or ())
    if seen_set is not None:
        seen_set.discard("_Opaque")
    _ext._registry["record_error"] = record_error

    async def run() -> None:
        for _ in range(3):
            cache_guard._wire_prefix_of({"config": _Opaque(), "contents": []}, None, cache_guard._wire_bytes)
        await asyncio.sleep(0.05)

    try:
        asyncio.run(run())
    finally:
        _ext._registry.clear()
        _ext._registry.update(saved)
        if seen_set is not None:
            seen_set.clear()
            seen_set.update(seen)

    blind = [r for r in rows if r.get("kind") == "prompt_cache_guard_blind"]
    assert len(blind) == 1, f"expected one captured blind-spot record, got {rows}"
    assert blind[0]["payload"] == {"config_type": "_Opaque"}
