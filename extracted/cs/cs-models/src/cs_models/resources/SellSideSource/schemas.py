from marshmallow import Schema, fields, validate


class SellSideSourceResourceSchema(Schema):
    id = fields.Integer(dump_only=True)

    # e.g. "Morgan Stanley"
    name = fields.String(required=True, validate=validate.Length(min=1))
    # e.g. "MS", "JPM"
    code = fields.String(allow_none=True)

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
