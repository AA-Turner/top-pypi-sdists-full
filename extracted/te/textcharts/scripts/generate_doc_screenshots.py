#!/usr/bin/env python3
"""Generate terminal screenshot assets for the Sphinx chart gallery."""

from __future__ import annotations

import html
import os
import subprocess
import tempfile
import time
from pathlib import Path

from ansi2html import Ansi2HTMLConverter
from PIL import Image

from textcharts import (
    BarChart,
    BoxPlot,
    CDFChart,
    ChartOptions,
    ComparisonBar,
    DivergingBar,
    Heatmap,
    Histogram,
    LineChart,
    NormalizedSpeedup,
    PercentileLadder,
    RankTable,
    ScatterPlot,
    SparklineTable,
    StackedBar,
    SummaryBox,
    BarData,
    BoxPlotSeries,
    CDFSeriesData,
    ColorMode,
    ComparisonBarData,
    DivergingBarData,
    HistogramBar,
    LinePoint,
    PercentileData,
    RankTableData,
    ScatterPoint,
    SparklineColumn,
    SparklineTableData,
    SpeedupData,
    StackedBarData,
    StackedBarSegment,
    SummaryStats,
    TerminalCapabilities,
)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "_static" / "screenshots"
CHROME_CANDIDATES = (
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
)

HTML_TEMPLATE = """\
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  * {{ box-sizing: border-box; }}
  html {{ background: #15181c; }}
  body {{
    margin: 0;
    background: #15181c;
    padding: 28px 30px;
    display: inline-block;
  }}
  pre {{
    margin: 0;
    font-family: "Fira Code", "JetBrains Mono", "SF Mono", "Menlo", "Consolas", monospace;
    font-size: 13.5px;
    line-height: 1.08;
    color: #d8dee9;
    white-space: pre;
  }}
  .ansi1 {{ font-weight: bold; }}
  .ansi32 {{ color: #4ec9b0; }}
  .ansi33 {{ color: #e6ab02; }}
  .ansi34 {{ color: #569cd6; }}
  .ansi35 {{ color: #c586c0; }}
  .ansi36 {{ color: #4ec9b0; }}
  .ansi37 {{ color: #d8dee9; }}
  .ansi38-5-36 {{ color: #4ec9b0; }}
  .ansi38-5-60 {{ color: #5a6478; }}
  .ansi38-5-70 {{ color: #6aaf6a; }}
  .ansi38-5-97 {{ color: #8b7fd6; }}
  .ansi38-5-130 {{ color: #b88746; }}
  .ansi38-5-162 {{ color: #d16ba5; }}
  .ansi38-5-166 {{ color: #d7875f; }}
  .ansi38-5-178 {{ color: #d6b34e; }}
  .ansi38-5-242 {{ color: #6b7075; }}
</style>
</head>
<body>
<pre>{content}</pre>
</body>
</html>
"""

GREYSCALE_COLOR_MAP = {
    "#1B9E77": "#F0F0F0",
    "#66A61E": "#D9D9D9",
    "#E6AB02": "#BFBFBF",
    "#D95F02": "#8F8F8F",
    "#E7298A": "#696969",
    "#7570B3": "#A6A6A6",
    "#666666": "#7A7A7A",
    "#2166AC": "#E6E6E6",
    "#67A9CF": "#CBCBCB",
    "#F7F7F7": "#B3B3B3",
    "#EF8A62": "#8C8C8C",
    "#B2182B": "#5E5E5E",
    "#4393C3": "#E8E8E8",
    "#92C5DE": "#CECECE",
    "#D1E5F0": "#B7B7B7",
    "#FDB863": "#909090",
    "#D6604D": "#626262",
    "#4EC9B0": "#E3E3E3",
    "#E6AB02": "#BFBFBF",
    "#569CD6": "#C9C9C9",
    "#C586C0": "#A1A1A1",
    "#D8DEE9": "#D8D8D8",
    "#5A6478": "#7E7E7E",
    "#6AAF6A": "#B5B5B5",
    "#8B7FD6": "#999999",
    "#B88746": "#A8A8A8",
    "#D16BA5": "#8A8A8A",
    "#D7875F": "#9B9B9B",
    "#D6B34E": "#AEAEAE",
    "#6B7075": "#787878",
}


