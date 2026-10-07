"""Bump the version in pyproject.toml: 5.0.0rc1 -> 5.0.0rc2, 5.0.0 -> 5.0.1.

Used by the Generate SDK workflow when a spec change alters the generated code.
"""

import re
from pathlib import Path

PYPROJECT = Path(__file__).resolve().parent.parent / "pyproject.toml"


def bump(version: str) -> str:
    pre = re.fullmatch(r"(.+?)(a|b|rc)(\d+)", version)
    if pre:
        return f"{pre.group(1)}{pre.group(2)}{int(pre.group(3)) + 1}"
    major, minor, patch = (int(part) for part in version.split("."))
    return f"{major}.{minor}.{patch + 1}"


def main() -> None:
    text = PYPROJECT.read_text()
    current = re.search(r'^version = "(.+)"$', text, re.M)
    assert current, "no version in pyproject.toml"
    new = bump(current.group(1))
    PYPROJECT.write_text(text.replace(current.group(0), f'version = "{new}"', 1))
    print(new)


if __name__ == "__main__":
    main()
