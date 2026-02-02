from marshmallow import (
    Schema,
    fields,
    pre_load,
    validate,
)
from ...utils.utils import pre_load_date_fields


class IPOOutboxResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    ipo_date = fields.DateTime(required=True)
    deal_value = fields.Decimal(allow_none=True)
    price = fields.String(allow_none=True)
    ticker = fields.String(allow_none=True)
    type = fields.String(allow_none=True)
    news_id = fields.Integer()
    currency = fields.String(allow_none=True)
    company_sec_id = fields.Integer(allow_none=True)
    company_ous_id = fields.Integer(allow_none=True)
    underwriters = fields.String(allow_none=True)
    counsels = fields.String(allow_none=True)
    llm_output = fields.String(allow_none=True)
    reviewed = fields.String(allow_none=True)
    historical = fields.Boolean(allow_none=True)
    updated_at = fields.DateTime()

    @pre_load
    def convert_string_to_datetime(self, in_data, **kwargs):
        date_fields = ['ipo_date']

        in_data = pre_load_date_fields(
            in_data,
            date_fields,
            date_format='%Y%m%dT%H%M%S',
        )
        return in_data
