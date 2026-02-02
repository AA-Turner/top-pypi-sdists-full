from marshmallow import (
    Schema,
    fields,
    validate,
    pre_load,
)
from ...utils.utils import pre_load_date_fields


class NCTChangeResourceSchema(Schema):
    not_blank = validate.Length(min=1, error="Field cannot be blank")

    id = fields.Integer(dump_only=True)
    nct_id = fields.String(required=True)
    nct_study_id = fields.Integer(allow_none=True)
    date = fields.DateTime(required=True)
    change_type = fields.String(required=True)
    news_id = fields.Integer(allow_none=True)
    pubmed_id = fields.Integer(allow_none=True)
    old_value = fields.String(allow_none=True)
    new_value = fields.String(allow_none=True)
    note = fields.String(allow_none=True)
    updated_at = fields.DateTime(dump_only=True)

    @pre_load
    def convert_string_to_datetime(self, in_data, **kwargs):
        date_fields = ['date']

        in_data = pre_load_date_fields(
            in_data,
            date_fields,
            date_format='%Y%m%dT%H%M%S',
        )
        return in_data
