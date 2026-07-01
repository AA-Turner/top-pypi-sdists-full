"""AIRT Reporting -- render campaign analytics into consumable formats.

- :func:`generate_markdown_report` -- Markdown for human review
- :func:`generate_json_report` -- JSON for CI/CD integration
- :func:`generate_executive_summary` -- optional LLM-enhanced narrative
"""

from dreadnode.airt.reporting.json_report import generate_json_report
from dreadnode.airt.reporting.llm_summary import generate_executive_summary
from dreadnode.airt.reporting.markdown import generate_markdown_report

__all__ = [
    "generate_executive_summary",
    "generate_json_report",
    "generate_markdown_report",
]
