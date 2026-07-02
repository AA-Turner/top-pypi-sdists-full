import datetime as dt

from securegroups.models import SmartFilter, SmartGroup
from securegroups.tasks import run_smart_group_update

from django.contrib.auth.models import Group
from django.utils.timezone import now
from eveuniverse.tests.testdata.factories_2 import EveEntityCorporationFactory

from app_utils.testdata_factories import EveCharacterFactory, EveCorporationInfoFactory
from app_utils.testing import NoSocketsTestCase
from memberaudit.tests.testdata.factories_2 import (
    CharacterCorporationHistoryFactory,
    CharacterFactory,
    CharacterTitleFactory,
    UserMainBasicAccessFactory,
)

from memberaudit_securegroups.tests.factories_2 import (
    CorporationTitleFilterFactory,
    TimeInCorporationFilterFactory,
)


class TestFilters(NoSocketsTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.group = Group.objects.create(name="Leadership")
        cls.corporation = EveCorporationInfoFactory()
        cls.corporation_entity = EveEntityCorporationFactory(
            id=cls.corporation.corporation_id
        )
        cls.character_1 = CharacterFactory(
            user=UserMainBasicAccessFactory(
                main_character__character=EveCharacterFactory(
                    corporation=cls.corporation
                )
            )
        )
        cls.character_2 = CharacterFactory(
            user=UserMainBasicAccessFactory(
                main_character__character=EveCharacterFactory(
                    corporation=cls.corporation
                )
            )
        )

    def test_corporation_title_filter(self):
        # given
        CharacterTitleFactory(character=self.character_1, name="CEO")
        CharacterTitleFactory(character=self.character_2, name="Diplomat")

        CorporationTitleFilterFactory(corporations=[self.corporation], title="CEO")
        smart_group = SmartGroup.objects.create(group=self.group, auto_group=True)
        title_filter = SmartFilter.objects.first()
        smart_group.filters.add(title_filter)

        # when
        run_smart_group_update(smart_group.id)

        # then
        self.assertEqual(
            title_filter.filter_object.name, "Member Audit Corporation Title"
        )
        self.assertIn(self.character_1.user, self.group.user_set.all())
        self.assertNotIn(self.character_2.user, self.group.user_set.all())

    def test_time_in_corporation_filter(self):
        # given
        CharacterCorporationHistoryFactory(
            character=self.character_1,
            corporation=self.corporation_entity,
            start_date=now() - dt.timedelta(days=31),
        )

        CharacterCorporationHistoryFactory(
            character=self.character_2,
            corporation=self.corporation_entity,
            start_date=now() - dt.timedelta(days=29),
        )

        TimeInCorporationFilterFactory(minimum_days=30)
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
        self.assertIn(self.character_1.user, self.group.user_set.all())
        self.assertNotIn(self.character_2.user, self.group.user_set.all())
