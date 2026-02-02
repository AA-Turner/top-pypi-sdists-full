from marshmallow import Schema, fields, EXCLUDE
from ..WorkbookThreadComment.schemas import (
    WorkbookThreadCommentSchema,
)


class WorkbookCommentThreadResourceSchema(Schema):
    """Class for AssistantCommandResource schema"""
    class Meta:
        unknown = EXCLUDE

    id = fields.Integer(dump_only=True, data_key="thread_id")
    workbook_id = fields.Integer(required=True)
    block_uid = fields.String(required=True)
    selected_text = fields.String(required=True)

    # Thread status
    is_resolved = fields.Boolean(allow_none=True)
    resolved_by = fields.String(allow_none=True)
    resolved_at = fields.DateTime(allow_none=True)

    # Soft delete
    is_deleted = fields.Boolean(allow_none=True)

    # Timestamps
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    created_by = fields.String(required=True)

    # Smart Grid Cells
    cell_session_id = fields.Integer(allow_none=True)
    cell_user_query_id = fields.Integer(allow_none=True)
    text_start_offset = fields.Integer(allow_none=True)
    text_end_offset = fields.Integer(allow_none=True)

    # Nested comments
    comments = fields.Nested(WorkbookThreadCommentSchema(exclude=("thread_id",)), many=True, dump_only=True)
