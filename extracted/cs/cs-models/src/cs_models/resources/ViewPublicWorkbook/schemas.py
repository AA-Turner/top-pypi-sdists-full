from marshmallow import (
    Schema,
    fields,
    validate,
)


class ViewPublicWorkbookResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    workbook_id = fields.Integer(required=True)
    data = fields.String(allow_none=True)
    updated_at = fields.DateTime()
