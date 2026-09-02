from __future__ import annotations

import fnmatch
import re
from dataclasses import dataclass, field

from matrx_ai.tools.vfs.commands.base import CommandContext, encode, fail, resolve_cwd
from matrx_ai.tools.vfs.commands.registry import register
from matrx_ai.tools.vfs.mimicry import (
    GrepOpts,
    format_grep_binary_warning,
    format_grep_count,
    format_grep_filenames_only,
    format_grep_match,
    grep_is_dir,
    grep_no_file,
)
from matrx_ai.tools.vfs.paths import join
from matrx_ai.tools.vfs.shell.runner import CommandResult


@dataclass(slots=True)
class _Opts:
    patterns: list[str] = field(default_factory=list)
    pattern_files: list[str] = field(default_factory=list)
    paths: list[str] = field(default_factory=list)
    show_lineno: bool = False
    count_only: bool = False
    files_with_matches: bool = False
    files_without_match: bool = False
    invert_match: bool = False
    ignore_case: bool = False
    word_regexp: bool = False
    line_regexp: bool = False
    only_matching: bool = False
    extended_regexp: bool = False
    fixed_strings: bool = False
    perl_regexp: bool = False
    recursive: bool = False
    deref_recursive: bool = False
    quiet: bool = False
    no_filename: bool = False
    with_filename: bool = False
    null_separator: bool = False
    text: bool = False
    skip_binary: bool = False
    binary_no_match: bool = False
    max_count: int | None = None
    after_context: int = 0
    before_context: int = 0
    include: list[str] = field(default_factory=list)
    exclude: list[str] = field(default_factory=list)
    exclude_dir: list[str] = field(default_factory=list)


_LONG_OPTS_NO_VALUE: dict[str, str] = {
    "--line-number": "n",
    "--count": "c",
    "--files-with-matches": "l",
    "--files-without-match": "L",
    "--invert-match": "v",
    "--ignore-case": "i",
    "--word-regexp": "w",
    "--line-regexp": "x",
    "--only-matching": "o",
    "--extended-regexp": "E",
    "--fixed-strings": "F",
    "--perl-regexp": "P",
    "--recursive": "r",
    "--dereference-recursive": "R",
    "--quiet": "q",
    "--silent": "q",
    "--no-filename": "h",
    "--with-filename": "H",
    "--null": "Z",
    "--text": "a",
    "--no-messages": "s",
}

_LONG_OPTS_VALUE: set[str] = {
    "--max-count",
    "--after-context",
    "--before-context",
    "--context",
    "--regexp",
    "--file",
    "--include",
    "--exclude",
    "--exclude-dir",
    "--binary-files",
}

_SHORT_VALUE_OPTS: set[str] = {"A", "B", "C", "m", "e", "f"}


def _usage_error() -> bytes:
    return encode(
        "Usage: grep [OPTION]... PATTERNS [FILE]...\n"
        "Try 'grep --help' for more information.\n"
    )


def _invalid_option(opt: str) -> bytes:
    return encode(
        f"grep: invalid option -- '{opt}'\nUsage: grep [OPTION]... PATTERNS [FILE]...\n"
        "Try 'grep --help' for more information.\n"
    )


def _invalid_max_count(value: str) -> bytes:
    return encode(f"grep: {value}: invalid max count\n")


def _invalid_context(value: str) -> bytes:
    return encode(f"grep: {value}: invalid context length argument\n")


def _bad_regex(msg: str) -> bytes:
    return encode(f"grep: {msg}\n")


def _apply_invocation_defaults(name: str, opts: _Opts) -> None:
    if name == "egrep":
        opts.extended_regexp = True
    elif name == "fgrep":
        opts.fixed_strings = True
    elif name == "rgrep":
        opts.recursive = True


def _parse_int(value: str) -> int | None:
    if not value or not value.lstrip("+").isdigit():
        return None
    try:
        n = int(value)
    except ValueError:
        return None
    if n < 0:
        return None
    return n


def _consume_short_value(
    args: list[str],
    i: int,
    rest: str,
    j: int,
    letter: str,
) -> tuple[str | None, int, int]:
    inline = rest[j + 1 :]
    if inline:
        return inline, i, len(rest)
    if i + 1 >= len(args):
        return None, i, j
    return args[i + 1], i + 1, len(rest)


