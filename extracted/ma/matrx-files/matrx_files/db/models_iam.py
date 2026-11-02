# File: matrx_files/db/models_iam.py
from matrx_orm import BooleanField, DateTimeField, EnumField, ForeignKey, MatrxEntity, TextField, UUIDField, model_registry, BaseDTO, BaseManager
from enum import StrEnum
from dataclasses import dataclass
from typing import ClassVar



class PermissionLevel(StrEnum):
    VIEWER = "viewer"
    COMMENTER = "commenter"
    EDIT_CONTENT = "edit_content"
    EDITOR = "editor"
    ADMIN = "admin"

class Permissions(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    resource_type = TextField(null=False)
    resource_id = UUIDField(null=False)
    granted_to_user_id = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    granted_to_organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', )
    is_public = BooleanField(default=False)
    permission_level = EnumField(enum_class=PermissionLevel, null=False, default='viewer')
    created_at = DateTimeField()
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    status = TextField(null=False, default='active')
    reviewed_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    reviewed_at = DateTimeField()
    review_note = TextField()
    expires_at = DateTimeField()
    granted_via = TextField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_files"
    _table_name = "permissions"
    _db_schema = "iam"
    _entity_token = "permission_grant"
    _is_versioned = False
    _has_soft_delete = False
    _is_org_scoped = False
    _rls_variant = "system"

__all__ = [
    "Permissions",
    "PermissionLevel",
]


model_registry.register_all(
[
        Permissions
    ],
    skip_existing=True
)