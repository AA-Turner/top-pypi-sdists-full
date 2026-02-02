from marshmallow import (
    Schema,
    fields,
    validate,
)


class UserWorkbookWorkflowsSharedResourceSchema(Schema):
    not_blank = validate.Length(min=1, error="Field cannot be blank")

    id = fields.Integer(dump_only=True)
    user_id = fields.String(required=True, validate=not_blank)
    user_workbook_workflow_id = fields.Integer(required=True)
    is_active = fields.Boolean(required=True)
    updated_at = fields.DateTime(dump_only=True)
