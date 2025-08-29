import ast
from urllib.parse import unquote

from django import forms
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.forms import modelformset_factory
from django.forms.models import BaseModelFormSet
from psycopg.types.range import DateRange, TimestamptzRange


class NonrelatedInlineFormSet(BaseModelFormSet):
    """
    A basic implementation of an inline formset that doesn't make assumptions
    about any relationship between the form model and its parent instance.
    """

    def __init__(self, instance=None, save_as_new=None, **kwargs):
        self.instance = instance
        super().__init__(**kwargs)
        self.queryset = self.real_queryset

    @classmethod
    def get_default_prefix(cls):
        opts = cls.model._meta
        return opts.app_label + "-" + opts.model_name

    def save_new(self, form, commit=True):
        obj = super().save_new(form, commit=False)
        self.save_new_instance(self.instance, obj)
        if commit:
            obj.save()
        return obj


def nonrelated_inlineformset_factory(
    model, obj=None, queryset=None, formset=NonrelatedInlineFormSet, save_new_instance=None, **kwargs
):
    """
    FormSet factory that sets an explicit queryset on new classes.
    """
    FormSet = modelformset_factory(model, formset=formset, **kwargs)
    FormSet.real_queryset = queryset
    FormSet.save_new_instance = save_new_instance
    return FormSet


class ContentTypeMultiValueField(forms.fields.MultiValueField):
    def __init__(self, fields=None, *args, **kwargs):
        if fields is None:
            fields = (forms.IntegerField(), forms.IntegerField())
        super().__init__(fields, *args, **kwargs)

    def clean(self, value):
        value = self.to_python(value)
        res = []
        for val in value:
            res.append(super().clean(val))
        return res

    def to_python(self, value):
        if value:
            return ast.literal_eval(value)
        return []

    def compress(self, data_list):
        content_type_id, object_id = data_list
        try:
            content_type = ContentType.objects.get_for_id(content_type_id)
            return content_type.get_object_for_this_type(id=object_id)
        except ObjectDoesNotExist:
            return None


class TupleWidget(forms.TextInput):
    """
    Format a input of the form "param=val1,val2"
    """

    def value_from_datadict(self, data, files, name):
        if res := data.get(name, None):
            return unquote(res).split(",")


class DateRangeField(forms.MultiValueField):
    """
    A date range
    """

    default_error_messages = {
        "invalid": "Enter a valid date range.",
    }
    widget = TupleWidget
    form_date_field = forms.DateField
    python_field = DateRange

    def validate(self, value):
        if value.lower and value.upper and value.upper < value.lower:
            raise ValidationError(
                self.error_messages["invalid"],
                code="invalid_choice",
            )

    def __init__(self, **kwargs):
        fields = (
            self.form_date_field(required=True),
            self.form_date_field(required=True),
        )
        super().__init__(fields, **kwargs)

    def compress(self, values):
        try:
            lower, upper = values
            return self.python_field(lower=lower, upper=upper)
        except ValueError:
            return None


class DateTimeRangeField(DateRangeField):
    """
    A date time range
    """

    form_date_field = forms.DateTimeField
    python_field = TimestamptzRange
