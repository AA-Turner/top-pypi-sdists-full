"""
Registered adapters from the SDK: `seq deploy <folder>` registers an @seq.adapter
class as a version of its own — the same code registered again is the version it already is, and nothing runs on the
platform (no machine, no image); `seq adapter ls / show / pull / rm / check` list, read, download, remove and check
them; `seq eval run --adapter ./file.py:Class` registers the file first and runs the version it is. The Python twins
are `adapters()`, `adapter()`, `adapter_source()`, `register()` and `remove()` here, returning what the gateway answered.

An adapter's steps and stats are not shown: to see or change what it does, pull its file, edit it and deploy it
again as the next version. The lossy / lossless status it used to show is gone too: every adapter is accepted, and
the universal checks apply to the actions it produces.

"""
from __future__ import annotations

import hashlib
import inspect
import json
import os
import re
from typing import Any, Callable

from seq.adapter import _ADAPTER_ATTR
from sequence_ai._core.names import segment

PAGE = 50


def _client(api_key: str | None = None, base_url: str | None = None) -> Any:
    from seq._eval_gateway import EvalGatewayClient

    return EvalGatewayClient(api_key=api_key, base_url=base_url)


def registration_body(cls: type, *, name: str | None = None, override: bool = False,
                      require_pairs: bool = True) -> dict:
    """What POST /v1/adapters takes for an @seq.adapter class: its name, its class and module:Class, the file it is
    defined in, the benchmark → policy pairs it converts between, and the parameters its __init__ declares (only when it
    declares some: none sent is none declared). Its two methods are in its file: nothing
    describes them beside it.
    An adapter that declares no pairs raises AdapterDefinitionError: no version registers without them, as no eval
    runs one. `require_pairs` off reads it all the same, for `seq adapter check` to say so."""
    from seq.adapter import adapter_registration
    from seq.errors import AdapterDefinitionError
    from seq.params import adapter_params
    from sequence_base.contract.adapters import as_json

    reg = adapter_registration(cls)


    from seq.registry import importable

    importable(cls)
    if reg.pairs is None and require_pairs:
        raise AdapterDefinitionError(f"adapter {name or reg.name} declares no pairs: {NO_PAIRS}")
    params = adapter_params(cls)
    with open(inspect.getsourcefile(cls) or "", encoding="utf-8") as f:
        source = f.read()
    return {"name": name or reg.name, "class_name": cls.__name__, "handler_ref": reg.handler_ref, "source": source,
            "override": bool(override),
            **({"pairs": as_json(reg.pairs)} if reg.pairs is not None else {}),

            **({"params": {k: v.model_dump(mode="json", exclude_none=True) for k, v in params.items()}}
               if params else {})}


def register(cls: type, *, name: str | None = None, override: bool = False, api_key: str | None = None,
             base_url: str | None = None) -> dict:
    """Register an @seq.adapter class: {"name", "version", "sha256", "created", ...} — `created` is False when the same
    code was already registered (that version is returned)."""
    return _client(api_key, base_url)._request("POST", "/v1/adapters",
                                               json=registration_body(cls, name=name, override=override))


def adapters(*, limit: int = PAGE, cursor: str | None = None, api_key: str | None = None,
             base_url: str | None = None) -> dict:
    """Your adapters by name, one page: {"adapters": [{"name", "latest", "versions", "class_name", "pairs",
    "created_at", "updated_at", "last_eval"}, ...], "total", "offset", "next_cursor"}."""
    params: dict = {"limit": limit}
    if cursor:
        params["cursor"] = cursor
    return _client(api_key, base_url)._request("GET", "/v1/adapters", params=params)


def adapter(name: str, *, api_key: str | None = None, base_url: str | None = None) -> dict:
    """One adapter: {"name", "versions": [{"version", "sha256", "class_name", "handler_ref", "created_at"}, ...]
    (newest first), "evals": [...]}."""
    return _client(api_key, base_url)._request("GET", f"/v1/adapters/{segment(name)}")


def _fetch_source(ref: str, *, api_key: str | None = None, base_url: str | None = None) -> dict:
    """A registered version's file (name@vN, or name for its latest) as the gateway keeps it, checked against the
    version's sha256 — the platform's own sum of its class name and its file — before anything is written."""
    from sequence_ai.errors import InvalidRequest

    name, at, ver = ref.partition("@v")


    if at and not (ver.isdigit() and int(ver) > 0):
        raise InvalidRequest(f"{ref}: a version is name@vN with N a whole number from 1 (`seq adapter ls` lists its "
                             "versions)")
    got = _client(api_key, base_url)._request("GET", f"/v1/adapters/{segment(name)}/source",
                                              params={"version": int(ver)} if ver else {})
    want = hashlib.sha256(f"{got['class_name']}\n{got['source']}".encode()).hexdigest()
    if want != got["sha256"]:
        raise InvalidRequest(f"{name}@v{got['version']}: the file received does not match its version's sha256; "
                             "nothing was written — try again")
    return got


