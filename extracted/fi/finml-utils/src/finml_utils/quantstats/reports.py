# original code: QuantStats: Portfolio analytics for quants
# https://github.com/ranaroussi/quantstats Copyright 2019-2023 Ran Aroussi
# Licensed originally under the Apache License, Version 2.0: http://www.apache.org/licenses/LICENSE-2.0
import contextlib
import re as _regex
from base64 import b64encode as _b64encode
from dataclasses import dataclass
from datetime import date
from datetime import datetime as _dt
from math import ceil as _ceil
from pathlib import Path
from typing import Literal

import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from tabulate import tabulate as _tabulate

from .. import stats
from . import stats as _stats
from . import utils as _utils
from .plotting.core import plot_horizontal_bar
from .plotting.wrappers import (
    drawdown,
    plot_component_heatmap,
    plot_daily_returns,
    plot_distribution,
    plot_drawdowns_periods,
    plot_histogram,
    plot_log_returns,
    plot_monthly_heatmap,
    plot_returns,
    plot_rolling_beta,
    plot_rolling_net_exposure,
    plot_rolling_sharpe,
    plot_rolling_volatility,
    plot_series,
    plot_yearly_returns,
)

with contextlib.suppress(ImportError):
    pass


def _get_trading_periods(periods_per_year: int = 252) -> tuple[int, int]:
    half_year = _ceil(periods_per_year / 2)
    return periods_per_year, half_year


def _match_dates(
    returns: pd.DataFrame | pd.Series, benchmark: pd.Series
) -> tuple[pd.DataFrame | pd.Series, pd.Series]:
    if isinstance(returns, pd.DataFrame):
        loc = max(returns[returns.columns[0]].ne(0).idxmax(), benchmark.ne(0).idxmax())
    else:
        loc = max(returns.ne(0).idxmax(), benchmark.ne(0).idxmax())
    returns = returns.loc[loc:]
    benchmark = benchmark.loc[loc:]

    return returns, benchmark


@dataclass(frozen=True)
class HTMLReport:
    source_code: str

    def write_html(self, full_path: Path | str) -> None:
        with open(full_path, "w", encoding="utf-8") as file:  # noqa
            file.write(str(self.source_code) + "\n")


