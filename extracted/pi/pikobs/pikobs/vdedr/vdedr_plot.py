#!/usr/bin/python3
"""Figures of pikobs.vdedr.

Three figures per selection, with the radiance channels on the y axis:

* ``omp_bias``  residual bias and raw bias, experience minus control
* ``omp_rel``   change of sigma(OMP) and of the number of observations, %
* ``oma_rel``   the same for OMA

Everything is computed from the sums stored by the extraction, so the
SQLite STDDEV extension is not needed any more and the numbers recombine
exactly over cycles.
"""

import os
import re
import traceback
from typing import Any, Dict, List, Optional, Sequence, Tuple

import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import numpy as np

from pikobs.figures import save_figure
from pikobs.obsdb import open_result
from pikobs.stats import (MIN_CONFIDENCE, moments_from_sums,
                          paired_ttest_confidence, ttest_confidence,
                          sigma_confidence)


# =============================================================================
# Metrics
# =============================================================================

METRICS = {
    'omp_bias': ('OMP', ('residual bias', 'raw bias')),
    'omp_rel':  ('OMP', ('% sigma', '% Nobs')),
    'oma_rel':  ('OMA', ('% sigma', '% Nobs')),
}


# =============================================================================
# Colours
# =============================================================================

ROUGE = '#FF9999'
ROUGEPUR = '#FF0000'
VERT = '#009900'
BLEU = '#1569C7'
NOIR = '#000000'

COULEURS = [
    BLEU,
    ROUGEPUR,
    ROUGE,
    VERT,
    NOIR,
]


# Sign convention:
#
# negative -> experience better -> red
# positive -> control better    -> blue
from pikobs.configobs.style import (
    CTL_BETTER,
    CTL_COLOUR,
    EXP_COLOUR,
    CTL_COLOUR,
    EXP_COLOUR,
    EXP_BETTER,
    NEUTRAL as NEUTRAL_LINE,
)


# Alternating channel row.
BAND = '#f3f4f5'


# =============================================================================
# Layout
# =============================================================================

# Enough vertical space for channel labels.
INCH_PER_CHANNEL = 0.20

MIN_HEIGHT = 7.2
MAX_HEIGHT = 260.0

# Wider than the old figure so that the scientific plot and the
# confidence/count columns do not compete for space.
FIGURE_WIDTH = 11.5


# Channel tick labels.
TICK_FONTSIZE_MAX = 9.0
TICK_FONTSIZE_MIN = 5.0


# PNG resolution.
DPI = 90


# Observation counts are useful when there are not too many rows.
MAX_CHANNELS_WITH_COUNTS = 300


# For very large channel sets keep the significance circles, but omit
# the numeric confidence percentage beside every circle.
MAX_CHANNELS_WITH_CONFIDENCE = 300


# =============================================================================
# Names
# =============================================================================

GRAPHE_NOMVAR = {
    11215: 'U COMPONENT OF WIND (10M)',
    11216: 'V COMPONENT OF WIND (10M)',
    12004: 'DRY BULB TEMPERATURE AT 2M',
    10051: 'PRESSURE REDUCED TO MEAN SEA LEVEL',
    10004: 'PRESSURE',
    12203: 'DEW POINT DEPRESSION (2M)',
    12001: 'TEMPERATURE/DRY BULB',
    11003: 'U COMPONENT OF WIND',
    11004: 'V COMPONENT OF WIND',
    12192: 'DEW POINT DEPRESSION',
    12163: 'BRIGHTNESS TEMPERATURE',
    15036: 'ATMOSPHERIC REFRACTIVITY',
    11001: 'WIND DIRECTION',
    11002: 'WIND SPEED',
    11011: 'WIND DIRECTION AT 10M',
    11012: 'WIND SPEED AT 10M',
}


def varno_name(varno) -> str:
    """Return a readable variable name."""

    try:
        varno = int(varno)

    except (TypeError, ValueError):
        return str(varno)

    if varno in GRAPHE_NOMVAR:
        return GRAPHE_NOMVAR[varno]

    try:
        import pikobs

        name, units, _ = pikobs.type_varno(varno)

        return f"{name} {units}".strip()

    except Exception:
        return str(varno)


