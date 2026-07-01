from enum import Enum

class ContentInspectionProvenance_source(str, Enum):
    Markdown = "markdown",
    Summary = "summary",
    Description = "description",
    Resource = "resource",

