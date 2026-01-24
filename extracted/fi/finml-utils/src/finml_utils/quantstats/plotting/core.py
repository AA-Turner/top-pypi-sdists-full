# original code: QuantStats: Portfolio analytics for quants
# https://github.com/ranaroussi/quantstats Copyright 2019-2023 Ran Aroussi
# Licensed originally under the Apache License, Version 2.0: http://www.apache.org/licenses/LICENSE-2.0

import contextlib

import matplotlib.dates as _mdates
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.patches import Rectangle
from matplotlib.ticker import FormatStrFormatter as _FormatStrFormatter
from matplotlib.ticker import FuncFormatter as _FuncFormatter

from .. import stats as _stats

sns.set_theme(
    font_scale=1.1,
    rc={
        "figure.figsize": (10, 6),
        "axes.facecolor": "white",
        "figure.facecolor": "white",
        "grid.color": "#dddddd",
        "grid.linewidth": 0.5,
        "lines.linewidth": 1.5,
        "text.color": "#333333",
        "xtick.color": "#666666",
        "ytick.color": "#666666",
    },
)

_FLATUI_COLORS = [
    "#FEDD78",
    "#348DC1",
    "#BA516B",
    "#4FA487",
    "#9B59B6",
    "#613F66",
    "#84B082",
    "#DC136C",
    "#559CAD",
    "#4A5899",
]
_GRAYSCALE_COLORS = [
    "#000000",
    "#222222",
    "#555555",
    "#888888",
    "#AAAAAA",
    "#CCCCCC",
    "#EEEEEE",
    "#333333",
    "#666666",
    "#999999",
]


def _get_colors(grayscale):
    colors = _FLATUI_COLORS
    ls = "-"
    alpha = 0.8
    if grayscale:
        colors = _GRAYSCALE_COLORS
        ls = "-"
        alpha = 0.5
    return colors, ls, alpha


def plot_returns_bars(  # noqa
    returns,
    benchmark=None,
    returns_label="Strategy",
    hline=None,
    hlw=None,
    hlcolor="red",
    hllabel="",
    resample="A",
    title="Returns",
    match_volatility=False,
    log_scale=False,
    figsize=(10, 6),
    grayscale=False,
    ylabel=True,
    subtitle=True,
    savefig=None,
):
    if match_volatility and benchmark is None:
        raise ValueError("match_volatility requires passing of " "benchmark.")
    if match_volatility and benchmark is not None:
        bmark_vol = benchmark.loc[returns.index].std()
        returns = (returns / returns.std()) * bmark_vol

    # ---------------
    colors, _, _ = _get_colors(grayscale)
    df = pd.DataFrame(index=returns.index, data={returns.name: returns})

    if isinstance(benchmark, pd.Series):
        df[benchmark.name] = benchmark[benchmark.index.isin(returns.index)]
        df = df[[benchmark.name, returns.name]]

    df = df.dropna()
    if resample is not None:
        df = df.resample(resample).apply(_stats.comp).resample(resample).last()
    # ---------------

    fig, ax = plt.subplots(figsize=figsize)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)

    # use a more precise date string for the x axis locations in the toolbar
    fig.suptitle(title, y=0.94, fontweight="bold", fontsize=14, color="black")

    if subtitle:
        ax.set_title(
            "{} - {}           \n".format(
                df.index.date[:1][0].strftime("%Y"),
                df.index.date[-1:][0].strftime("%Y"),
            ),
            fontsize=12,
            color="gray",
        )

    if benchmark is None:
        colors = colors[1:]
    df.plot(kind="bar", ax=ax, color=colors)

    fig.set_facecolor("white")
    ax.set_facecolor("white")

    try:
        ax.set_xticklabels(df.index.year)
        years = sorted(set(df.index.year))
    except AttributeError:
        ax.set_xticklabels(df.index)
        years = sorted(set(df.index))

    # ax.fmt_xdata = _mdates.DateFormatter('%Y-%m-%d')
    # years = sorted(list(set(df.index.year)))
    if len(years) > 10:
        mod = int(len(years) / 10)
        plt.xticks(
            np.arange(len(years)),
            [str(year) if not i % mod else "" for i, year in enumerate(years)],
        )

    # rotate and align the tick labels so they look better
    fig.autofmt_xdate()

    if hline is not None and not isinstance(hline, pd.Series):
        if grayscale:
            hlcolor = "gray"
        ax.axhline(hline, ls="--", lw=hlw, color=hlcolor, label=hllabel, zorder=2)

    ax.axhline(0, ls="--", lw=1, color="#000000", zorder=2)

    # if isinstance(benchmark, _pd.Series) or hline:
    ax.legend(fontsize=11)

    plt.yscale("symlog" if log_scale else "linear")

    ax.set_xlabel("")
    if ylabel:
        ax.set_ylabel("Returns", fontweight="bold", fontsize=12, color="black")
        ax.yaxis.set_label_coords(-0.1, 0.5)

    ax.yaxis.set_major_formatter(_FuncFormatter(format_pct_axis))

    if benchmark is None and len(pd.DataFrame(returns).columns) == 1:
        ax.get_legend().remove()

    with contextlib.suppress(Exception):
        plt.subplots_adjust(hspace=0, bottom=0, top=1)

    with contextlib.suppress(Exception):
        fig.tight_layout()

    if savefig:
        if isinstance(savefig, dict):
            plt.savefig(**savefig)
        else:
            plt.savefig(savefig)

    plt.close()
    return fig


