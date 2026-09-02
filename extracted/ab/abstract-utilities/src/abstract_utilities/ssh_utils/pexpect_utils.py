from .imports import *
# pexpect is optional; import lazily if you prefer

# keep your execute_cmd; add a thin wrapper that supports stdin text cleanly
def execute_cmd_input(
    *args,
    input_text: str | None = None,
    outfile: str | None = None,
    **kwargs
) -> str:
    """
    Like execute_cmd, but lets you pass text to stdin (subprocess.run(input=...)).
    """
    if input_text is not None:
        kwargs["input"] = input_text
        # ensure text mode so Python passes str not bytes
        kwargs.setdefault("text", True)
    return execute_cmd(*args, outfile=outfile, **kwargs)

# -------------------------
# Core: capture + printing
# -------------------------
def exec_sudo_capture(
    cmd: str,
    *,
    password: str | None = None,
    key: str | None = None,
    user_at_host: str | None = None,
    cwd: str | None = None,
    print_output: bool = False,
) -> str:
    """
    Run a sudo command and return its output (no temp file).
    """
    if password is None:
        password = get_env_value(key=key) if key else get_sudo_password()

    sudo_cmd = f"sudo -S -k {cmd}"

    if user_at_host:
        # build the remote command (bash -lc + optional cd)
        remote = get_remote_cmd(cmd=sudo_cmd, user_at_host=user_at_host, cwd=cwd)
        # feed password to remote's stdin (ssh forwards stdin)
        out = execute_cmd_input(remote, input_text=password + "\n",
                                shell=True, text=True, capture_output=True)
    else:
        out = execute_cmd_input(sudo_cmd, input_text=password + "\n",
                                shell=True, text=True, capture_output=True, cwd=cwd)

    if print_output:
        print_cmd(cmd, out or "")
    return out or ""



# ---------------------------------------------------
# SUDO helpers (local + SSH) with env/password options
# ---------------------------------------------------
def exec_sudo(
    cmd: str,
    *,
    password: Optional[str] = None,
    key: Optional[str] = None,
    user_at_host: Optional[str] = None,
    cwd: Optional[str] = None,
    outfile: Optional[str] = None,
    print_output: bool = False,
) -> str:
    """
    Execute `cmd` via sudo either locally or on remote.
    Password order of precedence:
      1) `password` arg
      2) `key` -> get_env_value(key)
      3) get_sudo_password()

    Uses: sudo -S -k    (-S read password from stdin, -k invalidate cached timestamp)
    """
    if password is None:
        if key:
            password = get_env_value(key=key)
        else:
            password = get_sudo_password()

    # Compose the sudo command that reads from stdin
    sudo_cmd = f"sudo -S -k {cmd}"

    if user_at_host:
        # For remote: the password is piped to SSH stdin, which flows to remote sudo's stdin.
        remote = get_remote_cmd(cmd=sudo_cmd, user_at_host=user_at_host, cwd=cwd)
        full = f"printf %s {shlex.quote(password)} | {remote}"
        out = execute_cmd(full, shell=True, text=True, capture_output=True, outfile=outfile)
    else:
        # Local
        full = f"printf %s {shlex.quote(password)} | {sudo_cmd}"
        out = execute_cmd(full, shell=True, text=True, capture_output=True, outfile=outfile)

    if print_output:
        print_cmd(cmd, out or "")
    return out or ""


# -------------------------------------------------
# Fire-and-forget (file-backed) compatible runner
# -------------------------------------------------
def cmd_run(
    cmd: str,
    output_text: str | None = None,
    print_output: bool = False,
    *,
    user_at_host: str | None = None,
    cwd: str | None = None,
) -> str | None:
    """
    If output_text is None → capture+return output (no file).
    If output_text is provided → legacy file-backed behavior.
    """
    if output_text is None:
        # capture mode
        if user_at_host:
            remote = get_remote_cmd(cmd=cmd, user_at_host=user_at_host, cwd=cwd)
            out = execute_cmd(remote, shell=True, text=True, capture_output=True)
        else:
            out = execute_cmd(cmd, shell=True, text=True, capture_output=True, cwd=cwd)
        if print_output:
            print_cmd(cmd, out or "")
        return out or ""

    # ---- legacy file-backed path (unchanged in spirit) ----
    # Clear output file
    with open(output_text, 'w'):
        pass

    # Append redirection + sentinel
    full_cmd = f'{cmd} >> {output_text}; echo END_OF_CMD >> {output_text}'

    # Execute local/remote
    if user_at_host:
        remote_line = get_remote_cmd(cmd=full_cmd, user_at_host=user_at_host, cwd=cwd)
        subprocess.call(remote_line, shell=True)
    else:
        subprocess.call(full_cmd, shell=True, cwd=cwd)

    # Wait for sentinel
    while True:
        get_sleep(sleep_timer=0.5)
        with open(output_text, 'r') as f:
            lines = f.readlines()
            if lines and lines[-1].strip() == 'END_OF_CMD':
                break

    if print_output:
        with open(output_text, 'r') as f:
            print_cmd(full_cmd, f.read().strip())

    try:
        os.remove(output_text)
    except OSError:
        pass

    return None


