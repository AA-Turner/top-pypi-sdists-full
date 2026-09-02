from .imports import *
from .module_imports import *
def get_pass_from_key(key=None,env_path=None):
    if key:
        return get_env_value(key=key,path=env_path)
def get_password(password=None,key=None,env_path=None):
    password = password or get_pass_from_key(key=key,env_path=env_path)
    return password

def get_print_sudo_cmd(
        cmd: str,
        password=None,
        key=None,
        env_path=None
    ):
    password = get_password(password=password,key=key,env_path=env_path)
    if password != None:
        
        cmd = get_password_cmd(password=password,cmd=cmd)
    return cmd
def get_password_cmd(password:str,cmd:str):
    sudo_cmd = get_sudo_cmd(cmd)
    password_sudo_cmd = get_raw_password_sudo_cmd(password=password,sudo_cmd=sudo_cmd)
    return password_sudo_cmd
def get_sudo_cmd(cmd: str):
    return f"sudo -S -k {cmd}"
def get_raw_password_sudo_cmd(password:str,sudo_cmd:str):
    return f"printf %s {shlex.quote(password)} | {sudo_cmd}"
def get_remote_bash(
            cmd: str,
            cwd: str | None = None
        ):
    return f"bash -lc {shlex.quote((f'cd {shlex.quote(cwd)} && {cmd}') if cwd else cmd)}"
def get_remote_ssh(
            user_at_host: str=None,
            remote:str=None
        ):
    return f"ssh {shlex.quote(user_at_host)} {shlex.quote(remote)}"
def get_remote_cmd(
            cmd: str,
            user_at_host: str,
            cwd: str | None = None,
            password=None,
            key=None,
            env_path=None
            
        ):
    cmd = get_print_sudo_cmd(
            cmd=cmd,
            password=password,
            key=key,
            env_path=env_path
        )
    remote = get_remote_bash(
        cmd=cmd,
        cwd=cwd
        )
    full = get_remote_ssh(
        user_at_host=user_at_host,
        remote=remote
        )
    return full


def execute_cmd(
        *args,
        outfile=None,
        **kwargs
    ) -> str:
    proc = subprocess.run(*args, **kwargs)
    output = (proc.stdout or "") + (proc.stderr or "")
    if outfile:
        try:
            with open(outfile, "w", encoding="utf-8", errors="ignore") as f:
                f.write(output)
        except Exception:
            pass
    return output

def run_local_cmd(
        cmd: str,
        cwd: str | None = None,
        outfile: Optional[str] = None,
        shell=True,
        text=True,
        capture_output=True,
        user_at_host: str=None,
        password=None,
        key=None,
        env_path=None
    ) -> str:
    cmd = get_print_sudo_cmd(
            cmd=cmd,
            password=password,
            key=key,
            env_path=env_path
        )
    return execute_cmd(
            cmd,
            outfile=outfile,
            shell=shell,
            cwd=cwd,
            text=text,
            capture_output=capture_output
        )

def run_remote_cmd(
        user_at_host: str,
        cmd: str,
        cwd: str | None = None,
        outfile: Optional[str] = None,
        shell=True,
        text=True,
        capture_output=True,
        password=None,
        key=None,
        env_path=None
    ) -> str:
    """
    Run on remote via SSH; capture stdout+stderr locally; write to local outfile.
    NOTE: we do *not* try to write the file on the remote to avoid later scp.
    """
    cmd = get_print_sudo_cmd(
            cmd=cmd,
            password=password,
            key=key,
            env_path=env_path
        )
    # wrap in bash -lc for PATH/profile + allow 'cd && ...'
    cmd = get_remote_cmd(
        cmd=cmd,
        user_at_host=user_at_host,
        cwd=cwd
        )
    return execute_cmd(
            cmd,
            outfile=outfile,
            shell=shell,
            text=text,
            capture_output=capture_output
        )

def run_cmd(
        cmd: str=None,
        cwd: str | None = None,
        outfile: Optional[str] = None,
        shell=True,
        text=True,
        capture_output=True,
        user_at_host: str=None,
        password=None,
        key=None,
        env_path=None
    ) -> str:

    if user_at_host:
        return run_ssh_cmd(
                user_at_host=user_at_host,
                cmd=cmd,
                cwd=cwd,
                outfile=outfile,
                shell=shell,
                text=text,
                capture_output=capture_output,
                password=password,
                key=key,
                env_path=env_path
            )
    return run_local_cmd(
            cmd=cmd,
            cwd=cwd,
            outfile=outfile,
            shell=shell,
            text=text,
            capture_output=capture_output,
            password=password,
            key=key,
            env_path=env_path
        )
run_ssh_cmd = run_remote_cmd
remote_cmd = run_remote_cmd
ssh_cmd = run_remote_cmd

local_cmd = run_local_cmd


run_any_cmd = run_cmd
any_cmd = run_cmd
cmd_run = run_cmd
