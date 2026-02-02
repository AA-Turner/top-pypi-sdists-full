from marshmallow import (
    Schema,
    fields,
    validate,
)


class InterventionNormNoteLinkResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    norm_cui = fields.String(required=True)
    notes = fields.String(allow_none=True)
    is_external = fields.Boolean(allow_none=True)
    is_deleted = fields.Boolean(allow_none=True)
    updated_at = fields.DateTime()
