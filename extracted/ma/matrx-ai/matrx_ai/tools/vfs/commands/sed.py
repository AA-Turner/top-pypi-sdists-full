from __future__ import annotations

import re
from dataclasses import dataclass, field

from matrx_ai.tools.vfs.commands.base import CommandContext, encode, fail, ok, resolve_cwd
from matrx_ai.tools.vfs.commands.registry import register
from matrx_ai.tools.vfs.mimicry import sed_no_file
from matrx_ai.tools.vfs.shell.runner import CommandResult


@dataclass(slots=True)
class _Address:
    kind: str  # 'num', 'last', 'regex', 'step'
    num: int | None = None
    step: int | None = None
    pattern: re.Pattern[str] | None = None


@dataclass(slots=True)
class _SedCmd:
    addr1: _Address | None = None
    addr2: _Address | None = None
    cmd: str = ""
    # for substitute:
    s_pattern: re.Pattern[str] | None = None
    s_repl: str = ""
    s_global: bool = False
    s_print: bool = False
    s_nth: int | None = None


@dataclass(slots=True)
class _Opts:
    quiet: bool = False
    extended: bool = False
    in_place: bool = False
    in_place_suffix: str = ""
    scripts: list[str] = field(default_factory=list)
    files: list[str] = field(default_factory=list)


def _err(msg: str) -> bytes:
    return encode(f"sed: {msg}\n")


def _parse_args(args: list[str]) -> tuple[_Opts, CommandResult | None]:
    opts = _Opts()
    have_script = False
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--":
            opts.files.extend(args[i + 1 :])
            break
        if a == "-":
            opts.files.append(a)
            i += 1
            continue
        if a.startswith("--"):
            name, has_eq, value = a[2:].partition("=")
            if name == "quiet" or name == "silent":
                opts.quiet = True
            elif name == "regexp-extended":
                opts.extended = True
            elif name == "expression":
                if not has_eq:
                    if i + 1 >= len(args):
                        return opts, fail(1, _err("option requires an argument"))
                    i += 1
                    value = args[i]
                opts.scripts.append(value)
                have_script = True
            elif name == "in-place":
                opts.in_place = True
                opts.in_place_suffix = value if has_eq else ""
            else:
                return opts, fail(1, _err(f"unrecognized option '--{name}'"))
            i += 1
            continue
        if a.startswith("-") and len(a) > 1:
            j = 1
            consumed = False
            while j < len(a):
                letter = a[j]
                if letter == "n":
                    opts.quiet = True
                    j += 1
                elif letter == "E" or letter == "r":
                    opts.extended = True
                    j += 1
                elif letter == "e":
                    inline = a[j + 1 :]
                    if inline:
                        opts.scripts.append(inline)
                        j = len(a)
                    else:
                        if i + 1 >= len(args):
                            return opts, fail(1, _err("option requires an argument -- 'e'"))
                        i += 1
                        opts.scripts.append(args[i])
                        consumed = True
                        j = len(a)
                    have_script = True
                elif letter == "i":
                    opts.in_place = True
                    inline = a[j + 1 :]
                    opts.in_place_suffix = inline
                    j = len(a)
                else:
                    return opts, fail(1, _err(f"invalid option -- '{letter}'"))
            i += 1
            _ = consumed
            continue
        if not have_script:
            opts.scripts.append(a)
            have_script = True
            i += 1
            continue
        opts.files.append(a)
        i += 1

    if not have_script:
        return opts, fail(1, _err("no script given"))
    return opts, None