def _parse_args(name: str, args: list[str]) -> tuple[_Opts, CommandResult | None]:
    opts = _Opts()
    _apply_invocation_defaults(name, opts)
    positional: list[str] = []
    have_pattern_arg = False
    end_of_opts = False
    i = 0
    while i < len(args):
        a = args[i]
        if end_of_opts:
            positional.append(a)
            i += 1
            continue
        if a == "--":
            end_of_opts = True
            i += 1
            continue
        if a.startswith("--"):
            name_part, has_eq, value = a[2:].partition("=")
            long_opt = "--" + name_part
            if long_opt in _LONG_OPTS_NO_VALUE:
                if has_eq:
                    return opts, fail(2, _invalid_option(name_part))
                _apply_short(opts, _LONG_OPTS_NO_VALUE[long_opt])
                i += 1
                continue
            if long_opt in _LONG_OPTS_VALUE:
                if not has_eq:
                    if i + 1 >= len(args):
                        return opts, fail(2, _invalid_option(name_part))
                    i += 1
                    value = args[i]
                err_res = _apply_long_value(opts, long_opt, value)
                if err_res is not None:
                    return opts, err_res
                if long_opt in ("--regexp", "--file"):
                    have_pattern_arg = True
                i += 1
                continue
            if long_opt == "--help":
                return opts, fail(2, _usage_error())
            return opts, fail(2, _invalid_option(name_part))
        if a == "-":
            positional.append(a)
            i += 1
            continue
        if a.startswith("-") and len(a) > 1:
            rest = a[1:]
            # Numeric shortcut: -NUM == -C NUM
            if rest[0].isdigit():
                n = _parse_int(rest)
                if n is None:
                    return opts, fail(2, _invalid_context(rest))
                opts.before_context = n
                opts.after_context = n
                i += 1
                continue
            j = 0
            while j < len(rest):
                letter = rest[j]
                if letter in _SHORT_VALUE_OPTS:
                    value, new_i, new_j = _consume_short_value(args, i, rest, j, letter)
                    if value is None:
                        return opts, fail(2, _invalid_option(letter))
                    err_res = _apply_short_value(opts, letter, value)
                    if err_res is not None:
                        return opts, err_res
                    if letter in ("e", "f"):
                        have_pattern_arg = True
                    i = new_i
                    j = new_j
                    break
                err_res = _apply_short(opts, letter)
                if err_res is not None:
                    return opts, err_res
                j += 1
            i += 1
            continue
        positional.append(a)
        i += 1

    # Distribute positional args: first is pattern (unless -e/-f used), rest are paths.
    if not have_pattern_arg:
        if not positional:
            return opts, fail(2, _usage_error())
        opts.patterns.append(positional[0])
        opts.paths.extend(positional[1:])
    else:
        opts.paths.extend(positional)
    return opts, None


def _apply_short(opts: _Opts, letter: str) -> CommandResult | None:
    if letter == "n":
        opts.show_lineno = True
    elif letter == "c":
        opts.count_only = True
    elif letter == "l":
        opts.files_with_matches = True
    elif letter == "L":
        opts.files_without_match = True
    elif letter == "v":
        opts.invert_match = True
    elif letter == "i" or letter == "y":
        opts.ignore_case = True
    elif letter == "w":
        opts.word_regexp = True
    elif letter == "x":
        opts.line_regexp = True
    elif letter == "o":
        opts.only_matching = True
    elif letter == "E":
        opts.extended_regexp = True
        opts.fixed_strings = False
        opts.perl_regexp = False
    elif letter == "F":
        opts.fixed_strings = True
        opts.extended_regexp = False
        opts.perl_regexp = False
    elif letter == "G":
        opts.extended_regexp = False
        opts.fixed_strings = False
        opts.perl_regexp = False
    elif letter == "P":
        opts.perl_regexp = True
        opts.extended_regexp = False
        opts.fixed_strings = False
    elif letter == "r":
        opts.recursive = True
    elif letter == "R":
        opts.recursive = True
        opts.deref_recursive = True
    elif letter == "q":
        opts.quiet = True
    elif letter == "h":
        opts.no_filename = True
        opts.with_filename = False
    elif letter == "H":
        opts.with_filename = True
        opts.no_filename = False
    elif letter == "Z":
        opts.null_separator = True
    elif letter == "a":
        opts.text = True
    elif letter == "I":
        opts.skip_binary = True
    elif letter == "s":
        # --no-messages: silently swallow file errors. Not modeled separately.
        pass
    else:
        return fail(2, _invalid_option(letter))
    return None


