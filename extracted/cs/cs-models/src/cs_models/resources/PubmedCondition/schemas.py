from marshmallow import (
    Schema,
    fields,
    validate,
)


class PubmedConditionResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    pubmed_id = fields.Integer(required=True)
    condition_id = fields.Integer(required=True)
    score = fields.Float(required=True)
    preferred = fields.Boolean(allow_none=True)
    data_readout = fields.Boolean(allow_none=True)
    date = fields.DateTime(allow_none=True)
    updated_at = fields.DateTime()
