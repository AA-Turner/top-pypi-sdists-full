"""`python -m probe.service`: run the Probe service (one instance per user).

    python -m probe.service             serve until idle; a duplicate exits 0 at once
    python -m probe.service --selftest  import the start path, print the modules it
                                        loaded as JSON, and exit (the import-budget test)

Spawned detached by `probe.foundation.service_api.start.ensure`, never through the `probe`
CLI entry point: that costs ~1 s and ~85 MB before a line of this runs (plan S1).
"""

from __future__ import annotations

import sys


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if args[:1] == ["--selftest"]:
        import json

        from ..foundation.service_api import (  # noqa: F401 -- the start path: the old client and protocol
            calls, cli, env, params, paths, procid, service_api, start, vocabularies, wire,
        )
        from . import actions, server, updater  # noqa: F401
        from .actions import children, statuscache  # noqa: F401
        from .sessions import runholds, sessions  # noqa: F401
        from .updater import manifest  # noqa: F401
        from .updater.app import locate  # noqa: F401
        from .updater.quiet import barrier  # noqa: F401

        print(json.dumps(sorted(sys.modules)))
        return 0
    if args:
        print("usage: python -m probe.service [--selftest]", file=sys.stderr)
        return 2
    from .server.main import run_service

    return run_service()


if __name__ == "__main__":
    sys.exit(main())