def _apply_short_value(opts: _Opts, letter: str, value: str) -> CommandResult | None:
    if letter == "A":
        n = _parse_int(value)
        if n is None:
            return fail(2, _invalid_context(value))
        opts.after_context = n
    elif letter == "B":
        n = _parse_int(value)
        if n is None:
            return fail(2, _invalid_context(value))
        opts.before_context = n
    elif letter == "C":
        n = _parse_int(value)
        if n is None:
            return fail(2, _invalid_context(value))
        opts.before_context = n
        opts.after_context = n
    elif letter == "m":
        n = _parse_int(value)
        if n is None:
            return fail(2, _invalid_max_count(value))
        opts.max_count = n
    elif letter == "e":
        opts.patterns.append(value)
    elif letter == "f":
        opts.pattern_files.append(value)
    return None


def _apply_long_value(opts: _Opts, long_opt: str, value: str) -> CommandResult | None:
    if long_opt == "--max-count":
        n = _parse_int(value)
        if n is None:
            return fail(2, _invalid_max_count(value))
        opts.max_count = n
    elif long_opt == "--after-context":
        n = _parse_int(value)
        if n is None:
            return fail(2, _invalid_context(value))
        opts.after_context = n
    elif long_opt == "--before-context":
        n = _parse_int(value)
        if n is None:
            return fail(2, _invalid_context(value))
        opts.before_context = n
    elif long_opt == "--context":
        n = _parse_int(value)
        if n is None:
            return fail(2, _invalid_context(value))
        opts.before_context = n
        opts.after_context = n
    elif long_opt == "--regexp":
        opts.patterns.append(value)
    elif long_opt == "--file":
        opts.pattern_files.append(value)
    elif long_opt == "--include":
        opts.include.append(value)
    elif long_opt == "--exclude":
        opts.exclude.append(value)
    elif long_opt == "--exclude-dir":
        opts.exclude_dir.append(value)
    elif long_opt == "--binary-files":
        if value == "without-match":
            opts.binary_no_match = True
        elif value == "text":
            opts.text = True
        elif value == "binary":
            pass
        else:
            return fail(2, encode(f"grep: {value}: invalid binary-files type\n"))
    return None


def _build_regex(opts: _Opts) -> tuple[re.Pattern[str] | None, CommandResult | None]:
    if not opts.patterns:
        return None, fail(2, _usage_error())
    if opts.fixed_strings:
        # Each pattern is a literal; allow multi-line patterns: each line is its own literal.
        literal_patterns: list[str] = []
        for p in opts.patterns:
            if p == "":
                literal_patterns.append("")
                continue
            for line in p.split("\n"):
                literal_patterns.append(re.escape(line))
        body = "|".join(p for p in literal_patterns) if literal_patterns else ""
    else:
        # Patterns: each may be multi-line (alternation per line).
        alts: list[str] = []
        for p in opts.patterns:
            if p == "":
                alts.append("")
                continue
            for line in p.split("\n"):
                alts.append(line)
        body = "|".join(f"(?:{p})" for p in alts) if alts else ""

    # Word and line constraints.
    if opts.line_regexp:
        body = f"^(?:{body})$" if body else r"^$"
    elif opts.word_regexp:
        body = rf"(?:^|\W)(?:{body})(?:\W|$)" if body else r"(?:^|\W)(?:\W|$)"

    flags = 0
    if opts.ignore_case:
        flags |= re.IGNORECASE
    try:
        compiled = re.compile(body, flags)
    except re.error as exc:
        return None, fail(2, _bad_regex(str(exc)))
    return compiled, None


def _split_lines(data: bytes) -> list[str]:
    # Split on '\n', preserving last unterminated line. We decode latin-1 so bytes
    # round-trip through Python re without losing high-byte content.
    text = data.decode("latin-1")
    if not text:
        return []
    lines = text.split("\n")
    # If text ends with '\n', `split` produces a trailing "" which represents
    # the empty line after the final newline. Drop that to match GNU's behavior
    # of not treating EOF newline as an extra line.
    if lines and lines[-1] == "" and text.endswith("\n"):
        lines.pop()
    return lines


def _is_binary(data: bytes) -> bool:
    head = data[:8192]
    return b"\x00" in head


def _line_match(opts: _Opts, pattern: re.Pattern[str], line: str) -> bool:
    if opts.line_regexp:
        m = pattern.match(line)
        return m is not None and m.end() == len(line)
    return bool(pattern.search(line))


