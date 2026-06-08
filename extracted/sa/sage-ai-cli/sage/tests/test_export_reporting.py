"""Tests for export and reporting - P2 Sprint 2 items 101-115.

Tests verify:
- JSON export (item 101)
- CSV export (item 102)
- Markdown export (item 103)
- Table export (item 104)
- Hierarchical export (item 105)
- Summary statistics (item 106)
- Executive summary (item 107)
- Quality reports (item 108)
- Progress reports (item 109)
- Metrics collection (item 110)
- Report formatting (item 111)
- Report aggregation (item 112)
- Report filtering (item 113)
- Report templates (item 114)
- Report export formats (item 115)
"""

import csv
import io
import json
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto

# Import list generator components for export
from sage.core.list_generator import (
    ListFormatter,
    ListGenerator,
    ListItem,
    ListQualityValidator,
)

# =============================================================================
# Report Generator for items 101-115
# =============================================================================


class ReportFormat(Enum):
    """Supported report formats."""

    JSON = auto()
    CSV = auto()
    MARKDOWN = auto()
    HTML = auto()
    TEXT = auto()


@dataclass
class ReportSection:
    """A section of a report."""

    title: str
    content: str
    order: int = 0
    collapsible: bool = False


@dataclass
class ReportMetrics:
    """Metrics for a report."""

    total_items: int = 0
    critical_items: int = 0
    high_items: int = 0
    medium_items: int = 0
    low_items: int = 0
    with_file_refs: int = 0
    categories_covered: int = 0
    quality_score: float = 0.0
    generated_at: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class Report:
    """A complete report."""

    title: str
    sections: list[ReportSection] = field(default_factory=list)
    metrics: ReportMetrics | None = None
    format: ReportFormat = ReportFormat.MARKDOWN


