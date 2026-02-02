from marshmallow import (
    Schema,
    fields,
    validate,
)


class VAParameterResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    pid = fields.Integer(required=True)
    cid = fields.Integer(required=True)
    pname = fields.String(required=True)
    ciso = fields.String(allow_none=True)
    u = fields.Integer(allow_none=True)
    sign = fields.String(allow_none=True)
    ppid = fields.Integer(allow_none=True)
    ftid = fields.Integer(allow_none=True)
    dpname = fields.String(allow_none=True)
    scid = fields.Integer(allow_none=True)
    so = fields.Integer(allow_none=True)
    llm_output = fields.String(allow_none=True)
    needs_review = fields.Boolean(allow_none=True)
    updated_at = fields.DateTime(dump_only=True)
