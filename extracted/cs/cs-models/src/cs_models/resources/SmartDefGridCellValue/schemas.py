from marshmallow import Schema, fields


class SmartDefGridCellValueResourceSchema(Schema):
    smart_def_grid_id = fields.Integer(required=True)
    applied_run_id = fields.Integer(allow_none=True)
    cell_id = fields.String(required=True)

    answer_id = fields.Integer(allow_none=True)
    raw_value = fields.Float(allow_none=True)
    display_text = fields.String(allow_none=True)
    citations = fields.Raw(allow_none=True)
    formatting_used = fields.Raw(allow_none=True)

    manual_override = fields.Boolean(required=True, default=False)
    note = fields.String(allow_none=True)

    applied_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