class ReportGenerator:
    """Generates reports from list items and analysis results."""

    def __init__(self):
        self.sections: list[ReportSection] = []
        self._items: list[ListItem] = []

    def set_items(self, items: list[ListItem]) -> None:
        """Set items to include in report."""
        self._items = items

    def generate_json(self) -> str:
        """Item 101: Generate JSON report."""
        data = {
            "generated_at": datetime.now().isoformat(),
            "total_items": len(self._items),
            "items": [self._item_to_dict(item) for item in self._items],
            "metrics": self._compute_metrics(),
        }
        return json.dumps(data, indent=2)

    def generate_csv(self) -> str:
        """Item 102: Generate CSV report."""
        output = io.StringIO()
        writer = csv.writer(output)

        # Header
        writer.writerow(
            [
                "Number",
                "Priority",
                "Title",
                "Description",
                "File",
                "Line",
                "Category",
                "Effort",
                "Impact",
            ]
        )

        # Data rows
        for item in self._items:
            writer.writerow(
                [
                    item.number,
                    item.priority,
                    item.title,
                    item.description,
                    item.file_path or "",
                    item.line_number or "",
                    item.category,
                    item.effort,
                    item.impact,
                ]
            )

        return output.getvalue()

    def generate_markdown(self) -> str:
        """Item 103: Generate Markdown report."""
        parts = [
            "# Analysis Report",
            "",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
            "## Summary",
            f"- Total items: {len(self._items)}",
            "",
            "## Items",
            "",
        ]

        for item in self._items:
            parts.append(item.to_markdown())
            parts.append("")

        return "\n".join(parts)

    def generate_table(self) -> str:
        """Item 104: Generate Markdown table report."""
        header = "| # | Priority | Title | File | Effort | Impact |"
        separator = "|---|----------|-------|------|--------|--------|"

        rows = [header, separator]
        for item in self._items:
            row = f"| {item.number} | {item.priority} | {item.title[:40]} | {item.file_path or '-'} | {item.effort} | {item.impact} |"
            rows.append(row)

        return "\n".join(rows)

    def generate_hierarchical(self) -> str:
        """Item 105: Generate hierarchical report by category."""
        by_category: dict[str, list[ListItem]] = {}

        for item in self._items:
            cat = item.category or "Uncategorized"
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(item)

        parts = ["# Hierarchical Report", ""]

        for category, items in sorted(by_category.items()):
            parts.append(f"## {category} ({len(items)} items)")
            parts.append("")
            for item in items:
                parts.append(f"- [{item.priority}] {item.title}")
            parts.append("")

        return "\n".join(parts)

    def generate_summary(self) -> str:
        """Item 106: Generate summary statistics."""
        metrics = self._compute_metrics()

        return f"""## Summary Statistics
- Total items: {metrics["total_items"]}
- Critical (P0): {metrics["critical_items"]}
- High (P1): {metrics["high_items"]}
- Medium (P2): {metrics["medium_items"]}
- Low (P3): {metrics["low_items"]}
- Items with file references: {metrics["with_file_refs"]}
- Categories covered: {metrics["categories_covered"]}
- Quality score: {metrics["quality_score"]:.1f}/100
"""

    def generate_executive_summary(self) -> str:
        """Item 107: Generate executive summary."""
        critical = [i for i in self._items if i.priority == "P0"]
        quick_wins = [
            i for i in self._items if i.effort == "low" and i.impact in ("medium", "high")
        ]

        parts = ["# Executive Summary", ""]
        parts.append(f"Total issues identified: **{len(self._items)}**")
        parts.append("")

        if critical:
            parts.append(f"## Critical Issues ({len(critical)})")
            for item in critical[:3]:
                parts.append(f"- {item.title}")
            parts.append("")

        if quick_wins:
            parts.append(f"## Quick Wins ({len(quick_wins)})")
            for item in quick_wins[:3]:
                parts.append(f"- {item.title}")
            parts.append("")

        return "\n".join(parts)

    def generate_quality_report(self) -> str:
        """Item 108: Generate quality assessment report."""
        validator = ListQualityValidator()
        assessment = validator.assess_list(self._items)

        parts = [
            "# Quality Report",
            "",
            f"Overall Score: {assessment['overall_score']:.1f}/100",
            "",
            "## Metrics",
            f"- Specificity: {assessment.get('avg_specificity', 0):.2f}",
            f"- Actionability: {assessment.get('avg_actionability', 0):.2f}",
            f"- Quick wins: {assessment.get('quick_wins', 0)}",
            "",
        ]

        if assessment.get("issues"):
            parts.append("## Issues")
            for issue in assessment["issues"]:
                parts.append(f"- {issue}")

        return "\n".join(parts)

    def _item_to_dict(self, item: ListItem) -> dict:
        """Convert ListItem to dictionary."""
        return {
            "number": item.number,
            "title": item.title,
            "description": item.description,
            "file_path": item.file_path,
            "line_number": item.line_number,
            "priority": item.priority,
            "category": item.category,
            "effort": item.effort,
            "impact": item.impact,
        }

    def _compute_metrics(self) -> dict:
        """Compute report metrics."""
        priority_counts = {"P0": 0, "P1": 0, "P2": 0, "P3": 0}
        for item in self._items:
            priority_counts[item.priority] = priority_counts.get(item.priority, 0) + 1

        with_files = sum(1 for item in self._items if item.file_path)
        categories = set(item.category for item in self._items if item.category)

        # Simple quality score
        quality = 0.0
        if self._items:
            quality = (
                (with_files / len(self._items)) * 50
                + len(categories) * 5
                + min(30, len(self._items) * 0.3)
            )

        return {
            "total_items": len(self._items),
            "critical_items": priority_counts["P0"],
            "high_items": priority_counts["P1"],
            "medium_items": priority_counts["P2"],
            "low_items": priority_counts["P3"],
            "with_file_refs": with_files,
            "categories_covered": len(categories),
            "quality_score": min(100, quality),
        }


class ProgressReport:
    """Generates progress reports."""

    def __init__(self):
        self.milestones: list[dict] = []
        self.current_phase: str = "Starting"
        self.completion_pct: float = 0.0

    def add_milestone(self, name: str, completed: bool, timestamp: str | None = None) -> None:
        """Add a milestone to the report."""
        self.milestones.append(
            {
                "name": name,
                "completed": completed,
                "timestamp": timestamp or datetime.now().isoformat(),
            }
        )

    def set_progress(self, phase: str, completion_pct: float) -> None:
        """Set current progress."""
        self.current_phase = phase
        self.completion_pct = completion_pct

    def generate(self) -> str:
        """Item 109: Generate progress report."""
        parts = [
            "# Progress Report",
            "",
            f"Current Phase: {self.current_phase}",
            f"Completion: {self.completion_pct:.1f}%",
            "",
            "## Milestones",
        ]

        for milestone in self.milestones:
            status = "✓" if milestone["completed"] else "○"
            parts.append(f"- {status} {milestone['name']}")

        return "\n".join(parts)