def _chrome_binary() -> str:
    for candidate in CHROME_CANDIDATES:
        if Path(candidate).exists():
            return candidate
    raise SystemExit("Chrome or Chromium not found in expected macOS application paths")


def _caps(color_mode: ColorMode, *, unicode_support: bool, interactive: bool) -> TerminalCapabilities:
    return TerminalCapabilities(
        width=96,
        height=40,
        color_mode=color_mode,
        unicode_support=unicode_support,
        interactive=interactive,
    )


def _options(mode: str) -> ChartOptions:
    if mode in {"color", "greyscale"}:
        opts = ChartOptions(width=96, use_color=True, use_unicode=True)
        opts._capabilities = _caps(ColorMode.TRUECOLOR, unicode_support=True, interactive=True)
        return opts
    if mode == "monochrome":
        opts = ChartOptions(width=96, use_color=False, use_unicode=False)
        opts._capabilities = _caps(ColorMode.NONE, unicode_support=False, interactive=False)
        return opts
    raise ValueError(f"unsupported mode: {mode}")


def _render_chart(chart, mode: str) -> str:
    """Force deterministic terminal capabilities for screenshot generation."""
    chart._capabilities = _caps(
        ColorMode.TRUECOLOR if mode in {"color", "greyscale"} else ColorMode.NONE,
        unicode_support=(mode in {"color", "greyscale"}),
        interactive=(mode in {"color", "greyscale"}),
    )
    chart.options._capabilities = chart._capabilities
    return chart.render()


def _bar_chart(mode: str) -> str:
    data = [
        BarData(label="Fiction", value=18400.0, is_best=True),
        BarData(label="Children", value=12650.0),
        BarData(label="Comics", value=9300.0, is_worst=True),
    ]
    chart = BarChart(
        data=data, title="April Bookstore Revenue", metric_label="USD",
        subtitle="Top three categories by total sales", options=_options(mode),
    )
    return _render_chart(chart, mode)


def _histogram(mode: str) -> str:
    bars = [
        HistogramBar(label="Route 1", value=12.0, is_best=True),
        HistogramBar(label="Route 2", value=28.0),
        HistogramBar(label="Route 3", value=9.0),
        HistogramBar(label="Route 4", value=45.0, is_worst=True),
        HistogramBar(label="Route 5", value=19.0),
        HistogramBar(label="Route 6", value=14.0),
    ]
    chart = Histogram(
        data=bars, title="Delivery Delays", y_label="Delay (min)",
        subtitle="Six routes measured over the past week", options=_options(mode),
    )
    return _render_chart(chart, mode)


def _heatmap(mode: str) -> str:
    matrix = [
        [88.0, 91.0, 84.0],
        [74.0, 79.0, 82.0],
        [93.0, 89.0, 95.0],
        [81.0, 86.0, 78.0],
    ]
    chart = Heatmap(
        matrix=matrix,
        row_labels=["Class A", "Class B", "Class C", "Class D"],
        col_labels=["Math", "Science", "History"],
        title="Classroom Scores",
        value_label="points",
        x_label="Subjects",
        subtitle="End-of-term averages across four classes",
        options=_options(mode),
    )
    return _render_chart(chart, mode)


def _box_plot(mode: str) -> str:
    series = [
        BoxPlotSeries(name="Downtown", values=[1825, 1900, 1980, 2100, 2250, 2400, 2550, 2710, 2980]),
        BoxPlotSeries(name="Riverside", values=[1450, 1525, 1600, 1680, 1750, 1820, 1950, 2080, 2220]),
        BoxPlotSeries(name="Midtown", values=[1650, 1710, 1780, 1840, 1920, 2010, 2140, 2280, 2450]),
    ]
    chart = BoxPlot(
        series=series, title="Apartment Rents",
        subtitle="Monthly rent distribution by neighborhood", options=_options(mode),
    )
    return _render_chart(chart, mode)


