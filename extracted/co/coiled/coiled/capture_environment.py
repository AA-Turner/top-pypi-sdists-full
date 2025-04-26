import asyncio
import contextlib
import logging
import platform
import sys
import typing
from logging import getLogger
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, cast

from rich.live import Live
from rich.panel import Panel
from rich.progress import BarColumn, Progress, TextColumn, TimeElapsedColumn
from typing_extensions import Literal

from coiled.context import track_context
from coiled.scan import scan_prefix
from coiled.software_utils import (
    check_pip_happy,
    create_wheels_for_local_python,
    create_wheels_for_packages,
    partition_ignored_packages,
    partition_local_packages,
    partition_local_python_code_packages,
)
from coiled.types import (
    KNOWN_PACKAGE_LEVELS,
    ArchitectureTypesEnum,
    PackageInfo,
    PackageLevel,
    PackageLevelEnum,
    ResolvedPackageInfo,
    parse_conda_channel,
)
from coiled.v2.core import CloudV2
from coiled.v2.widgets.rich import CONSOLE_WIDTH, print_rich_package_table
from coiled.v2.widgets.util import simple_progress, use_rich_widget

PYTHON_VERSION = platform.python_version_tuple()
ANY_AVAILABLE = "ANY-AVAILABLE"


logger = getLogger("coiled.package_sync")


async def default_python() -> PackageInfo:
    python_version = platform.python_version()
    return {
        "name": "python",
        "path": None,
        "source": "conda",
        "channel_url": ANY_AVAILABLE,
        "channel": ANY_AVAILABLE,
        "subdir": "linux-64",
        "conda_name": "python",
        "version": python_version,
        "wheel_target": None,
    }


