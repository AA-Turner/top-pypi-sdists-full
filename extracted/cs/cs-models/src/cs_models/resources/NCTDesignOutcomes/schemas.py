from marshmallow import (
    Schema,
    fields,
    validate,
    pre_load,
)
from ...utils.utils import pre_load_date_fields


class NCTDesignOutcomesResourceSchema(Schema):
    not_blank = validate.Length(min=1, error="Field cannot be blank")

    id = fields.Integer(dump_only=True)
    nct_study_id = fields.Integer(required=True)
    outcome_type = fields.String(allow_none=True)
    measure = fields.String(allow_none=True)
    time_frame = fields.String(allow_none=True)
    description = fields.String(allow_none=True)
    last_update_submitted_qc_date = fields.DateTime(allow_none=True)
    updated_at = fields.DateTime(dump_only=True)

    @pre_load
    def convert_string_to_datetime(self, in_data, **kwargs):
        date_fields = ['last_update_submitted_qc_date']

        in_data = pre_load_date_fields(
            in_data,
            date_fields,
            date_format='%Y%m%d',
        )
        return in_data
