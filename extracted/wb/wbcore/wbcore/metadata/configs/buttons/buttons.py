from dataclasses import dataclass, field
from typing import Iterable, Optional

from django.utils.translation import gettext as _
from django.utils.translation import gettext_lazy
from rest_framework.request import Request

from wbcore.enums import RequestType
from wbcore.metadata.configs.display.instance_display import Display
from wbcore.serializers import ListSerializer, RepresentationSerializer, Serializer
from wbcore.utils.urls import get_parse_endpoint, get_urlencode_endpoint

from .bases import ButtonConfig, ButtonTypeMixin, ButtonUrlMixin
from .enums import ButtonType


@dataclass
class DropDownButton(ButtonTypeMixin, ButtonConfig):
    button_type = ButtonType.DROPDOWN
    buttons: Iterable = field(default_factory=tuple)

    def __post_init__(self):
        if hasattr(super(), "__post_init__"):
            super().__post_init__()
        self.buttons = tuple(self.buttons)
        if not isinstance(self.buttons, tuple):
            raise TypeError(f"{type(self.buttons)} is not a tuple")

    def serialize(self, request, **kwargs):
        res = super().serialize(request, **kwargs)
        res["buttons"] = [
            btn.serialize(request, **kwargs)
            for btn in sorted(self.buttons, key=lambda e: (e.weight, e.label, e.title))
        ]
        return res

    def __hash__(self):
        return hash(self.title)


@dataclass
class WidgetButton(ButtonTypeMixin, ButtonUrlMixin, ButtonConfig):
    button_type = ButtonType.WIDGET
    new_mode: bool = False
    open_new_by_default: bool | None = None

    def serialize(self, request, **kwargs):
        if self.new_mode and self.endpoint:
            endpoint, params = get_parse_endpoint(self.endpoint)
            params["new_mode"] = "true"
            self.endpoint = get_urlencode_endpoint(endpoint, params)
        res = super().serialize(request, **kwargs)
        res["new_mode"] = self.new_mode

        # When open by default is not set but it new mode is True
        # then the default behaviour is to open the content in a new window
        if self.open_new_by_default is not None:
            res["open_new_by_default"] = self.open_new_by_default
        elif self.new_mode:
            res["open_new_by_default"] = True

        return res

    def __hash__(self):
        if self.key:
            return hash(self.key)
        else:
            return hash(self.endpoint)


@dataclass
class HyperlinkButton(ButtonTypeMixin, ButtonUrlMixin, ButtonConfig):
    button_type = ButtonType.HYPERLINK

    def __hash__(self):
        if self.key:
            return hash(self.key)
        else:
            return hash(self.endpoint)


@dataclass
class ActionButton(ButtonTypeMixin, ButtonUrlMixin, ButtonConfig):
    button_type = ButtonType.ACTION
    method: RequestType = RequestType.POST
    action_label: str = ""

    description_fields: str = _("<p>Are you sure you want to proceed?</p>")
    instance_display: Optional[Display] = None
    serializer: Optional[type[Serializer]] = None
    confirm_config: ButtonConfig = ButtonConfig(label=gettext_lazy("Confirm"), title=gettext_lazy("Confirm"))
    cancel_config: ButtonConfig = ButtonConfig(
        label=gettext_lazy("Cancel"),
        title=gettext_lazy("Cancel"),
    )

    identifiers: Iterable[str] = field(default_factory=list)

    def __hash__(self):
        if self.key:
            return hash(self.key)
        else:
            return hash(self.endpoint)

    def __post_init__(self):
        if hasattr(super(), "__post_init__"):
            super().__post_init__()

    def _get_fields(self, request: Request) -> dict:
        fields = dict()
        rs = RepresentationSerializer
        ls = ListSerializer
        if self.serializer and (field_items := self.serializer(context={"request": request}).fields.items()):
            for name, _field in filter(lambda f: not isinstance(f[1], (rs, ls)), field_items):
                field_name, representation = _field.get_representation(request, name)
                fields[name] = representation

            for name, _field in filter(lambda f: isinstance(f[1], (rs, ls)), field_items):
                field_name, representation = _field.get_representation(request, name)
                fields[representation["related_key"]].update(representation)
                del fields[representation["related_key"]]["related_key"]

        return fields

    def serialize(self, request, **kwargs):
        res = super().serialize(request, **kwargs)
        res["action_label"] = self.action_label
        res["method"] = self.method.value
        res["description_fields"] = self.description_fields
        res["confirm_config"] = self.confirm_config.serialize(request, **kwargs)
        res["cancel_config"] = self.cancel_config.serialize(request, **kwargs)
        res["identifiers"] = self.identifiers
        if self.instance_display:
            res["instance_display"] = self.instance_display.serialize()

        if self.serializer:
            res["fields"] = self._get_fields(request)
        return res
