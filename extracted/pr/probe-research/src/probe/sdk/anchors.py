"""What an artifact hangs off -- the closed anchor vocabulary.

A module of its own so the outbox's lower layers (`multipart.py`) can name an
anchor without importing `client.py`, which imports `run.py`, which imports
them. `client.Anchor` is this class, re-exported.
"""

from __future__ import annotations

from enum import Enum


class Anchor(str, Enum):
    """What an artifact hangs off.

    The database CHECKs that exactly one anchor is set, so this is a closed
    vocabulary, not a hint. Four of these are *artifacts*; workspace and shared are
    *files*, which is a different noun on the wire (see :meth:`Client.upload_file`).
    """

    RUN = "run"
    EXPERIMENT = "experiment"
    PROJECT = "project"
    WORKSPACE = "workspace"
    SHARED = "shared"
