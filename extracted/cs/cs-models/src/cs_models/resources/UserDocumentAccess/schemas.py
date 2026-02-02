from marshmallow import (
    Schema,
    fields,
    validate,
)


class UserDocumentAccessResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    user_id = fields.String(required=True)
    user_document_id = fields.Integer(required=True)
    provider_permission_id = fields.String(allow_none=True)
    is_inherited = fields.Boolean(allow_none=True)
    source_provider = fields.String(allow_none=True)
    is_deleted = fields.Boolean(allow_none=True)
    synced_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(dump_only=True)
