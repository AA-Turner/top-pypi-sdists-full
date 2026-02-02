from marshmallow import Schema, fields


class SmartDefGridCellAnswerResourceSchema(Schema):
    id = fields.String(dump_only=True)
    question_id = fields.Integer(required=True)
    smart_def_grid_id = fields.Integer(required=True)
    cell_id = fields.String(required=True)

    raw_value = fields.Float(allow_none=True)
    text_value = fields.String(allow_none=True)
    display_text = fields.String(allow_none=True)

    citations = fields.Raw(allow_none=True)              # list/dict (or keep normalized rows separately)
    extra_payload = fields.Raw(allow_none=True)          # provider-specific data

    provider = fields.String(allow_none=True)
    provider_meta = fields.Raw(allow_none=True)

    created_at = fields.DateTime(dump_only=True)

    # if you materialize normalized citations, expose them here:
    # citations_rel = fields.Nested(AnswerCitationResourceSchema, many=True, dump_only=True)
