# -*- coding: utf-8 -*-
"""
File to house the   class.

Created on Wed Jul 15 21:22:26 2026

@author: Richard Kellnberger
"""

# TODO docstrings

import os
import subprocess
from abc import ABC, abstractmethod

from mypy import api

from pylsp_mypy import log
from pylsp_mypy.typeDefs import WindowsFlag

# This flag only exists on Windows, hence the 'type: ignore[attr-defined]' below.
windows_flag: WindowsFlag = (
    {"creationflags": subprocess.CREATE_NO_WINDOW}  # type: ignore[attr-defined]
    if os.name == "nt"
    else {}
)


class Backend(ABC):

    @abstractmethod
    def run(self, command: list[str], args: list[str]) -> tuple[str, str, int]:
        pass

    def hover(self, command: list[str], args: list[str]) -> tuple[str, str, int]:
        return None

    def stop(self, command: list[str], status_file: str) -> None:
        pass


class MypyAPIBackend(Backend):

    def run(self, command: list[str], args: list[str]) -> tuple[str, str, int]:
        log.info(f"executing mypy {args=} via API")
        report, errors, exit_status = api.run(args)
        return report, errors, exit_status


class MypyCommandBackend(Backend):

    def run(self, command: list[str], args: list[str]) -> tuple[str, str, int]:
        log.info(f"executing mypy {args=} on PATH")
        completed_process = subprocess.run(
            [*command, *args], capture_output=True, **windows_flag, encoding="utf-8"
        )
        report = completed_process.stdout
        errors = completed_process.stderr
        exit_status = completed_process.returncode
        return report, errors, exit_status


class DmypyAPIBackend(Backend):

    def run(self, command: list[str], args: list[str]) -> tuple[str, str, int]:
        # Kill if hung
        self.reset(command, args)

        # run to use existing daemon or restart if required
        log.info(f"dmypy run {args=} via API")
        report, errors, exit_status = api.run_dmypy(args)

        return report, errors, exit_status

    def reset(self, command: list[str], args: list[str]) -> None:
        # If dmypy daemon is non-responsive calls to run will block.
        # Check daemon status, if non-zero daemon is dead or hung.
        # If daemon is hung, kill will reset
        # If daemon is dead/absent, kill will no-op.
        # In either case, reset to fresh state

        status_file = args[1]  # TODO this is not pretty; Set as member?

        _, errors, exit_status = api.run_dmypy(["--status-file", status_file, "status"])
        if exit_status != 0:
            log.info(
                f"restarting dmypy from status: {exit_status} message: {errors.strip()} via API"
            )
            api.run_dmypy(["--status-file", status_file, "restart"])

    def hover(self, command: list[str], args: list[str]) -> tuple[str, str, int]:
        # Kill if hung
        self.reset(command, args)

        log.info(f"dmypy inspect {args=} via API")
        report, errors, exit_status = api.run_dmypy(args)
        return report, errors, exit_status

    def stop(self, command: list[str], status_file: str) -> None:
        output, errors, exit_status = api.run_dmypy(["--status-file", status_file, "stop"])
        if exit_status != 0:
            log.warning(
                f"failed to stop dmypy; exit code: {exit_status}, message: {errors.strip()}"
            )
            log.warning("killing dmypy")
            api.run_dmypy(["--status-file", status_file, "kill"])
        else:
            log.info(f"dmypy stopped: {output.strip()}")


class DmypyCommandBackend(Backend):

    def run(self, command: list[str], args: list[str]) -> tuple[str, str, int]:
        # Kill if hung
        self.reset(command, args)

        # run to use existing daemon or restart if required
        log.info(f"dmypy run {args=} on PATH")
        completed_process = subprocess.run(
            [*command, *args], capture_output=True, **windows_flag, encoding="utf-8"
        )
        report = completed_process.stdout
        errors = completed_process.stderr
        exit_status = completed_process.returncode
        return report, errors, exit_status

    def reset(self, command: list[str], args: list[str]) -> None:
        # If dmypy daemon is non-responsive calls to run will block.
        # Check daemon status, if non-zero daemon is dead or hung.
        # If daemon is hung, kill will reset
        # If daemon is dead/absent, kill will no-op.
        # In either case, reset to fresh state

        status_file = args[1]  # TODO this is not pretty; Set as member?

        completed_process = subprocess.run(
            [*command, "--status-file", status_file, "status"],
            capture_output=True,
            **windows_flag,
            encoding="utf-8",
        )
        errors = completed_process.stderr
        exit_status = completed_process.returncode
        if exit_status != 0:
            log.info(
                f"restarting dmypy from status: {exit_status} message: {errors.strip()} on PATH"
            )
            subprocess.run(
                ["dmypy", "--status-file", status_file, "restart"],
                capture_output=True,
                **windows_flag,
                encoding="utf-8",
            )

    def hover(self, command: list[str], args: list[str]) -> tuple[str, str, int]:
        # Kill if hung
        self.reset(command, args)

        log.info(f"dmypy inspect {args=} on PATH")
        completed_process = subprocess.run(
            [*command, *args], capture_output=True, **windows_flag, encoding="utf-8"
        )
        report = completed_process.stdout
        errors = completed_process.stderr
        exit_status = completed_process.returncode
        return report, errors, exit_status

    def stop(self, command: list[str], status_file: str) -> None:
        completed_process = subprocess.run(
            [*command, "--status-file", status_file, "stop"],
            capture_output=True,
            **windows_flag,
            encoding="utf-8",
        )
        output, errors = completed_process.stdout, completed_process.stderr
        exit_status = completed_process.returncode
        if exit_status != 0:
            log.warning(
                "failed to stop dmypy via path; "
                f"exit code: {exit_status}, message: {errors.strip()}"
            )
            log.warning("killing dmypy on PATH")
            subprocess.run(
                [*command, "--status-file", status_file, "kill"],
                capture_output=True,
                **windows_flag,
                encoding="utf-8",
                check=True,
            )
        else:
            log.info(f"dmypy stopped on PATH: {output.strip()}")
