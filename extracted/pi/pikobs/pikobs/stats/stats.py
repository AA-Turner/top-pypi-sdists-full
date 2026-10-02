r"""
==========================================
pikobs.stats -- Significance of a change
==========================================

Every comparison Pikobs draws asks the same question: is the change
between the control and the experience larger than what chance alone
would produce? The answer depends on two things only, the quantity being
compared -- a bias or a sigma -- and whether the two runs were matched
observation by observation (``MATCH=on``) or not (``MATCH=off``). With
pairs, the bias goes through the paired t-test and the sigma through the
Pitman-Morgan test. Without them, the bias goes through Welch's t-test and
the sigma through the F-test. What follows is why, with the mathematics
and with numbers.

Nothing is kept observation by observation. For each selection -- a box,
a level, a channel, a cycle -- the extraction stores the number of pairs
and five sums, :math:`\sum x`, :math:`\sum y`, :math:`\sum x^2`,
:math:`\sum y^2` and :math:`\sum xy`, where :math:`x` is the departure of
the control and :math:`y` that of the experience for the same
observation. Everything else follows from them:

.. math::

   \bar{x} = \frac{\sum x}{N}, \qquad
   \sigma_x^2 = \frac{\sum x^2}{N} - \bar{x}^{\,2}, \qquad
   \mathrm{cov}(x, y) = \frac{\sum xy}{N} - \bar{x}\,\bar{y},

and the same for :math:`y`. The sample estimates the tests need use
:math:`N - 1`, :math:`s^2 = \sigma^2 N / (N - 1)`. Sums add, so the total
over a period is the sum over its cycles, and a figure over a month costs
no more than one over a day. Without pairs there is no :math:`\sum xy`,
and each run has its own count, :math:`N_x` and :math:`N_y`.

With pairs, the bias is tested on the differences
:math:`d_i = y_i - x_i`. Their variance comes from the same sums,

.. math::

   s_d^2 = \frac{N}{N-1}\left(\sigma_x^2 + \sigma_y^2
           - 2\,\mathrm{cov}(x, y)\right),
   \qquad
   t = \frac{|\bar{y} - \bar{x}|}{s_d / \sqrt{N}},

with :math:`N - 1` degrees of freedom. The covariance is the heart of it:
the more alike the two runs are, the smaller :math:`s_d`, and the smaller
the systematic change the test can detect. Without pairs there is no covariance to
subtract, and Welch's form treats the two runs as independent samples,

.. math::

   t = \frac{|\bar{y} - \bar{x}|}{\sqrt{s_x^2 / N_x + s_y^2 / N_y}},
   \qquad
   \nu = \frac{\left(s_x^2/N_x + s_y^2/N_y\right)^2}
              {\dfrac{(s_x^2/N_x)^2}{N_x - 1} + \dfrac{(s_y^2/N_y)^2}{N_y - 1}}.

The sigma needs the same distinction, and for a long time Pikobs did not
make it. The F-test compares two variances under the assumption that the
samples are independent,

.. math::

   F = \frac{s_{\mathrm{big}}^2}{s_{\mathrm{small}}^2},
   \qquad \nu_1 = N_{\mathrm{big}} - 1,\quad \nu_2 = N_{\mathrm{small}} - 1,

which is right without pairs and wrong with them: it ignores that the two
runs move together, and on matched runs it sees almost nothing. Pitman
and Morgan turned the question around. Take the sum and the difference of
the two departures; their covariance is exactly the difference of the two
variances,

.. math::

   \mathrm{cov}(x + y,\; y - x) = \sigma_y^2 - \sigma_x^2 ,

so the variances are equal precisely when :math:`x + y` and :math:`y - x`
are uncorrelated. The test is then the ordinary test of that correlation,

.. math::

   r = \frac{\sigma_y^2 - \sigma_x^2}
            {\sqrt{\left(\sigma_x^2 + \sigma_y^2 + 2\,\mathrm{cov}\right)
                   \left(\sigma_x^2 + \sigma_y^2 - 2\,\mathrm{cov}\right)}},
   \qquad
   t = r\,\sqrt{\frac{N - 2}{1 - r^2}},

with :math:`N - 2` degrees of freedom. It uses nothing that the paired
t-test does not already use. Every test is two-sided, since a change can
go either way, and reports a confidence :math:`(1 - p) \times 100`, where
:math:`p` is twice the upper tail of the distribution. A change counts
from 95 %. When the two runs are identical the difference has no variance
and there is nothing to test; the confidence is then 0, not a rounding
error dressed up as a certainty.

Eight observations are enough to see how much this matters. The five sums
of a box, the control and the experience seen on the same eight
observations,

.. code-block:: text

   N = 8   sum(x) = 2.4000   sum(x2) = 2.7018   sum(y) = 1.9600
           sum(y2) = 2.4028  sum(xy) = 2.5381

give means of 0.300 and 0.245, sample sigmas of 0.532 and 0.524, and a
correlation of 0.999 between the two runs. The bias improved by 0.055;
the sigma moved by 1.5 %. The four tests say:

.. code-block:: text

   bias,  paired t-test          100.0 %   significant
   bias,  Welch                   16.2 %   not significant
   sigma, Pitman-Morgan           57.1 %   not significant
   sigma, F-test                   3.1 %   not significant

The same eight numbers give 100 % or 16 % for the bias depending only on
whether the observations are paired. The runs differ by a hair on every
observation; pairing removes everything they share and leaves a change
that is small but systematic, while treated as independent the same
change drowns in a sigma of 0.5. For the sigma neither test passes on
eight observations, and they should not: 1.5 % is a very small change for
so few. But the F-test says 3 % and Pitman-Morgan 57 %, and only the
second is looking at the right thing.

The bias shows the effect of the correlation directly. A bias going from
0.30 K to 0.24 K, with 400 observations and a sigma of 1.20 K in both
runs:

.. code-block:: text

   independent samples (Welch)         52.0 %   not significant
   paired, runs correlated at 0.80     88.5 %   not significant
   paired, runs correlated at 0.95     99.8 %   significant
   paired, runs correlated at 0.99    100.0 %   significant

For the sigma the difference is starker. With 20 000 pairs correlated at
0.9999 and a sigma 0.3 % larger in the experience -- the situation of two
runs of the same suite -- Pitman-Morgan gives 100 % and the F-test 31 %.
Without pairs the F-test needs a large change or many observations: a
sigma going from 1.20 K to 1.05 K, twelve percent, reaches 59 % with 40
observations, 81 % with 100, and only passes from about 400.

On a real experiment, G0 against G2 from 16 to 21 September 2026, the
share of selections in which the change of the O-A sigma passes 95 %:

.. code-block:: text

   family  selection                          F-test   Pitman-Morgan
   ua      cycle, station, level               0.0 %        5.3 %
   sw      cycle, station, level               0.0 %        8.6 %
   iasi    cycle and channel                   0.0 %       17.5 %
   iasi    channel over the period             0.0 %       19.7 %
   ro      level, station by station           0.0 %       16.9 %
   ro      level, stations joined              0.0 %       50.5 %

That table has to be read against 5 %. A test at 95 % marks about one
selection in twenty by chance even when nothing changed; that is what the
threshold means. The radiosondes sit right there: no real change of their
sigma. The satellite winds are a little above, the radiances and the
radio occultations well above: the experiment changes their fit. The
F-test marks nothing anywhere, below chance, which is how a test that
does not fit its data looks. The O-P is not in the table because in this
experiment the two runs share their background almost everywhere -- in
iasi the O-P is identical on every observation -- and both tests
correctly find no change.

Two consequences for reading any comparison figure follow. In a map of a
hundred boxes, five coloured on their own mean nothing; a real change
shows as a pattern, a run of cycles, a band of channels, a region. And
the more observations a selection gathers, the smaller the change it can
detect: the radio occultations go from 17 % of their levels marked,
station by station, to half of them once the stations are joined, and a
small box of a map can stay grey on a change that the whole channel shows
plainly.

A departure improves only when both tests agree. An ``omp`` or ``oma``
value counts as significant when the bias test and the sigma test both
pass and both changes point the same way; a run that improves the bias
while degrading the sigma is marked, not counted. The confidence says
whether something changed, never in which direction; the sign of the
change says that, and the colours carry it, red where the experience is
better and blue where the control is.

The histogram adds one more question, whether the shape of the
distribution changed while its mean and sigma did not. The two-sample
Kolmogorov-Smirnov test takes the largest gap between the two cumulative
distributions, :math:`D = \max_x |F_x(x) - F_y(x)|`, and asks how likely
a gap that large is between two samples of the same distribution. It
assumes independent samples, so on matched runs its confidence is a
screening rather than a proof. With very large samples even small
differences can become significant, so :math:`D` itself, the maximum
separation between the two cumulative distributions, is the number to
read first.
Which test, and why
-------------------

Two experiments, the same period, the same observations. Each gives a mean
and a sigma of O-P, and the numbers are never exactly the same. The whole
question of this page is when a difference is real and when it is noise.

The usual answer treats the two experiments as two independent samples: an
F-test for the variances, Welch's t-test for the means, with :math:`n` the
number of observations of each. It is textbook statistics and it is not
wrong in itself. It rests on two assumptions, though, and neither holds when
two experiments are compared on the same observations.

**The first assumption: the two samples are unrelated.** They are not. Think
of two thermometers read by the same hundred people: a person who reads badly
reads badly on both. The same happens here. An observation that is far from
the truth -- a sonde with a wet sensor, a satellite pixel with a thin cloud --
is far from both analyses, so its O-P is large in both experiments. Write
:math:`c` and :math:`e` for the departures of one observation in the control
and in the experiment, and :math:`d = e - c` for their difference:

.. math::

   \operatorname{Var}(d) = \sigma_c^2 + \sigma_e^2 - 2\,\rho\,\sigma_c\,\sigma_e .

With :math:`\rho` the correlation between :math:`c` and :math:`e`, typically
0.9 or more, the difference of each pair moves far less than either
departure. A test that looks at the pairs sees through that shared noise; a
test that does not sees only the two large sigmas and misses changes that are
there. For the mean, the pair test is the paired t-test on the differences,

.. math::

   t = \frac{\bar{d}}{s_d / \sqrt{n}} .

For sigma it is the Pitman-Morgan test, which rests on a small identity.
With :math:`s = e + c`,

.. math::

   \operatorname{Cov}(s, d) = \sigma_e^2 - \sigma_c^2 ,

so the two variances are equal exactly when :math:`s` and :math:`d` are
uncorrelated, and testing the correlation :math:`r` of :math:`s` and
:math:`d` tests the variances:

.. math::

   t = r\,\sqrt{\frac{n - 2}{1 - r^2}} .

Pairs exist only with ``MATCH=on``. With ``MATCH=off`` the two runs do not
hold the same observations, and only the tests for independent samples
apply.

**The second assumption: every observation is a new piece of evidence.** It
is not either. All the observations of a cycle are compared with the same
forecast, so when that forecast goes wrong somewhere, thousands of them move
together: one event, counted thousands of times. With :math:`n` in the
millions, any test built on observations calls almost every difference
certain. The two mistakes pull in opposite directions -- ignoring the pairs
takes power away, overcounting :math:`n` gives confidence the data do not
have -- and with this much data the second one wins. Counting the cycles
instead of the observations is what the next section is about.

.. list-table:: Which test answers which question
   :widths: 22 26 26 26
   :header-rows: 1

   * - Question
     - Two independent samples
     - The same observations, in pairs
     - Over the cycles
   * - Same mean?
     - Welch's t-test
     - paired t-test
     - ``cycle_confidence`` on the change of the mean
   * - Same sigma?
     - F-test
     - Pitman-Morgan
     - ``cycle_confidence`` on the change of sigma
   * - What counts as one piece of evidence
     - an observation
     - a pair of observations
     - a cycle, fewer when the weather has memory

**A word on the bootstrap.** Resampling the cycles and looking at the sigma
of the resampled differences is the same idea as counting cycles, and a
sound one. Drawn one cycle at a time, though, it forgets that consecutive
cycles look alike and gives intervals that are too narrow; it has to draw
blocks of consecutive cycles to be right. The test on the cycles reaches the
same answer with a formula, at once.

**What the confidence says.** Pikobs reports :math:`100\,(1 - p)`, the
confidence with which the test rejects "no change". It is not the probability
that the experiments differ, though it is often read that way, and the other
tools that print the same number mean the same thing by it. And a confidence
of 99 % says a change is there, never that it matters: that is what the
thresholds of the scorecard are for.

Testing on the cycles
---------------------

I added this test after a summer experiment taught me something the tests
above could not. Its scorecard said that the experience had widened the O-A
of radiosonde humidity by 190 % below 10 km, with a confidence of 100 %.
The number was right. The conclusion was not: on a typical day the
experience was only 2 % wider, and about ten cycles out of four hundred,
each with one or two soundings whose O-A ran into the thousands of
kelvins, made all the rest.

The tests above count observations. A summer holds hundreds of thousands
of pairs, and they take each one as a new, independent piece of evidence.
Within a cycle that is not true. Every observation of a cycle is compared
with the same forecast, so when that forecast goes wrong somewhere,
thousands of observations move together. One event, counted thousands of
times.

So count cycles instead. Picture the season as a notebook with one page per
cycle, four pages a day. On each page write a single number, the change of
that cycle computed with its own observations only, for instance

.. math::

   c_k = \sigma_{\mathrm{exp},k} - \sigma_{\mathrm{ctl},k}.

A summer fills about 400 pages, and the question becomes a school one: is
the mean of these numbers away from zero, given how much they vary from
page to page?

.. math::

   \bar{c} = \frac{1}{n}\sum_{k=1}^{n} c_k, \qquad
   s_c^2 = \frac{1}{n-1}\sum_{k=1}^{n}\left(c_k - \bar{c}\right)^2, \qquad
   t = \frac{|\bar{c}|}{s_c / \sqrt{n}}.

Two notebooks can have the same mean and tell opposite stories. In the
first, nearly every page says the experience is 2 % wider: the pages agree,
:math:`s_c` is small, :math:`t` is large, and the change passes. In the
second, almost every page says zero and three pages say +500 %: the mean is
just as large, but the pages disagree wildly, :math:`s_c` is huge, and the
change does not pass. That second notebook is the humidity of the summer.

One more thing. Consecutive pages are not independent either, because the
weather has memory: 06 UTC looks like 00 UTC, and a situation that lasts
three days writes twelve pages of nearly the same story. The test measures
how much a page resembles the next one, the lag-1 correlation
:math:`r_1` of the series, and counts fewer pages accordingly:

.. math::

   n_{\mathrm{eff}} = n\,\frac{1 - r_1}{1 + r_1},
   \qquad
   t = \frac{|\bar{c}|}{s_c / \sqrt{n_{\mathrm{eff}}}},

with :math:`n_{\mathrm{eff}} - 1` degrees of freedom. With
:math:`r_1 = 0.5`, 400 pages are worth about 133 independent ones.
:math:`r_1` is kept between 0 and 0.95, so that a series never counts more
pages than it has. The correction matters. On simulated seasons of 400
cycles with no change at all, a test at 95 % should be fooled 5 % of the
time:

=====================  ===========================  =================
memory :math:`r_1`     fooled, with the correction  without it
=====================  ===========================  =================
0.0                    4.9 %                        4.8 %
0.5                    4.8 %                        24.6 %
0.8                    5.3 %                        53.2 %
=====================  ===========================  =================

Real is not the same as large. A change of 0.2 % that shows on nearly every
page is real, and this test will say so; whether 0.2 % matters is another
question, which is why the scorecard also asks for a change of at least
0.5 %. And the test needs pages: below twenty or so cycles it can rarely
tell anything apart, so on a short period a grey cell means "not shown",
not "no change". Every page weighs the same, whether its cycle holds fifty
observations or five thousand; the scorecard leaves out the cycles with
fewer than ten pairs.
"""

