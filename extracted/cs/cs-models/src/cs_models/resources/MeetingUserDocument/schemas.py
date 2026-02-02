from marshmallow import (
    Schema,
    fields,
    validate,
)


class MeetingUserDocumentResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    meeting_id = fields.Integer(required=True)
    user_document_id = fields.Integer(required=True)
    status = fields.String(required=True)
    is_active = fields.Boolean(allow_none=True)
    details = fields.String(allow_none=True)
    updated_at = fields.DateTime()
