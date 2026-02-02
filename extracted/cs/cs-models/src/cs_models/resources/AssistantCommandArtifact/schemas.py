from marshmallow import (
    Schema,
    fields,
    validate,
)


class AssistantCommandArtifactResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    assistant_command_id = fields.Integer(required=True)
    artifact_id = fields.String(required=True)
    score = fields.Float(allow_none=True)
    updated_at = fields.DateTime()
