from django.core.exceptions import ValidationError
from django.db.models import DecimalField, Field, FloatField, PositiveIntegerField


class AbstractDynamicField(Field):
    dependencies = []

    def __init__(self, *args, dependencies: list | None = None, **kwargs):
        blank = kwargs.pop("blank", True)
        null = kwargs.pop("null", True)
        self.dependencies = dependencies if dependencies else []
        super().__init__(*args, blank=blank, null=null, **kwargs)


class DynamicDecimalField(DecimalField, AbstractDynamicField):
    description = "Use a custom callback to compute this field if None"


class DynamicFloatField(FloatField, AbstractDynamicField):
    description = "Use a custom callback to compute this field if None"


def validate_year(year: int | None):
    if year and not len(str(year)) == 4:
        raise ValidationError("Please provide a valid 4-digit year.")


class YearField(PositiveIntegerField):
    default_validators = [validate_year]