@track_context
async def approximate_packages(
    cloud: CloudV2,
    packages: List[PackageInfo],
    priorities: Dict[Tuple[str, Literal["conda", "pip"]], PackageLevelEnum],
    progress: Optional[Progress] = None,
    strict: bool = False,
    architecture: ArchitectureTypesEnum = ArchitectureTypesEnum.X86_64,
    pip_check_errors: Optional[Dict[str, List[str]]] = None,
    gpu_enabled: bool = False,
) -> typing.List[ResolvedPackageInfo]:
    user_conda_installed_python = next((p for p in packages if p["name"] == "python"), None)
    user_conda_installed_pip = next(
        (i for i, p in enumerate(packages) if p["name"] == "pip" and p["source"] == "conda"),
        None,
    )
    if not user_conda_installed_pip:
        # This means pip was installed by pip, or the system
        # package manager
        # Insert a conda version of pip to be installed first, it will
        # then be used to install the users version of pip
        pip = next(
            (p for p in packages if p["name"] == "pip" and p["source"] == "pip"),
            None,
        )
        if not pip:
            # insert a modern version and hope it does not introduce conflicts
            packages.append({
                "name": "pip",
                "path": None,
                "source": "conda",
                "channel_url": "https://conda.anaconda.org/conda-forge/",
                "channel": "conda-forge",
                "subdir": "noarch",
                "conda_name": "pip",
                "version": "22.3.1",
                "wheel_target": None,
            })
        else:
            # insert the users pip version and hope it exists on conda-forge
            packages.append({
                "name": "pip",
                "path": None,
                "source": "conda",
                "channel_url": "https://conda.anaconda.org/conda-forge/",
                "channel": "conda-forge",
                "subdir": "noarch",
                "conda_name": "pip",
                "version": pip["version"],
                "wheel_target": None,
            })
    coiled_selected_python = None
    if not user_conda_installed_python:
        # insert a special python package
        # that the backend will pick a channel for
        coiled_selected_python = await default_python()
        packages.append(coiled_selected_python)
    packages, ignored_packages = partition_ignored_packages(packages, priorities=priorities)
    packages, local_python_code = partition_local_python_code_packages(packages)
    packages, local_python_wheel_packages = partition_local_packages(packages)
    with simple_progress("Validating environment", progress=progress):
        results = await cloud._approximate_packages(
            packages=[
                {
                    "name": pkg["name"],
                    "priority_override": (
                        PackageLevelEnum.CRITICAL
                        if (
                            pkg["version"]
                            and (
                                strict
                                or (
                                    pkg["wheel_target"]
                                    # Ignore should override wheel_target (see #2640)
                                    and not priorities.get((pkg["name"], pkg["source"])) == PackageLevelEnum.IGNORE
                                )
                            )
                        )
                        else priorities.get((
                            (cast(str, pkg["conda_name"]) if pkg["source"] == "conda" else pkg["name"]),
                            pkg["source"],
                        ))
                    ),
                    "python_major_version": PYTHON_VERSION[0],
                    "python_minor_version": PYTHON_VERSION[1],
                    "python_patch_version": PYTHON_VERSION[2],
                    "source": pkg["source"],
                    "channel_url": pkg["channel_url"],
                    "channel": pkg["channel"],
                    "subdir": pkg["subdir"],
                    "conda_name": pkg["conda_name"],
                    "version": pkg["version"],
                    "wheel_target": pkg["wheel_target"],
                }
                # Send all packages to backend to help with debugging
                for pkg in packages + local_python_code + local_python_wheel_packages + ignored_packages
            ],
            architecture=architecture,
            pip_check_errors=pip_check_errors,
            gpu_enabled=gpu_enabled,
        )
    finalized_packages: typing.List[ResolvedPackageInfo] = []
    finalized_packages.extend(await create_wheels_for_local_python(local_python_code, progress=progress))
    finalized_packages.extend(await create_wheels_for_packages(local_python_wheel_packages, progress=progress))
    for package_result in results:
        # Use channel URL for conda packages, but clean it up a little first
        if package_result["conda_name"] and package_result["channel_url"]:
            subdir = f"linux-{architecture.conda_suffix}"
            channel = parse_conda_channel(package_result["name"], package_result["channel_url"], subdir)[1]
        else:
            channel = package_result["channel_url"]
        # Remove channel_url note that endpoint returns for backward compatibility
        if (
            channel
            and package_result["note"]
            and (channel == package_result["note"] or package_result["note"].endswith(f",{channel}"))
        ):
            package_result["note"] = None

        finalized_packages.append({
            "name": package_result["name"],
            "source": "conda" if package_result["conda_name"] else "pip",
            "channel": channel,
            "conda_name": package_result["conda_name"],
            "client_version": package_result["client_version"],
            "specifier": package_result["specifier"] or "",
            "include": package_result["include"],
            "note": package_result["note"],
            "error": package_result["error"],
            "sdist": None,
            "md5": None,
        })

    return finalized_packages


@track_context
async def create_environment_approximation(
    cloud: CloudV2,
    priorities: Dict[Tuple[str, Literal["conda", "pip"]], PackageLevelEnum],
    only: Optional[Set[str]] = None,
    conda_extras: Optional[List[str]] = None,
    strict: bool = False,
    progress: Optional[Progress] = None,
    architecture: ArchitectureTypesEnum = ArchitectureTypesEnum.X86_64,
    gpu_enabled: bool = False,
) -> typing.List[ResolvedPackageInfo]:
    packages = await scan_prefix(progress=progress)
    pip_check_errors = await check_pip_happy(progress)
    if only:
        packages = [pkg for pkg in packages if pkg["name"] in only]
    extra_packages: List[PackageInfo] = [
        {
            "name": conda_extra,
            "path": None,
            "source": "conda",
            "channel_url": ANY_AVAILABLE,
            "channel": ANY_AVAILABLE,
            "subdir": f"linux-{architecture.conda_suffix}",
            "conda_name": conda_extra,
            "version": "",
            "wheel_target": None,
        }
        for conda_extra in (conda_extras or [])
    ]
    result = await approximate_packages(
        cloud=cloud,
        packages=[pkg for pkg in packages] + extra_packages,
        priorities=priorities,
        strict=strict,
        progress=progress,
        architecture=architecture,
        pip_check_errors=pip_check_errors,
        gpu_enabled=gpu_enabled,
    )
    return result


