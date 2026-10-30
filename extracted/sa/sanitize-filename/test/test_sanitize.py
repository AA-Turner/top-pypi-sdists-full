"""Tests for the sanitize function."""
from sanitize_filename import sanitize


def test_invalid_chars():
    """Make sure invalid characters are removed in filenames."""
    assert sanitize("A/B/C") == "ABC"
    assert sanitize("A*C.d") == "AC.d"
    assert sanitize("A?C.d") == "AC.d"


def test_invalid_suffix():
    """Dots are not allowed at the end."""
    assert sanitize("def.") == "def"
    assert sanitize("def.ghi") == "def.ghi"
    assert sanitize("X" * 1000 + ".").endswith("X")


def test_reserved_words():
    """Make sure reserved Windows words are prefixed."""
    assert sanitize("NUL") == "__NUL"
    assert sanitize("..") == "__"


def test_long_names():
    """Make sure long names are truncated."""
    assert len(sanitize("X" * 300)) == 255
    assert len(sanitize(".".join(["X" * 100, "X" * 100, "X" * 100]))) == 255
    assert len(sanitize(".".join(["X" * 300, "X" * 300, "X" * 300]))) == 255
    assert len(sanitize("." * 300 + ".txt")) == 255


def test_unicode_normalization():
    """Names should be NFKD normalized."""
    assert sanitize("\u045e") == chr(1091)+chr(774)


def test_extensions():
    """Filename extensions should be preserved when possible."""
    really_long_name = "X" * 1000 + ".pdf"
    assert sanitize(really_long_name).endswith(".pdf")
    assert sanitize("X" * 1000).endswith("X")
    assert sanitize("X" * 100 + "." + "X" * 100 + ".pdf").endswith(".pdf")
    assert sanitize("X" * 100 + "." + "X" * 400).endswith("X")
    assert sanitize("X" * 100 + "." + "X" * 400 + ".pdf").endswith(".pdf")


def test_unicode_lookalike_separators():
    """Characters that NFKD-normalize to blacklisted ones must not survive.

    E.g. the fullwidth solidus (U+FF0F) normalizes to "/", and could
    otherwise be used for path traversal.
    """
    payload = "\uFF0F..\uFF0F..\uFF0F..\uFF0Fetc\uFF0Fpasswd"
    result = sanitize(payload)
    assert "/" not in result
    assert not result.startswith("/")
    assert sanitize("A\uFF0FB") == "AB"  # fullwidth solidus
    assert sanitize("A\uFF3CB") == "AB"  # fullwidth reverse solidus
    assert sanitize("A\uFE68B") == "AB"  # small reverse solidus
    assert sanitize("A\uFF1AB") == "AB"  # fullwidth colon


def test_reserved_words_variants():
    """Reserved Windows words are case insensitive and ignore extensions."""
    assert sanitize("con") == "__con"
    assert sanitize("Com1") == "__Com1"
    assert sanitize("CON.txt") == "__CON.txt"
    assert sanitize("nul.tar.gz") == "__nul.tar.gz"
    assert sanitize("CONIN$") == "__CONIN$"
    assert sanitize("console.txt") == "console.txt"


def test_no_trailing_dot_behind_whitespace():
    """Unicode whitespace must not hide a trailing dot."""
    assert sanitize("a.\u2028") == "a"
    assert sanitize("a.\x85") == "a"
    assert sanitize("a. .\u3000") == "a"


def test_control_characters():
    """C0 and C1 control characters are removed."""
    assert sanitize("a\x7fb") == "ab"
    assert sanitize("a\x9bb") == "ab"
    assert sanitize("a\x1bb") == "ab"


def test_lone_surrogates():
    """Lone surrogates can not be encoded, and are removed."""
    assert sanitize("a\ud800b") == "ab"
    assert sanitize("\ud800") == "__"
