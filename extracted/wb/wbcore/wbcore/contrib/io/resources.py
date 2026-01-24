import re
from contextlib import suppress
from inspect import isfunction

import tablib
from django.template import Context, Template
from django.utils.module_loading import import_string
from import_export import resources

from wbcore.serializers import ListSerializer
from wbcore.serializers.fields.related import ListSerializer as RelatedListSerializer


class ExportResourceMixin:
    DUMMY_FIELD_MAP = {}

    def get_export_dummy_data(self) -> list[str]:
        """
        Returns a list in the same order as the headers with the fixture data that correspond to the header
        """
        res = []
        for header in self.get_export_headers():
            if value := self.DUMMY_FIELD_MAP.get(header):
                if callable(value):
                    value = value()
                res.append(value)
            else:
                res.append("")
        return res

    def export(self, queryset=None, *args, **kwargs):
        """
        override the functionality from import-export in order to allow empty queryset, which correspond to template export
        """
        if queryset is None:
            headers = self.get_export_headers()
            data = self.get_export_dummy_data()
            return tablib.Dataset(data, headers=headers)
        return super().export(*args, queryset=queryset, **kwargs)


class FilterModelResource(ExportResourceMixin, resources.ModelResource):
    """
    This class inherit from modelResource and provides few functionality out of the box:
    - Allow to define a template export and a map of field to corresponding dummy data to fill in the template with
    - Can instantiate the resource with a list of keyword argument that will be injected as field value before instance saving
    - Filter the queryset with the specified keyword argument
    """

    def __init__(self, filter_kwargs=None, request=None, **kwargs):
        super().__init__(**kwargs)
        if not filter_kwargs:
            filter_kwargs = dict()
        self.filter_kwargs = filter_kwargs
        self.request = request

    def before_save_instance(self, instance, *args):
        """
        For all specified `filter_kwargs`, set the attribute as field
        """
        for k, v in self.filter_kwargs.items():
            if not getattr(self, k, None):
                setattr(instance, k, v)

    def get_queryset(self):
        """
        Filter the queryset with the given keyword arguments
        """
        return self._meta.model.objects.filter(**self.filter_kwargs)


class ViewResource(ExportResourceMixin, resources.Resource):
    DEFAULT_PAGINATION_LIMIT: int = 200

    def __init__(
        self,
        columns_map: dict[str, str] | None = None,
        serializer_class=None,
        request=None,
        serializer_class_path: str | None = None,
        **kwargs,
    ):
        serializer_class_method_args = kwargs.pop("serializer_class_method_args", list())
        super().__init__(**kwargs)
        # in that case, serializer_class is lazy loaded,
        if serializer_class_path:
            serializer_class = import_string(serializer_class_path)
            if isfunction(serializer_class):
                serializer_class = serializer_class(*serializer_class_method_args)
        if not serializer_class:
            raise ValueError("ViewResource needs a serializer_class")
        self.serializer_class = serializer_class
        if not columns_map:
            columns_map = dict()
        self.columns_map = columns_map
        self.request = request

    def iter_queryset(self, queryset):
        serializer = self.serializer_class(queryset, many=True)
        return super().iter_queryset(serializer.data)

    def get_export_fields(self, selected_fields=None):
        res = []
        # Get default fields from the list display
        if "id" not in self.columns_map:
            res.append(
                resources.Field(
                    attribute="id",
                    column_name="id",
                    readonly=True,
                )
            )
        if self.columns_map:
            for key, label in self.columns_map.items():
                res.append(
                    resources.Field(
                        attribute=key,
                        column_name=label,
                        readonly=True,
                    )
                )
        else:
            for field_name, field in self.serializer_class().fields.items():
                res.append(
                    resources.Field(
                        attribute=field_name,
                        column_name=field.label,
                        readonly=True,
                    )
                )
        return res

    def export_resource(self, obj, selected_fields=None, **kwargs):
        if not selected_fields:
            selected_fields = self.get_export_fields()

        def _parse_representation(representation, template):
            template = re.sub(r"({{\W*}})", " ", template)
            t = Template(template).render(Context(representation))
            return t

        validated_data = []
        obj = dict(obj)
        for field in selected_fields:
            value = None
            if field.attribute in obj:
                value = obj[field.attribute]
                # Try to get the representation of this field derivated from the serializer field label key
                with suppress(KeyError):
                    representation_field_name = f"_{field.attribute}"
                    representation_field = self.serializer_class._declared_fields[representation_field_name]
                    if isinstance(representation_field, ListSerializer) or isinstance(
                        representation_field, RelatedListSerializer
                    ):
                        label_key = getattr(representation_field.child, "label_key", None)
                    else:
                        label_key = getattr(representation_field, "label_key", None)
                    if representation_field := obj.get(representation_field_name):
                        if isinstance(representation_field, list):
                            value = [
                                _parse_representation(representation, label_key)
                                for representation in representation_field
                            ]
                        else:
                            value = _parse_representation(representation_field, label_key)
            validated_data.append(value)
        return validated_data

    @classmethod
    def get_columns_map(cls, view):
        columns_map = {"id": "id"}
        # Get default fields from the list display
        if list_display := view.display_config_class(view, view.request, instance=None).get_list_display():
            for key, label in list_display.flatten_fields:
                columns_map[key] = label
        return columns_map
