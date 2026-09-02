"""npm dependency-manifest parsers.

Covers ``package.json`` and the ``package-lock.json`` / ``pnpm-lock.yaml`` /
``yarn.lock`` locks. The lockfile parsers are deliberately YAML-free (narrow
regexes) so the module needs only the standard library plus the RE2
``regex_safe`` wrapper.
"""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path

from runlayer_cli import regex_safe


def parse_package_json(path: Path) -> list[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    names: list[str] = []
    for section in ("dependencies", "devDependencies", "peerDependencies"):
        names.extend((data.get(section) or {}).keys())
    return names


def parse_package_lock_json(path: Path) -> list[str]:
    data = json.loads(path.read_text(encoding="utf-8"))
    names: set[str] = set()
    # lockfile v2/v3: "packages" maps "node_modules/<name>" -> metadata.
    for key in data.get("packages") or {}:
        if not key:
            continue  # the root package has an empty-string key
        marker = "node_modules/"
        idx = key.rfind(marker)
        names.add(key[idx + len(marker) :] if idx != -1 else key)
    # lockfile v1: top-level "dependencies" maps name -> metadata.
    names.update((data.get("dependencies") or {}).keys())
    return [n for n in names if n]


# RE2 `\s`/`\w`/`\d` are ASCII-only — fine: npm package names and lockfile
# indentation are ASCII by spec.
_PNPM_PKG_KEY = regex_safe.compile(r"^\s+'?/?((?:@[\w.-]+/)?[\w.-]+)@[\dvV^~*]")


def parse_pnpm_lock_yaml(path: Path) -> list[str]:
    """Best-effort ``pnpm-lock.yaml`` parse via the ``packages`` key shape.

    Avoids a YAML dependency: pnpm keys packages as ``/@scope/name@1.2.3`` (v6)
    or ``@scope/name@1.2.3`` (v9), which a narrow regex can recover.
    """
    names: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        match = _PNPM_PKG_KEY.match(line)
        if match:
            names.add(match.group(1))
    return sorted(names)


# `[^@\s"]` narrows with RE2's ASCII-only `\s`, so a name padded with a
# non-breaking space is accepted here where stdlib rejected it — a bogus
# dependency name entering the manifest set, not a missed one.
_YARN_ENTRY_NAME = regex_safe.compile(
    rf'^"?((?:@[^/]+/)?[^@{regex_safe.STDLIB_WS_BODY}"]+)@'
)


def parse_yarn_lock(path: Path) -> list[str]:
    """Best-effort ``yarn.lock`` parse from the entry header lines."""
    names: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line or line[0].isspace() or not line.rstrip().endswith(":"):
            continue
        header = line.rstrip()[:-1]
        for token in header.split(","):
            token = token.strip().strip('"')
            match = _YARN_ENTRY_NAME.match(token)
            if match:
                names.add(match.group(1))
    return sorted(names)


PARSERS: dict[str, Callable[[Path], list[str]]] = {
    "package.json": parse_package_json,
    "package-lock.json": parse_package_lock_json,
    "pnpm-lock.yaml": parse_pnpm_lock_yaml,
    "yarn.lock": parse_yarn_lock,
}
