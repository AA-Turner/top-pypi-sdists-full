from __future__ import annotations

import random
from dataclasses import dataclass, field

from matrx_ai.tools.vfs.commands.base import CommandContext, encode, fail, ok, resolve_cwd
from matrx_ai.tools.vfs.commands.registry import register
from matrx_ai.tools.vfs.shell.runner import CommandResult


@dataclass(slots=True)
class _Key:
    start_field: int
    start_char: int = 1
    end_field: int | None = None
    end_char: int | None = None


@dataclass(slots=True)
class _Opts:
    numeric: bool = False
    human: bool = False
    reverse: bool = False
    unique: bool = False
    ignore_case: bool = False
    keys: list[_Key] = field(default_factory=list)
    field_sep: str | None = None
    output_file: str | None = None
    check_only: bool = False
    merge: bool = False
    random_sort: bool = False
    files: list[str] = field(default_factory=list)


def _bad_arg(msg: str) -> bytes:
    return encode(f"sort: {msg}\nTry 'sort --help' for more information.\n")


def _parse_key_spec(spec: str) -> _Key | None:
    # FORMAT: F[.C][,F[.C]] (we ignore type-modifiers per-key for simplicity)
    parts = spec.split(",", 1)

    def parse_pos(s: str) -> tuple[int, int] | None:
        if "." in s:
            f, _, c = s.partition(".")
            if not f.isdigit() or not c.isdigit():
                return None
            return int(f), int(c)
        if not s.isdigit():
            return None
        return int(s), 1

    s_pos = parse_pos(parts[0])
    if s_pos is None or s_pos[0] < 1:
        return None
    key = _Key(start_field=s_pos[0], start_char=s_pos[1])
    if len(parts) == 2:
        e_pos = parse_pos(parts[1])
        if e_pos is None or e_pos[0] < 1:
            return None
        key.end_field = e_pos[0]
        key.end_char = e_pos[1]
    return key


def _parse_args(args: list[str]) -> tuple[_Opts, CommandResult | None]:
    opts = _Opts()
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
            if name == "numeric-sort":
                opts.numeric = True
            elif name == "human-numeric-sort":
                opts.human = True
            elif name == "reverse":
                opts.reverse = True
            elif name == "unique":
                opts.unique = True
            elif name == "ignore-case":
                opts.ignore_case = True
            elif name == "check":
                opts.check_only = True
            elif name == "merge":
                opts.merge = True
            elif name == "random-sort":
                opts.random_sort = True
            elif name == "key":
                if not has_eq:
                    if i + 1 >= len(args):
                        return opts, fail(2, _bad_arg("option requires an argument"))
                    i += 1
                    value = args[i]
                key = _parse_key_spec(value)
                if key is None:
                    return opts, fail(2, _bad_arg(f"invalid key '{value}'"))
                opts.keys.append(key)
            elif name == "field-separator":
                if not has_eq:
                    if i + 1 >= len(args):
                        return opts, fail(2, _bad_arg("option requires an argument"))
                    i += 1
                    value = args[i]
                if len(value) != 1:
                    return opts, fail(2, _bad_arg("multi-character tab"))
                opts.field_sep = value
            elif name == "output":
                if not has_eq:
                    if i + 1 >= len(args):
                        return opts, fail(2, _bad_arg("option requires an argument"))
                    i += 1
                    value = args[i]
                opts.output_file = value
            else:
                return opts, fail(2, _bad_arg(f"unrecognized option '--{name}'"))
            i += 1
            continue
        if a.startswith("-") and len(a) > 1:
            j = 1
            advanced = False
            while j < len(a):
                letter = a[j]
                if letter == "n":
                    opts.numeric = True
                    j += 1
                elif letter == "h":
                    opts.human = True
                    j += 1
                elif letter == "r":
                    opts.reverse = True
                    j += 1
                elif letter == "u":
                    opts.unique = True
                    j += 1
                elif letter == "f":
                    opts.ignore_case = True
                    j += 1
                elif letter == "c":
                    opts.check_only = True
                    j += 1
                elif letter == "m":
                    opts.merge = True
                    j += 1
                elif letter == "R":
                    opts.random_sort = True
                    j += 1
                elif letter == "b":
                    # ignore-leading-blanks - not applied per-key here
                    j += 1
                elif letter == "k":
                    inline = a[j + 1 :]
                    if inline:
                        value = inline
                        j = len(a)
                    else:
                        if i + 1 >= len(args):
                            return opts, fail(2, _bad_arg("option requires an argument -- 'k'"))
                        i += 1
                        value = args[i]
                        j = len(a)
                        advanced = True
                    key = _parse_key_spec(value)
                    if key is None:
                        return opts, fail(2, _bad_arg(f"invalid key '{value}'"))
                    opts.keys.append(key)
                elif letter == "t":
                    inline = a[j + 1 :]
                    if inline:
                        value = inline
                        j = len(a)
                    else:
                        if i + 1 >= len(args):
                            return opts, fail(2, _bad_arg("option requires an argument -- 't'"))
                        i += 1
                        value = args[i]
                        j = len(a)
                        advanced = True
                    if len(value) != 1:
                        return opts, fail(2, _bad_arg("multi-character tab"))
                    opts.field_sep = value
                elif letter == "o":
                    inline = a[j + 1 :]
                    if inline:
                        value = inline
                        j = len(a)
                    else:
                        if i + 1 >= len(args):
                            return opts, fail(2, _bad_arg("option requires an argument -- 'o'"))
                        i += 1
                        value = args[i]
                        j = len(a)
                        advanced = True
                    opts.output_file = value
                else:
                    return opts, fail(2, _bad_arg(f"invalid option -- '{letter}'"))
            _ = advanced
            i += 1
            continue
        opts.files.append(a)
        i += 1
    return opts, None


