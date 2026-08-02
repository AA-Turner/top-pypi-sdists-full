"""
test_visual_guards.py — permanent guards against the two recurring visual bugs:

  1. DARK MENUS: every text color (prompt_toolkit Style.from_dict values + chat
     CSS `color:` declarations) must clear a luminance floor. No more shipping a
     menu painted in near-invisible #383828 / #666666 / #706c54.

  2. NARROW OVERFLOW: the print()-based renders (welcome + integrations
     directory) must fit a split-pane width with no line spilling past the edge.

These two classes cost ~4 round-trips with the founder ("why so dark", "ai
slop"). They can't ship again.

Run: python3 -m unittest tests.test_visual_guards
"""
import os
import re
import sys
import unittest
from unittest import mock

_HERE = os.path.dirname(os.path.abspath(__file__))
_SRC = os.path.dirname(_HERE)
sys.path.insert(0, _SRC)

# Perceived-luminance floor for TEXT. Readable tones sit ~149-220; the dark bugs
# were ~52-108. 120 cleanly separates them.
LUM_FLOOR = 120

# Decorative tones that are intentionally dim and are NOT body/menu text:
#   - hairline / frame rules (subtle dividers)
#   - the dark ink printed ON the gold NX chip (correct contrast on a gold bg)
# Listed so the lint doesn't false-positive on them.
ALLOWED_DARK_HEX = {
    "#0a0a0a", "#050505", "#1a1600",  # backgrounds
}


def _lum_hex(h):
    h = h.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return 0.299 * r + 0.587 * g + 0.114 * b


def _lum_rgb(r, g, b):
    return 0.299 * r + 0.587 * g + 0.114 * b


def _py_files():
    for name in os.listdir(_SRC):
        if name.endswith(".py") and not name.startswith("test_"):
            yield os.path.join(_SRC, name)


class MenuPaletteLuminanceTests(unittest.TestCase):
    def test_menu_and_css_text_colors_meet_luminance_floor(self):
        """Every foreground text color in a Style.from_dict value or a CSS
        `color:` declaration must be readable (luminance >= floor)."""
        violations = []
        # Style.from_dict entries:  "key": "...#hex..."   and CSS:  color: #hex
        style_re = re.compile(r'"[\w-]+"\s*:\s*"([^"]*#[0-9a-fA-F]{6}[^"]*)"')
        css_re = re.compile(r'(?<!-)\bcolor\s*:\s*(#[0-9a-fA-F]{6})')
        hex_re = re.compile(r'(bg:)?(#[0-9a-fA-F]{6})')
        for path in _py_files():
            with open(path, encoding="utf-8") as f:
                for n, line in enumerate(f, 1):
                    candidates = []
                    for val in style_re.findall(line):
                        # a style value may be "bg:#xxx #yyy bold" — take the fg
                        for m in hex_re.finditer(val):
                            if not m.group(1):  # not a bg: token
                                candidates.append(m.group(2))
                    candidates += css_re.findall(line)
                    for hx in candidates:
                        if hx.lower() in ALLOWED_DARK_HEX:
                            continue
                        if _lum_hex(hx) < LUM_FLOOR:
                            violations.append(
                                f"{os.path.basename(path)}:{n} {hx} "
                                f"(lum {_lum_hex(hx):.0f} < {LUM_FLOOR})")
        self.assertEqual(violations, [],
                         "dark TEXT color(s) shipped:\n  " + "\n  ".join(violations))

    def test_known_dark_ansi_text_tones_absent(self):
        """The exact dark FOREGROUND ANSI tones that were confirmed bugs must not
        reappear in shipped source (the murky 'Working' line, dark menu dims)."""
        bad = ["120;98;44", "68;65;48", "38;36;22", "100;78;28",
               "80;80;80", "50;48;32", "120;116;96"]
        offenders = []
        for path in _py_files():
            with open(path, encoding="utf-8") as f:
                src = f.read()
            for tone in bad:
                if f"38;2;{tone}m" in src:
                    offenders.append(f"{os.path.basename(path)}: 38;2;{tone}")
        self.assertEqual(offenders, [],
                         "known-dark ANSI text tone(s) resurfaced:\n  " + "\n  ".join(offenders))


class NarrowRenderTests(unittest.TestCase):
    # 44 cols is a sane minimum split-pane; below that is not a realistic target.
    NARROW = (44, 48, 56, 64, 72)

    def test_welcome_fits_every_narrow_width(self):
        import nx_terminal
        for w in self.NARROW:
            buf = __import__("io").StringIO()
            with mock.patch.object(nx_terminal, "_w", return_value=w):
                import contextlib
                with contextlib.redirect_stdout(buf):
                    nx_terminal.print_welcome("v@gmail.com", "0.5.6", "strategy")
            plain = re.sub(r"\x1b\[[0-9;]*m", "", buf.getvalue())
            for line in plain.split("\n"):
                self.assertLessEqual(len(line), w,
                    f"welcome line overflows {w} cols: {line!r}")

    def test_directory_fits_every_narrow_width(self):
        import nx_integrations_directory as D
        for w in self.NARROW:
            plain = re.sub(r"\x1b\[[0-9;]*m", "", D.render_directory("sales", width=w))
            for line in plain.split("\n"):
                self.assertLessEqual(len(line), w,
                    f"directory line overflows {w} cols: {line!r}")


if __name__ == "__main__":
    unittest.main()
