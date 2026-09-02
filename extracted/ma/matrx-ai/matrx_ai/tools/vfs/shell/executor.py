from __future__ import annotations

from typing import TYPE_CHECKING

from .ast import (
    AndOrList,
    CommandList,
    Pipeline,
    Redirect,
    SimpleCommand,
    Subshell,
    Word,
)
from .expansion import ShellExpansionError, expand_word
from .runner import CommandResult

if TYPE_CHECKING:
    from .env import ShellEnv
    from .runner import CommandRunner


class _Captured:
    __slots__ = ("stdout", "stderr")

    def __init__(self) -> None:
        self.stdout: list[bytes] = []
        self.stderr: list[bytes] = []


async def execute(
    node: CommandList,
    env: ShellEnv,
    runner: CommandRunner,
    *,
    capture: bool = False,
) -> CommandResult:
    captured = _Captured() if capture else None
    last = CommandResult(b"", b"", env.last_exit)
    for i, andor in enumerate(node.items):
        sep = node.separators[i] if i < len(node.separators) else "\n"
        if sep == "&":
            # Background — fake bg pid, run synchronously, ignore result for
            # the foreground continuation.
            env.last_bg_pid += 1
            res = await _run_andor(andor, env, runner, captured)
            last = res
            env.last_exit = 0  # backgrounded commands return 0 for &
        else:
            res = await _run_andor(andor, env, runner, captured)
            last = res
            env.last_exit = res.exit_code
            if env.shell_opts.get("errexit") and res.exit_code != 0:
                break

    if captured is not None:
        return CommandResult(
            stdout=b"".join(captured.stdout),
            stderr=b"".join(captured.stderr),
            exit_code=last.exit_code,
        )
    return last


async def _run_andor(
    andor: AndOrList,
    env: ShellEnv,
    runner: CommandRunner,
    captured: _Captured | None,
) -> CommandResult:
    result = await _run_pipeline(andor.pipelines[0], env, runner, captured)
    for pipeline, op in zip(andor.pipelines[1:], andor.operators, strict=True):
        if op == "&&" and result.exit_code != 0:
            continue
        if op == "||" and result.exit_code == 0:
            continue
        result = await _run_pipeline(pipeline, env, runner, captured)
    return result


async def _run_pipeline(
    pipeline: Pipeline,
    env: ShellEnv,
    runner: CommandRunner,
    captured: _Captured | None,
) -> CommandResult:
    stdin = b""
    results: list[CommandResult] = []
    n = len(pipeline.commands)
    for i, cmd in enumerate(pipeline.commands):
        is_last = i == n - 1
        # Capture stdout for non-last stages so we can pipe.
        # For the last stage, only capture if our caller wanted it.
        cap_this = (not is_last) or (captured is not None)
        result = await _run_command(
            cmd,
            env,
            runner,
            stdin=stdin,
            capture_stdout=cap_this,
        )
        results.append(result)
        if not is_last:
            stdin = result.stdout

    last = results[-1]

    # Pipefail: first non-zero exit wins; otherwise last exit.
    if env.shell_opts.get("pipefail", False):
        exit_code = 0
        for r in results:
            if r.exit_code != 0:
                exit_code = r.exit_code
                break
    else:
        exit_code = last.exit_code

    if pipeline.negated:
        exit_code = 0 if exit_code != 0 else 1

    if captured is not None:
        captured.stdout.append(last.stdout)
        for r in results:
            captured.stderr.append(r.stderr)
    return CommandResult(
        stdout=last.stdout if captured is not None else b"",
        stderr=b"",
        exit_code=exit_code,
    )


async def _run_command(
    cmd: SimpleCommand | Subshell,
    env: ShellEnv,
    runner: CommandRunner,
    *,
    stdin: bytes,
    capture_stdout: bool,
) -> CommandResult:
    if isinstance(cmd, Subshell):
        return await _run_subshell(cmd, env, runner, stdin=stdin)
    return await _run_simple_command(cmd, env, runner, stdin=stdin, capture_stdout=capture_stdout)


async def _run_subshell(
    sh: Subshell,
    env: ShellEnv,
    runner: CommandRunner,
    *,
    stdin: bytes,
) -> CommandResult:
    sub_env = env.copy()
    # Apply redirects on the subshell as a whole — for simplicity we run the
    # body capturing, then route to the redirect targets afterwards.
    body_res = await execute(sh.body, sub_env, runner, capture=True)
    env.last_bg_pid = sub_env.last_bg_pid
    stdout = body_res.stdout
    stderr = body_res.stderr
    if sh.redirects:
        try:
            stdout, stderr = await _apply_output_redirects(
                sh.redirects, stdout, stderr, sub_env, runner
            )
        except OSError as e:
            return CommandResult(
                stdout=b"",
                stderr=f"{e.strerror or str(e)}\n".encode(),
                exit_code=1,
            )
    return CommandResult(stdout=stdout, stderr=stderr, exit_code=body_res.exit_code)


