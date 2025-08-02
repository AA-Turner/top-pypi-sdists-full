from marshmallow import (
    Schema,
    fields,
    validate,
)


class DOILinkResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')
    id = fields.Integer(dump_only=True)
    link = fields.Field(required=True)
    doi = fields.String(required=True, validate=not_blank)
