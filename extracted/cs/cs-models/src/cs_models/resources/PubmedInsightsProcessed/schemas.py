from marshmallow import (
    Schema,
    fields,
    validate,
)


class PubmedInsightsProcessedResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    pubmed_id = fields.Integer(required=True)
    s3 = fields.Boolean(allow_none=True)
    db = fields.Boolean(allow_none=True)
    date = fields.DateTime(allow_none=True)
    updated_at = fields.DateTime()
