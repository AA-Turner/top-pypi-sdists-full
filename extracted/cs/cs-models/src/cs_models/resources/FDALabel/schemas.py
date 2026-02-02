from marshmallow import (
    Schema,
    fields,
    validate,
)


class FDALabelResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    set_id = fields.String(required=True)
    doc_id = fields.String(required=True)
    date = fields.DateTime(required=True)
    version = fields.String(required=True)
    section_id = fields.String(required=True)
    section_text = fields.String(allow_none=True)
    section_type = fields.String(required=True)
    section_html_file_id = fields.Integer(allow_none=True)
    label_html_file_id = fields.Integer(required=True)
    is_active = fields.Boolean(allow_none=True)
    vector_active = fields.Boolean(allow_none=True)
    updated_at = fields.DateTime(dump_only=True)
