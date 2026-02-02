from marshmallow import (
    Schema,
    fields,
    validate,
)


class UserWorkbookWorkflowsResourceSchema(Schema):
    not_blank = validate.Length(min=1, error="Field cannot be blank")

    id = fields.Integer(dump_only=True)
    user_id = fields.String(required=True, validate=not_blank)
    is_active = fields.Boolean(required=True)
    workflow_template = fields.String(allow_none=True)
    updated_at = fields.DateTime(dump_only=True)
