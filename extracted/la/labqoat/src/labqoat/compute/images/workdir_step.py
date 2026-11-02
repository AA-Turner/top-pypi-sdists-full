"""Container working-directory selection in an authored image recipe."""

from dataclasses import dataclass


@dataclass(frozen=True)
class WorkdirStep:
    """Retain the absolute directory for subsequent build steps and execution."""

    path: str
