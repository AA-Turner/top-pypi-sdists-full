# AUTO-GENERATED from ts/packages/llm-ui Zod schemas — do not edit manually
# Re-generate with: pnpm --filter @mistral/llm-ui generate:workflow-sdk

from typing import Any, Literal

from pydantic import BaseModel, model_serializer

__all__ = [
    "Alert",
    "Avatar",
    "Badge",
    "ButtonLink",
    "Card",
    "Chart",
    "Column",
    "Image",
    "Markdown",
    "PieChart",
    "Row",
    "Tooltip",
    "LLM_UI_VERSION",
    "UIComponent",
]

LLM_UI_VERSION = "1.7.0"


class UIComponent(BaseModel):
    """Base class for all LLM UI components.

    Serializes to {"name": "<ClassName>", "props": {<fields>}} wire format.
    """

    @model_serializer
    def _serialize(self) -> dict[str, Any]:
        props: dict[str, Any] = {}
        for field_name in type(self).model_fields:
            value = getattr(self, field_name)
            if value is None:
                continue
            if isinstance(value, UIComponent):
                props[field_name] = value._serialize()
            elif isinstance(value, list):
                props[field_name] = [item._serialize() if isinstance(item, UIComponent) else item for item in value]
            else:
                props[field_name] = value
        return {"name": self.__class__.__name__, "props": props}


class Alert(UIComponent):
    """Displays important messages with different severity levels (info, warning, error, success)"""

    title: str | None = None
    children: str | list[UIComponent] | None = None
    variant: Literal["info", "warning", "error", "success"] | None = None


class Avatar(UIComponent):
    """Displays a user avatar image"""

    src: str | None = None
    alt: str | None = None
    text: str | None = None
    size: Literal["sm", "md", "lg"] | None = None


class Badge(UIComponent):
    """A small label for status indicators or counts"""

    children: str | list[UIComponent] | None = None
    variant: Literal["default", "primary", "success", "warning", "error"] | None = None
    size: Literal["sm", "md", "lg"] | None = None


class ButtonLink(UIComponent):
    """A link styled as a button"""

    href: str
    children: str | list[UIComponent] | None = None
    variant: Literal["primary", "secondary", "soft", "ghost", "brand", "destructive"] | None = None
    size: Literal["sm", "md", "lg"] | None = None
    external: bool | None = None


class Card(UIComponent):
    """A container component for displaying content with optional title and description"""

    title: str | None = None
    description: str | None = None
    padding: Literal["sm", "md", "lg"] | None = None
    children: str | list[UIComponent] | None = None


class Chart(UIComponent):
    """Displays data visualizations (line or bar charts)"""

    variant: Literal["line", "bar"]
    data: list[dict[str, str | int | float]]
    xAxis: str
    yAxis: str | list[str]
    yMin: int | float | Literal["auto"] | Literal["dataMin"] | None = None
    yMax: int | float | Literal["auto"] | Literal["dataMax"] | None = None
    title: str | None = None


class Column(UIComponent):
    """A vertical layout container for stacking children"""

    alignment: Literal["start", "center", "end", "stretch"] | None = None
    distribution: Literal["start", "center", "end", "spaceBetween", "spaceAround", "spaceEvenly"] | None = None
    gap: Literal["sm", "md", "lg"] | None = None
    children: str | list[UIComponent] | None = None


class Image(UIComponent):
    """Displays an image with optional styling variants"""

    src: str
    alt: str | None = None
    size: Literal["sm", "md", "lg", "full"] | None = None


class Markdown(UIComponent):
    """Renders markdown-formatted text content"""

    content: str


class PieChart(UIComponent):
    """Displays data as a pie chart with labeled segments"""

    data: list[dict[str, Any]]
    title: str | None = None


class Row(UIComponent):
    """A horizontal layout container for arranging children side by side"""

    alignment: Literal["start", "center", "end", "stretch", "baseline"] | None = None
    distribution: Literal["start", "center", "end", "spaceBetween", "spaceAround", "spaceEvenly"] | None = None
    gap: Literal["sm", "md", "lg"] | None = None
    wrap: bool | None = None
    children: str | list[UIComponent] | None = None


class Tooltip(UIComponent):
    """Displays additional information on hover"""

    children: str | list[UIComponent] | None = None
    trigger: str


Alert.model_rebuild()
Badge.model_rebuild()
ButtonLink.model_rebuild()
Card.model_rebuild()
Column.model_rebuild()
Row.model_rebuild()
Tooltip.model_rebuild()