def html(  # noqa
    returns: pd.Series,
    benchmark: pd.Series,
    weights: pd.DataFrame | None,
    metadata: str | None = None,
    delayed_sharpes: pd.Series | None = None,
    before_fee_returns: pd.Series | None = None,
    rf: float = 0.0,
    grayscale: bool = False,
    title: str = "Portfolio Tearsheet",
    subtitle: str = "",
    compounded: bool = True,
    periods_per_year=252,
    figfmt="svg",
    template_path=None,
    match_dates: bool = True,
    comparison_metrics: list[str] | None = None,
    background_dark: bool = False,
    component_level_stats: pd.DataFrame | None = None,
    component_returns_df: pd.DataFrame | None = None,
    cutoff: date | None = None,
    init_overlay_opacity: float = 0.0,
    no_overlay_toggle_button: bool = False,
    **kwargs,
) -> HTMLReport:
    cutoff = pd.Timestamp(cutoff) if isinstance(cutoff, date | _dt) else cutoff
    pd.options.mode.copy_on_write = False
    if match_dates:
        returns = returns.dropna()
    if init_overlay_opacity > 0.6:
        assert (
            no_overlay_toggle_button is False
        ), f"OOS period will never be visible without overlay toggle button and {init_overlay_opacity=}"

    win_year, win_half_year = _get_trading_periods(periods_per_year)

    tpl = ""
    with open(template_path or __file__[:-4] + ".html") as f:  # noqa
        tpl = f.read()
        f.close()

    tpl = tpl.replace(
        "{{background_color}}", "#141b2cff" if background_dark else "white"
    )
    tpl = tpl.replace("{{text_color}}", "white" if background_dark else "black")
    tpl = tpl.replace(
        "{{table_header_color}}", "#0e131fff" if background_dark else "#eee"
    )
    # prepare timeseries
    if match_dates:
        returns = returns.dropna()

    if cutoff is not None and (
        min(returns.index) > cutoff
        or (benchmark is not None and min(benchmark.index) > cutoff)
    ):
        cutoff = None

    strategy_title = kwargs.get("strategy_title", "Strategy")
    if isinstance(returns, pd.DataFrame):  # noqa
        if len(returns.columns) > 1 and isinstance(strategy_title, str):
            strategy_title = list(returns.columns)

    if benchmark is not None:
        benchmark_title = kwargs.get("benchmark_title", "Benchmark")
        if kwargs.get("benchmark_title") is None:
            if isinstance(benchmark, str):
                benchmark_title = benchmark
            elif isinstance(benchmark, pd.Series):
                benchmark_title = benchmark.name
            elif isinstance(benchmark, pd.DataFrame):
                benchmark_title = benchmark[benchmark.columns[0]].name

        if match_dates is True:
            returns, benchmark = _match_dates(returns, benchmark)
    else:
        benchmark_title = None

    date_range = returns.index.strftime("%e %b, %Y")
    tpl = tpl.replace("{{date_range}}", date_range[0] + " - " + date_range[-1])
    tpl = tpl.replace("{{title}}", f"<b>{title}</b> {subtitle}")
    tpl = tpl.replace("{{site_title}}", f"{title}{subtitle}")
    tpl = tpl.replace("{{init_overlay_opacity}}", str(init_overlay_opacity))
    tpl = tpl.replace(
        "{{button_display}}",
        "none" if (cutoff is None or no_overlay_toggle_button) else "block",
    )
    tpl = tpl.replace(
        "{{init_table_row_overlay_color}}",
        "black" if init_overlay_opacity > 0 else "#F0F8FF",
    )
    tpl = tpl.replace(
        "{{init_table_row_font_color}}",
        "black" if init_overlay_opacity > 0 else "#003366",
    )
    if metadata is not None:
        tpl = tpl.replace("{{metadata}}", f" - {metadata}")

    if benchmark is not None:
        benchmark.name = None

    if isinstance(returns, pd.Series):
        returns.name = strategy_title
    elif isinstance(returns, pd.DataFrame):
        returns.columns = strategy_title

    if cutoff is not None:
        mtrx_benchmark_full_period = _calculate_metrics(
            returns=returns,
            benchmark=benchmark,
            rf=rf,
            display=False,
            mode="full",
            sep=True,
            internal="True",
            compounded=compounded,
            periods_per_year=periods_per_year,
            benchmark_title=benchmark_title,
            strategy_title=f"{strategy_title} IS",
            weights=weights,
        )
        mtrx_is = _calculate_metrics(
            returns=returns.loc[:cutoff],
            benchmark=benchmark,  # .loc[:cutoff],
            rf=rf,
            display=False,
            mode="full",
            sep=True,
            internal="True",
            compounded=compounded,
            periods_per_year=periods_per_year,
            benchmark_title=benchmark_title,
            strategy_title=f"{strategy_title} IS",
            weights=weights,
        )
        mtrx_oos = _calculate_metrics(
            returns=returns.loc[cutoff:],
            benchmark=benchmark.loc[cutoff:],
            rf=rf,
            display=False,
            mode="full",
            sep=True,
            internal="True",
            compounded=compounded,
            periods_per_year=periods_per_year,
            benchmark_title=benchmark_title,
            strategy_title=f"{strategy_title} OOS",
            weights=weights,
        )
        mtrx = pd.DataFrame(index=mtrx_is.index)
        mtrx["Benchmark"] = mtrx_benchmark_full_period.iloc[:, 0]
        mtrx[f"{strategy_title}_IS"] = mtrx_is.iloc[:, -1]
        mtrx[f"{strategy_title}_OOS"] = mtrx_oos.iloc[:, -1]

    else:
        mtrx = _calculate_metrics(
            returns=returns,
            benchmark=benchmark,
            rf=rf,
            display=False,
            mode="full",
            sep=True,
            internal="True",
            compounded=compounded,
            periods_per_year=periods_per_year,
            benchmark_title=benchmark_title,
            strategy_title=strategy_title,
            weights=weights,
        )

    mtrx.index.name = "Metric"

    tpl = tpl.replace("{{metrics}}", _html_table(mtrx)).replace(
        "{{benchmark_name}}", benchmark_title or ""
    )
    if isinstance(returns, pd.DataFrame):
        num_cols = len(returns.columns) if cutoff is None else len(returns.columns) * 2
        for i in reversed(range(num_cols + 1, num_cols + 3)):
            str_td = "<td></td>" * i
            tpl = tpl.replace(
                f"<tr>{str_td}</tr>", f'<tr><td colspan="{i}"><hr></td></tr>'
            )

    tpl = tpl.replace(
        "<tr><td></td><td></td><td></td></tr>", '<tr><td colspan="3"><hr></td></tr>'
    )
    tpl = tpl.replace(
        "<tr><td></td><td></td><td></td><td></td></tr>",
        '<tr><td colspan="4"><hr></td></tr>',
    )
    tpl = tpl.replace(
        "<tr><td></td><td></td></tr>", '<tr><td colspan="3"><hr></td></tr>'
    )

    if benchmark is not None:
        yoy = _stats.compare(returns, benchmark, "A", compounded=compounded)
        if isinstance(returns, pd.Series):
            yoy.columns = [benchmark_title, strategy_title, "Multiplier", "Won"]
        elif isinstance(returns, pd.DataFrame):
            yoy.columns = list(
                pd.core.common.flatten([benchmark_title, strategy_title])
            )
        yoy.index.name = "Year"
        tpl = tpl.replace("{{eoy_title}}", "<h3>EOY Returns vs Benchmark</h3>")
        tpl = tpl.replace("{{eoy_table}}", _html_table(yoy))
    else:
        # pct multiplier
        yoy = pd.DataFrame(_utils.group_returns(returns, returns.index.year) * 100)
        if isinstance(returns, pd.Series):
            yoy.columns = ["Return"]
            yoy["Cumulative"] = _utils.group_returns(returns, returns.index.year, True)
            yoy["Return"] = yoy["Return"].round(2).astype(str) + "%"
            yoy["Cumulative"] = (yoy["Cumulative"] * 100).round(2).astype(str) + "%"
        elif isinstance(returns, pd.DataFrame):
            # Don't show cumulative for multiple strategy portfolios
            # just show compounded like when we have a benchmark
            yoy.columns = list(pd.core.common.flatten(strategy_title))

        yoy.index.name = "Year"
        tpl = tpl.replace("{{eoy_title}}", "<h3>EOY Returns</h3>")
        tpl = tpl.replace("{{eoy_table}}", _html_table(yoy))

    dd = _stats.to_drawdown_series(returns)
    dd_info = _stats.drawdown_details(dd).sort_values(
        by="max drawdown", ascending=True
    )[:10]
    dd_info = dd_info[["start", "end", "max drawdown", "days"]]
    dd_info.columns = ["Started", "Recovered", "Drawdown", "Days"]
    tpl = tpl.replace("{{dd_info}}", _html_table(dd_info, False))

    active = kwargs.get("active_returns", "False")
    # plots
    figfile = _utils._file_stream()
    plot_returns(
        returns,
        benchmark,
        grayscale=grayscale,
        figsize=(8, 5),
        subtitle=False,
        savefig={"fname": figfile, "format": figfmt},
        # ylabel=None,
        cumulative=compounded,
        cutoff=cutoff,
    )
    tpl = tpl.replace("{{returns_long_short}}", _embed_figure(figfile, figfmt))

    if delayed_sharpes is not None:
        figfile = _utils._file_stream()
        plot_series(
            delayed_sharpes,
            title="Delayed Execution - Portfolio Sharpes",
            grayscale=grayscale,
            figsize=(8, 5),
            subtitle=False,
            savefig={"fname": figfile, "format": figfmt},
            ylabel="Portfolio Sharpe",
            xlabel="Days of execution delay",
            cutoff=cutoff,
        )
        tpl = tpl.replace("{{returns_delayed}}", _embed_figure(figfile, figfmt))
    else:
        tpl = tpl.replace("{{returns_delayed}}", "")

    if comparison_metrics is not None and len(comparison_metrics) > 0:
        figfile = _utils._file_stream()
        plot_horizontal_bar(
            mtrx.loc[comparison_metrics, :],
            mtrx.columns[1],
            mtrx.columns[0],
            title="Portfolio Metrics",
            savefig={"fname": figfile, "format": figfmt},
        )
        tpl = tpl.replace("{{comparison_chart}}", _embed_figure(figfile, figfmt))
    else:
        tpl = tpl.replace("{{comparison_chart}}", "")

    figfile = _utils._file_stream()
    plot_log_returns(
        returns,
        benchmark,
        grayscale=grayscale,
        figsize=(8, 4),
        subtitle=False,
        savefig={"fname": figfile, "format": figfmt},
        ylabel=False,
        cumulative=compounded,
        cutoff=cutoff,
    )
    tpl = tpl.replace("{{log_returns}}", _embed_figure(figfile, figfmt))

    if benchmark is not None:
        figfile = _utils._file_stream()
        plot_returns(
            returns,
            benchmark,
            match_volatility=True,
            grayscale=grayscale,
            figsize=(8, 4),
            subtitle=False,
            savefig={"fname": figfile, "format": figfmt},
            ylabel=False,
            cumulative=compounded,
            cutoff=cutoff,
        )
        tpl = tpl.replace("{{vol_returns}}", _embed_figure(figfile, figfmt))

    if weights is not None:
        figfile = _utils._file_stream()
        plot_rolling_net_exposure(
            weights=weights,
            grayscale=grayscale,
            figsize=(8, 4),
            subtitle=False,
            savefig={"fname": figfile, "format": figfmt},
            ylabel=False,
            cutoff=cutoff,
        )
        tpl = tpl.replace("{{rolling_net_exposure}}", _embed_figure(figfile, figfmt))

    figfile = _utils._file_stream()
    plot_yearly_returns(
        returns,
        benchmark,
        grayscale=grayscale,
        figsize=(8, 4),
        subtitle=False,
        savefig={"fname": figfile, "format": figfmt},
        ylabel=False,
        compounded=compounded,
    )
    tpl = tpl.replace("{{eoy_returns}}", _embed_figure(figfile, figfmt))

    if cutoff is not None:
        figfile = _utils._file_stream()
        plot_histogram(
            returns.loc[:cutoff].rename(f"{strategy_title}-IS"),
            benchmark.loc[:cutoff],
            grayscale=grayscale,
            figsize=(7, 4),
            subtitle=True,
            savefig={"fname": figfile, "format": figfmt},
            ylabel=False,
            compounded=compounded,
        )
        tpl = tpl.replace("{{monthly_dist}}", _embed_figure(figfile, figfmt))
        figfile = _utils._file_stream()
        plot_histogram(
            returns.loc[cutoff:].rename(f"{strategy_title}-OOS"),
            benchmark.loc[cutoff:],
            grayscale=grayscale,
            figsize=(7, 4),
            subtitle=True,
            savefig={"fname": figfile, "format": figfmt},
            ylabel=False,
            compounded=compounded,
        )
        tpl = tpl.replace("{{monthly_dist_oos}}", _embed_figure(figfile, figfmt))
    else:
        figfile = _utils._file_stream()
        plot_histogram(
            returns,
            benchmark,
            grayscale=grayscale,
            figsize=(7, 4),
            subtitle=False,
            savefig={"fname": figfile, "format": figfmt},
            ylabel=False,
            compounded=compounded,
        )
        tpl = tpl.replace("{{monthly_dist}}", _embed_figure(figfile, figfmt))
        tpl = tpl.replace("{{monthly_dist_oos}}", "")

    figfile = _utils._file_stream()
    plot_daily_returns(
        returns,
        benchmark,
        grayscale=grayscale,
        figsize=(8, 3),
        subtitle=False,
        savefig={"fname": figfile, "format": figfmt},
        ylabel=False,
        active=active,
        cutoff=cutoff,
    )
    tpl = tpl.replace("{{daily_returns}}", _embed_figure(figfile, figfmt))

    if benchmark is not None:
        figfile = _utils._file_stream()
        plot_rolling_beta(
            returns,
            benchmark,
            grayscale=grayscale,
            figsize=(8, 3),
            subtitle=False,
            window1=win_half_year,
            window2=win_year,
            savefig={"fname": figfile, "format": figfmt},
            ylabel=False,
            cutoff=cutoff,
        )
        tpl = tpl.replace("{{rolling_beta}}", _embed_figure(figfile, figfmt))

    figfile = _utils._file_stream()
    plot_rolling_volatility(
        returns,
        benchmark,
        grayscale=grayscale,
        figsize=(8, 3),
        subtitle=False,
        savefig={"fname": figfile, "format": figfmt},
        ylabel=False,
        period=win_half_year,
        periods_per_year=win_year,
        cutoff=cutoff,
    )
    tpl = tpl.replace("{{rolling_vol}}", _embed_figure(figfile, figfmt))

    figfile = _utils._file_stream()
    plot_rolling_sharpe(
        returns,
        benchmark=benchmark,
        grayscale=grayscale,
        figsize=(8, 3),
        subtitle=False,
        savefig={"fname": figfile, "format": figfmt},
        ylabel=False,
        period=win_half_year,
        periods_per_year=win_year,
        cutoff=cutoff,
    )
    tpl = tpl.replace("{{rolling_sharpe}}", _embed_figure(figfile, figfmt))

    figfile = _utils._file_stream()
    plot_drawdowns_periods(
        returns,
        grayscale=grayscale,
        figsize=(8, 4),
        subtitle=False,
        title=returns.name,
        savefig={"fname": figfile, "format": figfmt},
        ylabel=False,
        compounded=compounded,
        cutoff=cutoff,
    )
    tpl = tpl.replace("{{dd_periods}}", _embed_figure(figfile, figfmt))
    figfile = _utils._file_stream()
    drawdown(
        returns,
        grayscale=grayscale,
        figsize=(8, 3),
        subtitle=False,
        savefig={"fname": figfile, "format": figfmt},
        ylabel=False,
        cutoff=cutoff,
    )
    tpl = tpl.replace("{{dd_plot}}", _embed_figure(figfile, figfmt))

    figfile = _utils._file_stream()
    plot_monthly_heatmap(
        returns,
        benchmark,
        grayscale=grayscale,
        figsize=(8, 4),
        cbar=False,
        returns_label=returns.name,
        savefig={"fname": figfile, "format": figfmt},
        ylabel=False,
        compounded=compounded,
        active=active,
    )
    tpl = tpl.replace("{{monthly_heatmap}}", _embed_figure(figfile, figfmt))

    if cutoff is not None:
        figfile = _utils._file_stream()

        plot_distribution(
            returns.loc[:cutoff],
            grayscale=grayscale,
            figsize=(8, 4),
            subtitle=False,
            title=f"{returns.name}-IS",
            savefig={"fname": figfile, "format": figfmt},
            ylabel=False,
            compounded=compounded,
        )
        tpl = tpl.replace("{{returns_dist}}", _embed_figure(figfile, figfmt))
        figfile = _utils._file_stream()

        plot_distribution(
            returns.loc[cutoff:],
            grayscale=grayscale,
            figsize=(8, 4),
            subtitle=False,
            title=f"{returns.name}-OOS",
            savefig={"fname": figfile, "format": figfmt},
            ylabel=False,
            compounded=compounded,
        )
        tpl = tpl.replace("{{returns_dist_oos}}", _embed_figure(figfile, figfmt))
    else:
        figfile = _utils._file_stream()

        plot_distribution(
            returns,
            grayscale=grayscale,
            figsize=(8, 4),
            subtitle=False,
            title=returns.name,
            savefig={"fname": figfile, "format": figfmt},
            ylabel=False,
            compounded=compounded,
        )
        tpl = tpl.replace("{{returns_dist}}", _embed_figure(figfile, figfmt))
        tpl = tpl.replace("{{returns_dist_oos}}", "")

    if component_returns_df is not None:
        figfile = _utils._file_stream()
        corr_matrix = component_returns_df.corr()
        plt.figure(figsize=(10, 8))

        def replace_repetitive_transformations(label: str) -> str:
            if "~ensemble" not in label:
                return label
            transformation = label.split("~ensemble(")[1].split("_")[0]
            return (
                label.replace(transformation, "")
                .replace("~ensemble(", f"~ensemble({transformation}")
                .replace("~", "~\n")
                .replace("ensemble(", "ensemble(\n")
            )

        wrapped_labels = [
            replace_repetitive_transformations(label) for label in corr_matrix.columns
        ]
        sns.heatmap(
            corr_matrix,
            annot=True,
            center=0,
            cmap="gray" if grayscale else "RdYlGn",
            xticklabels=wrapped_labels,
            yticklabels=wrapped_labels,
        )
        plt.title("Correlation Matrix")
        savefig = {"fname": figfile, "format": figfmt}
        if savefig:
            if isinstance(savefig, dict):
                plt.savefig(**savefig)
            else:
                plt.savefig(savefig)
        plt.close()
        tpl = tpl.replace("{{component_correlation}}", _embed_figure(figfile, figfmt))

    if component_level_stats is not None:
        figfile = _utils._file_stream()
        plot_component_heatmap(
            component_level_stats,
            grayscale=grayscale,
            figsize=(8, 4),
            cbar=False,
            savefig={"fname": figfile, "format": figfmt},
            ylabel=False,
        )
        tpl = tpl.replace("{{component_level_heatmap}}", _embed_figure(figfile, figfmt))
    else:
        tpl = tpl.replace("{{component_level_heatmap}}", "")

    tpl = _regex.sub(r"\{\{(.*?)\}\}", "", tpl)
    tpl = tpl.replace("white-space:pre;", "")
    pd.options.mode.copy_on_write = True
    return HTMLReport(tpl)


