from marshmallow import Schema, fields


class AssistantScratchPadResourceSchema(Schema):
    id = fields.Integer(dump_only=True)
    session_id = fields.Integer(required=True)
    artifact_id = fields.String(required=True)
    source_table = fields.String(required=True)
    source_id = fields.Integer(required=True)
    source_details = fields.String(allow_none=True)
    is_deleted = fields.Boolean(allow_none=True)
    updated_at = fields.DateTime(dump_only=True)
