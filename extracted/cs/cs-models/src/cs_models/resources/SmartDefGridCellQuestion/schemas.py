from marshmallow import Schema, fields, validate
from ..SmartDefGridCellAnswer.schemas import SmartDefGridCellAnswerResourceSchema


QUESTION_STATUS = ["pending", "queued", "running", "succeeded", "failed", "cancelled"]
EXPECTED_TYPE = ["number", "text", "citationList", "json"]


class SmartDefGridCellQuestionResourceSchema(Schema):
    not_blank = validate.Length(min=1, error="Field cannot be blank")

    id = fields.String(dump_only=True)
    smart_def_grid_id = fields.Integer(required=True)
    run_id = fields.Integer(allow_none=True)
    cell_id = fields.String(required=True)

    question_text = fields.String(required=True, validate=not_blank)
    expected_type = fields.String(required=True, validate=validate.OneOf(EXPECTED_TYPE))
    must_cite = fields.Boolean(required=True)

    topic_key = fields.Raw(allow_none=True)              # e.g., {"row":[...], "col":[...]}
    retrieval_hints = fields.Raw(allow_none=True)

    answer_text = fields.String(allow_none=True)
    answer_info = fields.Raw(allow_none=True)

    status = fields.String(required=True, validate=validate.OneOf(QUESTION_STATUS))
    priority = fields.Integer(required=True)
    attempts = fields.Integer(required=True)
    last_error = fields.String(allow_none=True)

    idempotency_key = fields.String(allow_none=True)
    dedupe_hash = fields.String(allow_none=True)

    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    started_at = fields.DateTime(dump_only=True)
    finished_at = fields.DateTime(dump_only=True)

    # light nesting of answers on read
    answers = fields.Nested(SmartDefGridCellAnswerResourceSchema(), many=True, dump_only=True)
