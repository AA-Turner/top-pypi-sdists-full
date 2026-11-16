"""Tests for the sanitize function."""
import pytest
from sanitize_filename import sanitize


def test_invalid_chars():
    """Make sure invalid characters are removed in filenames."""
    assert sanitize("A/B/C") == "ABC"
    assert sanitize("A*C.d") == "AC.d"
    assert sanitize("A?C.d") == "AC.d"
    assert sanitize("A\\B\\C") == "ABC"
    assert sanitize("A\"B\"C.d") == "ABC.d"
    assert sanitize("A<B<C.d") == "ABC.d"
    assert sanitize("A>B>C.d") == "ABC.d"
    assert sanitize("A|B|C.d") == "ABC.d"
    assert sanitize("\uff1f") == "__"

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
    """Names should be NFC normalized."""
    assert sanitize("\u045e") == "\u045e"
    # Decomposed input is composed
    assert sanitize("\u0443\u0306") == "\u045e"
    assert sanitize("Ga\u0308vle.csv") == "G\u00e4vle.csv"


def test_compatibility_characters_preserved():
    """Compatibility characters that are harmless should be kept as is."""
    # macOS screenshot names (US locale) use a narrow no-break space
    name = "Screenshot 2026-11-10 at 9.41.12\u202fAM.png"
    assert sanitize(name) == name
    assert sanitize("a\u00a0b.txt") == "a\u00a0b.txt"  # no-break space
    assert sanitize("\ufb01le.txt") == "\ufb01le.txt"  # fi ligature
    assert sanitize("\uff21\uff22\uff23") == "\uff21\uff22\uff23"  # fullwidth
    assert sanitize("x\u00b2.txt") == "x\u00b2.txt"  # superscript two


def test_trailing_no_break_spaces():
    """No-break spaces are still stripped from the ends."""
    assert sanitize("a\u202f") == "a"
    assert sanitize("a.\u00a0") == "a"
    assert sanitize("\u202fa") == "a"


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


def test_reserved_words_lookalikes():
    """Lookalikes of reserved words are reserved too (e.g. COM¹ on Windows)."""
    assert sanitize("COM\u00b9") == "__COM\u00b9"
    assert sanitize("lpt\u00b2.txt") == "__lpt\u00b2.txt"
    assert sanitize("\uff23\uff2f\uff2e") == "__\uff23\uff2f\uff2e"
    assert sanitize("\uff2e\uff35\uff2c.txt") == "__\uff2e\uff35\uff2c.txt"
    assert sanitize("COM\u00b9\u00b9") == "COM\u00b9\u00b9"


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


def test_length_in_bytes():
    """Length is limited in UTF-8 bytes, not characters."""
    result = sanitize("G\u00e4vle" * 100 + ".csv")
    assert len(result.encode("utf-8")) <= 255
    assert result.endswith(".csv")
    result = sanitize("\U0001f600" * 300)
    assert len(result.encode("utf-8")) <= 255
    assert result == "\U0001f600" * 63
    assert len(sanitize("x" * 300, max_bytes=100)) == 100
    assert sanitize("x" * 50, max_bytes=100) == "x" * 50


def test_truncation_keeps_clusters():
    """Truncation must not split characters from their combining marks etc."""
    assert sanitize("a" * 253 + "q\u0301z") == "a" * 253
    assert sanitize("a" * 250 + "\U0001f44d\U0001f3fd" * 3) == "a" * 250
    family = "\U0001f468\u200d\U0001f469\u200d\U0001f467"
    assert sanitize("a" * 251 + family) == "a" * 251
    assert sanitize("a" * 230 + family) == "a" * 230 + family


def test_truncation_extensions():
    """Only short, plausible suffixes are kept as extensions."""
    assert sanitize("X" * 300 + ".tar.gz").endswith("X.gz")
    # A long "extension" is not an extension, and the start is kept
    result = sanitize("Report. " + "x" * 300)
    assert result.startswith("Report. x")
    assert len(result) == 255
    result = sanitize("a." + "X" * 300)
    assert result.startswith("a.X")
    assert len(result) == 255
    # Dots before the extension are fine
    assert sanitize("." * 300 + ".txt") == "." * 251 + ".txt"


def test_truncation_no_trailing_dot_or_space():
    """Truncation must not leave a trailing dot or space."""
    assert sanitize("x" * 254 + " y") == "x" * 254
    assert sanitize("x" * 254 + ". z z") == "x" * 254


def test_truncation_reserved_words():
    """Truncation must not produce a reserved word."""
    result = sanitize("CON" + " " * 300 + "x.txt")
    assert result.startswith("__CON")
    assert result.endswith(".txt")
    assert len(result) == 255
    result = sanitize("CON." + "x" * 300)
    assert result.startswith("__CON.")
    assert len(result) == 255


def test_tiny_max_bytes():
    """The extension must not crowd out the whole name."""
    assert sanitize("x" * 200 + ".txt", max_bytes=2) == "xx"
    assert sanitize("x" * 200 + ".txt", max_bytes=4) == "xxxx"
    assert sanitize("x" * 200 + ".txt", max_bytes=5) == "x.txt"
    assert sanitize("..", max_bytes=1) == "_"
    with pytest.raises(ValueError):
        sanitize("abc", max_bytes=0)


def test_dot_lookalikes():
    """Lookalikes of dots (e.g. fullwidth full stop) count as dots."""
    assert sanitize("．．") == "__"  # fullwidth full stops
    assert sanitize("‥") == "__"  # two dot leader
    assert sanitize("․․") == "__"  # one dot leaders
    assert sanitize("a．") == "a"
    assert sanitize("a․ 　") == "a"
    assert sanitize("x" * 300 + "．").endswith("x")
    # Dot lookalikes are fine elsewhere
    assert sanitize("a．b") == "a．b"
    # Middle dots are not dot lookalikes
    assert sanitize("··") == "··"


def test_nfc_after_removals():
    """Output is NFC even if a removed character separated a combining mark."""
    assert sanitize("e/́") == "é"
    assert sanitize("e\x7f́") == "é"
    for name in ["e/́", "a\\̈x", "Y*́.txt"]:
        result = sanitize(name)
        assert sanitize(result) == result


def test_bidi_controls():
    """Bidi controls are removed, so that names display as they are."""
    assert sanitize("invoice‮txt.exe") == "invoicetxt.exe"
    assert sanitize("a⁦b⁩") == "ab"
    assert sanitize("שלום‏.txt") == \
        "שלום.txt"
    # Bidi controls must not hide reserved words
    assert sanitize("CON‎") == "__CON"
    assert sanitize("‪NUL.txt") == "__NUL.txt"


def test_invisible_names():
    """Names with nothing visible are replaced."""
    assert sanitize("​") == "__"  # zero width space
    assert sanitize("﻿") == "__"  # BOM
    assert sanitize("‍‌") == "__"
    assert sanitize("​ ​") == "__"
    assert sanitize("́") == "__"
    assert sanitize("​", max_bytes=1) == "_"
    # Visible characters are kept, along with any invisible ones
    assert sanitize("​.txt") == "​.txt"
    assert sanitize("") == ""  # private use
    # ZWJ and ZWNJ are needed for emoji and some scripts
    family = "\U0001f468‍\U0001f469"
    assert sanitize(family) == family
    persian = "می‌خواهم"
    assert sanitize(persian) == persian
