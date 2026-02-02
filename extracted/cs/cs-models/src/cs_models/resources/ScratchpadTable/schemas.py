from marshmallow import (
    Schema,
    fields,
    validate,
)


class ScratchpadTableResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    source_type = fields.String(required=True)
    source_id = fields.Integer(required=True)
    table_hash = fields.String(allow_none=True)
    table_info = fields.String(allow_none=True)
    table_html_file_id = fields.Integer(allow_none=True)
    updated_at = fields.DateTime()
