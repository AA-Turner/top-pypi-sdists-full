"""A permissive filename sanitizer."""
import unicodedata
import re


# 255 bytes is the limit on most Linux file systems. Every UTF-16 code unit
# is at least one UTF-8 byte, so this also respects the 255 UTF-16 unit limit
# of NTFS, APFS and HFS+
MAX_BYTES = 255
# Longer suffixes are not treated as file extensions when truncating
MAX_EXT_LENGTH = 16
ZWJ = "‍"
BLACKLIST = set("\\/:*?\"<>|")  # NUL is removed with other control chars
RESERVED = {"CON", "PRN", "AUX", "NUL", "CONIN$", "CONOUT$"} | {
    f"{p}{i}" for p in ("COM", "LPT") for i in range(10)
}  # Reserved words on Windows
# Unicode Bidi_Control characters. These can be used to make a name display
# differently from what it is, e.g. "invoice\u202etxt.exe" as invoiceexe.txt
BIDI_CONTROLS = set(
    "\u061c\u200e\u200f\u202a\u202b\u202c\u202d\u202e"
    "\u2066\u2067\u2068\u2069"
)

INVISIBLE = {"Cf", "Zs", "Zl", "Zp", "Mn", "Mc", "Me"}  # Unicode categories


def _cut(text, max_bytes):
    """Cut text to at most max_bytes UTF-8 bytes, not splitting characters."""
    if max_bytes <= 0:
        return ""
    i = len(text.encode("utf-8")[:max_bytes].decode("utf-8", "ignore"))
    # Back off to the start of the character sequence we cut through. This
    # approximates grapheme clusters (UAX #29): combining marks, zero width
    # joiners, variation selectors, emoji modifiers.
    while 0 < i < len(text) and (
        unicodedata.category(text[i]) in ("Mn", "Me", "Mc")
        or "︀" <= text[i] <= "️"
        or "\U0001f3fb" <= text[i] <= "\U0001f3ff"
        or ZWJ in text[i - 1:i + 1]
    ):
        i -= 1
    return text[:i]


def _truncate(filename, max_bytes):
    """Fit filename in max_bytes, and make sure it has a valid ending.

    Keeps the extension when sensible. Never returns an empty string.
    """
    if len(filename.encode("utf-8")) > max_bytes:
        stem, dot, ext = filename.rpartition(".")
        stem_cut = ""
        if dot and stem and re.fullmatch(r"\w{1,%d}" % MAX_EXT_LENGTH, ext):
            stem_cut = _cut(stem, max_bytes - len(ext.encode("utf-8")) - 1)
        if stem_cut:
            filename = stem_cut + "." + ext
        else:
            # No extension, or no room left for the name: Cut the whole thing
            filename = _cut(filename, max_bytes)
    # Windows does not allow names to end with a dot or space. Strip any
    # whitespace too, so that it can not hide a trailing dot. Include
    # lookalikes, as Windows' "best fit" conversion may turn e.g. a fullwidth
    # full stop into a dot.
    i = len(filename)
    while i > 0 and all(
        x == "." or x.isspace()
        for x in unicodedata.normalize("NFKD", filename[i - 1])
    ):
        i -= 1
    filename = filename[:i]
    # Empty names, or names with nothing visible (only format characters,
    # separators or combining marks, e.g. a zero width space) are replaced
    if all(unicodedata.category(c) in INVISIBLE for c in filename):
        return "__"[:max_bytes]
    return filename


def sanitize(filename, max_bytes=MAX_BYTES):
    """Return a fairly safe version of the filename.

    We don't limit ourselves to ascii,
    but we do want to get rid of anything potentially harmful,
    and make sure we do not exceed Windows filename length limits.
    Hence a less safe blacklist, rather than a whitelist.

    The result is at most max_bytes UTF-8 bytes long (default 255, which
    is safe on all common file systems).
    """
    if max_bytes < 1:
        raise ValueError("max_bytes must be at least 1")

    # Remove control characters (C0 and C1), lone surrogates, bidi controls,
    # and blacklisted characters, including lookalikes (e.g. fullwidth solidus)
    filename = "".join(
        c for c in filename
        if unicodedata.category(c) not in ("Cc", "Cs")
        and c not in BIDI_CONTROLS
        and not BLACKLIST.intersection(unicodedata.normalize("NFKD", c))
    )
    # NFC (not NFKD) to keep e.g. nnbsp. Do this after removing characters,
    # as a removal may leave a combining mark next to a base character
    filename = unicodedata.normalize("NFC", filename).strip()
    filename = _truncate(filename, max_bytes)

    # Reserved words are case insensitive, and apply regardless of extension
    # Include lookalike characters, as COM¹ is treated as COM1 on Windows
    base = unicodedata.normalize("NFKD", filename).split(".")[0]
    if base.rstrip().upper() in RESERVED:
        # The prefix may push us over the limit
        filename = _truncate("__" + filename, max_bytes)
    return filename