def _calculate_metrics(  # noqa
    returns: pd.Series,
    benchmark: pd.Series,
    rf: float = 0.0,
    display: bool = True,
    mode: Literal["basic", "full"] = "basic",
    sep: bool = False,
    compounded: bool = True,
    periods_per_year: int = 252,
    match_dates: bool = True,
    weights: pd.DataFrame | None = None,
    **kwargs,
) -> pd.DataFrame:
    if match_dates:
        returns = returns.dropna()
    returns.index = returns.index.tz_localize(None)
    win_year, _ = _get_trading_periods(periods_per_year)

    benchmark_colname = kwargs.get("benchmark_title", "Benchmark")
    strategy_colname = kwargs.get("strategy_title", "Strategy")

    benchmark_colname = (
        f"Benchmark {f"({benchmark.name.upper()})" if benchmark.name else ""}"
    )

    blank = [""]

    df = pd.DataFrame({"returns": returns})

    if match_dates is True:
        returns, benchmark = _match_dates(returns, benchmark)
    df["benchmark"] = benchmark
    if isinstance(returns, pd.Series):
        blank = ["", ""]
        df["returns"] = returns
    elif isinstance(returns, pd.DataFrame):
        blank = [""] * len(returns.columns) + [""]
        for i, strategy_col in enumerate(returns.columns):
            df["returns_" + str(i + 1)] = returns[strategy_col]

    s_start = {"returns": df["returns"].index.strftime("%Y-%m-%d")[0]}
    s_end = {"returns": df["returns"].index.strftime("%Y-%m-%d")[-1]}
    s_rf = {"returns": rf}

    if "benchmark" in df:
        s_start["benchmark"] = df["benchmark"].index.strftime("%Y-%m-%d")[0]
        s_end["benchmark"] = df["benchmark"].index.strftime("%Y-%m-%d")[-1]
        s_rf["benchmark"] = rf

    df = df.fillna(0)

    # pct multiplier
    pct = 100 if display or "internal" in kwargs else 1
    if kwargs.get("as_pct", False):
        pct = 100

    # return df
    dd = _calc_dd(
        df,
        display=(display or "internal" in kwargs),
        as_pct=kwargs.get("as_pct", False),
    )

    metrics = pd.DataFrame()
    metrics["Start Period"] = pd.Series(s_start)
    metrics["End Period"] = pd.Series(s_end)

    if weights is not None:
        metrics["Average Net Exposure %"] = [
            round(weights.sum(axis="columns").mean() * 100, 2),
            100,
        ]
        metrics["Average Gross Exposure %"] = [
            round(weights.abs().sum(axis="columns").mean() * 100, 2),
            100,
        ]
        metrics["Daily Turnover %"] = [
            round(weights.diff(1).abs().sum(axis=1).mean() * 100, 2),
            0.0,
        ]

    metrics["~"] = blank

    if compounded:
        metrics["Cumulative Return %"] = (_stats.comp(df) * pct).map("{:,.2f}".format)
    else:
        metrics["Total Return %"] = (df.sum() * pct).map("{:,.2f}".format)

    metrics["CAGR﹪%"] = round(_stats.cagr(df, rf, compounded, win_year) * pct, 2)

    metrics["~~~~~~~~~~~~~~"] = blank

    metrics["Sharpe"] = round(_stats.sharpe(df, rf, win_year, True), 2)

    metrics["Sortino"] = round(_stats.sortino(df, rf, win_year, True), 2)

    ret_vol = _stats.volatility(df["returns"], win_year, True) * pct

    if "benchmark" in df:
        bench_vol = round(
            (_stats.volatility(df["benchmark"], win_year, True) * pct),
            2,
        )

        vol_ = [ret_vol, bench_vol]
        metrics["Volatility (ann.) %"] = [round(v, 2) for v in vol_]

        # metrics["R^2"] = [
        #     round(
        #         _stats.r_squared(
        #             df["returns"], df["benchmark"]
        #         ),
        #         2,
        #     ),
        #     "-",
        # ]
        # metrics["Information Ratio"] = [
        #     round(
        #         _stats.information_ratio(
        #             df["returns"], df["benchmark"]
        #         ),
        #         2,
        #     ),
        #     "-",
        # ]
    else:
        metrics["Volatility (ann.) %"] = [ret_vol]

    if "benchmark" in df:
        metrics["~~~~~~~~~~~~"] = blank
        greeks = _stats.greeks(df["returns"], df["benchmark"], win_year)
        metrics["Beta"] = [str(round(greeks["beta"], 2)), "-"]
        metrics["Alpha"] = [str(round(greeks["alpha"], 2)), "-"]
        metrics["Correlation"] = [
            str(round(df["benchmark"].corr(df["returns"]) * pct, 2)) + "%",
            "-",
        ]
        metrics["Downside Corr."] = [
            str(
                round(
                    stats.downside_correlation(df["returns"], df["benchmark"]) * pct, 2
                )
            )
            + "%",
            "-",
        ]
        metrics["Upside Corr."] = [
            str(
                round(stats.upside_correlation(df["returns"], df["benchmark"]) * pct, 2)
            )
            + "%",
            "-",
        ]
        metrics["Downside Beta"] = [
            str(round(stats.downside_beta(df["returns"], df["benchmark"]), 2)),
            "-",
        ]
        metrics["Upside Beta"] = [
            str(round(stats.upside_beta(df["returns"], df["benchmark"]), 2)),
            "-",
        ]
        metrics["Weighted Downside Beta"] = [
            str(round(stats.weighted_downside_beta(df["returns"], df["benchmark"]), 2)),
            "-",
        ]

    metrics["~~~~~~~~"] = blank
    metrics["Max Drawdown %"] = blank
    metrics["Longest DD Days"] = blank

    if mode.lower() == "full":
        metrics["Calmar"] = round(_stats.calmar(df), 2)
        metrics["Skew"] = round(_stats.skew(df), 2)
        metrics["Kurtosis"] = round(_stats.kurtosis(df), 2)

        metrics["~~~~~~~~~~"] = blank

        metrics["Expected Daily %%"] = [
            round(s, 2)
            for s in (_stats.expected_return(df, compounded=compounded) * pct)
        ]
        metrics["Expected Monthly %%"] = [
            round(s, 2)
            for s in (
                _stats.expected_return(df, compounded=compounded, aggregate="M") * pct
            )
        ]
        metrics["Expected Yearly %%"] = round(
            (_stats.expected_return(df, compounded=compounded, aggregate="A") * pct),
            2,
        )
        metrics["Risk of Ruin %"] = round(_stats.risk_of_ruin(df), 2)

        metrics["Daily Value-at-Risk %"] = [
            round(s, 2) for s in -abs(_stats.var(df) * pct)
        ]
        metrics["Expected Shortfall (cVaR) %"] = [
            round(s, 2) for s in -abs(_stats.cvar(df) * pct)
        ]

    # returns
    metrics["~~"] = blank
    comp_func = _stats.comp if compounded else np.sum

    today = df.index[-1]  # _dt.today()
    metrics["MTD %"] = round(
        comp_func(df[df.index >= _dt(today.year, today.month, 1)]) * pct, 2
    )

    d = today - pd.DateOffset(months=3)
    metrics["3M %"] = round(comp_func(df[df.index >= d]) * pct, 2)

    d = today - pd.DateOffset(months=6)
    metrics["6M %"] = round(comp_func(df[df.index >= d]) * pct, 2)

    metrics["YTD %"] = round(comp_func(df[df.index >= _dt(today.year, 1, 1)]) * pct, 2)

    d = today - pd.DateOffset(years=1)
    metrics["1Y %"] = round(comp_func(df[df.index >= d]) * pct, 2)

    d = today - pd.DateOffset(months=35)
    metrics["3Y (ann.) %"] = round(
        _stats.cagr(df[df.index >= d], 0.0, compounded) * pct, 2
    )

    d = today - pd.DateOffset(months=59)
    metrics["5Y (ann.) %"] = round(
        _stats.cagr(df[df.index >= d], 0.0, compounded) * pct, 2
    )

    d = today - pd.DateOffset(years=10)
    metrics["10Y (ann.) %"] = round(
        _stats.cagr(df[df.index >= d], 0.0, compounded) * pct, 2
    )

    metrics["All-time (ann.) %"] = round(_stats.cagr(df, 0.0, compounded) * pct, 2)

    # best/worst
    if mode.lower() == "full":
        metrics["~~~"] = blank
        metrics["Best Day %"] = [
            round(s, 2) for s in _stats.best(df, compounded=compounded) * pct
        ]
        metrics["Worst Day %"] = [round(s, 2) for s in _stats.worst(df) * pct]
        metrics["Best Month %"] = [
            round(s, 2)
            for s in _stats.best(df, compounded=compounded, aggregate="M") * pct
        ]
        metrics["Worst Month %"] = [
            round(s, 2) for s in _stats.worst(df, aggregate="M") * pct
        ]
        metrics["Best Year %"] = [
            round(s, 2)
            for s in _stats.best(df, compounded=compounded, aggregate="A") * pct
        ]
        metrics["Worst Year %"] = [
            round(s, 2)
            for s in _stats.worst(df, compounded=compounded, aggregate="A") * pct
        ]

    # dd
    metrics["~~~~"] = blank
    for ix, row in dd.iterrows():
        metrics[ix] = row
    metrics["Recovery Factor"] = round(_stats.recovery_factor(df), 2)
    metrics["Ulcer Index"] = round(_stats.ulcer_index(df), 2)
    metrics["Serenity Index"] = round(_stats.serenity_index(df, rf), 2)

    # win rate
    if mode.lower() == "full":
        metrics["~~~~~"] = blank
        metrics["Positive Days %%"] = round(_stats.win_rate(df) * pct, 2)
        metrics["Positive Month %%"] = round(
            (_stats.win_rate(df, compounded=compounded, aggregate="M") * pct),
            2,
        )
        metrics["Positive Quarter %%"] = round(
            (_stats.win_rate(df, compounded=compounded, aggregate="Q") * pct),
            2,
        )
        metrics["Positive Year %%"] = round(
            (_stats.win_rate(df, compounded=compounded, aggregate="A") * pct),
            2,
        )

    # prepare for display
    for col in metrics.columns:
        if display or "internal" in kwargs:
            metrics[col] = metrics[col].astype(str)

        if (display or "internal" in kwargs) and "*int" in col:
            metrics[col] = metrics[col].str.replace(".0", "", regex=False)
            metrics = metrics.rename({col: col.replace("*int", "")}, axis=1)
        if (display or "internal" in kwargs) and "%" in col:
            metrics[col] = metrics[col] + "%"

    try:
        metrics["Longest DD Days"] = pd.to_numeric(metrics["Longest DD Days"]).astype(
            "int"
        )
        metrics["Avg. Drawdown Days"] = pd.to_numeric(
            metrics["Avg. Drawdown Days"]
        ).astype("int")

        if display or "internal" in kwargs:
            metrics["Longest DD Days"] = metrics["Longest DD Days"].astype(str)
            metrics["Avg. Drawdown Days"] = metrics["Avg. Drawdown Days"].astype(str)
    except Exception:  # noqa
        metrics["Longest DD Days"] = "-"
        metrics["Avg. Drawdown Days"] = "-"
        if display or "internal" in kwargs:
            metrics["Longest DD Days"] = "-"
            metrics["Avg. Drawdown Days"] = "-"

    metrics.columns = [col if "~" not in col else "" for col in metrics.columns]
    metrics.columns = [col[:-1] if "%" in col else col for col in metrics.columns]
    metrics = metrics.T

    if "benchmark" in df:
        column_names = [strategy_colname, benchmark_colname]
        if isinstance(strategy_colname, list):
            metrics.columns = list(pd.core.common.flatten(column_names))
        else:
            metrics.columns = column_names
    elif isinstance(strategy_colname, list):
        metrics.columns = strategy_colname
    else:
        metrics.columns = [strategy_colname]

    # cleanups
    metrics = metrics.replace([-0, "-0"], 0)
    metrics = metrics.replace(
        [
            np.nan,
            -np.nan,
            np.inf,
            -np.inf,
            "-nan%",
            "nan%",
            "-nan",
            "nan",
            "-inf%",
            "inf%",
            "-inf",
            "inf",
        ],
        "-",
    )

    # move benchmark to be the first column always if present
    if "benchmark" in df:
        metrics = metrics[
            [benchmark_colname]
            + [col for col in metrics.columns if col != benchmark_colname]
        ]

    if display:
        print(_tabulate(metrics, headers="keys", tablefmt="simple"))
        return None

    if not sep:
        metrics = metrics[metrics.index != ""]

    # remove spaces from column names
    metrics = metrics.T
    metrics.columns = [
        c.replace(" %", "").replace(" *int", "").strip() for c in metrics.columns
    ]
    return metrics.T


