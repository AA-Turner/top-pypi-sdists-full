from marshmallow import (
    Schema,
    fields,
    validate,
)


class BatchPipelineResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    index_name = fields.String(required=True)
    pipeline = fields.String(required=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(dump_only=True)
