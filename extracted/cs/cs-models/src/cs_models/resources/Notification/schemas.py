from marshmallow import (
    Schema,
    fields,
    validate,
)


class NotificationResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    saved_search_id = fields.Integer(required=True)
    source_type = fields.String(required=True)
    source_table = fields.String(required=True)
    source_id = fields.Integer(required=True)
    artifact_id = fields.String(required=True)
    text = fields.String(allow_none=True)
    score = fields.Float(allow_none=True)
    source_detail = fields.String(required=True)
    seen_at = fields.DateTime(allow_none=True)
    processed_at = fields.DateTime(allow_none=True)
    daily_processed_at = fields.DateTime(allow_none=True)
    weekly_processed_at = fields.DateTime(allow_none=True)
    date = fields.DateTime(required=True)
    updated_at = fields.DateTime()
