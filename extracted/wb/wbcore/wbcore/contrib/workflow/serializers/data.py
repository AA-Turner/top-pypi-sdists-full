from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError

from wbcore import serializers as wb_serializers
from wbcore.contrib.workflow.models import Data, DataValue, ProcessStep, Workflow
from wbcore.contrib.workflow.serializers.workflow import (
    WorkflowRepresentationSerializer,
)


class DataModelSerializer(wb_serializers.ModelSerializer):
    workflow = wb_serializers.PrimaryKeyRelatedField(
        default=wb_serializers.DefaultFromGET("workflow"),
        queryset=Workflow.objects.all(),
        label=_("Workflow"),
    )
    _workflow = WorkflowRepresentationSerializer(source="workflow")

    def validate(self, data: dict) -> dict:
        label: str | None = data.get("label", self.instance.label if self.instance else None)
        workflow: Workflow | None = data.get("workflow", self.instance.workflow if self.instance else None)
        required: bool | None = data.get("required", self.instance.required if self.instance else None)
        data_type: Data.DataType | None = data.get("data_type", self.instance.data_type if self.instance else None)
        if "default" in data:
            default: str = data["default"]
        else:
            default: str | None = self.instance.default if self.instance else None

        if label and hasattr(ProcessStep, label):
            raise ValidationError({"label": _("A field with this name already exists in the process step model.")})

        duplicate_data_obj = Data.objects.filter(label=label, workflow=workflow)
        if self.instance:
            duplicate_data_obj = duplicate_data_obj.exclude(id=self.instance.id)
        if duplicate_data_obj.exists():
            raise ValidationError(
                {"label": _("A data object with this label was already created for the selected workflow.")}
            )

        if default:
            if required:
                raise ValidationError({"required": _("Cannot set both required and a default value.")})
            if data_type:
                try:
                    Data.cast_value_to_datatype(data_type, default)
                except ValueError as e:
                    if data_type == Data.DataType.DATE:
                        raise ValidationError(
                            {
                                "default": _(
                                    "Invalid default value for this data type. Please use a date formatted to 'day.month.year'."
                                )
                            }
                        ) from None
                    elif data_type == Data.DataType.DATETIME:
                        raise ValidationError(
                            {
                                "default": _(
                                    "Invalid default value for this data type. Please use a datetime formatted to 'day.month.year hour:minute:second' in the 24h format."
                                )
                            }
                        ) from None
                    raise ValidationError({"default": _("Invalid default value for this data type.")}) from e

        return data

    class Meta:
        model = Data
        fields = (
            "id",
            "workflow",
            "_workflow",
            "label",
            "help_text",
            "data_type",
            "required",
            "default",
        )


class DataRepresentationSerializer(wb_serializers.RepresentationSerializer):
    _detail = wb_serializers.HyperlinkField(reverse_name="wbcore:workflow:data-detail")

    class Meta:
        model = Data
        fields = (
            "id",
            "_detail",
        )


class DataValueModelSerializer(wb_serializers.ModelSerializer):
    _data = DataRepresentationSerializer(source="data")

    def validate(self, data: dict) -> dict:
        value: str | None = data.get("value", self.instance.value if self.instance else None)
        data_obj: Data | None = data.get("data", self.instance.data if self.instance else None)

        if data_obj and value:
            try:
                Data.cast_value_to_datatype(data_obj.data_type, value)
            except ValueError as e:
                if data_obj.data_type == Data.DataType.DATE:
                    raise ValidationError(
                        {
                            "value": _(
                                "Invalid value for this data type. Please use a date formatted to 'day.month.year'."
                            )
                        }
                    ) from None
                elif data_obj.data_type == Data.DataType.DATETIME:
                    raise ValidationError(
                        {
                            "value": _(
                                "Invalid value for this data type. Please use a datetime formatted to 'day.month.year hour:minute:second' in the 24h format."
                            )
                        }
                    ) from None
                raise ValidationError({"value": _("Invalid value for this data type.")}) from e

        return data

    class Meta:
        model = DataValue
        fields = (
            "id",
            "data",
            "_data",
            "value",
        )


class DataValueRepresentationSerializer(wb_serializers.RepresentationSerializer):
    class Meta:
        model = DataValue
        fields = ("id",)
