# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel

__all__ = [
    "TraceInsightListResponse",
    "TraceInsight",
    "TraceInsightInsights",
    "TraceInsightInsightsOutputAnalysis",
    "TraceInsightInsightsOutputAnalysisErrorClassification",
    "TraceInsightInsightsOutputAnalysisPerformanceMetrics",
    "TraceInsightInsightsOutputAnalysisPerformanceMetricsAggregateScores",
]


class TraceInsightInsightsOutputAnalysisErrorClassification(BaseModel):
    description: Optional[str] = None

    evidence: Optional[str] = None

    explanation: Optional[str] = None

    immediate_fix: Optional[str] = None

    impact_details: Optional[str] = None

    impact_level: Optional[Literal["LOW", "MEDIUM", "MEDIUM-HIGH", "HIGH", "UNKNOWN", "NONE"]] = None

    spans: Optional[List[str]] = None

    suggested_prompt_fix: Optional[str] = None

    type: str


class TraceInsightInsightsOutputAnalysisPerformanceMetricsAggregateScores(BaseModel):
    instruction_adherence_score: Optional[str] = None

    overall_score: Optional[str] = None

    plan_optimality_score: Optional[str] = None

    reliability_score: Optional[str] = None

    security_score: Optional[str] = None


class TraceInsightInsightsOutputAnalysisPerformanceMetrics(BaseModel):
    aggregate_scores: Optional[TraceInsightInsightsOutputAnalysisPerformanceMetricsAggregateScores] = None


class TraceInsightInsightsOutputAnalysis(BaseModel):
    error_classification: Optional[List[TraceInsightInsightsOutputAnalysisErrorClassification]] = None

    overall_evaluation_analysis: Optional[str] = None

    performance_metrics: Optional[TraceInsightInsightsOutputAnalysisPerformanceMetrics] = None

    span_error_rate: Optional[str] = None


class TraceInsightInsights(BaseModel):
    input_analysis: Optional[str] = None

    output_analysis: Optional[TraceInsightInsightsOutputAnalysis] = None


class TraceInsight(BaseModel):
    app: Optional[str] = None

    created_at: datetime

    error_message: Optional[str] = None

    experiment_id: Optional[str] = None

    insights: Optional[TraceInsightInsights] = None

    job_id: str

    processing_status: Literal["pending", "success", "failed", "cancelled"]

    project_id: str

    trace_id: str


class TraceInsightListResponse(BaseModel):
    trace_insights: List[TraceInsight]
