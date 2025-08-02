from marshmallow import (
    Schema,
    fields,
    validate,
)


class ContextResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    key = fields.String(required=True)
    value = fields.String(validate=not_blank, required=True)
    artifact_id = fields.String(allow_none=True)
