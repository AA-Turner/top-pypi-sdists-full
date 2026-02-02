from marshmallow import (
    Schema,
    fields,
    validate,
)


class PubmedUpdateLedgerResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    pubmed_cui = fields.Integer(required=True)
    file_name_id = fields.Integer(required=True)
    file_name = fields.String(required=True)
    date = fields.DateTime(required=True)
    updated_at = fields.DateTime()
