from marshmallow import (
    Schema,
    fields,
)


class UserExplorerColumnResourceSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.String(required=True)
    artifact_ids = fields.String(required=True)
    prompt = fields.String(required=True)
    result = fields.String(required=True)
    is_completed = fields.Boolean(allow_none=True)
    updated_at = fields.DateTime(dump_only=True)
