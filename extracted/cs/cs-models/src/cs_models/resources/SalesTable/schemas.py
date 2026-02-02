from marshmallow import (
    Schema,
    fields,
    validate,
)


class SalesTableResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    sec_accession_number = fields.String(required=True)
    sec_cik = fields.String(required=True)
    sec_file_name = fields.String(required=True)
    table_number = fields.Integer(required=True)
    table_html = fields.String(required=True)
    table_preceding_info = fields.String(required=True)
    score = fields.Float(allow_none=True)
    processed = fields.Boolean(allow_none=True)
    updated_at = fields.DateTime()