def _safe(text) -> str:
    """Make text safe for filenames."""

    return re.sub(
        r'[^A-Za-z0-9._+-]',
        '_',
        str(text),
    )


# =============================================================================
# Read statistics
# =============================================================================

def _channel_stats(
    db_file: str,
    region: str,
    flag: str,
    stn_sql: str,
    varno: int,
    land_ocean: str = 'all',
    special: str = 'all',
) -> Dict[float, Dict[str, float]]:
    """Mean, sigma, count and mean bias correction of every channel.

    stn_sql is the station condition of the selector (empty for join), so
    several platforms are pooled by summing their moments.
    """

    with open_result(db_file) as conn:

        rows = conn.execute(
            f"""
            SELECT
                vcoord,
                SUM(Ntot),
                SUM(s_omp),
                SUM(s2_omp),
                SUM(s_oma),
                SUM(s2_oma),
                SUM(n_bcorr),
                SUM(s_bcorr)
            FROM serie_vdedr
            WHERE
                region = ?
                AND flag = ?
                AND land_ocean = ?
                AND special = ?
                AND varno = ?{stn_sql}
            GROUP BY vcoord;
            """,
            (
                region,
                flag,
                land_ocean,
                special,
                int(varno),
            ),
        ).fetchall()

    out: Dict[float, Dict[str, float]] = {}

    for (
        vcoord,
        n,
        s_omp,
        q_omp,
        s_oma,
        q_oma,
        n_bc,
        s_bc,
    ) in rows:

        if not n:
            continue

        n = float(n)

        stat = {
            'n': n,
        }

        for tag, s, q in (
            ('omp', s_omp, q_omp),
            ('oma', s_oma, q_oma),
        ):

            if s is None:

                stat[f'avg_{tag}'] = np.nan
                stat[f'std_{tag}'] = np.nan

                continue

            mean = s / n

            var = max(
                (q or 0.0) / n - mean * mean,
                0.0,
            )

            stat[f'avg_{tag}'] = mean
            stat[f'std_{tag}'] = np.sqrt(var)

        stat['bcorr'] = (
            s_bc / n_bc
            if n_bc and s_bc is not None
            else np.nan
        )

        out[float(vcoord)] = stat

    return out


# =============================================================================
# Figure dimensions
# =============================================================================

def _pair_stats(db_file, region, flag, stn_sql, varno, channels,
                land_ocean='all', special='all'):
    """Sums of the matched observations, per channel, in channel order.

    None when the run has no pair database -- an output made before vdedr
    learned to match -- and the caller keeps the Welch test.
    """
    if not db_file or not os.path.isfile(db_file):
        return None

    try:
        with open_result(db_file) as conn:
            rows = conn.execute(
                """
                SELECT vcoord,
                       SUM(n_omp), SUM(sx_omp), SUM(sy_omp),
                       SUM(sxx_omp), SUM(syy_omp), SUM(sxy_omp),
                       SUM(n_oma), SUM(sx_oma), SUM(sy_oma),
                       SUM(sxx_oma), SUM(syy_oma), SUM(sxy_oma)
                FROM pairs_vdedr
                WHERE region = ? AND flag = ? AND land_ocean = ?
                  AND special = ? AND varno = ?""" + stn_sql + """
                GROUP BY vcoord;
                """,
                (
                    region,
                    flag,
                    land_ocean,
                    special,
                    int(varno),
                ),
            ).fetchall()

    except Exception:
        return None

    if not rows:
        return None

    by_chan = {
        float(r[0]): r[1:]
        for r in rows
    }

    out = {}

    for j, tag in enumerate(
        (
            'omp',
            'oma',
        )
    ):

        base = j * 6

        for k, name in enumerate(
            (
                'n',
                'sx',
                'sy',
                'sxx',
                'syy',
                'sxy',
            )
        ):

            out[f'{name}_{tag}'] = np.array(
                [
                    float(
                        (
                            by_chan.get(float(c))
                            or [np.nan] * 12
                        )[base + k]
                        or np.nan
                    )
                    for c in channels
                ],
                dtype=float,
            )

    return out


