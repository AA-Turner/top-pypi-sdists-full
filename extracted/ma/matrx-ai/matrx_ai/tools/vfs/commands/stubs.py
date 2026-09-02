from __future__ import annotations

from matrx_ai.tools.vfs.commands.base import CommandContext, encode, fail, ok, resolve_cwd
from matrx_ai.tools.vfs.commands.registry import register
from matrx_ai.tools.vfs.shell.runner import CommandResult


def _first_non_flag(args: list[str]) -> str | None:
    for a in args:
        if not a.startswith("-"):
            return a
    return None


def _extract_host(args: list[str]) -> str:
    skip_next = False
    for a in args:
        if skip_next:
            skip_next = False
            continue
        if a in ("-p", "-i", "-l", "-o", "-F", "-P"):
            skip_next = True
            continue
        if a.startswith("-"):
            continue
        if "@" in a:
            return a.split("@", 1)[1].split(":", 1)[0]
        return a.split(":", 1)[0]
    return "host"


def _extract_url_host(args: list[str]) -> tuple[str, str]:
    skip_next_for: set[str] = {"-o", "-X", "-H", "-d", "-w", "--data", "--header", "--output"}
    skip_next = False
    url: str | None = None
    for a in args:
        if skip_next:
            skip_next = False
            continue
        if a in skip_next_for:
            skip_next = True
            continue
        if a.startswith("-"):
            continue
        url = a
        break
    if url is None:
        return "host", "host"
    raw = url
    if "://" in raw:
        host_part = raw.split("://", 1)[1]
    else:
        host_part = raw
    host = host_part.split("/", 1)[0].split(":", 1)[0].split("?", 1)[0]
    return raw, host or "host"


# ---------------------------------------------------------------------------
# Editors
# ---------------------------------------------------------------------------


@register("vim", "nvim", "vi")
async def cmd_vim(ctx: CommandContext) -> CommandResult:
    msg = (
        b"Vim: Warning: Output is not to a terminal\n"
        b"Vim: Warning: Input is not from a terminal\n"
    )
    return fail(1, msg)


@register("nano")
async def cmd_nano(ctx: CommandContext) -> CommandResult:
    return fail(1, b"Error opening terminal: dumb.\n")


@register("emacs")
async def cmd_emacs(ctx: CommandContext) -> CommandResult:
    return fail(1, b"emacs: standard input is not a tty\n")


# ---------------------------------------------------------------------------
# less / more — behave as cat when stdin is non-tty
# ---------------------------------------------------------------------------


@register("less", "more")
async def cmd_pager(ctx: CommandContext) -> CommandResult:
    name = ctx.name
    paths = [a for a in ctx.args if not a.startswith("-")]
    if not paths:
        return ok(ctx.stdin)
    out = bytearray()
    err_out = bytearray()
    exit_code = 0
    for path in paths:
        resolved = resolve_cwd(ctx.env, path)
        try:
            if await ctx.vfs._isdir(resolved):
                err_out.extend(encode(f"{name}: {path}: Is a directory\n"))
                exit_code = 1
                continue
            data = await ctx.vfs._cat_file(resolved)
            out.extend(data)
        except FileNotFoundError:
            err_out.extend(encode(f"{name}: {path}: No such file or directory\n"))
            exit_code = 1
        except IsADirectoryError:
            err_out.extend(encode(f"{name}: {path}: Is a directory\n"))
            exit_code = 1
        except OSError as e:
            err_out.extend(encode(f"{name}: {path}: {e.strerror or 'I/O error'}\n"))
            exit_code = 1
    return CommandResult(stdout=bytes(out), stderr=bytes(err_out), exit_code=exit_code)


# ---------------------------------------------------------------------------
# Network — unreachable / not found
# ---------------------------------------------------------------------------


@register("ssh")
async def cmd_ssh(ctx: CommandContext) -> CommandResult:
    host = _extract_host(ctx.args)
    msg = f"ssh: connect to host {host} port 22: Network is unreachable\n"
    return fail(255, encode(msg))


@register("scp")
async def cmd_scp(ctx: CommandContext) -> CommandResult:
    host = "host"
    for a in ctx.args:
        if a.startswith("-"):
            continue
        if ":" in a:
            left = a.split(":", 1)[0]
            if "@" in left:
                host = left.split("@", 1)[1]
            elif left:
                host = left
            break
    msg = (
        f"ssh: connect to host {host} port 22: Network is unreachable\n"
        f"lost connection\n"
    )
    return fail(1, encode(msg))


@register("rsync")
async def cmd_rsync(ctx: CommandContext) -> CommandResult:
    msg = (
        b"rsync: connection unexpectedly closed (0 bytes received so far) [sender]\n"
        b"rsync error: error in rsync protocol data stream (code 12) at io.c(231)"
        b" [sender=3.2.7]\n"
    )
    return fail(12, msg)


