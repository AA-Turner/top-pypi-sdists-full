"""
The `seq` command tree: every command and subcommand, its arguments and its help — `build_parser()`, which seq/cli.py's
`main` parses argv with (seq/cli.py keeps the dispatch: which function runs a parsed command). Moved out of seq/cli.py
when it reached 1500 lines; the help texts are unchanged, byte for byte.


Building the parser stays cheap: a command's heavy imports live inside the command, so `seq --help` loads neither numpy
nor mujoco (tests/test_port.py pins it).
"""
from __future__ import annotations

import argparse
import math
from typing import Any


class _DescFromHelp(argparse._SubParsersAction):
    """A subcommand's own --help should say what it does, not list its arguments alone. A command added with a one-line
    `help=` (what the parent's command list shows) and no `description=` gets that help as its description too, so `seq
    <cmd> --help` opens with it; a command that gives a fuller `description=` of its own keeps it. The help stays as the
    parent's list wants it (lower-case, to read after the command name); its description leads a page of its own, so its
    first letter is upper-cased - a description reads as a sentence, and the hand-written ones already begin capital.
    
"""

    def add_parser(self, name, **kwargs):
        help_text = kwargs.get("help")
        if help_text and not kwargs.get("description"):
            kwargs["description"] = help_text[0].upper() + help_text[1:]
        return super().add_parser(name, **kwargs)





_ELSEWHERE = {
    "balance": ("seq account", "seq billing credits"),
    "credit": ("seq account", "seq billing credits"),
    "credits": ("seq account", "seq billing credits"),
    "logs": ("seq policy logs", "seq eval logs"),
    "status": ("seq policy status", "seq eval status"),
}

_SAME = {"delete": "rm", "remove": "rm", "list": "ls"}


def _meant(prog: str, value: str, choices: list[str]) -> list[str]:
    """The one or two commands `prog value` most likely meant: another name for one of `choices`, a command elsewhere
    the word names, else the nearest spellings among `choices`; none when nothing is near."""
    import difflib

    if _SAME.get(value) in choices:
        return [f"{prog} {_SAME[value]}"]
    if value in _ELSEWHERE:
        return list(_ELSEWHERE[value])
    return [f"{prog} {c}" for c in difflib.get_close_matches(value, choices, n=2, cutoff=0.6)]


class _Parser(argparse.ArgumentParser):
    """seq's parser, its subcommands' too (argparse makes those of the parent's class): a command it does not have is
    said in one line with the one or two it most likely meant (_meant), where argparse printed its usage and every
    command at that level - a usage error still, ended as argparse ends one, exit 2.
"""

    def _check_value(self, action: argparse.Action, value: Any) -> None:
        if isinstance(action, argparse._SubParsersAction) and value not in action.choices:
            meant = _meant(self.prog, value, list(action.choices))
            said = (f"did you mean {' or '.join(f'`{m}`' for m in meant)}?" if meant
                    else f"`{self.prog} --help` lists them")

            self.exit(2, f"error[invalid_request]: `{self.prog} {value}` is no command: {said}\n")
        super()._check_value(action, value)


def _template_ref(text: str) -> str:
    """`--to TEMPLATE@vN`: a template's version, named with the template it is of (pi05-droid@v14, as `seq init --list`
    prints it) - a version is always NAME@vN, and `--to` names a template's alone: a deployment's own versions are
    `seq policy rollback NAME@vN`'s."""
    from sequence_ai.errors import InvalidRequest

    if version_alone(text) is not None:
        return f"v{version_alone(text)}"
    name, at, ver = str(text).strip().partition("@")
    try:
        _, version = at_version(f"{name}@{ver}", "template version") if at and name else (None, None)
    except InvalidRequest:
        version = None
    if version is None:
        raise argparse.ArgumentTypeError(f"{text!r} names no template version: write --to TEMPLATE@vN, the template "
                                         "it was made from and one of its versions (e.g. toy-policy@v3)")
    return f"{name}@v{version}"


def _seconds(text: str) -> float:
    """A time limit: seconds above 0, none that never runs out."""
    try:
        seconds = float(text)
    except ValueError:
        seconds = math.nan
    if not 0 < seconds < math.inf:
        raise argparse.ArgumentTypeError(f"{text!r} is no time: seconds above 0, e.g. 3600")
    return seconds


def _time_limit_arg(p: argparse.ArgumentParser, what: str) -> None:
    """`--timeout` of whatever starts a build.
"""
    p.add_argument("--timeout", type=_seconds, default=None, metavar="S",
                   help=f"how long {what} may run, in seconds from when the platform accepts it: then the platform stops "
                        "its build, whatever becomes of this terminal (--no-wait and Ctrl-C included) - its machines "
                        "end, what ran until then is billed, and a command still following it exits non-zero. Without "
                        "it, it runs until it ends, or to the platform's own limit")


def _upgrade_args(p: argparse.ArgumentParser, what: str) -> None:
    """`seq policy upgrade` and `seq benchmark upgrade` take the same arguments."""
    p.add_argument("name", help=f"{what} name")
    p.add_argument("--to", type=_template_ref, default=None, metavar="TEMPLATE@vN",
                   help=f"the template version to move to, any published one of the template the {what} was made "
                        "from: a beta one to try it, or an earlier one to go back (default: its stable one)")
    p.add_argument("--dry-run", action="store_true",
                   help="say what the upgrade changes, keeps and costs, and deploy nothing")
    p.add_argument("--no-wait", dest="wait", action="store_false", default=True,
                   help="return once the new version is accepted, without following its build")
    _time_limit_arg(p, "this upgrade")


def at_version(ref: str, what: str = "version") -> tuple[str, int | None]:
    """`NAME@vN` (or `NAME@N`) as (NAME, N), and a bare NAME as (NAME, None): every command that names a version writes it
    so, as `--adapter name@vN` always has - no --version beside it."""
    from sequence_ai.errors import InvalidRequest

    name, at, ver = str(ref).partition("@")
    if not at:
        return name, None
    v = ver.strip().lstrip("vV")
    if not name or not v.isdigit() or int(v) < 1:
        raise InvalidRequest(f"{ref!r} names no {what}: write NAME@vN, N a whole number from 1 (e.g. {name or 'name'}@v2)")
    return name, int(v)


def version_alone(ref: str) -> int | None:
    """N for `vN` (or `N`) written without the NAME@ of what it is a version of - which no command takes,
    `seq policy upgrade --to` saying the NAME@vN it meant; None for anything else."""
    v = str(ref).strip().lstrip("vV")
    return int(v) if "@" not in str(ref) and v.isdecimal() and int(v) >= 1 else None


def _version() -> str:


    from sequence_ai import __version__

    return __version__




