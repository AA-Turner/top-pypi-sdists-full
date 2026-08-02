"""Pretty-print document content statistics reports using rich."""

from __future__ import annotations

__all__ = ["print_content_stats_report"]

from typing import Any

from rich import get_console
from rich.console import Console, Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text


def _format_value(value: Any) -> str:
    """Format a single stat value into a rich-markup display string.

    Applies type-specific formatting so numbers, booleans, and missing
    values all render consistently across the report: floats get two
    decimal places, integers get thousands separators, booleans render
    as colored yes/no, and ``None`` renders as a dim em-dash.

    Args:
        value: The raw stat value to format. May be ``None``, ``bool``,
            ``int``, ``float``, or any other type (falls back to
            ``str(value)``).

    Returns:
        A string, potentially containing rich markup tags (e.g.
        ``"[dim]—[/dim]"``), ready to be embedded directly into a
        ``Table`` cell or ``Text`` object.

    Examples:
        >>> _format_value(None)
        '[dim]—[/dim]'
        >>> _format_value(True)
        '[green]yes[/green]'
        >>> _format_value(3.14159)
        '3.14'
        >>> _format_value(1000)
        '1,000'
        >>> _format_value("doc-1")
        'doc-1'
    """
    if value is None:
        return "[dim]—[/dim]"
    if isinstance(value, bool):
        return "[green]yes[/green]" if value else "[yellow]no[/yellow]"
    if isinstance(value, float):
        return f"{value:,.2f}"
    if isinstance(value, int):
        return f"{value:,}"
    return str(value)


def _format_percentage_of_total(count: int, total: int) -> str:
    """Format ``count`` as a dim, parenthesized percentage of ``total``.

    Used to annotate data-quality counts (e.g. "3 empty docs") with
    their share of the overall corpus, so severity can be judged at a
    glance without mental math.

    Args:
        count: The sub-count to express as a percentage (e.g. number of
            empty documents).
        total: The total document count. If falsy (zero), no percentage
            can be computed.

    Returns:
        A string like ``" [dim](0.3%)[/dim]"`` (with a leading space,
        ready to be appended directly after a formatted count), or an
        empty string if ``total`` is falsy.

    Examples:
        >>> _format_percentage_of_total(3, 1000)
        ' [dim](0.3%)[/dim]'
        >>> _format_percentage_of_total(0, 0)
        ''
    """
    if not total:
        return ""
    return f" [dim]({count / total:.1%})[/dim]"


def _build_stats_table(
    stats: dict[str, Any],
    *,
    is_exact: bool,
    p_suffix: str,
    dup_key: str,
    count: int,
) -> tuple[Table, bool]:
    """Build the combined "length distribution" + "data quality" table.

    Renders a single two-column (``Metric``, ``Value``) rich ``Table``
    with two labeled sections: length-distribution metrics (average,
    std dev, min, max, p50/p90/p99), and data-quality checks (empty
    content, whitespace-only content, non-string content, missing id,
    missing metadata, duplicates). Data-quality rows whose count is
    non-zero are highlighted in yellow, both the label and the value.

    Args:
        stats: The full analysis report dict (as returned by
            ``compute_doc_content_stats_exact`` or
            ``compute_doc_content_stats_approx``).
        is_exact: Whether the report used exact (``True``) or
            approximate (``False``) computation. Controls the section
            header suffix (``" (est.)"`` for approximate) and the
            duplicates row label (``"Duplicates"`` vs. ``"Duplicates
            (approx.)"``).
        p_suffix: Either ``""`` (exact reports, keys like
            ``"p50_chars"``) or ``"_approx"`` (approximate reports,
            keys like ``"p50_chars_approx"``), used to look up the
            correct percentile keys in ``analysis``.
        dup_key: The dict key under which the duplicate count is
            stored — ``"duplicate_count"`` for exact reports or
            ``"approx_duplicate_count"`` for approximate reports.
        count: Total document count, used as the denominator when
            computing each data-quality check's percentage of total.

    Returns:
        A tuple of ``(table, any_issues)`` where ``table`` is the built
        ``rich.table.Table`` and ``any_issues`` is ``True`` if at least
        one data-quality check had a non-zero count.

    Examples:
        >>> analysis = {"avg_chars": 5, "empty_count": 0, "duplicate_count": 0}
        >>> table, any_issues = _build_stats_table(
        ...     analysis, is_exact=True, p_suffix="", dup_key="duplicate_count", count=10
        ... )
        >>> any_issues
        False
    """
    table = Table(show_header=True, header_style="bold cyan", box=None, padding=(0, 1))
    table.add_column("Metric")
    table.add_column("Value", justify="right")

    def section(label: str) -> None:
        table.add_row(f"[dim]{label}[/dim]", "")

    def row(label: str, value: str, *, flagged: bool = False) -> None:
        label_text = f"[yellow]{label}[/yellow]" if flagged else label
        value_text = f"[yellow]{value}[/yellow]" if flagged else value
        table.add_row(f"  {label_text}", value_text)

    section(f"length distribution{'' if is_exact else '  (est.)'}")
    row("Average", _format_value(stats.get("avg_chars")))
    row("Std dev", _format_value(stats.get("std_dev_chars")))
    row("Min", _format_value(stats.get("min_chars")))
    row("Max", _format_value(stats.get("max_chars")))
    row("p50", _format_value(stats.get(f"p50_chars{p_suffix}")))
    row("p90", _format_value(stats.get(f"p90_chars{p_suffix}")))
    row("p99", _format_value(stats.get(f"p99_chars{p_suffix}")))

    section("data quality")
    health_checks = [
        ("Empty content", stats.get("empty_count", 0)),
        ("Whitespace-only", stats.get("whitespace_only_count", 0)),
        ("Non-string content", stats.get("none_or_non_str_content_count", 0)),
        ("Missing id", stats.get("none_id_count", 0)),
        ("Missing metadata", stats.get("missing_metadata_count", 0)),
        ("Duplicates" if is_exact else "Duplicates (approx.)", stats.get(dup_key, 0)),
    ]

    any_issues = False
    for label, value in health_checks:
        flagged = bool(value)
        any_issues = any_issues or flagged
        row(
            label,
            f"{_format_value(value)}{_format_percentage_of_total(value, count)}",
            flagged=flagged,
        )

    return table, any_issues


