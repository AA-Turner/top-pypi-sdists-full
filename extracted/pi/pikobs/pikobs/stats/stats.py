r"""
==========================================
pikobs.stats -- Significance of a change
==========================================

Is the difference between the control and the experience real, or just
noise? Pikobs uses the same two tests as dasverif: a t-test for the bias
and an F-test for the sigma, at 95 %.

The two tests
-------------

**t-test (bias).** With the means :math:`m_c, m_e`, the sample sigmas
:math:`s_c, s_e` and the counts :math:`n_c, n_e`:

.. math::

   t = \frac{m_e - m_c}{\sqrt{s_c^2/n_c + s_e^2/n_e}}

each run keeping its own sigma (Welch's degrees of freedom).

**F-test (sigma).** :math:`F = s_e^2 / s_c^2`, with :math:`n_e - 1` and
:math:`n_c - 1` degrees of freedom.

Both are two-sided. The figures show a confidence, :math:`100\,(1 - p)`;
a change counts above 95 % (``MIN_CONFIDENCE``).

An example
----------

One channel, ``MATCH=off``, 400 observations in each run:

.. list-table::
   :header-rows: 1
   :widths: 30 25 25 20

   * -
     - bias
     - sigma
     - n
   * - control
     - 0.30 K
     - 1.20 K
     - 400
   * - experience
     - 0.18 K
     - 1.08 K
     - 400

The sigma went down by 10 %: :math:`F = 1.08^2 / 1.20^2 = 0.81`, and the
F-test gives 96.4 % -- a real change. The bias moved by 0.12 K:
:math:`t = -1.49`, and the t-test gives 86.2 % -- not enough, it could be
noise. Both numbers are what Pikobs computes for these values.

Why the cycles, not the observations
------------------------------------

The observations of one cycle are all compared with the same background,
so they are not independent. 100 000 observations from 56 cycles are
closer to 56 pieces of evidence than to 100 000, and a test on every
observation finds "significant" changes that two or three bad cycles made.

So when a module sums a whole period, ``MATCH=on`` tests the cycles: the
change of each cycle (bias and sigma, on the pairs), then a block
bootstrap of their mean -- 2000 resamples made of blocks of consecutive
cycles, which keeps the memory of the weather. It needs 20 cycles of at
least 10 pairs each; with fewer, the figure says "not tested".

The same channel, cycle by cycle over 30 cycles: when the sigma of every
cycle goes down about as much (-8, -6, -10, -13, -11, -14 % ..., -10.5 %
on average), the bootstrap gives 100 %. When the cycles jump from one side
to the other (-16, -6, -11, -9, +8, -9 % ..., -2 % on average), it gives
80 %: the change is not shown to be real, however many observations went in.

Which test, where
-----------------

.. list-table::
   :header-rows: 1
   :widths: 40 30 30

   * - Module
     - ``MATCH=on``
     - ``MATCH=off``
   * - verifprofile, zone, vdedr, scatter, profile, histogram
     - bootstrap on the cycles
     - t-test and F-test
   * - cardio, timeserie
     - t-test and F-test on each date's pairs
     - t-test and F-test on each date
   * - obscountdb, flags, mapobs
     - none (they count, they do not compare)
     - none

``MATCH=no`` draws the comparison with no test at all.

Reading a confidence
--------------------

Significant does not mean large: with many observations almost any change
passes, so look at the size of the change too. In scatter, a box of
``omp`` or ``oma`` counts only when the bias and the sigma both pass and
move the same way. histogram adds a Kolmogorov-Smirnov test on the shape
of the distribution.
"""

from typing import Dict, Optional, Tuple

import math

import numpy as np

# A change counts when the confidence is strictly above this value.
MIN_CONFIDENCE = 95.0

__all__ = ["MIN_CONFIDENCE", "ftest_confidence", "ttest_confidence",
           "sigma_confidence", "is_significant", "sample_std",
           "moments_from_sums", "bias_and_sigma", "cycle_confidence",
           "cycle_bootstrap_confidence", "cycle_bootstrap_many"]


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def sample_std(std_pop, n):
    """Population standard deviation (divided by n) -> sample one (n - 1)."""
    n = np.asarray(n, float)
    with np.errstate(divide='ignore', invalid='ignore'):
        return np.where(n > 1, np.asarray(std_pop, float)
                        * np.sqrt(n / np.maximum(n - 1.0, 1.0)), np.nan)


def is_significant(conf, threshold: float = MIN_CONFIDENCE) -> np.ndarray:
    """Strictly above the threshold; NaN confidences are not significant."""
    return np.nan_to_num(conf, nan=0.0) > threshold


