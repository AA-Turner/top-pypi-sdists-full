"""
`seq volume put | ls | rm` and `seq secret set | ls | rm`: what the account stores on the platform. A secret
value is read from stdin or a hidden prompt only (`getpass`), never from argv, and no command reads one back.
Moved out of seq/cli.py when it reached 1500 lines; the commands and their output are unchanged.


"""
from __future__ import annotations

import argparse
import getpass
import re
import sys
from typing import Any, Callable

from sequence_base.contract import SecretCreateRequest

from seq import columns
from seq._gateway import SecretsClient
from seq.clock import stamp
from seq.cli_json import _print_json
from seq.secret import _validate_secret_name
from sequence_ai.errors import Conflict, InvalidRequest






_ENV_NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*\Z")


def _cmd_secret(args: argparse.Namespace) -> int:
    """`seq secret set | ls | rm`. A failure carries only names, a status and text the gateway client has masked —
    never a value (seq/_gateway.py, and the input checks below) — and `_main` reports it like any other."""
    if args.secret_cmd == "set":
        return _secret_set(args.name, args.env, args.base_url)
    if args.secret_cmd == "ls":
        return _secret_ls(args)
    return _secret_rm(args.name, args.base_url, getattr(args, "force", False))


def _shown(name: str) -> str:
    """A volume's name as a person reads it, as the console's Storage page shows it: a policy's checkpoint, stored as
    deploy:<policy>, by the policy's name. --json keeps the stored name."""
    if name.startswith("deploy:"):
        return name[len("deploy:"):]
    return name


def _used_by(v: dict) -> str:
    """What a volume is in use by, in a few words: its policies by name, then its benchmarks and its eval, each said so -
    "—" for nothing.
"""
    refs = v.get("referenced_by") or {}
    said = [*refs.get("deployments", []), *(f"benchmark {b}" for b in refs.get("benchmarks", [])),
            *(f"eval {e}" for e in refs.get("evals", [])),

            *refs.get("versions", [])]
    return ", ".join(said) or "—"


def _size(v: dict) -> str:


    shared = v.get("shared_size_bytes")
    return ("—" if v["state"] == "uploading"
            else f"{int(shared) / 1e6:.1f} MB shared · not billed" if shared
            else f"{int(v.get('size_bytes') or 0) / 1e6:.1f} MB")


def _replaced(v: dict) -> bool:
    """A volume a later `seq volume put` made a new version of: its earlier versions are billed no more - the platform's
    storage meter reads only the version in use - and `ls` and `show` say so, where the list showed v2 and left whether
    v1 was still billed unsaid.
    
"""
    return v.get("state") == "active" and int(v.get("version") or 0) > 1 and not v.get("shared_size_bytes")


_BILLED_NOTE = "a volume is billed for its version in use alone: the versions a later seq volume put replaced are not"


def volume_list(*, limit: int | None = None, cursor: str | None = None, base_url: str | None = None,
                echo: Callable[[str], Any] | None = None) -> dict:
    """Your volumes, one page - a checkpoint or a dataset you uploaded, a deployment's captured data, an eval's
    recordings - as `seq --json volume ls` prints it: {"data": [{name, kind, state, version, size_bytes,
    referenced_by, ...}, ...], "total", "offset", "next_cursor"}; `limit` rows (default 50) from the `cursor` the page
    before returned as `next_cursor`. Says the table as the command does only when given `echo`."""
    from seq.listing import _footer
    from seq.volume_upload import VolumesClient

    page = VolumesClient(base_url).page(limit=limit, cursor=cursor)
    if echo is not None:
        rows = page["data"]

        head = ["name", "kind", "state", "version", "size", "used by"]
        cells = [[_shown(v["name"]), v["kind"], v["state"], f"v{v['version']}" if v.get("version") else "—",
                  _size(v), _used_by(v)] for v in rows]
        widths = columns.widths([head, *cells])
        echo(columns.line(head, widths))
        for row in cells:
            echo(columns.line(row, widths))
        if any(_replaced(v) for v in rows):
            echo(_BILLED_NOTE)
        if rows:
            _footer(page, len(rows), echo)
    return page


