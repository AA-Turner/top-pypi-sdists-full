import re
from dataclasses import dataclass, field

_DECL = re.compile(r"--(color|radius|text)-([a-z0-9-]+)\s*:", re.IGNORECASE)


@dataclass
class ThemeTokens:
    colors: set[str] = field(default_factory=set)
    radii: set[str] = field(default_factory=set)
    text_sizes: set[str] = field(default_factory=set)


def parse_theme(css: str) -> ThemeTokens:
    t = ThemeTokens()
    bucket = {"color": t.colors, "radius": t.radii, "text": t.text_sizes}
    for kind, name in _DECL.findall(css):
        bucket[kind.lower()].add(name.lower())
    return t
