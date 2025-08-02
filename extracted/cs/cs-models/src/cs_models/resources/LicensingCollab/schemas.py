from marshmallow import (
    Schema,
    fields,
    pre_load,
    validate,
)
from ...utils.utils import pre_load_date_fields


class LicensingCollabResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    news_id = fields.Integer(required=True)
    date = fields.DateTime(required=True)
    is_deleted = fields.Boolean(allow_none=True)
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
