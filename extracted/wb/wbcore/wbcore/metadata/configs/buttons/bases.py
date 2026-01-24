from dataclasses import dataclass
from typing import Optional

from wbcore.metadata.utils import prefix_key

from .enums import ButtonDefaultColor


@dataclass
class ButtonConfig:
    label: Optional[str] = None
    icon: Optional[str] = None
    title: Optional[str] = None
    color: ButtonDefaultColor | str = ButtonDefaultColor.PRIMARY
    weight: int = 100
    disabled: bool = False
    always_render: bool = False
    placeholder: str | None = None

    def __hash__(self):
        return hash(self.title)

    def __post_init__(self):
        if post_init := getattr(super(), "__post_init__", None):
            post_init()
        if not self.label and not self.icon:
            raise ValueError("No label or icon specified")

    def __iter__(self):
        if iter := getattr(super(), "__iter__", None):
            yield from iter()

        for key in ["label", "icon", "title"]:
            value = getattr(self, key, None)
            if value:
                yield key, value
        color = getattr(self.color, "value", self.color)
        yield "color", color
        yield "disabled", self.disabled  # set to True if you want to set the css "disabled" property to that button
        yield "always_render", self.always_render  # set to True the button always needs to be rendered (even if empty)
        yield "placeholder", self.placeholder  # set to a valid string if a placeholder is needed onhover

    def serialize(self, request, key_prefix: str = None):
        res = dict(self)
        if key_prefix and "key" in res:
            res["key"] = prefix_key(res["key"], key_prefix)
        return res


@dataclass
class ButtonTypeMixin:
    def __post_init__(self):
        if post_init := getattr(super(), "__post_init__", None):
            post_init()
        if not hasattr(self, "button_type"):
            raise TypeError("button_type cannot be None.")

    def __iter__(self):
        if iter := getattr(super(), "__iter__", None):
            yield from iter()

        if button_type := getattr(self, "button_type", None):
            yield "type", button_type.value


@dataclass
class ButtonUrlMixin:
    key: Optional[str] = None
    endpoint: Optional[str] = None

    def __hash__(self):
        if self.key:
            return hash(self.key)
        else:
            return hash(self.endpoint)

    def __post_init__(self):
        if post_init := getattr(super(), "__post_init__", None):
            post_init()
        if bool(self.key) == bool(self.endpoint):
            raise ValueError("Either key or endpoint has to be defined. (Not both)")

    def __iter__(self):
        if iter := getattr(super(), "__iter__", None):
            yield from iter()
        if self.key:
            yield "key", self.key
        if self.endpoint:
            yield "endpoint", self.endpoint
