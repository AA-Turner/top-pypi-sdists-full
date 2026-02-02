from marshmallow import Schema, fields


class AssistantCopilotTaskResourceSchema(Schema):
    id = fields.Integer(dump_only=True)
    assistant_copilot_id = fields.Integer(required=True)
    assistant_search_copilot_id = fields.Integer(allow_none=True)
    assistant_session_id = fields.Integer(allow_none=True)
    task_info = fields.String(allow_none=True)
    updated_at = fields.DateTime(dump_only=True)