def file_name(got: dict) -> str:
    """The file a version was registered from, named by its module (toy_adapter:ToyReacherAdapter → toy_adapter.py).
    Only a Python module's name is taken from what the server said — never a path: "x./abs/dir/evil:Cls" wrote outside
    the working directory — else the adapter's own name.
"""
    module = str(got.get("handler_ref") or "").partition(":")[0].rsplit(".", 1)[-1]
    if not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", module):
        module = re.sub(r"[^A-Za-z0-9_]", "_", str(got.get("name") or "adapter"))
    return f"{module}.py"


def adapter_source(name: str, version: int | None = None, *, path: str | None = None, force: bool = False,
                   api_key: str | None = None, base_url: str | None = None) -> str:
    """A registered adapter's file, exactly as it was registered: its text, and, with `path`, written there byte for
    byte — a different file already at `path` stays unless `force` (as `seq adapter source`). `name` may carry its
    version (name@vN); without one, the latest. Edit it and `seq deploy` it again: the next version."""
    ref = name if version is None or "@v" in name else f"{name}@v{int(version)}"
    got = _fetch_source(ref, api_key=api_key, base_url=base_url)
    if path:
        _write(os.path.expanduser(path), got, force=force)
    return got["source"]


def _write(path: str, got: dict, *, force: bool) -> bool:
    """Write a version's file to `path`: False when the same bytes are already there, True once written. A different
    file already there stays unless `force`; a path that cannot be written (a folder, a missing folder, no permission)
    is said as such, not as a traceback.
"""
    from sequence_ai.errors import InvalidRequest

    data = got["source"].encode("utf-8")
    try:
        if os.path.isdir(path):
            raise IsADirectoryError(path)
        if os.path.exists(path):
            with open(path, "rb") as f:
                if f.read() == data:
                    return False
            if not force:
                raise InvalidRequest(f"{path} exists and differs from {got['name']}@v{got['version']}: pass --force "
                                     "to replace it, or -o to write elsewhere")
        with open(path, "wb") as f:
            f.write(data)
    except IsADirectoryError:
        raise InvalidRequest(f"{path} is a folder: name the file to write (-o {os.path.join(path, file_name(got))})") \
            from None
    except OSError as exc:
        raise InvalidRequest(f"{path} could not be written: {exc.strerror or exc}") from None
    return True


def remove(name: str, *, api_key: str | None = None, base_url: str | None = None) -> dict:
    """Remove every version of an adapter — refused while an eval that runs it waits or runs."""
    return _client(api_key, base_url)._request("DELETE", f"/v1/adapters/{segment(name)}")


def is_file_ref(value: str | None) -> bool:
    """`--adapter ./my_adapter.py:MyAdapter` (a local file to register first), as opposed to a registered
    name[@vN]."""
    if not value:
        return False
    target = value.partition(":")[0]
    return target.endswith(".py") or target.startswith(("./", "../", "/", "~"))


def resolve(adapter: Any, *, api_key: str | None = None, base_url: str | None = None,
            echo: Callable[[str], None] = print) -> str | None:
    """What an eval sends as its adapter. A @seq.adapter class, or a local file (`./my_adapter.py[:MyAdapter]`), is
    registered first — the same code is the version it already is — and sent as name@vN; a registered name[@vN] goes as
    written."""
    from sequence_ai.errors import InvalidRequest

    if adapter is None or (isinstance(adapter, str) and not adapter.strip()):
        return None
    if isinstance(adapter, str) and not is_file_ref(adapter):
        return adapter.strip()
    if isinstance(adapter, str):
        from seq.loading import load_deployable

        target, sep, cls_name = adapter.strip().partition(":")
        kind, cls = load_deployable(os.path.expanduser(target) + sep + cls_name)
        if kind != "adapter":
            raise InvalidRequest(f"--adapter {adapter}: {cls.__name__} is a @seq.{kind} class, not a @seq.adapter one")
    elif isinstance(adapter, type) and _ADAPTER_ATTR in adapter.__dict__:
        cls = adapter
    else:
        raise InvalidRequest("adapter= is a registered adapter (name or name@vN, see `seq adapter ls`), a @seq.adapter "
                             "class, or a file: ./my_adapter.py:MyAdapter")
    out = register(cls, api_key=api_key, base_url=base_url)
    print_registered(out, echo=echo, hint=False)
    return f"{out['name']}@v{out['version']}"