def _parse_address(text: str, pos: int, extended: bool) -> tuple[_Address | None, int]:
    n = len(text)
    if pos >= n:
        return None, pos
    ch = text[pos]
    if ch == "$":
        return _Address(kind="last"), pos + 1
    if ch == "/":
        # /regex/
        end = pos + 1
        while end < n:
            if text[end] == "\\" and end + 1 < n:
                end += 2
                continue
            if text[end] == "/":
                break
            end += 1
        if end >= n:
            return None, pos  # unterminated
        pat_text = text[pos + 1 : end]
        # Unescape \/ to /
        pat_text = pat_text.replace("\\/", "/")
        try:
            pat = re.compile(pat_text)
        except re.error:
            return None, pos
        _ = extended  # python re always uses ERE-ish
        return _Address(kind="regex", pattern=pat), end + 1
    if ch.isdigit():
        end = pos
        while end < n and text[end].isdigit():
            end += 1
        num = int(text[pos:end])
        if end < n and text[end] == "~":
            # num~step
            step_start = end + 1
            sp_end = step_start
            while sp_end < n and text[sp_end].isdigit():
                sp_end += 1
            if sp_end > step_start:
                step = int(text[step_start:sp_end])
                return _Address(kind="step", num=num, step=step), sp_end
        return _Address(kind="num", num=num), end
    return None, pos


def _split_script_into_commands(script: str) -> list[str]:
    # Split at top-level ';' and '\n'. Inside s/.../.../FLAGS, watch the delimiter.
    out: list[str] = []
    buf: list[str] = []
    i = 0
    n = len(script)
    while i < n:
        ch = script[i]
        if ch in (";", "\n"):
            cmd = "".join(buf).strip()
            if cmd:
                out.append(cmd)
            buf = []
            i += 1
            continue
        if ch == "s" and (not buf or buf[-1] in ("", " ", "\t")) and i + 1 < n:
            # Heuristic: if 's' starts a substitute command, parse the s/PAT/REPL/FLAGS
            # to consume up to the third delimiter, then continue.
            # We only treat as substitute when not preceded by an alphabetic char
            # (so it's a command rather than a partial token).
            # Actually, we need to handle addresses that come BEFORE s. So instead
            # of detecting s-start here, just push the char and rely on the s-parser
            # to know its delimiter.
            buf.append(ch)
            i += 1
            continue
        buf.append(ch)
        i += 1
    if buf:
        cmd = "".join(buf).strip()
        if cmd:
            out.append(cmd)
    return out


def _parse_substitute(rest: str, extended: bool) -> tuple[_SedCmd, bool]:
    # rest starts with the delimiter, e.g. "/pat/repl/flags"
    if not rest:
        return _SedCmd(), False
    delim = rest[0]
    # Find pat — up to next unescaped delim
    i = 1
    pat_start = i
    n = len(rest)
    while i < n:
        if rest[i] == "\\" and i + 1 < n:
            i += 2
            continue
        if rest[i] == delim:
            break
        i += 1
    if i >= n:
        return _SedCmd(), False
    pat_text = rest[pat_start:i]
    # Find repl
    i += 1
    repl_start = i
    while i < n:
        if rest[i] == "\\" and i + 1 < n:
            i += 2
            continue
        if rest[i] == delim:
            break
        i += 1
    if i >= n:
        return _SedCmd(), False
    repl_text = rest[repl_start:i]
    # Flags
    i += 1
    flags = rest[i:]
    s = _SedCmd(cmd="s")
    # Unescape \<delim> in pattern
    pat_text = pat_text.replace(f"\\{delim}", delim)
    repl_text = repl_text.replace(f"\\{delim}", delim)
    try:
        # Always use Python regex; -E gives ERE which is similar.
        s.s_pattern = re.compile(pat_text)
    except re.error:
        return _SedCmd(), False
    _ = extended
    # Convert sed backrefs \1..\9 to Python \g<1>...\g<9>; pass others through.
    s.s_repl = _convert_repl(repl_text)
    j = 0
    while j < len(flags):
        c = flags[j]
        if c == "g":
            s.s_global = True
        elif c == "p":
            s.s_print = True
        elif c.isdigit():
            num_end = j
            while num_end < len(flags) and flags[num_end].isdigit():
                num_end += 1
            s.s_nth = int(flags[j:num_end])
            j = num_end
            continue
        elif c.isspace():
            pass
        else:
            return _SedCmd(), False
        j += 1
    return s, True


