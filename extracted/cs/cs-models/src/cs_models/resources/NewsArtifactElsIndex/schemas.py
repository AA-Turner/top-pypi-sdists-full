from marshmallow import (
    Schema,
    fields,
    validate,
)


class NewsArtifactsElsIndexResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    artifact_id = fields.String(required=True)
    els_indexed = fields.Boolean(allow_none=True)
    updated_at = fields.DateTime()