def _calc_dd(
    df: pd.DataFrame, display: bool = True, as_pct: bool = False
) -> pd.DataFrame:
    dd = _stats.to_drawdown_series(df)
    dd_info = _stats.drawdown_details(dd)

    if dd_info.empty:
        return pd.DataFrame()

    if "returns" in dd_info:
        ret_dd = dd_info["returns"]
    # to match multiple columns like returns_1, returns_2, ...
    elif (
        any(dd_info.columns.get_level_values(0).str.contains("returns"))
        and dd_info.columns.get_level_values(0).nunique() > 1
    ):
        ret_dd = dd_info.loc[
            :, dd_info.columns.get_level_values(0).str.contains("returns")
        ]
    else:
        ret_dd = dd_info

    dd_stats = {
        "returns": {
            "Max Drawdown %": round(
                ret_dd.sort_values(by="max drawdown", ascending=True)[
                    "max drawdown"
                ].values[0]
                / 100,
                4,
            ),
            "Longest DD Days": str(
                np.round(
                    ret_dd.sort_values(by="days", ascending=False)["days"].values[0]
                )
            ),
            "Avg. Drawdown %": round(ret_dd["max drawdown"].mean() / 100, 4),
            "Avg. Drawdown Days": str(np.round(ret_dd["days"].mean())),
        }
    }
    if "benchmark" in df and (dd_info.columns, pd.MultiIndex):
        bench_dd = dd_info["benchmark"].sort_values(by="max drawdown")
        dd_stats["benchmark"] = {
            "Max Drawdown %": round(
                bench_dd.sort_values(by="max drawdown", ascending=True)[
                    "max drawdown"
                ].values[0]
                / 100,
                4,
            ),
            "Longest DD Days": str(
                np.round(
                    bench_dd.sort_values(by="days", ascending=False)["days"].values[0]
                )
            ),
            "Avg. Drawdown %": round(bench_dd["max drawdown"].mean() / 100, 4),
            "Avg. Drawdown Days": str(np.round(bench_dd["days"].mean())),
        }

    # pct multiplier
    pct = 100 if display or as_pct else 1

    dd_stats = pd.DataFrame(dd_stats).T
    dd_stats["Max Drawdown %"] = (
        dd_stats["Max Drawdown %"].astype(float).mul(pct).round(2)
    )
    dd_stats["Avg. Drawdown %"] = (
        dd_stats["Avg. Drawdown %"].astype(float).mul(pct).round(2)
    )

    return dd_stats.T


