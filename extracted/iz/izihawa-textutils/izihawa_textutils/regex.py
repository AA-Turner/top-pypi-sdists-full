import re
from typing import Final

NON_ALNUMWHITESPACE_REGEX = re.compile(r"([^\s\w])+")
EMAIL_REGEX = re.compile(r"([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})")
HASHTAG_REGEX = re.compile(r"([#@]+)([A-Za-z0-9_]+)")
MULTIWHITESPACE_REGEX = re.compile(r"\s+")
STICKER_REGEX = re.compile(
    "^[\U0001F1E0-\U0001F1FF"
    "\U0001F300-\U0001F5FF"
    "\U0001F600-\U0001F64F"
    "\U0001F680-\U0001F6FF"
    "\U0001F700-\U0001F77F"
    "\U0001F780-\U0001F7FF"
    "\U0001F800-\U0001F8FF"
    "\U0001F900-\U0001F9FF"
    "\U0001FA00-\U0001FA6F"
    "\U0001FA70-\U0001FAFF"
    "\U00002702-\U000027B0]$",
    flags=re.UNICODE,
)
URL_REGEX_TEXT = r"(https?|ftp)?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
URL_REGEX = re.compile(URL_REGEX_TEXT)
HIDDEN_CHAR = "‌"
TELEGRAM_LINK_REGEX = re.compile("(?:https?://)?t\\.me/(?!joinchat/)([A-Za-z0-9_]+)")

DOI_WILDCARD_REGEX_TEXT = r"(10.\d{4,9}).*\.\*"
DOI_REGEX_TEXT = (
    r"(?:doi.org/)?(10.\d{4,9})\s?(?:/|%2[Ff])\s?([%-._;()<>/:A-Za-z0-9]+[^.?\s])"
)
DOI_REGEX = re.compile(DOI_REGEX_TEXT)
ISBN_REGEX = re.compile(r"^(?:[iI][sS][bB][nN]\:?\s*)?((97(8|9))?\-?\d{9}(\d|X))$")
MD5_REGEX = re.compile(r"([A-Fa-f0-9]{32})")
ONLY_DOI_REGEX = re.compile(r"^(10.\d{4,9})\s?/\s?([-._;()<>/:A-Za-z0-9]+[^.?\s])$")
PUBMED_ID_REGEX = re.compile(
    r"(?:(?:https?://)?(?:www.)?ncbi.nlm.nih.gov/pubmed/|[Pp][Mm][Ii][Dd]\s?:?\s*)([0-9]+)"
)
CJK_CHAR_REGEX_TEXT = r"[\u4e00-\u9fff]"
MATHPIX_TABLE_RE = re.compile(
    r"(?P<open_tag>\\begin\{tabular})\{\s*(?P<header>\| \|)\s*}(?P<content>.*)(?P<close_tag>\\end\{tabular})"
)
TABLE_RE = re.compile(
    r"(?P<prefix>[^|\n][^\n]*\n{1,2})?(?P<table>(?:\|[^\n]+\|(?:\n|$))+)(?P<suffix>[^\n|]+)?",
    flags=re.DOTALL | re.MULTILINE,
)
TABLE_HEADER_RE = re.compile(r"(?:tab|таб)(?:\.|le|лица) *([^\n]*?)\n", flags=re.IGNORECASE | re.UNICODE)
SEPARATOR_RE = re.compile(r"^\|[-: |]+\|$")
UNICODE_BULLETS: Final[list[str]] = [
    "\u0095",
    "\u2022",
    "\u2023",
    "\u2043",
    "\u3164",
    "\u204C",
    "\u204D",
    "\u2219",
    "\u25CB",
    "\u25CF",
    "\u25D8",
    "\u25E6",
    "\u2619",
    "\u2765",
    "\u2767",
    "\u29BE",
    "\u29BF",
    "\u002D",
    "",
    r"\*",
    "\x95",
    "·",
]
BULLETS_PATTERN = "|".join(UNICODE_BULLETS)
UNICODE_BULLETS_RE = re.compile(f"(?:{BULLETS_PATTERN})(?!{BULLETS_PATTERN})")
