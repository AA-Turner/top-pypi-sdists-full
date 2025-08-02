from marshmallow import (
    Schema,
    fields,
    validate,
)


class UserDocumentResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    user_id = fields.String(required=True)
    file_id = fields.Integer(required=True)
    date = fields.DateTime(allow_none=True)
    title = fields.String(allow_none=True)
    type = fields.String(allow_none=True)
    type_score = fields.Float(allow_none=True)
    is_deleted = fields.Boolean(allow_none=True)
    upload_date = fields.DateTime(required=True)
    metadata_info = fields.String(allow_none=True)
    category = fields.String(allow_none=True)
    status = fields.String(allow_none=True)
    page_count = fields.Integer(allow_none=True)
    updated_at = fields.DateTime(dump_only=True)
