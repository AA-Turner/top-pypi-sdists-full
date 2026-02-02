from marshmallow import (
    Schema,
    fields,
    validate,
)


class ModalityBucketResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    modality_bucket = fields.String(required=True)
    updated_at = fields.DateTime()
