from django.utils.translation import gettext as _
from rest_framework.reverse import reverse

from wbcore import serializers as wb_serializers
from wbcore.contrib.authentication.serializers import (
    GroupRepresentationSerializer,
    PermissionRepresentationSerializer,
    UserRepresentationSerializer,
)
from wbcore.contrib.content_type.serializers import (
    ContentTypeRepresentationSerializer,
    DynamicObjectIDRepresentationSerializer,
)
from wbcore.contrib.workflow.models import Process, ProcessStep, Step
from wbcore.contrib.workflow.serializers.step import StepRepresentationSerializer
from wbcore.contrib.workflow.serializers.workflow import (
    WorkflowRepresentationSerializer,
)
from wbcore.enums import RequestType
from wbcore.metadata.configs import buttons as bt


class ProcessModelSerializer(wb_serializers.ModelSerializer):
    _instance_id = DynamicObjectIDRepresentationSerializer(
        source="instance_id",
        optional_get_parameters={"content_type": "content_type"},
        depends_on=[{"field": "content_type", "options": {}}],
    )
    _workflow = WorkflowRepresentationSerializer(source="workflow")
    _content_type = ContentTypeRepresentationSerializer(source="content_type")

    @wb_serializers.register_resource()
    def process_steps_inline(self, instance: Process, request, user) -> dict[str, str]:
        if not self.context.get("request"):
            return {}
        return {
            "process_steps": reverse(
                "wbcore:workflow:processstep-process-list",
                args=[instance.pk],
                request=self.context["request"],
            )
        }

    class Meta:
        model = Process
        dependency_map = {
            "instance_id": ["content_type"],
        }
        fields = (
            "id",
            "started",
            "finished",
            "instance_id",
            "_instance_id",
            "workflow",
            "_workflow",
            "_content_type",
            "content_type",
            "_additional_resources",
            "preserved_instance",
            "state",
        )


class ProcessRepresentationSerializer(wb_serializers.RepresentationSerializer):
    _detail = wb_serializers.HyperlinkField(reverse_name="wbcore:workflow:process-detail")

    class Meta:
        model = Process
        fields = (
            "id",
            "_detail",
        )


class ProcessStepModelSerializer(wb_serializers.ModelSerializer):
    _process = ProcessRepresentationSerializer(source="process")
    _step = StepRepresentationSerializer(source="step")
    _assignee = UserRepresentationSerializer(source="assignee")
    _group = GroupRepresentationSerializer(source="group")
    _permission = PermissionRepresentationSerializer(source="permission")

    @wb_serializers.register_dynamic_button()
    def next_process_step_buttons(self, instance: ProcessStep, request, user):
        buttons = []
        if (
            instance.state == ProcessStep.StepState.ACTIVE
            and instance.step.step_type == Step.StepType.USERSTEP
            and (
                user.is_superuser
                or user == instance.assignee
                or (user in instance.group.user_set.all() and not instance.step.get_casted_step().assignee_method)
            )
        ):
            for transition in instance.step.get_all_valid_outgoing_transitions(instance):
                buttons.append(
                    bt.ActionButton(
                        method=RequestType.PATCH,
                        identifiers=("workflow:step",),
                        endpoint=f"{reverse('wbcore:workflow:processstep-next', args=[instance.pk], request=request)}?transition_id={transition.pk}",
                        label=transition.name,
                        icon=transition.icon,
                        description_fields=_("Are you sure you want to activate {}?").format(transition.name),
                        title=transition.name,
                        action_label=_("Activating {}").format(transition.name),
                    )
                )
        return buttons

    class Meta:
        model = ProcessStep
        fields = (
            "id",
            "started",
            "finished",
            "permission",
            "_permission",
            "process",
            "_process",
            "_step",
            "step",
            "assignee",
            "_assignee",
            "group",
            "_group",
            "state",
            "status",
            "error_message",
            "_additional_resources",
            "_buttons",
        )


class ProcessStepRepresentationSerializer(wb_serializers.RepresentationSerializer):
    _detail = wb_serializers.HyperlinkField(reverse_name="wbcore:workflow:processstep-detail")

    class Meta:
        model = ProcessStep
        fields = (
            "id",
            "_detail",
        )


class AssignedProcessStepSerializer(wb_serializers.ModelSerializer):
    workflow_name = wb_serializers.CharField(label=_("Workflow"))
    _step = StepRepresentationSerializer(source="step")
    _assignee = UserRepresentationSerializer(source="assignee")
    _group = GroupRepresentationSerializer(source="group")
    _permission = PermissionRepresentationSerializer(source="permission")
    instance_endpoint = wb_serializers.SerializerMethodField()
    attached_model = wb_serializers.CharField(label=_("Attached Model"))

    def get_instance_endpoint(self, obj: ProcessStep) -> str:
        """Returns instance endpoint for attached instance object if possible"""

        if not self.context.get("request"):
            return ""
        instance_object = obj.process.instance if obj.process.instance else obj
        return reverse(
            f"{instance_object.get_endpoint_basename()}-detail",
            args=[instance_object.pk],
            request=self.context["request"],
        )

    class Meta:
        model = ProcessStep
        fields = (
            "id",
            "started",
            "finished",
            "permission",
            "_permission",
            "_step",
            "step",
            "assignee",
            "_assignee",
            "group",
            "_group",
            "status",
            "instance_endpoint",
            "workflow_name",
            "attached_model",
        )
