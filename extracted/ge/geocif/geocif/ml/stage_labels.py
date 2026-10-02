"""Chronological ordering of outlook stage labels — the ONE place that decides
"which stage is latest".

The results table in the outlook SQLite DB holds one row per Model x Region x
Harvest Year x Stage, and ``Stage Name`` is a free-text label such as
``"Aug 1-Mar 31"``, ``"Pre-Season (init Jan)"`` or ``"10%-100%"``. Those
strings do NOT sort chronologically as text: ``"Sep 1-Mar 31"`` sorts after
``"Oct 1-Mar 31"`` alphabetically although it is a month earlier, ``"May"`` >
``"Jul"``, and ``"Pre-Season (init Jan)"`` sorts after every in-season window.
Every "latest stage" pick must therefore go through :func:`latest_stage_rows`
(frames) or :func:`stage_sort_key` (lists of labels), never
``sort_values("Stage Name")`` / ``sorted(stage_names)``.

Which column is trusted
-----------------------
* ``Stage Window Display`` (written since 0.4.788) is ALWAYS calendar order,
  ``"<planting> 1-<as-of> 31"``, whatever the method. When a frame carries
  it, :func:`latest_stage_rows` ranks on it: the rank is the number of months
  from the planting month to the as-of month, ``(as_of - planting) % 12``.
* ``Stage Name`` is method-dependent. For ``_r`` (reverse-cumulative) methods,
  the production default, its FIRST month is the as-of month and the SECOND
  the planting month (``"Aug 1-Mar 31"`` = data through August for a
  March-planted season), so the rank is again ``(first - second) % 12``. For
  forward methods the label is calendar order and the rank is
  ``(second - first) % 12``. A frame without ``Stage Window Display`` (older
  DBs) falls back to ``Stage Name`` and :func:`infer_label_order` decides the
  convention from the set of labels (forward labels share one START month).
* Pre-season labels ``"Pre-Season (init <Mon>)"`` / ``"In-Season (init
  <Mon>)"`` are ordered by months-before-planting when a planting month is
  known (:func:`infer_planting_month`), else by a legacy March-planting wrap.
  Their rank is always below every in-season window.
* Season-normalized labels (``"10%-100%"``, ``"Stages 1-3"``) are ordered by
  their largest integer (the end of the window), so cumulative deciles that
  share a start (``"10%-20%"`` < ``"10%-30%"``) order correctly.
"""

import re

import numpy as np
import pandas as pd

MONTH_ORDER = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4, "May": 5, "Jun": 6,
    "Jul": 7, "Aug": 8, "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12,
}

STAGE_COL = "Stage Name"
SWD_COL = "Stage Window Display"

# Labels that describe a forecast issued BEFORE (or without) in-season EO
# data. They never count as "the latest stage" when an in-season window
# exists for the same region-year.
PRE_SEASON_PREFIXES = ("Pre-Season", "In-Season")

# Offset that puts every pre-season rank strictly below every in-season rank.
# Pre-season keys are in [-24, 0]; in-season keys are in [0, 11] for monthly
# windows and small positive integers for decile / growth-stage labels. A
# "(init Mar)" with March planting scores 0 and would otherwise tie with the
# in-season "Mar 1-Mar 31" (also 0).
_PRE_SEASON_OFFSET = 1000.0


def is_pre_season(name):
    """True for ``"Pre-Season (...)"`` / ``"In-Season (...)"`` labels."""
    return isinstance(name, str) and name.startswith(PRE_SEASON_PREFIXES)


def _month_token(token):
    """Month number of a ``"Mar 31"`` / ``"March"`` token, else ``None``."""
    if not isinstance(token, str) or not token.strip():
        return None
    return MONTH_ORDER.get(token.strip()[:3].title())


def _day_token(token):
    """Day-of-month of a ``"Apr 19"`` token, 0 when the token has no day."""
    if not isinstance(token, str):
        return 0
    match = re.search(r"\b(\d{1,2})\b", token)
    return int(match.group(1)) if match else 0


def window_months(label):
    """``"Mar 1-Jun 30"`` -> ``(3, 6)``; ``(None, None)`` when the label is not
    a two-month window (pre-season labels, decile labels, NaN)."""
    if not isinstance(label, str) or is_pre_season(label) or "-" not in label:
        return (None, None)
    left, right = label.split("-", 1)
    s, e = _month_token(left), _month_token(right)
    if s is None or e is None:
        return (None, None)
    return (s, e)


