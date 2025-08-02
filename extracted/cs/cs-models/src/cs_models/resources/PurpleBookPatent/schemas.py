from marshmallow import (
    Schema,
    fields,
    validate,
)


class PurpleBookPatentResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    bla_number = fields.String(required=True)
    applicant_name = fields.String(required=True)
    proprietary_name = fields.String(required=True)
    proper_name = fields.String(required=True)
    patent_number = fields.String(required=True)
    expiration_date = fields.DateTime(allow_none=True)
    updated_at = fields.DateTime(dump_only=True)
