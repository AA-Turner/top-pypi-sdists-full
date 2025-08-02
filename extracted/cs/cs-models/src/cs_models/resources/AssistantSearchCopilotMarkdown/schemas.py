from marshmallow import Schema, fields


class AssistantSearchCopilotMarkdownResourceSchema(Schema):
    id = fields.Integer(dump_only=True)
    search_copilot_id = fields.Integer(required=True)
    artifact_id = fields.String(required=True)
    updated_at = fields.DateTime(dump_only=True)
