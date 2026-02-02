from marshmallow import (
    Schema,
    fields,
    validate,
)


class VAParameterValueResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    va_parameter_id = fields.Integer(required=True)
    pid = fields.Integer(required=True)
    cid = fields.Integer(required=True)
    sid = fields.Integer(allow_none=True)
    r = fields.DateTime(allow_none=True)
    p = fields.String(allow_none=True)
    ap = fields.String(allow_none=True)
    v = fields.Float(allow_none=True)
    ciso = fields.String(allow_none=True)
    csym = fields.String(allow_none=True)
    u = fields.Integer(allow_none=True)
    mdt = fields.DateTime(allow_none=True)
    vt = fields.String(allow_none=True)
    dt = fields.String(allow_none=True)
    b = fields.Integer(allow_none=True)
    updated_at = fields.DateTime(dump_only=True)
