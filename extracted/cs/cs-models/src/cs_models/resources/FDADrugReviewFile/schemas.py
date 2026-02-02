from marshmallow import (
    Schema,
    fields,
    validate,
)


class FDADrugReviewFileResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    fda_drug_review_id = fields.Integer(required=True)
    file_id = fields.Integer(required=True)
    date = fields.DateTime(allow_none=True)
    title = fields.String(allow_none=True)
    page_count = fields.Integer(allow_none=True)
    type = fields.String(allow_none=True)
    orig_file_url = fields.String(allow_none=True)
    is_deleted = fields.Boolean(allow_none=True)
    unprocessed = fields.Boolean(allow_none=True)
    reviewed = fields.Boolean(allow_none=True)
    updated_at = fields.DateTime(dump_only=True)