def moments_from_sums(n, s_x, s_xx):
    """Mean and population variance from the sums a module stores."""
    n = np.asarray(n, float)
    with np.errstate(divide='ignore', invalid='ignore'):
        mean = np.where(n > 0, np.asarray(s_x, float) / n, np.nan)
        var = np.maximum(np.where(n > 0, np.asarray(s_xx, float) / n
                                  - mean * mean, np.nan), 0.0)
    return mean, var


def _t_sf(t, df):
    try:
        from scipy.stats import t as t_dist
        return t_dist.sf(t, df)
    except ImportError:                                  # pragma: no cover
        from math import erfc, sqrt
        return 0.5 * np.vectorize(lambda x: erfc(x / sqrt(2.0)))(t)


# ─────────────────────────────────────────────────────────────────────────────
# The tests
# ─────────────────────────────────────────────────────────────────────────────

def ftest_confidence(s_ref, n_ref, s_exp, n_exp) -> np.ndarray:
    """Two-sided F-test on two sigmas; confidence in percent.

    ``s_ref`` and ``s_exp`` are sample standard deviations (n - 1); use
    :func:`sample_std` when what you hold is the population one. NaN where
    the test is undefined (one observation, or a zero sigma).
    """
    s_ref, s_exp = np.asarray(s_ref, float), np.asarray(s_exp, float)
    n_ref, n_exp = np.asarray(n_ref, float), np.asarray(n_exp, float)
    conf = np.full(np.broadcast(s_ref, s_exp).shape, np.nan)
    ok = (n_ref > 1) & (n_exp > 1) & (s_ref > 0) & (s_exp > 0)
    if not np.any(ok):
        return conf
    exp_big = s_exp[ok] >= s_ref[ok]
    s_big = np.where(exp_big, s_exp[ok], s_ref[ok])
    s_small = np.where(exp_big, s_ref[ok], s_exp[ok])
    d_num = np.where(exp_big, n_exp[ok], n_ref[ok]) - 1.0
    d_den = np.where(exp_big, n_ref[ok], n_exp[ok]) - 1.0
    F = s_big ** 2 / s_small ** 2
    try:
        from scipy.stats import f as f_dist
        upper = f_dist.sf(F, d_num, d_den)
    except ImportError:                                  # pragma: no cover
        from math import erfc, sqrt
        z = np.log(F) / np.sqrt(2.0 / d_num + 2.0 / d_den)
        upper = 0.5 * np.vectorize(lambda x: erfc(x / sqrt(2.0)))(z)
    conf[ok] = (1.0 - np.minimum(1.0, 2.0 * upper)) * 100.0
    return conf


def ttest_confidence(mean_ref, std_ref, n_ref, mean_exp, std_exp,
                     n_exp) -> np.ndarray:
    """t-test on two means, for samples that cannot be matched (the form for
    unequal variances, also known as Welch's test).

    ``std_ref`` / ``std_exp`` are population standard deviations, which is
    what the modules derive from their stored sums.
    """
    m1, s1, n1 = (np.asarray(x, float) for x in (mean_ref, std_ref, n_ref))
    m2, s2, n2 = (np.asarray(x, float) for x in (mean_exp, std_exp, n_exp))
    conf = np.full(np.broadcast(m1, m2).shape, np.nan)
    ok = (n1 > 1) & (n2 > 1)
    if not np.any(ok):
        return conf
    v1 = s1[ok] ** 2 * n1[ok] / (n1[ok] - 1.0)
    v2 = s2[ok] ** 2 * n2[ok] / (n2[ok] - 1.0)
    se2 = v1 / n1[ok] + v2 / n2[ok]
    with np.errstate(divide='ignore', invalid='ignore'):
        t = np.where(se2 > 0, np.abs(m1[ok] - m2[ok]) / np.sqrt(se2), 0.0)
        df = np.where(se2 > 0, se2 ** 2 /
                      ((v1 / n1[ok]) ** 2 / (n1[ok] - 1.0)
                       + (v2 / n2[ok]) ** 2 / (n2[ok] - 1.0)), 1.0)
    conf[ok] = (1.0 - np.clip(2.0 * _t_sf(t, df), 0.0, 1.0)) * 100.0
    return conf


def sigma_confidence(var_ref, var_exp, n_ref, n_exp=None) -> np.ndarray:
    """The F-test on two sigmas, from population variances; confidence in
    percent. Each run with its own count (``n_exp`` defaults to ``n_ref``:
    the pairs of MATCH on, where both runs hold the same observations).
    """
    n_exp = n_ref if n_exp is None else n_exp
    s_ref = sample_std(np.sqrt(np.maximum(np.asarray(var_ref, float), 0.0)),
                       n_ref)
    s_exp = sample_std(np.sqrt(np.maximum(np.asarray(var_exp, float), 0.0)),
                       n_exp)
    return ftest_confidence(s_ref, n_ref, s_exp, n_exp)


