"""
`seq` — the one command line: start from a template, deploy a policy or register a benchmark, evaluate one on the
other, and manage what you deployed. Everything runs on the platform; nothing is built, run or stored on this machine.

Every command, a line each: `seq --help` - the one list, kept as seq/cli_parser.py's _OVERVIEW beside the command
tree it describes (this docstring's own copy fell behind it: no adapter, no tasks, no episodes).

`seq deploy` takes a folder (`.` by default) and uploads exactly it; `seq adapter check` takes a <file>:
`path/to/file.py`, `file.py:Class`, `pkg.module:Class`, or `-m pkg.module[:Class]`. The global flags go before the
command: `--json` prints what a command read as JSON.

WHY four verbs and a handful of nouns: the 39 flat commands this replaces mixed the core flow with the management of
what it produced, and a local mock backend shadowed every platform command with a `--remote` twin. With the platform
the only place anything runs, each command does one thing: one verb deploys a folder — `seq deploy [folder]` — and
nouns name what exists.

Where the code lives: this file parses argv and dispatches each command; the command tree and its help are
seq/cli_parser.py, deploy's request, echo and build progress with `policy status` / `policy logs --build` are
seq/deploy_cli.py, volumes and secrets seq/storage_cli.py, `--json` output seq/cli_json.py, and most nouns their own
modules (seq/deployments_cli.py, seq/ops_cli.py, seq/eval_cli.py, ...). Split when this file reached 1500 lines.

A secret VALUE is supplied only through stdin: there is no `--env KEY=VALUE` and no `--value`, so a value never reaches
argv, the shell history or the process listing, and no command reads a value back.

WHY running `seq` is import-deterministic where `python -c` is not: a console script's `sys.path[0]` is the
launcher directory, so the current directory is never prepended to the path. `python -c` prepends the cwd, so
running it from a checkout that ships a top-level `sequence_base/` shadows the installed one — the exact trap a
monorepo dev hits. `seq` sidesteps it: the user types `seq deploy` / `seq eval` / `seq secret`, never `python -c`.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Callable

from seq._http import RetryReads
from seq.cli_json import _print_json


from seq.cli_parser import at_version, _OVERVIEW, build_parser


from seq.deploy_cli import (_BuildProgress, _cmd_build_log, _cmd_status, _deploy_benchmark,
                            _deploy_policy, _print_code, _print_deps, _print_request, _request_of)
from seq.errors import SeqAuthoringError

from seq.loading import load_deployable as _load_deployable
from seq.loading import load_folder as _load_folder
from seq.storage_cli import _cmd_secret, _cmd_storage, _cmd_volume
from sequence_ai._core.capacity import IDLE_S
from sequence_ai.errors import AuthError, InvalidRequest, NotFound, SequencesError, Unavailable


def _page_kw(args: argparse.Namespace) -> dict:
    """The paging flags that were given, as keyword arguments (the list call's own defaults fill the rest)."""
    return {k: getattr(args, k) for k in ("limit", "cursor") if getattr(args, k) is not None}


def main(argv: list[str] | None = None) -> int:
    """`seq …`: parse, run the command, and the exit code. While it runs, the library's transport sends through
    RetryReads too, so a read it makes (`seq models`, `seq gpus`, `seq account`, a policy's status) rides out a failing
    connection as the command's own clients' reads do; put back once it ends - a robot's process never runs this.
    
"""
    from sequence_ai._core import transport

    _line_by_line(sys.stdout)
    transport.send_through(RetryReads)
    try:
        return _main(argv)
    finally:
        transport.send_through(None)


def _line_by_line(stream: Any) -> None:
    """Each line `seq` prints written as it is printed, whatever its stdout is: a script's, CI's or a pipe's held it until
    it filled, and a command that waits - `seq eval replay --no-browser`'s page, `seq eval logs --follow`, `seq eval
    status --watch` - kept its lines from whoever reads them until it ended. A stream that cannot be set so is left as
    it is."""
    if getattr(stream, "line_buffering", True):
        return
    try:
        stream.reconfigure(line_buffering=True)
    except (AttributeError, ValueError, OSError):
        pass


def _your_clock(base_url: str | None) -> None:
    """The times this command prints on your time zone and clock, as `seq login`, `seq account` and `seq account set`
    kept them with this machine's sign-in (person_cli.remember); this machine's zone and 24 hours without one - set afresh
    for each command, so one command's never carries into the next in a process that runs several."""
    from sequence_ai._core import login as signin

    from seq import clock
    from seq.login_cli import _base

    prefs = (signin.saved(_base(base_url)) or {}).get("prefs") or {}
    clock.use(time_zone=prefs.get("time_zone"), clock=prefs.get("clock"))


def _main(argv: list[str] | None = None) -> int:
    ap = build_parser()
    argv, command = _shell_command(list(sys.argv[1:] if argv is None else argv))
    args = ap.parse_args(argv)
    if command is not None:
        args.command = command
    if not args.cmd:
        ap.print_help()
        return 2
    group = ap.seq_groups.get(args.cmd)
    if group is not None and not getattr(args, f"{args.cmd}_cmd", None):
        group.print_help()
        return 2
    if args.json and not _json_ok(args):
        return _report(InvalidRequest(f"`seq {_command(args)}` has no JSON output"))
    _your_clock(args.base_url)
    try:
        return _dispatch(args)
    except KeyboardInterrupt:
        print("\ncancelled", file=sys.stderr)
        return 130
    except Exception as exc:


        if isinstance(exc, (SequencesError, SeqAuthoringError)) or getattr(exc, "code", None) == "policy_error":
            return _report(exc, _command(args))
        raise




_LIST_TITLES = {"fits": "adapters in your account that declare this pair:"}





_OWN_FLAGS = {
    (None, "robots_connected"): "add --force to delete it anyway",
    (None, "secret_in_use"): "add --force to delete it anyway; `seq secret set <name>` gives it a new value instead",
    (None, "machine_cards"): "use --policy-machines 2, or fewer --benchmark-machines",
    ("eval run", "gpu_limit_reached"): "use fewer --policy-machines / --benchmark-machines",
    ("eval run", "envs"): "add --benchmark-machines for more",
    (None, "nothing_to_change"): "give --expires, --limit, or both",
    (None, "budget_exhausted"): ("seq policy set <name> budget.monthly_usd=<usd> (or budget.monthly_usd= to clear it), "
                                 "then seq policy start <name>"),
    (None, "stopped"): "seq policy start <name>",
    (None, "storage_full"): "seq account set --storage-limit <GB>",
    (None, "unauthenticated"): "seq login, or set SEQUENCES_API_KEY",
    (None, "person_only"): "seq login",
    (None, "policy_error"): "seq policy logs <name>",
    ("deploy", "name_held"): "add --override to take it over, or give it another name with --name",
    ("deploy", "name_taken"): "give it another name with --name",
}


def _own_flags(exc: BaseException, command: str | None) -> str | None:
    """The line this CLI says under a refusal in its own flags (_OWN_FLAGS), or None."""
    details = getattr(exc, "details", None) or {}
    code = getattr(exc, "code", None)
    keys = ["budget_exhausted" if code == "budget_exhausted" else None, details.get("reason"),
            "stopped" if details.get("state") == "stopped" else None, details.get("field"), code]
    for key in filter(None, keys):
        for cmd in (command, None):
            if (cmd, key) in _OWN_FLAGS:
                return _OWN_FLAGS[(cmd, key)]
    return None


def _report(exc: BaseException, command: str | None = None) -> int:
    """How every failed command ends, on stderr: `error[<code>]: <detail>`, the
    lists the platform named (each under its title where one is known: _LIST_TITLES), a `hint:` line when there is
    one and another in this CLI's own flags (_OWN_FLAGS), `request_id:` for a 500 — and the exit code of the code's
    row (1 internal, 2 the request, 3 the key, 4 not there or gone, 5 the state, 6 money, 7 worth retrying), so a script
    tells retry from give up without reading the text. A declaration error is the request's (2)."""
    from sequence_ai._core.error_codes import CODES

    code = getattr(exc, "code", None) or ("invalid_request" if isinstance(exc, SeqAuthoringError) else "internal")

    print(f"error[{code}]: {getattr(exc, 'message', None) or exc}", file=sys.stderr)
    for key, items in (getattr(exc, "details", None) or {}).items():
        if isinstance(items, list) and all(isinstance(x, (str, int, float)) for x in items):
            if items and key in _LIST_TITLES:
                print(_LIST_TITLES[key], file=sys.stderr)
            for x in items:
                print(f"  {x}", file=sys.stderr)
    if getattr(exc, "remote_traceback", None):
        print(exc.remote_traceback.rstrip(), file=sys.stderr)
    if getattr(exc, "hint", None):
        print(f"hint: {exc.hint}", file=sys.stderr)
    if (own := _own_flags(exc, command)) is not None:
        print(f"hint: {own}", file=sys.stderr)
    spec = CODES.get(code)
    if getattr(exc, "request_id", None) and spec is not None and spec.status == 500:
        print(f"request_id: {exc.request_id}", file=sys.stderr)
    return spec.exit_code if spec is not None else 1


def _dispatch(args: argparse.Namespace) -> int:
    cmd = args.cmd
    if cmd == "init":
        return _cmd_init(args.template, args.dest, args.list_only, args.base_url,
                         no_source=getattr(args, "no_source", False))
    if cmd == "deploy":
        return _cmd_deploy(args)
    if cmd == "eval":
        return _cmd_eval(args)
    if cmd == "policy":
        return _cmd_policy(args)
    if cmd == "robot":
        return _cmd_robot(args)
    if cmd == "key":
        return _cmd_key(args)
    if cmd == "benchmark":
        return _cmd_benchmark(args)
    if cmd == "port":
        from seq.port import cli as port_cli

        return port_cli.run(args)
    if cmd == "adapter":
        return _cmd_adapter(args)
    if cmd == "volume":
        return _cmd_volume(args)
    if cmd == "storage":
        return _cmd_storage(args)
    if cmd == "secret":
        return _cmd_secret(args)
    if cmd in ("login", "logout"):
        from seq import login_cli

        return (_cmd_platform(args, login_cli.login, profile=args.profile) if cmd == "login"
                else _cmd_platform(args, login_cli.logout, args.id, profile=args.profile))
    if cmd == "profile":
        from seq import login_cli

        sub = args.profile_cmd
        if sub == "activate":
            return _cmd_platform(args, login_cli.profile_activate, args.name)
        if sub == "current":
            return _cmd_platform(args, login_cli.profile_current)
        return _cmd_platform(args, login_cli.profile_list)
    if cmd == "audit":
        from seq import audit_cli

        return audit_cli.run(args)
    if cmd in ("gpus", "account", "usage"):
        return _cmd_account(args)
    if cmd == "billing":
        return _cmd_billing(args)
    return _cmd_models(args)


def _command(args: argparse.Namespace) -> str:
    sub = getattr(args, f"{args.cmd}_cmd", None)
    return f"{args.cmd} {sub}" if sub else args.cmd


def _json_ok(args: argparse.Namespace) -> bool:
    """The commands `--json` applies to: those that read something back. An action (init, a real deploy or eval, an
    upload, a secret write) and doctor's report have no JSON form, and say so rather than ignore the flag. `seq policy
    logs` has one: the page as the platform sends it - the reference's Logs section says the lines are kept that way for
    `seq --json policy logs`."""
    sub = getattr(args, f"{args.cmd}_cmd", None)
    return (args.cmd in ("benchmark", "port", "audit", "models", "gpus", "account", "billing")
            or (args.cmd == "usage" and not args.csv)
            or (args.cmd == "adapter" and sub != "rm")
            or (args.cmd == "deploy" and args.dry_run)
            or (args.cmd == "policy" and sub != "doctor")
            or args.cmd in ("robot", "key")

            or (args.cmd == "eval" and (sub != "run" or args.dry_run)
                and not (getattr(args, "csv", False) and getattr(args, "out", None) is None))
            or (args.cmd == "volume" and sub in ("ls", "show", "files"))
            or args.cmd == "storage"
            or (args.cmd == "secret" and sub == "ls"))


def _require_ref(args: argparse.Namespace) -> str:
    """The target a command names: the positional file / module:Class, or `-m pkg.module[:Class]` — exactly one."""
    target, module = getattr(args, "target", None), getattr(args, "module", None)
    if target and module:
        raise SeqAuthoringError("name the target once: a file (or pkg.module:Class), or -m MODULE")
    if not (target or module):
        raise SeqAuthoringError("name a file (path/to/policy.py), file.py:Class, pkg.module:Class, or -m MODULE")
    return module or target



def _quiet(*_args: Any, **_kwargs: Any) -> None:
    """The `echo` a platform call gets under `seq --json`: its human lines are dropped and its return value printed."""


def _cmd_platform(args: argparse.Namespace, fn: Callable[..., Any], *pos: Any, **kw: Any) -> int:
    """Run one platform call for the CLI: its own lines on success (with `seq --json`, what it returned); a refusal
    raises, and `_main` reports it. Every such call takes `base_url=` and `echo=` and returns what it read."""
    out = fn(*pos, base_url=args.base_url, echo=_quiet if args.json else print, **kw)
    if args.json:
        _print_json(out)
    return 0



def _cmd_eval(args: argparse.Namespace) -> int:
    from seq import eval_cli

    if args.eval_cmd == "run":
        code = eval_cli.eval_remote(args)
        if not args.dry_run:
            from seq import storage_note

            storage_note.after_write(args.base_url)
        return code
    if args.eval_cmd == "status":
        return eval_cli.status(args)
    if args.eval_cmd == "report":
        return eval_cli.report(args)
    if args.eval_cmd == "cancel":
        return eval_cli.cancel(args)
    if args.eval_cmd == "rm":
        from seq import manage_cli

        return _cmd_platform(args, manage_cli.eval_rm, args.eval_id)
    if args.eval_cmd == "replay":
        from seq._replay_player import cli as replay_cli

        return replay_cli.replay(args)
    if args.eval_cmd == "ls":
        return _eval_ls(args)
    if args.eval_cmd == "logs":
        from seq import run_logs

        return _cmd_platform(args, run_logs.eval_logs, args.eval_id, side=args.side, arm=args.arm,
                             machine=args.machine, before=args.before, follow=args.follow, limit=args.limit)
    from seq import listing

    return _cmd_platform(args, listing.episodes, args.eval_id, task=args.task, outcome=args.outcome,
                         arm=args.arm, csv=args.csv, out=args.out, **_page_kw(args))


def _eval_ls(args: argparse.Namespace) -> int:
    """`seq eval ls`: with --benchmark, that benchmark's evals - only the named policy's if one is named - the one way
    to list them; with a policy alone, its evals over time (listing.eval_list)."""
    from seq import listing

    if getattr(args, "adapter", None):
        from seq import adapter_cli

        if any(getattr(args, k, None) is not None for k in ("limit", "cursor", "since")):

            raise InvalidRequest("--adapter lists the newest 200 evals that ran it, all at once; it takes no --limit, "
                                 "--cursor or --since")
        return _cmd_platform(args, adapter_cli.adapter_evals, args.adapter, policy=args.name, benchmark=args.benchmark,
                             status=args.status)
    if getattr(args, "status", None):


        raise InvalidRequest("--status filters an adapter's evals: add --adapter <name>")
    return _cmd_platform(args, listing.eval_list, args.name, benchmark=args.benchmark, since=args.since,
                         **_page_kw(args))


def _shell_command(argv: list[str]) -> tuple[list[str], list[str] | None]:
    """`seq policy shell NAME [options] -- COMMAND...` (and `seq benchmark shell`): its command's words - all after the
    first `--` past `shell`, options of theirs and `--` among them - taken out before the parser reads the rest, which
    an argparse before Python 3.12 does not hand a subcommand whole; (argv, None) for any other command."""
    at = next((i for i in range(len(argv) - 1) if argv[i:i + 2] in (["policy", "shell"], ["benchmark", "shell"])),
              None)
    if at is None or "--" not in argv[at + 2:]:
        return argv, None
    cut = argv.index("--", at + 2)
    return argv[:cut], argv[cut + 1:]


def _cmd_policy(args: argparse.Namespace) -> int:
    from seq import data_cli, deployments_cli as dc

    sub, name = args.policy_cmd, getattr(args, "name", None)
    if sub == "ls":
        return _cmd_platform(args, dc.list_remote, **_page_kw(args))
    if sub == "status":
        return _cmd_status(args)
    if sub == "shell":
        from seq import shell_cli

        out = shell_cli.shell(name, args.command, worker=args.worker, timeout_s=args.timeout, base_url=args.base_url,
                              echo=_quiet if args.json else print)
        if args.json:
            _print_json(out)
        return shell_cli.exit_code(out)
    if sub == "logs":
        name, version = at_version(name)
        if args.build:
            return _cmd_build_log(name, args.base_url, as_json=args.json, version=version)
        if version is not None:
            raise InvalidRequest(f"{args.name} names a version's build: add --build (seq policy logs {args.name} --build)")
        from seq.logs_cli import cmd_logs

        return cmd_logs(name, rid=args.rid, base_url=args.base_url, as_json=args.json, every=args.all,
                        worker=args.worker, since=args.since, before=args.before)
    if sub == "doctor":
        from seq.logs_cli import cmd_doctor

        return cmd_doctor(name, base_url=args.base_url)
    if sub in ("versions", "stop", "start"):
        return _cmd_platform(args, getattr(dc, sub), name)
    if sub == "upgrade":
        from seq import upgrade_cli

        return _cmd_platform(args, upgrade_cli.upgrade, name, kind="policy", to=args.to, dry_run=args.dry_run,
                             wait=args.wait, timeout=args.timeout)
    if sub == "source":
        name, version = at_version(name)
        return _cmd_platform(args, dc.source, name, version, args.out)
    if sub == "rm":
        return _cmd_platform(args, dc.rm, name, force=args.force, dry_run=args.dry_run)
    if sub == "rollback":
        name, version = at_version(name)
        return _cmd_platform(args, dc.rollback, name, version)
    if sub == "rename":
        return _cmd_platform(args, dc.rename, name, args.new)
    if sub == "fork":
        return _cmd_platform(args, dc.fork, args.source, args.new)
    if sub in ("set", "settings"):
        from seq import settings_cli

        if sub == "settings":
            return _cmd_platform(args, settings_cli.policy_settings, name)
        return _cmd_platform(args, settings_cli.policy_set, name, settings_cli.parse_pairs(args.pairs))
    if sub == "data":
        return _cmd_platform(args, data_cli.export, name, args.out, fmt=args.format)
    raise InvalidRequest(f"seq policy {sub} is not a command; `seq policy --help` lists them")


def _cmd_billing(args: argparse.Namespace) -> int:
    """`seq billing top-up | redeem | credits | plan | invoices | details`: the console's Billing page, you signed in
    ."""
    from seq import billing_cli

    sub = args.billing_cmd
    if sub == "top-up":

        said = {"link_echo": lambda line: print(line, file=sys.stderr)} if args.json else {}
        try:
            return _cmd_platform(args, billing_cli.billing_top_up, args.amount, wait=not args.no_wait, **said)
        except KeyboardInterrupt:
            print("stopped waiting; the payment still goes through - `seq billing credits` lists it once it lands")
            return 0
    if sub == "card":
        return _cmd_platform(args, billing_cli.billing_card)
    if sub == "redeem":

        return _cmd_platform(args, billing_cli.redeem_promo_code, args.code)
    if sub == "credits":
        return _cmd_platform(args, billing_cli.billing_credits, page=args.page)
    if sub == "plan":
        return _cmd_platform(args, billing_cli.billing_plan, args.to)
    if sub == "invoices":
        return _cmd_platform(args, billing_cli.billing_invoices, args.number, page=args.page)
    if sub == "details":
        return _cmd_platform(args, billing_cli.billing_details, args.change)
    raise InvalidRequest(f"seq billing {sub} is not a command; `seq billing --help` lists them")


def _cmd_robot(args: argparse.Namespace) -> int:
    """`seq robot add | list | status | revoke`: each robot's own key to a policy (seq/robot_cli.py), and one robot
    connected now (seq/machines_cli.py)."""
    from seq import machines_cli, robot_cli

    if args.robot_cmd == "add":
        return _cmd_platform(args, robot_cli.robot_add, args.policy, expires=args.expires, limit_usd=args.limit)
    if args.robot_cmd == "set":
        kw: dict = {}
        if args.limit is not None:
            if args.limit.strip().lower() == "none":
                kw["limit_usd"] = None
            else:
                try:
                    kw["limit_usd"] = float(args.limit)
                except ValueError:
                    raise InvalidRequest(f"--limit {args.limit!r}: an amount in dollars, or none") from None
        return _cmd_platform(args, robot_cli.robot_set, args.key, expires=args.expires, **kw)
    if args.robot_cmd == "list":
        return _cmd_platform(args, robot_cli.robot_list)
    if args.robot_cmd == "status":
        return _cmd_platform(args, machines_cli.robot_status, args.key, out=args.out)
    if args.robot_cmd == "revoke":
        return _cmd_platform(args, robot_cli.robot_revoke, args.key)
    raise InvalidRequest(f"seq robot {args.robot_cmd} is not a command; `seq robot --help` lists them")


def _cmd_key(args: argparse.Namespace) -> int:
    """`seq key list | add | set | revoke`: your keys, as you."""
    from seq import key_cli

    if args.key_cmd == "list":
        return _cmd_platform(args, key_cli.key_list)
    if args.key_cmd == "add":
        return _cmd_platform(args, key_cli.key_add, args.name, expires=args.expires, limit_usd=args.limit)
    if args.key_cmd == "set":
        kw: dict = {}
        if args.expires:
            kw["expires"] = args.expires
        if args.limit is not None:
            if args.limit.strip().lower() == "none":
                kw["limit_usd"] = None
            else:
                try:
                    kw["limit_usd"] = float(args.limit)
                except ValueError:
                    raise InvalidRequest(f"--limit {args.limit!r}: an amount in dollars, or none") from None
        if not kw:
            raise InvalidRequest("nothing to change: give --expires, --limit or both")
        return _cmd_platform(args, key_cli.key_set, args.key, **kw)
    if args.key_cmd == "revoke":
        return _cmd_platform(args, key_cli.key_revoke, args.key)
    raise InvalidRequest(f"seq key {args.key_cmd} is not a command; `seq key --help` lists them")


def _cmd_account(args: argparse.Namespace) -> int:
    """`seq gpus`, `seq account`, `seq usage`: the cards and their prices, the account's GPUs, what its machines used
    and cost."""
    from seq import capacity_cli

    if args.cmd == "gpus":
        return _cmd_platform(args, capacity_cli.gpus)
    if args.cmd == "account":
        sub = getattr(args, "account_cmd", None)
        if sub in ("set", "delete"):
            from seq import person_cli

            if sub == "delete":
                return _cmd_platform(args, person_cli.account_delete)
            named = {k: getattr(args, k) for k in ("name", "email", "photo", "time_zone", "clock", "storage_limit")
                     if getattr(args, k) is not None}
            return _cmd_platform(args, person_cli.account_set, **named)
        from seq import login_cli

        return _cmd_platform(args, login_cli.account)
    from seq import usage_hist

    if args.csv:

        usage_hist.usage_cli(since=args.since, until=args.until, by=args.by, group=args.group or "none",
                             policy=args.policy, csv_out=True, base_url=args.base_url)
        return 0
    return _cmd_platform(args, usage_hist.usage_cli, since=args.since, until=args.until, by=args.by,
                         group=args.group or "none", policy=args.policy)


def _cmd_adapter(args: argparse.Namespace) -> int:
    """`seq adapter ls / source / rm / check`
."""
    from seq import adapter_cli

    sub = args.adapter_cmd
    if sub == "ls":
        return _cmd_platform(args, adapter_cli.ls, **_page_kw(args))
    if sub == "versions":
        return _cmd_platform(args, adapter_cli.adapter_versions, args.name)
    if sub == "source":
        return _cmd_platform(args, adapter_cli.source, args.name, output=args.out, force=args.force)
    if sub == "rm":
        return _cmd_platform(args, adapter_cli.rm, args.name)
    from seq import adapter_check

    target = _require_ref(args)
    registered = adapter_check.is_registered(target)
    if registered:
        cls = adapter_check.load_registered(target, base_url=args.base_url)
    else:
        kind, cls = _load_deployable(target)
        if kind != "adapter":
            raise SeqAuthoringError(f"{cls.__name__} is a @seq.{kind} class; `seq adapter check` checks a @seq.adapter "
                                    "one")

    out = adapter_check.run(cls, echo=_quiet if args.json else print)
    if args.json:
        _print_json(out)
    return 0


def _cmd_benchmark(args: argparse.Namespace) -> int:
    """`seq benchmark ls`: your benchmarks, a page at a time; `seq benchmark versions <name>`: its versions and their
    builds; `seq benchmark logs <name>`: its eval runs' lines, or a version's build (--build), as a policy's logs read;
    `seq benchmark status <name>`: its build; `seq benchmark rm <name>`: delete one. Its evals
    are `seq eval ls --benchmark <name>`'s."""
    from seq import listing

    if args.benchmark_cmd == "ls":
        return _cmd_platform(args, listing.ls, **_page_kw(args))
    if args.benchmark_cmd == "shell":
        from seq import shell_cli

        name, version = at_version(args.name)
        if args.stop and args.command:

            raise InvalidRequest("--stop only ends the shell machine; it takes no command")
        echo = _quiet if args.json else print
        out = (shell_cli.benchmark_stop(name, base_url=args.base_url, echo=echo) if args.stop else
               shell_cli.benchmark_shell(name, args.command, version=version, timeout_s=args.timeout,
                                         base_url=args.base_url, echo=echo))
        if args.json:
            _print_json(out)
        return 0 if args.stop else shell_cli.exit_code(out)
    if args.benchmark_cmd == "upgrade":
        from seq import upgrade_cli

        return _cmd_platform(args, upgrade_cli.upgrade, args.name, kind="benchmark", to=args.to,
                             dry_run=args.dry_run, wait=args.wait, timeout=args.timeout)
    if args.benchmark_cmd == "cancel":
        from seq import benchmark_cancel_cli

        return _cmd_platform(args, benchmark_cancel_cli.cancel, args.name)
    if args.benchmark_cmd == "rm":
        from seq import benchmark_rm_cli

        return _cmd_platform(args, benchmark_rm_cli.rm, args.name, dry_run=args.dry_run, force=args.force)
    if args.benchmark_cmd == "versions":
        return _cmd_platform(args, listing.versions, args.name)
    if args.benchmark_cmd == "source":
        from seq import benchmark_source_cli

        name, version = at_version(args.name)
        return _cmd_platform(args, benchmark_source_cli.source, name, version, args.out)
    if args.benchmark_cmd == "logs":
        from seq import run_logs

        name, version = at_version(args.name)
        if args.build:
            if args.worker or args.since or args.before:
                raise InvalidRequest("--build is a version's build: --worker, --since and --before read its eval runs' "
                                     "lines")
            return _cmd_platform(args, run_logs.benchmark_build_log, name, version=version)
        if version is not None:
            raise InvalidRequest(f"{args.name} names a version's build: add --build (seq benchmark logs {args.name} "
                                 "--build)")
        return _cmd_platform(args, run_logs.benchmark_runs_logs, name, worker=args.worker, since=args.since,
                             before=args.before)
    if args.benchmark_cmd == "tasks":
        name, version = at_version(args.name)
        return _cmd_platform(args, listing.tasks, name, version=version)
    return _benchmark_status(args)


def _benchmark_status(args: argparse.Namespace) -> int:
    """`seq benchmark status <name> [--wait [--timeout S]]`: listing.benchmark_status, printed - with --json, as data,
    before the refusal a failed build ends in. A wait says each ask again through a lost connection on stderr, as an
    eval's wait prints it, and a build that goes on past its window on stdout."""
    from seq import listing
    from seq.deploy_cli import more_line
    from seq.eval_cli import lost_line

    listing.benchmark_status(args.name, wait=args.wait, timeout=args.timeout, base_url=args.base_url,
                             echo=None if args.json else print, on_retry=lost_line, on_more=more_line(args.name),
                             on_data=_print_json if args.json else None)
    return 0



_MEDIA = (("image", "Images"), ("video", "Video"), ("audio", "Audio"), ("file", "Files"))


def _short_tokens(n: Any) -> str:
    """A context length as the console's Models page shortens it: 1048576 → "1.05M", 128000 → "128K"."""
    if not isinstance(n, (int, float)) or n <= 0:
        return ""
    if n >= 1e6:
        return (f"{n / 1e6:.2f}".rstrip("0").rstrip(".") if n % 1e6 else f"{n / 1e6:.0f}") + "M"
    return f"{int(n / 1e3 + 0.5)}K" if n >= 1e3 else str(int(n))


def _model_cells(m: Any) -> list[str]:
    """One model as the console's Models page rows it: its name and
    kind; its price, "$10.5/M in · $52.5/M out" or "not yet priced"; its context, "128K context"; and what it takes -
    a chat model's inputs beyond text and Reasoning when it reasons, a decide model's Probabilities.
"""
    raw = m.raw or {}
    if m.endpoint == "decide":
        takes = ["Probabilities"]
    else:
        takes = [label for k, label in _MEDIA if k in (raw.get("input_modalities") or [])]
        takes += ["Reasoning"] if "reasoning" in (raw.get("supported_parameters") or []) else []
    ctx = _short_tokens(raw.get("context_length"))
    return [m.short_id, m.architecture or "", " · ".join(f"{r['amount']}/{r['unit']}" for r in m.pricing)
            or "not yet priced", f"{ctx} context" if ctx else "", ", ".join(takes)]


def _cmd_models(args: argparse.Namespace) -> int:
    """`seq models`: the list sequence_ai.models() returns, printed in sections — chat and decide models, then the
    template sections `seq init --list` prints (the same function over the same rows, so the two never differ).
    No flags: all of it; --endpoint narrows it to the models answering there, as models(endpoint=) does. The templates
    alone are `seq init --list`'s - `--kind template` said them a second way, and went
.
    """
    import sequence_ai
    from seq import template_fetch

    rows = sequence_ai.models(endpoint=args.endpoint, base_url=args.base_url)
    if args.json:
        _print_json(rows)
        return 0
    from seq import columns

    lines: list[str] = []

    for ep in [args.endpoint] if args.endpoint else ["chat", "decide"]:
        mine = sorted((m for m in rows if m.kind == "model" and m.endpoint == ep), key=lambda m: m.short_id)
        lines.append(f"{ep} models:")
        cells = [_model_cells(m) for m in mine]
        widths = columns.widths(cells) if cells else []
        lines += [f"  {columns.line(c, widths)}".rstrip() for c in cells] or ["  (none)"]
    if not args.endpoint:
        lines += template_fetch.lines_by_kind([m.raw for m in rows if m.kind == "template"])
    print("\n".join(lines))
    return 0



def _cmd_deploy(args: argparse.Namespace) -> int:
    """`seq deploy [folder]`: find the class the folder deploys (seq.loading.load_folder), assemble and check the
    request here, list the files it uploads, then (unless --dry-run) submit it — a @seq.policy to /v1/deployments, a
    @seq.benchmark to /v1/benchmarks — and by default follow the build to ready.
    """
    kind, cls = _load_folder(args.folder, args.name)
    if kind == "adapter":
        from seq import adapter_cli

        return adapter_cli.deploy(cls, args)
    snaps: list = []
    request = _request_of(kind, cls, name=args.name, require_cap=True, snapshots=snaps)
    if kind == "policy" and not (args.dry_run and args.json):
        from seq import deploy_cli

        deploy_cli.hold_cap_to_account(request, args.base_url)
    said: list[str] = []
    sampled = False
    if kind == "policy":
        from seq import parts




        said = parts.of(cls)
        sampled = parts.names_sample(cls)


        from seq.named import per_step

        step = per_step(cls)
        if step:
            print(f"warning: {step}", file=sys.stderr)
    if args.dry_run:
        if args.json:
            if kind == "policy":
                from seq import deploy_cli



                deploy_cli.request_check(request, base_url=args.base_url)
            print(request.model_dump_json(indent=2))
            return 0
        _print_request(kind, request, snaps[0] if snaps else None, cls)
        for line in said:
            print(line)
        checked = None
        if kind == "policy":
            from seq import deploy_cli




            claim = deploy_cli.name_claim(request.name, request.policy.handler_ref, args.base_url)
            print(deploy_cli.claim_line(request.name, claim))
            if getattr(args, "override", False) and (claim or {}).get("state") in ("version", "replace"):

                print(f"override    the version of {request.name} serving now is deleted for good once this one has "
                      "passed its check and its workers have ended; if this one fails, nothing is deleted")
            deploy_cli.refuse_claim(claim)

            checked = deploy_cli.platform_check(request, override=bool(getattr(args, "override", False)),
                                                base_url=args.base_url)
            print(deploy_cli.platform_line(checked))

            margin = deploy_cli.margin_line(checked)
            if margin:
                print(margin)

            memory = deploy_cli.memory_line(checked)
            if memory:
                print(memory)

            sizes = deploy_cli.weights_parts_line(checked)
            if sizes:
                print(sizes)

            from seq.upgrade_cli import kept_lines

            for line in kept_lines(request.name, (checked or {}).get("kept") or {}):
                print(line)

            for line in deploy_cli.first_start_lines(request.name, checked):
                print(line)
            if checked is not None:


                try:
                    _dry_run_price(request, args)
                except (AuthError, Unavailable) as exc:
                    print(f"price       not read: {exc}")
        elif kind == "benchmark":
            from seq import deploy_cli
            from seq._eval_gateway import EvalGatewayClient



            checked = deploy_cli.registration_check(lambda: EvalGatewayClient(base_url=args.base_url).validate(
                "/v1/benchmarks/validate", content=request.model_dump_json(exclude_none=True),
                headers={"Content-Type": "application/json"},
                params={"override": "true"} if getattr(args, "override", False) else None))
            print(deploy_cli.registration_line("benchmark", checked))
            if (checked or {}).get("replaces"):

                print(f"override    v{checked['replaces']}, the version evals run now, is deleted for good once this one "
                      "has passed its check")

            for line in deploy_cli.registration_price_lines(checked) + deploy_cli.first_start_lines(request.name,
                                                                                                    checked):
                print(line)
        print("\n--dry-run: " + ("the platform checked it and nothing was built" if checked else "nothing was sent")
              + "; without it, `seq deploy` submits this request.")
        return 0
    _print_deps(snaps[0] if snaps else None)
    _print_code(request.code, snaps[0] if snaps else None)
    for line in said:
        print(line)
    if kind == "benchmark":
        return _deploy_benchmark(args, request)
    return _deploy_policy(args, request, snaps[0] if snaps else None, sample=sampled)


def _dry_run_price(request: Any, args: argparse.Namespace) -> None:
    """A policy's price in a dry run, as `seq policy estimate` said it before it was folded in: its card per hour and
    its warm floor - its use priced by the hour, as no use of it is known yet - and, once it has been deployed, what its
    build check measured. Nothing is built.

"""
    from seq import ops_cli


    gpu = (request.resources.gpu or [None])[0]



    view = ops_cli.serving_view(request.name, base_url=args.base_url)
    cap = ops_cli.measured(request.name, None, base_url=args.base_url, echo=print, view=view) if view else None
    card = str(gpu or "cpu").split(":")[0]
    row = next((r for c, r in ((cap or {}).get("by_card") or {}).items() if c.lower() == card.lower()), None)



    batches = bool(request.concurrency.sizes)
    robots = ((view or {}).get("measured") or {}).get("robots") if batches else None



    took = (view or {}).get("new_machine_s")
    start_s = float(took) if isinstance(took, (int, float)) and not isinstance(took, bool) and took > 0 else None
    measured_robots = robots if isinstance(robots, int) and not isinstance(robots, bool) and robots >= 1 else None
    held = int(str(gpu).split(":", 1)[1]) if gpu and ":" in str(gpu) else 1
    per_copy = request.concurrency.gpus_per_replica


    from sequence_ai._core.capacity import wait_steps

    steps = wait_steps(request.policy.action_chunk_valid_len, request.policy.action_chunk_replan_at)
    try:

        ops_cli.estimate(gpu, min_workers=request.autoscaler.min_containers,
                         buffer_workers=request.autoscaler.buffer_containers or 0,
                         max_gpus=request.autoscaler.max_gpus, seats=measured_robots,
                         seats_by=(f"v{view['priced_version']}" if measured_robots and (view or {}).get("priced_version")
                                   else None),
                         batches=batches, copies=max(1, held // per_copy) if per_copy else 1, start_s=start_s,
                         hz=request.policy.hz, chunk_steps=steps, wait_s=request.policy.max_wait_for_batch,
                         base_url=args.base_url, echo=print,

                         idle_s=((view or {}).get("scaling") or {}).get("idle_timeout") or IDLE_S,
                         measured_per_hour=(row or {}).get("usd_per_hour"),
                         deployment=request.name, has_weights=request.weights is not None,


                         weights=request.weights.uri if request.weights is not None else None,
                         weights_others=[r.uri for r in (request.extra_weights or {}).values()],
                         cpu_cores=request.resources.cpu, memory_gib=request.resources.memory_gb)
    except ValueError as exc:
        raise InvalidRequest(str(exc)) from None







def _print_templates(base_url: str | None) -> None:
    """Every template `seq init` can write, by kind, with the version each channel points at."""
    from seq import template_fetch

    print("\n".join(template_fetch.lines_by_kind(template_fetch.list_remote(base_url))))
    print("\nseq init <template>[@stable|@beta|@vN] [directory]")


def _cmd_init(template: str | None, dest: str | None, list_only: bool, base_url: str | None, *,
              no_source: bool = False) -> int:
    """`seq init <template> [directory]`: one version of a template from the platform, by channel or version, unpacked
    into the directory, with the large upstream sources its image installs unless `--no-source`. `--list` shows them
    all."""
    if list_only or not template:
        _print_templates(base_url)
        return 0 if list_only else 2
    if _init_official(template, dest, base_url, no_source=no_source) is None:
        raise NotFound(f"no template named {template.partition('@')[0]!r}", hint="seq init --list shows the templates")
    return 0


def _init_official(spec: str, target: str | None, base_url: str | None, *, no_source: bool = False) -> int | None:
    """Fetch the template from the platform and unpack it; None when the platform has no template by that name. With no
    channel named, the version written is one this sequence-ai deploys (_deployable_version)."""
    from seq import template_fetch

    name, ref = template_fetch.split_ref(spec)
    dest = Path(target or name)

    template_fetch.refuse_occupied(dest)
    got = template_fetch.fetch(name, ref or "stable", base_url)
    if got is None:
        return None
    archive, version = _deployable_version(name, ref, *got, base_url=base_url)



    deploy_name = dest.name
    template_fetch.unpack(archive, dest, template=name, deploy_name=deploy_name)
    print(f"wrote {dest}/ ({name} {version})")
    _init_sources(dest, name, version, base_url, no_source=no_source)
    entry = template_fetch.entry_of(dest)
    readme = f"{dest}/README.md" if (dest / "README.md").exists() else None

    pick = template_fetch.entry_name(dest, entry) if entry else None
    deploy = f"seq deploy {dest}" + (f" --name {pick}" if pick else "")
    if entry == "adapter.py":


        print(f"next: `{deploy}` registers it; name it in an eval with --adapter {name}"
              + (f" (see {readme})" if readme else ""))
    elif entry:


        client = f"{dest}/client.py" if entry == "policy.py" and (dest / "client.py").exists() else None
        after = (f"; on the robot, see {' and '.join(filter(None, (readme, client)))}" if client
                 else f"; see {readme}" if readme else "")
        print(f"next: `{deploy}`{after}")
    return 0


def _deployable_version(name: str, ref: str | None, archive: bytes, version: str, *,
                        base_url: str | None) -> tuple[bytes, str]:
    """
    The version `seq init` writes, and a line when it is not simply the one fetched.

    In one sentence: the version fetched (the stable, with no channel named) is read as `seq deploy` reads it
    (template_fetch.check_archive) → it deploys: written as it is → it does not and no channel was named: the newest
    version this sequence-ai deploys is written instead, said in a line with why the stable is refused → a channel or
    version was named: written as named, with a warning that says which version deploys → none does: the version
    fetched, with a warning.

    WHY: a template's stable moves only on its end-to-end check, so it can stay on a version the SDK has since stopped
    reading - the five pi05 stables use @seq.batched, which 0.35.0 removed - and every `seq init pi05-droid` in the docs
    then wrote files `seq deploy` refused.


    """
    from seq import template_fetch
    from sequence_ai._core.transport import _version

    why = template_fetch.check_archive(archive, name)
    if why is None:
        return archive, version
    sdk = _version()
    other = template_fetch.newest_deployable(name, besides=version, base_url=base_url)
    found = None
    if other is not None:
        found = other[1] + (f" ({other[2]})" if other[2] else "")
    if ref is None and other is not None:
        print(f"{name}'s stable, {version}, does not deploy with this sequence-ai ({sdk}), so this is {found}, the "
              f"newest version that does. {version} is refused with:")
        print(f"  {why}")
        return other[0], other[1]
    asked = f"{name}'s stable, {version}," if ref is None else f"{name} {version}"
    tail = (f"; {found} does: seq init {name}@{other[1]}" if other is not None
            else ", and no newer version of it does either")
    print(f"warning: {asked} does not deploy with this sequence-ai ({sdk}){tail}. {version} is refused with:",
          file=sys.stderr)
    print(f"  {why}", file=sys.stderr)
    return archive, version


def _init_sources(dest: Path, name: str, version: str, base_url: str | None, *, no_source: bool) -> None:
    """The large upstream sources a template version's image installs (third_party/SOURCES.json), downloaded into
    third_party/ and checked, so the folder holds what the deployment runs - or, with --no-source, said and left out.
    A download the platform could not serve leaves the folder deployable (the image installs the official package
    either way) and says how to try again; a package unlike what SOURCES.json names is an error.
    """
    from seq import source, template_fetch
    from sequence_ai.errors import SequencesError

    wanted = source.read_sources(dest)
    if not wanted:
        return
    if no_source:
        names = ", ".join(f"third_party/{s.name} ({s.size / 1e6:.0f} MB)" for s in wanted)
        print(f"left out (--no-source): {names} - the image installs it from its official package; `seq init` "
              "without --no-source downloads the same package to read")
        return
    for s in wanted:
        print(f"downloading third_party/{s.name} ({s.size / 1e6:.0f} MB), the source the image installs...", flush=True)
        try:
            got = source.fetch_sources(dest, template=name, version=version, only=s.name,
                                       get=lambda up: template_fetch.source_stream(name, version, up, base_url))
        except source.SourceMismatch:
            raise
        except SequencesError as exc:
            print(f"  could not download it ({exc}); the folder still deploys - the image installs it from its "
                  f"official package - and `seq init {name}@{version} <another directory>` tries again")
            continue
        for done, n in got:
            print(f"  third_party/{done.name}: {n / 1e6:.0f} MB, as published (package sha256 "
                  f"{done.package_sha256[:12]}, tree sha256 {done.tree_sha256[:12]})")


if __name__ == "__main__":
    raise SystemExit(main())
