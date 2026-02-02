from marshmallow import (
    Schema,
    fields,
    validate,
)


class ArtifactVectorIndexResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    artifact_id = fields.String(required=True)
    embedding_created = fields.Boolean(allow_none=True)
    embedding_s3_key = fields.String(allow_none=True)
    vector_indexed = fields.Boolean(allow_none=True)
    updated_at = fields.DateTime()
