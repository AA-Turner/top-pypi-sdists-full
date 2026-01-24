from datetime import date, datetime

from django.db import models
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers as rest_serializers

from wbcore import serializers
from wbcore.models import WBModel


class Data(WBModel):
    """A blueprint for what data can be attached to a workflow."""

    class DataType(models.TextChoices):
        CHAR = "Text", _("Text")
        INT = "Number", _("Number")
        DATE = "Date", _("Date")
        DATETIME = "Date Time", _("Date Time")
        BOOL = "Boolean", _("Boolean")

        @classmethod
        def get_serializer_field_mapping(cls) -> dict:
            serializer_fields = [
                serializers.CharField(),
                serializers.IntegerField(),
                serializers.DateField(),
                serializers.DateTimeField(),
                serializers.BooleanField(),
            ]
            return {
                data_type: serializer_field
                for data_type, serializer_field in zip(cls, serializer_fields, strict=False)
            }

        @classmethod
        def get_cast_mapping(cls) -> dict:
            cast_callables = [
                str,
                int,
                datetime.strptime,
                datetime.strptime,
                bool,
            ]
            return {data_type: cast_callable for data_type, cast_callable in zip(cls, cast_callables, strict=False)}

    workflow = models.ForeignKey(
        to="workflow.Workflow",
        on_delete=models.CASCADE,
        verbose_name=_("Workflow"),
        related_name="attached_data",
    )
    label = models.CharField(max_length=64, verbose_name=_("Label"))
    help_text = models.CharField(max_length=128, verbose_name=_("Help Text"), null=True, blank=True)
    data_type = models.CharField(
        max_length=64, choices=DataType.choices, verbose_name=_("Data Type"), default=DataType.CHAR
    )
    required = models.BooleanField(
        verbose_name=_("Required"),
    )
    default = models.CharField(
        max_length=128,
        verbose_name=_("Default"),
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return f"{self.label} ({self.workflow})"

    def get_serializer_field(self) -> rest_serializers.Field:
        """Constructs a serializer field from the instance

        Returns:
            rest_serializers.Field: A serializer field based on the instance

        Raises:
            ValueError: If casting the default value fails
        """

        field = self.DataType.get_serializer_field_mapping()[self.data_type]
        field.set_attr("label", self.label)
        field.set_attr("required", self.required)
        if self.default:
            casted_value = Data.cast_value_to_datatype(self.data_type, self.default)
            field.set_attr("default", casted_value)
        if self.help_text:
            field.set_attr("help_text", self.help_text)
        return field

    @classmethod
    def cast_value_to_datatype(cls, data_type: DataType, value: str) -> datetime | str | int | bool:
        """Casts a value string into a provided data type

        Args:
            data_type (DataType): Selected data type
            value (str): The value string

        Returns:
            datetime | str | int | bool: Value string casted into selected data type

        Raises:
            ValueError: If casting fails
        """

        cast_callable = cls.DataType.get_cast_mapping()[data_type]
        if data_type == cls.DataType.DATE:
            # NOTE: Different format? ISO-8601? Create global dateime format preference?
            casted_value: date = cast_callable.__call__(value, "%d.%m.%Y").date()
        elif data_type == cls.DataType.DATETIME:
            casted_value: datetime = cast_callable.__call__(value, "%d.%m.%Y %H:%M:%S")
        elif data_type == cls.DataType.BOOL:
            if value.lower() == "true":
                casted_value: bool = True
            elif value.lower() == "false":
                casted_value: bool = False
            else:
                raise ValueError(gettext("Casting to bool failed."))
        else:
            casted_value: str | int = cast_callable.__call__(value)
        return casted_value

    @classmethod
    def cast_value_from_target_object(
        cls, target_type_object: datetime | date | bool | str | int, input_str: str
    ) -> datetime | date | bool | str | int | None:
        """Casts an input string into the type of a provided object. Supported data types: datetime | date | bool | str | int

        Args:
            target_type_object (datetime | date | bool | str | int): The target type object
            input_str (str): An input string to be casted

        Raises:
            ValueError: When an unsupported type is provided or casting failed

        Returns:
            datetime | date | bool | str | int | None: The casted input string
        """

        casted_output = None

        if isinstance(target_type_object, datetime):
            data_type = cls.DataType.DATETIME
        elif isinstance(target_type_object, date):
            data_type = cls.DataType.DATE
        elif isinstance(target_type_object, bool):
            data_type = cls.DataType.BOOL
        elif isinstance(target_type_object, int):
            data_type = cls.DataType.INT
        elif isinstance(target_type_object, str):
            data_type = cls.DataType.CHAR
        else:
            raise ValueError(gettext("Unsupported target type!"))

        casted_output = cls.cast_value_to_datatype(data_type, input_str)

        return casted_output

    @classmethod
    def cast_datatype_to_string(cls, data_type: DataType, data_object: datetime | str | int | bool) -> str:
        """Casts an object of type datatype into a str. Reverse function of 'cast_value_to_datatype'

        Args:
            data_type (DataType): Selected data type
            data_object (datetime | str | int | bool): The object to be casted

        Returns:
            str: A string representation of the object

        Raises:
            ValueError: If casting fails
        """

        if data_type in [cls.DataType.DATE, cls.DataType.DATETIME]:
            if data_type == cls.DataType.DATE:
                # NOTE: Different format? ISO-8601? Create global dateime format preference?
                format_str = "%d.%m.%Y"
            else:
                format_str = "%d.%m.%Y %H:%M:%S"
            try:
                casted_object = data_object.strftime(format_str)
            except AttributeError as e:
                raise ValueError(gettext("Date(time) type selected but no date(time) object provided!")) from e

        elif data_type == cls.DataType.BOOL:
            if data_object is True:
                casted_object = "True"
            elif data_object is False:
                casted_object = "False"
            else:
                raise ValueError(gettext("Wrong boolean value!"))
        else:
            casted_object = str(data_object)
        return casted_object

    @classmethod
    def get_endpoint_basename(cls):
        return "wbcore:workflow:data"

    @classmethod
    def get_representation_value_key(cls):
        return "id"

    @classmethod
    def get_representation_endpoint(cls):
        return "wbcore:workflow:datarepresentation-list"

    @classmethod
    def get_representation_label_key(cls):
        return "{{label}}"

    class Meta:
        verbose_name = _("Data")
        verbose_name_plural = _("Data")
        constraints = [
            models.UniqueConstraint(fields=["label", "workflow"], name="unique_label_workflow"),
        ]


class DataValue(models.Model):
    """A model that holds the value for a data object"""

    value = models.CharField(max_length=64, verbose_name=_("Value"), blank=True, null=True)
    data = models.ForeignKey(to=Data, related_name="values", on_delete=models.CASCADE, verbose_name=_("Data"))
    process = models.ForeignKey(
        to="workflow.Process", related_name="data_values", on_delete=models.CASCADE, verbose_name=_("Process")
    )

    def __str__(self) -> str:
        return f"{self.data}: {self.value}"

    @classmethod
    def get_representation_value_key(cls):
        return "id"

    @classmethod
    def get_representation_label_key(cls):
        return "{{value}}"

    class Meta:
        verbose_name = _("Data Value")
        verbose_name_plural = _("Data Values")
