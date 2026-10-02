"""`python -m probe.box` -- the watcher process itself.

Holds the box lease for its whole life and sweeps until the box goes quiet.
Exiting without the lease is not a failure: it means another watcher is
already doing the job, which is the ordinary outcome when sixty-four ranks
start at once and all of them try.
"""

from __future__ import annotations

import logging
import sys

from probe.box import spawn, watch


def main() -> int:
    logging.basicConfig(level=logging.WARNING)
    lease = spawn.hold_lease()
    if lease is None:
        return 0
    try:
        watch.watch_forever()
    except KeyboardInterrupt:
        pass
    finally:
        # Dropping the lease is what lets the next run start a watcher.
        try:
            lease.close()
        except Exception:  # noqa: BLE001
            pass
    return 0


if __name__ == "__main__":
    sys.exit(main())
