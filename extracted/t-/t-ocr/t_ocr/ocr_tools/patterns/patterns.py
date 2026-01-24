"""Module for Patterns."""
import re

__amount_pre_pattern = r"(?:(?<=\D)|(?<=^))"
__amount_post_pattern = r"(?:(?=\D)|(?=$))"

AMOUNT_PATTERN = re.compile(rf"{__amount_pre_pattern}-?\d+[,\.\d]*(,\.\d{1, 2})?{__amount_post_pattern}")

ADDRESS_PATTERN = re.compile(
    r"^(\d+)\s+([\w\s\-.]+)[,\s]+([a-zA-Z\s-]+)[,\s]+([A-Z]{2,})\s+(\d{5}$|\d{5}\-\d{4})\s+([A-Z]+\-[A-Z]{2})?",
    re.MULTILINE,
)
ZIP_PATTERN = re.compile(r"(^\d{5}$|^\d{5}\-\d{4}$)")

EMAIL_PATTERN = re.compile(
    r"[A-Za-z0-9#!%$‘&+*–/=?^_`.{|}~]"
    r"[A-Za-z0-9#!%$‘&+*–/=?^_`.{|}~\.]*"
    r"[A-Za-z0-9#!%$‘&+*–/=?^_`.{|}~]"
    r"@"
    r"[A-Za-z0-9][A-Za-z0-9-\.]*[A-Za-z0-9]"
    r"\."
    r"[A-Za-z0-9][A-Za-z0-9-]*[A-Za-z0-9]"
)

_DATE_PATTERNS = [
    # 02/17/2009 | 17/ 2/2009
    re.compile(r"\d{1,2} *[\/\-\. _] *\d{1,2} *[\/\-\. _] *\d{2,4}"),
    # 2009/02/17 | 2009/ 2/17
    re.compile(r"\d{2,4} *[\/\-\. _] *\d{1,2} *[\/\-\. _] *\d{1,2}"),
    #  September 17, 2009 | Feb 17, 2014
    re.compile(r"[A-Za-z]{3,9} ?\d{1,2},? ?\d{4}"),
    # 2009, February 17 | 2009, Feb 17
    re.compile(r"\d{4},? ?[A-Za-z]{3,9} ?\d{1,2}"),
    # 17 February, 2009 | 17 Feb, 2009 | 17Feb2009
    re.compile(r"\d{1,2} ?[A-Za-z]{3,9},? ?\d{4}"),
    # 17 February, 2009 | 17 Feb, 2009 | 17Feb2009
    re.compile(r"\d{1,2} ?[A-Za-z]{3,9},? ?\d{4}"),
]

__date_pre_pattern = r"(?:(?<=\W)|(?<=^))"
__date_post_pattern = r"(?:(?=\W)|(?=$))"

DATE_PATTERN = re.compile(
    r"|".join([rf"{__date_pre_pattern}{d_p.pattern}{__date_post_pattern}" for d_p in _DATE_PATTERNS])
)

_TIME_PATTERNS = [
    # 13:11:34.222-0700
    re.compile(r"\d{1,2}:\d{1,2}:\d{1,2}[\.,]\d+Z? ?[+-]\d{4}"),
    # 18:20:11 +0000 | 18:20 +0000
    re.compile(r"\d{1,2}:\d{1,2}(:\d{1,2})? ?[+-]\d{4}"),
    # 01:44:20.393 | 01:44:20.393Z
    re.compile(r"\d{1,2}:\d{1,2}:\d{1,2}[\.,]\d+Z?"),
    # 2:39:58 AM | 9:20pm
    re.compile(r"\d{1,2}:\d{1,2}(:\d{1,2})? ?[APap][Mm]"),
    # 18:20:11 | 18:20
    re.compile(r"\d{1,2}:\d{1,2}(:\d{1,2})?"),
]
__time_pre_pattern = r"(?:(?<=[\WT])|(?<=^))"
__time_post_pattern = r"(?:(?=\W)|(?=$))"

TIME_PATTERN = re.compile(
    r"|".join([rf"({__time_pre_pattern}{d_p.pattern}{__time_post_pattern})" for d_p in _TIME_PATTERNS])
)

__datetime_pre_pattern = r"(?:(?<=[\W])|(?<=^))"
__datetime_middle_pattern = r"[\sT']+"
__datetime_post_pattern = r"(?:(?=\W)|(?=$))"

DATE_TIME_PATTERN = re.compile(
    r"|".join(
        [
            rf"{__datetime_pre_pattern}{d_p.pattern}{__datetime_middle_pattern}{t_p.pattern}{__datetime_post_pattern}"
            for d_p in _DATE_PATTERNS
            for t_p in _TIME_PATTERNS
        ]
    )
)