def _line_chart(mode: str) -> str:
    points = [
        LinePoint(series="Organic", x=1, y=320.0, label="Week 1"),
        LinePoint(series="Organic", x=2, y=355.0, label="Week 2"),
        LinePoint(series="Organic", x=3, y=410.0, label="Week 3"),
        LinePoint(series="Referral", x=1, y=180.0, label="Week 1"),
        LinePoint(series="Referral", x=2, y=205.0, label="Week 2"),
        LinePoint(series="Referral", x=3, y=260.0, label="Week 3"),
    ]
    chart = LineChart(
        points=points,
        title="Weekly Signups",
        x_label="Week",
        y_label="Signups",
        subtitle="Organic vs referral channels over three weeks",
        options=_options(mode),
    )
    return _render_chart(chart, mode)


def _scatter_plot(mode: str) -> str:
    points = [
        ScatterPoint(name="Spring Launch", x=8.0, y=410.0),
        ScatterPoint(name="Retargeting", x=5.5, y=180.0),
        ScatterPoint(name="Video Ads", x=11.0, y=470.0),
        ScatterPoint(name="Newsletter", x=2.0, y=220.0),
    ]
    chart = ScatterPlot(
        points=points,
        title="Ad Spend vs Conversions",
        x_label="Cost (USD)",
        y_label="Conversions",
        subtitle="Four campaigns compared by cost efficiency",
        options=_options(mode),
    )
    return _render_chart(chart, mode)


def _comparison_bar(mode: str) -> str:
    data = [
        ComparisonBarData(
            label="Marketing", baseline_value=140.0, comparison_value=152.0, baseline_name="Planned", comparison_name="Actual"
        ),
        ComparisonBarData(
            label="Operations", baseline_value=110.0, comparison_value=101.0, baseline_name="Planned", comparison_name="Actual"
        ),
        ComparisonBarData(
            label="Support", baseline_value=75.0, comparison_value=81.0, baseline_name="Planned", comparison_name="Actual"
        ),
        ComparisonBarData(
            label="Research", baseline_value=95.0, comparison_value=88.0, baseline_name="Planned", comparison_name="Actual"
        ),
    ]
    chart = ComparisonBar(
        data=data,
        title="Budget vs Actual",
        metric_label="Budget (k USD)",
        subtitle="Q1 departmental spending review",
        options=_options(mode),
    )
    return _render_chart(chart, mode)


def _diverging_bar(mode: str) -> str:
    data = [
        DivergingBarData(label="Design", pct_change=12.0),
        DivergingBarData(label="Sales", pct_change=-8.0),
        DivergingBarData(label="Support", pct_change=18.0),
        DivergingBarData(label="Product", pct_change=4.0),
        DivergingBarData(label="Finance", pct_change=-5.0),
    ]
    chart = DivergingBar(
        data=data, title="Sentiment Change by Team",
        subtitle="Year-over-year employee survey results", options=_options(mode),
    )
    return _render_chart(chart, mode)


def _summary_box(mode: str) -> str:
    stats = SummaryStats(
        title="Riverfront Festival Attendance",
        primary_value=420.0,
        secondary_value=390.0,
        total_value=18600.0,
        num_items=18,
        best_items=[("Gate A", 180.0), ("Gate C", 240.0), ("Gate D", 275.0)],
        worst_items=[("Gate F", 860.0), ("Gate B", 710.0), ("Gate E", 650.0)],
        environment={"Venue": "Riverfront Park", "Days": "3", "Volunteers": "48"},
        platform_config={"Ticket Type": "All-access", "Peak Window": "Sat 6-8pm"},
    )
    chart = SummaryBox(stats=stats, subtitle="Three-day event summary", options=_options(mode))
    return _render_chart(chart, mode)


