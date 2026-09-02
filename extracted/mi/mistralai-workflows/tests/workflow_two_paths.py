"""Two-paths fan-out workflow for data-flow testing.

fetch_all_packages() returns data consumed by two independent paths:
a loop checking each Python package and a filter on npm packages.
Exercises: transform nodes, data_dep edges, and process group detection.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta

import mistralai.workflows as workflows


@dataclass
class AllPackages:
    python: list[str]
    npm: list[str]


@dataclass
class CheckResult:
    total: int
    pypi_missing: list[str]
    npm_unscoped: list[str]


@workflows.activity(
    name="fetch-all-packages",
    start_to_close_timeout=timedelta(seconds=30),
)
async def fetch_all_packages() -> AllPackages:
    return AllPackages(python=[], npm=[])


@workflows.activity(
    name="check-pypi-one",
    start_to_close_timeout=timedelta(seconds=10),
)
async def check_pypi_one(pkg: str) -> bool:
    return True


@workflows.activity(
    name="filter-npm-scope",
    start_to_close_timeout=timedelta(seconds=10),
)
async def filter_npm_scope(pkgs: list[str]) -> list[str]:
    return []


@workflows.workflow.define(name="two-paths")
class TwoPathsWorkflow:
    @workflows.workflow.entrypoint
    async def run(self, input: str) -> CheckResult:
        all_pkgs = await fetch_all_packages()

        pypi_missing: list[str] = []
        for pkg in all_pkgs.python:
            is_ok = await check_pypi_one(pkg)
            if not is_ok:
                pypi_missing.append(pkg)

        npm_unscoped = await filter_npm_scope(all_pkgs.npm)

        return CheckResult(
            total=len(all_pkgs.python) + len(all_pkgs.npm),
            pypi_missing=pypi_missing,
            npm_unscoped=npm_unscoped,
        )
