import sys
from datetime import datetime
from uuid import UUID

from celery import shared_task
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.db.models import Q
from django.template import Context, Template, TemplateSyntaxError
from django.utils.translation import gettext, pgettext_lazy
from django.utils.translation import gettext_lazy as _
from rest_framework.reverse import reverse

from wbcore.contrib.authentication.models import Group, Permission, User
from wbcore.contrib.notifications.dispatch import send_notification
from wbcore.contrib.notifications.utils import base_domain, create_notification_type
from wbcore.contrib.workflow.models import Process, ProcessStep
from wbcore.contrib.workflow.models.transition import Transition
from wbcore.contrib.workflow.sites import workflow_site
from wbcore.contrib.workflow.utils import get_model_serializer_class_for_instance
from wbcore.models import WBModel
from wbcore.utils.html import convert_html2text
from wbcore.utils.string_loader import StringSourceLoader
from wbcore.workers import Queue


class Step(WBModel):
    """One step in the workflow"""

    class StepType(models.TextChoices):
        STARTSTEP = "StartStep", _("Start Step")
        USERSTEP = "UserStep", _("User Step")
        DECISIONSTEP = "DecisionStep", _("Decision Step")
        SPLITSTEP = "SplitStep", _("Split Step")
        JOINSTEP = "JoinStep", _("Join Step")
        EMAILSTEP = "EmailStep", _("Email Step")
        SCRIPTSTEP = "ScriptStep", _("Script Step")
        FINISHSTEP = "FinishStep", _("Finish Step")

    name = models.CharField(max_length=128, verbose_name=_("Name"))
    workflow = models.ForeignKey(
        to="workflow.Workflow",
        verbose_name=_("Workflow"),
        on_delete=models.CASCADE,
        related_name="associated_steps",
    )
    code = models.PositiveIntegerField(verbose_name=_("Code"))
    status = models.CharField(
        max_length=64,
        verbose_name=_("Status"),
        help_text=_(
            "The status that will be set in the attached instance's status field upon transitioning to this step. Only applicable if attached model is set."
        ),
        null=True,
        blank=True,
    )
    step_type = models.CharField(max_length=64, default="", choices=StepType.choices, verbose_name=_("Step Type"))
    permission = models.ForeignKey(
        to=Permission,
        verbose_name=_("Permission"),
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="related_steps",
        help_text=_("Define which permission is needed to be able to view this step being executed."),
    )

    outgoing_transitions: models.QuerySet[Transition]
    incoming_transitions: models.QuerySet[Transition]

    def get_outgoing_transitions(self) -> models.QuerySet[Transition]:
        return self.outgoing_transitions.all()

    def get_incoming_transitions(self) -> models.QuerySet[Transition]:
        return self.incoming_transitions.all()

    def get_previous_steps(self) -> list["Step"]:
        previous_steps = []
        for transition in self.get_incoming_transitions():
            previous_steps.append(transition.from_step)
        return previous_steps

    def get_all_valid_outgoing_transitions(self, process_step: ProcessStep) -> list[Transition]:
        transition_list = []
        for transition in self.get_outgoing_transitions():
            if transition.all_conditions_satisfied(process_step):
                transition_list.append(transition)
        return transition_list

    def get_assigned_group(self) -> None:
        return None

    def get_assigned_user(self) -> None:
        return None

    def get_casted_step(self) -> "Step":
        """Casts the step into its child representative"""

        return getattr(sys.modules[__name__], self.step_type).objects.get(pk=self.pk)

    def user_can_see_step(self, user: User) -> bool:
        """Returns true if the user or any of the user groups he is part of has the permission to see the process step being executed and choose the next step

        Args:
            user (User): The user instance

        Returns:
            bool: True if the user has the permission and False otherwise
        """

        return (
            (not self.permission)
            or user.is_superuser
            or self.permission in user.user_permissions.all()
            or user.groups.filter(permissions=self.permission).exists()
        )

    def set_finished(self, process_step: ProcessStep):
        process_step.state = ProcessStep.StepState.FINISHED
        process_step.save()
        self.finish(process_step)

    def set_failed(self, process_step: ProcessStep, error_message: str):
        process_step.state = ProcessStep.StepState.FAILED
        # We don't want to overwrite a previous error message
        if not process_step.error_message:
            process_step.error_message = error_message
        process_step.save()

        # Check if the process can still finish
        process_can_finish.delay(process_step.process.pk)

    def set_canceled(self, process_step: ProcessStep):
        process_step.state = ProcessStep.StepState.CANCELED
        process_step.save()
        self.finish(process_step)

    def execute_single_next_step(self, process_step: ProcessStep):
        """Finds the next step and executes it. Fails if more than one step or no step can be transitioned to.

        Args:
            process_step (ProcessStep): Current process step
        """

        if len(valid_transitions := self.get_all_valid_outgoing_transitions(process_step)) == 1:
            Step.start_next_step(process_step, valid_transitions[0])
        elif not valid_transitions:
            self.set_failed(
                process_step,
                gettext("No valid outgoing transitions found for this step!"),
            )
        else:
            self.set_failed(
                process_step,
                gettext("More than one possible outgoing transition found for this step!"),
            )

    def run(self, process_step: ProcessStep):
        self.set_finished(process_step)

    def finish(self, process_step: ProcessStep):
        if process_step.state in [
            ProcessStep.StepState.FINISHED,
            ProcessStep.StepState.CANCELED,
        ]:
            # Set finished field
            process_step.finished = datetime.now()
            process_step.save()

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        self.step_type = self.__class__.__name__
        super().save(*args, **kwargs)

    @classmethod
    def start_next_step(cls, process_step: ProcessStep, transition: Transition):
        """Starts the next step of the transition and finishes the previous one

        Args:
            process_step (ProcessStep): The current process step
            transition (Transition): The transition that should be executed
        """

        next_step: Step = transition.to_step.get_casted_step()
        previous_step: Step = transition.from_step.get_casted_step()
        previous_step.set_finished(process_step)
        activate_step.delay(next_step.pk, process_step.process.pk)

    @classmethod
    def get_endpoint_basename(cls):
        return "wbcore:workflow:step"

    @classmethod
    def get_representation_value_key(cls):
        return "id"

    @classmethod
    def get_representation_endpoint(cls):
        return "wbcore:workflow:steprepresentation-list"

    @classmethod
    def get_representation_label_key(cls):
        return "{{name}}"

    class Meta:
        verbose_name = _("Step")
        verbose_name_plural = _("Steps")
        constraints = [
            models.UniqueConstraint(fields=["name", "workflow"], name="unique_name_workflow"),
            models.UniqueConstraint(fields=["code", "workflow"], name="unique_code_workflow"),
        ]


