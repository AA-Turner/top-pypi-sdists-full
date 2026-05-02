# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from datetime import datetime
from typing_extensions import Literal

from .._models import BaseModel
from .evaluation_datasets.evaluation_dataset_version import EvaluationDatasetVersion

__all__ = ["EvaluationDatasetRetrieveResponse"]


class EvaluationDatasetRetrieveResponse(BaseModel):
    id: str
    """The unique identifier of the entity."""

    account_id: str
    """The ID of the account that owns the given entity."""

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    created_by_identity_type: Literal["user", "service_account"]
    """The type of identity that created the entity."""

    created_by_user_id: str
    """The user who originally created the entity."""

    name: str
    """The name of the dataset"""

    schema_type: Literal["GENERATION", "FLEXIBLE"]
    """The schema type of the dataset."""

    updated_at: datetime
    """The date and time when the entity was last updated in ISO format."""

    archived_at: Optional[datetime] = None
    """The date and time when the entity was archived in ISO format."""

    evaluation_dataset_metadata: Optional[Dict[str, object]] = None
    """Metadata about the Evaluation Dataset that it is associated with"""

    evaluation_dataset_versions: Optional[List[EvaluationDatasetVersion]] = None

    knowledge_base_id: Optional[str] = None
    """ID of the knowledge base that the evaluation dataset is associated with."""

    out_of_date: Optional[bool] = None
    """
    Boolean to check whether or not the knowledge base has been uploaded to since
    publication of the dataset.
    """

    schema_sub_type: Optional[Literal["summarization", "translation"]] = None

    test_case_count: Optional[int] = None

    vendor: Optional[Literal["scale"]] = None
    """The vendor of the evaluation dataset (e.g.

    'Scale' for Scale off-the-shelf datasets). Null if the evaluation dataset is not
    from a vendor (e.g., is created by the customer).
    """
