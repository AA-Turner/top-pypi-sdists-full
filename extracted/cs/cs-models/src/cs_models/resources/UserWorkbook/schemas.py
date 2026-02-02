from marshmallow import (
    Schema,
    fields,
    validate,
)


class UserWorkbookResourceSchema(Schema):
    not_blank = validate.Length(min=1, error="Field cannot be blank")

    id = fields.Integer(dump_only=True)
    user_id = fields.String(required=True, validate=not_blank)
    is_active = fields.Boolean(required=True)
    workbook_id = fields.Integer(required=True)
    updated_at = fields.DateTime(dump_only=True)