class StartStep(Step):
    """The first step in a workflow"""

    def run(self, process_step: ProcessStep):
        self.execute_single_next_step(process_step)

    @classmethod
    def get_endpoint_basename(cls):
        return "wbcore:workflow:startstep"

    @classmethod
    def get_representation_endpoint(cls):
        return "wbcore:workflow:startsteprepresentation-list"

    class Meta:
        verbose_name = _("Start Step")
        verbose_name_plural = _("Start Steps")


class UserStep(Step):
    """A workflow step that needs an assigned user or user group to pick the next transition."""

    assignee = models.ForeignKey(
        to=User,
        verbose_name=_("Assignee"),
        on_delete=models.SET_NULL,
        related_name="assigned_workflow_steps",
        null=True,
        blank=True,
    )
    notify_user = models.BooleanField(verbose_name=_("Notify User"), default=True)
    group = models.ForeignKey(
        to=Group,
        verbose_name=_("Group"),
        on_delete=models.SET_NULL,
        related_name="assigned_workflow_steps",
        null=True,
        blank=True,
    )
    assignee_method = models.CharField(
        max_length=64,
        verbose_name=_("Assignee Method"),
        blank=True,
        null=True,
    )
    display = models.ForeignKey(
        to="workflow.Display",
        verbose_name=_("Display"),
        on_delete=models.SET_NULL,
        related_name="user_steps",
        null=True,
        blank=True,
    )
    kwargs = models.JSONField(verbose_name=_("Kwargs"), null=True, blank=True)

    def get_assigned_group(self) -> None | Group:
        return self.group

    def get_assigned_user(self) -> None | User:
        return self.assignee

    def execute_assignee_method(self, process_step: ProcessStep, method_name: str, **kwargs):
        for choice in workflow_site.assignees_methods:
            if method_name == choice[0]:
                process_step.assignee = choice[1](process_step, **kwargs)
                process_step.save()
                break

    def run(self, process_step: ProcessStep):
        if method := self.assignee_method:
            if self.kwargs:
                self.execute_assignee_method(process_step, method, **self.kwargs)
            else:
                self.execute_assignee_method(process_step, method)

        if not process_step.state == ProcessStep.StepState.FAILED:
            if self.get_all_valid_outgoing_transitions(process_step):
                if all_assignees := process_step.get_all_assignees():
                    if self.notify_user:
                        self.notify_assignees(all_assignees, process_step)
                else:
                    self.set_failed(process_step, gettext("No assignees selected!"))
            else:
                self.set_failed(
                    process_step,
                    gettext("No valid outgoing transitions found for this step!"),
                )

    def set_failed(self, process_step: ProcessStep, error_message: str):
        process_step.state = ProcessStep.StepState.FAILED
        # We don't want to overwrite a previous error message
        if not process_step.error_message:
            process_step.error_message = error_message
        process_step.save()
        if self.notify_user and (all_assignees := process_step.get_all_assignees()):
            self.notify_assignees(all_assignees, process_step, error_message)

        # Check if the process can still finish
        process_can_finish.delay(process_step.process.pk)

    def notify_assignees(self, assignees: list[User], process_step: ProcessStep, error_message: str = ""):
        if error_message:
            code = "workflow.userstep.notify_failed_step"
            title = gettext("Assigned Workflow Step Failed")
            body = gettext(
                "A workflow step you were assigned to just failed with the error message '{}'. Please take appropriate action."
            ).format(error_message)
        else:
            code = "workflow.userstep.notify_next_step"
            title = gettext("Workflow Step Awaiting Your Decision")
            body = gettext("You were assigned to a workflow step. Please select the next step.")

        for user in assignees:
            if user.is_active and self.user_can_see_step(user):
                send_notification(
                    code=code,
                    title=title,
                    body=body,
                    user=user,
                    endpoint=reverse(
                        f"{process_step.get_endpoint_basename()}-detail",
                        args=[process_step.id],
                    ),
                )

    @classmethod
    def get_endpoint_basename(cls):
        return "wbcore:workflow:userstep"

    @classmethod
    def get_representation_endpoint(cls):
        return "wbcore:workflow:usersteprepresentation-list"

    class Meta:
        verbose_name = _("User Step")
        verbose_name_plural = _("User Steps")
        constraints = [
            models.CheckConstraint(
                condition=~Q(assignee__isnull=False, group__isnull=False),
                name="check_not_both_assignee_group",
            ),
        ]
        notification_types = [
            create_notification_type(
                code="workflow.userstep.notify_next_step",
                title=gettext("Workflow Step Assignment Notification"),
                help_text=gettext(
                    "Notification for all assigned users that can transition a workflow step to the next step"
                ),
            ),
            create_notification_type(
                code="workflow.userstep.notify_failed_step",
                title=gettext("Failed Workflow Step Notification"),
                help_text=gettext("Notification for all assigned users of a failed workflow step"),
            ),
        ]


