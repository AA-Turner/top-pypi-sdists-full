"""The serialization helpers inherited by public response models."""

from __future__ import annotations

import inspect
import json
from datetime import datetime, timezone

from pydantic import ConfigDict, Field

from composio_client import BaseModel


class Example(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    created_at: datetime
    python_name: str = Field(alias="wireName")
    defaulted: str = "default"
    nullable: str | None = None


def test_serialization_helper_signatures_match_stainless() -> None:
    assert str(inspect.signature(BaseModel.to_dict)) == (
        "(self, *, mode: \"Literal['json', 'python']\" = 'python', "
        "use_api_names: 'bool' = True, exclude_unset: 'bool' = True, "
        "exclude_defaults: 'bool' = False, exclude_none: 'bool' = False, "
        "warnings: 'bool' = True) -> 'dict[str, object]'"
    )
    assert str(inspect.signature(BaseModel.to_json)) == (
        "(self, *, indent: 'int | None' = 2, use_api_names: 'bool' = True, "
        "exclude_unset: 'bool' = True, exclude_defaults: 'bool' = False, "
        "exclude_none: 'bool' = False, warnings: 'bool' = True) -> 'str'"
    )


def test_to_dict_preserves_stainless_defaults_and_options() -> None:
    created_at = datetime(2026, 8, 23, 10, 30, tzinfo=timezone.utc)
    value = Example(created_at=created_at, python_name="value", nullable=None, extra="kept")

    assert value.to_dict() == {
        "created_at": created_at,
        "wireName": "value",
        "nullable": None,
        "extra": "kept",
    }
    assert value.to_dict(
        mode="json",
        use_api_names=False,
        exclude_unset=False,
        exclude_none=True,
    ) == {
        "created_at": "2026-08-23T10:30:00Z",
        "python_name": "value",
        "defaulted": "default",
        "extra": "kept",
    }


def test_to_json_defaults_to_indented_api_names() -> None:
    value = Example(created_at=datetime(2026, 8, 23, tzinfo=timezone.utc), python_name="value")

    rendered = value.to_json()

    assert '\n  "wireName": "value"' in rendered
    assert json.loads(rendered) == {
        "created_at": "2026-08-23T00:00:00Z",
        "wireName": "value",
    }
    assert "\n" not in value.to_json(indent=None)
