from marshmallow import (
    Schema,
    fields,
    validate,
)


class InterventionDataRawResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    table_name = fields.String(required=True)
    table_id = fields.Integer(required=True)
    info = fields.String(allow_none=True)
    updated_at = fields.DateTime()
