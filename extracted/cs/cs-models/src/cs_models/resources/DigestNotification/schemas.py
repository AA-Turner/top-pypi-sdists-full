from marshmallow import (
    Schema,
    fields,
    validate,
)


class DigestNotificationResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    digest_id = fields.Integer(required=True)
    notification_id = fields.Integer(required=True)
    updated_at = fields.DateTime()
