"""The daemon checks `probe` commands against the CLI's tree rebuilt from data (plan M1).

`cli_spec.json` describes the CLI's click tree so the daemon (one daemon host per
machine) never imports the whole CLI and its API client (~33 MB) to check a
command. These keep it the CLI's own: regenerated from the live CLI it must be
byte-equal, and a corpus of commands parses alike through both trees.
"""

from __future__ import annotations

import copy
import subprocess
import sys

import pytest

from probe.daemon import cli_spec, precheck


def test_the_spec_file_is_the_live_clis_tree():
    current = cli_spec.SPEC_PATH.read_text(encoding="utf-8")
    assert current == cli_spec.render(cli_spec.dump()), (
        "agent/src/probe/daemon/cli_spec.json is stale: run `python -m probe.daemon.cli_spec --write`")


def _leaves(cmd, path):
    if hasattr(cmd, "commands"):
        for name, sub in cmd.commands.items():
            yield from _leaves(sub, path + [name])
    else:
        yield path, cmd


def _sample(p) -> str:
    t = type(p.type).__name__
    if "Choice" in t:
        return str(list(p.type.choices)[0])
    if "Range" in t:
        return "1"
    if "Path" in t:
        return "/tmp"
    return {"IntParamType": "3", "FloatParamType": "0.5", "BoolParamType": "true"}.get(t, "x-1")


def _corpus(root) -> list[list[str]]:
    corpus = [[], ["--help"], ["--async"], ["--sync", "run", "list"], ["--base-url", "http://x", "run", "list"],
              ["project", "create", "p", "--kind", "inference"], ["nosuch"], ["run"]]
    for path, cmd in _leaves(root, []):
        argv = list(path)
        corpus += [list(path), path + ["--help"]]
        argv += [_sample(p) for p in cmd.params if p.param_type_name == "argument"]
        corpus.append(list(argv))
        for p in cmd.params:
            if p.param_type_name != "option":
                continue
            if p.is_flag:
                corpus.append(argv + [p.opts[0]])
                if p.secondary_opts:
                    corpus.append(argv + [p.secondary_opts[0]])
            else:
                corpus += [argv + [p.opts[0], _sample(p)], argv + [p.opts[0]], argv + [f"{p.opts[0]}={_sample(p)}"]]
                if p.multiple:
                    corpus.append(argv + [p.opts[0], _sample(p), p.opts[0], _sample(p)])
        corpus += [argv + ["--no-such-flag"], argv + ["extra", "args"], argv + ["--", "a", "b"]]
    return corpus


def _parse(root, argv):
    precheck._ROOT = root
    try:
        parsed = precheck.parse(argv)
        result = ("ok", parsed.path, sorted((k, repr(v)) for k, v in parsed.params.items()), parsed.root_options,
                  parsed.help)
    except precheck.ParseError as exc:
        result = ("refused", str(exc))
    except Exception as exc:  # noqa: BLE001 -- compared as it is
        result = ("raised", type(exc).__name__, str(exc))
    try:
        helps = precheck.asks_help(argv)
    finally:
        precheck._ROOT = None
    return result, helps


@pytest.fixture(scope="module")
def trees(tmp_path_factory):
    # Module-scoped, so set up before the per-test home isolation: a stale spec's
    # copy must never be written into the real state folder.
    with pytest.MonkeyPatch.context() as mp:
        cache = tmp_path_factory.mktemp("cli-spec")
        mp.setattr(cli_spec, "_cache_path", lambda sha: cache / f"{sha[:24]}.json")
        return cli_spec.live_root(), cli_spec.load()


def test_every_command_parses_alike_through_both_trees(trees):
    real, rebuilt = trees
    assert rebuilt is not None
    corpus = _corpus(real)
    assert len(corpus) > 2000  # every command, every option, help, bad flags, `--`
    different = [argv for argv in corpus if _parse(real, argv) != _parse(rebuilt, argv)]
    assert different == []


def test_a_tree_that_differs_from_the_cli_is_caught(trees):
    real, _ = trees
    spec = copy.deepcopy(cli_spec.dump(real))
    tag = spec["root"]["commands"]["run"]["commands"]["tag"]
    first_option = next(p for p in tag["params"] if p["kind"] == "option" and not p.get("is_flag"))
    first_option["opts"] = ["--renamed-for-the-test"]
    mutant = cli_spec._build_command("probe", spec["root"])
    corpus = [argv for argv in _corpus(real) if argv[:2] == ["run", "tag"]]
    assert any(_parse(real, argv) != _parse(mutant, argv) for argv in corpus)


def test_the_daemons_checks_use_the_rebuilt_tree_and_load_no_cli():
    code = ("import sys\n"
            "from probe.cli import mcp_bridge\n"
            "from probe.daemon import precheck\n"
            "assert precheck.parse(['run', 'tag', 'r1', '--add', 'x']).path == 'run tag'\n"
            "print('probe.cli.main' in sys.modules, 'probe.sdk.client' in sys.modules)\n")
    out = subprocess.run([sys.executable, "-I", "-c", code], capture_output=True, text=True, timeout=120)
    assert out.returncode == 0, out.stderr
    assert out.stdout.split() == ["False", "False"]


def test_probe_cli_main_stays_the_function_and_its_seams_still_work(monkeypatch):
    import importlib

    import probe.cli as cli

    importlib.import_module("probe.cli.main")  # binding the submodule leaves the function in place
    assert callable(cli.main) and cli.main.__module__ == "probe.cli"
    sentinel = object()
    monkeypatch.setattr(cli, "Client", sentinel)  # the public monkeypatch seam
    implementation = importlib.import_module("probe.cli.main")
    seen = {}
    monkeypatch.setattr(implementation, "main", lambda argv: seen.setdefault("client", implementation.Client) and 0)
    assert cli.main([]) == 0 and seen["client"] is sentinel
    from probe.cli import app

    assert app is implementation.app
