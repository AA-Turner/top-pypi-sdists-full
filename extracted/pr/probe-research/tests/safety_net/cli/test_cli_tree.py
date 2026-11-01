"""The `probe` command tree: every command, every parameter, and a hash of its help strings.

Help text is pinned as raw strings (never rendered output), so a typer/rich/click upgrade
cannot move it; `cli_help.json` keeps the strings themselves so a changed hash reads as a diff.
"""

from __future__ import annotations

import difflib
import enum
import hashlib
import importlib
import inspect
import json
import os
from pathlib import Path

import pytest
import typer.main

BASELINES = Path(__file__).resolve().parent / "baselines"


def _root():
    # The CLI's module is the pinned entry `probe.cli.main` (entry_paths/), so this import survives moves.
    return typer.main.get_command(importlib.import_module("probe.cli.main").app)


def _text(value) -> str | None:
    if value is None:
        return None
    return inspect.cleandoc(str(value))  # 3.13 dedents docstrings at compile time; 3.12 does not


def _jsonable(value):
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, enum.Enum):
        return _jsonable(value.value)
    if isinstance(value, (list, tuple)):
        return [_jsonable(v) for v in value]
    if isinstance(value, os.PathLike):
        return str(value).replace(str(Path.home()), "~")
    if callable(value):
        return "<callable>"
    return f"<{type(value).__name__}>"  # a library sentinel (click's UNSET and kin)


def _type(t) -> str:
    """A canonical type name: click's own `.name` strings differ between versions."""
    name = type(t).__name__
    if "Choice" in name:
        return "CHOICE[" + "|".join(str(_jsonable(c)) for c in t.choices) + "]"
    if name in ("IntRange", "FloatRange"):
        bounds = f"{t.min}..{t.max}" + (" min_open" if t.min_open else "") + (" max_open" if t.max_open else "")
        return f"{'INT' if name == 'IntRange' else 'FLOAT'}_RANGE[{bounds}{' clamp' if t.clamp else ''}]"
    if "Path" in name:
        flags = ("exists", "file_okay", "dir_okay", "writable", "readable", "resolve_path", "allow_dash")
        return "PATH[" + ",".join(f for f in flags if getattr(t, f, False)) + "]"
    plain = {"StringParamType": "STRING", "BoolParamType": "BOOL", "IntParamType": "INT", "FloatParamType": "FLOAT",
             "UUIDParameterType": "UUID", "UnprocessedParamType": "UNPROCESSED", "DateTime": "DATETIME",
             "File": "FILE", "Tuple": "TUPLE"}
    return plain.get(name, name)


def _param(p) -> str:
    """One line per parameter: kind, name, opts[/secondary], type, then only what is set."""
    opts = ",".join(p.opts) + ("/" + ",".join(p.secondary_opts) if p.secondary_opts else "")
    words = [p.param_type_name, p.name or "-", opts, _type(p.type)]
    for flag in ("required", "multiple", "is_flag", "count", "hidden", "is_eager"):
        if getattr(p, flag, False):
            words.append(flag)
    if p.nargs != 1:
        words.append(f"nargs={p.nargs}")
    if not p.expose_value:
        words.append("not_exposed")
    if getattr(p, "prompt", None):
        words.append("prompt")
    if p.callback is not None:
        words.append("callback")
    if p.default is not None:
        words.append("default=" + json.dumps(_jsonable(p.default), sort_keys=True))
    if p.envvar:
        words.append("envvar=" + json.dumps(_jsonable(p.envvar)))
    return " ".join(words)


def _strings(cmd) -> dict:
    """Every help string a person or an agent reads for this command (unset ones left out)."""
    found = {
        "help": _text(cmd.help),
        "short_help": _text(cmd.short_help),
        "epilog": _text(cmd.epilog),
        "deprecated": _jsonable(cmd.deprecated) or None,
        "params": {p.name or "-": _text(p.help) for p in cmd.params if getattr(p, "help", None)} or None,
    }
    return {key: value for key, value in found.items() if value is not None}


def _settings(cmd) -> dict:
    return {key: _jsonable(value) for key, value in sorted((cmd.context_settings or {}).items())}


def walk(cmd=None, path: str = "probe", out: dict | None = None, helps: dict | None = None):
    """`(tree, help strings)`, both keyed by the command's words (`probe run list`)."""
    cmd = cmd if cmd is not None else _root()
    out = {} if out is None else out
    helps = {} if helps is None else helps
    strings = _strings(cmd)
    helps[path] = strings
    subs = getattr(cmd, "commands", None)
    flags = [name for name, on in (
        ("group", subs is not None),
        ("hidden", getattr(cmd, "hidden", False)),
        ("deprecated", cmd.deprecated),
        ("no_help_option", not getattr(cmd, "add_help_option", True)),
        ("no_args_is_help", getattr(cmd, "no_args_is_help", False)),
        ("invoke_without_command", getattr(cmd, "invoke_without_command", False)),
        ("chain", getattr(cmd, "chain", False)),
    ) if on]
    entry = {"class": type(cmd).__name__, "flags": flags, "params": [_param(p) for p in cmd.params],
             "help_sha256": hashlib.sha256(json.dumps(strings, sort_keys=True).encode()).hexdigest()}
    if cmd.context_settings:
        entry["context"] = _settings(cmd)
    out[path] = entry
    for name, sub in sorted((subs or {}).items()):
        walk(sub, f"{path} {name}", out, helps)
    return out, helps


@pytest.fixture(scope="module")
def tree():
    return walk()


def _recorded(name: str) -> dict:
    try:
        return json.loads((BASELINES / f"{name}.json").read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _help_changes(tree: dict, helps: dict) -> str:
    """A readable diff of the help strings behind every hash that moved (empty: none did)."""
    old_tree, old_help = _recorded("cli_tree"), _recorded("cli_help")
    parts = []
    for path in sorted(set(old_tree) & set(tree)):
        if old_tree[path].get("help_sha256") == tree[path]["help_sha256"]:
            continue
        before = json.dumps(old_help.get(path), indent=2, sort_keys=True).splitlines(keepends=True)
        after = json.dumps(helps[path], indent=2, sort_keys=True).splitlines(keepends=True)
        parts.append(f"--- help of `{path}`\n" + "".join(difflib.unified_diff(before, after, "baseline", "now", n=1)))
    return "\n".join(parts)


def test_cli_command_tree_and_parameters_are_unchanged(tree, baseline):
    commands, helps = tree
    changed = "" if os.environ.get("PROBE_SAFETY_NET_UPDATE") == "1" else _help_changes(commands, helps)
    try:
        baseline("cli_tree", commands)
        return
    except pytest.fail.Exception as exc:
        if not changed:
            raise
        failure = str(exc)
    # A moved hash alone says nothing: show the strings behind it.
    pytest.fail(f"{failure}\n\nhelp text changed under these commands:\n{changed[:20000]}", pytrace=False)


def test_cli_help_strings_are_unchanged(tree, baseline):
    baseline("cli_help", tree[1])


def test_cli_tree_covers_hidden_commands_and_every_parameter(tree):
    """Sanity: the walk reaches hidden commands and records every parameter of each."""
    commands, _ = tree
    root = _root()
    hidden = [p for p, c in commands.items() if "hidden" in c["flags"]]
    assert hidden, "no hidden command recorded: the walk skips them"
    total = 0

    def count(cmd):
        nonlocal total
        total += len(cmd.params)
        for sub in (getattr(cmd, "commands", None) or {}).values():
            count(sub)

    count(root)
    assert sum(len(c["params"]) for c in commands.values()) == total
