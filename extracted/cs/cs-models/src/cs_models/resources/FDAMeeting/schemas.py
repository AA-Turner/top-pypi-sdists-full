from marshmallow import (
    Schema,
    fields,
    validate,
)


class FDAMeetingResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    meeting_type = fields.String(required=True)
    meeting_name = fields.String(required=True)
    start_date = fields.DateTime(required=True)
    end_date = fields.DateTime(required=True)
    center = fields.String(allow_none=True)
    agenda = fields.String(allow_none=True)
    meeting_link = fields.String(allow_none=True)
    updated_at = fields.DateTime(dump_only=True)
