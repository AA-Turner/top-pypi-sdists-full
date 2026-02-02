from marshmallow import (
    Schema,
    fields,
    validate,
)


class DocChunkResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    artifact_id = fields.String(required=True)
    chunk_cui = fields.String(required=True)
    chunk_text = fields.String(required=True)
    chunk_embedding = fields.String(required=True)
    embedding_source = fields.String(required=True)
    is_deleted = fields.Boolean(allow_none=True)
    is_indexed = fields.Boolean(allow_none=True)
    indexed_date = fields.DateTime(allow_none=True)
    updated_at = fields.DateTime(dump_only=True)