async def _load_pattern_files(ctx: CommandContext, opts: _Opts) -> CommandResult | None:
    for path in opts.pattern_files:
        if path == "-":
            data = ctx.stdin
        else:
            resolved = resolve_cwd(ctx.env, path)
            try:
                data = await ctx.vfs._cat_file(resolved)
            except FileNotFoundError:
                return fail(2, encode(f"grep: {path}: No such file or directory\n"))
            except IsADirectoryError:
                return fail(2, encode(f"grep: {path}: Is a directory\n"))
            except OSError as exc:
                msg = exc.strerror or "I/O error"
                return fail(2, encode(f"grep: {path}: {msg}\n"))
        text = data.decode("latin-1")
        if text.endswith("\n"):
            text = text[:-1]
        for line in text.split("\n"):
            opts.patterns.append(line)
    return None


def _included(name: str, opts: _Opts) -> bool:
    if opts.include:
        if not any(fnmatch.fnmatch(name, pat) for pat in opts.include):
            return False
    if opts.exclude:
        if any(fnmatch.fnmatch(name, pat) for pat in opts.exclude):
            return False
    return True


def _dir_excluded(name: str, opts: _Opts) -> bool:
    return any(fnmatch.fnmatch(name, pat) for pat in opts.exclude_dir)


@dataclass(slots=True)
class _FileMatches:
    path: str
    display: str
    line_indices: list[int] = field(default_factory=list)
    lines: list[str] = field(default_factory=list)
    binary: bool = False
    matched: bool = False


def _scan_file(
    display: str,
    data: bytes,
    pattern: re.Pattern[str],
    opts: _Opts,
) -> _FileMatches:
    fm = _FileMatches(path=display, display=display)
    binary = _is_binary(data)
    fm.binary = binary
    if binary:
        if opts.skip_binary or opts.binary_no_match:
            return fm
    fm.lines = _split_lines(data)
    limit = opts.max_count
    for idx, line in enumerate(fm.lines):
        is_match = _line_match(opts, pattern, line)
        if opts.invert_match:
            is_match = not is_match
        if is_match:
            fm.line_indices.append(idx)
            fm.matched = True
            if limit is not None and len(fm.line_indices) >= limit:
                break
    return fm


def _emit_matches(
    fm: _FileMatches,
    opts: _Opts,
    multi_files: bool,
    out: bytearray,
) -> None:
    show_fn = _decide_show_filename(opts, multi_files)
    fopts = GrepOpts(show_filename=show_fn, show_lineno=opts.show_lineno)
    if opts.only_matching and not opts.invert_match:
        for idx in fm.line_indices:
            line = fm.lines[idx]
            for m in _only_match_iter(line, opts):
                emitted = _format_om_line(fm.display, idx + 1, m, opts, show_fn)
                out.extend(encode(emitted))
        return

    if opts.before_context == 0 and opts.after_context == 0:
        for idx in fm.line_indices:
            line = fm.lines[idx]
            text = format_grep_match(fm.display, idx + 1, line, fopts)
            if opts.null_separator and show_fn:
                text = text.replace(":", "\x00", 1) if ":" in text else text
            out.extend(encode(text + "\n"))
        return

    # Context mode.
    groups: list[tuple[int, int]] = []
    for idx in fm.line_indices:
        start = max(0, idx - opts.before_context)
        end = min(len(fm.lines) - 1, idx + opts.after_context)
        if groups and start <= groups[-1][1] + 1:
            prev_s, prev_e = groups[-1]
            groups[-1] = (prev_s, max(prev_e, end))
        else:
            groups.append((start, end))
    match_set = set(fm.line_indices)
    first_group = True
    for gstart, gend in groups:
        if not first_group:
            out.extend(b"--\n")
        first_group = False
        for li in range(gstart, gend + 1):
            sep = ":" if li in match_set else "-"
            line = fm.lines[li]
            prefix = _format_context_prefix(fm.display, li + 1, sep, opts, show_fn)
            out.extend(encode(prefix + line + "\n"))


def _format_context_prefix(
    display: str, lineno: int, sep: str, opts: _Opts, show_fn: bool
) -> str:
    file_sep = "\x00" if opts.null_separator else sep
    parts: list[str] = []
    if show_fn:
        parts.append(display)
        parts.append(file_sep)
    if opts.show_lineno:
        parts.append(str(lineno))
        parts.append(sep)
    return "".join(parts)


