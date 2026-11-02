# File: matrx_files/blocks/model.py
"""Hand-maintained model for `platform.acquisition_block` (board row H8).

NOT generated: this package's codegen scope is `files` + `iam` (see
`matrx_files/db/models_platform.py`, which borrows `platform.share_links` the
same way). The Block Ledger's one table lives in `platform`, and every host
that can hit a wall declares the columns it writes and keeps them in sync
with the migration (`matrx-frontend/migrations/acq_01_a_block_is_a_finding.sql`).
The canonical hand-maintained copy is `matrx_scraper.blocks.model.AcquisitionBlock`
— this one binds `_database = "matrx_files"` instead of `"matrx_web"` because
matrx-files cannot depend on matrx-scraper (independence boundary), but both
are the SAME physical row in the SAME one database.
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

from matrx_files.db import PACKAGE_DB_NAME

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
    _database = PACKAGE_DB_NAME
    _table_name = "acquisition_block"
    _db_schema = "platform"


model_registry.register_all([AcquisitionBlock], skip_existing=True)
