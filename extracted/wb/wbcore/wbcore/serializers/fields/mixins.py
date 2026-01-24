import logging
from contextlib import suppress
from typing import Any, ClassVar, Type

from django.db.models.fields import NOT_PROVIDED
from rest_framework.fields import empty
from rest_framework.serializers import Field

logger = logging.getLogger(__name__)


def decorator(position: str, value: str, decorator_type: str = "icon") -> dict:
    if position not in ("left", "right"):
        raise ValueError("Decorator Position can only be right or left")
    if decorator_type not in ("icon", "text"):
        raise ValueError("Decorator Type can only be icon or text")
    return {"position": position, "value": value, "type": decorator_type}


class WBCoreSerializerFieldMixin:
    """
    A mixin that takes care of adding all the necessary magic to each implementation
    of the serializer fields
    """

    def __init__(
        self,
        *args,
        decorators=None,
        depends_on=None,
        math=None,
        extra=None,
        read_only=False,
        copyable=None,
        related_key=None,
        on_unsatisfied_deps="read_only",
        clear_dependent_fields=True,
        **kwargs,
    ):
        if not decorators:
            decorators = list()
        if not depends_on:
            depends_on = list()
        self.extra = extra
        self.decorators = decorators
        self.depends_on = depends_on
        self.math = math
        self.copyable = copyable
        # To satisfy DRF assertion, we detect if the readonly given is a callable and in that case, we consider the default read only attribute to be true
        self._callable_read_only = None
        if callable(read_only):
            self._callable_read_only = read_only
            read_only = True
        self.related_key = related_key
        self.on_unsatisfied_deps = on_unsatisfied_deps
        self.clear_dependent_fields = clear_dependent_fields
        super().__init__(*args, read_only=read_only, **kwargs)

    def _evaluate_read_only(self, field_name, parent):
        if self._callable_read_only:
            # if view is present, we use it as parameter to the callable, otherwise we assume read_only is True
            if view := self.view:
                self.read_only = self._callable_read_only(view)
            else:
                self.read_only = True

        if meta := getattr(parent, "Meta", None):
            read_only_fields = getattr(meta, "read_only_fields", [])
            # By default, DRF do not apply extra_kwargs to declared field, this leds to confusion in our codebase so we take the conscious decision to make read_only_fields take presence over declared field attribute
            if field_name in read_only_fields:
                self.read_only = True

    def bind(self, field_name, parent):
        super().bind(field_name, parent)
        # After binding to the parent happens, we evaluate the callable readonly if given
        self._evaluate_read_only(field_name, parent)

    def get_related_key(self) -> str:
        return self.related_key or self.source

    @property
    def view(self):
        # Helper property to return the stored instantiated view in the context
        return self.context.get(
            "view",
            getattr(self.context.get("request"), "parser_context", {}).get("view"),
        )

    def set_attr(self, attr, value):
        setattr(self, attr, value)
        self._kwargs[attr] = value

    def append_depend_on(self, depend_on):
        existing_fields = [elem["field"] for elem in self.depends_on]
        if depend_on["field"] not in existing_fields:
            self.depends_on.append(depend_on)
            self._kwargs["depends_on"] = self.depends_on

    def get_representation(self, request, field_name) -> tuple[str, dict]:
        if meta := getattr(self.parent, "Meta", None):
            if field_name in getattr(meta, "required_fields", []):
                self.required = True

        representation = {
            "key": field_name,
            "label": getattr(self, "label", None),
            "type": getattr(self, "field_type", "undefined"),
            "required": getattr(self, "required", True),
            "read_only": getattr(self, "read_only", False),
        }

        default = getattr(self, "default", None)
        if default is None or default == empty or default == NOT_PROVIDED:
            with suppress(Exception):  # TODO Add some explicit exception handling
                default = self.parent.Meta.model._meta._forward_fields_map[field_name].default

        if default is not None and default != empty and default != NOT_PROVIDED:
            if callable(default):
                if getattr(default, "requires_context", False):
                    default = default(self)
                else:
                    default = default()
            if default is not None:
                representation["default"] = self.to_representation(default)

        representation["decorators"] = getattr(self, "decorators", [])
        representation["depends_on"] = getattr(self, "depends_on", [])

        for _attr in ["help_text", "extra"]:
            attr = getattr(self, _attr, None)
            if attr:
                representation[_attr] = attr

        if self.math:
            representation["math"] = self.math
        if self.copyable:
            representation["copyable"] = self.copyable
        if self.on_unsatisfied_deps != "read_only":
            representation["on_unsatisfied_deps"] = self.on_unsatisfied_deps
        if self.clear_dependent_fields is not True:
            representation["clear_dependent_fields"] = self.clear_dependent_fields
        return field_name, representation

    def validate_empty_values(self, data):
        if isinstance(data, str) and data == "null":
            data = None
        return super().validate_empty_values(data)


class RangeMixin(WBCoreSerializerFieldMixin, Field):
    """
    This mixin represents a range in the form of:
    (value1,value2)

    When using this mixin, you must supply the internal_field (usually the postgres wrapper) that converts the range tuple to some datastructure.
    """

    default_error_messages = {
        "lower_gt_upper": "The upper bound must be greater than the lower bound.",
    }
    internal_field: ClassVar[Type]

    def _transform_range(self, lower, upper, inward: bool | None = None):
        return lower, upper

    def to_internal_value(self, data) -> Any:
        # If formdata is used, we need to separate the string into the range
        if isinstance(data, str) and "," in data:
            data = data.split(",")
        lower = upper = None
        if isinstance(data, list):
            if len(data) > 0 and data[0]:
                lower = super().to_internal_value(data[0])
            if len(data) > 1 and data[1]:
                upper = super().to_internal_value(data[1])
        lower, upper = self._transform_range(lower, upper, inward=True)
        if lower and upper and lower >= upper:
            self.fail("lower_gt_upper")
        return self.internal_field(lower, upper)

    def to_representation(self, instance):
        if hasattr(instance, "lower"):
            lower = instance.lower
        else:
            lower = instance[0]

        if hasattr(instance, "upper"):
            upper = instance.upper
        else:
            upper = instance[1]
        lower, upper = self._transform_range(lower, upper, inward=False)
        with suppress(Exception):
            lower = super().to_representation(lower)
        with suppress(Exception):
            upper = super().to_representation(upper)
        return lower, upper