@register("curl")
async def cmd_curl(ctx: CommandContext) -> CommandResult:
    _, host = _extract_url_host(ctx.args)
    msg = f"curl: (6) Could not resolve host: {host}\n"
    return fail(6, encode(msg))


@register("wget")
async def cmd_wget(ctx: CommandContext) -> CommandResult:
    url, host = _extract_url_host(ctx.args)
    msg = (
        f"--2026-05-07 12:00:00--  {url}\n"
        f"Resolving {host} ({host})... failed: Name or service not known.\n"
        f"wget: unable to resolve host address '{host}'\n"
    )
    return fail(4, encode(msg))


@register("nc", "netcat", "telnet", "ftp")
async def cmd_net(ctx: CommandContext) -> CommandResult:
    return fail(1, encode(f"{ctx.name}: connect: Network is unreachable\n"))


@register("ping")
async def cmd_ping(ctx: CommandContext) -> CommandResult:
    host = _first_non_flag(ctx.args) or "host"
    return fail(2, encode(f"ping: {host}: Temporary failure in name resolution\n"))


# ---------------------------------------------------------------------------
# Containers / orchestration
# ---------------------------------------------------------------------------


@register("docker")
async def cmd_docker(ctx: CommandContext) -> CommandResult:
    msg = (
        b"Cannot connect to the Docker daemon at unix:///var/run/docker.sock."
        b" Is the docker daemon running?\n"
    )
    return fail(1, msg)


@register("kubectl")
async def cmd_kubectl(ctx: CommandContext) -> CommandResult:
    msg = (
        b"The connection to the server localhost:8080 was refused - did you specify"
        b" the right host or port?\n"
    )
    return fail(1, msg)


@register("podman")
async def cmd_podman(ctx: CommandContext) -> CommandResult:
    msg = (
        b"Cannot connect to Podman. Please verify your connection to the Linux system"
        b" using 'podman system connection list'\n"
    )
    return fail(125, msg)


# ---------------------------------------------------------------------------
# Build tools
# ---------------------------------------------------------------------------


@register("make")
async def cmd_make(ctx: CommandContext) -> CommandResult:
    cwd = ctx.env.cwd
    has_makefile = False
    for name in ("Makefile", "makefile"):
        candidate = resolve_cwd(ctx.env, name) if cwd != "/" else f"/{name}"
        if await ctx.vfs._isfile(candidate):
            has_makefile = True
            break
    if not has_makefile:
        return fail(2, b"make: *** No targets specified and no makefile found.  Stop.\n")
    target = _first_non_flag(ctx.args)
    if target is None:
        return ok(b"make: Nothing to be done for 'all'.\n")
    return fail(2, encode(f"make: *** No rule to make target '{target}'.  Stop.\n"))


@register("cmake", "ninja")
async def cmd_build_missing(ctx: CommandContext) -> CommandResult:
    return fail(127, encode(f"bash: {ctx.name}: command not found\n"))


# ---------------------------------------------------------------------------
# Language runtimes
# ---------------------------------------------------------------------------


@register("python", "python3", "python3.13")
async def cmd_python(ctx: CommandContext) -> CommandResult:
    args = ctx.args
    if any(a in ("--version", "-V") for a in args):
        return ok(b"Python 3.13.0\n")
    # Look for a script path argument (first non-flag, non -c value).
    i = 0
    while i < len(args):
        a = args[i]
        if a == "-c":
            return fail(127, b"bash: python: command not found\n")
        if a.startswith("-"):
            # Skip flags taking a value.
            if a in ("-m",) and i + 1 < len(args):
                i += 2
                continue
            i += 1
            continue
        # Treat as a script path.
        resolved = resolve_cwd(ctx.env, a)
        if not await ctx.vfs._isfile(resolved):
            return fail(
                2,
                encode(
                    f"python3: can't open file '{a}': [Errno 2] No such file or directory\n"
                ),
            )
        return fail(127, b"bash: python: command not found\n")
    return fail(127, b"bash: python: command not found\n")


@register("node", "nodejs")
async def cmd_node(ctx: CommandContext) -> CommandResult:
    args = ctx.args
    if any(a in ("--version", "-v") for a in args):
        return ok(b"v20.0.0\n")
    script = _first_non_flag(args)
    if script is not None:
        resolved = resolve_cwd(ctx.env, script)
        if not await ctx.vfs._isfile(resolved):
            return fail(
                1,
                encode(f"node: cannot open '{script}': No such file or directory\n"),
            )
    return fail(127, b"bash: node: command not found\n")


@register("npm", "pip", "pip3", "cargo", "go", "rustc", "gcc", "clang")
async def cmd_lang_missing(ctx: CommandContext) -> CommandResult:
    return fail(127, encode(f"bash: {ctx.name}: command not found\n"))


# ---------------------------------------------------------------------------
# TTY-only utilities
# ---------------------------------------------------------------------------


@register("htop", "top")
async def cmd_top(ctx: CommandContext) -> CommandResult:
    return fail(127, encode(f"bash: {ctx.name}: command not found\n"))
