from marshmallow import Schema, fields, validate


class SmartDefGridRunResourceSchema(Schema):
    """
        The user-defined table artifact (aka 'SmartDefGrid' resource).
        - id is your table_id (UUID string or int—your choice).
        - outline_json/original_table_json can be dicts (preferred) or JSON strings if you’d rather store serialized blobs.
        """
    not_blank = validate.Length(min=1, error="Field cannot be blank")

    id = fields.String(dump_only=True)  # table_id
    smart_def_grid_id = fields.Integer(allow_none=True)  # if you link to a workbook

    scope_mode = fields.String(required=True)

    # prefer dicts; switch to fields.String if you store JSON-serialized strings
    outline_json = fields.Raw(required=True)
    original_table_json = fields.Raw(required=True)
    targets_json = fields.Raw(allow_none=True)

    status = fields.String(required=True)
    started_by_user_id = fields.String(required=True)

    notes = fields.String(allow_none=True)
    client_token = fields.String(allow_none=True)

    created_at = fields.DateTime(dump_only=True)
    started_at = fields.DateTime(allow_none=True)
    finished_at = fields.DateTime(allow_none=True)
    updated_at = fields.DateTime(dump_only=True)
