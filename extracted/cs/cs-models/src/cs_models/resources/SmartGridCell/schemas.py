"""Marshmallow Schema for AssistantCommand."""
from marshmallow import Schema, fields
from ..AssistantUserQuery.schemas import AssistantUserQueryResourceSchema


class SmartGridCellResourceSchema(Schema):
    """Class for AssistantCommandResource schema"""

    id = fields.Integer(dump_only=True)
    smart_grid_id = fields.Integer(required=True)
    row = fields.Integer(required=True)
    col = fields.Integer(required=True)
    type = fields.String(required=True)
    data = fields.String(allow_none=True)
    user_query_id = fields.Integer(allow_none=True)
    user_query = fields.Nested(
        AssistantUserQueryResourceSchema(),
        dump_only=True,
    )
    reformulated_question = fields.String(allow_none=True)
    is_deleted = fields.Boolean(allow_none=True)
    updated_at = fields.DateTime(dump_only=True)
