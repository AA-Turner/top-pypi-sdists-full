from marshmallow import (
    Schema,
    fields,
    validate,
)


class MergerActionRecordeResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    merger_action_id = fields.Integer(required=True)
    table = fields.String(required=True)
    record_id = fields.Integer(required=True)
    updated_at = fields.DateTime()
