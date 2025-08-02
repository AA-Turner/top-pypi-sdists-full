from marshmallow import (
    Schema,
    fields,
    validate,
)


class VAParameterViewResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    user_va_parameter_view_id = fields.Integer(required=True)
    va_parameter_id = fields.Integer(required=True)
    is_deleted = fields.Boolean(allow_none=True)
    updated_at = fields.DateTime(dump_only=True)