def plot_timeseries(  # noqa
    returns,
    benchmark=None,
    title="Returns",
    compound=False,
    cumulative=True,
    fill=False,
    returns_label="Strategy",
    hline=None,
    hlw=None,
    hlcolor="red",
    hllabel="",
    percent=True,
    match_volatility=False,
    log_scale=False,
    resample=None,
    lw=1.5,
    figsize=(10, 6),
    ylabel: str = "",
    xlabel: str = "",
    grayscale=False,
    subtitle=True,
    savefig=None,
    marker: str | None = None,
    cutoff: pd.Timestamp | None = None,
):
    colors, ls, alpha = _get_colors(grayscale)

    returns = returns.fillna(0)
    if isinstance(benchmark, pd.Series):
        benchmark = benchmark.fillna(0)

    if match_volatility and benchmark is None:
        raise ValueError("match_volatility requires passing of " "benchmark.")
    if match_volatility and benchmark is not None:
        bmark_vol = benchmark.std()
        returns = (returns / returns.std()) * bmark_vol

    # ---------------
    if compound is True:
        if cumulative:
            returns = _stats.compsum(returns)
            if isinstance(benchmark, pd.Series):
                benchmark = _stats.compsum(benchmark)
        else:
            returns = returns.cumsum()
            if isinstance(benchmark, pd.Series):
                benchmark = benchmark.cumsum()

    if resample:
        returns = returns.resample(resample)
        returns = returns.last() if compound is True else returns.sum()
        if isinstance(benchmark, pd.Series):
            benchmark = benchmark.resample(resample)
            benchmark = benchmark.last() if compound is True else benchmark.sum()
    # ---------------

    fig, ax = plt.subplots(figsize=figsize)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)

    fig.suptitle(title, y=0.94, fontweight="bold", fontsize=14, color="black")

    if subtitle:
        ax.set_title(
            "{} - {}            \n".format(
                returns.index.date[:1][0].strftime("%e %b '%y"),
                returns.index.date[-1:][0].strftime("%e %b '%y"),
            ),
            fontsize=12,
            color="gray",
        )

    fig.set_facecolor("white")
    ax.set_facecolor("white")

    if isinstance(benchmark, pd.Series):
        ax.plot(
            benchmark,
            lw=lw,
            ls=ls,
            label=benchmark.name,
            color=colors[0],
            marker=marker,
        )

    alpha = 0.25 if grayscale else 1
    ax.plot(
        returns, lw=lw, label=returns.name, color=colors[1], alpha=alpha, marker=marker
    )

    if fill:
        ax.fill_between(returns.index, 0, returns, color=colors[1], alpha=0.25)

    # rotate and align the tick labels so they look better
    fig.autofmt_xdate()

    # use a more precise date string for the x axis locations in the toolbar
    # ax.fmt_xdata = _mdates.DateFormatter('%Y-%m-%d')

    if hline is not None and not isinstance(hline, pd.Series):
        if grayscale:
            hlcolor = "black"
        ax.axhline(hline, ls="--", lw=hlw, color=hlcolor, label=hllabel, zorder=2)

    ax.axhline(0, ls="-", lw=1, color="gray", zorder=1)
    ax.axhline(0, ls="--", lw=1, color="white" if grayscale else "black", zorder=2)

    # if isinstance(benchmark, _pd.Series) or hline is not None:
    ax.legend(fontsize=11)

    plt.yscale("symlog" if log_scale else "linear")

    if percent:
        ax.yaxis.set_major_formatter(_FuncFormatter(format_pct_axis))
        # ax.yaxis.set_major_formatter(_plt.FuncFormatter(
        #     lambda x, loc: "{:,}%".format(int(x*100))))

    ax.set_xlabel(xlabel, fontweight="bold", fontsize=12, color="black")
    if isinstance(returns.index[0], int):
        ax.xticks(returns.index)
    if ylabel:
        ax.set_ylabel(ylabel, fontweight="bold", fontsize=12, color="black")
    ax.yaxis.set_label_coords(-0.1, 0.5)

    if benchmark is None and len(pd.DataFrame(returns).columns) == 1:
        ax.get_legend().remove()

    if cutoff is not None:
        plot_is_oos_line(ax, cutoff)

    with contextlib.suppress(Exception):
        plt.subplots_adjust(hspace=0, bottom=0, top=1)

    with contextlib.suppress(Exception):
        fig.tight_layout()

    if savefig:
        if isinstance(savefig, dict):
            plt.savefig(**savefig)
        else:
            plt.savefig(savefig)

    plt.close()

    return fig


