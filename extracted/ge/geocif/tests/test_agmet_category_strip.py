"""Regression test: geoagmet must strip surrounding quotes from the
``[country] category`` config value.

Root cause (fixed 0.4.853): ``self.category = parser.get(country, "category")``
returned the raw value *including quotes* when a config had
``category = 'EWCM'`` (ConfigParser/INI does not strip quotes). That produced
a plots directory named literally ``'EWCM'``; ``_finalize_plots`` looks for
unquoted ``EWCM``/``AMIS``, found neither, and wrote **no** AMIS/EWCM ZIP even
though 283 plots rendered fine. The fix strips surrounding quotes/whitespace.

Checked structurally against the source so it needs no heavy geocif/geoprepare
import, and it fails on the pre-fix line.
"""
import re
from pathlib import Path

_GEOAGMET = Path(__file__).resolve().parent.parent / "geocif" / "agmet" / "geoagmet.py"


def test_category_assignment_strips_quotes():
    text = _GEOAGMET.read_text(encoding="utf-8")
    # The assignment line: `self.category = self.parser.get(...)...`
    m = re.search(r"self\.category\s*=[^\n]*", text)
    assert m, "could not find the `self.category = ...` assignment in geoagmet.py"
    line = m.group(0)
    assert "parser.get" in line and "category" in line, (
        "unexpected shape for the self.category assignment"
    )
    assert ".strip(" in line, (
        "geoagmet must strip surrounding quotes from the `category` config "
        "value (e.g. `.strip().strip(\"'\\\"\")`) so a quoted entry like "
        "`category = 'EWCM'` cannot create a mismatched dir that breaks the "
        "AMIS/EWCM ZIP finalize"
    )
