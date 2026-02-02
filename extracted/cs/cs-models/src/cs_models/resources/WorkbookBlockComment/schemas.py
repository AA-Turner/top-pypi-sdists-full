"""Marshmallow Schema for AssistantCommand."""
from marshmallow import Schema, fields


class WorkbookBlockCommentResourceSchema(Schema):
    """Class for AssistantCommandResource schema"""

    id = fields.Integer(dump_only=True)
    block_id = fields.Integer(required=True)
    user_id = fields.String(required=True)
    sequence_number = fields.Integer(required=True)
    comment = fields.String(allow_none=True)
    is_deleted = fields.Boolean(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
