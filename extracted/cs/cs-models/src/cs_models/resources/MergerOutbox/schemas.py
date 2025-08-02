from marshmallow import (
    Schema,
    fields,
    validate,
)


class MergerOutboxResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    announcement_date = fields.DateTime(required=True)
    news_id = fields.Integer(required=True)
    deal_value = fields.String(allow_none=True)
    price = fields.String(allow_none=True)
    advisors = fields.String(allow_none=True)
    counsels = fields.String(allow_none=True)
    sentences = fields.String(allow_none=True)
    reviewed = fields.Boolean(allow_none=True)
    llm_output = fields.String(allow_none=True)
    historical = fields.Boolean(allow_none=True)
    updated_at = fields.DateTime()