def _percentile_ladder(mode: str) -> str:
    data = [
        PercentileData(name="Algebra", p50=72.0, p90=89.0, p95=94.0, p99=98.0),
        PercentileData(name="Biology", p50=76.0, p90=91.0, p95=95.0, p99=99.0),
        PercentileData(name="History", p50=68.0, p90=85.0, p95=90.0, p99=96.0),
    ]
    chart = PercentileLadder(
        data=data,
        title="Exam Score Percentiles",
        metric_label="points",
        subtitle="Spring semester final exams",
        options=_options(mode),
    )
    return _render_chart(chart, mode)


def _normalized_speedup(mode: str) -> str:
    data = [
        SpeedupData(name="Laptop CPU", ratio=1.0, is_baseline=True),
        SpeedupData(name="Mobile GPU", ratio=1.65),
        SpeedupData(name="Workstation GPU", ratio=3.80),
        SpeedupData(name="Small VM", ratio=0.72),
    ]
    chart = NormalizedSpeedup(
        data=data, title="Inference Speedup vs CPU Baseline",
        subtitle="Image classification model on four hardware targets", options=_options(mode),
    )
    return _render_chart(chart, mode)


def _stacked_bar(mode: str) -> str:
    data = [
        StackedBarData(
            label="Weeknight Dinner",
            segments=[
                StackedBarSegment(phase_name="Prep", value=12_000.0),
                StackedBarSegment(phase_name="Cooking", value=22_000.0),
                StackedBarSegment(phase_name="Plating", value=6_000.0),
            ],
        ),
        StackedBarData(
            label="Weekend Brunch",
            segments=[
                StackedBarSegment(phase_name="Prep", value=18_000.0),
                StackedBarSegment(phase_name="Cooking", value=28_000.0),
                StackedBarSegment(phase_name="Plating", value=8_000.0),
            ],
        ),
    ]
    chart = StackedBar(
        data=data, title="Cooking Time Breakdown",
        subtitle="Minutes per phase for two meal types", options=_options(mode),
    )
    return _render_chart(chart, mode)


def _sparkline_table(mode: str) -> str:
    data = SparklineTableData(
        rows=["North Store", "Central Store", "South Store"],
        columns=[
            SparklineColumn(name="Revenue", values={"North Store": 82.0, "Central Store": 95.0, "South Store": 78.0}),
            SparklineColumn(name="Orders", values={"North Store": 64.0, "Central Store": 88.0, "South Store": 72.0}),
            SparklineColumn(name="Returns", values={"North Store": 6.0, "Central Store": 4.0, "South Store": 7.0}),
        ],
    )
    chart = SparklineTable(
        data=data, title="Store KPI Snapshot",
        subtitle="Revenue, orders, and returns across three locations", options=_options(mode),
    )
    return _render_chart(chart, mode)


def _cdf_chart(mode: str) -> str:
    data = [
        CDFSeriesData(name="Weekday", values=[2, 3, 4, 5, 6, 8, 10, 12, 15]),
        CDFSeriesData(name="Weekend", values=[3, 4, 5, 7, 9, 11, 14, 18, 24]),
    ]
    chart = CDFChart(
        data=data,
        title="Customer Wait Time Distribution",
        x_label="Wait Time (min)",
        y_label="Cumulative Share",
        subtitle="Weekday vs weekend service desk queues",
        options=_options(mode),
    )
    return _render_chart(chart, mode)


def _rank_table(mode: str) -> str:
    data = RankTableData(
        items=["Delivery", "Support", "Accuracy", "Onboarding"],
        groups=["Vendor A", "Vendor B", "Vendor C"],
        values={
            ("Vendor A", "Delivery"): 4.2,
            ("Vendor B", "Delivery"): 5.1,
            ("Vendor C", "Delivery"): 4.8,
            ("Vendor A", "Support"): 2.5,
            ("Vendor B", "Support"): 1.9,
            ("Vendor C", "Support"): 2.2,
            ("Vendor A", "Accuracy"): 1.8,
            ("Vendor B", "Accuracy"): 2.4,
            ("Vendor C", "Accuracy"): 1.6,
            ("Vendor A", "Onboarding"): 3.1,
            ("Vendor B", "Onboarding"): 2.7,
            ("Vendor C", "Onboarding"): 3.5,
        },
    )
    chart = RankTable(
        data=data, title="Vendor Evaluation Rankings",
        subtitle="Scored across four service dimensions", options=_options(mode),
    )
    return _render_chart(chart, mode)


