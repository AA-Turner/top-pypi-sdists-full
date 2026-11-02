# File: matrx_files/db/models.py
from matrx_orm import BooleanField, CharField, DateTimeField, FloatField, ForeignKey, IntegerField, JSONBField, MatrxEntity, Model, TextField, UUIDField, model_registry, BaseDTO, BaseManager
from enum import StrEnum
from dataclasses import dataclass
from typing import ClassVar

class Users(Model):
    id = UUIDField(primary_key=True, null=False)
    instance_id = UUIDField()
    aud = CharField()
    role = CharField()
    email = CharField()
    phone = TextField()
    raw_app_meta_data = JSONBField()
    raw_user_meta_data = JSONBField()
    is_super_admin = BooleanField()
    is_sso_user = BooleanField(null=False, default=False)
    is_anonymous = BooleanField(null=False, default=False)
    email_confirmed_at = DateTimeField()
    phone_confirmed_at = DateTimeField()
    confirmed_at = DateTimeField()
    last_sign_in_at = DateTimeField()
    invited_at = DateTimeField()
    banned_until = DateTimeField()
    created_at = DateTimeField()
    updated_at = DateTimeField()
    deleted_at = DateTimeField()

    _table_name = "users"
    _db_schema = "auth"
    _database = "matrx_files"
    _read_only = True

class AppInstances(MatrxEntity):
    id = UUIDField(primary_key=True, null=False)
    user_id = ForeignKey(to_model='Users', to_column='id', to_schema='iam', null=False)
    instance_id = TextField(null=False)
    instance_name = TextField(null=False, default='My Computer')
    platform = TextField()
    os_version = TextField()
    architecture = TextField()
    hostname = TextField()
    username = TextField()
    python_version = TextField()
    home_dir = TextField()
    cpu_model = TextField()
    cpu_cores = IntegerField()
    ram_total_gb = FloatField()
    is_active = BooleanField(null=False, default=True)
    last_seen = DateTimeField(null=False)
    created_at = DateTimeField(null=False)
    updated_at = DateTimeField(null=False)
    tunnel_url = TextField()
    tunnel_active = BooleanField(null=False, default=False)
    tunnel_updated_at = DateTimeField()
    hardware_uuid = TextField()
    serial_number = TextField()
    board_id = TextField()
    organization_id = ForeignKey(to_model='Organizations', to_column='id', to_schema='iam', null=False)
    project_id = ForeignKey(to_model='Projects', to_column='id', to_schema='projects', )
    task_id = ForeignKey(to_model='Tasks', to_column='id', to_schema='projects', )
    tunnel_ws_url = TextField()
    system_hardware = JSONBField()
    hardware_detected_at = DateTimeField()
    created_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    updated_by = ForeignKey(to_model='Users', to_column='id', to_schema='iam', )
    version = IntegerField(null=False, default=1)
    deleted_at = DateTimeField()
    metadata = JSONBField(null=False, default={})
    app_version = TextField()
    custom_fields = JSONBField(null=False, default={})
    test_run_id = UUIDField()
    test_expires_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_files"
    _entity_token = "app_instance"
    _is_versioned = False
    _has_soft_delete = True
    _is_org_scoped = True
    _rls_variant = "entity"

__all__ = [
    "AppInstances",
    "Users",
]


model_registry.register_all(
[
        AppInstances,
        Users
    ],
    skip_existing=True
)