def label(adapter: Any, *, at: str = "@v") -> str:
    """How a report names its adapter: name@vN for a registered one (`at=" v"` writes it as the benchmark's and the
    policy's versions are, "name vN"), "no adapter" for none - and one deleted since (the gateway's `deleted`: no later
    adapter of its name is the one it ran) said so, "name (deleted) vN" as a deleted policy's version is said beside
    its name, "name@vN (deleted)" after a reference."""
    if isinstance(adapter, dict):
        name, version = adapter.get("name"), adapter.get("version")
        if not adapter.get("deleted"):
            return f"{name}{at}{version}"
        return f"{name} (deleted){at}{version}" if at == " v" else f"{name}{at}{version} (deleted)"
    return "no adapter"


def _benchmark_said(row: dict) -> str:
    """The benchmark an eval of an adapter ran on, by its name - "(deleted)" beside it for one deleted since (the
    gateway's `benchmark_deleted`, by its id), which a benchmark registered again under its name is not."""
    return f"{row.get('benchmark')}" + (" (deleted)" if row.get("benchmark_deleted") else "")



def print_registered(out: dict, *, echo: Callable[[str], None] = print, hint: bool = True) -> None:
    how = "registered" if out.get("created") else "already registered (the same code: no new version)"
    echo(f"adapter {how}: {out['name']}@v{out['version']}")
    if hint:
        echo(f"use it with: seq eval run <policy> --benchmark <benchmark> --adapter {out['name']}@v{out['version']}")


def deploy(cls: type, args: Any) -> int:
    """`seq deploy <folder>` of an adapter: register it — nothing is built or run, it has no machine of its own; the
    eval that names it runs it in the benchmark's container. --dry-run prints what would be sent and has the platform
    check it, registering nothing (without a key or a connection, the checks here alone)."""
    body = registration_body(cls, name=args.name, override=args.override)
    if args.dry_run:
        if args.json:
            print(json.dumps({**{k: v for k, v in body.items() if k != "source"},
                              "source_bytes": len(body["source"].encode())}, indent=2))
            return 0
        _print_body(body, cls)
        from seq.deploy_cli import registration_check, registration_line



        checked = registration_check(lambda: _client(None, args.base_url).validate("/v1/adapters/validate", json=body))
        print(registration_line("adapter", checked))
        print("\n--dry-run: " + ("the platform checked it and nothing was built" if checked else "nothing was sent")
              + "; without it, `seq deploy` registers this adapter.")
        return 0
    print_registered(register(cls, name=args.name, override=args.override, base_url=args.base_url))
    return 0


def _print_body(body: dict, cls: type | None = None, *, echo: Callable[[str], None] = print) -> None:



    src = body.get("source")
    echo(f"adapter     {body['name']}" + (f"  {len(src.encode())} bytes of source" if src else ""))
    if cls is not None:
        for line in method_lines(cls):
            echo(line)
    for line in pair_lines(body.get("pairs"), none="none declared"):
        echo(line)


def method_lines(cls: type) -> list[str]:
    """Its two methods as `seq deploy --dry-run` and `seq adapter check` print them: which method turns the env's
    observation into the policy's input, and which turns the policy's answer into the env's actions."""
    from seq.adapter import adapter_bindings
    from sequence_base.contract import SeqFlags

    bindings = adapter_bindings(cls)
    return [f"{'observation':<11} {bindings[SeqFlags.OBSERVE]}(obs): the env's observation -> the policy's input",
            f"{'action':<11} {bindings[SeqFlags.ACTION]}(answer): the policy's answer -> the env's actions, one a step"]



NO_PAIRS = ('say which benchmark → policy pairs it converts between - @seq.adapter(pairs=[(benchmark, policy), ...]), '
            'each side a name in your account, template:<name> or *, or pairs="any" - and an eval with any other pair '
            'is refused before anything runs')


def pair_lines(pairs: Any, *, none: str | None = None, indent: str = "") -> list[str]:
    """An adapter's pairs as `seq adapter ls` and `check` print them: "pairs  a → b" and one more line each after;
    `none` for an adapter that declares none (nothing when None)."""
    from sequence_base.contract.adapters import describe

    said = describe(pairs) if pairs is not None else ([none] if none else [])
    return [f"{indent}{'pairs' if i == 0 else '':<11} {line}" for i, line in enumerate(said)]