# ----------------------------------------------------
# pexpect wrappers (local + SSH) for interactive flows
# ----------------------------------------------------
def exec_expect(
    command: str,
    child_runs: List[Dict[str, Any]],
    *,
    user_at_host: Optional[str] = None,
    cwd: Optional[str] = None,
    print_output: bool = False,
) -> int:
    """
    Run `command` and answer interactive prompts.

    child_runs: list of dicts like:
      { "prompt": r"Password:", "pass": "xyz" }
      { "prompt": r"Enter passphrase:", "key": "MY_KEY", "env_path": "/path/for/.env" }
    If "pass" is None, we resolve via get_env_value(key=..., start_path=env_path).

    Returns exitstatus (0=success).
    """
    if user_at_host:
        # Wrap command for remote execution
        remote_line = get_remote_cmd(cmd=command, user_at_host=user_at_host, cwd=cwd)
        spawn_cmd = f"{remote_line}"
    else:
        spawn_cmd = f"bash -lc {shlex.quote((f'cd {shlex.quote(cwd)} && {command}') if cwd else command)}"

    child = pexpect.spawn(spawn_cmd)

    for each in child_runs:
        child.expect(each["prompt"])

        if each.get("pass") is not None:
            pass_phrase = each["pass"]
        else:
            args = {}
            if "key" in each and each["key"] is not None:
                args["key"] = each["key"]
            if "env_path" in each and each["env_path"] is not None:
                args["start_path"] = each["env_path"]
            pass_phrase = get_env_value(**args)

        child.sendline(pass_phrase)
        if print_output:
            print("Answered prompt:", each["prompt"])

    child.expect(pexpect.EOF)
    out = child.before.decode("utf-8", errors="ignore")
    if print_output:
        print_cmd(command, out)

    return child.exitstatus if child.exitstatus is not None else 0


# ---------------------------------------
# Convenience shims to mirror your names
# ---------------------------------------
def cmd_run_sudo(
    cmd: str,
    password: str | None = None,
    key: str | None = None,
    output_text: str | None = None,
    *,
    user_at_host: str | None = None,
    cwd: str | None = None,
    print_output: bool = False,
) -> str | None:
    """
    If output_text is None → capture sudo output and return it.
    If output_text is provided → legacy file-backed behavior feeding sudo via stdin.
    """
    if output_text is None:
        return exec_sudo_capture(
            cmd,
            password=password,
            key=key,
            user_at_host=user_at_host,
            cwd=cwd,
            print_output=print_output,
        )

    # ---- legacy file-backed path ----
    # build the underlying sudo command
    sudo_cmd = f"sudo -S -k {cmd}"
    pw = password if password is not None else (get_env_value(key=key) if key else get_sudo_password())

    # We need to feed password to stdin in the same shell that runs sudo.
    # For file-backed mode we’ll inline a small shell that reads from a here-string.
    # Local:
    if not user_at_host:
        full = f'bash -lc {shlex.quote((f"cd {shlex.quote(cwd)} && " if cwd else "") + f"printf %s {shlex.quote(pw)} | {sudo_cmd}")}'
        return cmd_run(full, output_text=output_text, print_output=print_output)
    # Remote:
    # On remote, do the same in the remote bash -lc
    remote_sudo_line = f'printf %s {shlex.quote(pw)} | {sudo_cmd}'
    remote_full = get_remote_cmd(cmd=remote_sudo_line, user_at_host=user_at_host, cwd=cwd)
    return cmd_run(remote_full, output_text=output_text, print_output=print_output)
def pexpect_cmd_with_args(
    command: str,
    child_runs: list,
    output_text: str | None = None,
    *,
    user_at_host: str | None = None,
    cwd: str | None = None,
    print_output: bool = False
) -> int:
    """
    If output_text is None → return output string via print_output, else write to file then remove (legacy).
    """
    if user_at_host:
        spawn_cmd = get_remote_cmd(cmd=command, user_at_host=user_at_host, cwd=cwd)
    else:
        spawn_cmd = f"bash -lc {shlex.quote((f'cd {shlex.quote(cwd)} && {command}') if cwd else command)}"

    child = pexpect.spawn(spawn_cmd)

    for each in child_runs:
        child.expect(each["prompt"])
        if each.get("pass") is not None:
            pass_phrase = each["pass"]
        else:
            args = {}
            if "key" in each and each["key"] is not None:
                args["key"] = each["key"]
            if "env_path" in each and each["env_path"] is not None:
                args["start_path"] = each["env_path"]
            pass_phrase = get_env_value(**args)
        child.sendline(pass_phrase)
        if print_output:
            print("Answered prompt:", each["prompt"])

    child.expect(pexpect.EOF)
    out = child.before.decode("utf-8", errors="ignore")

    if output_text:
        with open(output_text, "w") as f:
            f.write(out)
        if print_output:
            print_cmd(command, out)
        # keep legacy? your old code removed the file; here we’ll keep it (safer).
        # If you want the old behavior, uncomment:
        # os.remove(output_text)
    else:
        if print_output:
            print_cmd(command, out)