KEY_EXPIRIES = ("7d", "1m", "3m", "6m", "1y", "never")

EVAL_STATES = ("pending", "queued", "running", "completed", "failed", "canceled")

_OVERVIEW = """\
Deploy robot policies and benchmarks to the platform, and evaluate one on the other, with the adapter between them
when their I/O differs. They are built and run on the platform; this machine imports a folder's class to deploy it,
and runs `seq adapter check` and `seq port` itself.

the core flow:
  init <template> [dir]     start from a template: a policy, a benchmark or an adapter (seq init --list)
  deploy [folder]           deploy the folder's @seq.policy, or register its @seq.benchmark or
                            @seq.adapter (--name picks one of several; --dry-run: check it, and price a policy, with
                            nothing built)
  eval run <policy> --benchmark <name> [--adapter <name>@vN]
                            evaluate a deployed policy on a registered benchmark

policy      ls status logs doctor shell debug versions source upgrade rollback stop start rename rm
            set settings fork data
robot       add set list status revoke                    (each robot's own key to a policy, a robot now)
record      add list revoke                               (keys for your own recorder of a policy's steps)
key         list add set revoke                           (your keys: you, signed in)
benchmark   ls tasks versions source logs shell status upgrade cancel rm
adapter     ls versions source rm check
eval        run status cancel rm report episodes replay ls logs
storage     storage · volume put|ls|show|files|get|rm · secret set|ls|rm
account     login · logout · profile · audit · models · gpus · account [set|delete] · usage
billing     top-up redeem credits plan invoices details card    (the console's Billing page; you signed in)
port        export check-model scaffold compare convert   (a CPU MuJoCo or SAPIEN benchmark to the GPU)

A [folder] is uploaded whole (`.` by default), less version control and caches, a virtualenv or build output at its
root, .env files and what a .seqignore leaves out. `seq <command> --help` tells more.
"""


def _target_args(p: argparse.ArgumentParser, what: str) -> None:
    """The file or module `seq adapter check` acts on: `adapter.py`, `adapter.py:Class`, `-m pkg.mod[:Class]`."""
    p.add_argument("target", nargs="?", help=f"the {what}: a file (path/to/adapter.py), file.py:Class, or "
                                             "pkg.module:Class - a registered one's file is downloaded and imported "
                                             "here, running its code")
    p.add_argument("-m", dest="module", default=None, metavar="MODULE",
                   help="a module instead of a file: -m pkg.module[:Class]")


def _page_args(p: argparse.ArgumentParser) -> None:
    """The paging flags of a list: the rows a page holds, and where the next page starts — the `next_cursor` the last
    page printed. The same pages the console's pager steps through.
    """
    p.add_argument("--limit", type=int, default=None, help="rows per page, 1-200 (default 50)")
    p.add_argument("--cursor", default=None, help="the next page: the cursor the previous page printed")


def _group(ap: argparse.ArgumentParser, sub: Any, name: str, description: str) -> Any:
    """A category: `seq <name> <command>`. Kept on the parser so a bare `seq <name>` can print its commands."""
    p = sub.add_parser(name, description=description)
    ap.seq_groups[name] = p
    return p.add_subparsers(dest=f"{name}_cmd", metavar="<command>", action=_DescFromHelp)


def _overview() -> str:
    """`seq --help`'s overview."""
    return _OVERVIEW


