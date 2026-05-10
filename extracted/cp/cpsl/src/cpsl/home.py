from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from .constants import ACCESS_PUBLIC, AccessLevel
from .session import RequestContext

SuggestionTarget = Literal["prompt", "workflow", "page"]


def _target_name(value: Any) -> str:
    name = getattr(value, "name", value)
    if not isinstance(name, str) or not name:
        raise ValueError("Suggestion target must be a non-empty string or object with a .name")
    return name


@dataclass(frozen=True, slots=True)
class Suggestion:
    """A typed action shown on an app's Capsule home screen.

    Targets are mutually exclusive:
      - ``prompt=`` starts a normal chat with that text.
      - ``workflow=`` opens the workflow launcher. Pass either the workflow
        object returned by ``app.workflow(...)`` or its string name.
      - ``workflow=`` plus ``input=`` immediately starts the workflow with
        that input. ``payload=`` is kept as a wire-format alias.
      - ``page=`` navigates to a page.
    """

    label: str
    prompt: str | None = None
    workflow: Any | None = None
    page: str | None = None
    description: str | None = None
    icon: str | None = None
    image: str | None = None
    accent: str | None = None
    primary: bool = False
    input: dict[str, Any] | None = None
    payload: dict[str, Any] | None = None

    def __post_init__(self) -> None:
        targets = [self.prompt is not None, self.workflow is not None, self.page is not None]
        if sum(targets) != 1:
            raise ValueError("Suggestion must define exactly one of prompt=, workflow=, or page=")
        if self.input and self.payload:
            raise ValueError("Suggestion accepts input= or payload=, not both")
        if (self.input or self.payload) and self.workflow is None:
            raise ValueError("Suggestion input is only supported with workflow=")

    def to_dict(self) -> dict[str, Any]:
        if self.prompt is not None:
            target: SuggestionTarget = "prompt"
            value = _target_name(self.prompt)
        elif self.workflow is not None:
            target = "workflow"
            value = _target_name(self.workflow)
        else:
            target = "page"
            value = _target_name(self.page)

        d: dict[str, Any] = {
            "label": self.label,
            "target": target,
            "value": value,
        }
        if self.description:
            d["description"] = self.description
        if self.icon:
            d["icon"] = self.icon
        if self.image:
            d["image"] = self.image
        if self.accent:
            d["accent"] = self.accent
        if self.primary:
            d["primary"] = True
        payload = self.input or self.payload
        if payload:
            d["payload"] = dict(payload)
        return d


@dataclass(frozen=True, slots=True)
class HomeConfig:
    title: str | None = None
    subtitle: str | None = None
    suggestions: tuple[Suggestion, ...] = ()
    widget_tree: dict[str, Any] | None = None
    dynamic_suggestions: bool = False
    dynamic_suggestions_access: AccessLevel = ACCESS_PUBLIC
    dynamic_suggestions_ttl: int = 0
    access: AccessLevel = ACCESS_PUBLIC

    def to_dict(self) -> dict[str, Any]:
        d: dict[str, Any] = {
            "suggestions": [s.to_dict() for s in self.suggestions],
            "dynamic_suggestions": self.dynamic_suggestions,
            "access": self.access,
        }
        if self.title:
            d["title"] = self.title
        if self.subtitle:
            d["subtitle"] = self.subtitle
        if self.widget_tree:
            d["widget_tree"] = self.widget_tree
        if self.dynamic_suggestions:
            d["dynamic_suggestions_access"] = self.dynamic_suggestions_access
            if self.dynamic_suggestions_ttl > 0:
                d["dynamic_suggestions_ttl"] = self.dynamic_suggestions_ttl
        return d


class HomeContext(RequestContext):
    """Context passed to ``@app.home_suggestions()`` handlers."""

    __slots__ = ("db", "app")

    def __init__(
        self,
        *,
        user,
        integrations,
        authenticated: bool = False,
        request: Any = None,
        db: Any = None,
        app: Any = None,
    ) -> None:
        super().__init__(
            user=user,
            integrations=integrations,
            authenticated=authenticated,
            request=request,
        )
        self.db = db
        self.app = app


def serialize_suggestions(value: Any) -> list[dict[str, Any]]:
    if value is None:
        return []
    if isinstance(value, Suggestion):
        return [value.to_dict()]
    if isinstance(value, dict):
        return [dict(value)]
    if not isinstance(value, (list, tuple)):
        raise TypeError("home suggestions must return a Suggestion, dict, list, or tuple")

    out: list[dict[str, Any]] = []
    for item in value:
        if isinstance(item, Suggestion):
            out.append(item.to_dict())
        elif isinstance(item, dict):
            out.append(dict(item))
        else:
            raise TypeError(
                f"home suggestion must be Suggestion or dict, got {type(item).__name__}"
            )
    return out