def plot_histogram(
    returns,
    benchmark,
    resample="ME",
    bins=20,
    grayscale=False,
    title="Returns",
    kde=True,
    figsize=(10, 6),
    ylabel=True,
    subtitle=True,
    compounded=True,
    savefig=None,
):
    # colors = ['#348dc1', '#003366', 'red']
    # if grayscale:
    #     colors = ['silver', 'gray', 'black']

    colors, _, _ = _get_colors(grayscale)

    apply_fnc = _stats.comp if compounded else np.sum
    if benchmark is not None:
        benchmark = (
            benchmark.fillna(0)
            .resample(resample)
            .apply(apply_fnc)
            .resample(resample)
            .last()
        )

    returns = (
        returns.fillna(0).resample(resample).apply(apply_fnc).resample(resample).last()
    )

    figsize = (0.995 * figsize[0], figsize[1])
    fig, ax = plt.subplots(figsize=figsize)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)

    fig.suptitle(title, y=0.94, fontweight="bold", fontsize=14, color="black")

    if subtitle:
        ax.set_title(
            "{} - {}           \n".format(
                returns.index.date[:1][0].strftime("%Y-%m-%d"),
                returns.index.date[-1:][0].strftime("%Y-%m-%d"),
            ),
            fontsize=10,
            color="gray",
        )

    fig.set_facecolor("white")
    ax.set_facecolor("white")

    if isinstance(returns, pd.DataFrame) and len(returns.columns) == 1:
        returns = returns[returns.columns[0]]

    pallete = colors[1:2] if benchmark is None else colors[:2]
    alpha = 0.7

    if benchmark is not None:
        combined_returns = (
            benchmark.to_frame()  # noqa
            .join(returns.to_frame())
            .stack()
            .reset_index()
            .rename(columns={"level_1": "", 0: "Returns"})
        )

        sns.histplot(
            data=combined_returns,
            x="Returns",
            bins=bins,
            alpha=alpha,
            kde=kde,
            stat="density",
            hue="",
            palette=pallete,
            ax=ax,
        )

    else:
        combined_returns = returns.copy()
        if kde:
            sns.kdeplot(data=combined_returns, color="black", ax=ax)
        sns.histplot(
            data=combined_returns,
            bins=bins,
            alpha=alpha,
            kde=False,
            stat="density",
            color=colors[1],
            ax=ax,
        )

    # Why do we need average?
    if isinstance(combined_returns, pd.Series) or len(combined_returns.columns) == 1:
        ax.axvline(
            combined_returns.mean(),
            ls="--",
            lw=1.5,
            zorder=2,
            label="Average",
            color="red",
        )

    # _plt.setp(x.get_legend().get_texts(), fontsize=11)
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f"{int(x * 100):,}%"))  # noqa

    # Removed static lines for clarity
    # ax.axhline(0.01, lw=1, color="#000000", zorder=2)
    # ax.axvline(0, lw=1, color="#000000", zorder=2)

    ax.set_xlabel("")
    ax.set_ylabel("Occurrences", fontweight="bold", fontsize=12, color="black")
    ax.yaxis.set_label_coords(-0.1, 0.5)

    # fig.autofmt_xdate()

    with contextlib.suppress(Exception):
        plt.subplots_adjust(hspace=0, bottom=0, top=1)

    with contextlib.suppress(Exception):
        fig.tight_layout()

    if savefig:
        if isinstance(savefig, dict):
            plt.savefig(**savefig)
        else:
            plt.savefig(savefig)

    plt.close()
    return fig


