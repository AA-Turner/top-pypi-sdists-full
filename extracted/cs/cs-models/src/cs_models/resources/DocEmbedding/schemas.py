from marshmallow import (
    Schema,
    fields,
    validate,
)


class DocEmbeddingResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    source_type = fields.String(required=True)
    source_id = fields.Integer(required=True)
    embedding_source = fields.String(required=True)
    embedding = fields.String(allow_none=True)
    updated_at = fields.DateTime()
