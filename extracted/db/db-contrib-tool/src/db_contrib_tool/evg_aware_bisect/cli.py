"""CLI for bisect."""

import os
import sys
from typing import Optional

import click
import inject
from click.core import ParameterSource

from db_contrib_tool.config import SETUP_REPRO_ENV_CONFIG, SetupReproEnvConfig
from db_contrib_tool.evg_aware_bisect import Bisect, BisectParameters
from db_contrib_tool.usage_analytics import CommandWithUsageTracking
from db_contrib_tool.utils.evergreen_conn import EVERGREEN_CONFIG_LOCATIONS

DEFAULT_PYTHON_INSTALLATION = "python3"
TOOLCHAIN_PYTHON3 = "/opt/mongodbtoolchain/v5/bin/python3"


@click.command(cls=CommandWithUsageTracking)
@click.pass_context
@click.option(
    "-l",
    "--lookback",
    default=365,
    help="Maximum number of days to look back for versions to test.",
)
@click.option(
    "-b", "--branch", required=True, help="The branch for which versions are being tested."
)
@click.option(
    "-v", "--variant", required=True, help="The variant for which versions are being tested."
)
@click.option(
    "-s",
    "--script",
    type=click.Path(),
    required=True,
    help="Location of the shell test script to run on the versions.",
)
@click.option(
    "-p",
    "--python-installation",
    type=click.Path(),
    default=DEFAULT_PYTHON_INSTALLATION,
    help="Location of a python installation to use for shell commands.",
    show_default=f"`{DEFAULT_PYTHON_INSTALLATION}` or `{TOOLCHAIN_PYTHON3}` (if toolchain is setup) will be used.",
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
def bisect(
    ctx: click.Context,
    lookback: int,
    branch: str,
    variant: str,
    script: str,
    python_installation: str,
    evergreen_config: Optional[str],
    debug: bool,
) -> None:  # noqa: D205, D400, D415
    """
    Perform an evergreen-aware git-bisect to find the 'last passing version' and
    'first failing version' of mongo, with respect to a user provided shell script.

    The 'bisect' command lets a user specify a '--branch', '--variant' & '--lookback' period on which to
    perform a bisect. The user also provides a shell test '--script' which exits with status code 0 to
    indicate a successful test. The command performs the following steps:

    (1) Get all versions for the given '--branch', '--variant' & '--lookback' period from Evergreen.

    (2) Filter the versions for versions that Evergreen has binaries and artifacts for.

    (3) Find the 'middle' version.

    (4) Setup a test environment.

        - The 'build/resmoke-bisect' directory will have a sub directory --
    'build/resmoke-bisect/{version_id}' containing the git repo for this version.

        - The 'binaries' & 'artifacts' will also be downloaded to the directory named
    'build/resmoke-bisect/{version_id}'.

        - Create a virtual environment at 'build/resmoke-bisect/bisect_venv' and
    install packages for this version.

    (5) Activate 'bisect_venv' & run the user provided shell script from within the
    'build/resmoke-bisect/{version_id}' directory.

    (6) Teardown the test environment.

    (7) Repeat steps (3)-(6) on the left half, if (5) failed, or right half, if (5) succeeded.

    This command will print the "Last Known Passing Version" & "First Known Failing Version".

    NOTE: This 'bisect' command assumes a perfect partition between passing & failing versions.
    ie: [Pass, Pass, Pass, Fail, Fail, Fail]
    If there is not a perfect partition, try modifying the '--lookback' period or shell '--script'.
    """
    if ctx.get_parameter_source(
        "python_installation"
    ) == ParameterSource.DEFAULT and os.path.isfile(TOOLCHAIN_PYTHON3):
        python_installation = TOOLCHAIN_PYTHON3

    def dependencies(binder: inject.Binder) -> None:
        """Dependencies for bisect command execution."""
        binder.bind(SetupReproEnvConfig, SETUP_REPRO_ENV_CONFIG)
        binder.bind(
            BisectParameters,
            BisectParameters(
                branch=branch,
                lookback=lookback,
                variant=variant,
                script=script,
                python_installation=python_installation,
                debug=debug,
                evergreen_config=evergreen_config,
            ),
        )

    inject.configure(dependencies)
    bisect_cmd = inject.instance(Bisect)

    success = bisect_cmd.execute()
    if not success:
        sys.exit(1)
