from marshmallow import (
    Schema,
    fields,
    validate,
)


class NCTResultResourceSchema(Schema):
    not_blank = validate.Length(min=1, error="Field cannot be blank")

    id = fields.Integer(dump_only=True)
    nct_study_id = fields.Integer(allow_none=True)
    results = fields.String(allow_none=True)
    updated_at = fields.DateTime(dump_only=True)
