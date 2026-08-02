import re
from collections.abc import Iterator

from .catalog import PRIMITIVES
from .findings import Finding

# Couleur flaggée UNIQUEMENT dans un contexte de style (valeur arbitraire Tailwind
# -[...] ou style inline), jamais nue dans un commentaire / JSX : évite les faux
# positifs sur les refs d'issues (#403) et codes HTTP (#409).
_COLOR = r"#[0-9a-fA-F]{3,8}\b|(?:rgb|rgba|hsl|hsla)\s*\([^)]*\)"
_HEX_ARBITRARY = re.compile(r"-\[(?:" + _COLOR + r")\]")
_STYLE_BLOCK = re.compile(r"style=\{\{[^}]*\}\}")
_STYLE_ATTR = re.compile(r'style="[^"]*"')  # style inline HTML (protos)
_COLOR_LITERAL = re.compile(_COLOR)
_ARBITRARY = re.compile(
    r"\b(?:p|m|px|py|mx|my|pt|pb|pl|pr|mt|mb|ml|mr|gap|w|h|rounded|leading|text|font|top|left|right|bottom)-\[[^\]]+\]"
)
_RAW_TAG = re.compile(r"<(" + "|".join(PRIMITIVES) + r")\b")


def _lines(src: str) -> Iterator[tuple[int, str]]:
    return enumerate(src.splitlines(), start=1)


def find_raw_colors(src: str) -> list[Finding]:
    out: list[Finding] = []
    msg = "Couleur brute interdite"
    fix = "Utiliser un token sémantique (ex: bg-brand, text-text-dark)"
    for n, line in _lines(src):
        for m in _HEX_ARBITRARY.finditer(line):
            out.append(Finding("R1", n, m.group(0), msg, fix))
    # blocs de style sur le src entier (JSX style={{...}} multilignes, ou HTML style="...")
    for pat in (_STYLE_BLOCK, _STYLE_ATTR):
        for sm in pat.finditer(src):
            for cm in _COLOR_LITERAL.finditer(sm.group(0)):
                line_no = src[: sm.start() + cm.start()].count("\n") + 1
                out.append(Finding("R1", line_no, cm.group(0), msg, fix))
    return out


def find_arbitrary_values(src: str) -> list[Finding]:
    out: list[Finding] = []
    msg = "Valeur arbitraire hors échelle"
    fix = "Utiliser l'échelle (ex: p-3, rounded-lg)"
    for n, line in _lines(src):
        for m in _ARBITRARY.finditer(line):
            # Une valeur arbitraire qui référence un token (-[var(--...)]) utilise
            # le design system : c'est l'inverse d'un magic number, on ne flague pas.
            if "var(--" in m.group(0):
                continue
            out.append(Finding("R2", n, m.group(0), msg, fix))
    return out


def find_raw_primitives(src: str, suggestions: dict[str, str]) -> list[Finding]:
    out: list[Finding] = []
    for n, line in _lines(src):
        for m in _RAW_TAG.finditer(line):
            tag = m.group(1)
            target = suggestions.get(tag)
            fix = f"Utiliser <{target}>" if target else "Utiliser un composant de components/ui/"
            out.append(Finding("R3", n, m.group(0), f"Primitive <{tag}> au lieu du composant catalogue", fix))
    return out


# R4 : classes de palette Tailwind par défaut (avec shade numérique) qui contournent
# les tokens. Exception : un stem présent dans le @theme du projet (ex: grey-500).
_PALETTE = (
    "slate|gray|zinc|neutral|stone|red|orange|amber|yellow|lime|green|emerald|"
    "teal|cyan|sky|blue|indigo|violet|purple|fuchsia|pink|rose"
)
_PALETTE_CLASS = re.compile(
    r"\b(?:bg|text|border|ring|from|to|via|fill|stroke|divide|outline|decoration)-((?:" + _PALETTE + r")-\d{2,3})\b"
)


def find_palette_classes(src: str, theme_colors: set[str]) -> list[Finding]:
    out: list[Finding] = []
    msg = "Palette Tailwind par défaut au lieu d'un token sémantique"
    fix = "Utiliser un token du design system (ex: text-text-neutral, bg-brand)"
    for n, line in _lines(src):
        for m in _PALETTE_CLASS.finditer(line):
            stem = m.group(1)
            if stem not in theme_colors:
                out.append(Finding("R4", n, m.group(0), msg, fix))
    return out
