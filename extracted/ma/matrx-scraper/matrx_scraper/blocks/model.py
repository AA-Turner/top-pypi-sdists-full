"""Hand-maintained model for `platform.acquisition_block`, the Block Ledger's one table.

NOT generated: this package's codegen scope is the `scraper` + `web` schemas, and the ledger
lives in `platform`. Same shape and same reason as `matrx_files/db/models_platform.py` — a
package that must write a canonical platform table declares the columns it writes and keeps
them in sync with the migration
(`matrx-frontend/migrations/acq_01_a_block_is_a_finding.sql`).

It binds the `matrx_web` config, which is the SAME ONE database as `web.*` and `scraper.*`
(one resolver, `matrx_scraper.db.web.bootstrap_web_db`) — so a block recorded by the hosted
scraper service and a block recorded by aidream are rows in one table, never two.
"""

from __future__ import annotations

from typing import ClassVar

from matrx_orm import (
    DateTimeField,
    IntegerField,
    JSONBField,
    Model,
    TextField,
    UUIDField,
    model_registry,
)

__all__ = ["AcquisitionBlock"]


class AcquisitionBlock(Model):
    id = UUIDField(primary_key=True, null=False)
    input_ref = TextField(null=False)
    input_label = TextField(null=False)
    source_type = TextField(null=False)
    engine = TextField(null=False)
    rung = TextField()
    rung_trail = JSONBField(null=False, default=[])
    error_class = TextField(null=False)
    error_sentence = TextField(null=False)
    unblock_note = TextField(null=False)
    lawful_route = TextField()
    first_seen_at = DateTimeField(null=False)
    last_seen_at = DateTimeField(null=False)
    occurrence_count = IntegerField(null=False, default=1)
    status = TextField(null=False, default="open")
    retry_count = IntegerField(null=False, default=0)
    last_retry_at = DateTimeField()
    handoff_id = UUIDField()
    library_id = UUIDField()
    detail = JSONBField(null=False, default={})
    organization_id = UUIDField(null=False)
    created_by = UUIDField()
    updated_by = UUIDField()
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    deleted_at = DateTimeField()
    version = IntegerField(null=False, default=1)
    metadata = JSONBField(null=False, default={})
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_web"
    _table_name = "acquisition_block"
    _db_schema = "platform"


model_registry.register_all([AcquisitionBlock], skip_existing=True)
