"""`python -I -m probe.sdk.delivery.service.background.outbox_drain <outbox>`: the service's own drain of one
outbox (plan D8), from this service's install and interpreter, whatever SDK wrote the journal: it reads
the frozen v1 contract (`sdk/delivery/journal/contract.py`) and holds what is newer. Exit codes as
the worker's: 0 drained or stepped aside, 3 auth-blocked, 4 paused."""

from __future__ import annotations

import sys


def main(argv: list[str]) -> int:
    if len(argv) != 1 or not argv[0].startswith("/"):
        print("usage: python -m probe.sdk.delivery.service.background.outbox_drain <outbox folder>", file=sys.stderr)
        return 2
    import os

    from probe.foundation.service_api.env import CALLER_FENCED_ENV
    from probe.sdk.delivery.journal.uploads import set_fenced_root
    from probe.sdk.delivery.outbox.outbox import run

    if os.environ.get(CALLER_FENCED_ENV) == "1":
        set_fenced_root(argv[0])  # a fenced caller's outbox: only its staged bytes go (H1)
    return run(argv[0])


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