# ─────────────────────────────────────────────────────────────────────────────
# The combined rule of omp / oma
# ─────────────────────────────────────────────────────────────────────────────

def ks_from_counts(counts_ref, counts_exp) -> Tuple[float, float]:
    """(D, confidence in %) of the two-sample Kolmogorov-Smirnov test.

    From two histograms on the same bins: the cumulative distributions are
    read at the bin edges, so D is the largest gap at an edge. Bins much
    narrower than the sigma lose almost nothing. The confidence is
    100 (1 - p), with the asymptotic Kolmogorov distribution and the
    effective size n_ref n_exp / (n_ref + n_exp).
    """
    a = np.asarray(counts_ref, float)
    b = np.asarray(counts_exp, float)
    na, nb = a.sum(), b.sum()
    if na <= 0 or nb <= 0:
        return float('nan'), float('nan')
    d = float(np.max(np.abs(np.cumsum(a) / na - np.cumsum(b) / nb)))
    ne = na * nb / (na + nb)
    from scipy.stats import kstwobign
    p = float(kstwobign.sf(d * np.sqrt(ne)))
    return d, 100.0 * (1.0 - p)


def bias_and_sigma(d_bias, d_sigma, t_conf, f_conf,
                    threshold: float = MIN_CONFIDENCE
                    ) -> Tuple[np.ndarray, Dict[str, np.ndarray]]:
    """Combine the two tests of a departure score.

    A point counts only when both tests pass **and** the bias and the
    sigma moved the same way: improving one while ruining the other is
    not an improvement. Returns ``(significant, confidences)``, where the
    confidences also carry ``'mixed'``, the points where both tests pass
    but the two changes disagree.
    """
    both = is_significant(t_conf, threshold) & is_significant(f_conf,
                                                              threshold)
    same = np.sign(np.asarray(d_bias)) == np.sign(np.asarray(d_sigma))
    return both & same, {'t': t_conf, 'F': f_conf, 'mixed': both & ~same}


def cycle_confidence(changes, axis: int = -1):
    """Confidence in percent that the mean change over the cycles is not
    zero, with the memory between consecutive cycles taken into account.

    ``changes`` holds the change of each cycle along ``axis`` -- for
    instance ``abs(mean_exp) - abs(mean_ctl)`` or ``sigma_exp - sigma_ctl``
    of every cycle; NaN marks a missing cycle and is skipped. The lag-1
    correlation r1 of the series, kept within [0, 0.95], gives the
    effective number of cycles n (1 - r1) / (1 + r1): a negative r1 is not
    allowed to count more cycles than there are. Fewer than three cycles
    give NaN. Returns an array of the shape of ``changes`` without
    ``axis``, a float for a single series.
    """
    d = np.moveaxis(np.asarray(changes, float), axis, -1)
    shape = d.shape[:-1]
    rows = d.reshape(-1, d.shape[-1])
    conf = np.full(rows.shape[0], np.nan)
    for i, row in enumerate(rows):
        x = row[np.isfinite(row)]
        n = x.size
        if n < 3:
            continue
        m = float(x.mean())
        s = float(x.std(ddof=1))
        if s == 0.0:
            conf[i] = 100.0 if abs(m) > 1e-12 else 0.0
            continue
        xc = x - m
        r1 = float(np.sum(xc[:-1] * xc[1:]) / np.sum(xc * xc))
        r1 = min(max(r1, 0.0), 0.95)
        n_eff = max(n * (1.0 - r1) / (1.0 + r1), 2.0)
        t = abs(m) / (s / np.sqrt(n_eff))
        p = float(np.clip(2.0 * _t_sf(t, n_eff - 1.0), 0.0, 1.0))
        conf[i] = (1.0 - p) * 100.0
    conf = conf.reshape(shape)
    return float(conf) if conf.ndim == 0 else conf


# ---------------------------------------------------------------------------
# The test on the cycles, by bootstrap
# ---------------------------------------------------------------------------

#: draws of the bootstrap: the confidence moves by less than 1 % between seeds
BOOT_DRAWS = 2000
#: the seed of every draw: the same input always gives the same confidence,
#: so a figure is the same from one run to the next
BOOT_SEED = 20251
#: fewer cycles than this and the bootstrap does not test (NaN, grey in a
#: figure): it only draws from the cycles it has, and with a few of them it
#: is surer of itself than it should be (5 days of 6-hour cycles)
BOOT_MIN_CYCLES = 20
#: a cycle counts in the bootstrap of a cell or a level from this many pairs
BOOT_MIN_PAIRS = 10


