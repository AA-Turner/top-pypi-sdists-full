"""Entry points: pipmaster-pair, pipmaster-relay, pipmaster-install."""

from __future__ import annotations

import argparse
import re
import sys

from .common import DEFAULT_PORT, AirgapError


def _duration(text: str) -> float:
    match = re.fullmatch(r"(\d+(?:\.\d+)?)([smh]?)", text.strip().lower())
    if not match:
        raise argparse.ArgumentTypeError("use e.g. 90s, 15m, 1h")
    return float(match.group(1)) * {"": 60, "s": 1, "m": 60, "h": 3600}[match.group(2)]


def pair_main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="pipmaster-pair", description="Pair a relay with an offline client."
    )
    sub = ap.add_subparsers(dest="cmd", required=True)
    create = sub.add_parser(
        "create", help="(online machine) create the relay identity, print the token"
    )
    create.add_argument(
        "--host", help="address the offline machine will use to reach the relay"
    )
    create.add_argument("--port", type=int, default=DEFAULT_PORT)
    create.add_argument(
        "--force", action="store_true", help="rotate: old pairings stop working"
    )
    sub.add_parser(
        "show", help="(online machine) print the current pairing token again"
    )
    accept = sub.add_parser("accept", help="(offline machine) store a pairing token")
    accept.add_argument("token")
    args = ap.parse_args(argv)
    try:
        if args.cmd == "create":
            from .relay import create_identity, load_identity

            token = create_identity(args.host, args.port, args.force)
            print("fingerprint:", load_identity()["fp"])
            print(
                "pairing token (secret, carry it to the offline machine once):\n"
                + token
            )
        elif args.cmd == "show":
            from .relay import current_token

            print(current_token())
        else:
            from .client import save_peer

            peer = save_peer(args.token)
            print("paired. relay fingerprint:", peer["fp"])
    except (AirgapError, OSError) as exc:
        print("error:", exc, file=sys.stderr)
        return 2
    return 0


def relay_main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="pipmaster-relay", description="Open the update link for a limited time."
    )
    ap.add_argument(
        "--host", default="0.0.0.0", help="interface to bind (default: all)"
    )
    ap.add_argument("--port", type=int, default=DEFAULT_PORT)
    ap.add_argument(
        "--for",
        dest="duration",
        type=_duration,
        default=900,
        help="how long the link stays open (default 15m)",
    )
    ap.add_argument(
        "--allow-from",
        action="append",
        metavar="IP_OR_CIDR",
        help="only accept this peer address/network (repeatable)",
    )
    ap.add_argument(
        "--min-age-days",
        type=float,
        default=7,
        help="skip releases younger than this (default 7, 0 disables)",
    )
    ap.add_argument(
        "--index-url", help="custom package index (requires --min-age-days 0)"
    )
    ap.add_argument(
        "--audit", action="store_true", help="run pip-audit on the resolved set"
    )
    ap.add_argument(
        "--keep-open", action="store_true", help="stay open after a successful session"
    )
    args = ap.parse_args(argv)
    try:
        from .relay import Relay, Resolver

        resolver = Resolver(args.index_url, args.min_age_days, args.audit)
        Relay(
            args.host,
            args.port,
            args.duration,
            args.allow_from,
            resolver,
            args.keep_open,
        ).serve()
    except (AirgapError, OSError) as exc:
        print("error:", exc, file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        print("relay closed")
    return 0


def install_main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        prog="pipmaster-install",
        description="Install or update packages through the paired relay.",
    )
    ap.add_argument(
        "paths",
        nargs="*",
        help="requirements files, project directories, pyproject.toml",
    )
    ap.add_argument(
        "-p",
        "--package",
        action="append",
        default=[],
        metavar="SPEC",
        help="extra requirement, e.g. 'rich>=13' (repeatable)",
    )
    ap.add_argument(
        "--relay", metavar="HOST[:PORT]", help="override the address stored at pairing"
    )
    ap.add_argument(
        "--upgrade-installed",
        action="store_true",
        help="also ask for the latest version of everything installed",
    )
    ap.add_argument(
        "--dry-run", action="store_true", help="show the plan, install nothing"
    )
    ap.add_argument(
        "-y", "--yes", action="store_true", help="skip the confirmation prompt"
    )
    args = ap.parse_args(argv)
    if not (args.paths or args.package or args.upgrade_installed):
        ap.error("give at least a path, -p SPEC or --upgrade-installed")
    try:
        from .client import run_install

        return run_install(
            args.paths,
            args.package,
            args.relay,
            args.upgrade_installed,
            args.dry_run,
            args.yes,
        )
    except (AirgapError, OSError) as exc:
        print("error:", exc, file=sys.stderr)
        return 2
    except KeyboardInterrupt:
        return 130