from typing import Dict, Optional, Tuple

import numpy as np

# A change counts when the confidence is strictly above this value.
MIN_CONFIDENCE = 95.0

__all__ = ["MIN_CONFIDENCE", "ftest_confidence", "ttest_confidence",
           "paired_ttest_confidence", "is_significant", "sample_std",
           "moments_from_sums", "bias_and_sigma", "cycle_confidence"]


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
    """Welch t-test on two means, for samples that cannot be matched.

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


def paired_ttest_confidence(mean_ref, mean_exp, var_ref, var_exp, cov,
                            n) -> np.ndarray:
    """Paired t-test, for runs matched observation by observation.

    ``var_ref``, ``var_exp`` and ``cov`` are population moments of the
    common observations; ``n`` the number of pairs.
    """
    n = np.asarray(n, float)
    mx, my = np.asarray(mean_ref, float), np.asarray(mean_exp, float)
    vx, vy = np.asarray(var_ref, float), np.asarray(var_exp, float)
    cxy = np.asarray(cov, float)
    conf = np.full(n.shape, np.nan)
    ok = n > 1
    if not np.any(ok):
        return conf
    d = np.abs(mx[ok] - my[ok])
    vd = np.maximum(vx[ok] + vy[ok] - 2.0 * cxy[ok], 0.0)
    se = np.sqrt(vd * n[ok] / (n[ok] - 1.0) / n[ok])
    with np.errstate(divide='ignore', invalid='ignore'):
        t = np.where(se > 0, d / se, np.where(d > 1e-12, np.inf, 0.0))
    conf[ok] = (1.0 - np.clip(2.0 * _t_sf(t, n[ok] - 1.0), 0.0, 1.0)) * 100.0
    return conf


def pitman_morgan_confidence(var_ref, var_exp, cov, n) -> np.ndarray:
    """Pitman-Morgan test on two sigmas, for runs matched observation by
    observation; confidence in percent.

    ``var_ref``, ``var_exp`` and ``cov`` are population moments of the
    common observations, ``n`` the number of pairs -- the same inputs as
    :func:`paired_ttest_confidence`, from the same five sums.

    The F-test treats the two sigmas as coming from independent samples.
    Matched runs are not: the observation and most of the background are
    the same on both sides, and their O-P correlate at 0.9999. The
    Pitman-Morgan test uses that. With x the control and y the
    experience, s = x + y and d = y - x have

        cov(s, d) = var(y) - var(x)

    so the two variances are equal exactly when s and d are uncorrelated.
    The test is the usual one on that correlation r:

        r = (var_y - var_x) / sqrt((var_x + var_y + 2 cov) (var_x + var_y - 2 cov))
        t = r sqrt((n - 2) / (1 - r^2)),   n - 2 degrees of freedom

    r is a ratio of moments, so population or sample moments give the
    same value. When the two runs are identical (var(d) = 0: the same O-P
    on every observation) there is nothing to test and the confidence is
    0, never a rounding error dressed up as 100 %. NaN where n < 3.
    """
    n = np.asarray(n, float)
    vx, vy = np.asarray(var_ref, float), np.asarray(var_exp, float)
    cxy = np.asarray(cov, float)
    shape = np.broadcast(n, vx, vy, cxy).shape
    n, vx, vy, cxy = (np.broadcast_to(a, shape) for a in (n, vx, vy, cxy))
    conf = np.full(shape, np.nan)
    ok = n > 2
    if not np.any(ok):
        return conf
    vs = vx[ok] + vy[ok] + 2.0 * cxy[ok]
    vd = vx[ok] + vy[ok] - 2.0 * cxy[ok]
    scale = np.maximum(vx[ok] + vy[ok], np.finfo(float).tiny)
    # var(d) below rounding level: the runs are the same, nothing moved
    same = (vd <= 1e-12 * scale) | (vs <= 1e-12 * scale)
    with np.errstate(divide='ignore', invalid='ignore'):
        r = np.where(same, 0.0,
                     (vy[ok] - vx[ok]) / np.sqrt(np.maximum(vs * vd, 0.0)))
    # |r| <= 1 by Cauchy-Schwarz; clip what rounding pushes past it
    r = np.clip(r, -1.0 + 1e-15, 1.0 - 1e-15)
    t = np.abs(r) * np.sqrt((n[ok] - 2.0) / (1.0 - r * r))
    conf[ok] = (1.0 - np.clip(2.0 * _t_sf(t, n[ok] - 2.0), 0.0, 1.0)) * 100.0
    return conf


def sigma_confidence(var_ref, var_exp, n_ref, n_exp=None,
                     cov=None) -> np.ndarray:
    """The sigma test the data call for; confidence in percent.

    Population variances in. With ``cov`` -- the runs were matched
    (MATCH=on) and ``n_ref`` is the number of pairs -- Pitman-Morgan.
    Without it (MATCH=off) the F-test on the two sample sigmas, each run
    with its own count (``n_exp`` defaults to ``n_ref``).
    """
    if cov is not None:
        return pitman_morgan_confidence(var_ref, var_exp, cov, n_ref)
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
