from contextlib import suppress
from functools import partial

from django.contrib.postgres.fields import (
    ArrayField,
    DateRangeField,
    DateTimeRangeField,
    DecimalRangeField,
)
from django.core.exceptions import ImproperlyConfigured
from django.db import models
from django.db.utils import ProgrammingError
from django.urls import resolve
from django.utils.http import urlencode
from django.utils.text import capfirst
from django_fsm import FSMField, get_available_user_FIELD_transitions
from rest_framework import serializers
from rest_framework.relations import ManyRelatedField, RelatedField
from rest_framework.reverse import NoReverseMatch, reverse
from rest_framework.serializers import PKOnlyObject, SerializerMetaclass
from timezone_field import TimeZoneField

from wbcore.contrib.color.fields import ColorField
from wbcore.contrib.icons.models import IconField
from wbcore.contrib.icons.serializers import IconSelectField
from wbcore.metadata.configs.display.list_display import BaseTreeGroupLevelOption
from wbcore.models.fields import YearField
from wbcore.serializers import (
    fields,
    register_only_instance_resource,
    register_resource,
)
from wbcore.serializers.fields.mixins import WBCoreSerializerFieldMixin
from wbcore.serializers.fields.related import ListSerializer
from wbcore.serializers.fields.types import WBCoreType
from wbcore.serializers.mixins import UserProfileMixin

from rest_framework.relations import Hyperlink  # NOQA # isort:skip


def _serialized_primarykey(instance, value):
    return value.id


def validate_nested_representation(instance, value):
    if isinstance(value, list):
        return [getattr(v, "id", None) for v in value]
    return getattr(value, "id", None)


class WBCoreSerializerMetaClass(SerializerMetaclass):
    def __new__(cls, *args, **kwargs):  # noqa: C901
        _class = super().__new__(cls, *args, **kwargs)

        if _meta := getattr(_class, "Meta", None):
            model = _meta.model
            only_fsm_transition_on_instance = getattr(_meta, "only_fsm_transition_on_instance", False)
            with suppress(AttributeError):
                for field in filter(lambda f: isinstance(f, FSMField), model._meta.fields):
                    transitions = getattr(model, f"get_all_{field.name}_transitions")(model())
                    for transition in transitions:

                        def method(self, instance, request, user, field, transition, view=None):
                            # if self.context["view"].historical_mode:
                            #     return {}

                            transitions = get_available_user_FIELD_transitions(instance, user, field)
                            if transition.name in [t.name for t in transitions]:
                                url = resolve(request.path_info)
                                namespace = f"{url.namespace}:" if url.namespace else ""
                                base_url_name = url.url_name.split("-")[:-1]

                                # We need to pass the kwargs from the view through to the reverse call
                                # And additionally pass in the instance.id as the pk
                                # NOTE: What happens if the reverse parameter is not called pk?
                                # NOTE: Is that even possible?

                                # If the view is not in the context, we just create an empty keyword dict.
                                # FIXME: This should actually never happen
                                try:
                                    kwargs = self.context["view"].kwargs
                                except KeyError:
                                    kwargs = {}

                                kwargs.update({"pk": instance.id})
                                try:
                                    endpoint = reverse(
                                        f"{namespace}{'-'.join(base_url_name)}-{transition.name}",
                                        kwargs=kwargs,
                                        request=request,
                                    )
                                except NoReverseMatch:
                                    return {}

                                return {transition.name: endpoint}
                            return {}

                        if only_fsm_transition_on_instance:
                            wrapped_method = register_only_instance_resource()(
                                partial(method, field=field, transition=transition)
                            )
                            wrapped_method.__name__ = transition.name
                        else:
                            wrapped_method = register_resource()(partial(method, field=field, transition=transition))
                            wrapped_method.__name__ = transition.name

                        setattr(
                            _class,
                            transition.name,
                            wrapped_method,
                        )

            # Flatten field from declared nested serializer
            for parent_field_name, child_fields in getattr(_meta, "flatten_fields", dict()).items():
                nested_serializer_class = getattr(child_fields, "serializer_class", None)
                nested_serializer = None
                # If a nested serializer class is provided, we get the list of flatten fields from it (e.g. JSONTableField)
                if nested_serializer_class:
                    nested_serializer = nested_serializer_class(json_serializer=True)
                    if flatten_field_names := getattr(child_fields, "flatten_field_names", []):
                        child_fields = nested_serializer.extract_representation_fields(
                            parent_field_name, flatten_field_names
                        )
                for child_field_name, serializer_field in child_fields:
                    # For each nested field, we include them in the class declaration
                    nested_field_name = f"{parent_field_name}__{child_field_name}"
                    _class._declared_fields[nested_field_name] = serializer_field
                    if nested_field_name not in _meta.fields:
                        _meta.fields = (*_meta.fields, nested_field_name)

                    # If the nested field is a related field, we check if a serializer is provided to get the RepresentationModelSerializer to attach
                    if issubclass(serializer_field.__class__, ManyRelatedField) or issubclass(
                        serializer_field.__class__, RelatedField
                    ):
                        setattr(
                            _class,
                            f"validate_{nested_field_name}",
                            lambda instance, value: validate_nested_representation(instance, value),
                        )
                        if nested_serializer and (
                            representation_serializer_field := nested_serializer.fields.get(
                                f"_{child_field_name}", None
                            )
                        ):
                            representation_serializer_field.set_attr("source", nested_field_name)
                            related_nested_field_name = f"_{nested_field_name}"
                            _class._declared_fields[related_nested_field_name] = representation_serializer_field
                            if related_nested_field_name not in _meta.fields:
                                _meta.fields = (*_meta.fields, related_nested_field_name)

        return _class


