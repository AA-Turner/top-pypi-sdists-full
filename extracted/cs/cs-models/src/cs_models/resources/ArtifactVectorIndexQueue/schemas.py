from marshmallow import (
    Schema,
    fields,
    validate,
)


class ArtifactVectorIndexQueueResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    artifact_id = fields.String(required=True)
    attempts = fields.Integer(allow_none=True)
    submitted = fields.Boolean(allow_none=True)
    submitted_date = fields.DateTime(allow_none=True)
    error = fields.String(allow_none=True)
    updated_at = fields.DateTime()
