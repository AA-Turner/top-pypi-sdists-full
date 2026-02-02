from marshmallow import (
    Schema,
    fields,
    validate,
)
from ..WorkbookWorkflowBlock.schemas import (
    WorkbookWorkflowBlockResourceSchema,
)


class WorkbookWorkflowResourceSchema(Schema):
    not_blank = validate.Length(min=1, error="Field cannot be blank")

    id = fields.Integer(dump_only=True)
    workbook_id = fields.Integer(required=True)
    status = fields.String(required=True)
    is_completed = fields.Boolean(allow_none=True)
    is_deleted = fields.Boolean(allow_none=True)
    workflow_blocks = fields.Nested(
        WorkbookWorkflowBlockResourceSchema(exclude=("workflow_id",)),
        many=True,
        dump_only=True,
    )
    updated_at = fields.DateTime(dump_only=True)