class DecisionStep(Step):
    """A background step that checks all conditions and activates the first transition that satisfies all of its conditions.
    Only really makes sense in conjunction with conditions that disable every transition but one.
    """

    def get_first_valid_transition(self, process_step: ProcessStep) -> Transition | None:
        for transition in self.get_outgoing_transitions():
            if transition.all_conditions_satisfied(process_step):
                return transition
        return None

    def run(self, process_step: ProcessStep):
        if transition := self.get_first_valid_transition(process_step):
            Step.start_next_step(process_step, transition)
        else:
            self.set_failed(
                process_step,
                gettext("No valid outgoing transition found for this step!"),
            )

    @classmethod
    def get_endpoint_basename(cls):
        return "wbcore:workflow:decisionstep"

    @classmethod
    def get_representation_endpoint(cls):
        return "wbcore:workflow:decisionsteprepresentation-list"

    class Meta:
        verbose_name = _("Decision Step")
        verbose_name_plural = _("Decision Steps")


class SplitStep(Step):
    """A background step that activates all transitions that meet all of their conditions"""

    def run(self, process_step: ProcessStep):
        if valid_transitions := self.get_all_valid_outgoing_transitions(process_step):
            self.set_finished(process_step)
            for transition in valid_transitions:
                next_step: Step = transition.to_step
                activate_step.delay(next_step.pk, process_step.process.pk)
        else:
            self.set_failed(
                process_step,
                gettext("No valid outgoing transitions found for this step!"),
            )

    @classmethod
    def get_endpoint_basename(cls):
        return "wbcore:workflow:splitstep"

    @classmethod
    def get_representation_endpoint(cls):
        return "wbcore:workflow:splitsteprepresentation-list"

    class Meta:
        verbose_name = _("Split Step")
        verbose_name_plural = _("Split Steps")


