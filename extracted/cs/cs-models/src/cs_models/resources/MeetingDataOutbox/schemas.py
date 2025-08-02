from marshmallow import (
    Schema,
    fields,
    validate,
)


class MeetingDataOutboxResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    meeting_id = fields.Integer(allow_none=True)
    meeting_name = fields.String(required=True)
    start_date = fields.DateTime(required=True)
    end_date = fields.DateTime(required=True)
    from_website = fields.Boolean(allow_none=True)
    meeting_bucket_id = fields.Integer(allow_none=True)
    reviewed = fields.Boolean(allow_none=True)
    submitted = fields.Boolean(allow_none=True)
    submitted_date = fields.DateTime(allow_none=True)
    file_id = fields.Integer(allow_none=True)
    error = fields.String(allow_none=True)
    checks = fields.String(allow_none=True)
    completed = fields.Boolean(allow_none=True)
    data_entry_type = fields.String(allow_none=True)
    note = fields.String(allow_none=True)
    updated_at = fields.DateTime()
