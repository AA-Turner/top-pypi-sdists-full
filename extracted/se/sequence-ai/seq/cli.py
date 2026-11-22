"""
`seq` — the open command line: start from a template (`seq init`), serve a policy from this machine's GPU (`seq serve`)
and download a template's weights (`seq weights get`). sequence-cloud, GS's client for its platform, adds the
platform's commands - deploy, eval, policy, gpu, account and the rest - to this same `seq` through the `seq.commands`
entry point (sequence_ai/_core/plugins.py): this file parses argv, runs its own three commands and hands every other to
it - a shell command's own words (split), whether it prints JSON (json_ok), your clock (prepare), the run (dispatch)
and a failure's report (report); the command tree is seq/cli_parser.py, which it mounts its commands on (register).

WHY running `seq` is import-deterministic where `python -c` is not: a console script's `sys.path[0]` is the
launcher directory, so the current directory is never prepended to the path. `python -c` prepends the cwd, so
running it from a checkout that ships a top-level `sequence_base/` shadows the installed one — the exact trap a
monorepo dev hits. `seq` sidesteps it: the user types `seq deploy` / `seq eval` / `seq secret`, never `python -c`.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from seq._http import RetryReads
from seq.cli_parser import _OVERVIEW, build_parser
from seq.errors import SeqAuthoringError
from sequence_ai._core.plugins import first, needs_cloud
from sequence_ai.errors import InvalidRequest, NotFound, SequencesError


_OWN = ("init", "serve", "weights", "teleop", "data")


_OPEN_FLAGS = {"unauthenticated": "set SEQUENCES_API_KEY"}


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



def _plugin() -> Any:
    """sequence-cloud's commands (the `seq.commands` entry point), or None where it is not installed."""
    return first("seq.commands")


def _main(argv: list[str] | None = None) -> int:
    ap = build_parser()
    plugin = _plugin()
    argv = list(sys.argv[1:] if argv is None else argv)

    argv, command = plugin.split(argv) if plugin is not None else (argv, None)
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

    if args.json and not (plugin is not None and plugin.json_ok(args)):
        return _failed(plugin, InvalidRequest(f"`seq {_command(args)}` has no JSON output"))
    if plugin is not None:
        plugin.prepare(args)
    try:
        return _dispatch(args) if args.cmd in _OWN else plugin.dispatch(args)
    except KeyboardInterrupt as exc:

        print(f"\n{exc}" if str(exc) else "\ncancelled", file=sys.stderr)
        return 130
    except Exception as exc:


        if isinstance(exc, (SequencesError, SeqAuthoringError)) or getattr(exc, "code", None) == "policy_error":
            return _failed(plugin, exc, _command(args))
        raise


def _failed(plugin: Any, exc: BaseException, command: str | None = None) -> int:
    """A failed command's report: sequence-cloud's (its commands' own words under a refusal) where it is installed, else
    _report with this CLI's (_OPEN_FLAGS)."""
    if plugin is not None:
        return plugin.report(exc, command)
    return _report(exc, command, own=_OPEN_FLAGS.get(getattr(exc, "code", None)))


def _report(exc: BaseException, command: str | None = None, *, titles: dict | None = None, said: Any = (),
            own: str | None = None) -> int:
    """How every failed command ends, on stderr: `error[<code>]: <detail>`, the
    lists the platform named (each under its title where one is known: `titles`; none its sentence already says:
    `said`), a `hint:` line when there is one and another in this CLI's own flags (`own`: sequence-cloud's report
    passes its commands', this file its own, _OPEN_FLAGS), `request_id:` for a 500 — and the exit code of the code's
    row (1 internal, 2 the request, 3 the key, 4 not there or gone, 5 the state, 6 money, 7 worth retrying), so a script
    tells retry from give up without reading the text. A declaration error is the request's (2)."""
    from sequence_ai._core.error_codes import CODES

    code = getattr(exc, "code", None) or ("invalid_request" if isinstance(exc, SeqAuthoringError) else "internal")

    print(f"error[{code}]: {getattr(exc, 'message', None) or exc}", file=sys.stderr)
    for key, items in (getattr(exc, "details", None) or {}).items():
        if key in said:
            continue
        if isinstance(items, list) and all(isinstance(x, (str, int, float)) for x in items):
            if items and key in (titles or {}):
                print(titles[key], file=sys.stderr)
            for x in items:
                print(f"  {x}", file=sys.stderr)
    if getattr(exc, "remote_traceback", None):
        print(exc.remote_traceback.rstrip(), file=sys.stderr)
    if getattr(exc, "hint", None):
        print(f"hint: {exc.hint}", file=sys.stderr)
    if own is not None:
        print(f"hint: {own}", file=sys.stderr)
    spec = CODES.get(code)
    if getattr(exc, "request_id", None) and spec is not None and spec.status == 500:
        print(f"request_id: {exc.request_id}", file=sys.stderr)


    return spec.exit_code if spec is not None else 1