class JoinStep(Step):
    """A background step that joins multiple steps into one. Waits until all incoming transitions are done by default.
    If wait_for_all is False the first incoming transition cancels all other active incoming transitions.
    """

    wait_for_all = models.BooleanField(
        default=True,
        verbose_name=_("Wait For All"),
        help_text=_("If False, will cancel all other incoming process steps as soon the first reaches this step."),
    )

    def cancel_if_leading_to_self(self, step: Step, process_step: ProcessStep):
        """Recursively goes through all outgoing transitions of the provided step. Cancels the provided process step as soon as a transition that leads to the current split step is found.

        Args:
            step (Step): The step from which all outgoing transitions need to be investigated
            process_step (ProcessStep): The related process step that would need to be canceled
        """

        for transition in step.outgoing_transitions.all():
            if transition.to_step.pk == self.pk:
                process_step.step.set_canceled(process_step)
            else:
                self.cancel_if_leading_to_self(transition.to_step, process_step)

    def run(self, process_step: ProcessStep):
        process_step.state = ProcessStep.StepState.WAITING
        process_step.save()

        if self.wait_for_all:
            # Look for incoming transitions with no process step (not activated yet) or not finished
            if not Transition.objects.filter(
                Q(to_step=self)
                & Q(
                    Q(from_step__process_steps__isnull=True)
                    | Q(
                        ~Q(
                            from_step__process_steps__state__in=[
                                ProcessStep.StepState.FINISHED,
                                ProcessStep.StepState.CANCELED,
                            ]
                        )
                        & Q(from_step__process_steps__process=process_step.process)
                    )
                )
            ).exists():
                self.execute_single_next_step(process_step)
        else:
            # Set every unfinished process step that at some point leads to this step to canceled
            for unfinished_process_step in ProcessStep.objects.filter(process=process_step.process).exclude(
                Q(
                    Q(pk=process_step.pk)
                    | Q(
                        state__in=[
                            ProcessStep.StepState.FINISHED,
                            ProcessStep.StepState.CANCELED,
                            ProcessStep.StepState.FAILED,
                        ]
                    )
                )
            ):
                self.cancel_if_leading_to_self(unfinished_process_step.step, unfinished_process_step)
            self.execute_single_next_step(process_step)

    @classmethod
    def get_endpoint_basename(cls):
        return "wbcore:workflow:joinstep"

    @classmethod
    def get_representation_endpoint(cls):
        return "wbcore:workflow:joinsteprepresentation-list"

    class Meta:
        verbose_name = _("Join Step")
        verbose_name_plural = _("Join Steps")


