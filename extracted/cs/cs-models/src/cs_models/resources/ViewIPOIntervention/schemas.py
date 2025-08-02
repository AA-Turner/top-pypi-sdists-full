from marshmallow import (
    Schema,
    fields,
    validate,
)


class ViewIPOInterventionResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    ipo_id = fields.Integer(required=True)
    intervention_id = fields.Integer(required=True)
    updated_at = fields.DateTime()
