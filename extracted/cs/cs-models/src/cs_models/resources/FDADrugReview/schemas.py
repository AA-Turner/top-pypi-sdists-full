from marshmallow import (
    Schema,
    fields,
    validate,
)


class FDADrugReviewResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    application_docs_id = fields.String(required=True)
    application_docs_type_id = fields.Integer(required=True)
    appl_no = fields.String(required=True)
    submission_type = fields.String(allow_none=True)
    submission_no = fields.String(allow_none=True)
    application_doc_url = fields.String(allow_none=True)
    application_doc_date = fields.DateTime(allow_none=True)
    updated_at = fields.DateTime(dump_only=True)
