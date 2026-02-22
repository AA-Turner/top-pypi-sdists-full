"""Schemas for Deep Research Report Versions."""
from marshmallow import Schema, fields, validate

from .models import ReportVersionStatusEnum


class DeepResearchReportVersionResourceSchema(Schema):
    """Schema for DeepResearchReportVersionModel."""

    not_blank = validate.Length(min=1, error="Field cannot be blank")

    id = fields.Integer(dump_only=True)
    session_id = fields.Integer(required=True)
    revision_id = fields.String(required=True, validate=not_blank)
    version_number = fields.Integer(required=True)
    mode = fields.String(allow_none=True)
    status = fields.Enum(ReportVersionStatusEnum, by_value=True)

    parent_report_version_id = fields.Integer(allow_none=True)

    feedback_payload = fields.String(allow_none=True)
    execution_arn = fields.String(allow_none=True)
    final_report_s3_key = fields.String(allow_none=True)
    error_message = fields.String(allow_none=True)

    is_deleted = fields.Boolean(allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    completed_at = fields.DateTime(allow_none=True)


class DeepResearchReportVersionCreateSchema(Schema):
    """Schema for creating a report revision."""

    revision_id = fields.String(required=True, validate=validate.Length(min=1))
    version_number = fields.Integer(required=True)
    mode = fields.String(allow_none=True)
    feedback_payload = fields.Dict(allow_none=True)
