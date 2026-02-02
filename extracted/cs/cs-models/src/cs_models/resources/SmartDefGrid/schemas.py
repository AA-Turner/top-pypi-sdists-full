from marshmallow import Schema, fields, validate
from ..SmartDefGridCell.schemas import SmartDefGridCellResourceSchema


class SmartDefGridResourceSchema(Schema):
    """
        The user-defined table artifact (aka 'SmartDefGrid' resource).
        - id is your table_id (UUID string or int—your choice).
        - outline_json/original_table_json can be dicts (preferred) or JSON strings if you’d rather store serialized blobs.
        """
    not_blank = validate.Length(min=1, error="Field cannot be blank")

    id = fields.String(dump_only=True)  # table_id
    workbook_id = fields.Integer(allow_none=True)  # if you link to a workbook
    source_block_id = fields.String(allow_none=True)

    outline_version = fields.Integer(allow_none=True)
    # prefer dicts; switch to fields.String if you store JSON-serialized strings
    outline_json = fields.Raw(required=True)
    original_table_json = fields.Raw(required=True)

    # read-only expansion of cells
    cells = fields.Nested(
        SmartDefGridCellResourceSchema(exclude=["smart_def_grid_id"]),
        many=True,
        dump_only=True,
        # if you strictly want to hide 'table_id' inside each cell in this view:
        # exclude=("table_id",),
    )

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class SmartDefGridDetailResourceSchema(Schema):
    id = fields.String(dump_only=True)
    workbook_id = fields.String(allow_none=True)
    source_block_id = fields.String(allow_none=True)
    outline_version = fields.Integer(allow_none=True)
    outline_json = fields.Raw(required=True)
    original_table_json = fields.Raw(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    cells = fields.Nested(
        SmartDefGridCellResourceSchema(),
        many=True,
        dump_only=True,
        # include answers inlined under latest_question if you like:
        only=("table_id","cell_id","row","col","is_header","formatting_spec",
              "latest_question","applied_value"),
    )
