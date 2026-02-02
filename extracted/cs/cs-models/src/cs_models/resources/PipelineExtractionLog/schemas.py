from marshmallow import Schema, fields


class PipelineExtractionLogSchema(Schema):
    id = fields.Int(dump_only=True)
    session_id = fields.Int(required=True)
    page_id = fields.Int(allow_none=True)
    log_level = fields.Str(required=True)
    message = fields.Str(required=True)
    extraction_method = fields.Str(allow_none=True)
    model_name = fields.Str(allow_none=True)
    tokens_used = fields.Int(allow_none=True)
    api_latency_ms = fields.Int(allow_none=True)
    exception_type = fields.Str(allow_none=True)
    exception_message = fields.Str(allow_none=True)
    stack_trace = fields.Str(allow_none=True)
    attempt_number = fields.Int(allow_none=True)
    max_attempts = fields.Int(allow_none=True)
    created_at = fields.DateTime(dump_only=True)


class PipelineExtractionLogResourceSchema(PipelineExtractionLogSchema):
    pass