def infer_planting_month(stage_names):
    """Return the planting month inferred from pre-season Stage Names.

    Pre-season init months always form a contiguous block in the calendar
    (set by ``utils.get_pre_season_init_months``); planting is the calendar
    month immediately after the latest init in the block, with year wrap.

    Returns ``None`` when no Pre-Season stages are present — callers fall
    back to the legacy ordering.
    """
    months = set()
    for name in stage_names:
        if isinstance(name, str) and name.startswith("Pre-Season"):
            match = re.search(r"init (\w+)", name)
            if match:
                mn = MONTH_ORDER.get(match.group(1))
                if mn:
                    months.add(mn)
    if not months:
        return None
    for candidate in range(1, 13):
        prev = 12 if candidate == 1 else candidate - 1
        if candidate not in months and prev in months:
            return candidate
    return None


def infer_label_order(stage_names):
    """``"forward"`` when the in-season ``Stage Name`` labels are calendar
    order (cumulative windows sharing one START month, e.g. the ``monthly``
    method), else ``"reverse"`` (the ``_r`` convention: first month = as-of).

    Only the single-calendar case is decidable from the labels alone; a mixed
    set (several planting months in one frame) is treated as ``_r`` because
    that is the production default. Frames carrying ``Stage Window Display``
    never need this (see :func:`latest_stage_rows`).
    """
    firsts, seconds, n = set(), set(), 0
    for name in stage_names:
        s, e = window_months(name)
        if s is None:
            continue
        n += 1
        firsts.add(s)
        seconds.add(e)
    if n >= 2 and len(firsts) == 1 and len(seconds) > 1:
        return "forward"
    return "reverse"


def stage_sort_key(name, planting_month=None, forward=False):
    """Chronological sort key of one ``Stage Name`` label (an int).

    Pre-Season stages sort first (before any in-season stage). When
    ``planting_month`` is provided, init months are ordered by
    "months-before-planting" descending — i.e. earliest forecast first,
    latest pre-season init right before planting last. Works for any
    hemisphere / cross-year season. When ``planting_month`` is ``None`` the
    legacy March-planting wrap is used.

    In-season windows score the number of months the window spans: for the
    ``_r`` convention (default) that is ``(first - second) % 12``; with
    ``forward=True`` (calendar-order labels) it is ``(second - first) % 12``.
    Season-normalized labels score their largest integer. Anything else
    scores 0.
    """
    if is_pre_season(name):
        match = re.search(r"init (\w+)", name)
        if match:
            m = MONTH_ORDER.get(match.group(1), 0)
            if planting_month is not None and 1 <= planting_month <= 12:
                if name.startswith("In-Season"):
                    # Inits at or after planting: months SINCE planting
                    # (>= 0), so "init Jan" outranks "init Nov" for a
                    # November planting instead of wrapping to 11 months
                    # before it (2026-10-01 review).
                    return (m - planting_month) % 12
                # Months-before-planting (mod 12); negate so ascending sort
                # puts the *earliest* (furthest-from-planting) init first.
                return -((planting_month - m) % 12)
            # Legacy fallback — March-planting wrap.
            return m - 24 if m >= 7 else m - 12
        return -1
    s, e = window_months(name)
    if s is not None:
        return (e - s) % 12 if forward else (s - e) % 12
    # Season-normalized numeric labels ("10%-100%", "Stages 1-3", "10-100"):
    # order by the window END (largest integer) so cumulative labels that
    # share a start still order; "Full Season" and unknown labels score 0.
    nums = re.findall(r"\d+", name) if isinstance(name, str) else []
    return max(int(n) for n in nums) if nums else 0