def plot_is_oos_line(ax, cutoff: pd.Timestamp) -> None:
    ax.axvline(cutoff, ls="--", lw=1, color="gray", zorder=2)
    ax.text(
        cutoff - pd.Timedelta(days=15),
        0.98,
        "IS",
        ha="right",
        va="center",
        color="gray",
        fontsize=8,
        transform=ax.get_xaxis_transform(),
    )
    ax.text(
        cutoff + pd.Timedelta(days=15),
        0.98,
        "OOS",
        ha="left",
        va="center",
        color="gray",
        fontsize=8,
        transform=ax.get_xaxis_transform(),
    )
    max_x = ax.get_xlim()[1]

    min_y, max_y = ax.get_ylim()

    # Create the rectangle
    rect = Rectangle(
        (mdates.date2num(cutoff), min_y),
        max_x - mdates.date2num(cutoff),  # Width: from cutoff to the right edge
        max_y - min_y,  # Height: full height of the graph
        color="black",
        alpha=1.0,
        transform=ax.transData,  # Use data coordinates for both x and y
    )
    rect.set_zorder(2)
    rect.set_gid("overlayRect")  # Assign unique ID
    ax.add_patch(rect)


def plot_rolling_stats(
    returns: pd.Series,
    benchmark: pd.Series | None = None,
    title: str = "",
    returns_label: str = "Strategy",
    hline=None,
    hlw=None,
    hlcolor: str = "red",
    hllabel: str = "",
    lw: float = 1.5,
    figsize: tuple[int, int] = (10, 6),
    ylabel: str = "",
    grayscale: bool = False,
    subtitle: bool = True,
    savefig: bool | None = None,
    cutoff: pd.Timestamp | None = None,
    reference_line: float = 0.0,
):
    colors, _, _ = _get_colors(grayscale)

    fig, ax = plt.subplots(figsize=figsize)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)

    df = pd.DataFrame(index=returns.index, data={returns_label: returns})

    if isinstance(benchmark, pd.Series):
        df["Benchmark"] = benchmark[benchmark.index.isin(returns.index)]
        df = df[["Benchmark", returns_label]].dropna()
        ax.plot(df[returns_label].dropna(), lw=lw, label=returns.name, color=colors[1])
        ax.plot(
            df["Benchmark"], lw=lw, label=benchmark.name, color=colors[0], alpha=0.8
        )
    else:
        df = df[[returns_label]].dropna()
        ax.plot(df[returns_label].dropna(), lw=lw, label=returns.name, color=colors[1])

    # rotate and align the tick labels so they look better
    fig.autofmt_xdate()

    # use a more precise date string for the x axis locations in the toolbar
    # ax.fmt_xdata = _mdates.DateFormatter('%Y-%m-%d')\
    fig.suptitle(title, y=0.94, fontweight="bold", fontsize=14, color="black")

    if subtitle:
        ax.set_title(
            "{} - {}           \n".format(
                df.index.date[:1][0].strftime("%e %b '%y"),
                df.index.date[-1:][0].strftime("%e %b '%y"),
            ),
            fontsize=12,
            color="gray",
        )

    if hline is not None and not isinstance(hline, pd.Series):
        if grayscale:
            hlcolor = "black"
        ax.axhline(hline, ls="--", lw=hlw, color=hlcolor, label=hllabel, zorder=2)

    ax.axhline(reference_line, ls="--", lw=1, color="#000000", zorder=2)

    if ylabel:
        ax.set_ylabel(ylabel, fontweight="bold", fontsize=12, color="black")
        ax.yaxis.set_label_coords(-0.1, 0.5)

    ax.yaxis.set_major_formatter(_FormatStrFormatter("%.2f"))

    ax.legend(fontsize=11)

    if benchmark is None and len(pd.DataFrame(returns).columns) == 1:
        ax.get_legend().remove()

    if cutoff is not None:
        plot_is_oos_line(ax, cutoff)

    with contextlib.suppress(Exception):
        plt.subplots_adjust(hspace=0, bottom=0, top=1)

    with contextlib.suppress(Exception):
        fig.tight_layout()

    if savefig:
        if isinstance(savefig, dict):
            plt.savefig(**savefig)
        else:
            plt.savefig(savefig)
    plt.close()
    return fig


