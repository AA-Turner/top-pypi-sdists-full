"""The `probe` CLI's command tree as data, for the daemon's command checks (plan M1).

`precheck` parses every `probe` command the daemon runs with the CLI's own parser
(click's `make_context`, resilient). Building that tree meant importing the whole
CLI and its API client (~33 MB, once per process: once per daemon host). Instead
the tree is described in `cli_spec.json`, generated from the real CLI
(`python -m probe.daemon.cli_spec --write`), and rebuilt here from plain click
objects: the parsing is still click's, with the same names, types, defaults,
nargs, flags and context settings. A test regenerates the file from the live CLI
and fails on any difference, and another parses a corpus through both trees.

What the CLI's own command classes add is not parsing (`_JsonCommand` prints
`--json` events for a usage error, `_RawArgsCommand` keeps the raw args in
`ctx.meta`, `_McpGroup` words its typo suggestions), so a plain Command/Group
gives the same `ctx.params`. The one context hook that changes values -- the
project-kind aliases (`token_normalize_func`) -- is kept as its alias table.
"""

from __future__ import annotations

import contextlib
import hashlib
import json
import os
import sys
import threading
import time
from pathlib import Path
from typing import Any

SPEC_PATH = Path(__file__).with_name("cli_spec.json")
FORMAT = 1


# -- dumping (from the real CLI; build time and tests) --------------------------------
def _jsonable(value: Any) -> Any:
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, (list, tuple)):
        return [_jsonable(v) for v in value]
    if hasattr(value, "value") and isinstance(getattr(value, "value"), (str, int)):
        return value.value  # an Enum default: click sees its value
    raise TypeError(f"default {value!r} has no JSON form")


def _dump_type(t: Any) -> dict:
    name = type(t).__name__
    if name == "StringParamType":
        return {"name": "STRING"}
    if name == "BoolParamType":
        return {"name": "BOOL"}
    if name == "IntParamType":
        return {"name": "INT"}
    if name == "FloatParamType":
        return {"name": "FLOAT"}
    if name in ("IntRange", "FloatRange"):
        return {"name": name, "min": t.min, "max": t.max, "min_open": t.min_open, "max_open": t.max_open,
                "clamp": t.clamp}
    if name == "TyperChoice":
        return {"name": "Choice", "choices": [_jsonable(c) for c in t.choices], "case_sensitive": t.case_sensitive}
    if name == "TyperPath":
        path_type = getattr(t, "type", None)
        return {"name": "Path", "exists": t.exists, "file_okay": t.file_okay, "dir_okay": t.dir_okay,
                "writable": t.writable, "readable": t.readable, "resolve_path": t.resolve_path,
                "allow_dash": t.allow_dash, "path_type": None if path_type is None else path_type.__name__}
    raise TypeError(f"a parameter type the spec cannot describe: {name}")


def _aliases(func: Any) -> dict | None:
    if func is None:
        return None
    import importlib

    cli_main = importlib.import_module("probe.cli.main")  # the module: `probe.cli.main` is the function
    if func is cli_main._PROJECT_KIND_CONTEXT["token_normalize_func"]:
        return dict(cli_main.LEGACY_PROJECT_KIND_ALIASES)
    raise TypeError(f"a token_normalize_func the spec cannot describe: {func!r}")


def _dump_param(p: Any) -> dict:
    kind = p.param_type_name
    if getattr(p, "callback", None) is not None and kind == "option" and not p.is_eager:
        raise TypeError(f"a callback on {p.name}: the spec would drop what it does")
    out: dict = {"kind": kind, "name": p.name, "opts": list(p.opts), "secondary_opts": list(p.secondary_opts),
                 "type": _dump_type(p.type), "nargs": p.nargs, "multiple": p.multiple, "required": p.required,
                 "expose_value": p.expose_value, "is_eager": p.is_eager,
                 "envvar": p.envvar if isinstance(p.envvar, (str, type(None))) else list(p.envvar),
                 "default": _jsonable(p.default)}
    if kind == "option":
        if p.count:
            raise TypeError(f"a count option ({p.name}): the spec does not describe those")
        out.update(is_flag=bool(p.is_flag), hidden=bool(p.hidden), allow_from_autoenv=bool(p.allow_from_autoenv))
    return out


