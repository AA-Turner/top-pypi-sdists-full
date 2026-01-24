from django.db.models import Model
from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError
from rest_framework.reverse import reverse

from wbcore import serializers as wb_serializers
from wbcore.contrib.content_type.serializers import ContentTypeRepresentationSerializer
from wbcore.contrib.icons import WBIcon
from wbcore.contrib.workflow.models import Workflow
from wbcore.contrib.workflow.sites import workflow_site
from wbcore.enums import RequestType
from wbcore.metadata.configs import buttons as bt


class WorkflowModelSerializer(wb_serializers.ModelSerializer):
    _model = ContentTypeRepresentationSerializer(source="model", allowed_types=workflow_site.model_content_types)
    graph = wb_serializers.ImageField(required=False, read_only=True, label=_("Graph"))

    @wb_serializers.register_resource()
    def steps_inline(self, instance: Workflow, request, user) -> dict[str, str]:
        if not self.context.get("request"):
            return {}
        return {
            "steps": reverse("wbcore:workflow:step-workflow-list", args=[instance.pk], request=self.context["request"])
        }

    @wb_serializers.register_resource()
    def transitions_inline(self, instance: Workflow, request, user) -> dict[str, str]:
        if not self.context.get("request"):
            return {}
        return {
            "transitions": reverse(
                "wbcore:workflow:transition-workflow-list", args=[instance.pk], request=self.context["request"]
            )
        }

    @wb_serializers.register_resource()
    def processes_inline(self, instance: Workflow, request, user) -> dict[str, str]:
        if not self.context.get("request"):
            return {}
        return {
            "processes": reverse(
                "wbcore:workflow:process-workflow-list", args=[instance.pk], request=self.context["request"]
            )
        }

    @wb_serializers.register_resource()
    def data_inline(self, instance: Workflow, request, user) -> dict[str, str]:
        if not self.context.get("request"):
            return {}
        return {
            "data": reverse("wbcore:workflow:data-workflow-list", args=[instance.pk], request=self.context["request"])
        }

    @wb_serializers.register_dynamic_button()
    def start_workflow_buttons(self, instance: Workflow, request, user):
        buttons = []
        for step in instance.get_start_steps_for_workflow():
            buttons.append(
                bt.ActionButton(
                    method=RequestType.PATCH,
                    identifiers=("workflow:process",),
                    endpoint=f"{reverse('wbcore:workflow:workflow-start', args=[instance.pk], request=request)}?step_id={step.pk}",
                    label=_("Start {}").format(step.workflow.name),
                    icon=WBIcon.START.icon,
                    description_fields=_("Are you sure you want to start workflow {}?").format(step.workflow.name),
                    title=_("Start {}").format(step.workflow.name),
                    action_label=_("Starting {}").format(step.workflow.name),
                )
            )
        return buttons

    def validate(self, data: dict) -> dict:
        if "status_field" in data:
            status_field: str | None = data["status_field"]
        else:
            status_field: str | None = self.instance.status_field if self.instance else None
        if "model" in data:
            model: Model | None = data["model"]
        else:
            model: Model | None = self.instance.model if self.instance else None
        preserve_instance: bool | None = data.get(
            "preserve_instance", self.instance.preserve_instance if self.instance else None
        )

        if preserve_instance and not bool(model):
            raise ValidationError({"preserve_instance": _("Can only preserve the instance when a model is attached.")})

        if model and status_field:
            if not (model_class := model.model_class()):
                raise ValidationError({"model": _("Model not found.")})
            if not hasattr(model_class, status_field):
                raise ValidationError({"status_field": _("This model does not implement the specified status field.")})
        return data

    class Meta:
        dependency_map = {
            "status_field": ["model"],
            "preserve_instance": ["model"],
        }
        model = Workflow
        fields = (
            "id",
            "name",
            "single_instance_execution",
            "model",
            "_model",
            "status_field",
            "_additional_resources",
            "_buttons",
            "preserve_instance",
            "graph",
        )


class WorkflowRepresentationSerializer(wb_serializers.RepresentationSerializer):
    _detail = wb_serializers.HyperlinkField(reverse_name="wbcore:workflow:workflow-detail")

    class Meta:
        model = Workflow
        fields = (
            "id",
            "name",
            "_detail",
        )