def _html_table(obj, showindex="default"):
    obj = _tabulate(
        obj, headers="keys", tablefmt="html", floatfmt=".2f", showindex=showindex
    )
    obj = obj.replace(' style="text-align: right;"', "")
    obj = obj.replace(' style="text-align: left;"', "")
    obj = obj.replace(' style="text-align: center;"', "")
    obj = _regex.sub("<td> +", "<td>", obj)
    obj = _regex.sub(" +</td>", "</td>", obj)
    obj = _regex.sub("<th> +", "<th>", obj)
    return _regex.sub(" +</th>", "</th>", obj)


def _download_html(html, filename: str = "quantstats-tearsheet.html"):
    jscode = _regex.sub(
        " +",
        " ",
        """<script>
    var bl=new Blob(['{{html}}'],{type:"text/html"});
    var a=document.createElement("a");
    a.href=URL.createObjectURL(bl);
    a.download="{{filename}}";
    a.hidden=true;document.body.appendChild(a);
    a.innerHTML="download report";
    a.click();</script>""".replace("\n", ""),
    )
    jscode = jscode.replace("{{html}}", _regex.sub(" +", " ", html.replace("\n", "")))


def _embed_figure(figfiles, figfmt):
    if isinstance(figfiles, list):
        embed_string = "\n"
        for figfile in figfiles:
            figbytes = figfile.getvalue()
            if figfmt == "svg":
                return figbytes.decode()
            data_uri = _b64encode(figbytes).decode()
            embed_string.join(f'<img src="data:image/{figfmt};base64,{data_uri}" />')
    else:
        figbytes = figfiles.getvalue()
        if figfmt == "svg":
            return figbytes.decode()
        data_uri = _b64encode(figbytes).decode()
        embed_string = f'<img src="data:image/{figfmt};base64,{data_uri}" />'
    return embed_string
