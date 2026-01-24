from random import choice

import factory
from django.db.models import signals
from faker import Faker

from wbcore.contrib.authentication.factories import GroupFactory
from wbcore.contrib.workflow.models import (
    DecisionStep,
    EmailStep,
    FinishStep,
    JoinStep,
    ScriptStep,
    SplitStep,
    StartStep,
    Step,
    UserStep,
)
from wbcore.contrib.workflow.sites import workflow_site

fake = Faker()


def _generate_random_printout() -> str:
    return f'def run(process_step):\r\n   print("{fake.sentence(nb_words=5)}")'


@factory.django.mute_signals(signals.post_save)
class StepFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("text", max_nb_chars=128)
    workflow = factory.SubFactory("wbcore.contrib.workflow.factories.WorkflowFactory")
    code = factory.Faker("pyint", min_value=0, max_value=9999)
    status = factory.Faker("text", max_nb_chars=64)

    class Meta:
        model = Step
        django_get_or_create = ["code", "workflow"]


class RandomChildStepFactory(StepFactory):
    @classmethod
    def create(cls, **kwargs):
        child_factories = [
            StartStepFactory,
            UserStepFactory,
            DecisionStepFactory,
            SplitStepFactory,
            JoinStepFactory,
            ScriptStepFactory,
            EmailStepFactory,
            FinishStepFactory,
        ]
        if exclude_factories := kwargs.get("exclude_factories"):
            child_factory = choice(list(set(child_factories) - set(exclude_factories)))
            kwargs.pop("exclude_factories")
        else:
            child_factory = choice(child_factories)

        # Create an instance using the selected child factory
        return child_factory.create(**kwargs)

    class Meta:
        model = Step
        django_get_or_create = ["code"]


class UserStepFactory(StepFactory):
    assignee_method = factory.Iterator([i[0] for i in workflow_site.assignees_choices])
    notify_user = factory.Faker("pybool")
    group = factory.SubFactory(GroupFactory)
    step_type = Step.StepType.USERSTEP
    display = factory.SubFactory("wbcore.contrib.workflow.factories.DisplayFactory")

    class Meta:
        model = UserStep


class DecisionStepFactory(StepFactory):
    step_type = Step.StepType.DECISIONSTEP

    class Meta:
        model = DecisionStep


class SplitStepFactory(StepFactory):
    step_type = Step.StepType.SPLITSTEP

    class Meta:
        model = SplitStep


class StartStepFactory(StepFactory):
    step_type = Step.StepType.STARTSTEP

    class Meta:
        model = StartStep


class JoinStepFactory(StepFactory):
    step_type = Step.StepType.JOINSTEP
    wait_for_all = factory.Faker("pybool")

    class Meta:
        model = JoinStep


class ScriptStepFactory(StepFactory):
    step_type = Step.StepType.SCRIPTSTEP
    script = factory.LazyAttribute(lambda o: _generate_random_printout())

    class Meta:
        model = ScriptStep


class EmailStepFactory(StepFactory):
    step_type = Step.StepType.EMAILSTEP
    template = factory.django.FileField(filename="testfile.dat", data=b"testdata")
    subject = factory.Faker("text", max_nb_chars=128)

    @factory.post_generation
    def to(self, create, extracted, **kwargs):
        if not create:
            return

        elif extracted:
            for recipient in extracted:
                self.to.add(recipient)

    @factory.post_generation
    def cc(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for recipient in extracted:
                self.cc.add(recipient)

    @factory.post_generation
    def bcc(self, create, extracted, **kwargs):
        if not create:
            return

        elif extracted:
            for recipient in extracted:
                self.bcc.add(recipient)

    class Meta:
        model = EmailStep
        skip_postgeneration_save = True


class FinishStepFactory(StepFactory):
    step_type = Step.StepType.FINISHSTEP
    write_preserved_instance = factory.SelfAttribute("workflow.preserve_instance")

    class Meta:
        model = FinishStep
