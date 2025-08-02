from marshmallow import (
    Schema,
    fields,
    validate,
)


class DeletedNewswireResourceSchema(Schema):
    not_blank = validate.Length(min=1, error="Field cannot be blank")

    id = fields.Integer(dump_only=True)
    date = fields.DateTime(required=True)
    source = fields.String(required=True)
    headline = fields.String(required=True)
    s3_key_name = fields.String(required=True)
    source_link = fields.String(allow_none=True)
    updated_at = fields.DateTime(dump_only=True)