def volume_show(name: str, *, base_url: str | None = None, echo: Callable[[str], Any] | None = None) -> dict:
    """One volume, as `seq --json volume show` prints it: its kind, state, version and size, when it was made and
    changed, and what it is in use by (`referenced_by`: the policies whose weights and the benchmarks whose assets it
    is, an eval's recordings their eval). `name` as `volume_list` names it. Says it as the command does only when given
    `echo`."""
    from seq.volume_upload import VolumesClient

    v = VolumesClient(base_url).get(name)
    if echo is not None:
        ver = f"v{v['version']}" if v.get("version") else "—"

        billed = (("billed", f"{ver} alone; the versions it replaced are not billed"),) if _replaced(v) else ()
        for key, said in (("name", _shown(v["name"])), ("kind", v["kind"]), ("state", v["state"]),
                          ("version", ver), ("size", _size(v)), *billed,
                          ("created", stamp(v.get("created_at"), unit="second", day="always")),
                          ("updated", stamp(v.get("updated_at"), unit="second", day="always")),
                          ("used by", _used_by(v)),):
            echo(f"{key:10}{said}")
    return v


def _cmd_volume(args: argparse.Namespace) -> int:
    """`seq volume put | ls | show | rm` — the volume client prints progress; a failure raises, and `_main` reports
    it."""
    from seq import deps_cost
    from seq.volume_upload import VolumesClient, put, volume_files, volume_get

    try:
        if args.volume_cmd == "put":
            put(args.name, args.path, kind=args.kind, base_url=args.base_url)
            from seq import storage_note

            storage_note.after_write(args.base_url)
            return 0

        if args.volume_cmd == "ls":
            page = volume_list(limit=args.limit, cursor=args.cursor, base_url=args.base_url,
                               echo=None if args.json else print)
            if args.json:
                _print_json(page)
            return 0
        if args.volume_cmd == "show":
            v = volume_show(args.name, base_url=args.base_url, echo=None if args.json else print)
            if args.json:
                _print_json(v)
            return 0
        client = VolumesClient(args.base_url)
        if args.volume_cmd == "files":

            files = volume_files(args.name, args.path, base_url=args.base_url)
            if args.json:
                _print_json({"name": _shown(args.name), "files": files})
                return 0
            if not files:
                print(f"{_shown(args.name)} has no file" + (f" under {args.path}" if args.path else "s"))
                return 0
            head = ["path", "size"]
            cells = [[f["path"], deps_cost.size(f["bytes"])] for f in files]
            widths = columns.widths([head, *cells])
            print(columns.line(head, widths))
            for row in cells:
                print(columns.line(row, widths))
            print(f"{len(files)} file{'s' if len(files) != 1 else ''}")
            return 0
        if args.volume_cmd == "get":
            written = volume_get(args.name, args.path, out=args.out, base_url=args.base_url)
            print(f"downloaded {len(written)} file{'s' if len(written) != 1 else ''} into {args.out}")
            return 0
        if args.volume_cmd == "rm":
            if args.path:


                try:
                    info = client.delete_file(args.name, args.path)
                except Conflict as exc:
                    d = exc.details if isinstance(exc.details, dict) else {}
                    if d.get("reason") == "would_empty":
                        print(f"{args.path} is every file in {args.name}; delete the volume instead: "
                              f"seq volume rm {args.name}", file=sys.stderr)
                    else:
                        who = ", ".join((d.get("deployments") or []) + (d.get("benchmarks") or []))
                        print(f"{args.name} is in use{(' by ' + who) if who else ''}; its files cannot change while it "
                              "is — point what uses it elsewhere, or delete those first", file=sys.stderr)
                    return 1
                print(f"deleted {args.path} from {args.name}; it is now v{info.get('version')}")
                return 0

            client.delete(args.name)
            print(f"deleted {args.name} for good")
            return 0
    except KeyboardInterrupt:
        print("\ninterrupted — run the same command again to resume", file=sys.stderr)
        return 130
    return 2