def _dispatch(args: argparse.Namespace) -> int:
    """One of this file's own commands (_OWN), run."""
    if args.cmd == "init":
        return _cmd_init(args.template, args.dest, args.list_only, args.base_url,
                         no_source=getattr(args, "no_source", False))
    if args.cmd == "serve":
        from seq import serve_local


        folder = _served(args.folder, args.base_url)
        return serve_local.serve(folder, args.name, host=args.host, port=args.port, weights=args.weights,
                                 token=args.token, base_url=args.base_url, cuda_graphs=args.cuda_graphs,
                                 whole_graph=args.whole_graph, torch_compile=args.torch_compile,
                                 fused_kernels=args.fused_kernels, tensorrt=args.tensorrt, precision=args.precision,
                                 tolerance=args.tolerance, cfg_parallel=args.cfg_parallel,
                                 pipeline_parallel=args.pipeline_parallel)
    if args.cmd == "teleop":
        import os

        from sequence_ai._core import teleop_serve

        token = args.token if args.token is not None else os.environ.get(teleop_serve.TOKEN_ENV)
        secret = args.turn_secret or os.environ.get(teleop_serve.TURN_SECRET_ENV)
        if args.turn and not secret:
            raise InvalidRequest(f"--turn needs its server's shared secret: --turn-secret, or ${teleop_serve.TURN_SECRET_ENV}")
        if args.moq and args.moq_port is not None:
            raise InvalidRequest("--moq names a MoQ relay of your own and --moq-port serves one here: one of the two")
        return teleop_serve.serve(args.host, args.port, token=token, robot=args.robot, record=args.record,
                                  turn=args.turn or (), turn_secret=secret,
                                  turn_ttl_s=args.turn_ttl or teleop_serve.TURN_TTL_S, moq=args.moq,
                                  moq_port=args.moq_port)
    if args.cmd == "data":
        from sequence_ai._core import dataset

        dataset.export(args.recordings, args.out, fmt=args.format, fps=args.fps)
        return 0
    return _cmd_weights(args)


def _command(args: argparse.Namespace) -> str:
    sub = getattr(args, f"{args.cmd}_cmd", None)
    return f"{args.cmd} {sub}" if sub else args.cmd


def _served(given: str, base_url: str | None) -> str:
    """
    What `seq serve <given>` serves: the folder or .py file of that name here, as before - or, where there is none and
    the name is a template's (pi05-droid, pi05-droid@v12), that template's code as `seq init` writes it, kept on this
    machine (template_fetch.keep), whose weights `seq serve` then downloads with your key as it does for any folder.

    In one sentence: a path here, or a name in no template's form → as given → a version named that is kept here → its
    folder, the platform asked nothing → else the template's one version, or the one named, fetched → kept here
    already: its folder → else kept, and its folder.

    WHY a folder here wins: `seq serve pi05-droid` in the folder `seq init pi05-droid` made serves what was written and
    perhaps edited there, as it did before a name could mean the template.
    WHY no check of whether it deploys (seq init's _say_undeployable): serving it here is no deploy.
    WHY no third_party sources (`seq init --no-source`): they are the upstream's code to read, which its image installs
    from the official package; what serves here is what this machine has installed (requirements-policy.lock).
    




    """
    from seq import template_fetch

    if Path(given).exists() or not template_fetch.names_a_template(given):
        return given
    name, ref = template_fetch.split_ref(given)

    kept = template_fetch.held(name, ref) if ref else None
    if kept is None:
        got = template_fetch.fetch(name, ref, base_url)
        if got is None:
            raise NotFound(f"{given}: no such folder, and no template by that name",
                           hint="seq init --list shows the templates")
        archive, version = got
        kept = template_fetch.held(name, version) or template_fetch.keep(archive, name, version)
    print(f"{name} {kept.name}: the template's code, in {kept}")
    return str(kept)








def _print_templates(base_url: str | None) -> None:
    """Every template `seq init` can write, by kind, with the version each channel points at."""
    from seq import template_fetch

    rows = template_fetch.list_remote(base_url)


    if _plugin() is None:
        rows = [r for r in rows if r.get("kind") == "policy"]
    print("\n".join(template_fetch.lines_by_kind(rows)))
    print("\nseq init <template>[@vN] [directory]")