def plot_rolling_beta(
    returns,
    benchmark,
    window1=126,
    window1_label="",
    window2=None,
    window2_label="",
    title="",
    hlcolor="red",
    figsize=(10, 6),
    grayscale=False,
    lw=1.5,
    ylabel=True,
    subtitle=True,
    savefig=None,
    cutoff: pd.Timestamp | None = None,
):
    colors, _, _ = _get_colors(grayscale)

    fig, ax = plt.subplots(figsize=figsize)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)

    fig.suptitle(title, y=0.94, fontweight="bold", fontsize=14, color="black")

    if subtitle:
        ax.set_title(
            "{} - {}           \n".format(
                returns.index.date[:1][0].strftime("%e %b '%y"),
                returns.index.date[-1:][0].strftime("%e %b '%y"),
            ),
            fontsize=12,
            color="gray",
        )

    beta = _stats.rolling_greeks(returns, benchmark, window1)["beta"].fillna(0)
    ax.plot(beta, lw=lw, label=window1_label, color=colors[1])

    if window2:
        lw = lw - 0.5
        ax.plot(
            _stats.rolling_greeks(returns, benchmark, window2)["beta"],
            lw=lw,
            label=window2_label,
            color="gray",
            alpha=0.8,
        )

    beta_min = (
        beta.min()
        if isinstance(returns, pd.Series)
        else min([b.min() for b in beta.values()])
    )
    beta_max = (
        beta.max()
        if isinstance(returns, pd.Series)
        else max([b.max() for b in beta.values()])
    )
    mmin = min([-100, int(beta_min * 100)])
    mmax = max([100, int(beta_max * 100)])
    step = 50 if (mmax - mmin) >= 200 else 100
    ax.set_yticks([x / 100 for x in list(range(mmin, mmax, step))])

    if isinstance(returns, pd.Series):
        hlcolor = "black" if grayscale else hlcolor
        ax.axhline(beta.mean(), ls="--", lw=1.5, color=hlcolor, zorder=2)

    ax.axhline(0, ls="--", lw=1, color="#000000", zorder=2)

    fig.autofmt_xdate()

    # use a more precise date string for the x axis locations in the toolbar
    ax.fmt_xdata = _mdates.DateFormatter("%Y-%m-%d")

    if ylabel:
        ax.set_ylabel("Beta", fontweight="bold", fontsize=12, color="black")
        ax.yaxis.set_label_coords(-0.1, 0.5)

    ax.legend(fontsize=11)
    if benchmark is None and len(pd.DataFrame(returns).columns) == 1:
        ax.get_legend().remove()

    if cutoff is not None:
        plot_is_oos_line(ax, cutoff)

    with contextlib.suppress(Exception):
        plt.subplots_adjust(hspace=0, bottom=0, top=1)

    with contextlib.suppress(Exception):
        fig.tight_layout()

    if savefig:
        if isinstance(savefig, dict):
            plt.savefig(**savefig)
        else:
            plt.savefig(savefig)

    plt.close()
    return fig


