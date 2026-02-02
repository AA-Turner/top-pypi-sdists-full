from marshmallow import (
    Schema,
    fields,
    validate,
)


class LLMCacheResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    message = fields.String(required=True)
    response = fields.String(required=True)
    model_name = fields.String(required=True)
    model_provider = fields.String(required=True)
    model_prompt = fields.String(required=True)
    updated_at = fields.DateTime()
