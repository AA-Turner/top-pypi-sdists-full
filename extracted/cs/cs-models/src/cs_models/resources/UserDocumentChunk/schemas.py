from marshmallow import (
    Schema,
    fields,
    validate,
)


class UserDocumentChunkResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    user_document_id = fields.Integer(required=True)
    chunk_cui = fields.String(required=True)
    chunk_text = fields.String(required=True)
    chunk_embedding = fields.String(required=True)
    embedding_source = fields.String(required=True)
    is_deleted = fields.Boolean(allow_none=True)
    updated_at = fields.DateTime(dump_only=True)