def plot_longest_drawdowns(
    returns,
    periods=5,
    lw=1.5,
    grayscale=False,
    title=None,
    log_scale=False,
    figsize=(10, 6),
    ylabel=True,
    subtitle=True,
    compounded=True,
    savefig=None,
    cutoff: pd.Timestamp | None = None,
):
    colors = ["#348dc1", "#003366", "red"]
    if grayscale:
        colors = ["#000000"] * 3

    dd = _stats.to_drawdown_series(returns.fillna(0))
    dddf = _stats.drawdown_details(dd)
    longest_dd = dddf.sort_values(by="days", ascending=False, kind="mergesort")[
        :periods
    ]

    fig, ax = plt.subplots(figsize=figsize)

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)

    fig.suptitle(
        f"{title} - Worst %.0f Drawdown Periods" % periods,
        y=0.94,
        fontweight="bold",
        fontsize=14,
        color="black",
    )
    if subtitle:
        ax.set_title(
            "{} - {}           \n".format(
                returns.index.date[:1][0].strftime("%e %b '%y"),
                returns.index.date[-1:][0].strftime("%e %b '%y"),
            ),
            fontsize=12,
            color="gray",
        )

    fig.set_facecolor("white")
    ax.set_facecolor("white")
    series = _stats.compsum(returns) if compounded else returns.cumsum()
    ax.plot(series, lw=lw, label="Backtest", color=colors[0])

    highlight = "black" if grayscale else "red"
    for _, row in longest_dd.iterrows():
        ax.axvspan(
            *_mdates.datestr2num([str(row["start"]), str(row["end"])]),
            color=highlight,
            alpha=0.1,
        )

    # rotate and align the tick labels so they look better
    fig.autofmt_xdate()

    # use a more precise date string for the x axis locations in the toolbar
    ax.fmt_xdata = _mdates.DateFormatter("%Y-%m-%d")

    ax.axhline(0, ls="--", lw=1, color="#000000", zorder=2)
    plt.yscale("symlog" if log_scale else "linear")
    if ylabel:
        ax.set_ylabel(
            "Cumulative Returns",
            fontweight="bold",
            fontsize=12,
            color="black",
        )
        ax.yaxis.set_label_coords(-0.1, 0.5)

    ax.yaxis.set_major_formatter(_FuncFormatter(format_pct_axis))
    # ax.yaxis.set_major_formatter(_plt.FuncFormatter(
    #     lambda x, loc: "{:,}%".format(int(x*100))))

    fig.autofmt_xdate()

    if cutoff is not None:
        plot_is_oos_line(ax, cutoff)

    with contextlib.suppress(Exception):
        plt.subplots_adjust(hspace=0, bottom=0, top=1)

    with contextlib.suppress(Exception):
        fig.tight_layout()

    if savefig:
        if isinstance(savefig, dict):
            plt.savefig(**savefig)
        else:
            plt.savefig(savefig)

    plt.close()
    return fig


