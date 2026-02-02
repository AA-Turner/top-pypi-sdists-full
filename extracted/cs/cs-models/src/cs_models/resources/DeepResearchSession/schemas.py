"""Schemas for Deep Research Sessions."""
from marshmallow import Schema, fields, validate

from .models import DeepResearchStatusEnum, HITLStatusEnum


class DeepResearchSessionResourceSchema(Schema):
    """Schema for DeepResearchSessionModel."""

    not_blank = validate.Length(min=1, error="Field cannot be blank")

    id = fields.Integer(dump_only=True)
    user_id = fields.String(required=True, validate=not_blank)
    org_id = fields.String(allow_none=True)
    workbook_id = fields.Integer(allow_none=True)

    # Query and config
    original_query = fields.String(required=True)
    research_config = fields.String(allow_none=True)

    # Status
    status = fields.Enum(DeepResearchStatusEnum, by_value=True)
    current_phase = fields.String(allow_none=True)

    # Step Functions
    step_function_arn = fields.String(allow_none=True)
    step_function_execution_arn = fields.String(allow_none=True)

    # Progress
    total_subtasks = fields.Integer(allow_none=True)
    completed_subtasks = fields.Integer(allow_none=True)
    failed_subtasks = fields.Integer(allow_none=True)

    # HITL
    hitl_status = fields.Enum(HITLStatusEnum, by_value=True)
    hitl_type = fields.String(allow_none=True)
    hitl_questions = fields.String(allow_none=True)
    hitl_responses = fields.String(allow_none=True)
    hitl_task_token = fields.String(allow_none=True)
    hitl_requested_at = fields.DateTime(allow_none=True)
    hitl_responded_at = fields.DateTime(allow_none=True)

    # Results
    final_report_s3_key = fields.String(allow_none=True)
    executive_summary = fields.String(allow_none=True)
    smart_grid_id = fields.Integer(allow_none=True)

    # Metadata
    total_citations = fields.Integer(allow_none=True)
    average_confidence = fields.Float(allow_none=True)
    total_documents_analyzed = fields.Integer(allow_none=True)

    # Error handling
    error_message = fields.String(allow_none=True)
    retry_count = fields.Integer(allow_none=True)

    # Timestamps
    is_deleted = fields.Boolean(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    completed_at = fields.DateTime(allow_none=True)

    # Nested relationships (dump only)
    subtasks = fields.Nested(
        "DeepResearchSubTaskResourceSchema",
        many=True,
        dump_only=True,
        exclude=("session_id",),
    )


class DeepResearchSessionCreateSchema(Schema):
    """Schema for creating a new Deep Research Session."""

    not_blank = validate.Length(min=1, error="Field cannot be blank")

    original_query = fields.String(required=True, validate=not_blank)
    workbook_id = fields.Integer(allow_none=True)
    research_config = fields.Dict(allow_none=True)  # Will be serialized to JSON


class DeepResearchSessionProgressSchema(Schema):
    """Schema for returning session progress."""

    id = fields.Integer()
    status = fields.Enum(DeepResearchStatusEnum, by_value=True)
    current_phase = fields.String(allow_none=True)
    total_subtasks = fields.Integer()
    completed_subtasks = fields.Integer()
    failed_subtasks = fields.Integer()
    hitl_status = fields.Enum(HITLStatusEnum, by_value=True)
    hitl_type = fields.String(allow_none=True)
    hitl_questions = fields.String(allow_none=True)
    error_message = fields.String(allow_none=True)
