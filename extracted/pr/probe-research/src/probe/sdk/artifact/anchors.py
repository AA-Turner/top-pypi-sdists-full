"""What an artifact hangs off -- the closed anchor vocabulary.

Its own module so `multipart.py` can name an anchor without importing `client.py`
(which imports `run.py`, which imports it). `client.Anchor` re-exports this.
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


#: Anchors addressed as "files": identity is (anchor, name), not (anchor, name,
#: content_hash), so re-uploading a name REPLACES it at confirm time. No
#: metadata-only form: a file is its bytes.
FILE_ANCHORS = frozenset({Anchor.WORKSPACE, Anchor.SHARED})
