"""The outbox journal's frozen contract (plan D8): v1 is what every release since 0.24.0 wrote, and
what a Probe service's own drain reads, whatever SDK wrote it. Never changed in place: a new field
is optional, a new op kind is held by an older drain (plan 1.11), anything else is v2 beside v1.
The layout and op fields: DESIGN.md, "The v1 contract"."""

from __future__ import annotations

from typing import Any

from ..ops.ops import DELIVERY_SCHEMA, OP_KINDS, SCHEMA

#: The journal version this SDK writes; a service lists those it reads in `service.hello`'s
#: `outbox_journals` (`foundation/service_api/wire.OUTBOX_JOURNALS`, held equal by a test).
JOURNAL_VERSION = 1
#: Every version this release's drain reads.
READ_VERSIONS = (1,)
#: The `schema` of a v1 op: the queue's, and the delivery-v1 receipts' (`delivery-v1/`).
V1_SCHEMAS = frozenset({SCHEMA, DELIVERY_SCHEMA})
#: The op kinds released SDKs queued, oldest first (R8, `git log -S` on the ops module):
#: http, upload, rejected_http (0.24.0, #107); create_run (0.192.0, #2036); multipart_upload
#: (0.194.0, #2074); catalog_manifest (0.253.0, #2791).
V1_KINDS = frozenset({"http", "upload", "rejected_http", "create_run", "multipart_upload", "catalog_manifest"})

assert V1_KINDS <= OP_KINDS, "a v1 kind this drain cannot deliver"


def is_newer_than_v1(op: Any) -> bool:
    """An op of a journal version after v1 (a `schema` string v1 does not name): a v1 drain holds
    it in its run's order, never sends or dead-letters it. An op with no `schema` is v1's."""
    schema = op.get("schema") if isinstance(op, dict) else None
    return isinstance(schema, str) and schema not in V1_SCHEMAS