def cycle_bootstrap_confidence(changes, axis: int = -1, draws: int = BOOT_DRAWS,
                               seed: int = BOOT_SEED, min_cycles: int = BOOT_MIN_CYCLES):
    """Confidence in percent that the mean change over the cycles is not
    zero: a calibrated block bootstrap of the cycles.

    The same input and output as :func:`cycle_confidence`: ``changes`` holds
    the change of each cycle along ``axis`` (NaN for a missing cycle, left
    out); fewer than ``min_cycles`` cycles (20) give NaN: no test.

    Blocks of consecutive cycles are drawn with replacement, wrapping round
    the end, until the series is as long as the original, and its mean is
    kept; ``draws`` times. A block is as long as the memory between cycles
    asks, (1 + r1) / (1 - r1) cycles, r1 the lag-1 correlation of the series
    (one cycle when there is none). The draws give the shape of the
    distribution of the mean; its width is set to the standard error that
    cycle_confidence uses, s / sqrt(n_eff), widened by sqrt(n_eff /
    (n_eff - 1)) for a short series: drawn blocks of a series with memory
    repeat each other, and a bootstrap left to itself would be too sure of
    itself (one series in three "significant" with no change at all, for
    cycles correlated at 0.8). The confidence is the widest central interval
    of the means that leaves zero out, (1 - p) x 100, p twice the share of
    means on the other side of zero. The seed is fixed: the result never
    changes from one run to the next.
    """
    d = np.moveaxis(np.asarray(changes, float), axis, -1)
    shape = d.shape[:-1]
    rows = d.reshape(-1, d.shape[-1])
    conf = np.full(rows.shape[0], np.nan)
    for i, row in enumerate(rows):
        x = row[np.isfinite(row)]
        n = x.size
        if n < max(int(min_cycles), 3):
            continue
        m = float(x.mean())
        s = float(x.std(ddof=1))
        if s == 0.0:
            conf[i] = 100.0 if abs(m) > 1e-12 else 0.0
            continue
        xc = x - m
        r1 = float(np.sum(xc[:-1] * xc[1:]) / np.sum(xc * xc))
        r1 = min(max(r1, 0.0), 0.95)
        n_eff = max(n * (1.0 - r1) / (1.0 + r1), 2.0)
        b = int(min(max(math.ceil((1.0 + r1) / (1.0 - r1)), 1), max(n // 3, 1)))
        k = -(-n // b)                                  # blocks per draw
        rng = np.random.default_rng(int(seed) + i)     # one stream per row
        idx = (rng.integers(0, n, size=(draws, k))[:, :, None] + np.arange(b)) % n
        means = x[idx.reshape(draws, k * b)[:, :n]].mean(axis=1)
        sd_draws = float(means.std())
        width = s / math.sqrt(n_eff) * math.sqrt(n_eff / max(n_eff - 1.0, 1.0))
        if sd_draws > 0.0:
            means = m + (means - m) * (width / sd_draws)
        other = (np.count_nonzero(means <= 0.0) if m > 0 else
                 np.count_nonzero(means >= 0.0) if m < 0 else draws)
        conf[i] = (1.0 - min(1.0, 2.0 * other / draws)) * 100.0
    conf = conf.reshape(shape)
    return float(conf) if conf.ndim == 0 else conf


def padded_rows(series) -> np.ndarray:
    """Series of different lengths as the rows of one array, NaN after the
    end of each: the input of cycle_bootstrap_many."""
    series = [np.asarray(x, float) for x in series]
    rows = np.full((len(series), max((x.size for x in series), default=0)), np.nan)
    for i, x in enumerate(series):
        rows[i, :x.size] = x
    return rows


def cycle_bootstrap_many(rows, draws: int = BOOT_DRAWS, seed: int = BOOT_SEED,
                         min_cycles: int = BOOT_MIN_CYCLES, chunk: int = 4096) -> np.ndarray:
    """cycle_bootstrap_confidence of many series at once -- every row of
    ``rows`` (a cell, a box, a channel; NaN for a missing cycle) -- with the
    same confidence as calling it on each row alone, about ten times faster.

    Called on one series, cycle_bootstrap_confidence draws its blocks from
    the same seed every time, so every series with the same number of cycles
    and the same block length gets the same draws. Those series are grouped;
    a draw only says how many times each cycle is taken, so the means of all
    their draws are one matrix product, ``chunk`` series at a time. The sums
    run in another order than one series at a time: the means differ in the
    last bits, never enough to move a draw across zero -- tried on 3000
    series, not one confidence changed."""
    rows = np.atleast_2d(np.asarray(rows, float))
    conf = np.full(rows.shape[0], np.nan)
    groups: Dict[Tuple[int, int], list] = {}
    stats_of: Dict[int, tuple] = {}
    for i, row in enumerate(rows):
        x = row[np.isfinite(row)]
        n = x.size
        if n < max(int(min_cycles), 3):
            continue
        m = float(x.mean())
        s = float(x.std(ddof=1))
        if s == 0.0:
            conf[i] = 100.0 if abs(m) > 1e-12 else 0.0
            continue
        xc = x - m
        r1 = float(np.sum(xc[:-1] * xc[1:]) / np.sum(xc * xc))
        r1 = min(max(r1, 0.0), 0.95)
        n_eff = max(n * (1.0 - r1) / (1.0 + r1), 2.0)
        b = int(min(max(math.ceil((1.0 + r1) / (1.0 - r1)), 1), max(n // 3, 1)))
        groups.setdefault((n, b), []).append(i)
        stats_of[i] = (x, m, s, n_eff)
    for (n, b), members in groups.items():
        k = -(-n // b)
        rng = np.random.default_rng(int(seed))          # the draws of a lone series
        idx = ((rng.integers(0, n, size=(draws, k))[:, :, None] + np.arange(b)) % n
               ).reshape(draws, k * b)[:, :n]
        weights = np.zeros((n, draws))                  # how often each cycle is drawn
        np.add.at(weights, (idx, np.arange(draws)[:, None]), 1.0)
        weights /= n
        for c0 in range(0, len(members), chunk):
            part = members[c0:c0 + chunk]
            all_means = np.stack([stats_of[i][0] for i in part]) @ weights
            m = np.array([stats_of[i][1] for i in part])
            s = np.array([stats_of[i][2] for i in part])
            n_eff = np.array([stats_of[i][3] for i in part])
            sd = all_means.std(axis=1)
            width = s / np.sqrt(n_eff) * np.sqrt(n_eff / np.maximum(n_eff - 1.0, 1.0))
            scale = np.where(sd > 0.0, width / np.where(sd > 0.0, sd, 1.0), 1.0)
            means = m[:, None] + (all_means - m[:, None]) * scale[:, None]
            other = np.where(m > 0, np.count_nonzero(means <= 0.0, axis=1),
                             np.where(m < 0, np.count_nonzero(means >= 0.0, axis=1), draws))
            conf[part] = (1.0 - np.minimum(1.0, 2.0 * other / draws)) * 100.0
    return conf


def cycle_changes(n_ctl, s_ctl, s2_ctl, n_exp=None, s_exp=None, s2_exp=None,
                  min_obs: int = 1):
    """The change of every cycle, from the sums of each cycle: (bias, sigma).

    ``n``, ``s`` (sum) and ``s2`` (sum of squares) of the control and of the
    experience, one value per cycle. Matched runs (MATCH=on) share one count:
    give ``n_ctl`` only. The bias change of a cycle is |mean exp| - |mean ctl|
    and its sigma change sigma exp - sigma ctl, both in units of the sigma of
    the control over the whole period (the sigma change in percent of it), as
    the scorecard has always shown them. A cycle with fewer than ``min_obs``
    observations on either side is NaN, and left out by the tests.
    """
    nc = np.asarray(n_ctl, float)
    ne = nc if n_exp is None else np.asarray(n_exp, float)
    c, c2 = np.asarray(s_ctl, float), np.asarray(s2_ctl, float)
    e, e2 = np.asarray(s_exp, float), np.asarray(s2_exp, float)
    with np.errstate(divide="ignore", invalid="ignore"):
        mc, me = c / nc, e / ne
        sc_k = np.sqrt(np.maximum(c2 / nc - mc * mc, 0.0))
        se_k = np.sqrt(np.maximum(e2 / ne - me * me, 0.0))
        n_all = np.nansum(nc)
        m_all = np.nansum(c) / n_all
        sigma = math.sqrt(max(np.nansum(c2) / n_all - m_all * m_all, 0.0)) if n_all > 0 else 0.0
        if sigma <= 0.0:
            nan = np.full(nc.shape, np.nan)
            return nan, nan
        bias = (np.abs(me) - np.abs(mc)) / sigma
        d_sigma = 100.0 * (se_k - sc_k) / sigma
    few = (nc < min_obs) | (ne < min_obs)
    bias[few] = np.nan
    d_sigma[few] = np.nan
    return bias, d_sigma

