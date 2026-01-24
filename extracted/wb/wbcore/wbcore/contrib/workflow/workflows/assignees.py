from random import choices, randint

from django.utils.translation import gettext as _

from wbcore.contrib.authentication.models import User
from wbcore.contrib.workflow.models import ProcessStep

from ..decorators import register_assignee

# We need to migrate upon name changes!


@register_assignee("Instance Assignee's Manager")
def manager_of_instance_assignee(process_step: ProcessStep, **kwargs) -> User | None:
    if (
        (assignee_field := kwargs.get("assignee_field"))
        and (assignee_type := kwargs.get("assignee_type"))
        and hasattr(process_step.process.instance, assignee_field)
    ):
        assignee = getattr(process_step.process.instance, assignee_field)
        if assignee_type == "employee":
            for manager in assignee.get_managers():
                if hasattr(manager, "user_account") and manager.user_account.is_active:
                    return manager.user_account
        elif assignee_type == "entry":
            for manager in assignee.relationship_managers.all():
                if hasattr(manager, "user_account") and manager.user_account.is_active:
                    return manager.user_account

    process_step.step.get_casted_step().set_failed(
        process_step, _("Error in assignee method: Incorrect input in kwargs field!")
    )
    return None


@register_assignee("Weighted Random Group Member")
def weighted_random(process_step: ProcessStep, **kwargs) -> User | None:
    if (group := process_step.group) and (group_user_count := group.user_set.count()):
        similar_process_steps_selected_assignees: list[str] = list(
            ProcessStep.objects.filter(
                state__in=[
                    ProcessStep.StepState.FINISHED,
                    ProcessStep.StepState.ACTIVE,
                ],
                process=process_step.process,
                group=group,
                assignee__isnull=False,
                step__step_type="UserStep",
            )
            .exclude(id=process_step.id)
            .values_list("assignee", flat=True)
        )
        group_member_list: list[User] = list(group.user_set.all())
        number_of_past_assignee_occurrences: list[int] = [
            similar_process_steps_selected_assignees.count(x.pk) for x in group_member_list
        ]

        if sum(number_of_past_assignee_occurrences):
            # We redistribute each occurrence number between all of the other list items to increase their probability
            redistributed_list: list[int] = [0 for i in range(group_user_count)]
            for index, elem in enumerate(number_of_past_assignee_occurrences):
                for index2 in range(len(redistributed_list)):
                    if not index2 == index:
                        redistributed_list[index2] += elem / (group_user_count - 1) if elem else 0
            # Transform the list of absolute values into percentages
            new_weights: list[float] = [x / sum(redistributed_list) for x in redistributed_list]
            new_assignee: User = choices(group_member_list, weights=new_weights)[0]  # noqa
        else:
            new_assignee: User = choices(group_member_list)[0]  # noqa
        return new_assignee

    process_step.step.get_casted_step().set_failed(
        process_step,
        _("Error in assignee method: No populated group to pick assignee from selected!"),
    )
    return None


@register_assignee("Random Group Member")
def random_group_member(process_step: ProcessStep, **kwargs) -> User | None:
    if (group := process_step.group) and group.user_set.exists():
        return group.user_set.all()[randint(0, group.user_set.count() - 1)]  # noqa

    process_step.step.get_casted_step().set_failed(
        process_step,
        _("Error in assignee method: No populated group to pick assignee from selected!"),
    )
    return None