def stage_rank(name, swd=None, planting_month=None, forward=False):
    """Scalar rank for "which stage is latest": in-season > pre-season > NaN.

    ``swd`` (the row's ``Stage Window Display``) wins when it parses: it is
    calendar order whatever the method, so the rank is ``(as_of - planting)
    % 12``. Otherwise the rank comes from :func:`stage_sort_key` on
    ``name``. Pre-season labels are pushed below every in-season rank and a
    missing label ranks ``-inf`` so it can never win a group that has
    anything else.
    """
    if not isinstance(name, str):
        return -np.inf
    if is_pre_season(name):
        return float(stage_sort_key(name, planting_month)) - _PRE_SEASON_OFFSET
    s, e = window_months(swd)
    if s is not None:
        # Calendar-order window: months from planting to the as-of month,
        # with the as-of calendar month and day as tie-breaks (sub-monthly
        # dekad_r / biweekly_r windows end in the same month; two monthly
        # windows can only tie when they belong to different calendars).
        e_day = _day_token(swd.split("-", 1)[1])
        return float((e - s) % 12) + e / 100.0 + e_day / 10000.0
    s, e = window_months(name)
    if s is not None:
        left, right = name.split("-", 1)
        as_of = e if forward else s
        as_of_day = _day_token(right if forward else left)
        return (
            float(stage_sort_key(name, planting_month, forward=forward))
            + as_of / 100.0 + as_of_day / 10000.0
        )
    return float(stage_sort_key(name, planting_month, forward=forward))


def stage_ranks(df, stage_col=STAGE_COL, swd_col=SWD_COL):
    """Per-row chronological rank of ``df[stage_col]`` as a float Series
    aligned on ``df.index`` (NaN labels rank ``-inf``).

    Uses ``swd_col`` when the frame has it (see :func:`stage_rank`); the
    planting month and the label convention are inferred once from the
    frame's distinct labels.
    """
    names = df[stage_col]
    valid = names.map(lambda v: isinstance(v, str))
    uniq = names[valid].unique()
    planting = infer_planting_month(uniq)
    forward = infer_label_order(uniq) == "forward"
    if swd_col in df.columns:
        swd = df[swd_col].where(df[swd_col].notna(), "").astype(str)
        key = names.astype(str) + "\x1f" + swd
        lookup = {}
        for k in key[valid].unique():
            n, w = k.split("\x1f", 1)
            lookup[k] = stage_rank(n, w or None, planting, forward)
        rank = key.map(lookup).astype(float)
    else:
        lookup = {n: stage_rank(n, None, planting, forward) for n in uniq}
        rank = names.map(lookup).astype(float)
    return rank.where(valid, -np.inf).fillna(-np.inf)


def latest_stage_rows(df, by, stage_col=STAGE_COL, swd_col=SWD_COL, keep="all"):
    """Rows of the chronologically latest stage per group.

    Args:
        df: frame with a ``stage_col`` column (returned unchanged when the
            column is absent or the frame is empty).
        by: grouping columns; names missing from ``df`` are ignored. With no
            usable key the whole frame is one group.
        stage_col: the stage-label column.
        swd_col: the calendar-order window column, preferred for ranking
            when present (see :func:`stage_rank`).
        keep: ``"all"`` returns every row of the group's latest stage;
            ``"last"`` collapses each group to its single last-inserted row
            of that stage (the cardinality of the old
            ``sort_values("Stage Name").groupby(by).last()`` pattern, but
            whole rows — never per-column last-non-null mixing).

    A pre-season label never beats an in-season window for the same group,
    and rows whose stage label is NaN rank last (they survive only when the
    group has nothing else). Row order and index are preserved.
    """
    if df is None or df.empty or stage_col not in df.columns:
        return df
    by = [c for c in by if c in df.columns]
    rank = stage_ranks(df, stage_col=stage_col, swd_col=swd_col)
    if by:
        grp_max = rank.groupby([df[c] for c in by], dropna=False).transform("max")
    else:
        grp_max = rank.max()
    out = df[rank == grp_max]
    if keep == "last":
        out = out.drop_duplicates(subset=by, keep="last") if by else out.tail(1)
    return out


def sort_stage_names(stage_names):
    """Distinct stage labels in chronological order (planting-month-aware,
    convention-aware). Convenience for axis ordering."""
    uniq = [n for n in pd.unique(pd.Series(list(stage_names))) if isinstance(n, str)]
    planting = infer_planting_month(uniq)
    forward = infer_label_order(uniq) == "forward"
    # Pre-season labels first even on a key tie ("In-Season (init Mar)" and
    # "Mar 1-Mar 31" both score 0 for March planting).
    return sorted(
        uniq,
        key=lambda s: (not is_pre_season(s),
                       stage_sort_key(s, planting, forward=forward)),
    )
