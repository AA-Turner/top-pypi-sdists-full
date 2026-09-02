from __future__ import annotations

from matrx_ai.tools.vfs.commands.base import CommandContext, encode, fail
from matrx_ai.tools.vfs.commands.registry import register
from matrx_ai.tools.vfs.shell.runner import CommandResult


def _split_ifs(line: str, ifs: str, n_vars: int) -> list[str]:
    if n_vars <= 0:
        return []
    if not ifs:
        return [line] + [""] * (n_vars - 1) if n_vars > 1 else [line]

    # Bash semantics: whitespace IFS chars (space/tab/newline) are special;
    # they are treated as a run separator. Non-whitespace IFS chars each
    # delimit a single field. Leading/trailing whitespace IFS is stripped.
    ws = "".join(c for c in ifs if c in " \t\n")
    non_ws = "".join(c for c in ifs if c not in " \t\n")

    # Strip leading whitespace IFS.
    s = line
    if ws:
        s = s.lstrip(ws)

    fields: list[str] = []
    buf: list[str] = []
    i = 0
    while i < len(s):
        if len(fields) == n_vars - 1:
            # Last var swallows the rest verbatim (after current leading WS).
            rest = s[i:]
            if ws:
                rest = rest.rstrip(ws)
            fields.append(rest)
            return fields
        ch = s[i]
        if ch in non_ws:
            fields.append("".join(buf))
            buf = []
            i += 1
            continue
        if ws and ch in ws:
            # Run of WS IFS is a single separator.
            fields.append("".join(buf))
            buf = []
            j = i
            while j < len(s) and s[j] in ws:
                j += 1
            i = j
            continue
        buf.append(ch)
        i += 1

    if buf or fields == []:
        fields.append("".join(buf))

    while len(fields) < n_vars:
        fields.append("")
    return fields


@register("read")
async def cmd_read(ctx: CommandContext) -> CommandResult:
    args = list(ctx.args)
    prompt: str | None = None
    raw_mode = False
    silent = False
    timeout: float | None = None

    i = 0
    while i < len(args):
        a = args[i]
        if a == "-r":
            raw_mode = True
            i += 1
            continue
        if a == "-s":
            silent = True
            i += 1
            continue
        if a == "-p":
            if i + 1 >= len(args):
                return fail(2, encode("bash: read: -p: option requires an argument\n"))
            prompt = args[i + 1]
            i += 2
            continue
        if a.startswith("-p"):
            prompt = a[2:]
            i += 1
            continue
        if a == "-t":
            if i + 1 >= len(args):
                return fail(2, encode("bash: read: -t: option requires an argument\n"))
            try:
                timeout = float(args[i + 1])
            except ValueError:
                return fail(
                    1,
                    encode(f"bash: read: {args[i + 1]}: invalid timeout specification\n"),
                )
            i += 2
            continue
        if a == "--":
            i += 1
            break
        if a.startswith("-") and len(a) > 1:
            return fail(2, encode(f"bash: read: {a}: invalid option\n"))
        break

    var_names = args[i:]
    if not var_names:
        var_names = ["REPLY"]

    # In our headless model, stdin is whatever was piped. With -t, behavior
    # mirrors interactive: if no stdin provided, fail. We don't truly time out
    # during execution since we never block.
    _ = silent  # acknowledged but no terminal; nothing to suppress
    _ = raw_mode  # default behavior is already "raw" — no escape processing

    if not ctx.stdin:
        if timeout is not None:
            return fail(142)  # bash uses 142 for read-timeout
        return fail(1)

    # Take the first line (split on \n). Decode as UTF-8 with surrogate escape.
    data = ctx.stdin
    nl = data.find(b"\n")
    if nl >= 0:
        line_bytes = data[:nl]
    else:
        line_bytes = data
    line = line_bytes.decode("utf-8", errors="surrogateescape")

    stderr_out = b""
    if prompt is not None:
        stderr_out = encode(prompt)

    ifs = ctx.env.ifs
    fields = _split_ifs(line, ifs, len(var_names))

    for name, value in zip(var_names, fields, strict=False):
        ctx.env.set(name, value)

    return CommandResult(stdout=b"", stderr=stderr_out, exit_code=0)
