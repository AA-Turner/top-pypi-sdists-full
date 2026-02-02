from marshmallow import (
    Schema,
    fields,
    validate,
)


class InvestorBucketResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    website = fields.String(allow_none=True)
    type = fields.String(allow_none=True)
    updated_at = fields.DateTime()