def _convert_repl(repl: str) -> str:
    out: list[str] = []
    i = 0
    n = len(repl)
    while i < n:
        c = repl[i]
        if c == "\\" and i + 1 < n:
            nxt = repl[i + 1]
            if nxt.isdigit():
                out.append(f"\\g<{nxt}>")
                i += 2
                continue
            if nxt == "n":
                out.append("\n")
                i += 2
                continue
            if nxt == "t":
                out.append("\t")
                i += 2
                continue
            if nxt == "\\":
                out.append("\\\\")
                i += 2
                continue
            if nxt == "&":
                out.append("&")
                i += 2
                continue
            out.append(nxt)
            i += 2
            continue
        if c == "&":
            out.append("\\g<0>")
            i += 1
            continue
        if c == "\\":
            out.append("\\\\")
            i += 1
            continue
        out.append(c)
        i += 1
    return "".join(out)


def _parse_command(text: str, extended: bool) -> tuple[_SedCmd | None, str | None]:
    # text is one command string. May start with optional addresses.
    s = text.strip()
    if not s:
        return None, None
    addr1, pos = _parse_address(s, 0, extended)
    if addr1 is None and s[0] not in ("=", "p", "d", "q", "n", "P", "D"):
        # Some forms — try parsing the command without an address.
        pos = 0
    addr2: _Address | None = None
    if addr1 is not None and pos < len(s) and s[pos] == ",":
        addr2, pos = _parse_address(s, pos + 1, extended)
        if addr2 is None:
            return None, "unterminated address"
    while pos < len(s) and s[pos] in (" ", "\t"):
        pos += 1
    if pos >= len(s):
        return None, "missing command"
    letter = s[pos]
    cmd = _SedCmd(addr1=addr1, addr2=addr2, cmd=letter)
    if letter == "s":
        sub, okflag = _parse_substitute(s[pos + 1 :], extended)
        if not okflag:
            return None, "unterminated 's' command"
        cmd.s_pattern = sub.s_pattern
        cmd.s_repl = sub.s_repl
        cmd.s_global = sub.s_global
        cmd.s_print = sub.s_print
        cmd.s_nth = sub.s_nth
        return cmd, None
    if letter in ("d", "p", "q", "=", "n"):
        return cmd, None
    return None, f"unknown command '{letter}'"


def _addr_matches(addr: _Address, lineno: int, total: int, line: str) -> bool:
    if addr.kind == "num":
        return addr.num == lineno
    if addr.kind == "last":
        return lineno == total
    if addr.kind == "regex":
        assert addr.pattern is not None
        return bool(addr.pattern.search(line))
    if addr.kind == "step":
        assert addr.num is not None and addr.step is not None
        if lineno < addr.num:
            return False
        return (lineno - addr.num) % addr.step == 0
    return False


def _cmd_applies(
    cmd: _SedCmd,
    lineno: int,
    total: int,
    line: str,
    range_state: dict[int, bool],
    cmd_idx: int,
) -> bool:
    if cmd.addr1 is None:
        return True
    if cmd.addr2 is None:
        return _addr_matches(cmd.addr1, lineno, total, line)
    # range mode
    in_range = range_state.get(cmd_idx, False)
    if not in_range:
        if _addr_matches(cmd.addr1, lineno, total, line):
            range_state[cmd_idx] = True
            in_range = True
    if in_range:
        if _addr_matches(cmd.addr2, lineno, total, line):
            # final line of range
            range_state[cmd_idx] = False
        return True
    return False


def _apply_substitute(line: str, cmd: _SedCmd) -> tuple[str, bool]:
    assert cmd.s_pattern is not None
    if cmd.s_global:
        new, count = cmd.s_pattern.subn(cmd.s_repl, line)
        return new, count > 0
    if cmd.s_nth is not None:
        # Replace only the Nth match
        n_target = cmd.s_nth
        counter = {"i": 0}

        def _repl(m: re.Match[str]) -> str:
            counter["i"] += 1
            if counter["i"] == n_target:
                return m.expand(cmd.s_repl)
            return m.group(0)

        new = cmd.s_pattern.sub(_repl, line)
        return new, counter["i"] >= n_target
    new, count = cmd.s_pattern.subn(cmd.s_repl, line, count=1)
    return new, count > 0


