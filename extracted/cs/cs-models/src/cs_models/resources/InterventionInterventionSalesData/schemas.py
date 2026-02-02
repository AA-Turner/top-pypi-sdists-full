from marshmallow import (
    Schema,
    fields,
    validate,
)


class InterventionInterventionSalesDataResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    intervention_id = fields.Integer(required=True)
    intervention_sales_data_id = fields.Integer(required=True)
    score = fields.Float(required=True)
    is_deleted = fields.Boolean(allow_none=True)
    updated_at = fields.DateTime()