def _only_match_iter(line: str, opts: _Opts):
    pat = _build_regex_for_only(opts)
    if pat is None:
        return
    for m in pat.finditer(line):
        if not m.group(0):
            continue
        yield m.group(0)


def _build_regex_for_only(opts: _Opts) -> re.Pattern[str] | None:
    if not opts.patterns:
        return None
    if opts.fixed_strings:
        alts: list[str] = []
        for p in opts.patterns:
            for line in p.split("\n"):
                if line:
                    alts.append(re.escape(line))
        body = "|".join(alts)
    else:
        alts = []
        for p in opts.patterns:
            for line in p.split("\n"):
                if line:
                    alts.append(line)
        body = "|".join(f"(?:{p})" for p in alts)
    if not body:
        return None
    if opts.word_regexp:
        body = rf"\b(?:{body})\b"
    flags = re.IGNORECASE if opts.ignore_case else 0
    try:
        return re.compile(body, flags)
    except re.error:
        return None


def _format_om_line(display: str, lineno: int, match: str, opts: _Opts, show_fn: bool) -> str:
    sep = "\x00" if opts.null_separator else ":"
    parts: list[str] = []
    if show_fn:
        parts.append(display)
        parts.append(sep)
    if opts.show_lineno:
        parts.append(str(lineno))
        parts.append(":")
    parts.append(match)
    parts.append("\n")
    return "".join(parts)


def _decide_show_filename(opts: _Opts, multi_files: bool) -> bool:
    if opts.no_filename:
        return False
    if opts.with_filename:
        return True
    if opts.recursive:
        return True
    return multi_files


def _relativize(path: str, root: str) -> str:
    if path == root:
        return ""
    if path.startswith(root.rstrip("/") + "/"):
        return path[len(root.rstrip("/")) + 1 :]
    return path


@register("grep", "egrep", "fgrep", "rgrep")
async def cmd_grep(ctx: CommandContext) -> CommandResult:
    opts, err = _parse_args(ctx.name, ctx.args)
    if err is not None:
        return err

    err_load = await _load_pattern_files(ctx, opts)
    if err_load is not None:
        return err_load

    if not opts.patterns:
        return fail(2, _usage_error())

    pattern, err_pat = _build_regex(opts)
    if err_pat is not None:
        return err_pat
    assert pattern is not None

    # Resolve path list. When recursive and no path given, default to '.'.
    raw_paths = list(opts.paths)
    if opts.recursive and not raw_paths:
        raw_paths = ["."]
    if not raw_paths:
        # No path: read from stdin.
        return await _grep_stdin(ctx, pattern, opts)

    # Expand recursive directories into file lists; track display names.
    files_to_scan: list[tuple[str, str, str]] = []  # (resolved, display, original)
    err_out = bytearray()
    file_errors = False

    for orig in raw_paths:
        if orig == "-":
            files_to_scan.append(("-", "(standard input)", orig))
            continue
        resolved = resolve_cwd(ctx.env, orig)
        try:
            is_dir = await ctx.vfs._isdir(resolved)
        except OSError:
            is_dir = False
        try:
            exists = await ctx.vfs._exists(resolved)
        except OSError:
            exists = False
        if not exists:
            err_out.extend(encode(grep_no_file(orig)))
            file_errors = True
            continue
        if is_dir:
            if not opts.recursive:
                err_out.extend(encode(grep_is_dir(orig)))
                file_errors = True
                continue
            # Walk
            async for cur_root, dirs, files_in in ctx.vfs._walk(resolved):
                # Compute relative path under orig.
                rel = _relativize(cur_root, resolved)
                # Skip if any path component excluded.
                if rel:
                    if any(_dir_excluded(p, opts) for p in rel.split("/") if p):
                        continue
                # Also: skip processing dirs whose name is excluded — but _walk already
                # descends; we can't easily prune. Filter on path components above.
                for fname in files_in:
                    if not _included(fname, opts):
                        continue
                    full = join(cur_root, fname)
                    if rel:
                        display = orig.rstrip("/") + "/" + rel + "/" + fname
                    else:
                        display = orig.rstrip("/") + "/" + fname if orig != "" else fname
                    while "//" in display:
                        display = display.replace("//", "/")
                    files_to_scan.append((full, display, orig))
        else:
            files_to_scan.append((resolved, orig, orig))

    # Compute show_filename decision.
    multi_files = len(files_to_scan) > 1 or opts.recursive

    out = bytearray()
    found_any = False

    # quiet mode: terminate on first match
    for resolved, display, orig in files_to_scan:
        if resolved == "-":
            data = ctx.stdin
        else:
            try:
                data = await ctx.vfs._cat_file(resolved)
            except FileNotFoundError:
                err_out.extend(encode(grep_no_file(orig)))
                file_errors = True
                continue
            except IsADirectoryError:
                err_out.extend(encode(grep_is_dir(orig)))
                file_errors = True
                continue
            except OSError as exc:
                msg = exc.strerror or "I/O error"
                err_out.extend(encode(f"grep: {orig}: {msg}\n"))
                file_errors = True
                continue

        is_bin = _is_binary(data)
        if is_bin and not opts.text:
            if opts.skip_binary or opts.binary_no_match:
                continue

        fm = _scan_file(display, data, pattern, opts)
        if opts.quiet:
            if fm.matched:
                found_any = True
                # Early termination
                exit_code = 0
                if file_errors:
                    exit_code = 2
                return CommandResult(stdout=b"", stderr=bytes(err_out), exit_code=exit_code)
            continue

        if opts.files_with_matches:
            if fm.matched:
                found_any = True
                sep = "\x00" if opts.null_separator else "\n"
                out.extend(encode(display + sep))
            continue

        if opts.files_without_match:
            if not fm.matched:
                out.extend(encode(display + "\n"))
            else:
                found_any = True
            continue

        if opts.count_only:
            count = len(fm.line_indices)
            if count > 0:
                found_any = True
            sf = _decide_show_filename(opts, multi_files)
            cnt_opts = GrepOpts(show_filename=sf)
            line = format_grep_count(display, count, cnt_opts)
            if opts.null_separator and sf:
                line = line.replace(":", "\x00", 1)
            out.extend(encode(line + "\n"))
            continue

        if is_bin and not opts.text:
            # Default: emit "Binary file X matches" only if there were matches.
            if fm.matched:
                found_any = True
                out.extend(encode(format_grep_binary_warning(display) + "\n"))
            continue

        if fm.matched:
            found_any = True
        _emit_matches(fm, opts, multi_files, out)

    if opts.quiet:
        exit_code = 0 if found_any else 1
        if file_errors and not found_any:
            exit_code = 2
        return CommandResult(stdout=b"", stderr=bytes(err_out), exit_code=exit_code)

    if file_errors:
        exit_code = 2
    elif found_any:
        exit_code = 0
    else:
        exit_code = 1
    return CommandResult(stdout=bytes(out), stderr=bytes(err_out), exit_code=exit_code)