async def _run_simple_command(
    cmd: SimpleCommand,
    env: ShellEnv,
    runner: CommandRunner,
    *,
    stdin: bytes,
    capture_stdout: bool,
) -> CommandResult:
    # 1. Evaluate assignments.
    assignment_values: list[tuple[str, str]] = []
    try:
        for name, word in cmd.assignments:
            vals = await expand_word(word, env, runner, for_assignment=True)
            assignment_values.append((name, vals[0] if vals else ""))
    except ShellExpansionError as e:
        return CommandResult(b"", f"{e}\n".encode(), 1)

    if not cmd.argv:
        # Assignment-only command: persist into env.
        for name, value in assignment_values:
            env.set(name, value)
        # Process redirects (e.g. `> file` alone): truncate target.
        try:
            for r in cmd.redirects:
                await _apply_redirect_sideeffect(r, env, runner)
        except OSError as e:
            return CommandResult(b"", f"{e.strerror or str(e)}\n".encode(), 1)
        return CommandResult(b"", b"", 0)

    # 2. Expand argv.
    try:
        argv_strs: list[str] = []
        for w in cmd.argv:
            # Brace expansion first (textual).
            for braced in _brace_expand_word(w):
                expanded = await expand_word(braced, env, runner)
                argv_strs.extend(expanded)
    except ShellExpansionError as e:
        return CommandResult(b"", f"{e}\n".encode(), 1)

    if not argv_strs:
        # All argv expanded to empty (rare). Treat as empty command.
        return CommandResult(b"", b"", 0)

    # 3. Resolve redirects: build a transient env for the command (assignments
    # are scoped to this command unless `export` is used).
    cmd_env = env.copy()
    for name, value in assignment_values:
        cmd_env.set(name, value, export=True)

    # Input redirects: < file or <<< word or << heredoc
    actual_stdin = stdin
    try:
        for r in cmd.redirects:
            if r.op in ("<", "<<<", "<<", "<<-"):
                actual_stdin = await _resolve_input_redirect(r, cmd_env, runner)
    except OSError as e:
        return CommandResult(b"", f"{e.strerror or str(e)}\n".encode(), 1)
    except ShellExpansionError as e:
        return CommandResult(b"", f"{e}\n".encode(), 1)

    # 4. Run.
    result = await runner.run(argv_strs, cmd_env, actual_stdin, cmd_env.cwd)

    # Standardize "command not found" messaging if runner returned 127 with
    # no stderr.
    if result.exit_code == 127 and not result.stderr:
        msg = f"{env.script_name}: {argv_strs[0]}: command not found\n"
        result = CommandResult(stdout=result.stdout, stderr=msg.encode(), exit_code=127)

    # 5. Output redirects.
    if any(r.op in (">", ">>", "2>", "2>>", "&>", "&>>") for r in cmd.redirects):
        try:
            new_out, new_err = await _apply_output_redirects(
                cmd.redirects, result.stdout, result.stderr, cmd_env, runner
            )
            result = CommandResult(stdout=new_out, stderr=new_err, exit_code=result.exit_code)
        except OSError as e:
            return CommandResult(b"", f"{e.strerror or str(e)}\n".encode(), 1)
        except ShellExpansionError as e:
            return CommandResult(b"", f"{e}\n".encode(), 1)

    if not capture_stdout:
        # If our caller doesn't want the stdout, drop it (already consumed by
        # any > redirect).
        result = CommandResult(stdout=b"", stderr=result.stderr, exit_code=result.exit_code)
    return result


async def _resolve_input_redirect(r: Redirect, env: ShellEnv, runner: CommandRunner) -> bytes:
    if r.op == "<":
        path = await _redir_target_path(r, env, runner)
        return await runner.read_file(path, env)
    if r.op == "<<<":
        # here-string
        text = await _redir_target_path(r, env, runner)
        return (text + "\n").encode("utf-8")
    if r.op in ("<<", "<<-"):
        body = r.heredoc_body or ""
        if r.heredoc_expand and not r.heredoc_quoted:
            body = await _expand_heredoc_body(body, env, runner)
        return body.encode("utf-8")
    return b""


