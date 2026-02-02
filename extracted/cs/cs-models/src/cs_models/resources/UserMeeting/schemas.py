from marshmallow import (
    Schema,
    fields,
)


class UserMeetingResourceSchema(Schema):
    id = fields.Integer(dump_only=True)
    user_id = fields.String(required=True)
    meeting_id = fields.Integer(required=True)
    notification_status = fields.Boolean(allow_none=True)
    updated_at = fields.DateTime(dump_only=True)
