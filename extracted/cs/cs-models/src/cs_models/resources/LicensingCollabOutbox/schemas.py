from marshmallow import (
    Schema,
    fields,
    pre_load,
    validate,
)
from ...utils.utils import pre_load_date_fields


class LicensingCollabOutboxResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    date = fields.DateTime(required=True)
    news_id = fields.Integer(required=True)
    upfronts = fields.String(allow_none=True)
    milestones = fields.String(allow_none=True)
    sentences = fields.String(allow_none=True)
    reviewed = fields.String(allow_none=True)
    llm_output = fields.String(allow_none=True)
    historical = fields.Boolean(allow_none=True)
    updated_at = fields.DateTime()

    @pre_load
    def convert_string_to_datetime(self, in_data, **kwargs):
        date_fields = ['date']

        in_data = pre_load_date_fields(
            in_data,
            date_fields,
            date_format='%Y%m%dT%H%M%S',
        )
        return in_data
