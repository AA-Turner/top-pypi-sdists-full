from marshmallow import (
    Schema,
    fields,
    validate,
)


class ViewInterventionNormDataResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    norm_cui = fields.String(required=True)
    date = fields.DateTime(required=True)
    table_name = fields.String(required=True)
    table_id = fields.Integer(required=True)
    pivotal = fields.Boolean(allow_none=True)
    intervention_data_info_id = fields.Integer(allow_none=True)
    updated_at = fields.DateTime()