def _dump_command(cmd: Any) -> dict:
    settings = dict(cmd.context_settings or {})
    out: dict = {
        "group": hasattr(cmd, "commands"),
        "hidden": bool(getattr(cmd, "hidden", False)),
        "context": {
            "help_option_names": settings.get("help_option_names"),
            "ignore_unknown_options": settings.get("ignore_unknown_options"),
            "allow_extra_args": settings.get("allow_extra_args"),
            "allow_interspersed_args": settings.get("allow_interspersed_args"),
            "aliases": _aliases(settings.get("token_normalize_func")),
        },
        "add_help_option": bool(getattr(cmd, "add_help_option", True)),
        "params": [_dump_param(p) for p in cmd.params],
    }
    unknown = set(settings) - {"help_option_names", "ignore_unknown_options", "allow_extra_args",
                               "allow_interspersed_args", "token_normalize_func"}
    if unknown:
        raise TypeError(f"context settings the spec cannot describe: {sorted(unknown)}")
    if out["group"]:
        out["commands"] = {name: _dump_command(sub) for name, sub in sorted(cmd.commands.items())}
    return out


def live_root() -> Any:
    """The real CLI's click tree (imports the whole CLI)."""
    import importlib

    import typer.main

    return typer.main.get_command(importlib.import_module("probe.cli.main").app)


#: Outside `probe/cli`, the modules the CLI's choices come from (`--kind`, `--role`):
#: in the fingerprint too. Any other source of the tree is the nightly `--check`'s.
VOCABULARY = ("sdk/artifact_kinds.py", "sdk/catalog_vocab.py")


def source_sha() -> str:
    """A fingerprint of the CLI's source (every `probe/cli` module and its
    VOCABULARY, by path and bytes; a release bump touches none): the spec names
    the source it was made from, so one older than the CLI it ships beside is
    never used (`load`)."""
    package = Path(__file__).resolve().parent.parent
    digest = hashlib.sha256()
    paths = sorted((package / "cli").rglob("*.py")) + [package / name for name in VOCABULARY]
    for path in paths:
        digest.update(path.relative_to(package).as_posix().encode())
        digest.update(b"\0")
        digest.update(path.read_bytes())
    return digest.hexdigest()


def dump(root: Any | None = None) -> dict:
    from probe import __version__

    return {"format": FORMAT, "cli": str(__version__), "cli_source": source_sha(),
            "root": _dump_command(root if root is not None else live_root())}


def render(spec: dict) -> str:
    """The file's bytes (no version: the tree, not the release, decides staleness)."""
    return json.dumps({"format": spec["format"], "cli_source": spec["cli_source"], "root": spec["root"]},
                      indent=1, sort_keys=True) + "\n"


# -- building (the daemon, at run time) -----------------------------------------------
# Typer's own classes (it carries its own copy of click, `typer._click`): the tree
# parses exactly as the CLI's does. `typer` alone is light (~1 MB); the CLI is not.
def _build_type(d: dict) -> Any:
    from typer import _types as typer_types
    from typer import models as typer_models
    from typer._click import types as kt

    name = d["name"]
    if name == "STRING":
        return kt.STRING
    if name == "BOOL":
        return kt.BOOL
    if name == "INT":
        return kt.INT
    if name == "FLOAT":
        return kt.FLOAT
    if name in ("IntRange", "FloatRange"):
        cls = kt.IntRange if name == "IntRange" else kt.FloatRange
        return cls(d["min"], d["max"], min_open=d["min_open"], max_open=d["max_open"], clamp=d["clamp"])
    if name == "Choice":
        return typer_types.TyperChoice(d["choices"], case_sensitive=d["case_sensitive"])
    if name == "Path":
        path_type = {"str": str, "bytes": bytes, "Path": Path, "PosixPath": Path, None: None}.get(d["path_type"])
        return typer_models.TyperPath(exists=d["exists"], file_okay=d["file_okay"], dir_okay=d["dir_okay"],
                                      writable=d["writable"], readable=d["readable"], resolve_path=d["resolve_path"],
                                      allow_dash=d["allow_dash"], path_type=path_type)
    raise ValueError(f"unknown type {name}")