class ScriptStep(Step):
    """A background step that will execute a provided python script."""

    script = models.TextField(verbose_name=_("Script"))

    def run(self, process_step: ProcessStep):
        try:
            loader = StringSourceLoader(self.script)
            loader.load_module().run(process_step)
        except Exception as e:
            self.set_failed(process_step, gettext("Executing script failed: {}".format(e)))
            return
        loader.cleanup()
        self.execute_single_next_step(process_step)

    @classmethod
    def get_endpoint_basename(cls):
        return "wbcore:workflow:scriptstep"

    @classmethod
    def get_representation_endpoint(cls):
        return "wbcore:workflow:scriptsteprepresentation-list"

    class Meta:
        verbose_name = _("Script Step")
        verbose_name_plural = _("Script Steps")


class EmailStep(Step):
    """A background step that sends an email to a list of email contacts."""

    template = models.FileField(
        max_length=256,
        verbose_name=_("Template"),
        upload_to="workflow/templates/Test_Templates.txt",
    )
    subject = models.CharField(
        max_length=128,
        verbose_name=_("Subject"),
    )
    to = models.ManyToManyField(
        "directory.EmailContact",
        related_name="workflow_step_receiver",
        verbose_name=pgettext_lazy("Email context", "To"),
    )
    cc = models.ManyToManyField(
        "directory.EmailContact",
        related_name="workflow_steps_cc",
        verbose_name=_("CC"),
        blank=True,
    )
    bcc = models.ManyToManyField(
        "directory.EmailContact",
        related_name="workflow_steps_bcc",
        verbose_name=_("BCC"),
        blank=True,
    )

    def run(self, process_step: ProcessStep):
        context = {
            "process_step_endpoint": base_domain()
            + reverse(f"{process_step.get_endpoint_basename()}-detail", args=[process_step.id]),
            "process_step": process_step,
        }
        try:
            rendered_html = Template(self.template.file).render(Context(context))
            msg = EmailMultiAlternatives(
                self.subject,
                convert_html2text(rendered_html),
                settings.DEFAULT_FROM_EMAIL,
                to=list(self.to.values_list("address", flat=True)),
                cc=list(self.cc.values_list("address", flat=True)),
                bcc=list(self.bcc.values_list("address", flat=True)),
            )
            msg.attach_alternative(rendered_html, "text/html")
            msg.send()
            self.execute_single_next_step(process_step)
        except TemplateSyntaxError:
            self.set_failed(process_step, gettext("Error in template syntax!"))

    @classmethod
    def get_endpoint_basename(cls):
        return "wbcore:workflow:emailstep"

    @classmethod
    def get_representation_endpoint(cls):
        return "wbcore:workflow:emailsteprepresentation-list"

    class Meta:
        verbose_name = _("Email Step")
        verbose_name_plural = _("Email Steps")


class FinishStep(Step):
    """The last step in a workflow"""

    write_preserved_instance = models.BooleanField(
        default=False,
        verbose_name=_("Write Preserved Instance"),
        help_text=_(
            "Writes the instance data backup onto the instance restoring its state to the beginning of the workflow."
        ),
    )

    def run(self, process_step: ProcessStep):
        # Finish if there are no running process steps for this process
        if (
            ProcessStep.objects.filter(
                process=process_step.process,
                state__in=[ProcessStep.StepState.WAITING, ProcessStep.StepState.ACTIVE],
            )
            .exclude(id=process_step.pk)
            .exists()
        ):
            self.set_failed(
                process_step,
                gettext("There are process steps still running for this workflow!"),
            )
        else:
            self.set_finished(process_step)

    def finish(self, process_step: ProcessStep):
        super().finish(process_step)

        if process_step.state == ProcessStep.StepState.FINISHED:
            # Save preserved instance
            if self.write_preserved_instance and (preserved_data := process_step.process.preserved_instance):
                attached_instance = process_step.process.instance
                serializer = get_model_serializer_class_for_instance(attached_instance)(data=preserved_data)
                serializer.is_valid()
                validated_data: dict = serializer.validated_data
                serializer.update(attached_instance, validated_data)

            # Finish entire process if process step is finished
            process: Process = process_step.process
            process.finished = datetime.now()
            process.state = Process.ProcessState.FINISHED
            process.save()

    @classmethod
    def get_endpoint_basename(cls):
        return "wbcore:workflow:finishstep"

    @classmethod
    def get_representation_endpoint(cls):
        return "wbcore:workflow:finishsteprepresentation-list"

    class Meta:
        verbose_name = _("Finish Step")
        verbose_name_plural = _("Finish Steps")


