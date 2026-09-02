""".NET (nuget) dependency-manifest parser: ``*.csproj`` PackageReference items."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from xml.etree import ElementTree

from runlayer_cli.scan.agents.manifests._common import local_tag


def parse_csproj(path: Path) -> list[str]:
    root = ElementTree.parse(path).getroot()
    names: list[str] = []
    for el in root.iter():
        if local_tag(el.tag) != "PackageReference":
            continue
        include = el.attrib.get("Include") or el.attrib.get("Update")
        if include:
            names.append(include.strip())
    return names


PARSERS: dict[str, Callable[[Path], list[str]]] = {
    ".csproj": parse_csproj,
}