def _build_param(d: dict) -> Any:
    from typer import core as tc

    common = dict(type=_build_type(d["type"]), required=d["required"], default=d["default"],
                  expose_value=d["expose_value"], is_eager=d["is_eager"], envvar=d["envvar"])
    if d["kind"] == "argument":
        return tc.TyperArgument(param_decls=[d["name"]], nargs=d["nargs"], **common)
    if d["secondary_opts"]:
        decls = [d["name"], "/".join(d["opts"]) + "/" + "/".join(d["secondary_opts"])]
    else:
        decls = [d["name"], *d["opts"]]
    kwargs = dict(param_decls=decls, multiple=d["multiple"], hidden=d.get("hidden", False),
                  allow_from_autoenv=d.get("allow_from_autoenv", True), **common)
    if d.get("is_flag"):
        kwargs["is_flag"] = True
    else:
        kwargs["nargs"] = d["nargs"]
    return tc.TyperOption(**kwargs)


def _settings(d: dict) -> dict:
    context = d["context"]
    settings = {k: v for k, v in context.items() if k != "aliases" and v is not None}
    aliases = context.get("aliases")
    if aliases:
        settings["token_normalize_func"] = lambda token, _a=dict(aliases): _a.get(token, token)
    return settings


def _build_command(name: str, d: dict) -> Any:
    from typer import core as tc

    params = [_build_param(p) for p in d["params"]]
    kwargs = dict(params=params, context_settings=_settings(d), hidden=d["hidden"],
                  add_help_option=d["add_help_option"])
    if d["group"]:
        return tc.TyperGroup(name=name, commands={n: _build_command(n, sub) for n, sub in d["commands"].items()},
                             **kwargs)
    return tc.TyperCommand(name, **kwargs)


#: How long the child that writes the spec for this CLI may take (`_generate`; about 1 s).
GENERATE_TIMEOUT_S = 20.0
#: A copy for another CLI source is removed once it is this old (two installs may share a state folder).
CACHE_KEEP_S = 7 * 86_400.0
_GENERATE_LOCK = threading.Lock()
#: The fingerprints this process already tried to have a spec written for: one child each at most.
_TRIED: set[str] = set()


def _read(path: Path) -> dict | None:
    try:
        spec = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not isinstance(spec, dict) or spec.get("format") != FORMAT or not isinstance(spec.get("root"), dict):
        return None
    return spec


def _cache_key(sha: str) -> str:
    """The copy's name: the CLI source AND this module (its dumper and builder), so a
    copy an older dumper wrote is never read by a newer builder."""
    digest = hashlib.sha256(f"{FORMAT}:{sha}:".encode())
    digest.update(Path(__file__).read_bytes())
    return digest.hexdigest()[:24]


def _cache_path(sha: str) -> Path:
    """Where the spec written for one CLI source lives (the daemon's state folder)."""
    from probe.daemon.store import state_dir

    return state_dir() / "cli-spec" / f"{_cache_key(sha)}.json"


def _generate(target: Path) -> str | None:
    """Write this CLI's spec to `target` from a child process: the whole CLI
    (35 MB) is imported there, for about a second, never in the daemon. The child
    runs as its parent does (`-I` in the host and the workers), from the folder
    that holds `probe` (never the writable cache folder: nothing planted there is
    imported) and with the process's own environment, never a session's (its
    PYTHONPATH may name a research repo with a `probe` package of its own). What
    went wrong, or None."""
    import subprocess

    target.parent.mkdir(parents=True, exist_ok=True)
    flags = ["-I"] if sys.flags.isolated else []
    env = dict(getattr(os.environ, "base", os.environ))  # the process's, not the run's (`runctx.ContextEnviron`)
    package_root = Path(__file__).resolve().parents[2]
    try:
        done = subprocess.run([sys.executable, *flags, "-m", "probe.daemon.cli_spec", "--write-to", str(target)],
                              env=env, cwd=str(package_root), stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                              stderr=subprocess.PIPE, timeout=GENERATE_TIMEOUT_S, check=False)
    except subprocess.TimeoutExpired:
        return f"it took over {GENERATE_TIMEOUT_S:.0f} s"
    if done.returncode != 0:
        tail = (done.stderr or b"").decode("utf-8", "replace").strip().splitlines()[-1:]
        return f"exit {done.returncode}: {tail[0][:200] if tail else ''}"
    return None