async def scan_and_create(
    cloud: CloudV2,
    cluster=None,
    show_widget: bool = False,
    workspace: Optional[str] = None,
    region_name: Optional[str] = None,
    package_sync_strict: bool = False,
    package_sync_conda_extras: Optional[List[str]] = None,
    package_sync_ignore: Optional[List[str]] = None,
    package_sync_only: Optional[Set[str]] = None,
    package_sync_fail_on: PackageLevelEnum = PackageLevelEnum.CRITICAL,
    use_uv_installer: bool = True,
    architecture: ArchitectureTypesEnum = ArchitectureTypesEnum.X86_64,
    gpu_enabled: bool = False,
    force_rich_widget: bool = False,
):
    use_widget = force_rich_widget or (show_widget and use_rich_widget())

    local_env_name = Path(sys.prefix).name
    if use_widget:
        progress = Progress(TextColumn("[progress.description]{task.description}"), BarColumn(), TimeElapsedColumn())
        live = Live(Panel(progress, title=f"[green]Package Sync for {local_env_name}", width=CONSOLE_WIDTH))
    else:
        live = contextlib.nullcontext()
        progress = None

    with live:
        with simple_progress("Fetching latest package priorities", progress):
            logger.info(f"Resolving your local {local_env_name} Python environment...")
            async with (
                cluster._time_cluster_event("package sync", "fetch package levels")
                if cluster
                else contextlib.nullcontext()
            ):
                package_levels = await cloud._fetch_package_levels(workspace=workspace)

        package_level_lookup: Dict[Tuple[str, Literal["pip", "conda"]], PackageLevelEnum] = {
            (pkg["name"], pkg["source"]): (
                PackageLevelEnum(pkg["level"]) if pkg["level"] in KNOWN_PACKAGE_LEVELS else pkg["level"]
            )
            for pkg in package_levels
        }
        if package_sync_ignore:
            for package in package_sync_ignore:
                package_level_lookup[(package, "conda")] = PackageLevelEnum.IGNORE
                package_level_lookup[(package, "pip")] = PackageLevelEnum.IGNORE
        # Never ignore packages in package_sync_conda_extras
        if package_sync_conda_extras:
            for package in package_sync_conda_extras:
                if package_level_lookup.get((package, "conda")) == PackageLevelEnum.IGNORE:
                    package_level_lookup[(package, "conda")] = PackageLevelEnum.LOOSE
        async with (
            cluster._time_cluster_event("package sync", "approximate environment")
            if cluster
            else contextlib.nullcontext()
        ):
            approximation = await create_environment_approximation(
                cloud=cloud,
                only=package_sync_only,
                priorities=package_level_lookup,
                strict=package_sync_strict,
                progress=progress,
                architecture=architecture,
                gpu_enabled=gpu_enabled,
                conda_extras=package_sync_conda_extras,
            )

        if not package_sync_only:
            # if we're not operating on a subset, check
            # all the coiled defined critical packages are present
            packages_by_name: Dict[str, ResolvedPackageInfo] = {p["name"]: p for p in approximation}
            _check_halting_issues(package_levels, packages_by_name, package_sync_fail_on, package_sync_strict)
        packages_with_errors = [
            (
                pkg,
                package_level_lookup.get(
                    (
                        (cast(str, pkg["conda_name"]) if pkg["source"] == "conda" else pkg["name"]),
                        pkg["source"],
                    ),
                    PackageLevelEnum.WARN,
                ),
            )
            for pkg in approximation
            if pkg["error"]
        ]
        packages_with_notes = [
            pkg
            for pkg in approximation
            if (
                pkg["note"]
                and (
                    package_level_lookup.get(
                        (
                            (cast(str, pkg["conda_name"]) if pkg["source"] == "conda" else pkg["name"]),
                            pkg["source"],
                        ),
                        PackageLevelEnum.WARN,
                    )
                    > PackageLevelEnum.IGNORE
                )
            )
        ]
        if not use_widget:
            for pkg_with_error, level in packages_with_errors:
                # Only log as warning if we are not going to show a widget
                if level >= PackageLevelEnum.WARN:
                    logfunc = logger.warning
                else:
                    logfunc = logger.info
                logfunc(f"Package - {pkg_with_error['name']}, {pkg_with_error['error']}")

            for pkg_with_note in packages_with_notes:
                logger.debug(f"Package - {pkg_with_note['name']}, {pkg_with_note['note']}")

        async with cluster._time_cluster_event("package sync", "create env") if cluster else contextlib.nullcontext():
            package_sync_env_alias = await cloud._create_package_sync_env(
                packages=approximation,
                workspace=workspace,
                progress=progress,
                gpu_enabled=gpu_enabled,
                architecture=architecture,
                # This is okay because we will default to account
                # default region in declarative service create_software_environment
                region_name=region_name,
                use_uv_installer=use_uv_installer,
            )
    if use_widget:
        print_rich_package_table(packages_with_notes, packages_with_errors)

    return package_sync_env_alias


