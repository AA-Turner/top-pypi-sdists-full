from marshmallow import Schema, fields
from sqlalchemy import UniqueConstraint

from ..AssistantUserQuery.schemas import AssistantUserQueryResourceSchema


class AssistantSessionResourceSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.String(required=True)
    type = fields.String(required=True)
    label = fields.String(required=True)
    display_label = fields.String(allow_none=True)
    user_queries = fields.Nested(
        AssistantUserQueryResourceSchema(exclude=("session_id",)),
        many=True,
        dump_only=True,
    )
    is_deleted = fields.Boolean(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    internal_doc_only = fields.Boolean(allow_none=True)
    workbook_id = fields.Integer(allow_none=True)
    updated_at = fields.DateTime(dump_only=True)

    __table_args__ = (UniqueConstraint("user_id", "label"),)