def _run_script(commands: list[_SedCmd], lines: list[str], opts: _Opts) -> str:
    out: list[str] = []
    total = len(lines)
    range_state: dict[int, bool] = {}
    for idx, line in enumerate(lines):
        lineno = idx + 1
        pattern_space = line
        deleted = False
        quit_after = False
        for ci, cmd in enumerate(commands):
            if not _cmd_applies(cmd, lineno, total, pattern_space, range_state, ci):
                continue
            if cmd.cmd == "s":
                new, did = _apply_substitute(pattern_space, cmd)
                pattern_space = new
                if did and cmd.s_print:
                    out.append(pattern_space + "\n")
            elif cmd.cmd == "d":
                deleted = True
                break
            elif cmd.cmd == "p":
                out.append(pattern_space + "\n")
            elif cmd.cmd == "q":
                quit_after = True
            elif cmd.cmd == "=":
                out.append(f"{lineno}\n")
            elif cmd.cmd == "n":
                # auto-print and load next line — minimal version: print pattern space
                if not opts.quiet:
                    out.append(pattern_space + "\n")
                # We are in for-loop over lines; "n" semantics need a different
                # control flow. Here we approximate by printing and continuing.
                pattern_space = line
        if deleted:
            continue
        if not opts.quiet:
            out.append(pattern_space + "\n")
        if quit_after:
            break
    return "".join(out)


def _compile_scripts(scripts: list[str], extended: bool) -> tuple[list[_SedCmd], str | None]:
    cmds: list[_SedCmd] = []
    for script in scripts:
        for piece in _split_script_into_commands(script):
            cmd, err_msg = _parse_command(piece, extended)
            if err_msg is not None:
                return [], err_msg
            if cmd is not None:
                cmds.append(cmd)
    return cmds, None


def _split_input_lines(data: bytes) -> tuple[list[str], bool]:
    if not data:
        return [], False
    text = data.decode("latin-1")
    ends_in_nl = text.endswith("\n")
    if ends_in_nl:
        text = text[:-1]
    return text.split("\n"), ends_in_nl


@register("sed")
async def cmd_sed(ctx: CommandContext) -> CommandResult:
    opts, err = _parse_args(ctx.args)
    if err is not None:
        return err

    cmds, msg = _compile_scripts(opts.scripts, opts.extended)
    if msg is not None:
        return fail(1, _err(f"-e expression #1, char 0: {msg}"))

    if opts.in_place and not opts.files:
        return fail(1, _err("-i may not be used with stdin"))

    if not opts.files:
        lines, _ = _split_input_lines(ctx.stdin)
        out_text = _run_script(cmds, lines, opts)
        return ok(out_text.encode("latin-1"))

    err_out = bytearray()
    out = bytearray()
    exit_code = 0
    for path in opts.files:
        if path == "-":
            data = ctx.stdin
        else:
            resolved = resolve_cwd(ctx.env, path)
            try:
                data = await ctx.vfs._cat_file(resolved)
            except FileNotFoundError:
                err_out.extend(encode(sed_no_file(path)))
                exit_code = 2
                continue
            except OSError as exc:
                err_out.extend(encode(f"sed: can't read {path}: {exc.strerror or 'I/O error'}\n"))
                exit_code = 2
                continue
        lines, _nl = _split_input_lines(data)
        result_text = _run_script(cmds, lines, opts)
        if opts.in_place and path != "-":
            resolved = resolve_cwd(ctx.env, path)
            if opts.in_place_suffix:
                backup_path = resolved + opts.in_place_suffix
                await ctx.vfs._pipe_file(backup_path, data)
            await ctx.vfs._pipe_file(resolved, result_text.encode("latin-1"))
            continue
        out.extend(result_text.encode("latin-1"))
    return CommandResult(stdout=bytes(out), stderr=bytes(err_out), exit_code=exit_code)
