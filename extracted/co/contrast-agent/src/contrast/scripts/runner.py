# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.

import argparse
import os
import sys
import shutil

import contrast
from contrast_rewriter import log_stderr

DESCRIPTION = """
The command-line runner for the Contrast Python Agent.
"""

USAGE = "%(prog)s [-h] -- cmd [cmd ...]"

EPILOG = """
Insert this command before the one you usually use to start your webserver
to apply Contrast's instrumentation. See our public documentation for details:
https://docs.contrastsecurity.com/en/python.html
"""


def _log(msg: str) -> None:
    log_stderr(msg, logger_name="contrast-runner")


def runner() -> None:
    _log("Preparing environment for Contrast instrumentation")
    _log(f"Python Agent version: {contrast.__version__}")
    parser = argparse.ArgumentParser(
        description=DESCRIPTION,
        usage=USAGE,
        epilog=EPILOG,
    )
    # if you add public arguments here, update USAGE accordingly
    parser.add_argument(
        "cmd",
        nargs="+",
        help="Command to run with the agent. cmd should be available in the operating system PATH.",
    )

    parsed = parser.parse_args()

    cmd_path, *args = shutil.which(parsed.cmd[0]), *parsed.cmd
    if cmd_path is None:
        _log(f"ERROR: command not found: {parsed.cmd[0]}")
        _log(f"Run '{sys.argv[0]} --help' for usage information.")
        sys.exit(1)
        return

    loader_path = os.path.join(os.path.dirname(contrast.__file__), "loader")
    os.environ["PYTHONPATH"] = os.path.pathsep.join([loader_path] + sys.path)
    os.environ["CONTRAST_INSTALLATION_TOOL"] = "CONTRAST_PYTHON_RUN"

    _log(f"Entering target process: {parsed.cmd[0]}")
    os.execl(cmd_path, *args)
