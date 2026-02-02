from marshmallow import (
    Schema,
    fields,
    validate,
)


class CampaignTrackerResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    email = fields.String(allow_none=True)
    company = fields.String(allow_none=True)
    promo_code = fields.String(allow_none=True)
    campaign_description = fields.String(allow_none=True)
    updated_at = fields.DateTime(dump_only=True)
