"""
GPU machines you run yourself: `sequence_ai.gpu.add` opens them near a place, `.list` shows them,
`.remove` shuts one down, and `.places` lists the cities a place can be chosen from, each with its
latitude and longitude. A machine is a container you are root in, on one card, reached over SSH
(`seq gpu ssh`) — install and run what you like; `remove` ends the machine and its disk, and stops
its billing.

These are owner-scoped: a full key or a signed-in session, never a robot key. They count against
your account's GPU limit — the ceiling serving and evals share — and draw on its credit like any
machine. `sequence_ai.gpus()` (no namespace) is a different thing entirely: the catalogue of cards
and their prices.
"""
from __future__ import annotations

from typing import Any
from urllib.parse import urlencode

from ._core.names import segment
from ._core.transport import Transport


def _owned(api_key: str | None, base_url: str | None) -> Transport:
    """A transport for the GPU management calls — owner-scoped (login=True: a full key or a signed-in
    session, never a robot key), with the mock tier mapped as the rest of the SDK maps it. `sequence_ai`
    is imported here, not at module load, because this module is imported while `sequence_ai.__init__`
    is still running."""
    import sequence_ai

    return Transport(api_key=api_key, base_url=sequence_ai._resolve_base_url(base_url), login=True)


def add(place: str, gpu: str, count: int = 1, *, api_key: str | None = None,
        base_url: str | None = None) -> list[dict[str, Any]]:
    """
    Open `count` GPU machines near `place`, each with a `gpu` card — a machine you are root on,
    reached over SSH (`seq gpu ssh`), yours until you `remove` it. Returns the machines just
    started, one dict each, status "starting":
    `[{"id", "where", "gpu", "status", "started_at", "usd_so_far", "usd_per_hour"}]`.

    `place` is the exact spot you want them near — a city ("San Francisco, CA") or a lat,lon
    ("37.77,-122.42"); `places` lists the cities, each with its lat,lon. The platform opens each
    on the nearest place it can get the card, and `where` is which of our regions it landed in.
    `count` over 1 is all-or-nothing. They count
    against your account's GPU limit (the ceiling serving and evals share) and draw on its credit;
    no card is needed. Owner-scoped: a full key or a signed-in session, never a robot key.

    """
    t = _owned(api_key, base_url)
    try:
        return t.post("/v1/gpus", {"place": place, "gpu": gpu, "count": int(count)})["gpus"]
    finally:
        t.close()


def places(q: str = "", limit: int = 8, *, api_key: str | None = None,
           base_url: str | None = None) -> list[dict[str, Any]]:
    """
    The cities a place for `add` can be chosen from: `[{"name", "region", "country", "lat", "lon", "also"}]`,
    those whose name or another name they go by starts with `q` (case and accents aside), those of their
    own name first, each the largest first, `limit` of them (1 to 20); with no `q`, the largest cities. A
    state or a country after a comma narrows them ("Springfield, IL"). `region` is None for a city with
    none (Singapore); `also` is the other name a city was found by ("paris" finds Warsaw as "Paris of the
    North"), None where `q` starts its own. Pass one's `f"{lat},{lon}"` as `add(place=...)`. The list the
    console's City picker shows; `seq gpu places` prints it. Owner-scoped.
    {the user 11-11: "a city drop down list and auto fill the long and lat"}
    """
    t = _owned(api_key, base_url)
    try:
        return t.get(f"/v1/gpus/places?{urlencode({'q': q, 'limit': int(limit)})}")["data"]
    finally:
        t.close()


def list(*, api_key: str | None = None, base_url: str | None = None) -> dict[str, Any]:
    """
    Your GPU machines and how many of your GPU limit they hold:
    `{"gpus": [{"id", "where", "gpu", "status", "started_at", "usd_so_far", "reason"?}],
    "quota": {"used", "limit"}}`. `status` is "starting", "running" (SSH connects now), "failed"
    (with `reason`), or "shut_down" (removed, or ended when the account ran out of credit). What
    `seq gpu list` prints. Owner-scoped.
    """
    t = _owned(api_key, base_url)
    try:
        return t.get("/v1/gpus")
    finally:
        t.close()


def remove(id: str, *, api_key: str | None = None, base_url: str | None = None) -> dict[str, Any]:
    """
    Shut a GPU machine down now — this ends the machine and its disk, and stops its billing.
    Returns `{"id", "status": "shut_down"}`; removing one already gone answers the same. Owner-scoped.
    """
    t = _owned(api_key, base_url)
    try:
        return t.delete(f"/v1/gpus/{segment(id, 'gpu id')}")
    finally:
        t.close()
