"""Image: environment specification for a Capsule app's runtime.

image = Image(python_packages=["openai", "numpy"])

image = (
    Image()
    .add_python_packages(["openai", "numpy"])
    .add_commands(["apt-get install -y ffmpeg"])
)

image = Image(python_packages="requirements.txt")
"""

from __future__ import annotations

from pathlib import Path
from typing import Sequence, Union


class Image:
    """Environment specification for an app's runtime.

    Translates to install commands executed inside the instance on first provision.
    """

    def __init__(
        self,
        *,
        python_packages: Union[list[str], str, None] = None,
        apt_packages: list[str] | None = None,
        commands: list[str] | None = None,
    ) -> None:
        if isinstance(python_packages, str):
            python_packages = self._load_requirements_file(python_packages)

        self.python_packages: list[str] = list(python_packages or [])
        self.apt_packages: list[str] = list(apt_packages or [])
        self.commands: list[str] = list(commands or [])

    def add_python_packages(self, packages: Union[Sequence[str], str]) -> "Image":
        """Add Python packages. Accepts a list or a path to requirements.txt."""
        if isinstance(packages, str):
            packages = self._load_requirements_file(packages)
        self.python_packages.extend(packages)
        return self

    def add_apt_packages(self, packages: Sequence[str]) -> "Image":
        """Add system packages to install via apt-get."""
        self.apt_packages.extend(packages)
        return self

    def add_commands(self, commands: Sequence[str]) -> "Image":
        """Add shell commands to run during setup."""
        self.commands.extend(commands)
        return self

    def to_dict(self) -> dict:
        return {
            "python_packages": list(self.python_packages),
            "apt_packages": list(self.apt_packages),
            "commands": list(self.commands),
        }

    @staticmethod
    def _load_requirements_file(path: str) -> list[str]:
        """Parse a requirements.txt into a list of package specs."""
        p = Path(path)
        if not p.is_file():
            raise FileNotFoundError(f"Requirements file not found: {path}")

        packages = []
        for line in p.read_text().splitlines():
            line = line.strip()
            if line and not line.startswith("#") and not line.startswith("-"):
                packages.append(line)
        return packages

    def __repr__(self) -> str:
        parts = []
        if self.python_packages:
            parts.append(f"pip=[{', '.join(self.python_packages)}]")
        if self.apt_packages:
            parts.append(f"apt=[{', '.join(self.apt_packages)}]")
        if self.commands:
            parts.append(f"cmds={len(self.commands)}")
        return f"Image({', '.join(parts)})"
