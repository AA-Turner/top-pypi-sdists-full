################################################################################
# This entrypoint is also used in the empty hud-sdk package.
# Do not import any modules from the hud-sdk package here.
################################################################################

import argparse
import os
import shutil
import sys
from typing import Optional


def log_to_user(msg: str) -> None:
    print(msg, file=sys.stderr)


def find_command_executable(command: str) -> Optional[str]:
    if os.path.isfile(command):
        return command
    return shutil.which(command)


def set_auto_init_dir() -> None:
    auto_init_dir = os.path.dirname(os.path.abspath(__file__))
    python_path = os.environ.get("PYTHONPATH", "")
    python_path = f"{auto_init_dir}{os.path.pathsep}{python_path}"
    os.environ["PYTHONPATH"] = python_path


def set_modules_to_trace(extra_modules: str) -> None:
    modules_to_trace = os.environ.get("HUD_MODULES_TO_TRACE")
    if modules_to_trace:
        modules_to_trace = f"{modules_to_trace},{extra_modules}"
    else:
        modules_to_trace = extra_modules
    os.environ["HUD_MODULES_TO_TRACE"] = modules_to_trace


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--include-modules",
        default="",
        help="Comma-separated list of modules to include in Hud instrumentation",
    )
    parser.add_argument("command", nargs=argparse.REMAINDER, help="Command to run")

    args = parser.parse_args()

    if args.include_modules:
        set_modules_to_trace(args.include_modules)

    set_auto_init_dir()
    if not args.command:
        # In case you want to change this log, please edit it both here and in the users_logs.py file for docs purposes.
        log_to_user("[ERROR] Hud: Please provide a valid command to run.")
        sys.exit(1)

    command_found = find_command_executable(args.command[0])
    if not command_found:
        # In case you want to change this log, please edit it both here and in the users_logs.py file for docs purposes.
        log_to_user("[ERROR] Hud: Command executable not found.")
        sys.exit(1)

    os.execl(command_found, command_found, *args.command[1:])


if __name__ == "__main__":
    main()
