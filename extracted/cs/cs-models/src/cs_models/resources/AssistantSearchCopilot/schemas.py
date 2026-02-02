from marshmallow import Schema, fields


class AssistantSearchCopilotResourceSchema(Schema):
    id = fields.Integer(dump_only=True)
    assistant_user_query_id = fields.Integer(allow_none=True)
    status = fields.String(allow_none=True)
    status_code = fields.String(allow_none=True)
    search_payloads = fields.String(allow_none=True)
    updated_at = fields.DateTime(dump_only=True)
