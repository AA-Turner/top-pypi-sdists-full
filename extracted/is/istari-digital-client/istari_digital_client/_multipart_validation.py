"""Hand-maintained validation shared by both generated storage clients."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from pydantic import BaseModel, model_validator


def reject_legacy_part_keys(value: Any) -> Any:
    """Reject S3 wire keys rather than silently dropping a supplied ETag."""
    if isinstance(value, Mapping) and {"PartNumber", "ETag"}.intersection(value):
        raise ValueError(
            "Use canonical part_number and etag keys, not PartNumber or ETag"
        )
    return value


class AssertedUploadPartValidation(BaseModel):
    """Reject legacy keys while retaining canonical ETags without normalization."""

    @model_validator(mode="before")
    @classmethod
    def validate_part_input(cls, value: Any) -> Any:
        """Check the original dictionary before generated parsing can drop keys."""
        return reject_legacy_part_keys(value)


class FinalizeMultipartUploadRequestValidation(BaseModel):
    """Enforce the complete-upload part plan without restricting cancellation."""

    @model_validator(mode="before")
    @classmethod
    def validate_finalize_input(cls, value: Any) -> Any:
        """Reject legacy keys even when canonical keys are supplied alongside them."""
        if isinstance(value, Mapping):
            reject_legacy_part_keys(value)
            parts = value.get("completed_parts")
            if isinstance(parts, (list, tuple)):
                for part in parts:
                    reject_legacy_part_keys(part)
        return value

    @model_validator(mode="after")
    def validate_complete_part_plan(self) -> FinalizeMultipartUploadRequestValidation:
        """Require precisely the expected dense set of part numbers for complete."""
        if getattr(self, "action", None) != "complete":
            return self
        object_size = getattr(self, "object_size", None)
        part_size = getattr(self, "part_size", None)
        if object_size is None or object_size < 0:
            raise ValueError("complete requires object_size >= 0")
        if part_size is None or part_size <= 0:
            raise ValueError("complete requires part_size > 0")
        count = max(1, (object_size + part_size - 1) // part_size)
        if count > 10000:
            raise ValueError("complete requires at most 10000 parts")
        parts = getattr(self, "completed_parts", None)
        if not parts or len(parts) != count:
            raise ValueError(
                "completed_parts must contain exactly the expected part plan"
            )
        numbers = [part.part_number for part in parts]
        if set(numbers) != set(range(1, count + 1)):
            raise ValueError(
                "completed_parts must have unique dense part_number values from 1 to N"
            )
        return self
