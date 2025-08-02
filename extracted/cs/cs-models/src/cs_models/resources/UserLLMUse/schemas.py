from marshmallow import (
    Schema,
    fields,
    validate,
)


class UserLLMUseResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    user_id = fields.String(required=True)
    model_provider = fields.String(required=True)
    model_name = fields.String(required=True)
    tokens_used = fields.Integer(required=True)
    pipeline = fields.String(required=True)
    timestamp = fields.DateTime(dump_only=True)
