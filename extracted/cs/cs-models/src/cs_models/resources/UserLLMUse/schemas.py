from marshmallow import (
    Schema,
    fields,
    validate,
)


class UserLLMUseResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    user_id = fields.String(required=True)
    user_query_id = fields.Integer(allow_none=True)
    model_provider = fields.String(required=True)
    model_name = fields.String(required=True)
    input_tokens = fields.Integer(load_default=0)
    thinking_tokens = fields.Integer(load_default=0)
    output_tokens = fields.Integer(load_default=0)
    tokens_used = fields.Integer(load_default=0)
    pipeline = fields.String(required=True)
    timestamp = fields.DateTime()
