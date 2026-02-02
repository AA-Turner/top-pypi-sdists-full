from marshmallow import (
    Schema,
    fields,
    validate,
)


class ExplorerColumnResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    artifact_id = fields.String(required=True)
    prompt = fields.String(required=True)
    answer = fields.String(allow_none=True)
    is_completed = fields.Boolean(allow_none=True)
    updated_at = fields.DateTime()
