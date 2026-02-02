from marshmallow import (
    Schema,
    fields,
    validate,
)


class PromptIndicesSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    prompt_index = fields.String(required=True)
    text = fields.String(required=True)
    metadatas = fields.String(required=True)
    vector = fields.String(required=True)
    search_type = fields.String(allow_none=True)
    updated_at = fields.DateTime()