def _build_overview_line(stats: dict[str, Any], count: int) -> Text:
    """Build the "N docs · N chars" summary line shown at the top of the
    report.

    Args:
        stats: The full analysis report dict. Only ``total_chars`` is read
            from it.
        count: Total document count, shown as the first part of the
            line (passed separately from ``analysis`` since callers
            already need to compute/validate it, e.g. for the empty-
            input early return).

    Returns:
        A ``rich.text.Text`` object with the document count in bold and
        the character count in dim, separated by a middle dot.

    Examples:
        >>> text = _build_overview_line({"total_chars": 500}, 10)
        >>> text.plain
        '10 docs  ·  500 chars'
    """
    overview = Text()
    overview.append(f"{_format_value(count)} docs", style="bold")
    overview.append("  ·  ")
    overview.append(f"{_format_value(stats.get('total_chars'))} chars", style="dim")
    return overview


def _build_doc_ids_grid(stats: dict[str, Any]) -> Table:
    """Build the "Shortest: ... / Longest: ..." two-line doc-id grid.

    Shown below the metrics table so the shortest/longest document ids
    are visible without cluttering the table's Min/Max rows.

    Args:
        stats: The full analysis report dict. Reads ``min_doc_id`` and
            ``max_doc_id``; missing keys render as an empty string.

    Returns:
        A borderless ``rich.table.Table`` grid with two rows
        (``Shortest:``/``Longest:``), the label column dimmed.

    Examples:
        >>> grid = _build_doc_ids_grid({"min_doc_id": "a", "max_doc_id": "z"})
        >>> isinstance(grid, Table)
        True
    """
    doc_ids = Table.grid(padding=(0, 1))
    doc_ids.add_column(style="dim")
    doc_ids.add_column()
    doc_ids.add_row("Shortest:", str(stats.get("min_doc_id", "")))
    doc_ids.add_row("Longest:", str(stats.get("max_doc_id", "")))
    return doc_ids


def _build_status_line(any_issues: bool) -> Text:
    """Build the single-line pass/fail summary shown below the table.

    Args:
        any_issues: Whether any data-quality check was flagged (as
            returned by ``_build_stats_table``).

    Returns:
        A bold ``rich.text.Text``: green "✓ no issues detected" if
        ``any_issues`` is ``False``, or yellow "⚠ potential issues
        detected" if ``True``.

    Examples:
        >>> _build_status_line(False).plain
        '✓ no issues detected'
        >>> _build_status_line(True).plain
        '⚠ potential issues detected'
    """
    if any_issues:
        return Text("⚠ potential issues detected", style="bold yellow")
    return Text("✓ no issues detected", style="bold green")


