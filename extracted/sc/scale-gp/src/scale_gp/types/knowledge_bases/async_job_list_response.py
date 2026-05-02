# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import TYPE_CHECKING, Dict, Optional
from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ..._models import BaseModel

__all__ = ["AsyncJobListResponse"]


class AsyncJobListResponse(BaseModel):
    id: str
    """The unique identifier of the entity."""

    account_id: str
    """The ID of the account that owns the given entity."""

    created_at: datetime
    """The date and time when the entity was created in ISO format."""

    job_type: Literal[
        "evaluation-auto-eval",
        "evaluation-test-cases-result-gen",
        "evaluation-metrics-gen",
        "evaluation-builder",
        "evaluation-dataset-generation",
        "knowledge_base_upload",
        "application-variant-report-generation",
        "application-interaction-evaluation",
        "deploy-inference-model",
        "update-inference-model",
        "evaluation-task-execution",
        "evaluation-task-runner",
        "parse-document",
    ]

    status: str

    updated_at: datetime
    """The date and time when the entity was last updated in ISO format."""

    created_by_identity_type: Optional[Literal["user", "service_account"]] = None
    """The type of identity that created the entity."""

    created_by_user_id: Optional[str] = None
    """The user who originally created the entity."""

    idempotency_key: Optional[str] = None

    job_metadata: Optional[Dict[str, object]] = None

    parent_job_id: Optional[str] = None

    progress: Optional[Dict[str, object]] = None

    status_reason: Optional[str] = None

    if TYPE_CHECKING:
        # Some versions of Pydantic <2.8.0 have a bug and don’t allow assigning a
        # value to this field, so for compatibility we avoid doing it at runtime.
        __pydantic_extra__: Dict[str, object] = FieldInfo(init=False)  # pyright: ignore[reportIncompatibleVariableOverride]

        # Stub to indicate that arbitrary properties are accepted.
        # To access properties that are not valid identifiers you can use `getattr`, e.g.
        # `getattr(obj, '$type')`
        def __getattr__(self, attr: str) -> object: ...
    else:
        __pydantic_extra__: Dict[str, object]
