from marshmallow import (
    Schema,
    fields,
    validate,
)
from ..WorkbookBlock.schemas import (
    WorkbookBlockResourceSchema,
)


class WorkbookResourceSchema(Schema):
    not_blank = validate.Length(min=1, error="Field cannot be blank")

    id = fields.Integer(dump_only=True)
    user_id = fields.String(required=True, validate=not_blank)
    workbook_name = fields.String(required=True)
    blocks = fields.Nested(
        WorkbookBlockResourceSchema(exclude=("workbook_id",)),
        many=True,
        dump_only=True,
    )
    is_deleted = fields.Boolean(allow_none=True)
    is_public = fields.Boolean(allow_none=True)
    is_help_center = fields.Boolean(allow_none=True)
    created_at = fields.DateTime(required=True)
    updated_at = fields.DateTime(dump_only=True)