def _build_approx_footnote_items(
    stats: dict[str, Any], *, is_exact: bool, count: int
) -> list[Text]:
    """Build the footer note explaining Bloom-filter/reservoir settings
    for approximate reports.

    For exact reports, no footnote is needed (there's nothing
    approximate to caveat), so this returns an empty list.

    Args:
        stats: The full analysis report dict. Reads
            ``bloom_filter_fp_rate`` and ``reservoir_sample_size``.
        is_exact: Whether the report used exact computation. If
            ``True``, no footnote is produced.
        count: Total document count, included in the footnote text so
            the reader can judge the reservoir sample's coverage (e.g.
            "sample size=1000 of 1000 docs").

    Returns:
        A list containing a single dim, italic ``rich.text.Text`` with
        the Bloom filter false-positive rate and reservoir sample size,
        or an empty list if ``is_exact`` is ``True``.

    Examples:
        >>> analysis = {"bloom_filter_fp_rate": 0.01, "reservoir_sample_size": 100}
        >>> items = _build_approx_footnote_items(analysis, is_exact=False, count=100)
        >>> len(items)
        1
        >>> _build_approx_footnote_items({}, is_exact=True, count=10)
        []
    """
    if is_exact:
        return []

    fp_rate = stats.get("bloom_filter_fp_rate")
    sample_size = stats.get("reservoir_sample_size")
    return [
        Text(
            f"Approximate report — Bloom filter fp_rate={fp_rate!r}, "
            f"percentile/std-dev sample size={sample_size!r} of {count!r} docs",
            style="italic dim",
        )
    ]


def print_content_stats_report(
    stats: dict[str, Any],
    *,
    title: str = "Document Content Stats",
    console: Console | None = None,
) -> None:
    """Render a document-content-analysis report (from
    ``compute_doc_content_stats_exact`` or
    ``compute_doc_content_stats_approx``) as a single wide table, with
    one row per metric, followed by a schematic length-distribution bar
    chart, in the terminal. The panel shrinks to fit its content rather
    than stretching to the full terminal width.

    Automatically detects whether the report is exact or approximate
    (via the ``duplicate_count_exact`` / ``percentiles_exact`` keys) and
    labels sections accordingly (in both the panel title and subtitle),
    including a footer note about the Bloom-filter false-positive rate
    and reservoir sample size when relevant, shown after the bar chart.

    This function orchestrates the report layout by delegating each
    section to a dedicated builder: ``_build_stats_table`` (metrics
    table), ``_build_overview_line`` (doc/char count summary),
    ``_build_doc_ids_grid`` (shortest/longest doc ids),
    ``_build_status_line`` (pass/fail summary),
    ``_build_bar_chart_items`` (schematic distribution shape), and
    ``_build_approx_footnote_items`` (approximate-report caveat).

    Args:
        stats: The dict returned by ``compute_doc_content_stats_exact``
            or ``compute_doc_content_stats_approx``. Expected to
            contain (at minimum) a ``count`` key; all other keys are
            read defensively via ``.get(...)`` with sensible defaults,
            so a partial dict will not raise but may render blanks.
        title: Panel title shown above the report, at the top-left of
            the panel border.
        console: An existing ``rich.console.Console`` to print to. A
            new one is created via ``Console()`` if not provided.

    Returns:
        None. Output is printed directly to ``console``.

    Examples:
        >>> analysis = {
        ...     "count": 2, "total_chars": 10, "avg_chars": 5,
        ...     "std_dev_chars": 1, "min_chars": 4, "max_chars": 6,
        ...     "min_doc_id": "a", "max_doc_id": "b",
        ...     "p50_chars": 5, "p90_chars": 6, "p99_chars": 6,
        ...     "empty_count": 0, "whitespace_only_count": 0,
        ...     "none_or_non_str_content_count": 0, "none_id_count": 0,
        ...     "missing_metadata_count": 0, "duplicate_count": 0,
        ...     "duplicate_count_exact": True, "percentiles_exact": True,
        ... }
        >>> print_content_stats_report(analysis)  # doctest: +SKIP
    """
    console = console or get_console()

    is_exact = stats.get("duplicate_count_exact", True)
    dup_key = "duplicate_count" if "duplicate_count" in stats else "approx_duplicate_count"
    p_suffix = "" if stats.get("percentiles_exact", True) else "_approx"
    count = stats.get("count", 0)

    mode_label = "exact" if is_exact else "approximate"
    panel_title = f"[bold]{title}[/bold]  [dim]({mode_label})[/dim]"

    if count == 0:
        console.print(
            Panel(
                "[dim]No documents processed.[/dim]",
                title=panel_title,
                title_align="left",
                subtitle=f"[dim]{mode_label}[/dim]",
                border_style="dim",
                expand=False,
            )
        )
        return

    table, any_issues = _build_stats_table(
        stats, is_exact=is_exact, p_suffix=p_suffix, dup_key=dup_key, count=count
    )
    overview = _build_overview_line(stats, count)
    doc_ids = _build_doc_ids_grid(stats)
    status_line = _build_status_line(any_issues)
    footnote_items = _build_approx_footnote_items(stats, is_exact=is_exact, count=count)

    body = Group(
        overview,
        Text(),
        table,
        Text(),
        doc_ids,
        Text(),
        status_line,
        *([Text(), *footnote_items] if footnote_items else []),
    )

    console.print(
        Panel(
            body,
            title=panel_title,
            title_align="left",
            subtitle=f"[dim]{mode_label}[/dim]",
            border_style="cyan",
            expand=False,
        )
    )
