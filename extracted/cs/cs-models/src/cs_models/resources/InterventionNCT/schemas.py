from marshmallow import (
    Schema,
    fields,
    validate,
)


class InterventionNCTResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    intervention_id = fields.Integer(required=True)
    nct_study_id = fields.Integer(required=True)
    score = fields.Float(required=True)
    preferred = fields.Boolean(allow_none=True)
    study_start_date = fields.DateTime(allow_none=True)
    updated_at = fields.DateTime()
