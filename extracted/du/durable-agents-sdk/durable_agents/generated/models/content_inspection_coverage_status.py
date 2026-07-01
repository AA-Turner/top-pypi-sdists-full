from enum import Enum

class ContentInspectionCoverage_status(str, Enum):
    Full = "full",
    Partial = "partial",
    Preview = "preview",
    Truncated = "truncated",

