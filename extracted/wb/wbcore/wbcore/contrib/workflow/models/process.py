import uuid

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models
from django.utils.translation import gettext
from django.utils.translation import gettext_lazy as _

from wbcore.contrib.authentication.models import User
from wbcore.contrib.color.enums import WBColor
from wbcore.models import WBModel


class Process(WBModel):
    """Starting a workflow creates a process"""

    class ProcessState(models.TextChoices):
        ACTIVE = "Active", _("Active")
        FINISHED = "Finished", _("Finished")
        FAILED = "Failed", _("Failed")

        @classmethod
        def get_color_map(cls):
            colors = [
                WBColor.BLUE_LIGHT.value,
                WBColor.GREEN_LIGHT.value,
                WBColor.RED_LIGHT.value,
            ]
            return [choice for choice in zip(cls, colors, strict=False)]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_("UUID"))
    workflow = models.ForeignKey(
        to="workflow.Workflow", on_delete=models.PROTECT, verbose_name=_("Workflow"), editable=False
    )
    started = models.DateTimeField(auto_now_add=True, verbose_name=_("Started"))
    finished = models.DateTimeField(verbose_name=_("Finished"), null=True, blank=True, editable=False)
    instance_id = models.CharField(blank=True, null=True, editable=False, verbose_name=_("Instance"), max_length=128)
    content_type = models.ForeignKey(
        to=ContentType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Attached Model"),
        editable=False,
    )
    instance = GenericForeignKey("content_type", "instance_id")
    preserved_instance = models.JSONField(
        verbose_name=_("Preserved Instance"), null=True, blank=True, encoder=DjangoJSONEncoder
    )
    state = models.CharField(
        max_length=64,
        choices=ProcessState.choices,
        verbose_name=_("State"),
        help_text=_("The current state of this process. Can be one of: 'Active', 'Finished' or 'Failed'"),
        editable=False,
        default=ProcessState.ACTIVE,
    )

    def set_failed(self):
        """Sets the entire process and all remaining active process steps to failed"""
        from wbcore.contrib.workflow.models.step import Step, UserStep

        # Set all active process steps to failed
        for active_process_step in self.process_steps.filter(
            state__in=[ProcessStep.StepState.ACTIVE, ProcessStep.StepState.WAITING]
        ):
            # We cannot use "set_failed" or we run into infinite loops
            active_process_step.state = ProcessStep.StepState.FAILED
            error_message = gettext("Entire process failed due to unreachable steps")
            active_process_step.error_message = error_message
            active_process_step.save()

            # Notify assignees if user step
            if active_process_step.step.step_type == Step.StepType.USERSTEP:
                step: UserStep = active_process_step.step.get_casted_step()
                if step.notify_user and (all_assignees := active_process_step.get_all_assignees()):
                    step.notify_assignees(all_assignees, active_process_step, error_message)

        # Set process to failed
        self.state = self.ProcessState.FAILED
        self.save()

    def __str__(self) -> str:
        return _("Process {} for workflow {}").format(str(self.id), self.workflow.name)

    @classmethod
    def get_endpoint_basename(cls):
        return "wbcore:workflow:process"

    @classmethod
    def get_representation_value_key(cls):
        return "id"

    @classmethod
    def get_representation_endpoint(cls):
        return "wbcore:workflow:processrepresentation-list"

    @classmethod
    def get_representation_label_key(cls):
        return "{{id}}"

    class Meta:
        verbose_name = _("Process")
        verbose_name_plural = _("Processes")


class ProcessStep(WBModel):
    """The running instance of a step created after a process was started"""

    class StepState(models.TextChoices):
        ACTIVE = "Active", _("Active")
        FINISHED = "Finished", _("Finished")
        WAITING = "Waiting", _("Waiting")
        FAILED = "Failed", _("Failed")
        CANCELED = "Canceled", _("Canceled")

        @classmethod
        def get_color_map(cls):
            colors = [
                WBColor.BLUE_LIGHT.value,
                WBColor.GREEN_LIGHT.value,
                WBColor.YELLOW_LIGHT.value,
                WBColor.RED_LIGHT.value,
                WBColor.GREY.value,
            ]
            return [choice for choice in zip(cls, colors, strict=False)]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, verbose_name=_("UUID"))
    process = models.ForeignKey(
        to=Process, on_delete=models.CASCADE, verbose_name=_("Process"), editable=False, related_name="process_steps"
    )
    step = models.ForeignKey(
        to="workflow.Step",
        on_delete=models.CASCADE,
        verbose_name=_("Step"),
        editable=False,
        related_name="process_steps",
    )
    started = models.DateTimeField(auto_now_add=True, verbose_name=_("Started"))
    finished = models.DateTimeField(verbose_name=_("Finished"), null=True, blank=True, editable=False)
    assignee = models.ForeignKey(
        to="authentication.User",
        verbose_name=_("Assignee"),
        on_delete=models.SET_NULL,
        related_name="assigned_process_steps",
        editable=False,
        null=True,
        blank=True,
    )
    group = models.ForeignKey(
        to="authentication.Group",
        verbose_name=_("Group"),
        on_delete=models.SET_NULL,
        related_name="assigned_process_steps",
        editable=False,
        null=True,
        blank=True,
    )
    permission = models.ForeignKey(
        to="authentication.Permission",
        verbose_name=_("Permission"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        editable=False,
        related_name="related_process_steps",
        help_text=_("The permission needed to be able to view this step being executed."),
    )
    state = models.CharField(
        max_length=64,
        choices=StepState.choices,
        verbose_name=_("State"),
        help_text=_(
            "The current state of this process step. Can be one of: 'Active', 'Finished', 'Waiting', 'Failed' or 'Canceled'"
        ),
        editable=False,
        default=StepState.ACTIVE,
    )
    status = models.CharField(
        max_length=64,
        verbose_name=_("Status"),
        help_text=_("The status that will be set in the attached model upon transitioning to this step"),
        null=True,
        blank=True,
        editable=False,
    )
    error_message = models.CharField(
        max_length=128,
        verbose_name=_("Error Message"),
        help_text=_("An error message will be displayed when this step fails"),
        null=True,
        blank=True,
        editable=False,
    )

    def get_instance(self):
        """Returns the attached instance that shall be checked by a condition

        Returns:
            The attached instance
        """

        if self.process.instance:
            return self.process.instance
        # elif self.process.data_values.exists():
        # TODO: How do we integrate data values into this logic?
        return None

    def get_all_assignees(self) -> list[User]:
        """Returns the selected assignee or every member of the selected group of this process step

        Returns:
            list[User] | None: A list of assigned users
        """

        if assignee := self.assignee:
            return [assignee]
        elif group := self.group:
            return list(group.user_set.all())
        return []

    def __str__(self) -> str:
        return _("Process step {} for step {}").format(str(self.id), self.step.name)

    @classmethod
    def get_endpoint_basename(cls):
        return "wbcore:workflow:processstep"

    @classmethod
    def get_representation_value_key(cls):
        return "id"

    @classmethod
    def get_representation_endpoint(cls):
        return "wbcore:workflow:processsteprepresentation-list"

    @classmethod
    def get_representation_label_key(cls):
        return "{{id}}"

    class Meta:
        verbose_name = _("Process Step")
        verbose_name_plural = _("Process Steps")
