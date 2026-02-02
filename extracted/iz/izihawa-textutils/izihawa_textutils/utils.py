import re
import struct
from urllib.parse import unquote

import isbnlib

from .regex import (EMAIL_REGEX, HASHTAG_REGEX, MULTIWHITESPACE_REGEX,
                    NON_ALNUMWHITESPACE_REGEX, TELEGRAM_LINK_REGEX,
                    UNICODE_BULLETS_RE, URL_REGEX)

_link_regex = re.compile(r"\[(.*?)]\(")
_image_regex = re.compile(r"!\[(.*?)]\(")


def add_surrogate(text):
    return "".join(
        # SMP -> Surrogate Pairs (Telegram offsets are calculated with these).
        # See https://en.wikipedia.org/wiki/Plane_(Unicode)#Overview for more.
        (
            "".join(chr(y) for y in struct.unpack("<HH", x.encode("utf-16le")))
            if (0x10000 <= ord(x) <= 0x10FFFF)
            else x
        )
        for x in text
    )


def cast_string_to_single_string(s):
    processed = MULTIWHITESPACE_REGEX.sub(" ", NON_ALNUMWHITESPACE_REGEX.sub(" ", s))
    processed = processed.strip().replace(" ", "-")
    return processed


def despace(text):
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n[ \t]+", "\n", text)
    return text


def despace_full(text):
    return re.sub(r"\s+", " ", text).strip()


def despace_smart(text):
    text = re.sub(r"\n\s*[-•]+\s*", r"\n", text)
    text = re.sub(r"\n{2,}", "\n", text).strip()
    text = re.sub(r"\.?(\s+)?\n", r". ", text)
    text = re.sub(r"\s+", " ", text)
    return text


def escape_format(
    text: str,
    escape_font: bool = True,
    escape_quote: bool = True,
    escape_brackets: bool = True,
):
    if isinstance(text, str):
        if escape_font:
            text = re.sub(r"([_*]){2,}", r"\g<1>", text)
        if escape_quote:
            text = text.replace("`", "'")
        if escape_brackets:
            text = text.replace("[", r"`[`").replace("]", r"`]`")
    elif isinstance(text, bytes):
        if escape_font:
            text = re.sub(rb"([_*]){2,}", rb"\g<1>", text)
        if escape_quote:
            text = text.replace(b"`", b"'")
        if escape_brackets:
            text = text.replace(b"[", rb"`[`").replace(b"]", rb"`]`")
    return text


def find_closing_bracket(s: str, start_from: int) -> int:
    counter = 0
    for i, c in enumerate(s[start_from:]):
        if c == "(":
            counter += 1
        elif c == ")":
            counter -= 1
        if counter == 0:
            return start_from + i
    return len(s) - 1


def fix_markdown(text: str):
    if text.count("**") % 2 == 1:
        position = text.rfind("**")
        text = text[:position] + text[position + 2 :]
    if text.count("__") % 2 == 1:
        position = text.rfind("__")
        text = text[:position] + text[position + 2 :]
    for i in reversed(range(0, len(text))):
        if text[i] == "]":
            break
        if text[i] == "[":
            text = text[:i] + text[i + 1 :]
            break
    return text


def strip_md_link(text: str, keep_text: bool | str = False, regex=_link_regex):
    for link_beginning in reversed(list(re.finditer(regex, text))):
        closing_bracket = find_closing_bracket(text, link_beginning.end() - 1)
        if not keep_text:
            text = text[: link_beginning.start()] + text[closing_bracket + 1 :]
        else:
            if isinstance(keep_text, str):
                replacer = keep_text
            else:
                replacer = text[
                    link_beginning.start() + 1 : link_beginning.end() - 2
                ].strip()
            text = (
                text[: link_beginning.start()] + replacer + text[closing_bracket + 1 :]
            )
    return text


def remove_mm_commands(text: str):
    text = re.sub(
        r"\\+(?:usepackage|nonumber|prod|alpha|beta|left|right|texttt|documentclass|setlength|varvec)(?:[{\[][A-Za-z\d\-.\\]+[}\]])*",
        "",
        text,
    )
    text = re.sub("[ \t]+", " ", text).strip()
    return text


def remove_markdown(
    text: str,
    remove_tables: bool = True,
    remove_math: bool = True,
    escape_brackets: bool = True,
):
    if remove_math:
        text = re.sub(r"(\D)\${1,2}[^$\n]+\${1,2}", r"\g<1>", text)
    text = re.sub(r"^#{1,6}\s*([^\n$]*)", r"\g<1>", text, flags=re.MULTILINE)
    text = re.sub(r"~([^~\n]+)~", r"\g<1>", text)
    text = re.sub(r"\^([^\^\n]+)\^", r"\g<1>", text)
    text = strip_md_link(text, keep_text=False, regex=_image_regex)
    text = strip_md_link(text, keep_text=True)
    text = re.sub(r"(^|[^\\])[_*]{2,}", r"\g<1>", text)
    text = re.sub(r"\\\*+", "\\*", text)
    text = re.sub(r"\\_+", "\\_", text)
    if escape_brackets:
        text = re.sub(r"([[\]])", r"`\g<1>`", text)
    if remove_tables:
        text = re.sub(
            r"^\\begin\{tabular}.*?^\\end\{tabular}",
            "",
            text,
            flags=re.DOTALL | re.MULTILINE,
        )
        text = re.sub(r"(^\|[^\n]+\|(?:\n|$))+", "", text, flags=re.MULTILINE)
    text = remove_mm_commands(text)
    return text


