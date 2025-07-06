# canonmap/services/artifact_generator/ingestion/date_type_helpers.py
# Module containing date format patterns and helper constants

DATE_FORMATS = [
    # ISO formats
    "%Y-%m-%d",
    "%Y-%m-%dT%H:%M:%S",
    "%Y-%m-%dT%H:%M:%S.%f",
    "%Y-%m-%dT%H:%M:%S%z",
    "%Y-%m-%dT%H:%M:%S.%f%z",
    "%Y-%m-%d %H:%M:%S",
    "%Y-%m-%d %H:%M:%S.%f",
    "%Y-%m-%d %H:%M",
    "%Y-%m-%d", "%Y",

    # Common US formats
    "%m/%d/%Y", "%m-%d-%Y", "%m/%d/%y",
    "%m/%d/%Y %H:%M:%S", "%m/%d/%Y %I:%M:%S %p",
    "%m/%d/%y %H:%M:%S", "%m/%d/%Y %H:%M",
    "%m/%d/%Y %I:%M %p", "%m/%d",

    # Common UK/European formats
    "%d/%m/%Y", "%d-%m-%Y", "%d/%m/%y",
    "%d/%m/%Y %H:%M:%S", "%d/%m/%Y %I:%M:%S %p",
    "%d/%m/%y %H:%M:%S", "%d/%m/%Y %H:%M",
    "%d/%m/%Y %I:%M %p", "%d/%m", "%d.%m.%Y", "%d.%m.%y",

    # Other common formats
    "%Y%m%d", "%Y%m%d%H%M%S", "%Y%m%d%H%M",
    "%b %d %Y", "%B %d %Y", "%d %b %Y", "%d %B %Y",
    "%d-%b-%y", "%b %d %Y %H:%M:%S", "%B %d %Y %H:%M:%S",
    "%b %d %Y %I:%M %p", "%B %d %Y %I:%M %p",
    "%b %d", "%B %d", "%b %Y", "%B %Y",
    "%b-%d-%Y", "%B-%d-%Y",

    # Formats with timezone names/offsets
    "%Y-%m-%d %H:%M:%S %Z", "%Y-%m-%d %H:%M:%S%z",
    "%Y-%m-%d %H:%M:%S UTC%z", "%Y-%m-%d %H:%M:%S GMT%z",
    "%Y-%m-%d %H:%M:%S PST", "%Y-%m-%d %H:%M:%S EST",
    "%Y-%m-%d %H:%M:%S CST", "%Y-%m-%d %H:%M:%S MST",
    "%Y-%m-%d %H:%M:%S AEST",
    "%Y-%m-%d %H:%M:%S.%f %Z", "%Y-%m-%d %H:%M:%S.%f%z",

    # Excel/Spreadsheet formats
    "%Y-%m-%d %H:%M:%S.%f000", "%m/%d/%Y %H:%M:%S.%f000",

    # Formats with weekday names
    "%A, %B %d, %Y", "%a, %b %d, %Y",
    "%A, %d %B %Y", "%a, %d %b %Y",

    # Additional international formats
    "%Y年%m月%d日",  # Japanese
    "%d-%m-%Y %H:%M:%S", "%d-%m-%y %H:%M:%S",
    "%d/%m/%Y %H.%M.%S", "%d.%m.%Y %H:%M:%S"
]


DOMINANCE_THRESHOLD = 0.9