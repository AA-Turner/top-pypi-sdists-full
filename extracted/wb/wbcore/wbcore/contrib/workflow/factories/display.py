import random

import factory
from faker import Faker

from wbcore.contrib.directory.serializers import PersonModelSerializer
from wbcore.contrib.workflow.models import Display

fake = Faker()


def _generate_grid_areas() -> list[list[str]]:
    outer_list = []
    inner_list_length = random.randint(1, 5)
    for _ in range(random.randint(1, 5)):
        inner_list = []
        for _ in range(inner_list_length):
            inner_list.append(random.choice(PersonModelSerializer.Meta.fields))
        outer_list.append(inner_list)
    return outer_list


class DisplayFactory(factory.django.DjangoModelFactory):
    name = factory.Faker("text", max_nb_chars=128)
    grid_template_areas = factory.LazyAttribute(lambda o: _generate_grid_areas())

    class Meta:
        model = Display
