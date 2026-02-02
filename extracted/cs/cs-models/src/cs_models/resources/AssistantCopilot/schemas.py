from marshmallow import Schema, fields


class AssistantCopilotResourceSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.String(required=True)
    query = fields.String(required=True)
    timestamp = fields.DateTime(required=True)
    llm_result = fields.String(allow_none=True)
    status = fields.String(allow_none=True)
    status_code = fields.String(allow_none=True)
    updated_at = fields.DateTime(dump_only=True)
