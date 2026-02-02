from marshmallow import (
    Schema,
    fields,
    validate,
)


class UserDocumentHierarchyResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    provider_id = fields.String(required=True)
    user_id = fields.String(required=True)
    type = fields.String(required=True)
    document_name = fields.String(allow_none=True)
    parent_id = fields.Integer(allow_none=True)
    is_folder = fields.Boolean(allow_none=True)
    user_document_id = fields.Integer(allow_none=True)
    workbook_id = fields.Integer(allow_none=True)
    sha1 = fields.String(allow_none=True)
    is_deleted = fields.Boolean(allow_none=True)
    is_trashed = fields.Boolean(allow_none=True)
    is_locked = fields.Boolean(allow_none=True)
    updated_at = fields.DateTime(dump_only=True)