class AdditionalMetadataMixin:
    def __init__(self, *args, **kwargs):
        self.json_serializer = kwargs.pop("json_serializer", False)
        super().__init__(*args, **kwargs)

    def validate(self, data):
        data = super().validate(data)
        if hasattr(self, "Meta"):
            for parent_field in getattr(self.Meta, "flatten_fields", {}).keys():
                primary_data = getattr(self.instance, parent_field, {})
                updated_data = data.get(parent_field, {})
                primary_data.update(updated_data)
                data[parent_field] = primary_data
        return data

    def set_attr(self, attr, value):
        setattr(self, attr, value)
        self._kwargs[attr] = value

    def build_standard_field(self, field_name, model_field):
        field_class, field_kwargs = super().build_standard_field(field_name, model_field)
        if isinstance(model_field, FSMField):
            field_class = self.serializer_fsm_field
        if model_field and not field_kwargs.get("label", None) and model_field.verbose_name:
            field_kwargs["label"] = capfirst(model_field.verbose_name)
        return field_class, field_kwargs

    def build_relational_field(self, field_name, relation_info):
        model_field, related_model, to_many, to_field, has_through_model, reverse = relation_info
        field_class, field_kwargs = super().build_relational_field(field_name, relation_info)
        if has_through_model:
            field_kwargs["queryset"] = related_model.objects.all()
            field_kwargs["read_only"] = False
        if (
            relation_info.model_field
            and not field_kwargs.get("label", None)
            and relation_info.model_field.verbose_name
        ):
            field_kwargs["label"] = capfirst(model_field.verbose_name)
        return field_class, field_kwargs

    def build_property_field(self, field_name, model_class):
        field_class = fields.ReadOnlyField
        field_kwargs = {}

        return field_class, field_kwargs

    @classmethod
    def get_decorators(cls):
        if hasattr(cls, "Meta"):
            yield from getattr(cls.Meta, "decorators", dict()).items()

    @classmethod
    def get_percent_fields(cls):
        if hasattr(cls, "Meta"):
            yield from getattr(cls.Meta, "percent_fields", list())

    @classmethod
    def get_dependency_map(cls):
        if hasattr(cls, "Meta"):
            yield from getattr(cls.Meta, "dependency_map", dict()).items()

    def get_fields(self):
        fields = super().get_fields()

        # This shouldn't impact performance much has get_fields is used behind a cached property

        # Get decorators specified in Meta and append the argument accordingly
        for key, value in self.get_decorators():
            if field := fields.get(key, None):
                field.set_attr("decorators", [value])

        # Get percent fields specified in Meta and append the argument accordingly
        for key in self.get_percent_fields():
            if field := fields.get(key, None):
                field.set_percent(True)

        # Get dependency map specified in Meta and append the argument accordingly
        for key, values in self.get_dependency_map():
            for value in values:
                if depends_on_field := fields.get(key, None):
                    depends_on_field.append_depend_on({"field": value, "options": {}})

        return fields

    def extract_representation_fields(self, parent_field_name, nested_field_names):
        """
        Use to extract fields that are define on the serializer as nested fields
        """
        for flatten_field_name in nested_field_names:
            with suppress(AttributeError, ImproperlyConfigured):
                nested_serializer_field = self.fields[flatten_field_name]
                if not hasattr(nested_serializer_field, "endpoint"):
                    # It's not representation serializer field
                    nested_serializer_field.set_attr("source", f"{parent_field_name}.{flatten_field_name}")
                    nested_serializer_field.set_attr("allow_null", True)
                    nested_serializer_field.set_attr("read_only", False)
                    yield flatten_field_name, nested_serializer_field