def _changes(versions: list[dict], text: dict) -> dict:
    """Each version's file against the version before it, as the console's Versions tab says it (seq/line_diff.py):
    "changes" set on each - "first"; "rewritten" past 2,000 changed lines; "class only", the same file under another
    class; else {"added", "removed"} - and {version: its changed lines with three kept around each run of them}."""
    from seq.line_diff import diff_stat, hunks, line_diff

    shown: dict = {}
    for i, v in enumerate(versions):
        before = versions[i + 1] if i + 1 < len(versions) else None
        ops = None if before is None else line_diff(text[before.get("version")], text[v.get("version")])
        stat = diff_stat(ops) if ops is not None else {}
        v["changes"] = ("first" if before is None else "rewritten" if ops is None else
                        stat if stat["added"] or stat["removed"] else "class only")
        if isinstance(v["changes"], dict):
            shown[v.get("version")] = hunks(ops)
    return shown


def adapter_versions(name: str, *, base_url: str | None = None, echo: Callable[[str], None] | None = None) -> dict:
    """`seq adapter versions <name>[@vN]` / seq.adapter_versions: an adapter's versions, newest first - each one's time,
    sha256, class, whether its parameters changed from the version before, the lines its file changed against that one
    (+added −removed; "first", "class only" or "rewritten", as the console's Versions tab says them) and how many evals
    ran it - and its newest version's pairs; with @vN, the lines that version changed, three kept ones around each run
    of them, as its row opens on the console. Returns GET /v1/adapters/{name} as the platform sent it, each version
    with its "changes", and with @vN its "diff" - the lines said. What the console's adapter page shows in Versions and
    its Overview.
"""
    from collections import Counter

    from sequence_ai.errors import InvalidRequest, NotFound
    from seq import clock

    name, at, ver = name.partition("@v")
    if at and not (ver.isdigit() and int(ver) > 0):
        raise InvalidRequest(f"{name}@v{ver}: a version is name@vN with N a whole number from 1")
    got = adapter(name, base_url=base_url) or {}
    vs = list(got.get("versions") or [])
    if ver and not any(str(v.get("version")) == ver for v in vs):
        raise NotFound(f"{name} has no v{ver}: `seq adapter versions {name}` lists its versions")

    diffs = _changes(vs, {v.get("version"): _fetch_source(f"{name}@v{v.get('version')}", base_url=base_url)["source"]
                          for v in vs})
    ran = Counter(e.get("version") for e in got.get("evals") or [])
    say = echo or (lambda _line: None)
    say(f"{got.get('name') or name}  {len(vs)} version{'' if len(vs) == 1 else 's'}")
    for i, v in enumerate(vs):
        before = vs[i + 1] if i + 1 < len(vs) else None
        params = "" if before is None else (" · parameters changed" if (v.get("params") or {}) != (before.get("params")
                                                                                                   or {})
                                            else " · parameters the same")
        c = v["changes"]
        lines = f"+{c['added']} −{c['removed']} lines" if isinstance(c, dict) else c
        n = ran.get(v.get("version"), 0)
        say(f"  v{v.get('version')}  {clock.stamp(v.get('created_at')) if v.get('created_at') else '-'}  "
            f"sha256 {str(v.get('sha256') or '')[:12]}  {v.get('class_name') or '-'}{params} · {lines} · "
            f"{n} eval{'' if n == 1 else 's'}")
    say("pairs (newest version):")
    for line in pair_lines(got.get("pairs"), none="  none declared", indent="  "):
        say(line)
    if ver:
        i = next(i for i, v in enumerate(vs) if str(v.get("version")) == ver)
        got["diff"] = diffs.get(vs[i].get("version"), [])
        said = {"first": "is the first version: there is none before it to compare it with",
                "rewritten": "rewrote the file: more than 2,000 lines changed",
                "class only": "is the file of the version before it under another class name"}
        say(f"v{ver} against v{vs[i + 1].get('version')}:" if got["diff"] else f"v{ver} {said[vs[i]['changes']]}")
        for o in got["diff"]:
            say(f"… {o['text']}" if o["op"] == "…" else f"{o['op']} {o['text']}")
    return got


