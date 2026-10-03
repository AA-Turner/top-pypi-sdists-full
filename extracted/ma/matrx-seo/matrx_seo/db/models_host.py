# File: matrx_seo/db/models_host.py
"""Package-owned models for the HOST surfaces matrx-seo is granted.

These are minimal, deliberately narrow mirrors of canonical host tables the
SEO vertical reads (``web.site`` / ``web.page`` / ``projects.projects``) plus
the platform association edge table it writes keyword→project links through.
The read surfaces are ``_read_only`` — the vertical never mutates a host row.
All bind to the ``matrx_seo`` database name (hosted alias or svc_seo pool).
"""

from typing import ClassVar

from matrx_orm import (
    BooleanField,
    DateTimeField,
    IntegerField,
    JSONBField,
    Model,
    TextField,
    UUIDField,
    model_registry,
)


class WebSite(Model):
    id = UUIDField(primary_key=True, null=False)
    organization_id = UUIDField(null=False)
    root_url = TextField(null=False)
    created_by = UUIDField()
    integrations = JSONBField(null=False, default={})
    status = TextField(null=False)
    deleted_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "site"
    _db_schema = "web"
    _read_only = True


class WebPage(Model):
    id = UUIDField(primary_key=True, null=False)
    organization_id = UUIDField(null=False)
    site_id = UUIDField(null=False)
    url = TextField(null=False)
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "page"
    _db_schema = "web"
    _read_only = True


class WorkspaceProject(Model):
    id = UUIDField(primary_key=True, null=False)
    organization_id = UUIDField(null=False)
    name = TextField(null=False)
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "projects"
    _db_schema = "projects"
    _read_only = True


class PlatformCategory(Model):
    """``platform.categories`` — THE keyword-facet vocabulary registry (D37).

    Read-only on purpose: a dimension or value is authored by a HUMAN through
    ``seo.facet_dimension_upsert`` / ``seo.facet_value_upsert``, never by the
    classifier. The classifier reads this table to learn what it is allowed to
    say, and ``seo.keyword_facet`` FKs into it, so a value the classifier can
    write is a value a user created — by construction, not by convention."""

    id = UUIDField(primary_key=True, null=False)
    organization_id = UUIDField(null=False)
    dimension = TextField(null=False)
    slug = TextField(null=False)
    name = TextField(null=False)
    parent_id = UUIDField()
    position = IntegerField()
    is_system = BooleanField()
    metadata = JSONBField(null=False, default={})
    created_at = DateTimeField()
    updated_at = DateTimeField()
    deleted_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "categories"
    _db_schema = "platform"
    _read_only = True


class PlatformAssociation(Model):
    id = UUIDField(primary_key=True, null=False, default="gen_random_uuid()")
    source_type = TextField(null=False)
    source_id = UUIDField(null=False)
    target_type = TextField(null=False)
    target_id = UUIDField(null=False)
    organization_id = UUIDField()
    role = TextField()
    metadata = JSONBField(null=False, default={})
    created_by = UUIDField()
    created_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "associations"
    _db_schema = "platform"


__all__ = [
    "PlatformAssociation",
    "PlatformCategory",
    "WebPage",
    "WebSite",
    "WorkspaceProject",
]


model_registry.register_all(
    [WebSite, WebPage, WorkspaceProject, PlatformAssociation, PlatformCategory],
    skip_existing=True,
)
