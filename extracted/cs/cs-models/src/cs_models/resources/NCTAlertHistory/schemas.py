"""
Marshmallow schemas for NCTAlertHistoryModel.

Provides serialization, deserialization, and validation for NCT alert history records.
"""

from marshmallow import Schema, fields, EXCLUDE


class NCTAlertHistorySchema(Schema):
    """
    Schema for serializing/deserializing NCTAlertHistoryModel.

    Used for API responses and data validation.
    """

    class Meta:
        unknown = EXCLUDE

    id = fields.Integer(dump_only=True)
    user_nct_alert_id = fields.Integer(required=True)
    user_id = fields.String(required=True)
    nct_change_id = fields.Integer(required=True)
    nct_study_id = fields.Integer(required=True)
    change_type = fields.String(allow_none=True)
    old_value = fields.String(allow_none=True)
    new_value = fields.String(allow_none=True)
    email_status = fields.String(load_default="pending")
    email_sent_at = fields.DateTime(allow_none=True)
    email_message_id = fields.String(allow_none=True)
    batch_id = fields.String(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
