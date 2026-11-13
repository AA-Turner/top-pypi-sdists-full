"""Lifted verbatim from fitevict/estimate/sizing.py (sha256 6e0805b915fdf054): rank_candidates, host_fit, room_gpu, room_ram and what they reach in that file.
Written by tools/refactors/core-off-fitevict-20261110/lift.py; the definitions below are the original text."""
from __future__ import annotations

import math
from typing import Optional

MOE_SPLIT = 'explicit'                       # fitevict imports.constants.estimation.SIZING_MOE_SPLIT
_owned_C_AUTO_GOALS = ('quality', 'fast')    # fitevict imports.constants.placement.AUTO_GOALS


def host_fit(r: dict, room_ram: Optional[int], room_swap: Optional[int] = None) -> "tuple[bool, str]":
    """F1 host side with swap as the SECOND tier: the ANONYMOUS bytes (repacked
    CPU weights, host KV/recurrent state, compute) must fit MemAvailable room +
    SwapFree — swap backs anonymous memory only. FILE-MAPPED bytes (the GGUF
    pages: all weights in RAM-only, the experts in a split) never go to swap;
    they are page cache that drops and re-reads from the file, so past the RAM
    room they stream from disk — reported, not refused. Unknown host room is
    not a fit. Returns (fits, text)."""
    if room_ram is None:
        return False, "host memory budget is unmeasured"
    anon = int(r.get("ram_anon") if r.get("ram_anon") is not None else (r.get("ram") or 0))
    filep = int(r.get("ram_file") or 0)
    swap = int(room_swap or 0)
    fits = anon <= int(room_ram) + swap
    if r.get('disk_mmap'):
        fits = fits and int(r['ram_file_reservation']) <= max(0, int(room_ram) - anon)

    txt = f"RAM anon {anon:,} B ≤ room {int(room_ram):,} B" if anon <= int(room_ram) else \
        (f"RAM anon {anon:,} B ≤ room {int(room_ram):,} + swap {swap:,} B" if fits else
         f"RAM anon {anon:,} B > room {int(room_ram):,} + swap {swap:,} B")
    if filep:
        txt += (f"; {filep:,} B file-mapped" + (" — streams from disk past the RAM room"
                                                if anon + filep > int(room_ram) else ""))
    return fits, txt


def room_gpu(card: dict, ours: "set", static_pids: "set", probe_pids: "set", g7: int) -> int:
    """D7 + F1 — the device bytes a NEW placement can claim now, evictions included:
    usable − external − static residents, where external (D6) = used − Σ our
    processes − Σ probes (and their G7); each EVICTABLE process of ours returns
    its G7 driver bytes when evicted. card = {usable, used, processes{pid: bytes}}."""
    procs = {str(k): int(v) for k, v in (card.get("processes") or {}).items()}
    ours = {str(p) for p in ours}
    static = {str(p) for p in static_pids} & ours
    probes = [str(p) for p in probe_pids if procs.get(str(p))]
    external = int(card["used"]) - sum(procs.get(p, 0) for p in ours) - sum(procs[p] + int(g7) for p in probes)
    evictable = [p for p in ours - static if procs.get(p)]
    return int(card["usable"]) - (external - len(evictable) * int(g7)) - sum(procs.get(p, 0) for p in static)


def room_ram(mem_available: int, anon_by_pid: dict, static_pids: "set") -> int:
    """F1 host side: MemAvailable + the anonymous RSS every EVICTABLE resident
    returns (file-backed pages are already inside MemAvailable)."""
    static = {str(p) for p in static_pids}
    return int(mem_available) + sum(int(v) for p, v in (anon_by_pid or {}).items() if str(p) not in static)


def rank_candidates(candidates: list, goal: str = "quality", latency_target_s=None) -> list:
    """Rank the ADMISSIBLE candidates after the hard gates (operator 2026-10-08).
    Each candidate carries (all optional except as noted):
      q            index in the approved representation list (0 = selected artifact)
      T            estimated seconds to complete, from the box's MEASURED rates
                   (cores/rates.py); None = UNMEASURED — never invented
      R            estimated reload cost (seconds) of the residents it displaces
      E_hot        number of pinned / high-priority residents it displaces
      ladder_index the fallback-order index, the tie-break for an UNMEASURED T
    Returns the candidates sorted best-first, each with "rank" (its sort key) added.
    Auto tries GPU-only, then mixed GPU/RAM, then RAM-only placements. Within
    those groups, the minimized tuple, left to right, is:
      quality  -> (q, placement order, T+R, T)
      fast -> (T, q, R)
    An UNMEASURED T falls back to the ladder order and sorts AFTER any measured
    candidate it is compared with (we never invent a bandwidth to rank it)."""
    g = str(goal or "quality").lower()
    if g not in _owned_C_AUTO_GOALS:
        g = "quality"

    placement_order = {"gpu-only":0, MOE_SPLIT:1, "max-gpu":1, "max-ram":1, "ram-only":2}
    def key(c):
        raw = c.get('T')
        known = raw is not None and math.isfinite(float(raw)) and float(raw) >= 0
        T = float(raw) if known else float('inf')
        reload_known = c.get('R') is not None
        R = max(0,float(c['R'])) if reload_known else 0
        q = int(c.get('q') or 0)
        d = placement_order.get(c.get('mode'),99)
        i = int(c.get('ladder_index') or 0)
        disk = int(bool(c.get('disk_mmap')))
        # Deadline preferences never turn an unknown estimate into a known fit.
        # A soft target annotates the candidate; the requested goal stays primary.
        try:
            target=float(latency_target_s) if latency_target_s is not None else None
        except (TypeError,ValueError):
            target=None
        c['within_latency_target'] = T <= target if known and target is not None and target > 0 else None
        if g == 'fast':
            return (disk, int(not known), T if known else i, q if known else 0, d if known else 0, int(not reload_known), R, i)
        return (disk, q, d, int(not known), int(not reload_known), T+R, T, i)
    ranked = sorted(candidates or [], key=key)
    for c in ranked:
        # Infinity is useful only inside the comparator. The reported rank is
        # persisted as JSON by Core, where an unknown timing must be null.
        c["rank"] = tuple(v if math.isfinite(v) else None for v in key(c))
        c["goal"] = g
    return ranked
