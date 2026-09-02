"""Kinds for the ``instance_*`` tool family (KIND_TOOL_LEDGER, ``lead-w2e``).

The five saved-kind-instance tools (``implementations/kind_instance.py``)
return three shapes:

* ``kind_instance_write_result`` — ONE union receipt for the three writes
  (create / update / delete), the ``db_scoped_result`` two-tools-one-shape
  precedent: every "a write happened to one instance" receipt is one kind,
  with branch-only fields optional (create adds ``kind_definition_id`` +
  ``message``, update adds ``warning``, delete adds ``deleted``).
* ``kind_instance_page`` — the ``instance_list`` page, nesting the light
  summary projection.
* ``kind_instance_detail`` — the ``instance_get`` full read: the record
  (payload included — the payload carries its OWN ``__kind``, stamped at
  write) plus the pinned-behind-current verdict.

Placeholder tier: receipts and projections of our own rows, no rich provider
data.
"""

from __future__ import annotations

from pydantic import JsonValue

from matrx_graph.content_ir.model import KindModel, KindSubModel
from matrx_graph.content_ir.sdk import kind


@kind(
    "kind_instance_write_result",
    label="Kind Instance Write",
    family="kind_instances",
    example={
        "instance_id": "1d1cf4c2-0000-4000-8000-000000000000",
        "kind": "postal_address",
        "kind_version": 3,
        "title": "Head office",
        "validation_status": "passed",
        "message": "Instance saved as 'Head office' (kind 'postal_address' v3, verdict: passed).",
    },
    maturity="placeholder",
)
class KindInstanceWriteResult(KindModel):
    """Receipt for one write to a saved kind instance (create/update/delete)."""

    instance_id: str = ""
    #: The instance's kind slug (create/update; delete omits it).
    kind: str | None = None
    #: Create only: the kind_definition row the instance was pinned to.
    kind_definition_id: str | None = None
    #: The kind_version the instance is pinned to after the write.
    kind_version: int | None = None
    title: str | None = None
    #: The DB derived-on-write trigger's verdict, read back as the truth.
    validation_status: str | None = None
    message: str | None = None
    #: Update only: loud non-passed verdict guidance (None when passed).
    warning: str | None = None
    #: Delete only: the soft-delete confirmation.
    deleted: bool | None = None


class KindInstanceSummary(KindSubModel):
    """The light list projection of one saved instance."""

    id: str = ""
    kind_definition_id: str = ""
    title: str | None = None
    kind_version: int | None = None
    validation_status: str | None = None
    updated_at: str | None = None
    deleted: bool = False
    #: The kind slug (resolved per page; "unknown" when the kind row is gone).
    kind: str | None = None


@kind(
    "kind_instance_page",
    label="Kind Instances",
    family="kind_instances",
    example={
        "total": 1,
        "limit": 50,
        "offset": 0,
        "instances": [
            {
                "id": "1d1cf4c2-0000-4000-8000-000000000000",
                "kind_definition_id": "aa11aa11-0000-4000-8000-000000000000",
                "title": "Head office",
                "kind_version": 3,
                "validation_status": "passed",
                "updated_at": "2026-08-26 12:00:00+00:00",
                "deleted": False,
                "kind": "postal_address",
            }
        ],
    },
    maturity="placeholder",
)
class KindInstancePage(KindModel):
    """One page of the caller's saved instances (``instance_list``)."""

    total: int = 0
    limit: int = 0
    offset: int = 0
    instances: list[KindInstanceSummary] = []


class KindInstanceRecord(KindSubModel):
    """The full stored record of one saved instance (``instance_get``)."""

    id: str = ""
    kind_definition_id: str = ""
    title: str | None = None
    kind_version: int | None = None
    validation_status: str | None = None
    updated_at: str | None = None
    deleted: bool = False
    kind: str | None = None
    #: The instance payload — carries its OWN root ``__kind`` marker.
    data: JsonValue | None = None
    validated_at: str | None = None
    visibility: str | None = None
    created_at: str | None = None
    metadata: dict[str, JsonValue] = {}


@kind(
    "kind_instance_detail",
    label="Kind Instance",
    family="kind_instances",
    example={
        "instance": {
            "id": "1d1cf4c2-0000-4000-8000-000000000000",
            "kind_definition_id": "aa11aa11-0000-4000-8000-000000000000",
            "title": "Head office",
            "kind_version": 3,
            "validation_status": "passed",
            "updated_at": "2026-08-26 12:00:00+00:00",
            "deleted": False,
            "kind": "postal_address",
            "data": {"__kind": "postal_address", "street": "1 Main St"},
            "validated_at": "2026-08-26 12:00:00+00:00",
            "visibility": "private",
            "created_at": "2026-08-26 12:00:00+00:00",
            "metadata": {},
        },
        "kind_current_version": 4,
        "pinned_behind_current": True,
    },
    maturity="placeholder",
)
class KindInstanceDetail(KindModel):
    """One saved instance in full, with the version-pin verdict beside it."""

    instance: KindInstanceRecord
    #: The kind's CURRENT version (None when the kind row no longer resolves).
    kind_current_version: int | None = None
    #: True when the instance is pinned behind the kind's current schema.
    pinned_behind_current: bool = False