def plot_horizontal_bar(  # noqa
    df: pd.DataFrame,
    result_col: str,
    comparison_col: str,
    title: str,
    figsize=(10, 9),
    savefig=None,
):
    def handle_range(x: str) -> str:
        category = ""
        if "%" in x:
            category += "precentage-"
        if x[0] == "-":
            category += "negative"
        else:
            category += "positive"
        return category

    df["xlim_category"] = df["Strategy"].apply(lambda x: handle_range(x))
    grouped = df.groupby(by="xlim_category")
    fig, ax = plt.subplots(nrows=len(grouped), figsize=figsize, sharex=False)
    for i, (name, group) in enumerate(grouped):
        group = group[[result_col, comparison_col]]  # noqa
        if name == "precentage-negative":
            group[result_col] = group[result_col].apply(
                lambda x: float(x.replace("%", ""))
            )
            group[comparison_col] = group[comparison_col].apply(
                lambda x: float(x.replace("%", ""))
            )
            xlim = (0, -100)
            ax[i].yaxis.set_major_formatter(_FuncFormatter(format_pct_axis))
        elif name == "precentage-positive":
            group[result_col] = group[result_col].apply(
                lambda x: float(x.replace("%", ""))
            )
            group[comparison_col] = group[comparison_col].apply(
                lambda x: float(x.replace("%", ""))
            )
            xlim = (0, 100)
            ax[i].yaxis.set_major_formatter(_FuncFormatter(format_pct_axis))
        elif name == "negative":
            group = group.astype(float)  # noqa
            xlim = (0, -1)
        elif name == "positive":
            group = group.astype(float)  # noqa
            xlim = (0, 3)
        else:
            raise ValueError(f"Unknown category {name}")
        ax[i].set(xlim=xlim, ylabel="", xlabel="")
        ax[i].set_facecolor("white")
        sns.set_color_codes("pastel")

        group["index"] = group.index
        sns.barplot(
            x=result_col,
            y="index",
            data=group,
            label=result_col,
            color="g",
            ax=ax[i],
            alpha=1.0,
        ).set(xlabel=None, ylabel=None)

        sns.set_color_codes("muted")
        sns.barplot(
            x=comparison_col,
            y="index",
            data=group,
            label=comparison_col,
            color="gray",
            ax=ax[i],
            alpha=0.2,
        ).set(xlabel=None, ylabel=None)
        if i == 0:
            ax[i].legend(ncol=2, loc="upper right", frameon=True)
        else:
            ax[i].get_legend().remove()

    # _sns.despine(left=True, bottom=True)

    fig.set_facecolor("white")
    fig.suptitle(title, y=0.94, fontweight="bold", fontsize=14, color="black")

    with contextlib.suppress(Exception):
        plt.subplots_adjust(hspace=0)
    with contextlib.suppress(Exception):
        fig.tight_layout(w_pad=0, h_pad=0)

    if savefig:
        if isinstance(savefig, dict):
            plt.savefig(**savefig)
        else:
            plt.savefig(savefig)
    plt.close()
    return fig


def plot_distribution(
    returns,
    figsize=(10, 6),
    grayscale=False,
    ylabel=True,
    subtitle=True,
    compounded=True,
    title=None,
    savefig=None,
):
    colors = _FLATUI_COLORS
    if grayscale:
        colors = ["#f9f9f9", "#dddddd", "#bbbbbb", "#999999", "#808080"]
    # colors, ls, alpha = _get_colors(grayscale)

    port = pd.DataFrame(returns.fillna(0))
    port.columns = ["Daily"]

    apply_fnc = _stats.comp if compounded else np.sum

    port["Weekly"] = port["Daily"].resample("W-MON").apply(apply_fnc)
    port["Weekly"] = port["Weekly"].ffill()

    port["Monthly"] = port["Daily"].resample("ME").apply(apply_fnc)
    port["Monthly"] = port["Monthly"].ffill()

    port["Quarterly"] = port["Daily"].resample("QE").apply(apply_fnc)
    port["Quarterly"] = port["Quarterly"].ffill()

    port["Yearly"] = port["Daily"].resample("YE").apply(apply_fnc)
    port["Yearly"] = port["Yearly"].ffill()

    fig, ax = plt.subplots(figsize=figsize)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_visible(False)
    ax.spines["left"].set_visible(False)

    title = f"{title} - Return Quantiles" if title else "Return Quantiles"
    fig.suptitle(title, y=0.94, fontweight="bold", fontsize=14, color="black")

    if subtitle:
        ax.set_title(
            "{} - {}            \n".format(
                returns.index.date[:1][0].strftime("%e %b '%y"),
                returns.index.date[-1:][0].strftime("%e %b '%y"),
            ),
            fontsize=12,
            color="gray",
        )

    fig.set_facecolor("white")
    ax.set_facecolor("white")

    sns.boxplot(
        data=port,
        ax=ax,
        palette={
            "Daily": colors[0],
            "Weekly": colors[1],
            "Monthly": colors[2],
            "Quarterly": colors[3],
            "Yearly": colors[4],
        },
    )

    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, loc: f"{int(x * 100):,}%"))  # noqa

    if ylabel:
        ax.set_ylabel("Returns", fontweight="bold", fontsize=12, color="black")
        ax.yaxis.set_label_coords(-0.1, 0.5)

    fig.autofmt_xdate()

    with contextlib.suppress(Exception):
        plt.subplots_adjust(hspace=0)
    with contextlib.suppress(Exception):
        fig.tight_layout(w_pad=0, h_pad=0)

    if savefig:
        if isinstance(savefig, dict):
            plt.savefig(**savefig)
        else:
            plt.savefig(savefig)
    plt.close()
    return fig


