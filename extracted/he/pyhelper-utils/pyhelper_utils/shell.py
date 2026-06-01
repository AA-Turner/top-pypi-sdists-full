from __future__ import annotations

import contextlib
import subprocess
from typing import Any, Final

import paramiko
from rrmngmnt import Host
from simple_logger.logger import get_logger
from timeout_sampler import TimeoutSampler

from pyhelper_utils.exceptions import CommandExecFailed

LOGGER = get_logger(name=__name__)

TIMEOUT_30MIN = 30 * 60

DEFAULT_SSH_EXCEPTIONS: Final[dict[type[Exception], list[str]]] = {paramiko.SSHException: []}


def run_command(
    command: list[str],
    verify_stderr: bool = True,
    shell: bool = False,
    timeout: int | None = None,
    capture_output: bool = True,
    check: bool = True,
    hide_log_command: bool = False,
    log_errors: bool = True,
    **kwargs: Any,
) -> tuple[bool, str, str]:
    """
    Run command locally.

    Args:
        command (list): Command to run
        verify_stderr (bool, default True): Check command stderr
        shell (bool, default False): run subprocess with shell toggle
        timeout (int, optional): Command wait timeout
        capture_output (bool, default False): Capture command output
        check (bool, default True):  If check is True and the exit code was non-zero, it raises a
            CalledProcessError
        hide_log_command (bool, default False): If hide_log_command is True and check will be set to False,
            CalledProcessError will not get raise and command will not be printed.
        log_errors (bool, default True): If log_errors is True, error message will be logged.

    Returns:
        tuple: True, out if command succeeded, False, err otherwise.

    Raises:
        CalledProcessError: when check is True and command execution fails
    """
    command_for_log = ["Hide", "By", "User"] if hide_log_command else command

    LOGGER.info(f"Running {' '.join(command_for_log)} command")

    # when hide_log_command is set to True, check should be set to False to avoid logging sensitive data in
    # the exception
    sub_process = subprocess.run(
        command,
        capture_output=capture_output,
        check=check if not hide_log_command else False,
        shell=shell,
        text=True,
        timeout=timeout,
        **kwargs,
    )
    out_decoded = sub_process.stdout
    err_decoded = sub_process.stderr

    error_msg = (
        f"Failed to run {command_for_log}. rc: {sub_process.returncode}, out: {out_decoded}, error: {err_decoded}"
    )

    if sub_process.returncode != 0:
        if log_errors:
            LOGGER.error(error_msg)

        return False, out_decoded, err_decoded

    # From this point and onwards we are guaranteed that sub_process.returncode == 0
    if err_decoded and verify_stderr:
        if log_errors:
            LOGGER.error(error_msg)

        return False, out_decoded, err_decoded

    return True, out_decoded, err_decoded


def _execute_ssh_commands(
    host: Host,
    commands_list: list[list[str]],
    get_pty: bool,
    check_rc: bool,
    timeout: int,
    tcp_timeout: float | None,
) -> list[str]:
    """
    Execute SSH commands on a remote host (single attempt).

    This is a private helper used by ``run_ssh_commands``. It opens an SSH
    session, runs each command, and performs ProxyCommand cleanup.

    Args:
        host (Host): rrmngmnt host to execute the commands from.
        commands_list (list): Normalised list of command lists.
        get_pty (bool): get_pty parameter for remote session.
        check_rc (bool): if True checks command return code and raises if rc != 0.
        timeout (int): ssh exec timeout.
        tcp_timeout (float): an optional timeout (in seconds) for the TCP connect.

    Returns:
        list: List of commands output.

    Raises:
        CommandExecFailed: If command failed to execute.
    """
    results: list[str] = []

    executor = host.executor()
    try:
        with executor.session(timeout=tcp_timeout) as ssh_session:
            for cmd in commands_list:
                rc, out, err = ssh_session.run_cmd(cmd=cmd, get_pty=get_pty, timeout=timeout)
                LOGGER.info(f"[SSH][{host.fqdn}] Executed: {' '.join(cmd)}, rc:{rc}, out: {out}, error: {err}")
                if rc and check_rc:
                    raise CommandExecFailed(name=" ".join(cmd), err=err)

                results.append(out)
    finally:
        # Workaround for Paramiko's ProxyCommand.close() file descriptors leaks bug
        # https://github.com/paramiko/paramiko/pull/2570
        sock = getattr(executor, "sock", None)
        if isinstance(sock, paramiko.ProxyCommand):
            with contextlib.suppress(OSError):
                sock.close()
            try:
                sock.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                with contextlib.suppress(OSError):
                    sock.process.kill()
                with contextlib.suppress(OSError):
                    sock.process.wait(timeout=5)
            except OSError as exp:
                LOGGER.debug(f"ProxyCommand cleanup error: {exp}")

    return results


def run_ssh_commands(
    host: Host,
    commands: list[Any],
    get_pty: bool = False,
    check_rc: bool = True,
    timeout: int = TIMEOUT_30MIN,
    tcp_timeout: float | None = None,
    wait_timeout: int = 0,
    sleep: int = 5,
    exceptions_dict: dict[type[Exception], list[str]] | None = DEFAULT_SSH_EXCEPTIONS,
) -> list[str]:
    """
    Run commands on remote host via SSH

    Args:
        host (Host): rrmngmnt host to execute the commands from.
        commands (list): List of multiple command lists [[cmd1, cmd2, cmd3]] or a list with a single command [cmd]
            Examples:
                 single command: shlex.split("sudo reboot"),
                 multiple commands: [shlex.split("sleep 5"), shlex.split("date")]

        get_pty (bool): get_pty parameter for remote session (equivalent to -t argument for ssh)
        check_rc (bool): if True checks command return code and raises if rc != 0
        timeout (int): ssh exec timeout
        tcp_timeout (float): an optional timeout (in seconds) for the TCP connect
        wait_timeout (int): total retry timeout in seconds. 0 means no retry (default behavior).
        sleep (int): seconds between retry attempts (default 5). Only used when ``wait_timeout > 0``
        exceptions_dict (dict | None): exception types that trigger a retry.
            Defaults to ``DEFAULT_SSH_EXCEPTIONS`` (``{paramiko.SSHException: []}``).
            Pass ``None`` to catch all exceptions.
            Only used when ``wait_timeout > 0``.

    Returns:
        list: List of commands output.

    Raises:
        CommandExecFailed: If command failed to execute.
        TimeoutExpiredError: If wait_timeout > 0 and retries are exhausted.
    """
    commands_list: list[list[str]] = commands if isinstance(commands[0], list) else [commands]

    if wait_timeout == 0:
        return _execute_ssh_commands(
            host=host,
            commands_list=commands_list,
            get_pty=get_pty,
            check_rc=check_rc,
            timeout=timeout,
            tcp_timeout=tcp_timeout,
        )

    for sample in TimeoutSampler(
        wait_timeout=wait_timeout,
        sleep=sleep,
        func=_execute_ssh_commands,
        exceptions_dict=exceptions_dict,
        host=host,
        commands_list=commands_list,
        get_pty=get_pty,
        check_rc=check_rc,
        timeout=timeout,
        tcp_timeout=tcp_timeout,
    ):
        return sample

    return []  # pragma: no cover
