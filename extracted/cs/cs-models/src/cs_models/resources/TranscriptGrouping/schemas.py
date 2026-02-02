from marshmallow import (
    Schema,
    fields,
    validate,
)


class TranscriptGroupingResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    grouping_id = fields.Integer(required=True)
    grouping_name = fields.String(required=True)
    updated_at = fields.DateTime()
