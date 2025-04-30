"""CLI for setup_repro_env."""

import logging
import os
import platform
import sys
from typing import List, Optional, Tuple

import click
import inject
import structlog
from click.core import ParameterSource
from evergreen import EvergreenApi

from db_contrib_tool.clients.resmoke_proxy import ResmokeProxy
from db_contrib_tool.config import (
    CONTINUOUS_RELEASE_ALIAS,
    LTS_RELEASE_ALIAS,
    SETUP_REPRO_ENV_CONFIG,
    SETUP_REPRO_ENV_CONFIG_FILE,
    SetupReproEnvConfig,
)
from db_contrib_tool.setup_repro_env.download_service import DownloadOptions
from db_contrib_tool.setup_repro_env.setup_repro_env import (
    SetupReproOrchestrator,
    SetupReproParameters,
)
from db_contrib_tool.usage_analytics import CommandWithUsageTracking
from db_contrib_tool.utils.evergreen_conn import EVERGREEN_CONFIG_LOCATIONS, get_evergreen_api

DEFAULT_INSTALL_DIR = os.path.join(os.getcwd(), "build", "multiversion_bin")
DEFAULT_LINK_DIR = os.getcwd()
DEFAULT_WITH_ARTIFACTS_INSTALL_DIR = os.path.join(os.getcwd(), "repro_envs")
DEFAULT_WITH_ARTIFACTS_LINK_DIR = os.path.join(
    DEFAULT_WITH_ARTIFACTS_INSTALL_DIR, "multiversion_bin"
)

EDITIONS = ("base", "enterprise", "targeted")
DEFAULT_EDITION = "enterprise"
ARCHITECTURES = ("x86_64", "arm64", "aarch64", "ppc64le", "s390x")
DEFAULT_ARCHITECTURE = "x86_64"

DEFAULT_RESMOKE_CMD = "python buildscripts/resmoke.py"

EXTERNAL_LOGGERS = [
    "evergreen",
    "github",
    "inject",
    "urllib3",
]
LOGGER = structlog.get_logger(__name__)


def setup_logging(debug: bool = False) -> None:
    """
    Enable logging.

    :param debug: Whether to setup debug logging.
    """
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        format="[%(asctime)s - %(name)s - %(levelname)s] %(message)s",
        level=log_level,
        stream=sys.stdout,
    )
    for logger in EXTERNAL_LOGGERS:
        logging.getLogger(logger).setLevel(logging.WARNING)
    structlog.configure(logger_factory=structlog.stdlib.LoggerFactory())