@shared_task(queue=Queue.DEFAULT.value)
def activate_step(step_id: int, process_id: UUID):
    step = Step.objects.get(pk=step_id).get_casted_step()
    process = Process.objects.get(pk=process_id)

    # We need to prevent creating a duplicate join step
    if (
        step.step_type == Step.StepType.JOINSTEP
        and (
            process_step_qs := ProcessStep.objects.filter(
                process=process,
                step=step,
                permission=step.permission,
                status=step.status,
                state=ProcessStep.StepState.WAITING,
                finished__isnull=True,
                group=step.get_assigned_group(),
                assignee=step.get_assigned_user(),
            )
        ).count()
        == 1
    ):
        process_step: ProcessStep = process_step_qs.first()
    else:
        process_step = ProcessStep.objects.create(
            process=process,
            step=step,
            permission=step.permission,
            status=step.status,
            group=step.get_assigned_group(),
            assignee=step.get_assigned_user(),
        )

    # Set status in attached model
    if step.status and (attached_instance := process_step.process.instance):
        field_name = process_step.process.workflow.status_field
        if hasattr(attached_instance, field_name):
            if attached_instance.__class__._meta.get_field(field_name).get_internal_type() == "CharField":
                setattr(attached_instance, field_name, step.status)
                attached_instance.save()

    step.run(process_step)


def _check_previous_steps_failed(step: Step, process: Process, check_all: bool = False):
    """Recursively checks if the previous steps of a step have failed and fails the process if they were critical.

    Args:
        step (Step): The step to be checked
        process (Process): The process to be checked
        check_all (bool, optional): Indicates if all of a step's previous steps need to fail in order to fail the entire process. Defaults to False.
    """

    previous_steps = step.get_previous_steps()
    failed_steps = 0
    for previous_step in previous_steps:
        if (process_steps_for_process_qs := previous_step.process_steps.filter(process=process)).exists():
            if process_steps_for_process_qs.first().state == ProcessStep.StepState.FAILED:
                if check_all:
                    # Only fail process if ALL previous steps have failed
                    failed_steps += 1
                    if failed_steps == len(previous_steps):
                        process.set_failed()
                        return
                else:
                    process.set_failed()
                    return
        else:
            for step in previous_step.get_previous_steps():
                if previous_step.step_type == Step.StepType.JOINSTEP:
                    if previous_step.get_casted_step().wait_for_all is False:
                        _check_previous_steps_failed(step, process, check_all=True)
                    # Join steps with wait_for_all=True will be checked by main for loop
                    continue
                else:
                    _check_previous_steps_failed(step, process)


@shared_task(queue=Queue.DEFAULT.value)
def process_can_finish(process_id: UUID):
    """Checks if all critical steps for a process can still be reached. Fails the process if this is not the case.

    Args:
        process_id (UUID): ID of the process to be checked
    """

    process = Process.objects.get(pk=process_id)

    # We can immediately fail the entire process when there are no more active process steps
    if not process.process_steps.filter(
        state__in=[ProcessStep.StepState.WAITING, ProcessStep.StepState.ACTIVE]
    ).exists():
        process.set_failed()

    # Otherwise we need to check if all unfinished join steps that need several inputs can still be reached
    else:
        waiting_join_steps = JoinStep.objects.filter(
            Q(workflow=process.workflow)
            & Q(wait_for_all=True)
            & Q(
                Q(process_steps__isnull=True)
                | Q(
                    Q(
                        process_steps__state__in=[
                            ProcessStep.StepState.ACTIVE,
                            ProcessStep.StepState.WAITING,
                        ]
                    )
                    & Q(process_steps__process=process)
                )
            )
        )
        for join_step in waiting_join_steps:
            _check_previous_steps_failed(join_step, process)
