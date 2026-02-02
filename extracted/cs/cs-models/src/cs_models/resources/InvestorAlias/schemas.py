from marshmallow import (
    Schema,
    fields,
    validate,
)


class InvestorAliasResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    investor_id = fields.Integer(allow_none=True)
    alias = fields.String(required=True)
    updated_at = fields.DateTime()
