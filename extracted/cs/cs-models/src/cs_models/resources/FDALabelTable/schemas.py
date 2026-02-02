from marshmallow import (
    Schema,
    fields,
    validate,
)


class FDALabelTableResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    fda_label_id = fields.Integer(required=True)
    table_text = fields.String(required=True)
    table_info = fields.String(allow_none=True)
    table_hash = fields.String(allow_none=True)
    is_deleted = fields.Boolean(allow_none=True)
    updated_at = fields.DateTime()
