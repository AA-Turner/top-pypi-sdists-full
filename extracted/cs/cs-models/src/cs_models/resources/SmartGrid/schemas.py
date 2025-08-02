from marshmallow import Schema, fields, validate
from ..SmartGridCell.schemas import SmartGridCellResourceSchema


class SmartGridResourceSchema(Schema):
    not_blank = validate.Length(min=1, error="Field cannot be blank")

    id = fields.Integer(dump_only=True)
    user_id = fields.String(required=True, validate=not_blank)
    workbook_id = fields.Integer(allow_none=True)
    table_info = fields.String(allow_none=True)
    is_deleted = fields.Boolean(allow_none=True)
    cells = fields.Nested(
        SmartGridCellResourceSchema(exclude=("smart_grid_id",)),
        many=True,
        dump_only=True,
    )
    updated_at = fields.DateTime(dump_only=True)
