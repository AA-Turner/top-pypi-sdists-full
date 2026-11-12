"""Praxis-1's sessions (catalog wire ``praxis``, DSL-424): a robot runs every real row of each
answer (21 when a call starts the model's context, 24 after), as Runway's chunked schedule does.

The server's contract and every release's identity still say 21 executed rows: the rows SDKs
before 0.1.0a317 run, kept so the qualified releases and those clients stay as they are. The
worker reads however many steps a robot ran (upstream's ``executed_rows``), so both serve on one
release; this SDK runs its own contract's rows in place of the server's.
"""

from __future__ import annotations

from dreamscale_transport.praxis import EXECUTION_HORIZON, RUN_ROWS


def execution_horizon(model: str, served: int | None) -> int | None:
    """Every real row (``RUN_ROWS``) where the server says the older 21 (or nothing); any other
    count it sends is its own, and stands."""
    return RUN_ROWS if served in (None, EXECUTION_HORIZON) else served
