from marshmallow import (
    Schema,
    fields,
    validate,
)


class NoteResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    note_hash = fields.String(required=True)
    note_heading = fields.String(required=True)
    note = fields.String(required=True)
    note_insights = fields.String(allow_none=True)
    updated_at = fields.DateTime()