def convert_markdown_to_telegram_markdown(text: str):
    text = convert_table_to_telegram_emoji(text)
    text = convert_math_to_telegram_emoji(text)
    text = re.sub(r"^#{1,6}\s*([^\n$]*)", r"**\g<1>**", text, flags=re.MULTILINE)
    text = re.sub(r"~([^~\n]+)~", r"\g<1>", text)
    text = re.sub(r"\^([^\^\n]+)\^", r"\g<1>", text)
    text = strip_md_link(text, keep_text="🖼️", regex=_image_regex)
    text = strip_md_link(text, keep_text=True)
    text = re.sub(r"\\\*+", r"*", text)
    text = re.sub(r"\\_+", r"_", text)
    text = re.sub(r"\*{2,}", r"**", text)
    text = re.sub(r"_{2,}", r"__", text)
    text = re.sub(r"(^\|[^\n]+\|(?:\n|$))+", "🔢\n", text, flags=re.MULTILINE)
    return text


def convert_table_to_telegram_emoji(text: str):
    text = re.sub(
        r"^\\begin\{tabular}.*?^\\end\{tabular}$",
        "🔢\n",
        text,
        flags=re.DOTALL | re.MULTILINE,
    )
    text = re.sub(r"^\|.*\|$", "🔢\n", text, flags=re.DOTALL | re.MULTILINE)
    return text


def convert_math_to_telegram_emoji(text: str):
    text = re.sub(r"(\D)\${1,2}[^$\n]+\${1,2}", r"\g<1>🧮", text)
    return text


def remove_emails(text: str):
    return re.sub(EMAIL_REGEX, "", text)


def remove_hashtags(text: str):
    return re.sub(HASHTAG_REGEX, "", text)


def remove_hidden_chars(text: str):
    return text.replace("\xad", "")


def remove_url(text: str):
    return re.sub(URL_REGEX, "", text)


def replace_telegram_link(text: str):
    return re.sub(TELEGRAM_LINK_REGEX, r"@\1", text)


def split_at(s, pos):
    if len(s) < pos:
        return s
    pos -= 10
    pos = max(0, pos)
    for p in range(pos, min(pos + 20, len(s) - 1)):
        if s[p] in [" ", "\n", ".", ",", ":", ";", "-"]:
            return s[:p] + "..."
    return s[:pos] + "..."


def unwind_hashtags(text: str):
    return re.sub(HASHTAG_REGEX, r"\2", text)


def clean_empty_references(text: str):
    text = re.sub(r"\((?:[Ff]ig|[Tt]able|[Ss]ection)\.?\s*[^)]*\)", "", text)
    text = re.sub(r"\[[,\s–\d]*]", "", text, flags=re.MULTILINE)
    text = re.sub(r"\s+([.,;])", r"\g<1>", text, flags=re.MULTILINE)
    return text


def process_isbns(isbnlikes):
    isbns = []
    for isbnlike in isbnlikes:
        if not isbnlike:
            continue
        if isbnlike[0].isalpha() and len(isbnlike) == 10 and isbnlike[1:].isalnum():
            isbns.append(isbnlike.upper())
            continue
        isbn = isbnlib.canonical(isbnlike)
        if not isbn:
            continue
        isbns.append(isbn)
        if isbnlib.is_isbn10(isbn):
            if isbn13 := isbnlib.to_isbn13(isbn):
                isbns.append(isbn13)
        elif isbnlib.is_isbn13(isbn):
            if isbn10 := isbnlib.to_isbn10(isbn):
                isbns.append(isbn10)
    return list(sorted(set(isbns)))


def camel_to_snake(name):
    s1 = re.sub("(.)([A-Z][a-z]+)", r"\1_\2", name)
    return re.sub("([a-z0-9])([A-Z])", r"\1_\2", s1).lower()


def mask(text):
    if text is None:
        return None
    text = str(text)
    if len(text) < 4:
        return "*" * len(text)
    return text[:2] + "*" * (len(text) - 4) + text[-2:]


def canonize_doi(doi):
    return (
        unquote(doi.lower())
        .replace("\\n", "\n")
        .replace("\n", "")
        .replace("\\", "")
        .strip("'\"")
        .replace("\x00", "")
        .strip()
    )


def clean_trailing_punctuation(text: str) -> str:
    """Clean all trailing punctuation in text

    Example
    -------
    ITEM 1.     BUSINESS. -> ITEM 1.     BUSINESS
    """
    return text.strip().rstrip(".,:;")


def clean_extra_whitespace(text: str) -> str:
    """Cleans extra whitespace characters that appear between words.

    Example
    -------
    ITEM 1.     BUSINESS -> ITEM 1. BUSINESS
    """
    cleaned_text = re.sub(r"([^|])[\xa0\n]([^|])", r"\g<1> \g<2>", text)
    cleaned_text = re.sub(r"( {2,})", " ", cleaned_text)
    return cleaned_text.strip()


def clean_bullets(text: str) -> str:
    """Cleans unicode bullets from a section of text.

    Example
    -------
    ●  This is an excellent point! -> This is an excellent point!
    """
    search = UNICODE_BULLETS_RE.match(text)
    if search is None:
        return text

    cleaned_text = UNICODE_BULLETS_RE.sub("", text, 1)
    return cleaned_text.strip()