def _split_fields(line: str, sep: str | None) -> list[str]:
    if sep is None:
        # Default GNU: each field is a maximal sequence of non-blank chars
        # preceded by zero or more blanks. Keep leading blanks as the field
        # "boundary"; we handle by manual scanning.
        fields: list[str] = []
        i = 0
        n = len(line)
        # Standard split-on-whitespace mimicry: split() collapses runs.
        # GNU default puts the leading blanks at the start of each field, but
        # for sort key extraction split() is close enough for our needs.
        while i < n:
            start = i
            while i < n and line[i] in (" ", "\t"):
                i += 1
            while i < n and line[i] not in (" ", "\t"):
                i += 1
            fields.append(line[start:i].lstrip(" \t"))
        return fields
    return line.split(sep)


def _extract_key(line: str, key: _Key, sep: str | None) -> str:
    fields = _split_fields(line, sep)
    if key.start_field > len(fields):
        return ""
    start_idx = key.start_field - 1
    end_idx = (key.end_field - 1) if key.end_field is not None else len(fields) - 1
    end_idx = min(end_idx, len(fields) - 1)

    if start_idx == end_idx:
        s = fields[start_idx]
        a = max(0, key.start_char - 1)
        if key.end_char is not None:
            return s[a : key.end_char]
        return s[a:]
    parts = []
    first = fields[start_idx]
    parts.append(first[max(0, key.start_char - 1) :])
    for k in range(start_idx + 1, end_idx):
        parts.append(fields[k])
    if end_idx > start_idx:
        last = fields[end_idx]
        if key.end_char is not None:
            parts.append(last[: key.end_char])
        else:
            parts.append(last)
    sep_str = sep if sep is not None else " "
    return sep_str.join(parts)


def _numeric_value(s: str) -> float:
    s = s.lstrip(" \t")
    if not s:
        return 0.0
    end = 0
    if end < len(s) and s[end] in ("+", "-"):
        end += 1
    saw_digit = False
    saw_dot = False
    while end < len(s):
        c = s[end]
        if c.isdigit():
            saw_digit = True
            end += 1
        elif c == "." and not saw_dot:
            saw_dot = True
            end += 1
        else:
            break
    if not saw_digit:
        return 0.0
    try:
        return float(s[:end])
    except ValueError:
        return 0.0


