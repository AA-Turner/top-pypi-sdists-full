from marshmallow import (
    Schema,
    fields,
)


class VAAlertHistoryResourceSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_va_alert_id = fields.Integer(required=True)
    user_id = fields.String(required=True)
    threshold_percent = fields.Float(required=True)
    old_value = fields.Float(allow_none=True)
    new_value = fields.Float(allow_none=True)
    actual_change_percent = fields.Float(required=True)
    old_revision_date = fields.DateTime(allow_none=True)
    new_revision_date = fields.DateTime(allow_none=True)
    email_sent_at = fields.DateTime(allow_none=True)
    email_status = fields.String(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
