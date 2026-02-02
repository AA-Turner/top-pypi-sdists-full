from marshmallow import Schema, fields


class WorkbookThreadCommentSchema(Schema):
    """Class for AssistantCommandResource schema"""

    id = fields.Integer(dump_only=True)
    thread_id = fields.Integer(required=True)
    user_id = fields.String(required=True)
    sequence_number = fields.Integer(required=True)
    comment = fields.String(required=True)
    is_deleted = fields.Boolean(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
