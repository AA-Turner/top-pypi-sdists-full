from __future__ import annotations

from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError, requires, version

from packaging.requirements import Requirement

SERVER_DISTRIBUTION = "langgraph-api"
SDK_DISTRIBUTION = "mcp"


@dataclass(frozen=True, slots=True)
class InstalledSdk:
    required: Requirement
    installed: str | None

    @classmethod
    def find(cls) -> InstalledSdk:
        return cls(_declared_requirement(), _installed_version())

    @property
    def is_supported(self) -> bool:
        return self.installed is not None and self.required.specifier.contains(
            self.installed, prereleases=True
        )


def _declared_requirement() -> Requirement:
    return next(
        requirement
        for requirement in map(Requirement, requires(SERVER_DISTRIBUTION) or ())
        if requirement.name == SDK_DISTRIBUTION
    )


def _installed_version() -> str | None:
    try:
        return version(SDK_DISTRIBUTION)
    except PackageNotFoundError:
        return None