def _cmd_weights(args: argparse.Namespace) -> int:
    """`seq weights get <template>[@vN] [--dir DIR]`: one version of a template's weights here; prints the folder."""
    from seq import template_fetch, weights_get

    name, ref = template_fetch.split_ref(args.template)
    folder = weights_get.fetch(name, ref, dest=args.dir, base_url=args.base_url)
    print(folder)
    return 0



def _cmd_init(template: str | None, dest: str | None, list_only: bool, base_url: str | None, *,
              no_source: bool = False) -> int:
    """`seq init <template> [directory]`: a template's one version from the platform, or the version named (@vN),
    unpacked into the directory, with the large upstream sources its image installs unless `--no-source`. `--list`
    shows them all."""
    if list_only or not template:
        _print_templates(base_url)
        return 0 if list_only else 2
    if _init_official(template, dest, base_url, no_source=no_source) is None:
        raise NotFound(f"no template named {template.partition('@')[0]!r}", hint="seq init --list shows the templates")
    return 0



def _init_official(spec: str, target: str | None, base_url: str | None, *, no_source: bool = False) -> int | None:
    """Fetch the template's one version, or the one named, from the platform and unpack it; None when the platform has
    no template by that name. With sequence-cloud installed, a version this sequence-ai cannot deploy is said
    (_say_undeployable)."""
    from seq import template_fetch

    name, ref = template_fetch.split_ref(spec)
    dest = Path(target or name)

    template_fetch.refuse_occupied(dest)
    got = template_fetch.fetch(name, ref, base_url)
    if got is None:
        return None
    archive, version = got




    cloud = _plugin() is not None
    if cloud:
        _say_undeployable(name, archive, version)



    deploy_name = dest.name
    template_fetch.unpack(archive, dest, template=name, deploy_name=deploy_name)
    print(f"wrote {dest}/ ({name} {version})")
    _init_sources(dest, name, version, base_url, no_source=no_source)
    entry = template_fetch.entry_of(dest)
    readme = f"{dest}/README.md" if (dest / "README.md").exists() else None

    pick = template_fetch.entry_name(dest, entry) if entry else None
    deploy = f"seq deploy {dest}" + (f" --name {pick}" if pick else "")
    if entry and entry != "policy.py" and not cloud:
        print(f"next: {needs_cloud('registering it on the platform')}" + (f"; see {readme}" if readme else ""))
        return 0
    if entry == "adapter.py":


        print(f"next: `{deploy}` registers it; name it in an eval with --adapter {name}"
              + (f" (see {readme})" if readme else ""))
    elif entry == "policy.py":




        client = f"{dest}/client.py" if (dest / "client.py").exists() else None
        after = (f"; on the robot, see {' and '.join(filter(None, (readme, client)))}" if client
                 else f"; see {readme}" if readme else "")
        print(f"next: `seq serve {dest}` serves it from this machine - a robot connects with "
              f'sequence_ai.connect("http://<this machine>:8000"){after}')
        if template_fetch.weights_from_gs(dest, entry):
            print("its weights download with a General Sequences key: seq serve reads it from "
                  + ("`seq login` or " if cloud else "") + "SEQUENCES_API_KEY")
        if cloud:
            flags = template_fetch.deploy_flags(template_fetch.deploy_items(dest)) or ["--gpu", "CARD"]
            print(f"on the General Sequences platform: `{deploy} {' '.join(flags)}`")
    elif entry:
        print(f"next: `{deploy}`" + (f"; see {readme}" if readme else ""))
    return 0


def _say_undeployable(name: str, archive: bytes, version: str) -> None:
    """
    A warning when this sequence-ai cannot deploy the version `seq init` writes: the version read as `seq deploy` reads
    it (template_fetch.check_archive), its refusal said under the warning; nothing when it deploys.

    WHY a warning and nothing written instead: a template has one version, so there is none to write in its place - the
    newest-that-deploys choice went with the stable and beta channels - and what is left to say, before a `seq deploy`
    finds it out, is that this sequence-ai cannot deploy it.

    """
    from seq import template_fetch
    from sequence_ai._core.transport import _version

    why = template_fetch.check_archive(archive, name)
    if why is None:
        return
    print(f"warning: {name} {version} does not deploy with this sequence-ai ({_version()}). {version} is refused "
          "with:", file=sys.stderr)
    print(f"  {why}", file=sys.stderr)



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