class Serializer(AdditionalMetadataMixin, UserProfileMixin, serializers.Serializer):
    _additional_resources = fields.AdditionalResourcesField()
    _buttons = fields.DynamicButtonField()


class ModelSerializer(
    AdditionalMetadataMixin,
    UserProfileMixin,
    serializers.ModelSerializer,
    metaclass=WBCoreSerializerMetaClass,
):
    serializer_field_mapping = {
        models.AutoField: fields.PrimaryKeyField,
        models.BigAutoField: fields.PrimaryKeyField,
        models.BooleanField: fields.BooleanField,
        models.CharField: fields.CharField,
        models.DateField: fields.DateField,
        models.DateTimeField: fields.DateTimeField,
        models.TimeField: fields.TimeField,
        models.DecimalField: fields.DecimalField,
        models.DurationField: fields.DurationField,
        models.FileField: fields.FileField,
        models.FloatField: fields.FloatField,
        models.ImageField: fields.ImageField,
        models.IntegerField: fields.IntegerField,
        models.PositiveIntegerField: fields.IntegerField,
        models.PositiveSmallIntegerField: fields.IntegerField,
        models.SmallIntegerField: fields.IntegerField,
        models.TextField: fields.TextField,
        models.URLField: fields.URLField,
        models.UUIDField: fields.CharField,
        models.GenericIPAddressField: fields.CharField,
        ArrayField: fields.ListField,
        DateTimeRangeField: fields.DateTimeRangeField,
        DateRangeField: fields.DateRangeField,
        models.JSONField: fields.JSONTableField,
        fields.StarRatingField: fields.StarRatingField,
        fields.EmojiRatingField: fields.EmojiRatingField,
        ColorField: fields.ColorPickerField,
        DecimalRangeField: fields.DecimalRangeField,
        IconField: IconSelectField,
        TimeZoneField: fields.TimeZoneField,
        YearField: fields.YearField,
    }
    serializer_related_field = fields.PrimaryKeyRelatedField
    serializer_choice_field = fields.ChoiceField
    serializer_multiple_choice_field = fields.MultipleChoiceField
    serializer_fsm_field = fields.FSMStatusField

    _additional_resources = fields.AdditionalResourcesField()
    _buttons = fields.DynamicButtonField()