CHARTS = {
    "bar_chart": _bar_chart,
    "histogram": _histogram,
    "heatmap": _heatmap,
    "box_plot": _box_plot,
    "line_chart": _line_chart,
    "scatter_plot": _scatter_plot,
    "comparison_bar": _comparison_bar,
    "diverging_bar": _diverging_bar,
    "summary_box": _summary_box,
    "percentile_ladder": _percentile_ladder,
    "normalized_speedup": _normalized_speedup,
    "stacked_bar": _stacked_bar,
    "sparkline_table": _sparkline_table,
    "cdf_chart": _cdf_chart,
    "rank_table": _rank_table,
}


def _ansi_to_html(text: str, color_map: dict[str, str] | None = None) -> str:
    converter = Ansi2HTMLConverter(inline=True, scheme="ansi2html", dark_bg=True)
    html_text = converter.convert(text, full=False)
    if not color_map:
        return html_text
    for src, dst in color_map.items():
        html_text = html_text.replace(src, dst)
    return html_text


def _estimate_height(text: str, pad: int = 72) -> int:
    lines = text.count("\n") + 1
    return min(max(lines * 24 + pad * 2, 200), 2600)


def _save_png(html_content: str, out_path: Path, text: str, *, width: int = 850) -> None:
    chrome = _chrome_binary()
    height = _estimate_height(text)
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False) as handle:
        handle.write(html_content)
        tmp_html = handle.name
    try:
        command = [
            chrome,
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--hide-scrollbars",
            "--force-device-scale-factor=2",
            f"--window-size={width},{height}",
            "--screenshot=" + str(out_path),
            "file://" + tmp_html,
        ]
        env = {**os.environ, "TERM": "xterm-256color", "FORCE_COLOR": "1"}
        for attempt in range(3):
            try:
                subprocess.run(command, check=True, capture_output=True, env=env)
                break
            except subprocess.CalledProcessError:
                if attempt == 2:
                    raise
                time.sleep(0.5)
    finally:
        Path(tmp_html).unlink(missing_ok=True)


def _crop_png(path: Path) -> None:
    image = Image.open(path).convert("RGB")
    pixels = image.load()
    width, height = image.size
    bg = (21, 24, 28)

    def is_bg(x: int, y: int) -> bool:
        pixel = pixels[x, y]
        return all(abs(pixel[idx] - bg[idx]) <= 4 for idx in range(3))

    last_row = height - 1
    for y in range(height - 1, 0, -1):
        if not all(is_bg(x, y) for x in range(0, width, 4)):
            last_row = min(y + 36, height)
            break
    image.crop((0, 0, width, last_row)).save(path)


def _render_mode(chart_name: str, mode: str) -> Path:
    text = CHARTS[chart_name](mode)
    out_dir = OUT / chart_name
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{mode}.png"
    if mode == "color":
        html_body = _ansi_to_html(text)
    elif mode == "greyscale":
        html_body = _ansi_to_html(text, GREYSCALE_COLOR_MAP)
    else:
        html_body = html.escape(text)
    _save_png(HTML_TEMPLATE.format(content=html_body), out_path, text)
    _crop_png(out_path)
    return out_path


def main() -> None:
    for chart_name in CHARTS:
        print(f"Generating {chart_name}")
        _render_mode(chart_name, "color")
        _render_mode(chart_name, "greyscale")
        _render_mode(chart_name, "monochrome")
    print(f"Generated screenshots in {OUT}")


if __name__ == "__main__":
    main()
