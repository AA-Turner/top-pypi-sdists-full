from marshmallow import (
    Schema,
    fields,
    validate,
)


class ViewPublicationNCTResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    nct_study_id = fields.Integer(required=True)
    date = fields.DateTime(required=True)
    table_name = fields.String(required=True)
    table_id = fields.Integer(required=True)
    updated_at = fields.DateTime()
