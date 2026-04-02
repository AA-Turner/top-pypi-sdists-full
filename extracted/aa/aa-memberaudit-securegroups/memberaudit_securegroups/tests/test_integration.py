# Standard Library
import datetime as dt

# Third Party
from securegroups.models import SmartFilter, SmartGroup
from securegroups.tasks import run_smart_group_update

# Django
from django.contrib.auth.models import Group
from django.test import TestCase
from django.utils.timezone import now

# Alliance Auth
from allianceauth.eveonline.models import EveCorporationInfo

# Member Audit
from memberaudit.tests.testdata.factories import (
    create_character_corporation_history,
    create_character_title,
)
from memberaudit.tests.testdata.load_entities import load_entities
from memberaudit.tests.utils import create_memberaudit_character

# Alliance Auth (External Libs)
from eveuniverse.models import EveEntity

from .factories import (
    create_corporation_title_filter,
    create_time_in_corporation_filter,
)


class TestFilters(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        load_entities()
        cls.group = Group.objects.create(name="Leadership")
        cls.corporation_2001 = EveCorporationInfo.objects.get(corporation_id=2001)
        cls.corporation_entity_2001 = EveEntity.objects.get(id=2001)
        cls.corporation_entity_2002 = EveEntity.objects.get(id=2002)

    def test_corporation_title_filter(self):
        # given
        character_1001 = create_memberaudit_character(1001)  # in corp 2001
        user_1001 = character_1001.character_ownership.user
        create_character_title(character=character_1001, name="CEO")

        character_1002 = create_memberaudit_character(1002)  # in corp 2001
        user_1002 = character_1002.character_ownership.user
        create_character_title(character=character_1001, name="Diplomat")

        create_corporation_title_filter(
            corporations=[self.corporation_2001], title="CEO"
        )
        smart_group = SmartGroup.objects.create(group=self.group, auto_group=True)
        title_filter = SmartFilter.objects.first()
        smart_group.filters.add(title_filter)

        # when
        run_smart_group_update(smart_group.id)

        # then
        self.assertEqual(
            title_filter.filter_object.name, "Member Audit Corporation Title"
        )
        self.assertIn(user_1001, self.group.user_set.all())
        self.assertNotIn(user_1002, self.group.user_set.all())

    def test_time_in_corporation_filter(self):
        # given
        character_1001 = create_memberaudit_character(1001)
        user_1001 = character_1001.user
        create_character_corporation_history(
            character=character_1001,
            corporation=self.corporation_entity_2001,
            start_date=now() - dt.timedelta(days=31),
        )

        character_1002 = create_memberaudit_character(1002)
        user_1002 = character_1002.user
        create_character_corporation_history(
            character=character_1002,
            corporation=self.corporation_entity_2001,
            start_date=now() - dt.timedelta(days=29),
        )

        create_time_in_corporation_filter(minimum_days=30)
        smart_group = SmartGroup.objects.create(group=self.group, auto_group=True)
        my_filter = SmartFilter.objects.first()
        smart_group.filters.add(my_filter)

        # when
        run_smart_group_update(smart_group.id)

        # then
        self.assertEqual(
            my_filter.filter_object.name,
            "Member Audit Time in Corporation Filter",
        )
        self.assertIn(user_1001, self.group.user_set.all())
        self.assertNotIn(user_1002, self.group.user_set.all())
