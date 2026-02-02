from marshmallow import (
    Schema,
    fields,
    validate,
)


class ConditionNormSynResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    alias = fields.String(required=True, validate=not_blank)
    condition_norm_cui = fields.String(required=True)
    updated_at = fields.DateTime()
