from marshmallow import (
    Schema,
    fields,
    validate,
)


class CollectionResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    type = fields.String(required=True)
    global_access = fields.Boolean(allow_none=True)
    updated_at = fields.DateTime(dump_only=True)
