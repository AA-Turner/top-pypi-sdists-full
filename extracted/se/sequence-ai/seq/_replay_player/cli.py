"""
`seq eval replay EVAL_ID|FILE [--episode N] [--no-browser]` - an eval's episodes in 3D as the console's Replay plays
them (orbit, zoom, the timeline, the cameras beside it), on a page on this machine; or one .seqreplay file `seq eval
report --replays` saved, with the scene it put beside it, offline.

In one sentence: the eval's details read first (no such eval, or nothing to play, is said here and nothing opens) →
the page's server on 127.0.0.1 (server.py) → its one-time link printed, and opened in the browser unless this is a
shell over SSH or --no-browser asks not to → served until Ctrl-C.
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import webbrowser

from seq._replay_player.server import ReplayServer
from seq._replay_player.sources import FileSource, GatewaySource
from sequence_ai.errors import SequencesError


def _remote() -> bool:
    """A shell over SSH with no display forwarded: a browser opened here is not in front of whoever reads this."""
    return bool(os.environ.get("SSH_CONNECTION") or os.environ.get("SSH_TTY")) and not os.environ.get("DISPLAY")


def replay(args: argparse.Namespace) -> int:
    target = args.target
    if os.path.isfile(target) or target.endswith(".seqreplay"):
        if not os.path.isfile(target):
            print(f"No such file: {target}", file=sys.stderr)
            return 1
        try:
            source = FileSource(target)
        except ValueError as exc:
            print(f"{target}: {exc}", file=sys.stderr)
            return 1
        if source.sha and source.scene_path is None:
            print(f"No scene beside {os.path.basename(target)}: the page shows its episode without it. `seq eval report "
                  "<id> --replays DIR` saves each scene into DIR/scenes/.", file=sys.stderr)
        title, name = f"{os.path.basename(target)} · Replay", os.path.splitext(os.path.basename(target))[0]
    else:
        from seq._eval_gateway import EvalGatewayClient

        source = GatewaySource(EvalGatewayClient(base_url=getattr(args, "base_url", None)), target)
        try:
            details = json.loads(source.details())
        except SequencesError as exc:
            print(f"eval {target}: {exc.message}", file=sys.stderr)
            return 1
        episodes = details.get("episodes") or []
        if (details.get("replay") or {}).get("state") == "deleted":
            print(f"Nothing to replay: the recordings of eval {target} are no longer stored.", file=sys.stderr)
            return 1
        if not any(e.get("replay") is True or e.get("record") is True or e.get("recorded") is True for e in episodes):
            print("Nothing to replay: no episode of this eval kept a 3D replay or a recording (its benchmark declares "
                  "no replay=, it ran with --replay none, or it has not finished one yet).", file=sys.stderr)
            return 1
        title, name = f"Eval {target[:8]} · Replay", f"eval-{target}"
    server = ReplayServer(source, title=title, name=name, episode=args.episode)
    print(f"Replay: {server.url}")
    print("  the link opens once, in one browser on this machine; Ctrl-C stops the page")
    if args.no_browser or _remote():
        print(f"  from another machine: ssh -L {server.port}:127.0.0.1:{server.port} <this host>, then open the link "
              "there")
    elif not webbrowser.open(server.url):
        print("  no browser opened: open the link yourself")



    sys.stdout.flush()
    try:
        server.serve()
    except KeyboardInterrupt:
        print()
    finally:
        server.close()
    return 0