def _human_value(s: str) -> float:
    s = s.lstrip(" \t")
    if not s:
        return 0.0
    sign = 1.0
    if s[0] == "-":
        sign = -1.0
        s = s[1:]
    elif s[0] == "+":
        s = s[1:]
    end = 0
    saw_dot = False
    while end < len(s):
        c = s[end]
        if c.isdigit() or (c == "." and not saw_dot):
            if c == ".":
                saw_dot = True
            end += 1
        else:
            break
    if end == 0:
        return 0.0
    try:
        val = float(s[:end])
    except ValueError:
        return 0.0
    suffix = s[end : end + 1]
    mult: dict[str, float] = {
        "K": 1024,
        "k": 1000,
        "M": 1024 ** 2,
        "G": 1024 ** 3,
        "T": 1024 ** 4,
        "P": 1024 ** 5,
        "E": 1024 ** 6,
    }
    if suffix in mult:
        val *= mult[suffix]
    return sign * val


def _sort_key(line: str, opts: _Opts) -> tuple:
    if opts.keys:
        keys_out: list = []
        for k in opts.keys:
            s = _extract_key(line, k, opts.field_sep)
            if opts.ignore_case:
                s = s.lower()
            if opts.numeric:
                keys_out.append(_numeric_value(s))
            elif opts.human:
                keys_out.append(_human_value(s))
            else:
                keys_out.append(s)
        return tuple(keys_out)
    s = line
    if opts.ignore_case:
        s = s.lower()
    if opts.numeric:
        return (_numeric_value(s),)
    if opts.human:
        return (_human_value(s),)
    return (s,)


@register("sort")
async def cmd_sort(ctx: CommandContext) -> CommandResult:
    opts, err = _parse_args(ctx.args)
    if err is not None:
        return err

    all_lines: list[str] = []
    if not opts.files:
        data = ctx.stdin
        all_lines.extend(_data_to_lines(data))
    else:
        for path in opts.files:
            if path == "-":
                all_lines.extend(_data_to_lines(ctx.stdin))
                continue
            resolved = resolve_cwd(ctx.env, path)
            try:
                data = await ctx.vfs._cat_file(resolved)
            except FileNotFoundError:
                return fail(
                    2, encode(f"sort: cannot read: '{path}': No such file or directory\n")
                )
            except OSError as exc:
                return fail(
                    2, encode(f"sort: cannot read: '{path}': {exc.strerror or 'I/O error'}\n")
                )
            all_lines.extend(_data_to_lines(data))

    if opts.check_only:
        sorted_lines = _sort_lines(all_lines, opts)
        if sorted_lines != all_lines:
            return fail(1, b"")
        return ok(b"")

    sorted_lines = _sort_lines(all_lines, opts)
    if opts.unique:
        deduped: list[str] = []
        prev_key: tuple | None = None
        for line in sorted_lines:
            k = _sort_key(line, opts)
            if k != prev_key:
                deduped.append(line)
                prev_key = k
        sorted_lines = deduped

    text = "".join(line + "\n" for line in sorted_lines)
    body = text.encode("latin-1")
    if opts.output_file:
        resolved = resolve_cwd(ctx.env, opts.output_file)
        await ctx.vfs._pipe_file(resolved, body)
        return ok(b"")
    return ok(body)


def _data_to_lines(data: bytes) -> list[str]:
    if not data:
        return []
    text = data.decode("latin-1")
    if text.endswith("\n"):
        text = text[:-1]
    if text == "":
        return [""]
    return text.split("\n")


def _sort_lines(lines: list[str], opts: _Opts) -> list[str]:
    if opts.random_sort:
        rng = random.Random(0)
        out = list(lines)
        rng.shuffle(out)
        return out
    out = sorted(lines, key=lambda line: _sort_key(line, opts))
    if opts.reverse:
        out.reverse()
    return out