async def _grep_stdin(
    ctx: CommandContext, pattern: re.Pattern[str], opts: _Opts
) -> CommandResult:
    data = ctx.stdin
    display = "(standard input)"
    out = bytearray()
    is_bin = _is_binary(data)
    if is_bin and not opts.text:
        if opts.skip_binary or opts.binary_no_match:
            return CommandResult(stdout=b"", stderr=b"", exit_code=1)
    fm = _scan_file(display, data, pattern, opts)
    if opts.quiet:
        return CommandResult(stdout=b"", stderr=b"", exit_code=0 if fm.matched else 1)

    if opts.files_with_matches:
        if fm.matched:
            sep = "\x00" if opts.null_separator else "\n"
            out.extend(encode(display + sep))
        return CommandResult(stdout=bytes(out), exit_code=0 if fm.matched else 1)

    if opts.files_without_match:
        if not fm.matched:
            out.extend(encode(display + "\n"))
        return CommandResult(stdout=bytes(out), exit_code=0 if not fm.matched else 1)

    if opts.count_only:
        count = len(fm.line_indices)
        sf = opts.with_filename and not opts.no_filename
        cnt_opts = GrepOpts(show_filename=sf)
        line = format_grep_count(display, count, cnt_opts)
        out.extend(encode(line + "\n"))
        return CommandResult(stdout=bytes(out), exit_code=0 if count > 0 else 1)

    if is_bin and not opts.text:
        if fm.matched:
            out.extend(encode(format_grep_binary_warning(display) + "\n"))
        return CommandResult(stdout=bytes(out), exit_code=0 if fm.matched else 1)

    _emit_matches(fm, opts, multi_files=False, out=out)
    return CommandResult(stdout=bytes(out), exit_code=0 if fm.matched else 1)


# Keep the helper visible to satisfy linter and the planned extension surface.
_ = format_grep_filenames_only
