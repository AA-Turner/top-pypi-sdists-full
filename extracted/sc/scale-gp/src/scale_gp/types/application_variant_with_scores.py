# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from datetime import datetime
from typing_extensions import Literal, TypeAlias

from . import evaluation_dataset as _evaluation_dataset
from .._models import BaseModel

__all__ = [
    "ApplicationVariantWithScores",
    "CategoryScore",
    "CategoryScoreApplicationCategoryScoreAccuracy",
    "CategoryScoreApplicationCategoryScoreAccuracyMetricScore",
    "CategoryScoreApplicationCategoryScoreAccuracyMetricScoreApplicationMetricScoreAnswerCorrectness",
    "CategoryScoreApplicationCategoryScoreAccuracyMetricScoreApplicationMetricScoreAnswerRelevance",
    "CategoryScoreApplicationCategoryScoreRetrieval",
    "CategoryScoreApplicationCategoryScoreRetrievalMetricScore",
    "CategoryScoreApplicationCategoryScoreRetrievalMetricScoreApplicationMetricScoreFaithfulness",
    "CategoryScoreApplicationCategoryScoreRetrievalMetricScoreApplicationMetricScoreContextRecall",
    "CategoryScoreApplicationCategoryScoreQuality",
    "CategoryScoreApplicationCategoryScoreQualityMetricScore",
    "CategoryScoreApplicationCategoryScoreQualityMetricScoreApplicationMetricScoreCoherence",
    "CategoryScoreApplicationCategoryScoreQualityMetricScoreApplicationMetricScoreGrammar",
    "CategoryScoreApplicationCategoryScoreTrustAndSafety",
    "CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScore",
    "CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafety",
    "CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafetySubMetricScore",
    "CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafetySubMetricScoreApplicationMetricScoreLiteralApplicationScoreCategoryEnumTrustAndSafetyTrustAndSafetyLiteralSafetySubMetricTypeEnumBiasAndStereotypingSafetyBiasAndStereotyping",
    "CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafetySubMetricScoreApplicationMetricScoreLiteralApplicationScoreCategoryEnumTrustAndSafetyTrustAndSafetyLiteralSafetySubMetricTypeEnumOpinionsDisputedTopicsSafetyOpinionsDisputedTopics",
    "CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafetySubMetricScoreApplicationMetricScoreLiteralApplicationScoreCategoryEnumTrustAndSafetyTrustAndSafetyLiteralSafetySubMetricTypeEnumUnethicalHarmfulActivitiesSafetyUnethicalHarmfulActivities",
    "CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafetySubMetricScoreApplicationMetricScoreLiteralApplicationScoreCategoryEnumTrustAndSafetyTrustAndSafetyLiteralSafetySubMetricTypeEnumCopyrightViolationsSafetyCopyrightViolations",
    "CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafetySubMetricScoreApplicationMetricScoreLiteralApplicationScoreCategoryEnumTrustAndSafetyTrustAndSafetyLiteralSafetySubMetricTypeEnumHarmfulContentSafetyHarmfulContent",
    "CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafetySubMetricScoreApplicationMetricScoreLiteralApplicationScoreCategoryEnumTrustAndSafetyTrustAndSafetyLiteralSafetySubMetricTypeEnumPrivacyViolationsSafetyPrivacyViolations",
    "CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreModeration",
    "EvaluationDataset",
]


class CategoryScoreApplicationCategoryScoreAccuracyMetricScoreApplicationMetricScoreAnswerCorrectness(BaseModel):
    category: Literal["accuracy"]

    metric_type: Literal["answer-correctness"]

    score: Optional[float] = None


class CategoryScoreApplicationCategoryScoreAccuracyMetricScoreApplicationMetricScoreAnswerRelevance(BaseModel):
    category: Literal["accuracy"]

    metric_type: Literal["answer-relevance"]

    score: Optional[float] = None


CategoryScoreApplicationCategoryScoreAccuracyMetricScore: TypeAlias = Union[
    CategoryScoreApplicationCategoryScoreAccuracyMetricScoreApplicationMetricScoreAnswerCorrectness,
    CategoryScoreApplicationCategoryScoreAccuracyMetricScoreApplicationMetricScoreAnswerRelevance,
]