@click.command(cls=CommandWithUsageTracking)
@click.pass_context
@click.argument(
    "versions",
    nargs=-1,
    required=False,
    metavar="[VERSION=BIN_SUFFIX]...",
)
@click.option(
    "-i",
    "--installDir",
    "install_dir",
    type=click.Path(),
    default=DEFAULT_INSTALL_DIR,
    help="Directory to install the download archive.",
    show_default=f"`{DEFAULT_INSTALL_DIR}`, if --downloadArtifacts is passed"
    f" the value defaults to `{DEFAULT_WITH_ARTIFACTS_INSTALL_DIR}`",
)
@click.option(
    "-l",
    "--linkDir",
    "link_dir",
    type=click.Path(),
    default=DEFAULT_LINK_DIR,
    help="Directory to install the download archive.",
    show_default=f"`{DEFAULT_LINK_DIR}`, if --downloadArtifacts is passed"
    f" the value defaults to `{DEFAULT_WITH_ARTIFACTS_LINK_DIR}`",
)
@click.option(
    "-e",
    "--edition",
    type=click.Choice(EDITIONS, case_sensitive=False),
    default=DEFAULT_EDITION,
    help="Edition of the build to download.",
)
@click.option(
    "-p",
    "--platform",
    "_platform",
    help=f"Platform to download. Available platforms can be found in {SETUP_REPRO_ENV_CONFIG_FILE}.",
)
@click.option(
    "-a",
    "--architecture",
    type=click.Choice(ARCHITECTURES, case_sensitive=False),
    help="Architecture to download.",
)
@click.option(
    "-v",
    "--variant",
    help="Specify a variant to use, which supersedes the --platform, --edition and --architecture options.",
)
@click.option(
    "--installLastLTS",
    "install_last_lts",
    is_flag=True,
    help="If specified, the last LTS version will be installed.",
)
@click.option(
    "--installLastContinuous",
    "install_last_continuous",
    is_flag=True,
    help="If specified, the last continuous version will be installed.",
)
@click.option(
    "-sb",
    "--skipBinaries",
    "skip_binaries",
    is_flag=True,
    help="Whether to skip downloading binaries.",
)
@click.option(
    "-ds",
    "--downloadSymbols",
    "download_symbols",
    is_flag=True,
    help="Whether to download debug symbols.",
)
@click.option(
    "-da",
    "--downloadArtifacts",
    "download_artifacts",
    is_flag=True,
    help="Whether to download artifacts.",
)
@click.option(
    "-dv",
    "--downloadPythonVenv",
    "download_python_venv",
    is_flag=True,
    help="Whether to download python venv.",
)
@click.option(
    "-ec",
    "--evergreenConfig",
    "evergreen_config",
    type=click.Path(),
    help="Location of evergreen configuration file.",
    show_default=f"If not specified it will look for it in the following locations: {EVERGREEN_CONFIG_LOCATIONS}.",
)
@click.option(
    "-d",
    "--debug",
    is_flag=True,
    help="Set DEBUG logging level.",
)
@click.option(
    "-rp",
    "--require-push",
    is_flag=True,
    help="Require the push task to be successful for assets to be downloaded.",
)
@click.option(
    "--resmokeCmd",
    "resmoke_cmd",
    default=DEFAULT_RESMOKE_CMD,
    help="Command to invoke resmoke.py.",
)
@click.option(
    "--fallbackToMaster",
    "fallback_to_master",
    is_flag=True,
    help="Fallback to downloading the latest binaries from master if the requested"
    " version is not found (Only application for mongo versions).",
)
@click.option(
    "--evgVersionsFile",
    "evg_versions_file",
    type=click.Path(),
    hidden=True,
)
@click.option(
    "-ed",
    "--extractDownloads",
    "extract_downloads",
    default=True,
    hidden=True,
)
@click.option(
    "-bn",
    "--binariesName",
    "binaries_name",
    hidden=True,
)
@click.option(
    "-dn",
    "--debugsymbolsName",
    "debugsymbols_name",
    hidden=True,
)
def setup_repro_env(
    ctx: click.Context,
    install_dir: str,
    link_dir: str,
    edition: str,
    _platform: Optional[str],
    architecture: str,
    variant: Optional[str],
    versions: Tuple[str],
    install_last_lts: bool,
    install_last_continuous: bool,
    skip_binaries: bool,
    download_symbols: bool,
    download_artifacts: bool,
    download_python_venv: bool,
    evergreen_config: Optional[str],
    debug: bool,
    require_push: bool,
    resmoke_cmd: str,
    fallback_to_master: bool,
    evg_versions_file: str,
    extract_downloads: bool,
    binaries_name: str,
    debugsymbols_name: str,
) -> None:
    """
    Set up MongoDB repro environment.

    Downloads and installs particular MongoDB versions into install directory
    and symlinks the binaries to another directory. Each symlink name will
    include the binary release version, e.g. mongod-6.1. This script supports
    community and enterprise builds.

    Accepts the following values:

        - binary versions - examples: <major.minor>, 4.2, 4.4, 5.0 etc.

        - `last-lts` and `last-continuous` - will be translated into
        corresponding versions, e.g. 8.0, 8.1

        - `master` and release branch names

        - full git commit hashes

        - evergreen version ids

        - evergreen task ids

    Optionally with the version accepts binary suffix, e.g. <version>=<bin_suffix>:

        - aliases `last-lts`, `last-continuous` will be translated into
        corresponding versions, e.g. 8.0, 8.1.

    If no versions are specified the last LTS and the last continuous versions
    will be installed.
    """
    if ctx.get_parameter_source("install_dir") == ParameterSource.DEFAULT and download_artifacts:
        install_dir = DEFAULT_WITH_ARTIFACTS_INSTALL_DIR
    if ctx.get_parameter_source("link_dir") == ParameterSource.DEFAULT and download_artifacts:
        link_dir = DEFAULT_WITH_ARTIFACTS_LINK_DIR

    setup_logging(debug)

    if architecture is None:
        architecture = platform.machine()
        if architecture in ARCHITECTURES:
            LOGGER.info(f"Auto detected architecture: {architecture}")
        else:
            LOGGER.info(f"Could not auto detect architecture, defaulting to {DEFAULT_ARCHITECTURE}")
            LOGGER.debug(f"Platform details: {platform.uname()}")
            architecture = DEFAULT_ARCHITECTURE

    download_options = DownloadOptions(
        download_binaries=(not skip_binaries),
        download_symbols=download_symbols,
        download_artifacts=download_artifacts,
        download_python_venv=download_python_venv,
        install_dir=os.path.abspath(install_dir),
        link_dir=os.path.abspath(link_dir),
        extract_downloads=extract_downloads,
        binaries_name=binaries_name,
        debugsymbols_name=debugsymbols_name,
    )
    setup_repro_params = SetupReproParameters(
        edition=edition.lower(),
        platform=_platform.lower() if _platform else None,
        architecture=architecture.lower(),
        variant=variant.lower() if variant else None,
        versions=massage_versions(install_last_continuous, install_last_lts, versions),
        ignore_failed_push=(not require_push),
        fallback_to_master=fallback_to_master,
        download_options=download_options,
        evg_versions_file=evg_versions_file,
    )
    evg_api = get_evergreen_api(evergreen_config)

    def dependencies(binder: inject.Binder) -> None:
        """Define dependencies for execution."""
        binder.bind(SetupReproEnvConfig, SETUP_REPRO_ENV_CONFIG)
        binder.bind(EvergreenApi, evg_api)
        binder.bind(ResmokeProxy, ResmokeProxy.with_cmd(resmoke_cmd))

    inject.configure(dependencies)
    setup_repro_orchestrator = inject.instance(SetupReproOrchestrator)

    success = setup_repro_orchestrator.execute(setup_repro_params)
    if not success:
        sys.exit(1)


def massage_versions(
    install_last_continuous: bool, install_last_lts: bool, input_versions: Tuple[str]
) -> List[str]:
    """
    Process input parameters to get the list of version requests.

    :param install_last_continuous: Whether the last continuous version requested.
    :param install_last_lts: Whether the last lts version requested.
    :param input_versions: Requested versions.
    :return: The list of version requests.
    """
    versions = []
    for version in input_versions:
        if version in [LTS_RELEASE_ALIAS, CONTINUOUS_RELEASE_ALIAS]:
            versions.append(f"{version}={version}")
        else:
            versions.append(version)

    if install_last_lts:
        versions.append(f"{LTS_RELEASE_ALIAS}={LTS_RELEASE_ALIAS}")

    if install_last_continuous:
        versions.append(f"{CONTINUOUS_RELEASE_ALIAS}={CONTINUOUS_RELEASE_ALIAS}")

    if len(versions) == 0:
        versions = [
            f"{LTS_RELEASE_ALIAS}={LTS_RELEASE_ALIAS}",
            f"{CONTINUOUS_RELEASE_ALIAS}={CONTINUOUS_RELEASE_ALIAS}",
        ]

    return list(set(versions))
