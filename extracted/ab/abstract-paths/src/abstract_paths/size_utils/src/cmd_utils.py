import subprocess, shlex
from typing import Optional
from abstract_apis import *

def execute_cmd(cmd: str, outfile: Optional[str] = None,
                workdir: str = None, shell: bool = True, **kwargs) -> str:
    """
    Run command, capture stdout+stderr, decode safely as UTF-8.
    """
    proc = subprocess.run(cmd,
                          shell=shell,
                          cwd=workdir,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,
                          text=False)  # capture raw bytes
    output = proc.stdout.decode("utf-8", errors="ignore")

    if outfile:
        try:
            with open(outfile, "w", encoding="utf-8", errors="ignore") as f:
                f.write(output)
        except Exception:
            pass
    return output

def run_local_cmd(cmd: str, workdir: str = None, outfile: Optional[str] = None, **kwargs) -> str:
    return execute_cmd(cmd, outfile=outfile, workdir=workdir)

def run_local_sudo(cmd: str, password: str, workdir: str = None,
                   outfile: Optional[str] = None, **kwargs) -> str:
    """
    Run local command with sudo, suppressing the password prompt output.
    """
    if workdir:
        wrapped = f"cd {shlex.quote(workdir)} && {cmd}"
    else:
        wrapped = cmd
    # -p "" prevents `[sudo] password for user:` in output
    full = f'echo {shlex.quote(password)} | sudo -S -p "" bash -c {shlex.quote(wrapped)}'
    return execute_cmd(full, outfile=outfile)

def run_remote_cmd(user_at_host: str, cmd: str, workdir: str = None,
                   outfile: Optional[str] = None, **kwargs) -> str:
    remote_cmd = f"cd {shlex.quote(workdir)} && {cmd}" if workdir else cmd
    ssh_cmd = f"ssh {shlex.quote(user_at_host)} {shlex.quote(remote_cmd)}"
    return execute_cmd(ssh_cmd, outfile=outfile)

def run_remote_sudo(user_at_host: str, cmd: str, password: str,
                    workdir: str = None, outfile: Optional[str] = None, **kwargs) -> str:
    """
    Run remote command with sudo, suppressing the password prompt output.
    """
    if workdir:
        wrapped = f"cd {shlex.quote(workdir)} && {cmd}"
    else:
        wrapped = cmd
    remote_cmd = f"echo {shlex.quote(password)} | sudo -S -p \"\" bash -c {shlex.quote(wrapped)}"
    ssh_cmd = f"ssh {shlex.quote(user_at_host)} {shlex.quote(remote_cmd)}"
    return execute_cmd(ssh_cmd, outfile=outfile)
