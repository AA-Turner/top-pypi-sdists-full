from marshmallow import (
    Schema,
    fields,
    validate,
)


class PatentIFWResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    patent_id = fields.Integer(allow_none=True)
    patent_application_id = fields.Integer(required=True)
    appl_id = fields.String(required=True)
    document_identifier = fields.String(required=True, validate=not_blank)
    document_code = fields.String(allow_none=True)
    document_description = fields.String(allow_none=True)
    direction_category = fields.String(allow_none=True)
    official_date = fields.DateTime(allow_none=True)
    total_pages = fields.Integer(allow_none=True)
    updated_at = fields.DateTime()
