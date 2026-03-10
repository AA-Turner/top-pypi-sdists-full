"""Structured payloads for human-in-the-loop world termination."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field


class AnnotationWorkspaceItem(BaseModel):
    """A workspace-backed artifact that should be reviewed by a human."""

    workspace: str = Field(description="Workspace name (for example: recordings, code, reports)")
    path: str = Field(description="Path within the workspace (relative preferred, absolute allowed)")
    kind: Literal["file", "directory", "json", "markdown", "text", "image", "other"] = "file"
    label: str | None = Field(default=None, description="Short display label")
    description: str | None = Field(default=None, description="Reviewer-facing explanation")
    open_url: str | None = Field(
        default=None,
        description="Optional direct UI URL to open this artifact",
    )
    metadata: dict[str, Any] = Field(default_factory=dict)


class HumanAnnotationRequest(BaseModel):
    """Structured request rendered by Chronos for human review."""

    title: str = Field(description="Primary title shown in annotation UI")
    summary: str | None = Field(default=None, description="Short one-paragraph summary")
    instructions: str = Field(
        default="Review the attached artifacts and provide annotation notes.",
        description="Concrete instructions for the reviewer",
    )
    items: list[AnnotationWorkspaceItem] = Field(default_factory=list)
    context: dict[str, Any] = Field(default_factory=dict)
    suggested_questions: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)


class RequiresHumanAnnotation(RuntimeError):
    """Raise from a world to terminate early and request human review."""

    def __init__(
        self,
        request: HumanAnnotationRequest | dict[str, Any],
        message: str | None = None,
    ) -> None:
        self.request = (
            request if isinstance(request, HumanAnnotationRequest) else HumanAnnotationRequest.model_validate(request)
        )
        detail = message or self.request.summary or self.request.title
        super().__init__(detail)

    def result_payload(self) -> dict[str, Any]:
        """Result payload embedded into Chronos session.result."""
        return {
            "requires_human_annotation": True,
            "annotation_request": self.request.model_dump(mode="python"),
        }
