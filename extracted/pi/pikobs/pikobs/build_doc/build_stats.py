#!/usr/bin/env python3
"""Draw the figure of the statistics page: what each test sees.

    python build_stats_figure.py docs/source/_static/stats_tests.png

Three panels, with the control in blue and the experience in red:

* the bias moved and the sigma did not  -> the t-test sees it
* the sigma changed and the bias did not -> the F-test sees it
* the two runs share their observations   -> why pairing is sharper

The numbers come from the module itself, so the confidences printed on
the figure are the ones Pikobs would report.
"""

import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

from pikobs.stats import (ftest_confidence, paired_ttest_confidence,
                          ttest_confidence)

CTL = '#2166AC'
EXP = '#B2182B'
GREY = '#666666'
N = 400


def _bell(ax, mu, sigma, colour, label, style='-'):
    x = np.linspace(-5, 5, 400)
    y = np.exp(-0.5 * ((x - mu) / sigma) ** 2) / (sigma * np.sqrt(2 * np.pi))
    ax.plot(x, y, style, color=colour, lw=2.2, label=label)
    ax.fill_between(x, y, color=colour, alpha=0.12)
    ax.axvline(mu, color=colour, lw=1.0, ls=':', alpha=0.8)
    return y.max()


def main(out_png: str) -> None:
    fig, axes = plt.subplots(1, 3, figsize=(16.5, 5.2), facecolor='white')
    ax1, ax2, ax3 = axes

    # ---- the bias moved -------------------------------------------------
    m1, m2, sig = 0.30, -0.30, 1.20
    top = max(_bell(ax1, m1, sig, CTL, 'control'),
              _bell(ax1, m2, sig, EXP, 'experience', '-'))
    t_conf = ttest_confidence([m1], [sig], [N], [m2], [sig], [N])[0]
    f_conf = ftest_confidence([sig], [N], [sig], [N])[0]
    ax1.annotate('', xy=(m2, top * 0.55), xytext=(m1, top * 0.55),
                 arrowprops=dict(arrowstyle='<->', color=GREY, lw=2.0))
    ax1.text((m1 + m2) / 2, top * 0.60, 'the centre moved', ha='center',
             color=GREY, fontsize=11, fontweight='bold')
    ax1.set_ylim(0, top * 1.15)
    ax1.set_title('The bias moved, the sigma did not\n'
                  f't-test {t_conf:.1f} %   |   F-test '
                  f'{0.0 if not np.isfinite(f_conf) else f_conf:.1f} %',
                  fontsize=12, fontweight='bold')

    # ---- the sigma changed ---------------------------------------------
    s1, s2 = 1.20, 0.85
    top = max(_bell(ax2, 0.0, s1, CTL, 'control'),
              _bell(ax2, 0.0, s2, EXP, 'experience'))
    t_conf2 = ttest_confidence([0.0], [s1], [N], [0.0], [s2], [N])[0]
    f_conf2 = ftest_confidence([s1], [N], [s2], [N])[0]
    for sign in (-1, 1):
        ax2.annotate('', xy=(sign * s2, top * 0.30),
                     xytext=(sign * s1 * 1.6, top * 0.30),
                     arrowprops=dict(arrowstyle='<->', color=GREY, lw=2.0))
    ax2.text(0.0, top * 0.37, 'the width changed', ha='center', color=GREY,
             fontsize=11, fontweight='bold')
    ax2.set_ylim(0, top * 1.15)
    ax2.set_title('The sigma changed, the bias did not\n'
                  f't-test {t_conf2:.1f} %   |   F-test {f_conf2:.1f} %',
                  fontsize=12, fontweight='bold')

    for ax in (ax1, ax2):
        ax.set_xlabel('departure  [K]', fontsize=11)
        ax.set_ylabel('density', fontsize=11)
        ax.legend(fontsize=10, frameon=False, loc='upper right')
        ax.grid(True, ls=':', alpha=0.4)

    # ---- why pairing is sharper -----------------------------------------
    rng = np.random.default_rng(3)
    base = rng.normal(0.0, 1.20, N)
    ctl = base + 0.30
    exp = base * 0.999 + 0.24 + rng.normal(0, 0.38, N)   # correlated runs
    r = float(np.corrcoef(ctl, exp)[0, 1])
    welch = ttest_confidence([ctl.mean()], [ctl.std()], [N],
                             [exp.mean()], [exp.std()], [N])[0]
    cov = float(np.cov(ctl, exp, bias=True)[0, 1])
    paired = paired_ttest_confidence([ctl.mean()], [exp.mean()],
                                     [ctl.var()], [exp.var()], [cov], [N])[0]
    ax3.scatter(ctl, exp, s=12, color=GREY, alpha=0.45, linewidths=0)
    lim = [-4.5, 4.5]
    ax3.plot(lim, lim, color='black', lw=1.0, ls='--',
             label='no change at all')
    ax3.set_xlim(lim)
    ax3.set_ylim(lim)
    ax3.set_xlabel('departure, control  [K]', fontsize=11)
    ax3.set_ylabel('departure, experience  [K]', fontsize=11)
    ax3.grid(True, ls=':', alpha=0.4)
    ax3.legend(fontsize=10, frameon=False, loc='upper left')
    ax3.set_title('The same observations, seen twice\n'
                  f'correlation {r:.2f}   |   Welch {welch:.1f} %   |   '
                  f'paired {paired:.1f} %', fontsize=12, fontweight='bold')
    ax3.text(0.98, 0.04,
             'each dot is one observation:\nthe pair cancels what the two\n'
             'runs have in common',
             transform=ax3.transAxes, ha='right', va='bottom', fontsize=10,
             color=GREY,
             bbox=dict(facecolor='white', edgecolor='#cccccc',
                       boxstyle='round,pad=0.4'))

    fig.suptitle('What each test sees, on 400 observations',
                 fontsize=15, fontweight='bold')
    fig.tight_layout(rect=(0, 0, 1, 0.93))
    fig.savefig(out_png, dpi=110, facecolor='white')
    plt.close(fig)
    print(f"written: {out_png}")


if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1
         else 'docs/source/_static/stats_tests.png')
