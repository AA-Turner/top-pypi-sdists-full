from marshmallow import (
    Schema,
    fields,
    validate,
)


class LLMQueueResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    source_type = fields.String(required=True)
    source_id = fields.Integer(required=True)
    llm_task_type = fields.String(required=True)
    processed = fields.Boolean(allow_none=True)
    error = fields.String(allow_none=True)
    submitted = fields.Boolean(allow_none=True)
    submitted_date = fields.DateTime(allow_none=True)
    historical = fields.Boolean(allow_none=True)
    updated_at = fields.DateTime(dump_only=True)
