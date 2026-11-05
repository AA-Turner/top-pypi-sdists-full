"""`python -I -m probe.sdk.delivery.service`: the delivery service, which the SDK starts where no machine
service serves it (plan D9, D28). One per machine folder; a duplicate exits 0 at once."""

from __future__ import annotations

import sys

if __name__ == "__main__":
    import os

    from probe.sdk.delivery.service.service import run_delivery_service

    code = run_delivery_service()
    sys.stdout.flush()
    sys.stderr.flush()
    # Never wait on a relay thread still sending past IN_FLIGHT_WAIT_S: the socket and lock went first.
    os._exit(code)
