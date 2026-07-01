from enum import Enum

class ContentInspectionCoverage_source_kind(str, Enum):
    Inline_markdown = "inline_markdown",
    Stored_summary = "stored_summary",
    Stored_description = "stored_description",
    Resource_name = "resource_name",