def adapter_evals(name: str, *, policy: str | None = None, benchmark: str | None = None, status: str | None = None,
                  base_url: str | None = None, echo: Callable[[str], None] | None = None) -> list[dict]:
    """`seq eval ls --adapter <name>[@vN] [--status STATE]`: the evals that ran an adapter - with @vN that version's
    alone, with `status` those in that state alone, and only the named policy's or benchmark's if one is named - each
    by its id, the adapter version, its status, its benchmark and policy, and its figures; as the console's adapter page
    lists them in Evals, by version and by state as its filters pick them.
"""
    from sequence_ai.errors import InvalidRequest

    name, at, ver = name.partition("@v")
    if at and not (ver.isdigit() and int(ver) > 0):
        raise InvalidRequest(f"{name}@v{ver}: a version is name@vN with N a whole number from 1")
    rows = [e for e in (adapter(name, base_url=base_url) or {}).get("evals") or []
            if (policy is None or e.get("model") == policy) and (benchmark is None or e.get("benchmark") == benchmark)
            and (not ver or str(e.get("version")) == ver) and (status is None or e.get("status") == status)]
    if ver:
        name = f"{name}@v{ver}"
    say = echo or (lambda _line: None)
    for e in rows:
        figures = " ".join(f"{k} {v:.3g}" if isinstance(v, (int, float)) else f"{k} -"
                           for k, v in (e.get("metrics") or {}).items())

        say(f"  {str(e.get('eval_id') or '')[:8]}  v{e.get('version')}  {e.get('status')}  "
            f"{_benchmark_said(e)} → {e.get('model')}" + (f"  {figures}" if figures else ""))
    if not rows:
        say(f"no eval ran {name}" + (f" with {policy}" if policy else "") + (f" on {benchmark}" if benchmark else "")
            + (f" ({status})" if status else ""))
    return rows


def ls(*, limit: int = PAGE, cursor: str | None = None, base_url: str | None = None,
       echo: Callable[[str], None] = print) -> dict:
    """`seq adapter ls [--limit N] [--cursor C]`: one page of your adapters, printed."""
    out = adapters(limit=limit, cursor=cursor, base_url=base_url)
    rows = out.get("adapters") or []
    if not rows:
        echo("no adapters yet: register one with `seq deploy <folder>` (try `seq init toy-adapter`)")
        return out
    echo(f"{'name':<24} {'latest':>6} {'versions':>8}  last eval")
    for a in rows:
        last = a.get("last_eval") or {}

        used = (f"{str(last.get('eval_id'))[:8]} v{last.get('version')} on {_benchmark_said(last)} with "
                f"{last.get('model')}") if last else "-"
        echo(f"{a['name']:<24} {'v' + str(a['latest']):>6} {a['versions']:>8}  {used}")
        for line in pair_lines(a.get("pairs"), none="none declared (registered before pairs): an eval refuses it",
                               indent="  ") if "pairs" in a else []:
            echo(line)
    if out.get("next_cursor"):
        echo(f"more: seq adapter ls --cursor {out['next_cursor']}")
    return out


def source(ref: str, *, output: str | None = None, force: bool = False, base_url: str | None = None,
           echo: Callable[[str], None] = print) -> dict:
    """`seq adapter source <name>[@vN] [-o PATH] [--force]`: a version's file, byte for byte as it was registered, to
    PATH (default: its module's file name here) - as `seq policy source` writes a policy version's code. A different
    file already there stays unless --force; the same one is left as it is. It was `seq adapter pull`, a name of its
    own for the same thing."""
    got = _fetch_source(ref, base_url=base_url)
    path = os.path.expanduser(output or file_name(got))
    data = got["source"].encode("utf-8")
    sha = hashlib.sha256(data).hexdigest()
    out = {"name": got["name"], "version": got["version"], "path": path, "bytes": len(data), "sha256": sha,
           "written": False}
    if not _write(path, got, force=force):
        echo(f"{path} is already {got['name']}@v{got['version']}")
        return out
    out["written"] = True
    echo(f"{got['name']}@v{got['version']} -> {path}  ({len(data)} bytes, sha256 {sha[:12]})")
    echo(f"edit it, then `seq deploy {os.path.dirname(path) or '.'} --name {got['name']}` registers the next version")
    return out


def rm(name: str, *, base_url: str | None = None, echo: Callable[[str], None] = print) -> dict:
    """`seq adapter rm <name>`: every version deleted for good — refused while an eval that runs it waits or runs."""
    out = remove(name, base_url=base_url)
    echo(f"deleted {out['name']} for good ({out['deleted_versions']} version(s))")
    return out


