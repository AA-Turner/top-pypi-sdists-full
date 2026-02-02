"""
Marshmallow schemas for UserNCTAlertModel.

Provides serialization, deserialization, and validation for user NCT alert subscriptions.
"""

from marshmallow import Schema, fields, EXCLUDE


class UserNCTAlertResourceSchema(Schema):
    """
    Schema for serializing/deserializing UserNCTAlertModel.

    Used for API responses and data validation.
    """

    class Meta:
        unknown = EXCLUDE

    id = fields.Integer(dump_only=True)
    user_id = fields.String(required=True)
    nct_study_id = fields.Integer(required=True)
    is_active = fields.Boolean(load_default=True)
    is_deleted = fields.Boolean(load_default=False, dump_only=True)
    last_notified_at = fields.DateTime(dump_only=True, allow_none=True)
    last_notified_change_id = fields.Integer(dump_only=True, allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True, allow_none=True)