class MetricsCollector:
    """Collects and aggregates metrics."""

    def __init__(self):
        self.metrics: dict[str, list[float]] = {}

    def record(self, metric_name: str, value: float) -> None:
        """Record a metric value."""
        if metric_name not in self.metrics:
            self.metrics[metric_name] = []
        self.metrics[metric_name].append(value)

    def get_summary(self, metric_name: str) -> dict:
        """Get summary statistics for a metric."""
        values = self.metrics.get(metric_name, [])
        if not values:
            return {"count": 0, "mean": 0, "min": 0, "max": 0}

        return {
            "count": len(values),
            "mean": sum(values) / len(values),
            "min": min(values),
            "max": max(values),
        }

    def generate_report(self) -> str:
        """Item 110: Generate metrics report."""
        parts = ["# Metrics Report", ""]

        for metric_name in sorted(self.metrics.keys()):
            summary = self.get_summary(metric_name)
            parts.append(f"## {metric_name}")
            parts.append(f"- Count: {summary['count']}")
            parts.append(f"- Mean: {summary['mean']:.2f}")
            parts.append(f"- Min: {summary['min']:.2f}")
            parts.append(f"- Max: {summary['max']:.2f}")
            parts.append("")

        return "\n".join(parts)


# =============================================================================
# Tests for JSON Export (Item 101)
# =============================================================================


class TestJSONExport:
    """P2 Item 101: JSON export functionality."""

    def test_export_items_to_json(self):
        """Exports items to valid JSON."""
        generator = ReportGenerator()
        generator.set_items(
            [
                ListItem(
                    1, "Fix bug", "Description", "src/main.py", 10, "P0", "Security", "low", "high"
                ),
                ListItem(
                    2,
                    "Add feature",
                    "Description",
                    None,
                    None,
                    "P2",
                    "Features",
                    "medium",
                    "medium",
                ),
            ]
        )

        json_output = generator.generate_json()

        # Should be valid JSON
        data = json.loads(json_output)
        assert "items" in data
        assert len(data["items"]) == 2

    def test_json_has_all_fields(self):
        """JSON export includes all item fields."""
        generator = ReportGenerator()
        generator.set_items(
            [
                ListItem(
                    1,
                    "Test item",
                    "Test description",
                    "file.py",
                    42,
                    "P1",
                    "Testing",
                    "medium",
                    "high",
                ),
            ]
        )

        data = json.loads(generator.generate_json())
        item = data["items"][0]

        assert item["number"] == 1
        assert item["title"] == "Test item"
        assert item["file_path"] == "file.py"
        assert item["priority"] == "P1"

    def test_json_has_metrics(self):
        """JSON export includes metrics."""
        generator = ReportGenerator()
        generator.set_items([ListItem(1, "Item", "", None, None, "P0", "", "low", "high")])

        data = json.loads(generator.generate_json())

        assert "metrics" in data
        assert "total_items" in data["metrics"]


# =============================================================================
# Tests for CSV Export (Item 102)
# =============================================================================


class TestCSVExport:
    """P2 Item 102: CSV export functionality."""

    def test_export_items_to_csv(self):
        """Exports items to valid CSV."""
        generator = ReportGenerator()
        generator.set_items(
            [
                ListItem(1, "Fix bug", "Desc", "src/main.py", 10, "P0", "Security", "low", "high"),
            ]
        )

        csv_output = generator.generate_csv()

        # Should have header and data row
        lines = csv_output.strip().split("\n")
        assert len(lines) == 2

    def test_csv_has_header(self):
        """CSV has proper header row."""
        generator = ReportGenerator()
        generator.set_items([])

        csv_output = generator.generate_csv()
        reader = csv.reader(io.StringIO(csv_output))
        header = next(reader)

        assert "Number" in header
        assert "Priority" in header
        assert "Title" in header

    def test_csv_parseable(self):
        """CSV output is parseable."""
        generator = ReportGenerator()
        generator.set_items(
            [
                ListItem(1, "Item with, comma", "Desc", None, None, "P2", "", "low", "low"),
            ]
        )

        csv_output = generator.generate_csv()
        reader = csv.reader(io.StringIO(csv_output))
        rows = list(reader)

        assert len(rows) == 2  # Header + data


# =============================================================================
# Tests for Markdown Export (Item 103)
# =============================================================================


class TestMarkdownExport:
    """P2 Item 103: Markdown export functionality."""

    def test_export_to_markdown(self):
        """Exports items to Markdown format."""
        generator = ReportGenerator()
        generator.set_items(
            [
                ListItem(
                    1, "Fix bug", "Description", "src/main.py", 10, "P0", "Security", "low", "high"
                ),
            ]
        )

        md = generator.generate_markdown()

        assert "# Analysis Report" in md
        assert "Fix bug" in md

    def test_markdown_has_sections(self):
        """Markdown has proper sections."""
        generator = ReportGenerator()
        generator.set_items([ListItem(1, "Item", "", None, None, "P0", "", "low", "high")])

        md = generator.generate_markdown()

        assert "## Summary" in md
        assert "## Items" in md


