"""Go dependency-manifest parser: ``go.mod`` require directives."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from runlayer_cli import regex_safe

_GO_REQUIRE_LINE = regex_safe.compile(r"^\s*([^\s()]+)\s+v\S+")


def parse_go_mod(path: Path) -> list[str]:
    names: list[str] = []
    in_block = False
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if not in_block and stripped.startswith("require") and "(" in stripped:
            in_block = True
            continue
        if in_block:
            if stripped.startswith(")"):
                in_block = False
                continue
            match = _GO_REQUIRE_LINE.match(stripped)
            if match:
                names.append(match.group(1))
            continue
        if stripped.startswith("require "):
            match = _GO_REQUIRE_LINE.match(stripped[len("require ") :])
            if match:
                names.append(match.group(1))
    return names


PARSERS: dict[str, Callable[[Path], list[str]]] = {
    "go.mod": parse_go_mod,
}
