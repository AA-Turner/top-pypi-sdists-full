"""JVM (maven / gradle) dependency-manifest parsers.

Covers ``pom.xml`` and ``build.gradle`` / ``build.gradle.kts``. Dependencies are
normalized to ``group:artifact`` coordinates.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from xml.etree import ElementTree

from runlayer_cli import regex_safe
from runlayer_cli.scan.agents.manifests._common import local_tag


def parse_pom(path: Path) -> list[str]:
    root = ElementTree.parse(path).getroot()
    names: list[str] = []
    for el in root.iter():
        if local_tag(el.tag) != "dependency":
            continue
        group = artifact = None
        for child in el:
            local = local_tag(child.tag)
            if local == "groupId":
                group = (child.text or "").strip()
            elif local == "artifactId":
                artifact = (child.text or "").strip()
        if group and artifact:
            names.append(f"{group}:{artifact}")
    return names


# Gradle coordinate inside a quoted string: ``group:artifact`` optionally
# followed by ``:version``. Captures the discriminating ``group:artifact`` pair.
_GRADLE_COORD = regex_safe.compile(
    r"""['"]([A-Za-z0-9_.-]+:[A-Za-z0-9_.-]+)(?::[^'"]*)?['"]"""
)


def parse_build_gradle(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    return _GRADLE_COORD.findall(text)


PARSERS: dict[str, Callable[[Path], list[str]]] = {
    "pom.xml": parse_pom,
    "build.gradle": parse_build_gradle,
    "build.gradle.kts": parse_build_gradle,
}