async def _expand_heredoc_body(body: str, env: ShellEnv, runner: CommandRunner) -> str:
    # Heredoc bodies expand $VAR, $(...), `...` but not glob and not splitting.
    # We reuse the parser by wrapping body in a synthesized double-quoted
    # word would lose newlines; instead do a focused inline pass.
    from .parser import parse as _parse  # noqa: PLC0415

    out: list[str] = []
    i = 0
    n = len(body)
    while i < n:
        ch = body[i]
        if ch == "\\" and i + 1 < n and body[i + 1] in ('"', "$", "`", "\\", "\n"):
            if body[i + 1] == "\n":
                i += 2
                continue
            out.append(body[i + 1])
            i += 2
            continue
        if ch == "$":
            seg, end = _extract_dollar(body, i)
            if seg is None:
                out.append(ch)
                i += 1
                continue
            if seg.startswith("$((") and seg.endswith("))"):
                from .expansion import _eval_arith  # noqa: PLC0415

                out.append(str(_eval_arith(seg[3:-2], env)))
            elif seg.startswith("$(") and seg.endswith(")"):
                cl = _parse(seg[2:-1])
                res = await execute(cl, env, runner, capture=True)
                out.append(res.stdout.decode("utf-8", errors="replace").rstrip("\n"))
            elif seg.startswith("${") and seg.endswith("}"):
                from .parser import _parse_brace_var  # noqa: PLC0415

                wp = _parse_brace_var(seg[2:-1])
                if hasattr(wp, "name"):
                    from .expansion import _expand_var  # noqa: PLC0415

                    out.append(_expand_var(wp, env))  # type: ignore[arg-type]
                else:
                    out.append(seg)
            elif seg.startswith("$") and len(seg) >= 2:
                from .ast import VarPart  # noqa: PLC0415
                from .expansion import _expand_var  # noqa: PLC0415

                out.append(_expand_var(VarPart(name=seg[1:], mode="plain"), env))
            else:
                out.append(seg)
            i = end
            continue
        if ch == "`":
            end = i + 1
            while end < n:
                if body[end] == "\\" and end + 1 < n:
                    end += 2
                    continue
                if body[end] == "`":
                    break
                end += 1
            if end < n:
                cl = _parse(body[i + 1 : end])
                res = await execute(cl, env, runner, capture=True)
                out.append(res.stdout.decode("utf-8", errors="replace").rstrip("\n"))
                i = end + 1
                continue
            out.append(ch)
            i += 1
            continue
        out.append(ch)
        i += 1
    return "".join(out)


def _extract_dollar(text: str, start: int) -> tuple[str | None, int]:
    n = len(text)
    if start + 1 >= n:
        return None, start + 1
    nxt = text[start + 1]
    if nxt == "(":
        if start + 2 < n and text[start + 2] == "(":
            depth = 2
            i = start + 3
            while i < n and depth:
                c = text[i]
                if c == "(":
                    depth += 1
                elif c == ")":
                    depth -= 1
                    if depth == 0:
                        return text[start : i + 1], i + 1
                i += 1
            return None, n
        depth = 1
        i = start + 2
        while i < n and depth:
            c = text[i]
            if c == "(":
                depth += 1
            elif c == ")":
                depth -= 1
                if depth == 0:
                    return text[start : i + 1], i + 1
            i += 1
        return None, n
    if nxt == "{":
        depth = 1
        i = start + 2
        while i < n and depth:
            c = text[i]
            if c == "{":
                depth += 1
            elif c == "}":
                depth -= 1
                if depth == 0:
                    return text[start : i + 1], i + 1
            i += 1
        return None, n
    if nxt.isalpha() or nxt == "_":
        i = start + 2
        while i < n and (text[i].isalnum() or text[i] == "_"):
            i += 1
        return text[start:i], i
    if nxt.isdigit() or nxt in "?$!#@*-":
        return text[start : start + 2], start + 2
    return None, start + 1


async def _redir_target_path(r: Redirect, env: ShellEnv, runner: CommandRunner) -> str:
    if r.target is None:
        raise OSError("redirect missing target")
    vals = await expand_word(r.target, env, runner, for_redirect=True)
    if not vals:
        raise OSError("redirect target expanded to empty")
    if len(vals) > 1:
        raise OSError(f"ambiguous redirect: {' '.join(vals)}")
    return vals[0]


async def _apply_output_redirects(
    redirects: list[Redirect],
    stdout: bytes,
    stderr: bytes,
    env: ShellEnv,
    runner: CommandRunner,
) -> tuple[bytes, bytes]:
    new_stdout = stdout
    new_stderr = stderr
    for r in redirects:
        if r.op in (">", ">>"):
            path = await _redir_target_path(r, env, runner)
            data = new_stdout
            await runner.write_file(path, data, env, append=(r.op == ">>"))
            new_stdout = b""
        elif r.op in ("2>", "2>>"):
            path = await _redir_target_path(r, env, runner)
            await runner.write_file(path, new_stderr, env, append=(r.op == "2>>"))
            new_stderr = b""
        elif r.op in ("&>", "&>>"):
            path = await _redir_target_path(r, env, runner)
            await runner.write_file(
                path,
                new_stdout + new_stderr,
                env,
                append=(r.op == "&>>"),
            )
            new_stdout = b""
            new_stderr = b""
    return new_stdout, new_stderr