@track_context
def _check_halting_issues(
    package_levels: List[PackageLevel],
    packages_by_name: Dict[str, ResolvedPackageInfo],
    package_sync_fail_on: PackageLevelEnum,
    package_sync_strict,
):
    critical_packages = [pkg["name"] for pkg in package_levels if pkg["level"] == PackageLevelEnum.CRITICAL]
    halting_failures = []
    for critical_package in critical_packages:
        if critical_package not in packages_by_name:
            problem: ResolvedPackageInfo = {
                "name": critical_package,
                "sdist": None,
                "source": "pip",
                "channel": None,
                "conda_name": critical_package,
                "client_version": "n/a",
                "specifier": "n/a",
                "include": False,
                "note": None,
                "error": f"Could not detect package locally, please install {critical_package}",
                "md5": None,
            }
            halting_failures.append(problem)
        elif not packages_by_name[critical_package]["include"]:
            halting_failures.append(packages_by_name[critical_package])
    for package_level in package_levels:
        package = packages_by_name.get(package_level["name"])
        if package and package["error"]:
            if package_level["level"] > package_sync_fail_on or package_sync_strict:
                halting_failures.append(package)
    if halting_failures:
        # fall back to the note if no error is present
        # this only really happens if a user specified
        # a critical package to ignore
        failure_str = ", ".join([f"{pkg['name']} - {pkg['error'] or pkg['note']}" for pkg in halting_failures])
        raise RuntimeError(f"""Issues with critical packages: {failure_str}

Your software environment has conflicting dependency requirements.
Creating a new environment with only the packages you need typically
resolves most common issues.

If you use conda:

    $ conda create -n myenv -c conda-forge coiled package1 package2 ...

If you use pip, venv, uv, pixi, etc. create a new environment and then:

    $ pip install coiled package1 package2 ...

See https://docs.coiled.io/user_guide/software/package_sync_best_practices.html
for more best practices. If that doesn't solve your issue, please contact support@coiled.io.""")


if __name__ == "__main__":
    from logging import basicConfig

    basicConfig(level=logging.INFO)

    from rich.console import Console
    from rich.table import Table

    async def run():
        async with CloudV2(asynchronous=True) as cloud:
            return await create_environment_approximation(
                cloud=cloud,
                priorities={
                    ("dask", "conda"): PackageLevelEnum.CRITICAL,
                    ("twisted", "conda"): PackageLevelEnum.IGNORE,
                    ("graphviz", "conda"): PackageLevelEnum.LOOSE,
                    ("icu", "conda"): PackageLevelEnum.LOOSE,
                },
            )

    result = asyncio.run(run())

    table = Table(title="Packages")
    keys = ("name", "source", "include", "client_version", "specifier", "error", "note")

    for key in keys:
        table.add_column(key)

    for pkg in result:
        row_values = [str(pkg.get(key, "")) for key in keys]
        table.add_row(*row_values)
    console = Console()
    console.print(table)
    console.print(table)
