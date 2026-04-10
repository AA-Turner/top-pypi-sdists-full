"""Internal entrypoint for detached Chronos workspace mount helpers."""

from __future__ import annotations

import argparse
import asyncio

from plato.cli.chronos.mount import run_mount_daemon


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="plato chronos mount-daemon")
    parser.add_argument("--alias", required=True)
    parser.add_argument("--session-id", required=True)
    parser.add_argument("--repo-name")
    parser.add_argument("--step-name")
    parser.add_argument("--mount-path")
    parser.add_argument("--cpus", type=int, default=1)
    parser.add_argument("--memory", type=int, default=2048)
    parser.add_argument("--disk", type=int, default=10240)
    return parser


def main() -> None:
    args = _build_parser().parse_args()
    asyncio.run(
        run_mount_daemon(
            args.alias,
            args.session_id,
            repo_name=args.repo_name,
            step_name=args.step_name,
            mount_path=args.mount_path,
            cpus=args.cpus,
            memory=args.memory,
            disk=args.disk,
        )
    )


if __name__ == "__main__":
    main()
