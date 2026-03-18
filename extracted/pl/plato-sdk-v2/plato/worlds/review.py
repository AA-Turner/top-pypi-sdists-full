"""Review model schema system for Plato worlds.

Allows worlds to define typed review data schemas with render hints and
feedback specifications. These schemas are published alongside the world
config and consumed by the frontend for dynamic rendering.

Usage::

    from plato.worlds.review import RenderHint, FeedbackField, review_model

    @review_model(name="task_score", description="Per-task scoring")
    class TaskScore(ReviewData):
        score: Annotated[float, RenderHint(widget="score_bar")] = Field(ge=0, le=1)
        passed: Annotated[bool, RenderHint(widget="pass_fail_badge")] = False
        evidence: Annotated[str, RenderHint(widget="markdown")] = ""

        class Feedback(BaseModel):
            correct: Annotated[bool, FeedbackField(widget="boolean")] = True
            notes: Annotated[str, FeedbackField(widget="textarea")] = ""
"""

from __future__ import annotations

import typing
from dataclasses import dataclass
from dataclasses import field as dataclass_field
from typing import Any, Literal

from pydantic import BaseModel

# ---------------------------------------------------------------------------
# Base class for review data
# ---------------------------------------------------------------------------


class ReviewData(BaseModel):
    """Base class for all review model data.

    Subclasses decorated with ``@review_model`` automatically get a ``type``
    field set to the model's registered name. Calling ``.to_data()`` returns
    the serialized dict ready for ``VerifierFinding.data``.
    """

    type: str = ""

    def model_post_init(self, __context: Any) -> None:
        # Auto-fill type from the @review_model name if not explicitly set
        if not self.type:
            meta = getattr(self.__class__, "_review_model_meta", None)
            if meta is not None:
                object.__setattr__(self, "type", meta.name)

    def to_data(self) -> dict[str, Any]:
        """Serialize to a dict suitable for ``VerifierFinding.data``."""
        return self.model_dump()


# ---------------------------------------------------------------------------
# Render hint — Annotated metadata for display fields
# ---------------------------------------------------------------------------

RENDER_WIDGETS = Literal[
    "score_bar",
    "pass_fail_badge",
    "severity_badge",
    "code_snippet",
    "markdown",
    "json_tree",
    "link",
    "tag_list",
    "image",
    "diff",
    "table",
    "hidden",
]

FEEDBACK_WIDGETS = Literal[
    "text",
    "textarea",
    "select",
    "boolean",
    "rating",
]


@dataclass(frozen=True)
class RenderHint:
    """Annotation marker that tells the frontend how to render a field.

    Attach via ``Annotated``::

        score: Annotated[float, RenderHint(widget="score_bar")]
    """

    widget: str
    label: str | None = None
    options: dict[str, Any] = dataclass_field(default_factory=dict)


@dataclass(frozen=True)
class FeedbackField:
    """Annotation marker that declares a feedback input field.

    Attach via ``Annotated``::

        correct: Annotated[bool, FeedbackField(widget="boolean")]
    """

    widget: str
    label: str | None = None
    options: dict[str, Any] = dataclass_field(default_factory=dict)


# ---------------------------------------------------------------------------
# @review_model decorator
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ReviewModelMeta:
    """Metadata stored on classes decorated with ``@review_model``."""

    name: str
    description: str = ""


def review_model(name: str, description: str = ""):
    """Decorator that registers a Pydantic model as a review data schema.

    Automatically sets the ``type`` field default to ``name`` so instances
    are self-identifying when serialized.

    The decorated class must be a :class:`ReviewData` subclass. It may
    optionally contain a nested ``Feedback`` class (also a BaseModel) whose
    fields are annotated with :class:`FeedbackField`.
    """

    def decorator(cls: type) -> type:
        if not (isinstance(cls, type) and issubclass(cls, BaseModel)):
            raise TypeError(f"@review_model can only decorate BaseModel subclasses, got {cls}")

        # Store metadata — ReviewData.model_post_init reads this to set type
        cls._review_model_meta = ReviewModelMeta(name=name, description=description)  # type: ignore[attr-defined]
        return cls

    return decorator


def get_review_model_meta(cls: type) -> ReviewModelMeta | None:
    """Return the :class:`ReviewModelMeta` for a ``@review_model``-decorated class, or None."""
    return getattr(cls, "_review_model_meta", None)


# ---------------------------------------------------------------------------
# Schema extraction
# ---------------------------------------------------------------------------


def _extract_hint(field_info: Any, marker_type: type) -> dict[str, Any] | None:
    """Extract a RenderHint or FeedbackField from pydantic field metadata."""
    for meta in field_info.metadata:
        if isinstance(meta, marker_type):
            result: dict[str, Any] = {"widget": meta.widget}
            if meta.label:
                result["label"] = meta.label
            if meta.options:
                result["options"] = meta.options
            return result

    # Check Annotated args on the annotation itself
    annotation = field_info.annotation
    origin = typing.get_origin(annotation)
    if origin is typing.Annotated:
        for arg in typing.get_args(annotation)[1:]:
            if isinstance(arg, marker_type):
                result = {"widget": arg.widget}
                if arg.label:
                    result["label"] = arg.label
                if arg.options:
                    result["options"] = arg.options
                return result
    return None


def review_model_to_json_schema(cls: type) -> dict[str, Any]:
    """Generate a JSON Schema for a ``@review_model``-decorated class.

    Injects ``x-render-hint`` extensions from :class:`RenderHint` annotations
    and ``x-feedback-schema`` from a nested ``Feedback`` class.
    """
    meta = get_review_model_meta(cls)
    if meta is None:
        raise ValueError(f"{cls} is not decorated with @review_model")

    schema = cls.model_json_schema()  # type: ignore[union-attr]

    # Inject x-render-hint on each property
    properties = schema.get("properties", {})
    for field_name, field_info in cls.model_fields.items():  # type: ignore[union-attr]
        hint = _extract_hint(field_info, RenderHint)
        if hint and field_name in properties:
            properties[field_name]["x-render-hint"] = hint

    # Ensure the type discriminator property has a const value
    if "type" in properties:
        properties["type"] = {"const": meta.name, "default": meta.name}

    schema["properties"] = properties

    # Add description from decorator
    if meta.description:
        schema["description"] = meta.description

    # Extract feedback schema from nested Feedback class
    feedback_cls = getattr(cls, "Feedback", None)
    if feedback_cls is not None and isinstance(feedback_cls, type) and issubclass(feedback_cls, BaseModel):
        feedback_schema = feedback_cls.model_json_schema()
        fb_properties = feedback_schema.get("properties", {})
        for field_name, field_info in feedback_cls.model_fields.items():
            hint = _extract_hint(field_info, FeedbackField)
            if hint and field_name in fb_properties:
                fb_properties[field_name]["x-feedback"] = hint
        feedback_schema["properties"] = fb_properties
        schema["x-feedback-schema"] = feedback_schema

    return schema


def collect_review_schemas(world_cls: type) -> dict[str, Any]:
    """Collect review schemas from a world class's ``review_models`` attribute.

    Returns a dict keyed by review model name → JSON Schema with extensions.
    """
    review_models: list[type] = getattr(world_cls, "review_models", [])
    schemas: dict[str, Any] = {}
    for model_cls in review_models:
        meta = get_review_model_meta(model_cls)
        if meta is None:
            raise ValueError(f"{model_cls} in {world_cls}.review_models is not decorated with @review_model")
        schemas[meta.name] = review_model_to_json_schema(model_cls)
    return schemas