def _prune(keep: Path) -> None:
    """Copies for other CLI sources that nobody has written for CACHE_KEEP_S, and
    temp files a killed child left."""
    now = time.time()
    for old in list(keep.parent.glob("*.json")) + list(keep.parent.glob(".*.tmp")):
        if old == keep:
            continue
        with contextlib.suppress(OSError):
            limit = GENERATE_TIMEOUT_S * 2 if old.name.endswith(".tmp") else CACHE_KEEP_S
            if now - old.stat().st_mtime > limit:
                old.unlink()


def _written_for(sha: str) -> dict | None:
    """The copy for this CLI source, written by a child once per process if need be."""
    cache = _cache_path(sha)
    with _GENERATE_LOCK:  # the daemon host's runs ask at once after an update: one child
        spec = _read(cache)
        if spec is not None and spec.get("cli_source") == sha:
            return spec
        if sha in _TRIED:
            return None  # tried in this process already: the CLI's own tree, no second child
        _TRIED.add(sha)
        try:
            why = _generate(cache)
        except Exception as exc:  # noqa: BLE001 -- no spec: the CLI's own tree
            why = f"{type(exc).__name__}: {exc}"
        spec = _read(cache)
        if spec is not None and spec.get("cli_source") == sha:
            _prune(cache)
            return spec
        import logging

        logging.getLogger("probe.daemon").warning(
            "no command spec could be written for this CLI (%s): the CLI's own tree is used",
            why or "the copy written is for another CLI")
        return None


def load(path: Path = SPEC_PATH) -> Any | None:
    """The tree from the spec file. A shipped spec older than the installed CLI
    (any edit to its source makes it so) is replaced, once per CLI source, by
    one a child process writes into the daemon's state folder (`_written_for`).
    None when neither can be had, or when this process has the whole CLI loaded
    already (the CLI's own tree then costs nothing): the caller then builds the
    CLI's own, so a stale spec costs memory, never a refused command."""
    try:
        sha = source_sha()
    except OSError:
        return None
    spec = _read(path)
    if spec is None or spec.get("cli_source") != sha:
        if "probe.cli.main" in sys.modules:
            return None
        spec = _written_for(sha)
        if spec is None:
            return None
    try:
        return _build_command("probe", spec["root"])
    except Exception:  # noqa: BLE001 -- a spec this code cannot build: the real tree
        return None


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    text = render(dump())
    if args[:1] == ["--write"]:
        SPEC_PATH.write_text(text, encoding="utf-8")
        print(f"wrote {SPEC_PATH}")
        return 0
    if args[:1] == ["--write-to"] and len(args) == 2:
        # The daemon's own copy for this CLI (`load`): whole, or not at all.
        from probe._shared.oscompat import replace

        target = Path(args[1])
        tmp = target.with_name(f".{target.name}.{os.getpid()}.tmp")
        try:
            tmp.write_text(text, encoding="utf-8")
            replace(tmp, target)
        except BaseException:
            with contextlib.suppress(OSError):
                tmp.unlink()
            raise
        return 0
    if args[:1] == ["--check"]:
        current = SPEC_PATH.read_text(encoding="utf-8") if SPEC_PATH.exists() else ""
        if current != text:
            print(f"{SPEC_PATH} is stale: run `python -m probe.daemon.cli_spec --write`", file=sys.stderr)
            return 1
        return 0
    sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
