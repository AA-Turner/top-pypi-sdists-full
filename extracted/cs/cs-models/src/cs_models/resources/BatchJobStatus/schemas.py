from marshmallow import (
    Schema,
    fields,
    validate,
)


class BatchJobStatusResourceSchema(Schema):
    not_blank = validate.Length(min=1, error='Field cannot be blank')

    id = fields.Integer(dump_only=True)
    pipeline_id = fields.Integer(required=True)
    job_id = fields.String(required=True)
    job_def = fields.String(required=True)
    job_queue = fields.String(required=True)
    parameters = fields.String(allow_none=True)
    status = fields.String(required=True)
    reason = fields.String(allow_none=True)
    exit_code = fields.String(allow_none=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(dump_only=True)