def _paired_conf(pairs, tag, fallback):
    """Paired confidence of one quantity; Welch where a channel has no pair.

    The covariance is what does the work: the more alike the two runs
    are, the smaller the sigma of their difference, and the easier it is
    to see a change that an independent test drowns in the sigma.
    """
    if pairs is None:
        return fallback

    n = pairs.get(f'n_{tag}')

    if (
        n is None
        or not np.any(
            np.nan_to_num(n) > 1
        )
    ):
        return fallback

    mx, vx = moments_from_sums(
        n,
        pairs[f'sx_{tag}'],
        pairs[f'sxx_{tag}'],
    )

    my, vy = moments_from_sums(
        n,
        pairs[f'sy_{tag}'],
        pairs[f'syy_{tag}'],
    )

    with np.errstate(
        divide='ignore',
        invalid='ignore',
    ):

        cxy = np.where(
            np.nan_to_num(n) > 0,
            pairs[f'sxy_{tag}'] / n - mx * my,
            np.nan,
        )

    conf = paired_ttest_confidence(
        mx,
        my,
        vx,
        vy,
        cxy,
        n,
    )

    gap = ~np.isfinite(conf)

    return (
        np.where(gap, fallback, conf)
        if np.any(gap)
        else conf
    )



def _paired_sigma_conf(pairs, tag, fallback):
    """The sigma of matched channels: Pitman-Morgan on the pair sums.

    The sister of :func:`_paired_conf` for the bias. The two runs share
    the observation and most of the background, so their departures move
    together; the F-test takes them for independent samples and misses
    nearly every change of sigma between them. Where a channel has no
    pairs, ``fallback`` (the F-test on each run's own moments) stands.
    """
    if pairs is None:
        return fallback
    n = pairs.get(f'n_{tag}')
    if n is None or not np.any(np.nan_to_num(n) > 2):
        return fallback
    mx, vx = moments_from_sums(n, pairs[f'sx_{tag}'], pairs[f'sxx_{tag}'])
    my, vy = moments_from_sums(n, pairs[f'sy_{tag}'], pairs[f'syy_{tag}'])
    with np.errstate(divide='ignore', invalid='ignore'):
        cxy = np.where(np.nan_to_num(n) > 0,
                       pairs[f'sxy_{tag}'] / n - mx * my, np.nan)
    conf = sigma_confidence(vx, vy, n, cov=cxy)
    return np.where(np.isfinite(conf), conf, fallback)

def _figure_size(
    n_channels: int,
) -> Tuple[float, float]:
    """Figure size adapted to the number of channels."""

    height = min(
        max(
            MIN_HEIGHT,
            3.3 + INCH_PER_CHANNEL * n_channels,     # the header: 0.5 in more
        ),
        MAX_HEIGHT,
    )

    return FIGURE_WIDTH, height


def _tick_fontsize(
    n_channels: int,
    fig_height: float,
) -> float:
    """Largest readable channel font for the available vertical space."""

    if n_channels <= 0:
        return TICK_FONTSIZE_MAX

    plot_height = max(
        fig_height - 2.2,
        1.0,
    )

    inch_per_row = (
        plot_height
        / n_channels
    )

    points = (
        inch_per_row
        * 72.0
        / 1.35
    )

    return float(
        np.clip(
            points,
            TICK_FONTSIZE_MIN,
            TICK_FONTSIZE_MAX,
        )
    )


# =============================================================================
# Public plotting entry point
# =============================================================================

