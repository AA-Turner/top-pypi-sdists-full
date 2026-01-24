import re

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _
from rest_framework import serializers
from rest_framework.reverse import reverse

from .mixins import WBCoreSerializerFieldMixin
from .types import ReturnContentType, WBCoreType


class CharField(WBCoreSerializerFieldMixin, serializers.CharField):
    field_type = WBCoreType.TEXT.value

    def __init__(self, *args, **kwargs):
        self.secure = kwargs.pop("secure", False)
        self.placeholder = kwargs.pop("placeholder", None)
        super().__init__(*args, allow_null=kwargs.pop("allow_null", True), **kwargs)

    def get_representation(self, request, field_name) -> tuple[str, dict]:
        key, representation = super().get_representation(request, field_name)

        if self.placeholder:
            representation["placeholder"] = self.placeholder

        # Add secure attribute if required
        if self.secure:
            representation["secure"] = True

        return key, representation

    def validate_empty_values(self, data):
        if (self.allow_null or self.allow_blank) and data is None:
            data = ""
        return super().validate_empty_values(data)


class TelephoneField(CharField):
    field_type = WBCoreType.TELEPHONE.value


class StringRelatedField(WBCoreSerializerFieldMixin, serializers.StringRelatedField):
    field_type = WBCoreType.TEXT.value


class TextAreaField(CharField):
    field_type = WBCoreType.TEXTAREA.value


class CodeField(CharField):
    field_type = WBCoreType.TEXTAREA.value

    def to_internal_value(self, data):
        try:
            compile(data, "", "exec")
        except Exception as e:
            raise ValidationError(_("Compiling script failed with the exception: {}".format(e))) from e
        return super().to_internal_value(data)


class TextField(CharField):
    field_type = WBCoreType.TEXTEDITOR.value
    texteditor_content_type = ReturnContentType.HTML.value

    def __init__(self, *args, **kwargs):
        """The constructor method.
        This pops the 'plugin_configs' dict from the kwargs and calls the
        parents init method.

        Parameters
        ----------
        plugin_configs : dict, optional
            A dictionary that contains a dictionary for each plugin of the
            texteditor. The configuration for each plugin must be available
            under a unique key.
        """
        self.plugin_configs = kwargs.pop("plugin_configs", None)
        self.disclaimer_length = kwargs.pop("disclaimer_length", None)
        super().__init__(*args, **kwargs)

    def get_representation(self, request, field_name) -> tuple[str, dict]:
        key, representation = super().get_representation(request, field_name)
        representation["content_type"] = self.texteditor_content_type
        if not self.plugin_configs:
            representation["plugin_configs"] = {}
        else:
            representation["plugin_configs"] = self.plugin_configs(request)

        if self.disclaimer_length:
            representation["disclaimer_length"] = self.disclaimer_length

        return key, representation


class MarkdownTextField(TextField):
    field_type = WBCoreType.MARKDOWNEDITOR.value
    texteditor_content_type = ReturnContentType.MARKDOWN.value

    def __init__(self, metadata_field=None, *args, **kwargs):
        self.metadata_field = metadata_field
        super().__init__(*args, **kwargs)

    def get_representation(self, request, field_name) -> tuple[str, dict]:
        key, representation = super().get_representation(request, field_name)
        representation["image_upload"] = reverse("wbcore:markdown-asset-upload", request=request)
        representation["tags"] = reverse("wbcore:markdown-tags", request=request)
        if self.metadata_field:
            representation["metadata_field"] = self.metadata_field
        return key, representation


class ColorPickerField(CharField):
    field_type = WBCoreType.COLOR.value

    def __init__(self, *args, **kwargs):
        kwargs["copyable"] = True
        super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        if not re.search(r"^#(?:[0-9a-fA-F]{3}){1,2}$", data):
            raise ValidationError(_("Please provide a valid hexadecimal color."))
        return super().to_internal_value(data)


class URLField(CharField):
    field_type = WBCoreType.URL.value

    def __init__(self, open_internally: bool = False, *args, **kwargs):
        """
        Args:
            open_internally: If true, notify the frontend to open the url as an internal widget
        """
        self.open_internally = open_internally
        super().__init__(*args, **kwargs)

    def get_representation(self, request, field_name) -> tuple[str, dict]:
        key, representation = super().get_representation(request, field_name)
        representation["open_internally"] = (
            self.open_internally(self.view) if callable(self.open_internally) else self.open_internally
        )
        return key, representation
