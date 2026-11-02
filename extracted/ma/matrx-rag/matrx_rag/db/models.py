# File: matrx_rag/db/models.py
from dataclasses import dataclass
from enum import Enum
from typing import ClassVar

from matrx_orm import (
    BaseDTO,
    BaseManager,
    BooleanField,
    CharField,
    DateTimeField,
    DecimalField,
    FloatField,
    ForeignKey,
    IntegerField,
    JSONBField,
    Model,
    SmallIntegerField,
    TextArrayField,
    TextField,
    UUIDField,
    model_registry,
)


class Users(Model):
    id = UUIDField(primary_key=True, null=False)
    email = CharField(null=False)

    _table_name = "users"
    _db_schema = "auth"
    _database = "matrx_rag"


class Organizations(Model):
    id = UUIDField(primary_key=True, null=False)
    _table_name = "organizations"
    _database = "matrx_rag"
    _unfetchable = True


# ProcessedDocuments + ProcessedDocumentPages removed — see the note by
# register_all below. Canonical docproc models live in models_docproc.py
# (schema=docproc) / the host's db.models.

__all__ = [
    "Users",
    "Organizations",
]


# ProcessedDocuments / ProcessedDocumentPages were REMOVED here: the 2026 docproc
# reorg moved those tables to the `docproc` schema and their canonical models now
# live in models_docproc.py (with _db_schema="docproc"). The stale copies in this
# file had NO schema, so registering them created a schema-less duplicate ->
# get_db_model('ProcessedDocumentPages') was "ambiguous across schemas" and SQL
# emitted an unqualified `FROM processed_document_pages`. Never re-add them here;
# resolve docproc models from the host (db.models) or models_docproc.py.
model_registry.register_all(
    [
        Organizations,
        Users,
    ],
    skip_existing=True,
)