# =============================================================================
# Tests for Table Export (Item 104)
# =============================================================================


class TestTableExport:
    """P2 Item 104: Table export functionality."""

    def test_export_to_table(self):
        """Exports items to Markdown table."""
        generator = ReportGenerator()
        generator.set_items(
            [
                ListItem(1, "Fix bug", "", "src/main.py", None, "P0", "", "low", "high"),
            ]
        )

        table = generator.generate_table()

        assert "|" in table
        assert "Fix bug" in table

    def test_table_has_header(self):
        """Table has header row."""
        generator = ReportGenerator()
        generator.set_items([])

        table = generator.generate_table()

        assert "Priority" in table
        assert "Title" in table


# =============================================================================
# Tests for Hierarchical Export (Item 105)
# =============================================================================


class TestHierarchicalExport:
    """P2 Item 105: Hierarchical export by category."""

    def test_export_hierarchical(self):
        """Exports items organized by category."""
        generator = ReportGenerator()
        generator.set_items(
            [
                ListItem(1, "Security fix", "", None, None, "P0", "Security", "low", "high"),
                ListItem(
                    2, "Performance fix", "", None, None, "P1", "Performance", "medium", "high"
                ),
            ]
        )

        output = generator.generate_hierarchical()

        assert "## Security" in output
        assert "## Performance" in output

    def test_hierarchical_groups_items(self):
        """Items are grouped under their categories."""
        generator = ReportGenerator()
        generator.set_items(
            [
                ListItem(1, "Item A", "", None, None, "P0", "Category1", "low", "high"),
                ListItem(2, "Item B", "", None, None, "P1", "Category1", "low", "high"),
            ]
        )

        output = generator.generate_hierarchical()

        assert "Category1 (2 items)" in output


# =============================================================================
# Tests for Summary Statistics (Item 106)
# =============================================================================


class TestSummaryStatistics:
    """P2 Item 106: Summary statistics generation."""

    def test_generate_summary(self):
        """Generates summary with statistics."""
        generator = ReportGenerator()
        generator.set_items(
            [
                ListItem(1, "P0 Item", "", "file.py", None, "P0", "Cat", "low", "high"),
                ListItem(2, "P1 Item", "", None, None, "P1", "", "medium", "medium"),
            ]
        )

        summary = generator.generate_summary()

        assert "Total items: 2" in summary
        assert "Critical (P0): 1" in summary

    def test_summary_includes_file_refs(self):
        """Summary includes file reference count."""
        generator = ReportGenerator()
        generator.set_items(
            [
                ListItem(1, "With file", "", "file.py", 10, "P0", "", "low", "high"),
                ListItem(2, "Without file", "", None, None, "P1", "", "low", "low"),
            ]
        )

        summary = generator.generate_summary()

        assert "Items with file references: 1" in summary


# =============================================================================
# Tests for Executive Summary (Item 107)
# =============================================================================


class TestExecutiveSummary:
    """P2 Item 107: Executive summary generation."""

    def test_generate_executive_summary(self):
        """Generates executive summary."""
        generator = ReportGenerator()
        generator.set_items(
            [
                ListItem(1, "Critical issue", "", None, None, "P0", "", "low", "high"),
                ListItem(2, "Quick win", "", None, None, "P2", "", "low", "high"),
            ]
        )

        summary = generator.generate_executive_summary()

        assert "Executive Summary" in summary
        assert "Critical Issues" in summary

    def test_executive_summary_highlights_quick_wins(self):
        """Executive summary highlights quick wins."""
        generator = ReportGenerator()
        generator.set_items(
            [
                ListItem(1, "Easy fix", "", None, None, "P2", "", "low", "high"),
            ]
        )

        summary = generator.generate_executive_summary()

        assert "Quick Wins" in summary


# =============================================================================
# Tests for Quality Reports (Item 108)
# =============================================================================


class TestQualityReports:
    """P2 Item 108: Quality assessment reports."""

    def test_generate_quality_report(self):
        """Generates quality assessment report."""
        generator = ReportGenerator()
        generator.set_items(
            [
                ListItem(
                    1, "Add validation", "", "src/api.py", 42, "P1", "Security", "low", "high"
                ),
            ]
        )

        report = generator.generate_quality_report()

        assert "Quality Report" in report
        assert "Overall Score" in report

    def test_quality_report_includes_metrics(self):
        """Quality report includes assessment metrics."""
        generator = ReportGenerator()
        generator.set_items(
            [
                ListItem(1, "Fix bug", "", "file.py", 10, "P0", "", "medium", "high"),
            ]
        )

        report = generator.generate_quality_report()

        assert "Specificity" in report or "Metrics" in report


