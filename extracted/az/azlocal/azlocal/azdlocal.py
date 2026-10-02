#!/usr/bin/env python

"""
Thin wrapper around the "azd" command line interface (CLI) for use
with LocalStack.

The "azdlocal" CLI allows you to easily spin up your IaC against LocalStack
without having to configure anything.

Example:
Instead of the following command ...
HTTPS_PROXY=... SSL_CERT_FILE=... azd up
... you can simply use this:
azdlocal up

Options:
  Run "azdlocal help" for more details on the Azure CLI subcommands.
"""

import os
import sys

from .shared import check_emulator_is_running, get_proxy_endpoint, prepare_environment


def usage() -> None:
    print(__doc__.strip())


def run(cmd: list[str], env: dict[str, str] | None = None) -> None:
    """
    Replaces this process with the AZ CLI process, with the given command and environment
    """
    os.execvpe(cmd[0], cmd, env)  # type: ignore[arg-type]


def main() -> None:
    if len(sys.argv) > 1 and sys.argv[1] == "-h":
        return usage()
    run_as_separate_process()


def run_as_separate_process() -> None:
    """
    Constructs a command line string and calls "az" as an external process.
    """

    cmd_args = list(sys.argv)
    cmd_args[0] = "azd"
    if ("help" in cmd_args) or ("version" in cmd_args):
        # Early exit - if we only want to know the version/help, we don't need LS to be running
        run(cmd_args, None)
        return

    check_emulator_is_running()
    proxy_endpoint = get_proxy_endpoint()

    env_dict = prepare_environment(proxy_endpoint)

    # Hijack the login command to automatically login
    if len(cmd_args) > 1 and cmd_args[1] == "auth" and "--help" not in cmd_args:
        cmd_args = [
            "azd",
            "auth",
            "login",
            "--client-id",
            "any-app",
            "--client-secret",
            "any-pass",
            "--tenant-id",
            "any-tenant",
        ]

    # run the command
    run(cmd_args, env_dict)


if __name__ == "__main__":
    main()