def plot_table(
    tbl,
    columns=None,
    title="",
    title_loc="left",
    header=True,
    colWidths=None,
    rowLoc="right",
    colLoc="right",
    colLabels=None,
    edges="horizontal",
    orient="horizontal",
    figsize=(5.5, 6),
    savefig=None,
):
    if columns is not None:
        with contextlib.suppress(Exception):
            tbl.columns = columns

    fig = plt.figure(figsize=figsize)
    ax = plt.subplot(111, frame_on=False)

    if title != "":
        ax.set_title(
            title, fontweight="bold", fontsize=14, color="black", loc=title_loc
        )

    the_table = ax.table(
        cellText=tbl.values,
        colWidths=colWidths,
        rowLoc=rowLoc,
        colLoc=colLoc,
        edges=edges,
        colLabels=(tbl.columns if header else colLabels),
        loc="center",
        zorder=2,
    )

    the_table.auto_set_font_size(False)
    the_table.set_fontsize(12)
    the_table.scale(1, 1)

    for (row, col), cell in the_table.get_celld().items():
        cell.set_height(0.08)
        cell.set_text_props(color="black")
        cell.set_edgecolor("#dddddd")
        if row == 0 and header:
            cell.set_edgecolor("black")
            cell.set_facecolor("black")
            cell.set_linewidth(2)
            cell.set_text_props(weight="bold", color="black")
        elif col == 0 and "vertical" in orient:
            cell.set_edgecolor("#dddddd")
            cell.set_linewidth(1)
            cell.set_text_props(weight="bold", color="black")
        elif row > 1:
            cell.set_linewidth(1)

    ax.grid(False)
    ax.set_xticks([])
    ax.set_yticks([])

    with contextlib.suppress(Exception):
        plt.subplots_adjust(hspace=0)
    with contextlib.suppress(Exception):
        fig.tight_layout(w_pad=0, h_pad=0)

    if savefig:
        if isinstance(savefig, dict):
            plt.savefig(**savefig)
        else:
            plt.savefig(savefig)

    plt.close()
    return fig


def format_cur_axis(x, _):
    if x >= 1e12:
        res = "$%1.1fT" % (x * 1e-12)
        return res.replace(".0T", "T")
    if x >= 1e9:
        res = "$%1.1fB" % (x * 1e-9)
        return res.replace(".0B", "B")
    if x >= 1e6:
        res = "$%1.1fM" % (x * 1e-6)
        return res.replace(".0M", "M")
    if x >= 1e3:
        res = "$%1.0fK" % (x * 1e-3)
        return res.replace(".0K", "K")
    res = f"${x:1.0f}"
    return res.replace(".0", "")


def format_pct_axis(x, _):
    x *= 100  # lambda x, loc: "{:,}%".format(int(x * 100))
    if x >= 1e12:
        res = "%1.1fT%%" % (x * 1e-12)
        return res.replace(".0T%", "T%")
    if x >= 1e9:
        res = "%1.1fB%%" % (x * 1e-9)
        return res.replace(".0B%", "B%")
    if x >= 1e6:
        res = "%1.1fM%%" % (x * 1e-6)
        return res.replace(".0M%", "M%")
    if x >= 1e3:
        res = "%1.1fK%%" % (x * 1e-3)
        return res.replace(".0K%", "K%")
    res = f"{x:1.0f}%"
    return res.replace(".0%", "%")
