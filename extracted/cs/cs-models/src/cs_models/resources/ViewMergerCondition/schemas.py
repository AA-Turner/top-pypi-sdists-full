from marshmallow import (
    Schema,
    fields,
    validate,
)


class ViewMergerConditionResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    merger_id = fields.Integer(required=True)
    condition_id = fields.Integer(required=True)
    stage = fields.Integer(allow_none=True)
    updated_at = fields.DateTime()