def _land_special(task, sep="_") -> str:
    """The land filter and the special value, only when there is one: a
    run without them keeps its file names and its titles."""
    bits = []
    if task.get('land_ocean', 'all') not in (None, '', 'all'):
        bits.append(str(task['land_ocean']))
    if task.get('special_label', 'all') not in (None, '', 'all'):
        bits.append(str(task['special_label']))
    if sep == "_":
        return "".join(f"_{_safe(b)}" for b in bits)
    return "".join(f"{sep}{b}" for b in bits)


def vdedr_plot_task(
    task: Dict[str, Any],
) -> Optional[List[Dict[str, str]]]:
    """Draw the three figures of one selection; returns their paths."""

    try:
        return _plot(task)

    except Exception:

        print(
            f"[vdedr] plot failed for "
            f"{task.get('family')} "
            f"{task.get('id_stn')} "
            f"varno {task.get('varno')}:\n"
            f"{traceback.format_exc()}",
            flush=True,
        )

        plt.close('all')

        return None


# =============================================================================
# Main plot
# =============================================================================

def _plot(
    task: Dict[str, Any],
) -> Optional[List[Dict[str, str]]]:

    # -------------------------------------------------------------------------
    # Read control / experiment
    # -------------------------------------------------------------------------

    stn_sql = task.get(
        'stn_sql',
        '',
    )

    ctl = _channel_stats(
        task['files_in'][0],
        task['region'],
        task['flag'],
        stn_sql,
        task['varno'],
        task.get('land_ocean', 'all'),
        task.get('special', 'all'),
    )

    exp = _channel_stats(
        task['files_in'][1],
        task['region'],
        task['flag'],
        stn_sql,
        task['varno'],
        task.get('land_ocean', 'all'),
        task.get('special', 'all'),
    )

    channels = sorted(
        set(ctl) & set(exp),
        reverse=True,
    )

    if not channels:
        return None

    name1, name2 = task['names_in']

    period = (
        f"{task['datestart']}  →  "
        f"{task['dateend']}"
    )

    idlev = np.arange(
        len(channels)
    )

    n1 = np.array(
        [
            ctl[c]['n']
            for c in channels
        ],
        dtype=float,
    )

    n2 = np.array(
        [
            exp[c]['n']
            for c in channels
        ],
        dtype=float,
    )

    def col(src, key):

        return np.array(
            [
                src[c][key]
                for c in channels
            ],
            dtype=float,
        )

    # -------------------------------------------------------------------------
    # Quantities shown in the three figures
    # -------------------------------------------------------------------------

    with np.errstate(
        divide='ignore',
        invalid='ignore',
    ):

        series = {

            'omp_bias': (
                col(exp, 'avg_omp')
                - col(ctl, 'avg_omp'),

                (
                    col(exp, 'avg_omp')
                    - col(exp, 'bcorr')
                )
                -
                (
                    col(ctl, 'avg_omp')
                    - col(ctl, 'bcorr')
                ),
            ),

            'omp_rel': (
                100.0
                * (
                    col(exp, 'std_omp')
                    - col(ctl, 'std_omp')
                )
                / col(ctl, 'std_omp'),

                100.0
                * (
                    n2 - n1
                )
                / n1,
            ),

            'oma_rel': (
                100.0
                * (
                    col(exp, 'std_oma')
                    - col(ctl, 'std_oma')
                )
                / col(ctl, 'std_oma'),

                100.0
                * (
                    n2 - n1
                )
                / n1,
            ),
        }

    # -------------------------------------------------------------------------
    # Statistical tests
    # -------------------------------------------------------------------------

    # the matched observations of this selection, if the run made them

    pairs = _pair_stats(

        task.get('db_pairs'),

        task['region'],

        task['flag'],

        stn_sql,

        task['varno'],

        channels,

        task.get('land_ocean', 'all'),

        task.get('special', 'all'),

    )


    conf = {

        # the sigma: Pitman-Morgan on the pairs of each channel, the
        # sigma test on each run's own moments where a channel has none
        'omp_rel': _paired_sigma_conf(
            pairs, 'omp',
            sigma_confidence(np.square(col(ctl, 'std_omp')),
                             np.square(col(exp, 'std_omp')), n1, n2)),

        'oma_rel': _paired_sigma_conf(
            pairs, 'oma',
            sigma_confidence(np.square(col(ctl, 'std_oma')),
                             np.square(col(exp, 'std_oma')), n1, n2)),

        # paired when the run matched the observations, Welch
        # when it could not: on two runs of the same suite that
        # is the difference between seeing a change and not
        'omp_bias': _paired_conf(
            pairs,
            'omp',
            ttest_confidence(
            col(ctl, 'avg_omp'),
            col(ctl, 'std_omp'),
            n1,
            col(exp, 'avg_omp'),
            col(exp, 'std_omp'),
            n2,
        ),
        ),
    }

    # For the bias, winner means the run whose mean is closer to zero.
    winner = {

        'omp_bias':
            np.abs(
                col(exp, 'avg_omp')
            )
            -
            np.abs(
                col(ctl, 'avg_omp')
            )
    }

    out: List[Dict[str, str]] = []

    # =========================================================================
    # One figure per metric
    # =========================================================================

    for metric, (
        first,
        second,
    ) in series.items():

        typer, legend = METRICS[metric]

        fig_w, fig_h = _figure_size(
            len(channels)
        )

        tick_fs = _tick_fontsize(
            len(channels),
            fig_h,
        )

        # ---------------------------------------------------------------------
        # Figure
        # ---------------------------------------------------------------------

        fig, ax = plt.subplots(
            figsize=(
                fig_w,
                fig_h,
            ),
            facecolor='white',
        )

        ax.set_facecolor(
            '#fcfcfc'
        )

        # Fixed physical margins.
        left_in = 0.95

        # A little more room than before for:
        #
        # sigma test | Confidence | N control | N experience
        right_in = 3.00

        top_in = 2.05
        bottom_in = 0.80

        fig.subplots_adjust(
            left=left_in / fig_w,
            right=1.0 - right_in / fig_w,
            top=1.0 - top_in / fig_h,
            bottom=bottom_in / fig_h,
        )

        # ---------------------------------------------------------------------
        # Background
        # ---------------------------------------------------------------------

        for y in idlev[::2]:

            ax.axhspan(
                y - 0.5,
                y + 0.5,
                color=BAND,
                zorder=0,
            )

        ax.grid(
            True,
            axis='x',
            linestyle=':',
            linewidth=0.65,
            color='#a0a0a0',
            alpha=0.48,
            zorder=1,
        )

        ax.set_axisbelow(
            True
        )

        ax.axvline(
            0.0,
            color='#404040',
            lw=1.15,
            alpha=0.85,
            zorder=2,
        )

        for spine in ax.spines.values():

            spine.set_color(
                '#555555'
            )

            spine.set_linewidth(
                0.75
            )

        # ---------------------------------------------------------------------
        # Main series
        # ---------------------------------------------------------------------

        signed = metric in (
            'omp_rel',
            'oma_rel',
        )

        ax.plot(
            first,
            idlev,
            linestyle='-',
            linewidth=1.45,
            zorder=3,
            color=(
                NEUTRAL_LINE
                if signed
                else NEUTRAL_LINE
            ),
            label=legend[0],
        )

        if signed:

            # Negative -> experiment better -> red.
            ax.plot(
                np.where(
                    first < 0,
                    first,
                    np.nan,
                ),
                idlev,
                linestyle='none',
                marker='o',
                markersize=5.0,
                markeredgewidth=0.0,
                color=EXP_BETTER,
                zorder=4,
                label=(
                    f"{legend[0]} < 0: "
                    "Exp better"
                ),
            )

            # Positive -> control better -> blue.
            ax.plot(
                np.where(
                    first > 0,
                    first,
                    np.nan,
                ),
                idlev,
                linestyle='none',
                marker='o',
                markersize=5.0,
                markeredgewidth=0.0,
                color=CTL_BETTER,
                zorder=4,
                label=(
                    f"{legend[0]} > 0: "
                    "Ctl better"
                ),
            )

        else:

            ax.plot(
                first,
                idlev,
                linestyle='none',
                marker='o',
                markersize=4.8,
                markeredgewidth=0.0,
                color=NEUTRAL_LINE,
                zorder=4,
            )

        # Nobs / second metric.
        ax.plot(
            second,
            idlev,
            linestyle='-',
            marker='o',
            color=COULEURS[3],
            markersize=3.6,
            markeredgewidth=0.0,
            linewidth=1.35,
            zorder=3,
            label=legend[1],
        )

        # ---------------------------------------------------------------------
        # Channel axis
        # ---------------------------------------------------------------------

        ax.set_yticks(
            idlev
        )

        ax.set_yticklabels(
            [
                f"{c:g}"
                for c in channels
            ],
            fontsize=tick_fs,
        )

        ax.set_ylim(
            idlev[0] - 0.5,
            idlev[-1] + 0.5,
        )

        ax.tick_params(
            axis='y',
            pad=5,
            length=2.5,
            width=0.6,
            labelcolor='#202020',
        )

        ax.tick_params(
            axis='x',
            labelsize=9.5,
            length=3,
            width=0.6,
            pad=5,
        )

        ax.set_ylabel(
            'Channel',
            fontsize=12,
            fontweight='semibold',
            color='#202020',
            labelpad=11,
        )

        ax.set_xlabel(
            (
                f"{legend[0]}"
                f"    /    "
                f"{legend[1]}"
            ),
            fontsize=11,
            fontweight='medium',
            labelpad=8,
        )

        # =====================================================================
        # Confidence / statistical test
        # =====================================================================

        c_vals = conf.get(
            metric
        )

        # ---------------------------------------------------------------------
        # Column positions
        #
        # Keep these clearly separated:
        #
        #       sigma test    Confidence    N control    N experience
        #         ○         99.7%         18976          28196
        # ---------------------------------------------------------------------

        CIRCLE_X = 1.015
        CONF_X = 1.085
        N_CTL_X = 1.220
        N_EXP_X = 1.350

        if c_vals is not None:

            test_name = (
                't-test'
                if metric == 'omp_bias'
                else 'sigma test'
            )

            # no percentages: the circle, filled where the test passes,
            # says all there is to say
            show_confidence_value = False

            # -----------------------------------------------------------------
            # Confidence circles + percentages
            # -----------------------------------------------------------------

            for y in idlev:

                if not np.isfinite(
                    c_vals[y]
                ):
                    continue

                sign = winner.get(
                    metric,
                    first,
                )[y]

                if (
                    c_vals[y]
                    > MIN_CONFIDENCE
                ):

                    face = (
                        CTL_BETTER
                        if sign > 0
                        else EXP_BETTER
                    )

                else:

                    face = 'white'

                # -------------------------------------------------------------
                # sigma test / t-test marker: circle
                # -------------------------------------------------------------

                ax.scatter(
                    CIRCLE_X,
                    y,
                    s=30,
                    marker='o',
                    facecolor=face,
                    edgecolor='#555555',
                    linewidths=0.55,
                    clip_on=False,
                    zorder=5,
                    transform=ax.get_yaxis_transform(),
                )

                # the percentage only where the test passes: the empty
                # circle already says the others did not
                if show_confidence_value and c_vals[y] > MIN_CONFIDENCE:

                    ax.text(
                        CONF_X,
                        y,
                        f"{c_vals[y]:.1f}%",
                        fontsize=tick_fs,
                        va='center',
                        ha='center',
                        color='#222222',
                        fontweight='semibold',
                        transform=ax.get_yaxis_transform(),
                    )

            # -----------------------------------------------------------------
            # Test summary
            # -----------------------------------------------------------------

            sig = (
                c_vals
                > MIN_CONFIDENCE
            )

            side = winner.get(
                metric,
                first,
            )

            n_sig = int(
                np.nansum(
                    sig
                )
            )

            n_better = int(
                np.nansum(
                    sig
                    & (side < 0)
                )
            )

            n_worse = int(
                np.nansum(
                    sig
                    & (side > 0)
                )
            )

            ax.annotate(
                (
                    f"{test_name} > "
                    f"{MIN_CONFIDENCE:.0f}%: "
                    f"{n_sig}/{len(channels)}"
                    f"   •   "
                    f"Exp {n_better}"
                    f"   •   "
                    f"Ctl {n_worse}"
                ),
                xy=(
                    N_EXP_X + 0.025,
                    1.0,
                ),
                xycoords='axes fraction',
                xytext=(
                    0,
                    36,
                ),
                textcoords='offset points',
                fontsize=9.0,
                fontweight='bold',
                color='#202020',
                ha='right',
                va='bottom',
            )

            # -----------------------------------------------------------------
            # Column headers
            # -----------------------------------------------------------------

            ax.annotate(
                test_name,
                xy=(
                    CIRCLE_X,
                    1.0,
                ),
                xycoords='axes fraction',
                xytext=(
                    0,
                    14,
                ),
                textcoords='offset points',
                fontsize=8.2,
                fontweight='bold',
                color='#303030',
                ha='center',
            )

            if show_confidence_value:

                ax.annotate(
                    'conf.',
                    xy=(
                        CONF_X,
                        1.0,
                    ),
                    xycoords='axes fraction',
                    xytext=(
                        0,
                        14,
                    ),
                    textcoords='offset points',
                    fontsize=8.2,
                    fontweight='bold',
                    color='#303030',
                    ha='center',
                )

        # =====================================================================
        # Observation counts
        # =====================================================================

        if (
            len(channels)
            <= MAX_CHANNELS_WITH_COUNTS
        ):

            # -----------------------------------------------------------------
            # Column headers
            # -----------------------------------------------------------------

            ax.annotate(
                "N Ctl",
                xy=(
                    N_CTL_X,
                    1.0,
                ),
                xycoords='axes fraction',
                xytext=(
                    0,
                    14,
                ),
                textcoords='offset points',
                fontsize=8.2,
                fontweight='bold',
                color=CTL_COLOUR,
                ha='center',
            )

            ax.annotate(
                "N Exp",
                xy=(
                    N_EXP_X,
                    1.0,
                ),
                xycoords='axes fraction',
                xytext=(
                    0,
                    14,
                ),
                textcoords='offset points',
                fontsize=8.2,
                fontweight='bold',
                color=EXP_COLOUR,
                ha='center',
            )

            # -----------------------------------------------------------------
            # Count values
            # -----------------------------------------------------------------

            for y in idlev:

                ax.text(
                    N_CTL_X,
                    y,
                    f"{int(n1[y])}",
                    fontsize=tick_fs,
                    color=CTL_COLOUR,
                    va='center',
                    ha='center',
                    transform=ax.get_yaxis_transform(),
                )

                ax.text(
                    N_EXP_X,
                    y,
                    f"{int(n2[y])}",
                    fontsize=tick_fs,
                    color=EXP_COLOUR,
                    va='center',
                    ha='center',
                    transform=ax.get_yaxis_transform(),
                )

        # =====================================================================
        # Figure header
        # =====================================================================

        def at(inch):
            return 1.0 - inch / fig_h

        def _when(stamp) -> str:
            s = str(stamp)
            return f"{s[:4]}-{s[4:6]}-{s[6:8]} {s[8:10]} UTC"

        what = {'omp_bias': 'bias of O-P', 'omp_rel': 'sigma of O-P',
                'oma_rel': 'sigma of O-A'}.get(metric, metric)
        x0, grey = left_in / fig_w, '#5F6B76'
        fig.text(x0, at(0.12), f"{varno_name(task['varno'])}  \u00b7  {what}",
                 ha='left', va='top', fontsize=15, fontweight='bold',
                 color='#1F2933')
        fig.text(0.985, at(0.14), f"{_when(task['datestart'])}  to  "
                 f"{_when(task['dateend'])}", ha='right', va='top',
                 fontsize=10.5, color=grey)
        fig.text(x0, at(0.45), "  \u00b7  ".join(
            [task['family'], f"{task['region']}{_land_special(task, ', ')}",
             f"flag {task['flag']}", f"platforms {task['id_stn']}"]),
            ha='left', va='top', fontsize=11, color=grey)
        t = fig.text(x0, at(0.72), f"Ctl  {name1}", ha='left', va='top',
                     fontsize=13, fontweight='bold', color=CTL_COLOUR)
        box = t.get_window_extent(renderer=fig.canvas.get_renderer())
        fig.text(fig.transFigure.inverted().transform((box.x1, box.y0))[0]
                 + 0.02, at(0.72), f"Exp  {name2}", ha='left', va='top',
                 fontsize=13, fontweight='bold', color=EXP_COLOUR)
        fig.text(x0, at(0.99),
                 "MATCH on: the tests on the observations both runs hold, "
                 "pair by pair" if pairs else
                 "MATCH off: each run with all its own observations; "
                 "F-test and Welch", ha='left', va='top', fontsize=10.5,
                 fontweight='semibold', color='#30343A')
        fig.add_artist(plt.Line2D([x0, 0.985], [at(1.24), at(1.24)],
                                  transform=fig.transFigure,
                                  color='#D9DDE2', linewidth=0.9))

        # =====================================================================
        # Legend
        # =====================================================================

        handles, labels = (
            ax.get_legend_handles_labels()
        )

        if handles:

            legend_y = (
                1.0
                - 1.32 / fig_h
            )

            fig.legend(
                handles,
                labels,
                loc='upper center',
                bbox_to_anchor=(
                    0.40,
                    legend_y,
                ),
                bbox_transform=fig.transFigure,
                ncol=min(
                    4,
                    len(handles),
                ),
                fontsize=9.0,
                frameon=False,
                columnspacing=1.4,
                handletextpad=0.5,
                handlelength=2.0,
                borderaxespad=0.0,
            )

        # =====================================================================
        # Save
        # =====================================================================

        rel = os.path.join(
            task['family'],
            (
                f"{metric}_"
                f"{_safe(task['family'])}_"
                f"{_safe(task.get('stn_tag', task['id_stn']))}_"
                f"{_safe(name1)}-{_safe(name2)}_"
                f"{_safe(task['region'])}{_land_special(task)}_"
                f"{_safe(task['flag'])}_"
                f"varno{int(task['varno'])}.png"
            ),
        )

        path = os.path.join(
            task['pathwork'],
            rel,
        )

        os.makedirs(
            os.path.dirname(path),
            exist_ok=True,
        )

        save_figure(
            fig,
            path,
            svg=task.get(
                'svg',
                False,
            ),
            dpi=DPI,
        )

        plt.close(
            fig
        )

        out.append(
            {
                'metric': metric,
                'filename': rel,
            }
        )

    return out


# =============================================================================
# Viewer
# =============================================================================

def vdedr_viewer_items(
    tasks: Sequence[Dict[str, Any]],
    results: Sequence[Any],
) -> List[Dict[str, str]]:
    """One viewer entry per figure actually written."""

    items: List[Dict[str, str]] = []

    for task, res in zip(
        tasks,
        results,
    ):

        if not res:
            continue

        for fig in res:

            items.append(
                {
                    'comparison':
                        task['comparison'],

                    'metric':
                        fig['metric'],

                    'family':
                        str(
                            task['family']
                        ).strip(),

                    'region':
                        str(
                            task['region']
                        ).strip(),

                    'land_ocean':
                        str(task.get('land_ocean', 'all')),

                    'special':
                        str(task.get('special_label', 'all')),

                    'flag':
                        str(
                            task['flag']
                        ).strip(),

                    'id_stn':
                        str(
                            task['id_stn']
                        ).strip(),

                    'varno':
                        str(
                            task['varno']
                        ).strip(),

                    'filename':
                        fig['filename'],
                }
            )

    return items
