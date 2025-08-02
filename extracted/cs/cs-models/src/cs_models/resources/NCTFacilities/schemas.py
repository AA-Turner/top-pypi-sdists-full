from marshmallow import (
    Schema,
    fields,
    validate,
)


class NCTFacilityResourceSchema(Schema):
    not_blank = validate.Length(min=1, error="Field cannot be blank")

    id = fields.Integer(dump_only=True)
    nct_study_id = fields.Integer(required=True)
    facility_name = fields.String(allow_none=True)
    facility_city = fields.String(allow_none=True)
    facility_country = fields.String(allow_none=True)
    facility_zip_code = fields.String(allow_none=True)
    updated_at = fields.DateTime(dump_only=True)
