"""
Correlation id — one value threads a logical `act()` through sdk → worker → gateway, so "what
happened to that call" is one grep instead of three log stores and a stopwatch.

── Why this file is a copy, not an import ─────────────────────────────
The convention lives in `sequence_base.obs.rid`, but the SDK deliberately does NOT depend on
sequence-base at runtime: it stays httpx-only / Python 3.9 so it installs on the robot platforms
base's pydantic + 3.11 floor would exclude (ROS 2 Humble ships 3.10; JetPack older still). The two
sides only ever exchange JSON — never Python objects — so importing base would buy nothing on the
wire and cost the platform matrix. This module reproduces base's format *bit for bit* (prefix `r-`,
exactly 8 lowercase hex characters) and `tests/test_rid_convention.py` pins the two together as a
TEST-ONLY check, so a drift in either spelling fails CI rather than silently breaking correlation.

3.9-clean (no `X | Y` at runtime, no `match`), stdlib only, never imports sequence_base.
"""
from __future__ import annotations

import uuid





HEADER = "X-Seq-Request-Id"


def new_rid() -> str:
    """A fresh correlation id: `r-` + 8 hex chars.

    Short (read off a terminal, quoted in bug reports) + random (nothing coordinates rid issuance
    across robots or reconnects, so it must not collide). `uuid4().hex` is lowercase hex already, so
    the slice is inside the character set the convention allows without any further normalisation.
    """
    return "r-" + uuid.uuid4().hex[:8]


