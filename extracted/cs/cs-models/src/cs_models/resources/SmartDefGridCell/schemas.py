from marshmallow import Schema, fields, validate
from ..SmartDefGridCellQuestion.schemas import SmartDefGridCellQuestionResourceSchema
from ..SmartDefGridCellValue.schemas import SmartDefGridCellValueResourceSchema


class SmartDefGridCellResourceSchema(Schema):
    """
    One logical (master) cell from the user-defined table.
    """
    not_blank = validate.Length(min=1, error="Field cannot be blank")

    smart_def_grid_id = fields.Integer(required=True)
    cell_id = fields.String(required=True)

    row = fields.Integer(required=True)
    col = fields.Integer(required=True)
    row_span = fields.Integer(required=True, data_key="rowSpan")
    col_span = fields.Integer(required=True, data_key="colSpan")
    is_header = fields.Boolean(required=True)

    header_path_row = fields.List(fields.String(), required=True, data_key="headerPathRow")
    header_path_col = fields.List(fields.String(), required=True, data_key="headerPathCol")

    formatting_spec = fields.Raw(allow_none=True, data_key="formattingSpec")

    latest_question_id = fields.String(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    # optional, read-only projections
    latest_question = fields.Nested(
        SmartDefGridCellQuestionResourceSchema(),
        dump_only=True,
        exclude=("answers",),
    )
    applied_value = fields.Nested(
        SmartDefGridCellValueResourceSchema(),
        dump_only=True,
    )
