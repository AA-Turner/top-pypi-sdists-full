from __future__ import annotations

from matrx_ai.tools.vfs.commands.base import CommandContext, encode, fail, ok
from matrx_ai.tools.vfs.commands.registry import register
from matrx_ai.tools.vfs.shell.runner import CommandResult

# Synthetic process table — stable across invocations so tests can assert.
_FAKE_PROCESSES: list[dict[str, object]] = [
    {"pid": 1, "ppid": 0, "user": "root", "tty": "?", "time": "00:00:00", "cmd": "/sbin/init"},
    {"pid": 2, "ppid": 0, "user": "root", "tty": "?", "time": "00:00:00", "cmd": "[kthreadd]"},
]

# Signals supported by `kill -l`. Order matches typical bash output.
_SIGNALS: tuple[tuple[int, str], ...] = (
    (1, "HUP"),
    (2, "INT"),
    (3, "QUIT"),
    (9, "KILL"),
    (15, "TERM"),
    (17, "STOP"),
    (18, "CONT"),
)

_SIGNAL_BY_NAME: dict[str, int] = {name: num for num, name in _SIGNALS}
_SIGNAL_BY_NUM: dict[int, str] = {num: name for num, name in _SIGNALS}


def _shell_process(env_pid: int) -> dict[str, object]:
    return {
        "pid": env_pid,
        "ppid": 1,
        "user": "user",
        "tty": "pts/0",
        "time": "00:00:00",
        "cmd": "bash",
    }


def _process_table(env_pid: int) -> list[dict[str, object]]:
    return _FAKE_PROCESSES + [_shell_process(env_pid)]


def _format_default(procs: list[dict[str, object]]) -> bytes:
    out = bytearray()
    out.extend(b"  PID TTY          TIME CMD\n")
    for p in procs:
        out.extend(encode(f"{int(p['pid']):>5} {str(p['tty']):<8} {p['time']} {p['cmd']}\n"))
    return bytes(out)


def _format_full(procs: list[dict[str, object]]) -> bytes:
    out = bytearray()
    out.extend(b"UID          PID    PPID  C STIME TTY          TIME CMD\n")
    for p in procs:
        out.extend(
            encode(
                f"{str(p['user']):<12} {int(p['pid']):>4} {int(p['ppid']):>7}"
                f"  0 00:00 {str(p['tty']):<8} {p['time']} {p['cmd']}\n"
            )
        )
    return bytes(out)


def _format_aux(procs: list[dict[str, object]]) -> bytes:
    out = bytearray()
    out.extend(b"USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND\n")
    for p in procs:
        out.extend(
            encode(
                f"{str(p['user']):<12} {int(p['pid']):>4}  0.0  0.0   1234   567 "
                f"{str(p['tty']):<8} Ss   00:00   {p['time']} {p['cmd']}\n"
            )
        )
    return bytes(out)


def _parse_ps_args(args: list[str]) -> tuple[str, set[int] | None, CommandResult | None]:
    # Returns (format, pid_filter_or_None, error_or_None).
    fmt = "default"
    pid_filter: set[int] | None = None

    i = 0
    while i < len(args):
        a = args[i]
        # BSD-style: `aux` is a single argument (no leading dash).
        if a == "aux":
            fmt = "aux"
            i += 1
            continue
        if a == "ax" or a == "ef":
            fmt = "full"
            i += 1
            continue
        if a == "-p" or a == "p":
            if i + 1 >= len(args):
                return (
                    fmt,
                    pid_filter,
                    fail(
                        1,
                        encode("error: list of process IDs must follow -p\n"),
                    ),
                )
            try:
                pid_filter = {int(x) for x in args[i + 1].replace(",", " ").split()}
            except ValueError:
                return (
                    fmt,
                    pid_filter,
                    fail(
                        1,
                        encode("error: invalid PID list\n"),
                    ),
                )
            i += 2
            continue
        if a.startswith("-"):
            body = a[1:]
            if body == "e" or body == "A":
                fmt = "default" if fmt == "default" else fmt
                i += 1
                continue
            if body == "ef":
                fmt = "full"
                i += 1
                continue
            if body == "f":
                fmt = "full"
                i += 1
                continue
            # Unknown flag: ignore silently for robustness.
            i += 1
            continue
        i += 1

    return fmt, pid_filter, None


