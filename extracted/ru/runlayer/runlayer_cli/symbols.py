import sys


def _supports_unicode() -> bool:
    try:
        "✓".encode(sys.stdout.encoding or "ascii")
        return True
    except (UnicodeEncodeError, LookupError, AttributeError):
        return False


if _supports_unicode():
    OK = "✓"
    FAIL = "✗"
    WARN = "⚠"
else:
    OK = "[ok]"
    FAIL = "[error]"
    WARN = "[warn]"
