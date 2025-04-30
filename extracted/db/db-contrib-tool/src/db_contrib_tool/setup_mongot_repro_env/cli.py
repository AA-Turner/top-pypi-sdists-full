"""CLI for setup_mongot_repro_env."""

import logging
import os
import sys

import click
import inject
import structlog

from db_contrib_tool.setup_repro_env.download_service import ArtifactDownloadService, DownloadUrl
from db_contrib_tool.usage_analytics import CommandWithUsageTracking

DEFAULT_INSTALL_DIR = os.path.join(os.getcwd(), "build")
VERSIONS = ("latest", "release")
ARCHITECTURES = ("x86_64", "aarch64")
DEFAULT_ARCHITECTURE = "x86_64"
PLATFORMS = ("linux", "macos")
DEFAULT_PLATFORM = "linux"

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
    "version",
    nargs=1,
    required=False,
    default="latest",
    type=click.Choice(VERSIONS, case_sensitive=False),
)
@click.option(
    "-i",
    "--installDir",
    "install_dir",
    type=click.Path(),
    default=DEFAULT_INSTALL_DIR,
    help="Directory to install the download archive.",
    show_default=f"`{DEFAULT_INSTALL_DIR}`",
)
@click.option(
    "-p",
    "--platform",
    "_platform",
    default=DEFAULT_PLATFORM,
    type=click.Choice(PLATFORMS, case_sensitive=False),
    help=f"Platform to download. Available platforms are {PLATFORMS}.",
)
@click.option(
    "-a",
    "--architecture",
    default=DEFAULT_ARCHITECTURE,
    type=click.Choice(ARCHITECTURES, case_sensitive=False),
    help="Architecture to download.",
)
def setup_mongot_repro_env(
    ctx: click.Context,
    install_dir: str,
    _platform: str,
    architecture: str,
    version: str,
) -> None:
    """
    Set up Mongot repro environment.

    Downloads and installs particular Mongot versions into install directory.

    Accepts `latest` and `release` versions.

    If no version and no architecture are specified the latest linux_x86_64 binary will be installed.
    """
    setup_logging(True)

    inject.configure()
    artifact_download_service = inject.instance(ArtifactDownloadService)
    artifact_download_service.download_with_retries(
        DownloadUrl(primary=massage_url_path(version, architecture, _platform)),
        os.path.abspath(install_dir),
        True,
    )


def massage_url_path(version: str, architecture: str, platform: str) -> str:
    """
    Return url path to be used for downloading appropriate mongot binary.

    10gen/mongot releases latest and production binaries to constant/hardcoded S3 links.
    In this way, the latest describes the binaries created by the most recent commit merged to 10gen/mongot.
    Release refers to the mongot binaries running in atlas prod.

    This function processes input parameters to figure out the
    desired url path (release or latest of given arch + platform combo). Release and latest versions differ only in
    the url path, as binary names stay the same across both versions (for any given arch + platform combo).

    As macos with aarch64 is not supported, possible binary names would be:
    - mongot_latest_linux_x86_64.tgz
    - mongot_latest_linux_aarch64.tgz
    - mongot_latest_macos_x86_64.tgz
    """
    if platform == "macos" and architecture == "aarch64":
        raise ValueError("Mongot doesn't support macos with aarch64 architecture")
    url_version_path = (
        "release/mongot_latest_localdev"
        if version == "release"
        else "atlas-search-localdev/mongot_latest"
    )
    return (
        f"https://mciuploads.s3.amazonaws.com/fts/{url_version_path}_{platform}_{architecture}.tgz"
    )
