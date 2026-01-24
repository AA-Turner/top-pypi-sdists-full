from contextlib import suppress

from django.core.exceptions import FieldDoesNotExist
from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.relations import ManyRelatedField, PKOnlyObject
from rest_framework.request import Request

from .list import ListFieldMixin
from .mixins import WBCoreSerializerFieldMixin
from .types import WBCoreType


class WBCoreManyRelatedField(ListFieldMixin, WBCoreSerializerFieldMixin, ManyRelatedField):
    def __init__(self, *args, **kwargs):
        required = kwargs.get("required", True)
        if not required:
            kwargs["allow_null"] = True
        super().__init__(*args, **kwargs)

    def bind(self, field_name, parent):
        super().bind(field_name, parent)
        # The `many=True` parameter on the related field returns this class,
        # where `children_relation` is directly bound to it. However, the context
        # processor does not yet have access to the request, so the `view` property
        # is currently `None`. To handle this, we need to explicitly re-evaluate
        # the `read_only` property for the `children_relation` when the binding
        # occurs from the List serializer to this instance.
        self.child_relation.context["view"] = self.view
        self.child_relation._evaluate_read_only(field_name, parent)
        if not self.child_relation.read_only and hasattr(self.child_relation, "_queryset"):
            self.child_relation.queryset = self.child_relation._queryset

    def get_representation(self, request: Request, field_name: str) -> tuple[str, dict]:
        key, representation = self.child_relation.get_representation(request, field_name)
        representation["multiple"] = True
        if not representation.get("label", None) and self.label:
            representation["label"] = self.label
        return key, representation


class PrimaryKeyRelatedField(WBCoreSerializerFieldMixin, serializers.PrimaryKeyRelatedField):
    MANY_RELATION_KWARGS = (
        "read_only",
        "write_only",
        "required",
        "default",
        "initial",
        "source",
        "label",
        "help_text",
        "style",
        "error_messages",
        "allow_empty",
        "html_cutoff",
        "html_cutoff_text",
        "allow_null",
    )

    def __init__(self, *args, queryset=None, read_only=False, **kwargs):
        self.field_type = kwargs.pop("field_type", WBCoreType.PRIMARY_KEY.value)
        if callable(read_only) and queryset is not None:
            self._queryset = queryset  # we unset any given queryset to be compliant with the RelatedField assertion
            queryset = None
        super().__init__(*args, queryset=queryset, read_only=read_only, **kwargs)

    def __new__(cls, *args, **kwargs):
        kwargs["style"] = {"base_template": "input.html"}
        return super().__new__(cls, *args, **kwargs)

    def bind(self, field_name, parent):
        super().bind(field_name, parent)
        # In case we had to unset the queryset attribute because read_only was a callable, we reinstate it here.
        if not self.read_only and hasattr(self, "_queryset"):
            self.queryset = self._queryset

    @classmethod
    def many_init(cls, *args, **kwargs):
        list_kwargs = {"child_relation": cls(*args, **kwargs)}
        for key in kwargs:
            if key in cls.MANY_RELATION_KWARGS:
                list_kwargs[key] = kwargs[key]
        return WBCoreManyRelatedField(**list_kwargs)

    def run_validation(self, data=empty):
        if (data is empty) and (view := self.parent.context.get("view", None)):
            parent_model_id = view.kwargs.get(f"{self.field_name}_id")
            if parent_model_id:
                data = parent_model_id

        return super().run_validation(data)

    def get_representation(self, request: Request, field_name: str) -> tuple[str, dict]:
        key, representation = super().get_representation(request, field_name)
        if default := representation.get("default", None):
            if isinstance(default, list):
                representation["default"] = [getattr(d, "id", d) for d in default]
            elif id := getattr(default, "id", None):
                representation["default"] = id
        return key, representation

    def to_representation(self, value):
        # In case we annotate the representation, we need to ensure that the value is an object
        if isinstance(value, (list, tuple, set)):
            return [self.to_representation(d) for d in value]
        with suppress(Exception):  # TODO: investigate what exception are we expecting here
            if isinstance(value, str):
                try:
                    value = int(value)
                except ValueError:
                    value = None
            if isinstance(value, int):
                value = PKOnlyObject(value)
            return super().to_representation(value)
        return None

    def get_queryset(self):
        """
        Allow queryset to be callable
        """
        if callable(self.queryset):
            self.queryset = self.queryset()
        qs = super().get_queryset()

        # if limite_choices_to is defined on the model field, we use it to restrict the related queryset
        with suppress(AttributeError, FieldDoesNotExist):
            if limit_choices_to := getattr(
                self.parent.Meta.model._meta.get_field(self.field_name), "_limit_choices_to", None
            ):
                if isinstance(limit_choices_to, dict):
                    qs = qs.filter(**limit_choices_to)
                else:
                    qs = qs.filter(limit_choices_to)
        return qs


class ListSerializer(WBCoreSerializerFieldMixin, serializers.ListSerializer):
    """
    A Wrapper around the normal DRF ListSerializer which also return the child representation
    """

    def get_representation(self, request: Request, field_name: str) -> tuple[str, dict]:
        _, representation = self.child.get_representation(request, field_name)
        representation["multiple"] = True
        related_key = self.get_related_key()
        representation["related_key"] = related_key

        # TODO: improve and don't monkeypatch
        rv = related_key if "." not in related_key else related_key.replace(".", "__")
        return rv, representation