def _cmd_storage(args: argparse.Namespace) -> int:
    """`seq storage` — the overview: total stored, by kind (checkpoints, datasets, captured data, eval recordings), and
    about what it costs a month at the platform's storage price. A row for a cap and what is left is drawn only when the
    account has one.
"""
    from seq import deps_cost
    from seq.volume_upload import storage

    s = storage(base_url=args.base_url)
    if args.json:
        _print_json(s)
        return 0
    by = s.get("by_kind") or {}
    order = ["checkpoint", "dataset", "captured data", "recordings"]
    rows = [k for k in order if k in by] + [k for k in by if k not in order]
    if rows:
        head = ["kind", "volumes", "size"]
        cells = [[k, str(by[k]["volumes"]), deps_cost.size(by[k]["bytes"])] for k in rows]
        widths = columns.widths([head, *cells])
        print(columns.line(head, widths))
        for row in cells:
            print(columns.line(row, widths))
    total = f"total {deps_cost.size(s['bytes'])}"
    if s.get("monthly_usd") is not None:
        total += (f" · about {deps_cost.money(s['monthly_usd'])}/month "
                  f"at {deps_cost.money(s['usd_per_gb_month'])}/GB-month")
    print(total)
    lim = s.get("limit_bytes")
    if lim is not None:
        from seq import storage_note

        used = int(s.get("used_bytes") or s["bytes"])
        left = max(0, lim - used)
        print(f"{deps_cost.size(used)} of {deps_cost.size(lim)} used · {deps_cost.size(left)} left · "
              f"{storage_note.whose(s)}")

        said = storage_note.note(s)
        if said:
            print(said, file=sys.stderr)
    return 0


def _secret_set(name: str, env_keys: list[str] | None, base_url: str | None) -> int:
    """Validate everything, read each value from stdin, then POST once. Any malformed input raises BEFORE a
    request is built, so nothing partial reaches the gateway (goal 13)."""

    name = _validate_secret_name(name)


    if not env_keys:
        raise InvalidRequest(
            "seq secret set requires at least one --env KEY (e.g. --env MODEL_API_KEY)"
        )

    seen: set[str] = set()
    for key in env_keys:
        if key in seen:
            raise InvalidRequest(f"--env {key} given more than once")
        seen.add(key)
        if not _ENV_NAME.match(key):
            raise InvalidRequest(
                f"{key!r} is not a valid environment-variable name "
                "(letters, digits, underscore; not starting with a digit)"
            )



    interactive = sys.stdin.isatty()
    env: dict[str, str] = {}
    for key in env_keys:
        value = _read_value(key, interactive)
        if value == "":
            raise InvalidRequest(f"empty value for {key}; a secret value cannot be empty")
        env[key] = value


    req = SecretCreateRequest(name=name, env=env)
    SecretsClient(base_url=base_url).create(req)


    print(f"stored secret {name!r} ({', '.join(sorted(env))})")
    return 0


def _read_value(key: str, interactive: bool) -> str:
    """Read one secret value for `key` from stdin. Interactive → prompt on the tty and read without echo;
    piped → one line per KEY, stripped of its trailing newline only."""
    if interactive:

        return getpass.getpass(f"Value for {key} (input hidden): ")
    line = sys.stdin.readline()
    if line == "":

        raise InvalidRequest(
            f"no value for {key} on stdin (pipe one line per --env KEY)"
        )

    return line.rstrip("\n").rstrip("\r")



def _secret_ls(args: argparse.Namespace) -> int:
    """List the caller's secrets as metadata. Zero secrets → an empty list message, not an error."""
    secrets = SecretsClient(base_url=args.base_url).list()
    if args.json:
        _print_json(secrets)
        return 0
    if not secrets:
        print("no secrets")
        return 0


    head = ["name", "env", "created", "last used"]
    cells = [[s.name, ", ".join(s.env_keys) or "—",
              stamp(s.created_at, unit="second", day="always"),
              stamp(s.last_used_at, unit="second", day="always") if s.last_used_at else "never"]
             for s in sorted(secrets, key=lambda x: x.name)]
    widths = columns.widths([head, *cells])
    print(columns.line(head, widths))
    for row in cells:
        print(columns.line(row, widths))
    return 0



def _secret_rm(name: str, base_url: str | None, force: bool = False) -> int:
    """Delete a named secret. A name that does not exist raises NotFound. Refused (409 secret_in_use, listing the
    deployments that bind it) unless `force`; deleting a bound secret then stops those deployments' workers
    (fail-closed). To rotate a leaked value use `seq secret set` instead."""
    name = _validate_secret_name(name)
    SecretsClient(base_url=base_url).delete(name, force=force)
    print(f"deleted secret {name!r}")
    return 0