class RepresentationSerializer(WBCoreSerializerFieldMixin, ModelSerializer):
    field_type = WBCoreType.SELECT.value

    def __init__(self, *args, tree_config: BaseTreeGroupLevelOption | None = None, **kwargs):
        self.ignore_filter = kwargs.pop("ignore_filter", getattr(self, "ignore_filter", None))
        self.filter_params = kwargs.pop("filter_params", getattr(self, "filter_params", None))
        self.endpoint = kwargs.pop(
            "endpoint",
            getattr(self, "endpoint", getattr(self.Meta.model, "get_representation_endpoint", None)),
        )
        if callable(self.endpoint):
            self.endpoint = self.endpoint()
        self.value_key = kwargs.pop(
            "value_key",
            getattr(self, "value_key", getattr(self.Meta.model, "get_representation_value_key", None)),
        )
        if callable(self.value_key):
            self.value_key = self.value_key()
        self.label_key = kwargs.pop(
            "label_key",
            getattr(self, "label_key", getattr(self.Meta.model, "get_representation_label_key", None)),
        )
        if callable(self.label_key):
            self.label_key = self.label_key()
        self.label_key = kwargs.pop("label_key", self.label_key)
        self.optional_get_parameters = kwargs.pop(
            "optional_get_parameters",
            getattr(self, "optional_get_parameters", None),
        )
        self.tree_config = tree_config
        self.select_first_choice = kwargs.pop("select_first_choice", getattr(self, "select_first_choice", None))
        super().__init__(*args, **kwargs)

    def to_representation(self, value):
        # In case we annotate the representation, we need to ensure that the value is an Pk object
        if isinstance(value, int):
            value = PKOnlyObject(value)
        with suppress(ProgrammingError):
            if isinstance(value, PKOnlyObject) and self.Meta.model:
                try:
                    value = self.Meta.model._default_manager.get(id=value.pk)
                except self.Meta.model.DoesNotExist:
                    value = None
        return super().to_representation(value)

    @classmethod
    def many_init(cls, *args, **kwargs):
        kwargs["child"] = cls(
            *args,
            # depends_on=kwargs.get("depends_on", None),
            **kwargs,
        )
        fields = [
            "filter_params",
            "endpoint",
            "value_key",
            "label_key",
            "optional_get_parameters",
            "extra",
            "decorators",
            "depends_on",
            "math",
            "ignore_filter",
        ]
        for field in fields:
            if field in kwargs:
                del kwargs[field]
        return ListSerializer(*args, **kwargs)

    def __new__(cls, *args, **kwargs):
        if "read_only" not in kwargs:
            kwargs["read_only"] = True
        return super().__new__(cls, *args, **kwargs)

    def _get_filter_params(self, request):
        if not self.ignore_filter:
            if self.filter_params is not None:
                if callable(self.filter_params):
                    return self.filter_params(request)
                else:
                    return self.filter_params
            elif (get_filter_parm := getattr(self, "get_filter_params", None)) and callable(get_filter_parm):
                return get_filter_parm(request)
        return {}

    def get_representation(self, request, field_name):
        _, super_representation = super().get_representation(request, field_name)
        url = reverse(self.endpoint, request=request)

        filter_params = self._get_filter_params(request)
        if isinstance(filter_params, dict):
            # Sanitize None values from the filter dictionary (otherwise urlencode will throw an error)
            filter_params = {k: v for k, v in filter_params.items() if v is not None}
            url = f"{url}?{urlencode(filter_params)}"

        representation = {
            "type": self.field_type,
            "depends_on": super_representation.get("depends_on"),
            "representation_key": field_name,
            "related_key": self.get_related_key(),
            "endpoint": {
                "url": url,
                "value_key": self.value_key,
                "label_key": self.label_key,
            },
        }

        if self.select_first_choice:
            representation["select_first_choice"] = True

        if self.help_text:
            representation["help_text"] = self.help_text

        if self.optional_get_parameters:
            representation["endpoint"]["optional_get_parameters"] = self.optional_get_parameters

        if self.tree_config:
            representation["tree_config"] = dict(self.tree_config)
        return self.get_related_key(), representation