def build_parser() -> argparse.ArgumentParser:
    """The `seq` command tree: four core verbs at the top — init, validate, deploy, eval run — and the rest grouped by
    what they act on (policy, benchmark, eval, storage and credentials, account). The categories list their commands
    in `seq --help`; each command's own `--help` explains it. Exposed (not inlined into `main`) so tests can drive it.
    """
    ap = _Parser(prog="seq", description=_overview(), formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.seq_groups = {}
    ap.add_argument("--version", action="version", version=f"seq {_version()}")

    ap.add_argument("--base-url", default=None, help=argparse.SUPPRESS)
    ap.add_argument("--json", action="store_true", help="print what the command read as JSON, for scripts")
    sub = ap.add_subparsers(dest="cmd", metavar="<command>", help="one of the commands above", action=_DescFromHelp)


    p = sub.add_parser("init", description="Start from a template: a policy, a benchmark or an adapter, from the "
                                           "platform, by channel or version.")
    p.add_argument("template", nargs="?",
                   help="a template, optionally with a channel or a version (pi05-droid, pi05-droid@stable, "
                        "pi05-droid@beta, or @vN of a version `seq init --list` shows); without one, its stable "
                        "version when this sequence-ai can deploy it, else the newest version it can")
    p.add_argument("dest", nargs="?", default=None,
                   help="the directory to create (default: the template's name): a policy deploys under it; a "
                        "benchmark or an adapter keeps the name its file gives, which the next step names")
    p.add_argument("--list", action="store_true", dest="list_only", help="list the templates, by kind")
    p.add_argument("--no-source", action="store_true", dest="no_source",
                   help="do not download a template's large upstream sources (third_party/SOURCES.json) - the image "
                        "installs them from their official packages either way")

    p = sub.add_parser("deploy", description="Deploy a @seq.policy, or register a @seq.benchmark, from a folder. "
                                             "The folder is uploaded whole - less version control and caches, a "
                                             "virtualenv or build output at its root, .env files, and what each "
                                             "folder's .seqignore names, each said - and is the version's code: "
                                             "nothing of an earlier version is kept. The class it deploys is the "
                                             "one decorated in it, found by reading its files and then imported "
                                             "here, as on the platform - what its file imports must be installed on "
                                             "this machine; of several, --name picks. A @seq.adapter is registered "
                                             "as a version of its own: its file "
                                             "is sent, nothing is built or run, and the same code is the version it "
                                             "already is.")
    p.add_argument("folder", nargs="?", default=".",
                   help="the folder to deploy (default: this one); it is the code's top, as on your machine")
    p.add_argument("--name", default=None,
                   help="which class of the folder to deploy, by its name= (or class name) when it holds several; "
                        "with one, the deployment's name (default: the decorator's name=, else the class name in "
                        "lower-case with hyphens)")
    p.add_argument("--override", action="store_true",
                   help="replace the version that serves (a benchmark's: the one evals run): it goes on until this "
                        "one has passed its check and serves, then it is deleted for good once its workers and evals "
                        "have ended (without --override every version is kept); and take over a name this account "
                        "holds for another module:Class - a deployment (its robots switch to this policy once it "
                        "builds) or an adapter (its versions stay)")
    p.add_argument("--dry-run", action="store_true",
                   help="check it here and on the platform without building anything: the request and the files it "
                        "uploads, what the platform says of it, and a policy's price per hour, day and month "
                        "(without an API key or a connection: the checks here alone)")
    p.add_argument("--no-wait", dest="wait", action="store_false", default=True,
                   help="return once the build has started (follow it with `seq policy status <name> --wait`, a "
                        "benchmark's with `seq benchmark status <name> --wait`)")
    _time_limit_arg(p, "this deploy")


    esub = _group(ap, sub, "eval", "Evaluate a deployed policy on a registered benchmark, on the platform; read the "
                                   "reports.")
    p_run = esub.add_parser("run", help="evaluate a deployed policy on a registered benchmark",
                            description="Evaluate a deployed policy on a registered benchmark, on the platform. You "
                                        "lay it out: policy machines and their card, and benchmark machines, each on "
                                        "the card the benchmark was registered on - and the platform builds each "
                                        "benchmark machine's worlds. It holds "
                                        "policy machines × their cards + benchmark machines × theirs at once, counted "
                                        "with serving against your account's GPU limit; when they are not free the "
                                        "whole eval waits in line, up to 10 minutes, then fails (queue_timeout). "
                                        "--dry-run says which, before anything starts.")
    p_run.add_argument("policy", metavar="POLICY", help="the deployed policy (see `seq policy ls`); one with a @seq.plan "
                                                        "plans each episode on the robot's clock")
    p_run.add_argument("--benchmark", required=True,
                       help="your registered benchmark: NAME for its latest version that passed its check, NAME@vN for "
                            "any version it keeps (see `seq benchmark versions`)")
    p_run.add_argument("--adapter", default=None,
                       help="the adapter between the sim and the policy's own I/O: a registered one (name@vN, or name "
                            "for its latest; see `seq adapter ls`), or a file, ./my_adapter_user.py[:Class], "
                            "registered first. Without one, an eval whose policy and benchmark do not fit still "
                            "starts, with a warning, and stops at its first act if they really do not")
    p_run.add_argument("--trials", default=None, metavar="N|TASK=N,...",
                       help="how many times each chosen task runs - its declared seeds in order, and past the "
                            "last the same seeds again as repeated starts, marked so - or per task: "
                            "libero_spatial/3=20,*=5 ('*' for the rest; with no --tasks and only per-task entries, "
                            "only the tasks named run)")

    p_run.add_argument("--policy-machines", type=int, default=1, metavar="N",
                       help="policy machines: copies of the policy, each on its own machine (default 1)")
    p_run.add_argument("--benchmark-machines", type=int, default=1, metavar="N",
                       help="benchmark machines per arm, each on the card the benchmark was registered on "
                            "(default 1)")
    p_run.add_argument("--dry-run", action="store_true",
                       help="only estimate wall-clock and cost, report the GPUs - how many, how many are free, "
                            "whether it would wait in line - and the fastest layout within your GPU limit with the "
                            "flags that run it; start nothing")
    p_run.add_argument("--no-wait", dest="wait", action="store_false", default=True,
                       help="return once the eval has started (read it with `seq eval report <id> --wait`)")
    p_cancel = esub.add_parser("cancel", help="stop a running eval: what ran is billed and reported")
    p_cancel.add_argument("eval_id", help="the eval id `seq eval run` printed")

    esub.add_parser("rm", help="delete ended evals for good: their reports, episodes and recordings (a queued or "
                               "running one: seq eval cancel first)").add_argument(
        "eval_id", nargs="+", help="the eval ids seq eval run and seq eval ls print")
    p = esub.add_parser("status", help="an eval's status - pending (accepted, about to start), queued (waiting for "
                                       "GPUs), running, completed, failed or "
                                       "canceled - and how far it has got: episodes done of the total, every metric "
                                       "so far")
    p.add_argument("eval_id", help="the eval id `seq eval run` printed")
    p.add_argument("--watch", action="store_true", help="read it again every few seconds, printing it whenever it "
                                                        "moved, until the eval ends")
    p.add_argument("--every", type=float, default=5.0, help="seconds between reads with --watch (default 5)")
    p_report = esub.add_parser("report", help="read an eval's report")
    p_report.add_argument("eval_id", help="the eval id `seq eval run` printed")
    p_report.add_argument("--wait", action="store_true",
                          help="wait until the eval ends: completed, failed or canceled")
    p_report.add_argument("--timeout", type=float, default=None, help="seconds to wait with --wait (default 7200)")
    from seq import eval_cli

    eval_cli.add_arguments(p_run, p_report)
    p = esub.add_parser("replay", help="watch an eval's episodes in 3D as the console's Replay plays them - orbit, "
                                       "zoom, the timeline - on a page only this machine can open; or a .seqreplay "
                                       "file `seq eval report --replays` saved, offline")
    p.add_argument("target", metavar="EVAL_ID|FILE", help="the eval id `seq eval run` printed, or a .seqreplay file")
    p.add_argument("--episode", type=int, default=None, metavar="N", help="the episode to open first")
    p.add_argument("--no-browser", action="store_true", help="print the page's link, open no browser")
    p = esub.add_parser("ls", help="a deployed policy's evals over time; or with --benchmark, every eval on that "
                                   "benchmark - a page at a time either way; with --adapter, the newest 200 that ran "
                                   "it, at once")
    p.add_argument("name", nargs="?", default=None, help="the deployed policy")
    p.add_argument("--benchmark", default=None,
                   help="every eval on this benchmark of yours, across your policies (only the named policy's if one "
                        "is named)")
    p.add_argument("--since", default=None, help="with --benchmark: evals submitted since a date (2026-10-01), a "
                                                 "time, or a span back from now (7d, 24h)")
    p.add_argument("--adapter", default=None, metavar="NAME[@vN]",
                   help="the evals that ran this adapter of yours - with @vN, that version (only the named policy's, "
                        "or --benchmark's, if one is named)")
    p.add_argument("--status", default=None, choices=EVAL_STATES,
                   help="with --adapter: its evals in this state alone, as the console's adapter page filters them")
    _page_args(p)
    p = esub.add_parser("episodes", help="an eval's episodes, a page at a time - each one's task, seed, steps, seconds "
                                         "on the robot's clock, steps paused waiting for an answer, how it ended "
                                         "and its metrics - by task, outcome or arm (a running eval's too, as far "
                                         "as they have reported)")
    p.add_argument("eval_id", help="the eval id `seq eval run` printed")
    p.add_argument("--task", action="append", default=None, help="only this task's episodes (repeatable)")
    p.add_argument("--outcome", default=None, choices=("success", "failure", "error"),
                   help="only the episodes of this result; success and failure as the benchmark's step said of each, "
                        "a run at its time limit counted a failure and a platform timeout an error")
    p.add_argument("--arm", type=int, default=None, help="only this arm's episodes")
    p.add_argument("--csv", action="store_true",
                   help="every episode these filters take, not a page, as the CSV file the console downloads: on "
                        "stdout, or written to -o PATH")
    p.add_argument("-o", "--out", default=None, metavar="PATH", help="with --csv: the file to write it to")
    _page_args(p)
    p = esub.add_parser("logs", help="an eval's logs: its benchmark machines' output and its policy machines' lines "
                                     "(acts and prints kept 7 days, refused requests 14, the rest 30); --follow until "
                                     "it ends")
    p.add_argument("eval_id", help="the eval id `seq eval run` printed")
    p.add_argument("--side", choices=("benchmark", "policy"), default=None, help="only the benchmark's or the policy's")
    p.add_argument("--arm", type=int, default=None, help="only this arm's benchmark machines")
    p.add_argument("--machine", default=None, metavar="NAME",
                   help="only this machine, by the name its lines carry (a benchmark machine a0-1, a policy machine "
                        "p0-1)")
    p.add_argument("--before", default=None, metavar="WHEN|SEQ",
                   help="the lines before this point: a line's number (the one the last line names to read on back) "
                        "or a time - 30m, 2h, 1d back, or an ISO time (2026-10-18T12:00:00Z)")
    p.add_argument("--follow", action="store_true", help="keep printing new lines until the eval ends")
    p.add_argument("--limit", type=int, default=500,
                   help="how many of the newest lines to start with, 1-2000 (default 500)")

    psub = _group(ap, sub, "policy", "Manage your deployed policies: their builds, logs, versions, traffic, cost and "
                                     "field data.")
    p = psub.add_parser("ls", help="your deployed policies, newest first, a page at a time")
    _page_args(p)
    p = psub.add_parser("shell", help="a terminal in a container of the deployment's worker serving now, or one "
                                      "command run there - what is installed, where its files are, what its card "
                                      "says - its exit code this command's")
    p.add_argument("name", help="deployment name")
    p.add_argument("--worker", default=None, metavar="WORKER",
                   help="the worker to open it on, as seq policy status names them (default: one serving now)")
    p.add_argument("--timeout", type=float, default=30.0, metavar="SECONDS",
                   help="a command's time limit where it runs once - piped, redirected or from a script: up to 120 s "
                        "(default 30)")
    p.add_argument("command", nargs="*",
                   help="after --: the command, e.g. -- pip list, or -- \"nvidia-smi | head -15\" (its options after "
                        "the --, so they are its own): typed at a terminal it runs in one; piped, redirected or from a "
                        "script, once, its output printed. None: a terminal on the worker")
    p = psub.add_parser("debug", help="a machine of its own on the version the deployment serves - its image, card, "
                                      "files and settings, no robot sent to it - that plays its sample episode, from "
                                      "the start each time you run this, with any breakpoint() stopping in your "
                                      "terminal, then a terminal on it")
    p.add_argument("name", help="deployment name")
    p.add_argument("--episode", default=None, metavar="ID",
                   help="play this episode of its field data in place of its sample: the id its robot gave it, as "
                        "seq policy data export writes it")
    p.add_argument("--stop", action="store_true",
                   help="end its debug machine now (else it ends 10 minutes after you leave it)")
    p = psub.add_parser("status", help="a deployment's state (building / ready / failed, and why), its workers — "
                                       "copies, seats, sessions, why one died — and the robots waiting for a slot")
    p.add_argument("name", help="deployment name")
    p.add_argument("--wait", action="store_true", help="poll until the build reaches ready / failed")
    p.add_argument("--timeout", type=float, default=None, help="seconds to wait with --wait (default 1800)")
    logs_said = ("a deployment's logs as events: its machines' starts and ends, its robots joining and leaving, each "
                 "robot's acts folded by run and a print repeated folded with its count (--all: every one), errors, "
                 "slow acts and refused requests on their own - acts and prints are kept 7 days, refused requests 14, "
                 "the rest 30, and none readable once the deployment is removed (seq policy rm) - or one request's "
                 "timeline (--rid)")
    p = psub.add_parser("logs", help=logs_said)
    p.add_argument("name", help="deployment name; NAME@vN with --build: that version's build")
    p.add_argument("--rid", default=None, help="only this request id - an act, a connect or a refused request - its "
                                               "lines joined with the client's own timing")
    p.add_argument("--all", action="store_true", help="every act and every print on its own, not folded")
    p.add_argument("--worker", default=None, metavar="WORKER",
                   help="one worker's events alone: its name as seq policy status and the log show it, e.g. a0001")
    p.add_argument("--since", default=None, metavar="WHEN",
                   help="the events since then: 30m, 2h, 1d back, or an ISO time (2026-10-18T12:00:00Z), every one "
                        "of them, read back a page at a time; left off, the newest page of events, not a window back "
                        "in time")
    p.add_argument("--before", default=None, metavar="WHEN|SEQ",
                   help="the page of events before this point: a line's number (the one the last line names to read "
                        "on back) or a time, in --since's forms; with --since, every event between the two")
    p.add_argument("--build", action="store_true",
                   help="the newest version's build (NAME@vN: that version's): its steps and its log, kept as long as "
                        "its version is")
    p = psub.add_parser("doctor", help="check a deployment on the platform, segment by segment, starting nothing: its "
                                       "state and serving version, its capacity, its last start and a running "
                                       "worker's /ping")
    p.add_argument("name", help="deployment name")
    said = ("a deployment's versions - building, serving, every earlier one kept until you delete it or a deploy "
            "--override replaces it, and the newest 3 failed builds a later deploy replaced, for 7 days - each with "
            "its build: how long it took, why it was built, where a failed one stopped - each build's log kept as long "
            "as its version is")
    p = psub.add_parser("versions", help=said)
    p.add_argument("name", help="deployment name")
    p = psub.add_parser("source", help="the code a version runs, as it deployed it: downloaded into a new folder")
    p.add_argument("name", help="deployment name, or NAME@vN for that version (default: the one serving)")
    p.add_argument("-o", "--out", default=None, metavar="PATH",
                   help="where to write it: a new or empty folder (default: ./<name>-v<N>)")
    p = psub.add_parser("upgrade", help="move a deployment made from a template to the template's newer version: built "
                                        "beside the one serving, what you set differently (weights, resources, "
                                        "concurrency) and its scaling kept; one whose code you changed is "
                                        "refused - deploy the new code")
    _upgrade_args(p, "deployment")
    p = psub.add_parser("rollback", help="serve a kept earlier version again: it serves from now on, nothing rebuilt; "
                                          "robots on another version are disconnected, and each connects again to "
                                          "reach it, after a cold start when none of its workers runs; a version "
                                          "still building is dropped")
    p.add_argument("name", metavar="NAME[@vN]",
                   help="the deployment, or NAME@vN for that kept version as `seq policy versions` lists it (default: "
                        "the version before the one serving)")


    for verb, text, said in (
            ("stop", "end every worker now and refuse connects until `seq policy start` (a version still building "
                     "finishes, and serves once started)",
             "Stop a deployment: every worker ends now, and robots cannot connect until `seq policy start` - a version "
             "still building finishes, and serves once it is started."),
            ("start", "let robots connect to a stopped deployment again",
             "Start a stopped deployment again: robots can connect, and the first to connect starts a worker - not "
             "while this month's spend is at its budget (raise it with `seq policy set <name> "
             "budget.monthly_usd=USD`, or clear it with `budget.monthly_usd=`).")):
        psub.add_parser(verb, help=text, description=said).add_argument("name", help="deployment name")
    p = psub.add_parser("rm", help="delete a deployment for good, listing first what goes with it: its workers end now, "
                                   "its robot keys, versions and weights copy go - its captured data stays as a "
                                   "dataset, and the evals that ran it keep their reports - and its name and quota "
                                   "slot are free; nothing can bring it back (refused while robots are connected or "
                                   "evals run on it, unless --force)")
    p.add_argument("name", metavar="NAME[@vN]", help="deployment name, or NAME@vN to delete that version alone for good: "
                                                     "the policy and its other versions stay, and a version goes once "
                                                     "its workers have ended (the one serving cannot be)")
    p.add_argument("--force", action="store_true", help="delete it with robots connected or evals running on it (the "
                                                        "robots are disconnected, the evals canceled)")
    p.add_argument("--dry-run", action="store_true", help="list what deleting it would touch, and delete nothing")
    p = psub.add_parser("rename", help="give a deployment a new name (its workers end; robots use the new name)")
    p.add_argument("name", help="deployment name")
    p.add_argument("new", help="the new name")


    p = psub.add_parser("set", help="change a deployment's settings without a redeploy, each said with when it takes "
                                    "effect - a machine one (gpu, weights, cpu, memory) builds a new version from the "
                                    "same code: KEY=VALUE ...; KEY= puts one back to what the code says (`seq policy "
                                    "settings` lists them)")
    p.add_argument("name", help="deployment name")
    p.add_argument("pairs", nargs="+", metavar="KEY=VALUE", help="e.g. min_workers=1 max_wait_for_batch=1.7")
    psub.add_parser("settings", help="a deployment's every setting: its value, where it comes from, how far its last "
                                     "change has reached").add_argument("name", help="deployment name")
    p = psub.add_parser("fork", help="copy a policy to a new one of its own - code, settings and weights; nothing of "
                                     "the first changes")
    p.add_argument("source", help="the policy to copy")
    p.add_argument("new", help="the new policy's name")
    p = psub.add_parser("data", help="the field data a deployment captured")
    dsub = p.add_subparsers(dest="data_cmd", required=True, metavar="<command>", action=_DescFromHelp)
    p = dsub.add_parser("export", help="download it as a LeRobot dataset - pip install 'sequence-ai[data]' first - or "
                                       "the raw JSONL")
    p.add_argument("name", help="deployment name, or the dataset a deleted one's data is kept as "
                                "(capture:<name>-<id8>, in `seq volume ls`)")
    p.add_argument("-o", "--out", required=True, metavar="DIR", help="where to write it: a folder")
    p.add_argument("--format", default="lerobot", choices=("lerobot", "jsonl"),
                   help="lerobot (the default): a LeRobot dataset at the policy's hz; jsonl: the kept files as they "
                        "are")



    rsub = _group(ap, sub, "robot", "Each robot's own key to a policy: issue one, change it, list them, see one "
                                    "connected now, revoke one.")
    p = rsub.add_parser("add", help="issue a new robot key to a policy, printed this once")
    p.add_argument("--policy", required=True, help="the policy its robot connects to")
    p.add_argument("--expires", metavar="WHEN", choices=KEY_EXPIRIES,
                   help="when it expires: 7d, 1m, 3m, 6m, 1y or never (default: never)")
    p.add_argument("--limit", type=float, metavar="USD",
                   help="the most its robot may spend, in dollars (default: no cap)")
    p = rsub.add_parser("set", help="change a robot key's expiry or spending limit")
    p.add_argument("key", help="the key's id, or its last four")
    p.add_argument("--expires", metavar="WHEN", choices=KEY_EXPIRIES,
                   help="when it expires: 7d, 1m, 3m, 6m, 1y, or never to lift the expiry")
    p.add_argument("--limit", default=None, metavar="USD|none",
                   help="the most its robot may spend, in dollars; none lifts the limit")
    rsub.add_parser("list", help="the account's robot keys, offline ones too, by their id and last four, each with its "
                                 "connections now, expiry, limit and spend")
    p = rsub.add_parser("status", help="one robot connected now, as the console's Machines page opens it: what its "
                                       "worker holds of each connection - its cameras' newest frames, its episode and "
                                       "step, its link (round trip, retransmits, two-trip uploads), its latest actions "
                                       "and plans")
    p.add_argument("key", help="the key's name, id or last four")
    p.add_argument("-o", "--out", default=None, metavar="DIR",
                   help="save each camera's newest frame here as a JPEG file, <connection>-<camera>.jpg")
    rsub.add_parser("revoke", help="revoke a robot key: its robot is cut off now and connects no more").add_argument(
        "key", help="the key's id, or its last four")



    resub = _group(ap, sub, "record", "Keys for your own recorder of a policy's steps (sequence_ai.record): each step "
                                      "straight from its workers, nothing kept by the platform. Turn it on with "
                                      "`seq policy set <name> record=on`.")
    p = resub.add_parser("add", help="issue a new record key of a policy, printed this once: it reads that policy's "
                                     "steps and opens nothing else")
    p.add_argument("--policy", required=True, help="the policy whose steps it reads")
    p.add_argument("--expires", metavar="WHEN", choices=KEY_EXPIRIES,
                   help="when it expires: 7d, 1m, 3m, 6m, 1y or never (default: never)")
    resub.add_parser("list", help="your record keys, by their id and last four, each with its policy, expiry and last "
                                  "use")
    resub.add_parser("revoke", help="revoke a record key: its recorders are closed now and it connects no more"
                     ).add_argument("key", help="the key's id, or its last four")


    kysub = _group(ap, sub, "key", "Your keys: list them, add one, set its expiry or limit, revoke "
                                   "one - you, signed in (seq login): a key makes no keys.")
    kysub.add_parser("list", help="your keys, newest first: name, last four, what each spent "
                                  "and its limit, when it lapses and was last used, and how many more your plan allows")
    p = kysub.add_parser("add", help="add a key, printed this once")
    p.add_argument("name", help="its name, e.g. ci_user")
    p.add_argument("--expires", required=True, choices=KEY_EXPIRIES, help="when it lapses")
    p.add_argument("--limit", type=float, default=None, metavar="USD", help="what it may spend in all (default: no "
                                                                            "limit)")
    p = kysub.add_parser("set", help="change a key's expiry or limit; what you leave out stays")
    p.add_argument("key", help="the key's id, the first characters of it, or its last four")
    p.add_argument("--expires", choices=KEY_EXPIRIES, default=None, help="when it lapses, from today")
    p.add_argument("--limit", default=None, metavar="USD|none", help="what it may spend in all; none removes the limit")
    kysub.add_parser("revoke", help="revoke a key: it opens nothing within 30 s").add_argument(
        "key", help="the key's id, the first characters of it, or its last four")
    bsub = _group(ap, sub, "benchmark", "Your registered benchmarks (register one with `seq deploy <folder>`).")
    p = bsub.add_parser("upgrade", help="move a benchmark registered from a template to the template's newer version "
                                        "(or back to an earlier one with --to), what you set differently kept; one "
                                        "whose code you changed is refused - register the new code")
    _upgrade_args(p, "benchmark")
    p = bsub.add_parser("ls", help="your benchmarks, newest first: version, status, template, card, worlds, latest "
                                   "eval")
    _page_args(p)
    p = bsub.add_parser("versions", help="a benchmark's versions, newest first - each one's build: its state, how long "
                                         "it took, where a failed one stopped - and the one new evals run")
    p.add_argument("name", help="the benchmark name")
    p = bsub.add_parser("source", help="the code a version runs, as it was registered: downloaded into a new folder")
    p.add_argument("name", metavar="NAME[@vN]",
                   help="the benchmark, or NAME@vN for that version (default: the one new evals run)")
    p.add_argument("-o", "--out", default=None, metavar="PATH",
                   help="where to write it: a new or empty folder (default: ./<name>-v<N>)")
    said = ("a benchmark's logs, as a policy's read: its eval runs are its workers - the lines their machines printed, "
            "the newest 5 runs merged by time, or one (--worker) - and --build is a version's build and check log "
            "(the image build, then the check's own output), kept as long as its version is")
    p = bsub.add_parser("logs", help=said)
    p.add_argument("name", help="the benchmark name; NAME@vN with --build: that version's build")
    p.add_argument("--worker", default=None, metavar="RUN",
                   help="one eval run's lines alone: its eval id, or the start of it, as `seq eval ls --benchmark` "
                        "lists it")
    p.add_argument("--since", default=None, metavar="WHEN",
                   help="the lines since then: 30m, 2h, 1d back, or an ISO time (2026-10-18T12:00:00Z), every one "
                        "of them, each run read back a page at a time")
    p.add_argument("--before", default=None, metavar="WHEN|SEQ",
                   help="each run's lines before this point: a line's number (the one the last line names to read on "
                        "back) or a time, in --since's forms; with --since, every line between the two")
    p.add_argument("--build", action="store_true",
                   help="the latest version's build (NAME@vN: that version's): its phases, its check and its log")
    p = bsub.add_parser("tasks", help="a benchmark's tasks - each one's description, seeds, episodes and time limit - "
                                      "with the template, channel and 3D replay of that version")
    p.add_argument("name", metavar="NAME[@vN]",
                   help="the benchmark, or NAME@vN for that version: the latest, or the latest that passed its check - "
                        "the two whose tasks are kept (default: the current one)")
    p = bsub.add_parser("shell", help="a terminal on a machine of the benchmark's newest version, or one command run "
                                      "there - in its image, on the card it declares: one up already, else one opened "
                                      "for it - its exit code this command's")
    p.add_argument("name", metavar="NAME", help="the benchmark name: a shell runs on its newest version alone")
    p.add_argument("--timeout", type=float, default=30.0, metavar="SECONDS",
                   help="a command's time limit where it runs once - piped, redirected or from a script: up to 120 s "
                        "(default 30)")
    p.add_argument("--stop", action="store_true",
                   help="end its machine now (else it ends 10 minutes after its last command, or after you leave its "
                        "terminal)")
    p.add_argument("command", nargs="*",
                   help="after --: the command, e.g. -- nvidia-smi, or -- \"ls /isaac-sim/exts | head\" (its options "
                        "after the --, so they are its own): typed at a terminal it runs in one; piped, redirected or "
                        "from a script, once, its output printed. None: a terminal on the machine")
    p = bsub.add_parser("status", help="a benchmark's build status (building / ready / failed), the template it comes "
                                       "from, and the driver its card runs with when it names one")
    p.add_argument("name", help="the benchmark name")
    p.add_argument("--wait", action="store_true", help="poll until the build reaches ready / failed")
    p.add_argument("--timeout", type=float, default=None, help="seconds to wait with --wait (default 3600, and up to 3 "
                   "hours while its build log still moves)")
    p = bsub.add_parser("cancel", help="stop the benchmark's registration in flight: its machines end now, billed for "
                                       "what they ran until then, and evals run the version before it",
                        description="Stop a benchmark's registration in flight: the version it was registering is "
                                    "canceled, its machines end, billed for what they ran until then, and evals run "
                                    "the version before it if one passed its check.")
    p.add_argument("name", help="the benchmark name")
    p = bsub.add_parser("rm", help="delete a benchmark for good: what it stores goes, its name and quota place are free at "
                                   "once, and nothing can bring it back; the evals that ran it keep their reports and "
                                   "recordings (refused while an eval runs on it, unless --force). NAME@vN deletes that "
                                   "version alone")
    p.add_argument("name", metavar="NAME[@vN]", help="the benchmark name, or NAME@vN for one version of it")
    p.add_argument("--dry-run", action="store_true", help="say what deleting it would touch; delete nothing")
    p.add_argument("--force", action="store_true", help="cancel the evals running or waiting on it, then delete it")


    asub = _group(ap, sub, "adapter", "Your registered adapters: what maps a benchmark's sim to a policy's own I/O. "
                                      "Register one with `seq deploy <folder>`; name it per eval with --adapter.")
    p = asub.add_parser("ls", help="your adapters: latest version, versions, last eval")
    _page_args(p)

    asub.add_parser("versions", help="an adapter's versions, newest first: when, sha256, class, whether its parameters "
                                     "changed, the lines each changed against the one before, how many evals ran "
                                     "each; and its newest version's pairs").add_argument(
        "name", metavar="NAME[@vN]", help="the adapter name; with @vN, the lines that version changed")
    p = asub.add_parser("source", help="the file a version runs, as it was registered: downloaded to edit and "
                                       "`seq deploy` again")
    p.add_argument("name", help="the adapter name, or NAME@vN for that version (default: its latest)")
    p.add_argument("-o", "--out", default=None, metavar="PATH",
                   help="where to write it: a file (default: its module's file name here)")
    p.add_argument("--force", action="store_true", help="replace a different file already at that path")
    p = asub.add_parser("rm", help="delete an adapter for good, every version (refused while an eval that runs it waits or "
                                   "runs)")
    p.add_argument("name", help="the adapter name")
    p = asub.add_parser("check", help="check an adapter here, without an eval or a GPU: its two methods - the env's "
                                      "observation to the policy's input, the policy's answer to the env's actions - "
                                      "and its pairs; exits non-zero when it declares no pairs")
    _target_args(p, "adapter (or a registered name[@vN])")


    vsub = _group(ap, sub, "volume", "Upload a local directory as a named volume (resumable; files are checked by md5 "
                                     "when it completes; run again, only changed files are sent), list your volumes "
                                     "and what uses each, show one, delete one. Deploy an "
                                     "uploaded checkpoint with weights=seq.Volume.from_name(\"<name>\").")






    p = vsub.add_parser("put", help="upload a directory as a volume (run again: only changed files are sent, and an "
                                    "interrupted upload resumes)",
                        description="Upload a local directory as a volume. Run it again after changing files and only "
                                    "those are sent, as a new version that replaces the one in use - which is billed no "
                                    "more; with none changed it says the volume is already up to date and makes no "
                                    "version. Run again after an interruption, it resumes where it stopped. Each "
                                    "file's size and md5 are checked when the upload completes. Deploy an uploaded "
                                    "checkpoint with "
                                    "weights=seq.Volume.from_name(\"<name>\").")
    p.add_argument("name", help="volume name, e.g. pi05_ft_user")
    p.add_argument("path", help="local directory to upload")
    p.add_argument("--kind", choices=("checkpoint", "dataset"), default="checkpoint",
                   help="what it holds: checkpoint (the default) or dataset - what seq storage counts it as")
    p = vsub.add_parser("ls", help="list your volumes and what uses each, a page at a time",
                        description="Your volumes, a page at a time, each with what uses it: the policies whose "
                                    "weights and the benchmarks whose assets it is.")
    _page_args(p)
    p = vsub.add_parser("show", help="one volume: its version, its size and what uses it - the policies whose weights "
                                     "and the benchmarks whose assets it is",
                        description="One volume: its version, its size and what uses it - the policies whose weights "
                                    "and the benchmarks whose assets it is.")
    p.add_argument("name", help="volume name, as `seq volume ls` prints it")
    p = vsub.add_parser("rm", help="delete a volume for good (refused while a deployment's weights or a benchmark's "
                                   "assets use it)",
                        description="Delete a volume for good, refused while a deployment's weights or a benchmark's "
                                    "assets use it; nothing can bring it back. A policy's own copy of its weights goes with "
                                    "the policy: `seq policy rm`.")
    p.add_argument("name", help="volume name, an eval's recordings (eval:<id>), or a deployment's captured data: "
                                "capture:<name> while it is deployed, capture:<name>-<id8> once it is deleted")
    p.add_argument("path", nargs="?", default=None,
                   help="a file or folder inside a volume you uploaded to delete (an eval's recordings and captured "
                        "data go whole); omit to delete the whole volume. Deleting a file leaves a new version without "
                        "it; refused while a deployment or benchmark uses the volume")

    p = vsub.add_parser("files", help="list every file of a volume, its path and size",
                        description="Every file of a volume you uploaded - a checkpoint or a dataset - each by its "
                                    "path and size, all of them at once; a PATH narrows them to a folder. Also a "
                                    "deployment's "
                                    "captured data (capture:<name>-<id8>) and an eval's recordings (eval:<id>).")
    p.add_argument("name", help="volume name, as `seq volume ls` prints it")
    p.add_argument("path", nargs="?", default=None, help="a folder to narrow the listing to, e.g. params")
    p = vsub.add_parser("get", help="download a volume's files to a local directory (resumable)",
                        description="Download a volume's files into --out, keeping each file's path under it: one file "
                                    "(PATH names a file), a folder (PATH names a folder), or the whole volume (no PATH). "
                                    "A large file whose connection drops resumes with a byte range - run the same "
                                    "command again.")
    p.add_argument("name", help="volume name")
    p.add_argument("path", nargs="?", default=None,
                   help="a file or folder to download; omit for the whole volume")
    p.add_argument("-o", "--out", required=True, metavar="DIR", help="local directory to write the files into")

    ssub = _group(ap, sub, "secret", "Store, list and remove your credential bundles. A secret is one name bound to a "
                                     "set of env vars; values are read from stdin only and are never displayed back. "
                                     "A policy refers to one by name: "
                                     "@seq.policy(secrets=[seq.Secret.from_name('model_key')]).")
    p = ssub.add_parser("set", help="store or rotate a named secret (values read from stdin)")
    p.add_argument("name", help="secret name, e.g. model_key")
    p.add_argument("--env", dest="env", action="append", metavar="KEY", default=None,
                   help="an env-var NAME to store (value is read from stdin, never on the command line); repeatable")
    ssub.add_parser("ls", help="list your secrets by name and env-var names (never values)")
    _secret_rm_p = ssub.add_parser("rm", help="delete a named secret (refused while a deployment uses it, unless --force)")
    _secret_rm_p.add_argument("name", help="secret name to delete")
    _secret_rm_p.add_argument("--force", action="store_true",
                              help="delete even while deployments use it — their workers then stop (fail-closed)")




    p = sub.add_parser("login", description="Sign in on this machine as you, as on the console: a code you confirm on "
                                             "the console's page, opened in your browser (or printed, to open "
                                             "anywhere). Then a command with no SEQUENCES_API_KEY runs as you; keys, "
                                             "payments and the account itself need you signed in.")
    p.add_argument("--profile", metavar="NAME", help="sign in under this name and make it the active profile (seq "
                                                     "profile list): one person's sign-in kept apart from another's")
    p = sub.add_parser("logout", description="Sign out on this machine; with an id from seq account, end that sign-in "
                                             "wherever it is - another machine, a lost one.")
    p.add_argument("id", nargs="?", default=None, help="a sign-in's id, or its first characters, as seq account lists it")
    p.add_argument("--profile", metavar="NAME", help="sign out of this profile (the active one by default)")


    psub = _group(ap, sub, "profile", "The profiles your sign-ins are kept under on this machine: list them, make one "
                                      "active, or say which is. SEQUENCES_PROFILE picks one for a "
                                      "single process.")
    psub.add_parser("list", help="each profile, who is signed in under it at which platform, the active one starred")
    psub.add_parser("activate", help="make a profile the one seq signs in as from now on").add_argument(
        "name", help="the profile's name, as seq profile list shows it")
    psub.add_parser("current", help="the profile seq signs in as now")
    p = sub.add_parser("audit", description="Who did what to your account, newest first, a page at a time.")
    p.add_argument("--limit", type=int, default=50, help="events per page (1-200)")
    p.add_argument("--before", type=int, default=None, help="continue below this event id (the last one shown)")
    p = sub.add_parser("models", description="Everything you can start from: the models the platform serves (chat, "
                                             "decide) and the templates seq init writes (policy, benchmark, "
                                             "adapter) — what sequence_ai.models() returns. The templates alone: "
                                             "seq init --list.")
    p.add_argument("--endpoint", choices=["chat", "decide"], default=None,
                   help="only the models answering on it (a plan's model call: --endpoint chat)")
    sub.add_parser("gpus", description="The cards gpu= can name: memory, price per hour, whether a policy and a "
                                       "benchmark may use it, RT cores, video encoding; and what a CPU core and a "
                                       "GiB of memory cost.")
    acct = sub.add_parser("account", description="What this month has spent under your plan's monthly limit and "
                                                 "the payment method its bill goes to, and your GPUs: the limit, how "
                                                 "many serving, evals, "
                                                 "build checks and shells hold now, how many are left, and the evals waiting for "
                                                 "GPUs. `set` and `delete` change the account as the console's Account "
                                                 "page does - they need you signed in (seq login).")

    asub = acct.add_subparsers(dest="account_cmd", metavar="<command>", action=_DescFromHelp)
    p = asub.add_parser("set", help="change your name, email, photo, time zone, clock or storage limit, as the "
                                    "console's Account page does")
    p.add_argument("--name", help="the name the console shows")
    p.add_argument("--email", help="a new email: a link goes to the old address and one to the new, and the change is "
                                   "made once both are opened")
    p.add_argument("--photo", metavar="PATH|none",
                   help="a PNG, JPEG or WebP file of 2 MB at most, or none to remove it")
    p.add_argument("--time-zone", metavar="ZONE|local", help="the zone the console and the CLI show times in "
                                                            "(Asia/Tokyo), or local for each machine's own")
    p.add_argument("--clock", type=int, choices=(12, 24), help="12- or 24-hour times (24 when never chosen)")
    p.add_argument("--storage-limit", metavar="SIZE|plan",
                   help="everything you keep counts toward it: 500GB, 2TB or a number of GB, with no ceiling of ours "
                        "(storage is billed by the GB); plan for your plan's own")
    asub.add_parser("delete", help="delete the account on the console's Account page, where you confirm it: the page, "
                                   "opened in your browser - nothing is deleted from here")

    bsub = _group(ap, sub, "billing", "Your money as the console's Billing page shows it: a top-up's payment page and "
                                      "the wait for its credit, the credits added, the plan and a move to another, the "
                                      "invoices and the details they print. Each needs you signed in (seq login); a "
                                      "card is typed on the payment page, never here.")
    p = bsub.add_parser("top-up", help="add credit ahead of the month's bill, which it is spent before (billing is "
                                       "postpaid: usage is billed at the month's end): the payment page's link, "
                                       "opened in your browser, then the wait for the credit to land")
    p.add_argument("amount", type=float, metavar="USD", help="how much, $5 at least")
    p.add_argument("--no-wait", action="store_true", help="say the link and return, without waiting for the credit")

    bsub.add_parser("card", help="the payment method your month's bill goes to (billing is postpaid): the page where "
                                 "it is added or made the default, opened in your browser")

    bsub.add_parser("redeem", help="redeem a promotion code from our team: its free credit added to your balance, once "
                                   "per account").add_argument("code", help="the promotion code, as you were given it")
    bsub.add_parser("credits", help="the credits added, newest first: card, invoice payment, starting credit, grant, "
                                    "promotion code").add_argument(
        "--page", type=int, default=1, help="which page: 20 a page, newest first (default 1)")
    bsub.add_parser("plan", help="your plan and every plan; with starter or team, the move to it").add_argument(
        "to", nargs="?", choices=("starter", "team"), help="the plan to move to")
    p = bsub.add_parser("invoices", help="the month so far and the invoices issued; with a NUMBER, that invoice whole")
    p.add_argument("number", nargs="?", help="an invoice's number, as the list shows it")
    p.add_argument("--page", type=int, default=1, help="which page of the invoices issued: 20 a page, newest first "
                                                       "(default 1)")
    bsub.add_parser("details", help="the details invoices print; with --change, the page to change them").add_argument(
        "--change", action="store_true", help="open the page where the details invoices print are changed")
    p = sub.add_parser("storage", description="What you keep on the platform: the total, and by kind - checkpoints, "
                                              "datasets, captured data, eval recordings - how many volumes and how "
                                              "much each, with about what it costs a month at the platform's storage "
                                              "price. `seq volume ls` lists the volumes; `seq volume files` their "
                                              "files.")
    p = sub.add_parser("usage", description="What your machines used and cost: GPU card-hours (seconds x cards / 3600) "
                                            "per hour or day, with what they cost (GPU, CPU and memory) - the "
                                            "console's Usage page. This billing period (the UTC month so far) unless "
                                            "--since / --until name another window, at most 90 days by the hour or day and 400 by "
                                            "the month, in UTC.")
    p.add_argument("--policy", default=None, metavar="NAME",
                   help="one policy's use alone, and what its robots did: their acts, round trips and the share of "
                        "their answers that came before the one they played ran out, as their SDK reports it; a "
                        "benchmark's name reads its eval machines' use")
    p.add_argument("--since", default=None, metavar="WHEN",
                   help="from a date (2026-10-01, midnight UTC), a time, or a span back from now (7d, 24h)")
    p.add_argument("--until", default=None, metavar="WHEN", help="to a date, a time or a span back (default: now)")
    p.add_argument("--by", choices=("hour", "day", "month"), default=None,
                   help="bucket size (default: hours up to a week); month, as the console's twelve months")
    p.add_argument("--group", choices=("deployment", "gpu", "kind"), default=None,
                   help="split each bucket by deployment, card type, or kind of machine (policy workers, evals, "
                        "build checks, weight copies, builds, shells, and extra: a machine started beside the one a "
                        "request got, billed while it held a card)")
    p.add_argument("--csv", action="store_true", help="print the rows as CSV (start, group, card_hours, cost_usd)")




    from seq.port import cli as port_cli

    psub = _group(ap, sub, "port", "Move a CPU MuJoCo or SAPIEN benchmark to the GPU: export its scenes, check the "
                                   "GPU engine builds them the same, scaffold the GPU benchmark, compare its motion - "
                                   "a MuJoCo one's; a SAPIEN port is compared by an eval (convert: the first three in "
                                   "one go).")
    port_cli.add_parsers(psub)
    return ap

