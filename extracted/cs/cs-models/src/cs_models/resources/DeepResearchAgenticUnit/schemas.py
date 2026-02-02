"""Marshmallow schemas for Deep Research Agentic Units."""

from marshmallow import Schema, fields, EXCLUDE


class DeepResearchAgenticUnitResourceSchema(Schema):
    """Schema for reading agentic unit resources."""

    class Meta:
        unknown = EXCLUDE

    id = fields.Integer(dump_only=True)
    session_id = fields.Integer(required=True)
    unit_id = fields.String(required=True)
    unit_label = fields.String(allow_none=True)
    objective = fields.String(required=True)
    depends_on = fields.String(allow_none=True)  # JSON string
    wave_number = fields.Integer(allow_none=True)
    internal_dag = fields.String(allow_none=True)  # JSON string
    internal_dag_planned = fields.Boolean(allow_none=True)
    status = fields.String(allow_none=True)
    result_s3_key = fields.String(allow_none=True)
    result_summary = fields.String(allow_none=True)
    entities_discovered = fields.String(allow_none=True)  # JSON string
    confidence = fields.Float(allow_none=True)
    gaps_identified = fields.String(allow_none=True)  # JSON string
    tokens_used = fields.Integer(allow_none=True)
    tasks_completed = fields.Integer(allow_none=True)
    tasks_failed = fields.Integer(allow_none=True)
    input_context = fields.String(allow_none=True)  # JSON string
    created_at = fields.DateTime(dump_only=True)
    started_at = fields.DateTime(allow_none=True)
    completed_at = fields.DateTime(allow_none=True)
    updated_at = fields.DateTime(dump_only=True)
    error_message = fields.String(allow_none=True)
    retry_count = fields.Integer(allow_none=True)


class DeepResearchAgenticUnitCreateSchema(Schema):
    """Schema for creating agentic units."""

    class Meta:
        unknown = EXCLUDE

    session_id = fields.Integer(required=True)
    unit_id = fields.String(required=True)
    unit_label = fields.String(allow_none=True)
    objective = fields.String(required=True)
    depends_on = fields.String(allow_none=True)  # JSON string of unit_ids
    wave_number = fields.Integer(allow_none=True, load_default=0)