async def _apply_redirect_sideeffect(r: Redirect, env: ShellEnv, runner: CommandRunner) -> None:
    if r.op in (">", ">>"):
        path = await _redir_target_path(r, env, runner)
        await runner.write_file(path, b"", env, append=(r.op == ">>"))
    elif r.op in ("2>", "2>>"):
        path = await _redir_target_path(r, env, runner)
        await runner.write_file(path, b"", env, append=(r.op == "2>>"))
    elif r.op in ("&>", "&>>"):
        path = await _redir_target_path(r, env, runner)
        await runner.write_file(path, b"", env, append=(r.op == "&>>"))


def _brace_expand_word(word: Word) -> list[Word]:
    # Apply brace expansion textually across literal-only segments. We render
    # the word as a string with placeholders for non-literal parts, expand
    # braces, then rebuild Word objects substituting the placeholders back.
    from .ast import (  # noqa: PLC0415
        ArithPart as _Arith,  # noqa: F401
    )
    from .ast import (
        CmdSubPart as _Cmd,  # noqa: F401
    )
    from .ast import (
        GlobPart as _Glob,
    )
    from .ast import (
        LiteralPart as _Lit,
    )
    from .ast import (
        TildePart as _Tilde,
    )
    from .ast import (
        VarPart as _Var,  # noqa: F401
    )
    from .ast import (
        Word as _Word,
    )
    from .parser import _brace_expand  # noqa: PLC0415

    pieces: list[str] = []
    placeholders: list[object] = []
    PLACE_OPEN = "\x10"
    PLACE_CLOSE = "\x11"
    has_brace = False
    for part in word.parts:
        if isinstance(part, _Lit):
            if not part.quoted and ("{" in part.text):
                has_brace = True
            pieces.append(part.text if not part.quoted else _escape_braces(part.text))
        elif isinstance(part, _Glob):
            # globs may contain braces but bash only does brace expansion on
            # unquoted text; glob patterns from us came from unquoted literal,
            # so allow braces here too.
            if "{" in part.pattern:
                has_brace = True
            pieces.append(part.pattern)
        elif isinstance(part, _Tilde):
            pieces.append(f"~{part.user or ''}")
        else:
            idx = len(placeholders)
            placeholders.append(part)
            pieces.append(f"{PLACE_OPEN}{idx}{PLACE_CLOSE}")

    if not has_brace:
        return [word]

    flat = "".join(pieces)
    expansions = _brace_expand(flat)
    if len(expansions) <= 1:
        return [word]

    out: list[_Word] = []
    for ex in expansions:
        new_parts: list = []
        i = 0
        n = len(ex)
        cur = []
        while i < n:
            ch = ex[i]
            if ch == PLACE_OPEN:
                if cur:
                    new_parts.append(_make_lit_or_glob("".join(cur)))
                    cur = []
                end = ex.index(PLACE_CLOSE, i + 1)
                idx = int(ex[i + 1 : end])
                new_parts.append(placeholders[idx])
                i = end + 1
                continue
            if ch == "~" and i == 0:
                # leading tilde survives
                cur.append(ch)
                i += 1
                continue
            cur.append(ch)
            i += 1
        if cur:
            new_parts.append(_make_lit_or_glob("".join(cur)))
        # leading tilde reconstruction
        if new_parts and isinstance(new_parts[0], _Lit) and new_parts[0].text.startswith("~"):
            text = new_parts[0].text
            j = 1
            while j < len(text) and text[j] not in ("/", ":"):
                j += 1
            user = text[1:j] or None
            tilde = _Tilde(user=user)
            rest = text[j:]
            head = [tilde]
            if rest:
                head.append(_make_lit_or_glob(rest))
            new_parts = head + new_parts[1:]
        out.append(_Word(parts=new_parts))
    return out


def _make_lit_or_glob(text: str):
    from .ast import GlobPart as _Glob  # noqa: PLC0415
    from .ast import LiteralPart as _Lit

    if any(c in "*?[" for c in text):
        return _Glob(pattern=text)
    return _Lit(text=text, quoted=False)


def _escape_braces(text: str) -> str:
    return text.replace("{", "\x12").replace("}", "\x13")
