"""The two REAL COLUMNS that carry a file's produced-artifact identity.

WHY THESE COLUMNS EXIST (2026-09-17, CS-27/CS-30). The coding-session Files tab
reads ``files.files`` for one session's artifacts. It used to filter on two
JSONB paths — ``metadata->>'kind'`` and ``metadata->>'cli_session_id'`` — and
that read timed out about one open in four, with no index able to save it:
``files.files`` has RLS enabled, and PostgreSQL may not evaluate a qual whose
operator is not LEAKPROOF before the security quals, so a ``->>`` qual can never
become an index condition. Measured as admin on production: 161,861 rows walked,
4.8-29 s, against role ``authenticated``'s 8 s statement_timeout.

So the identity a client filters by lives in real ``text`` columns, where
``texteq`` IS leakproof and a btree index answers under RLS (measured after:
6,614 candidate rows by Index Cond; 0.1 ms for a session whose rows the reader
owns). The columns are:

    files.files.artifact_kind        <- metadata['kind']
    files.files.provider_session_id  <- metadata['cli_session_id']

THE METADATA KEYS REMAIN THE CONTRACT with every client that uploads; these
columns are the server's derived, filterable copy, written by the ONE upload
door (``cloud_sync.sync_engine``'s insert/update payloads and the TUS
transport's row builder) so no caller has to know they exist — including the
placement-alias rows a dedup'd upload creates (``duplicate_of_file_id``), which
are ordinary inserts through the same door.

Adding a kind: put it in :data:`PROVIDER_SESSION_ARTIFACT_KINDS`. The backfill
migration stamped exactly the kinds listed here, so a kind added to this set
without a matching backfill leaves older rows unfindable by the fast path —
stamp them in the same change.
"""

from __future__ import annotations

#: Metadata ``kind`` values whose rows carry a provider session id worth
#: filtering by. Deliberately explicit: ``metadata['kind']`` is a word several
#: features use for unrelated senses, and ``artifact_kind`` must not become a
#: dumping ground for all of them.
PROVIDER_SESSION_ARTIFACT_KINDS: frozenset[str] = frozenset({"coding_session_artifact"})

#: The metadata key holding the provider's session id for those kinds.
PROVIDER_SESSION_METADATA_KEY = "cli_session_id"


def artifact_identity_columns(metadata: dict | None) -> dict[str, str | None]:
    """The column values this row's metadata implies — ``{}`` when it implies none.

    Returns a dict ready to merge into an insert payload or an update dict. A
    row whose metadata names a recognized kind gets BOTH columns (the session id
    may still be ``None`` if the uploader omitted it — that is the uploader's
    defect to see, not something to paper over with a guess). A row whose
    metadata names no recognized kind gets nothing, so an unrelated write never
    clears or invents an identity.
    """
    kind = (metadata or {}).get("kind")
    if not isinstance(kind, str) or kind not in PROVIDER_SESSION_ARTIFACT_KINDS:
        return {}
    session_id = (metadata or {}).get(PROVIDER_SESSION_METADATA_KEY)
    return {
        "artifact_kind": kind,
        "provider_session_id": str(session_id) if isinstance(session_id, (str, int)) else None,
    }