@register("ps")
async def cmd_ps(ctx: CommandContext) -> CommandResult:
    fmt, pid_filter, err = _parse_ps_args(list(ctx.args))
    if err is not None:
        return err

    procs = _process_table(ctx.env.pid)
    if pid_filter is not None:
        procs = [p for p in procs if int(p["pid"]) in pid_filter]
        if not procs:
            return fail(1)

    if fmt == "full":
        return ok(_format_full(procs))
    if fmt == "aux":
        return ok(_format_aux(procs))
    return ok(_format_default(procs))


def _resolve_signal(spec: str) -> int | None:
    # Accepts: "9", "KILL", "SIGKILL".
    if spec.isdigit():
        return int(spec)
    name = spec.upper()
    if name.startswith("SIG"):
        name = name[3:]
    if name in _SIGNAL_BY_NAME:
        return _SIGNAL_BY_NAME[name]
    return None


@register("kill")
async def cmd_kill(ctx: CommandContext) -> CommandResult:
    args = list(ctx.args)

    if not args:
        return fail(
            2,
            encode(
                "kill: usage: kill [-s sigspec | -n signum | -sigspec] pid | jobspec ... "
                "or kill -l [sigspec]\n"
            ),
        )

    if args[0] == "-l":
        out = bytearray()
        rest = args[1:]
        if not rest:
            for num, name in _SIGNALS:
                out.extend(encode(f"{num}) SIG{name}\t"))
            if out and out[-1] == 0x09:
                out[-1] = 0x0A
            else:
                out.extend(b"\n")
            return ok(bytes(out))
        # `kill -l NAME` or `kill -l NUM` — translate.
        for token in rest:
            sig = _resolve_signal(token)
            if sig is None:
                return fail(1, encode(f"bash: kill: {token}: invalid signal specification\n"))
            if token.isdigit():
                name = _SIGNAL_BY_NUM.get(int(token))
                if name is None:
                    return fail(1, encode(f"bash: kill: {token}: invalid signal specification\n"))
                out.extend(encode(f"{name}\n"))
            else:
                out.extend(encode(f"{sig}\n"))
        return ok(bytes(out))

    # Optional -SIG / -s SIG / -n NUM / -0
    signal_num: int | None = None
    i = 0
    if args[0] == "-s":
        if len(args) < 2:
            return fail(1, encode("bash: kill: -s: option requires an argument\n"))
        sig = _resolve_signal(args[1])
        if sig is None:
            return fail(1, encode(f"bash: kill: {args[1]}: invalid signal specification\n"))
        signal_num = sig
        i = 2
    elif args[0] == "-n":
        if len(args) < 2:
            return fail(1, encode("bash: kill: -n: option requires an argument\n"))
        sig = _resolve_signal(args[1])
        if sig is None:
            return fail(1, encode(f"bash: kill: {args[1]}: invalid signal specification\n"))
        signal_num = sig
        i = 2
    elif args[0].startswith("-") and len(args[0]) > 1:
        sig = _resolve_signal(args[0][1:])
        if sig is None:
            return fail(1, encode(f"bash: kill: {args[0][1:]}: invalid signal specification\n"))
        signal_num = sig
        i = 1

    if i >= len(args):
        return fail(2, encode("kill: usage: kill [-sigspec] pid ...\n"))

    procs = _process_table(ctx.env.pid)
    valid_pids = {int(p["pid"]) for p in procs}

    err_out = bytearray()
    exit_code = 0

    for token in args[i:]:
        try:
            pid = int(token)
        except ValueError:
            err_out.extend(encode(f"bash: kill: {token}: arguments must be process or job IDs\n"))
            exit_code = 1
            continue
        if signal_num == 0:
            # `kill -0`: just probe — we don't model real liveness, so treat
            # any unknown PID as failure.
            if pid not in valid_pids:
                err_out.extend(encode(f"bash: kill: ({pid}) - No such process\n"))
                exit_code = 1
            continue
        if pid not in valid_pids:
            err_out.extend(encode(f"bash: kill: ({pid}) - No such process\n"))
            exit_code = 1
            continue
        if pid == 1:
            err_out.extend(encode(f"bash: kill: ({pid}) - Operation not permitted\n"))
            exit_code = 1
            continue
        # Otherwise: pretend success.

    return CommandResult(stdout=b"", stderr=bytes(err_out), exit_code=exit_code)