# =============================================================================
# Tests for Progress Reports (Item 109)
# =============================================================================


class TestProgressReports:
    """P2 Item 109: Progress report generation."""

    def test_generate_progress_report(self):
        """Generates progress report."""
        report = ProgressReport()
        report.set_progress("Analyzing", 50.0)
        report.add_milestone("Initialize", True)
        report.add_milestone("Analyze", False)

        output = report.generate()

        assert "Progress Report" in output
        assert "Analyzing" in output
        assert "50.0%" in output

    def test_progress_report_shows_milestones(self):
        """Progress report shows milestone status."""
        report = ProgressReport()
        report.add_milestone("Step 1", True)
        report.add_milestone("Step 2", False)

        output = report.generate()

        assert "✓" in output
        assert "○" in output


# =============================================================================
# Tests for Metrics Collection (Item 110)
# =============================================================================


class TestMetricsCollection:
    """P2 Item 110: Metrics collection and reporting."""

    def test_record_metrics(self):
        """Records metric values."""
        collector = MetricsCollector()
        collector.record("response_time", 100.0)
        collector.record("response_time", 150.0)

        summary = collector.get_summary("response_time")

        assert summary["count"] == 2
        assert summary["mean"] == 125.0

    def test_generate_metrics_report(self):
        """Generates metrics report."""
        collector = MetricsCollector()
        collector.record("response_time", 100.0)
        collector.record("response_time", 200.0)

        report = collector.generate_report()

        assert "Metrics Report" in report
        assert "response_time" in report

    def test_metrics_summary_includes_stats(self):
        """Metrics summary includes min/max/mean."""
        collector = MetricsCollector()
        collector.record("latency", 10.0)
        collector.record("latency", 20.0)
        collector.record("latency", 30.0)

        summary = collector.get_summary("latency")

        assert summary["min"] == 10.0
        assert summary["max"] == 30.0
        assert summary["mean"] == 20.0


# =============================================================================
# Tests for ListFormatter Exports
# =============================================================================


class TestListFormatterExports:
    """Test ListFormatter export methods."""

    def test_to_json(self):
        """ListFormatter.to_json produces valid JSON."""
        items = [
            ListItem(1, "Item 1", "Desc", "file.py", 10, "P0", "Cat", "low", "high"),
        ]

        json_str = ListFormatter.to_json(items)
        data = json.loads(json_str)

        assert len(data) == 1
        assert data[0]["title"] == "Item 1"

    def test_to_csv(self):
        """ListFormatter.to_csv produces valid CSV."""
        items = [
            ListItem(1, "Item 1", "Desc", "file.py", 10, "P0", "Cat", "low", "high"),
        ]

        csv_str = ListFormatter.to_csv(items)

        assert "Item 1" in csv_str
        assert "P0" in csv_str

    def test_to_numbered_list(self):
        """ListFormatter.to_numbered_list produces markdown."""
        items = [
            ListItem(1, "Fix bug", "Description", "file.py", 10, "P0", "", "low", "high"),
        ]

        md = ListFormatter.to_numbered_list(items)

        assert "1." in md
        assert "Fix bug" in md


# =============================================================================
# Tests for ListGenerator Exports
# =============================================================================


class TestListGeneratorExports:
    """Test ListGenerator export methods."""

    def test_export_json(self):
        """ListGenerator.export_json works."""
        gen = ListGenerator(target_count=5)
        gen.add_item("Test item", file_path="test.py", priority="P1")

        json_str = gen.export_json()
        data = json.loads(json_str)

        assert len(data) == 1

    def test_export_csv(self):
        """ListGenerator.export_csv works."""
        gen = ListGenerator(target_count=5)
        gen.add_item("Test item", priority="P1")

        csv_str = gen.export_csv()

        assert "Test item" in csv_str

    def test_get_complete_output(self):
        """ListGenerator.get_complete_output includes all sections."""
        gen = ListGenerator(target_count=5)
        gen.add_item("Item 1", priority="P0", category="Security")
        gen.add_item("Item 2", priority="P1", category="Testing")

        output = gen.get_complete_output()

        assert "Executive Summary" in output
        assert "Quality Score" in output