class CategoryScoreApplicationCategoryScoreAccuracy(BaseModel):
    category: Literal["accuracy"]

    metric_scores: List[CategoryScoreApplicationCategoryScoreAccuracyMetricScore]

    score: Optional[float] = None


class CategoryScoreApplicationCategoryScoreRetrievalMetricScoreApplicationMetricScoreFaithfulness(BaseModel):
    category: Literal["retrieval"]

    metric_type: Literal["faithfulness"]

    score: Optional[float] = None


class CategoryScoreApplicationCategoryScoreRetrievalMetricScoreApplicationMetricScoreContextRecall(BaseModel):
    category: Literal["retrieval"]

    metric_type: Literal["context-recall"]

    score: Optional[float] = None


CategoryScoreApplicationCategoryScoreRetrievalMetricScore: TypeAlias = Union[
    CategoryScoreApplicationCategoryScoreRetrievalMetricScoreApplicationMetricScoreFaithfulness,
    CategoryScoreApplicationCategoryScoreRetrievalMetricScoreApplicationMetricScoreContextRecall,
]


class CategoryScoreApplicationCategoryScoreRetrieval(BaseModel):
    category: Literal["retrieval"]

    metric_scores: List[CategoryScoreApplicationCategoryScoreRetrievalMetricScore]

    score: Optional[float] = None


class CategoryScoreApplicationCategoryScoreQualityMetricScoreApplicationMetricScoreCoherence(BaseModel):
    category: Literal["quality"]

    metric_type: Literal["coherence"]

    score: Optional[float] = None


class CategoryScoreApplicationCategoryScoreQualityMetricScoreApplicationMetricScoreGrammar(BaseModel):
    category: Literal["quality"]

    metric_type: Literal["grammar"]

    score: Optional[float] = None


CategoryScoreApplicationCategoryScoreQualityMetricScore: TypeAlias = Union[
    CategoryScoreApplicationCategoryScoreQualityMetricScoreApplicationMetricScoreCoherence,
    CategoryScoreApplicationCategoryScoreQualityMetricScoreApplicationMetricScoreGrammar,
]


class CategoryScoreApplicationCategoryScoreQuality(BaseModel):
    category: Literal["quality"]

    metric_scores: List[CategoryScoreApplicationCategoryScoreQualityMetricScore]

    score: Optional[float] = None


class CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafetySubMetricScoreApplicationMetricScoreLiteralApplicationScoreCategoryEnumTrustAndSafetyTrustAndSafetyLiteralSafetySubMetricTypeEnumBiasAndStereotypingSafetyBiasAndStereotyping(
    BaseModel
):
    category: Literal["trust-and-safety"]

    metric_type: Literal["safety-bias-and-stereotyping"]

    score: Optional[float] = None


class CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafetySubMetricScoreApplicationMetricScoreLiteralApplicationScoreCategoryEnumTrustAndSafetyTrustAndSafetyLiteralSafetySubMetricTypeEnumOpinionsDisputedTopicsSafetyOpinionsDisputedTopics(
    BaseModel
):
    category: Literal["trust-and-safety"]

    metric_type: Literal["safety-opinions-disputed-topics"]

    score: Optional[float] = None


class CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafetySubMetricScoreApplicationMetricScoreLiteralApplicationScoreCategoryEnumTrustAndSafetyTrustAndSafetyLiteralSafetySubMetricTypeEnumUnethicalHarmfulActivitiesSafetyUnethicalHarmfulActivities(
    BaseModel
):
    category: Literal["trust-and-safety"]

    metric_type: Literal["safety-unethical-harmful-activities"]

    score: Optional[float] = None


class CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafetySubMetricScoreApplicationMetricScoreLiteralApplicationScoreCategoryEnumTrustAndSafetyTrustAndSafetyLiteralSafetySubMetricTypeEnumCopyrightViolationsSafetyCopyrightViolations(
    BaseModel
):
    category: Literal["trust-and-safety"]

    metric_type: Literal["safety-copyright-violations"]

    score: Optional[float] = None


class CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafetySubMetricScoreApplicationMetricScoreLiteralApplicationScoreCategoryEnumTrustAndSafetyTrustAndSafetyLiteralSafetySubMetricTypeEnumHarmfulContentSafetyHarmfulContent(
    BaseModel
):
    category: Literal["trust-and-safety"]

    metric_type: Literal["safety-harmful-content"]

    score: Optional[float] = None


class CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafetySubMetricScoreApplicationMetricScoreLiteralApplicationScoreCategoryEnumTrustAndSafetyTrustAndSafetyLiteralSafetySubMetricTypeEnumPrivacyViolationsSafetyPrivacyViolations(
    BaseModel
):
    category: Literal["trust-and-safety"]

    metric_type: Literal["safety-privacy-violations"]

    score: Optional[float] = None


CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafetySubMetricScore: TypeAlias = Union[
    CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafetySubMetricScoreApplicationMetricScoreLiteralApplicationScoreCategoryEnumTrustAndSafetyTrustAndSafetyLiteralSafetySubMetricTypeEnumBiasAndStereotypingSafetyBiasAndStereotyping,
    CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafetySubMetricScoreApplicationMetricScoreLiteralApplicationScoreCategoryEnumTrustAndSafetyTrustAndSafetyLiteralSafetySubMetricTypeEnumOpinionsDisputedTopicsSafetyOpinionsDisputedTopics,
    CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafetySubMetricScoreApplicationMetricScoreLiteralApplicationScoreCategoryEnumTrustAndSafetyTrustAndSafetyLiteralSafetySubMetricTypeEnumUnethicalHarmfulActivitiesSafetyUnethicalHarmfulActivities,
    CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafetySubMetricScoreApplicationMetricScoreLiteralApplicationScoreCategoryEnumTrustAndSafetyTrustAndSafetyLiteralSafetySubMetricTypeEnumCopyrightViolationsSafetyCopyrightViolations,
    CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafetySubMetricScoreApplicationMetricScoreLiteralApplicationScoreCategoryEnumTrustAndSafetyTrustAndSafetyLiteralSafetySubMetricTypeEnumHarmfulContentSafetyHarmfulContent,
    CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafetySubMetricScoreApplicationMetricScoreLiteralApplicationScoreCategoryEnumTrustAndSafetyTrustAndSafetyLiteralSafetySubMetricTypeEnumPrivacyViolationsSafetyPrivacyViolations,
]


class CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafety(BaseModel):
    category: Literal["trust-and-safety"]

    metric_type: Literal["safety"]

    sub_metric_scores: List[
        CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafetySubMetricScore
    ]

    score: Optional[float] = None


class CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreModeration(BaseModel):
    category: Literal["trust-and-safety"]

    metric_type: Literal["moderation"]

    score: Optional[float] = None


CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScore: TypeAlias = Union[
    CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreSafety,
    CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScoreApplicationMetricScoreModeration,
]


class CategoryScoreApplicationCategoryScoreTrustAndSafety(BaseModel):
    category: Literal["trust-and-safety"]

    metric_scores: List[CategoryScoreApplicationCategoryScoreTrustAndSafetyMetricScore]

    score: Optional[float] = None


CategoryScore: TypeAlias = Union[
    CategoryScoreApplicationCategoryScoreAccuracy,
    CategoryScoreApplicationCategoryScoreRetrieval,
    CategoryScoreApplicationCategoryScoreQuality,
    CategoryScoreApplicationCategoryScoreTrustAndSafety,
]


class EvaluationDataset(BaseModel):
    evaluation_dataset: _evaluation_dataset.EvaluationDataset

    evaluation_dataset_version_num: int

    generation_status: Literal["Pending", "Running", "Completed", "Failed", "Canceled"]

    scored_test_case_count: Optional[int] = None


class ApplicationVariantWithScores(BaseModel):
    id: str
    """The unique identifier of the entity."""

    account_id: str
    """The ID of the account that owns the given entity."""

    application_spec_id: str

    application_variant_id: str

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    updated_at: datetime
    """The date and time when the entity was last updated in ISO format."""

    category_scores: Optional[List[CategoryScore]] = None

    evaluation_datasets: Optional[List[EvaluationDataset]] = None

    score: Optional[float] = None
