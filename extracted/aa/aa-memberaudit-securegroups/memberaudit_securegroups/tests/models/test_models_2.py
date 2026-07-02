import datetime as dt

from django.contrib.auth.models import User
from django.utils.timezone import now
from eveuniverse.tests.testdata.factories_2 import EveEntityCorporationFactory

from app_utils.testdata_factories import EveCharacterFactory, EveCorporationInfoFactory
from app_utils.testing import NoSocketsTestCase
from memberaudit.tests.testdata.factories_2 import (
    CharacterCloneInfoFactory,
    CharacterCorporationHistoryFactory,
    CharacterFactory,
    CharacterSkillpointsFactory,
    CharacterSkillSetCheckFactory,
    LocationStationFactory,
    NavigationSkillTypeFactory,
    SkillSetFactory,
    SkillSetSkillFactory,
    UserMainBasicAccessFactory,
)

from memberaudit_securegroups.models import SkillSetFilter
from memberaudit_securegroups.tests.factories_2 import (
    HomeStationFilterFactory,
    SkillPointFilterFactory,
    SkillSetFilterFilterFactory,
    TimeInCorporationFilterFactory,
)
from memberaudit_securegroups.tests.helpers import make_user_queryset


class TestHomeStationFilter_ProcessFilter(NoSocketsTestCase):
    def test_should_return_name(self):
        # given
        my_filter = HomeStationFilterFactory()

        # when/then
        self.assertTrue(my_filter.name)

    def test_should_return_true_when_main_has_correct_home_location(self):
        # given
        location_1 = LocationStationFactory()
        my_filter = HomeStationFilterFactory(home_station=location_1)
        user = UserMainBasicAccessFactory()
        character = CharacterFactory(user=user)
        CharacterCloneInfoFactory(character=character, home_location=location_1)

        # when/then
        self.assertTrue(my_filter.process_filter(user))

    def test_should_return_false_when_alt_has_correct_home_location_and_alts_excluded(
        self,
    ):
        # given
        location_1 = LocationStationFactory()
        my_filter = HomeStationFilterFactory(
            home_station=location_1, include_alts=False
        )
        user = UserMainBasicAccessFactory()
        character = CharacterFactory(user=user, is_main=False)
        CharacterCloneInfoFactory(character=character, home_location=location_1)

        # when/then
        self.assertFalse(my_filter.process_filter(user))

    def test_should_return_true_when_alt_has_correct_home_location_and_alts_included(
        self,
    ):
        # given
        location_1 = LocationStationFactory()
        my_filter = HomeStationFilterFactory(home_station=location_1, include_alts=True)
        user = UserMainBasicAccessFactory()
        character = CharacterFactory(user=user, is_main=False)
        CharacterCloneInfoFactory(character=character, home_location=location_1)

        # when/then
        self.assertTrue(my_filter.process_filter(user))

    def test_should_return_false_when_main_has_different_home_location(self):
        # given
        location_1 = LocationStationFactory()
        my_filter = HomeStationFilterFactory(home_station=location_1)
        user = UserMainBasicAccessFactory()
        character = CharacterFactory(user=user)
        location_2 = LocationStationFactory()
        CharacterCloneInfoFactory(character=character, home_location=location_2)

        # when/then
        self.assertFalse(my_filter.process_filter(user))

    def test_should_return_false_when_main_no_home_location_info(self):
        # given
        location_1 = LocationStationFactory()
        my_filter = HomeStationFilterFactory(home_station=location_1)
        user = UserMainBasicAccessFactory()
        CharacterFactory(user=user)

        # when/then
        self.assertFalse(my_filter.process_filter(user))

    def test_should_return_false_when_user_no_memberaudit_character(self):
        # given
        location_1 = LocationStationFactory()
        my_filter = HomeStationFilterFactory(home_station=location_1)
        user = UserMainBasicAccessFactory()

        # when/then
        self.assertFalse(my_filter.process_filter(user))


class TestHomeStationFilter_AuditFilter(NoSocketsTestCase):
    def test_should_return_audit_data_for_users_and_mains_only(self):
        # given
        location_1 = LocationStationFactory()
        my_filter = HomeStationFilterFactory(
            home_station=location_1, include_alts=False
        )

        main_1 = EveCharacterFactory(character_name="Bruce Wayne")
        user_1 = UserMainBasicAccessFactory(main_character__character=main_1)
        character_11 = CharacterFactory(user=user_1)
        CharacterCloneInfoFactory(character=character_11, home_location=location_1)
        alt_1 = EveCharacterFactory()
        character_12 = CharacterFactory(user=user_1, is_main=False, alt_character=alt_1)
        CharacterCloneInfoFactory(character=character_12, home_location=location_1)

        user_2 = UserMainBasicAccessFactory()
        alt_2 = EveCharacterFactory()
        character_2 = CharacterFactory(user=user_2, is_main=False, alt_character=alt_2)
        CharacterCloneInfoFactory(character=character_2, home_location=location_1)

        user_3 = UserMainBasicAccessFactory()

        # when
        users = make_user_queryset(user_1, user_2, user_3)
        result = my_filter.audit_filter(users)

        # then
        self.assertEqual(len(result), 3)
        self.assertDictEqual(
            result[user_1.id], {"message": "Bruce Wayne", "check": True}
        )
        self.assertFalse(result[user_2.id]["check"])
        self.assertFalse(result[user_3.id]["check"])

    def test_should_return_audit_data_for_three_users_and_including_alts(self):
        # given
        location_1 = LocationStationFactory()
        my_filter = HomeStationFilterFactory(home_station=location_1, include_alts=True)

        main_1 = EveCharacterFactory(character_name="Bruce Wayne")
        user_1 = UserMainBasicAccessFactory(main_character__character=main_1)
        character_11 = CharacterFactory(user=user_1)
        CharacterCloneInfoFactory(character=character_11, home_location=location_1)
        alt_1 = EveCharacterFactory()
        character_12 = CharacterFactory(user=user_1, is_main=False, alt_character=alt_1)
        CharacterCloneInfoFactory(character=character_12, home_location=location_1)

        user_2 = UserMainBasicAccessFactory()
        alt_2 = EveCharacterFactory()
        character_2 = CharacterFactory(user=user_2, is_main=False, alt_character=alt_2)
        CharacterCloneInfoFactory(character=character_2, home_location=location_1)

        user_3 = UserMainBasicAccessFactory()

        # when
        users = make_user_queryset(user_1, user_2, user_3)
        result = my_filter.audit_filter(users)

        # then
        self.assertEqual(len(result), 3)
        self.assertTrue(result[user_1.id]["check"])
        self.assertTrue(result[user_2.id]["check"])
        self.assertFalse(result[user_3.id]["check"])


class TestSkillSetFilter_Base(NoSocketsTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        # user with a main and an alt
        main = EveCharacterFactory(character_name="Bruce Wayne")
        cls.user = UserMainBasicAccessFactory(main_character__character=main)
        cls.character_11 = CharacterFactory(user=cls.user)
        alt = EveCharacterFactory(character_name="Clark Kent")
        cls.character_12 = CharacterFactory(
            user=cls.user, is_main=False, alt_character=alt
        )
        # amarr carrier skill set
        cls.amarr_carrier_skill_type = NavigationSkillTypeFactory(name="Amarr Carrier")
        cls.amarr_carrier_skill_set = SkillSetFactory()
        cls.amarr_carrier_skill_set_skill = SkillSetSkillFactory(
            skill_set=cls.amarr_carrier_skill_set,
            eve_type=cls.amarr_carrier_skill_type,
            required_level=3,
            recommended_level=5,
        )
        # caldari carrier skill set
        cls.caldari_carrier_skill_type = NavigationSkillTypeFactory(
            name="Caldari Carrier"
        )
        cls.caldari_carrier_skill_set = SkillSetFactory()


class TestSkillSetFilter_ProcessFilter(TestSkillSetFilter_Base):
    def test_should_return_name(self):
        # given
        my_filter = SkillSetFilterFilterFactory()

        # when/then
        self.assertTrue(my_filter.name)

    def test_should_return_false_when_user_does_not_have_skill_set_check(self):
        # given
        my_filter = SkillSetFilterFilterFactory(
            skill_sets=[self.amarr_carrier_skill_set, self.caldari_carrier_skill_set]
        )

        # when/then
        self.assertFalse(my_filter.process_filter(self.user))

    def test_should_return_false_when_user_did_not_pass_skill_set_check(self):
        # given
        my_filter = SkillSetFilterFilterFactory(
            skill_sets=[self.amarr_carrier_skill_set, self.caldari_carrier_skill_set]
        )
        skill_set_check = CharacterSkillSetCheckFactory(
            character=self.character_11, skill_set=self.amarr_carrier_skill_set
        )
        skill_set_check.failed_required_skills.add(self.amarr_carrier_skill_set_skill)

        # when/then
        self.assertFalse(my_filter.process_filter(self.user))

    def test_should_return_true_when_user_passes_skill_set(self):
        # given
        my_filter = SkillSetFilterFilterFactory(
            skill_sets=[self.amarr_carrier_skill_set, self.caldari_carrier_skill_set]
        )
        CharacterSkillSetCheckFactory(
            character=self.character_11, skill_set=self.amarr_carrier_skill_set
        )

        # when/then
        self.assertTrue(my_filter.process_filter(self.user))

    def test_should_return_true_when_user_passes_skill_set_except_recommended_skills(
        self,
    ):
        # given
        my_filter = SkillSetFilterFilterFactory(
            skill_sets=[self.amarr_carrier_skill_set, self.caldari_carrier_skill_set]
        )
        skill_set_check = CharacterSkillSetCheckFactory(
            character=self.character_11, skill_set=self.amarr_carrier_skill_set
        )
        skill_set_check.failed_recommended_skills.add(
            self.amarr_carrier_skill_set_skill
        )

        # when/then
        self.assertTrue(my_filter.process_filter(self.user))

    def test_should_return_false_when_character_is_main_but_alt_required(self):
        # given
        my_filter = SkillSetFilterFilterFactory(
            character_type=SkillSetFilter.CharacterType.ALTS_ONLY,
            skill_sets=[self.amarr_carrier_skill_set, self.caldari_carrier_skill_set],
        )
        CharacterSkillSetCheckFactory(
            character=self.character_11, skill_set=self.amarr_carrier_skill_set
        )

        # when/then
        self.assertFalse(my_filter.process_filter(self.user))

    def test_should_return_false_when_character_is_main_and_main_required(self):
        # given
        my_filter = SkillSetFilterFilterFactory(
            character_type=SkillSetFilter.CharacterType.MAINS_ONLY,
            skill_sets=[self.amarr_carrier_skill_set, self.caldari_carrier_skill_set],
        )
        CharacterSkillSetCheckFactory(
            character=self.character_11, skill_set=self.amarr_carrier_skill_set
        )

        # when/then
        self.assertTrue(my_filter.process_filter(self.user))

    def test_should_return_true_when_character_is_main_and_any_allowed(self):
        # given
        my_filter = SkillSetFilterFilterFactory(
            character_type=SkillSetFilter.CharacterType.ANY,
            skill_sets=[self.amarr_carrier_skill_set, self.caldari_carrier_skill_set],
        )
        CharacterSkillSetCheckFactory(
            character=self.character_11, skill_set=self.amarr_carrier_skill_set
        )

        # when/then
        self.assertTrue(my_filter.process_filter(self.user))

    def test_should_return_false_when_character_is_alt_but_main_required(self):
        # given
        my_filter = SkillSetFilterFilterFactory(
            character_type=SkillSetFilter.CharacterType.MAINS_ONLY,
            skill_sets=[self.amarr_carrier_skill_set, self.caldari_carrier_skill_set],
        )
        CharacterSkillSetCheckFactory(
            character=self.character_12, skill_set=self.amarr_carrier_skill_set
        )
        # when/then
        self.assertFalse(my_filter.process_filter(self.user))

    def test_should_return_true_when_character_is_alt_and_any_allowed(self):
        # given
        my_filter = SkillSetFilterFilterFactory(
            character_type=SkillSetFilter.CharacterType.ANY,
            skill_sets=[self.amarr_carrier_skill_set, self.caldari_carrier_skill_set],
        )
        CharacterSkillSetCheckFactory(
            character=self.character_12, skill_set=self.amarr_carrier_skill_set
        )
        # when/then
        self.assertTrue(my_filter.process_filter(self.user))

    def test_should_return_true_when_character_is_alt_and_alt_required(self):
        # given
        my_filter = SkillSetFilterFilterFactory(
            character_type=SkillSetFilter.CharacterType.ALTS_ONLY,
            skill_sets=[self.amarr_carrier_skill_set, self.caldari_carrier_skill_set],
        )
        CharacterSkillSetCheckFactory(
            character=self.character_12, skill_set=self.amarr_carrier_skill_set
        )
        # when/then
        self.assertTrue(my_filter.process_filter(self.user))


class TestSkillSetFilter_AuditFilter(TestSkillSetFilter_Base):
    def test_should_return_audit_data_with_several_users(self):
        # given
        my_filter = SkillSetFilterFilterFactory()
        my_filter.skill_sets.add(
            self.amarr_carrier_skill_set, self.caldari_carrier_skill_set
        )
        CharacterSkillSetCheckFactory(
            character=self.character_11, skill_set=self.amarr_carrier_skill_set
        )
        CharacterSkillSetCheckFactory(
            character=self.character_12, skill_set=self.amarr_carrier_skill_set
        )

        user_2 = UserMainBasicAccessFactory()
        character_3 = CharacterFactory(user=user_2)

        CharacterSkillSetCheckFactory(
            character=character_3, skill_set=self.amarr_carrier_skill_set
        )

        user_3 = UserMainBasicAccessFactory()

        # when
        users = make_user_queryset(self.user, user_2, user_3)
        result = my_filter.audit_filter(users)

        # then
        self.assertEqual(len(result), 3)
        self.assertTrue(result[self.user.id]["check"])
        self.assertTrue(result[user_2.id]["check"])
        self.assertFalse(result[user_3.id]["check"])

    def test_should_return_audit_data_when_character_is_main_but_alt_required(self):
        # given
        my_filter = SkillSetFilterFilterFactory(
            character_type=SkillSetFilter.CharacterType.ALTS_ONLY
        )
        my_filter.skill_sets.add(
            self.amarr_carrier_skill_set, self.caldari_carrier_skill_set
        )
        CharacterSkillSetCheckFactory(
            character=self.character_11, skill_set=self.amarr_carrier_skill_set
        )

        # when
        users = make_user_queryset(self.user)
        result = my_filter.audit_filter(users)

        # then
        self.assertEqual(len(result), 1)
        self.assertFalse(result[self.user.id]["check"])

    def test_should_return_audit_data_when_character_is_main_and_main_required(self):
        # given
        my_filter = SkillSetFilterFilterFactory(
            character_type=SkillSetFilter.CharacterType.MAINS_ONLY
        )
        my_filter.skill_sets.add(
            self.amarr_carrier_skill_set, self.caldari_carrier_skill_set
        )
        CharacterSkillSetCheckFactory(
            character=self.character_11, skill_set=self.amarr_carrier_skill_set
        )

        # when
        users = make_user_queryset(self.user)
        result = my_filter.audit_filter(users)

        # then
        expected = {self.user.id: {"check": True, "message": "Bruce Wayne"}}
        self.assertDictEqual(result, expected)

    def test_should_return_audit_data_when_character_is_main_and_any_allowed(self):
        # given
        my_filter = SkillSetFilterFilterFactory(
            character_type=SkillSetFilter.CharacterType.ANY
        )
        my_filter.skill_sets.add(
            self.amarr_carrier_skill_set, self.caldari_carrier_skill_set
        )
        CharacterSkillSetCheckFactory(
            character=self.character_11, skill_set=self.amarr_carrier_skill_set
        )
        # when
        users = make_user_queryset(self.user)
        result = my_filter.audit_filter(users)

        # then
        expected = {self.user.id: {"check": True, "message": "Bruce Wayne"}}
        self.assertDictEqual(result, expected)

    def test_should_return_audit_data_when_character_is_alt_but_main_required(self):
        # given
        my_filter = SkillSetFilterFilterFactory(
            character_type=SkillSetFilter.CharacterType.MAINS_ONLY
        )
        my_filter.skill_sets.add(
            self.amarr_carrier_skill_set, self.caldari_carrier_skill_set
        )
        CharacterSkillSetCheckFactory(
            character=self.character_12, skill_set=self.amarr_carrier_skill_set
        )
        # when
        users = make_user_queryset(self.user)
        result = my_filter.audit_filter(users)

        # then
        self.assertEqual(len(result), 1)
        self.assertFalse(result[self.user.id]["check"])

    def test_should_return_audit_data_when_character_is_alt_and_any_allowed(self):
        # given
        my_filter = SkillSetFilterFilterFactory(
            character_type=SkillSetFilter.CharacterType.ANY
        )
        my_filter.skill_sets.add(
            self.amarr_carrier_skill_set, self.caldari_carrier_skill_set
        )
        CharacterSkillSetCheckFactory(
            character=self.character_12, skill_set=self.amarr_carrier_skill_set
        )

        # when
        users = make_user_queryset(self.user)
        result = my_filter.audit_filter(users)

        # then
        expected = {self.user.id: {"check": True, "message": "Clark Kent"}}
        self.assertDictEqual(result, expected)

    def test_should_return_audit_data_when_character_is_alt_and_alt_required(self):
        # given
        my_filter = SkillSetFilterFilterFactory(
            character_type=SkillSetFilter.CharacterType.ANY
        )
        my_filter.skill_sets.add(
            self.amarr_carrier_skill_set, self.caldari_carrier_skill_set
        )
        CharacterSkillSetCheckFactory(
            character=self.character_12, skill_set=self.amarr_carrier_skill_set
        )

        # when
        users = make_user_queryset(self.user)
        result = my_filter.audit_filter(users)

        # then
        expected = {self.user.id: {"check": True, "message": "Clark Kent"}}
        self.assertDictEqual(result, expected)

    def test_should_default_to_any_as_character_type(self):
        # given
        my_filter = SkillSetFilterFilterFactory(character_type="")
        my_filter.skill_sets.add(
            self.amarr_carrier_skill_set, self.caldari_carrier_skill_set
        )
        CharacterSkillSetCheckFactory(
            character=self.character_12, skill_set=self.amarr_carrier_skill_set
        )

        self.assertEqual(my_filter.character_type, SkillSetFilter.CharacterType.ANY)


class TestSkillPointFilter(NoSocketsTestCase):
    def test_should_return_name(self):
        # given
        my_filter = SkillPointFilterFactory()

        # when/then
        self.assertTrue(my_filter.name)

    def test_should_return_true_when_main_has_sufficient_skill_points(self):
        # given
        skill_point_threshold = 5_000_000
        my_filter = SkillPointFilterFactory(skill_point_threshold=skill_point_threshold)
        user = UserMainBasicAccessFactory()
        character = CharacterFactory(user=user)
        CharacterSkillpointsFactory(
            character=character, total=skill_point_threshold + 1
        )

        # when/then
        self.assertTrue(my_filter.process_filter(user))

    def test_should_return_false_when_no_character_has_sufficient_skill_points(
        self,
    ):
        # given
        skill_point_threshold = 5_000_000
        my_filter = SkillPointFilterFactory(skill_point_threshold=skill_point_threshold)
        user = UserMainBasicAccessFactory()
        character = CharacterFactory(user=user)
        CharacterSkillpointsFactory(character=character, total=1)

        # when/then
        self.assertFalse(my_filter.process_filter(user))

    def test_should_return_false_when_character_has_no_skill_point_data(
        self,
    ):
        # given
        skill_point_threshold = 5_000_000
        my_filter = SkillPointFilterFactory(skill_point_threshold=skill_point_threshold)
        user = UserMainBasicAccessFactory()
        CharacterFactory(user=user)

        # when/then
        self.assertFalse(my_filter.process_filter(user))

    def test_should_return_true_when_alt_has_sufficient_skill_points(self):
        # given
        skill_point_threshold = 5_000_000
        my_filter = SkillPointFilterFactory(skill_point_threshold=skill_point_threshold)
        user = UserMainBasicAccessFactory()
        character = CharacterFactory(user=user, is_main=False)
        CharacterSkillpointsFactory(
            character=character, total=skill_point_threshold + 1
        )

        # when/then
        self.assertTrue(my_filter.process_filter(user))

    def test_should_return_correct_audit_data_for_users(self):
        # given
        skill_point_threshold = 5_000_000
        my_filter = SkillPointFilterFactory(skill_point_threshold=skill_point_threshold)

        main_1 = EveCharacterFactory(character_name="Bruce Wayne")
        user_1 = UserMainBasicAccessFactory(main_character__character=main_1)
        character_11 = CharacterFactory(user=user_1)
        CharacterSkillpointsFactory(
            character=character_11, total=skill_point_threshold + 1
        )
        alt_1 = EveCharacterFactory(character_name="Clark Kent")
        character_12 = CharacterFactory(user=user_1, is_main=False, alt_character=alt_1)
        CharacterSkillpointsFactory(
            character=character_12, total=skill_point_threshold + 1
        )

        user_2 = UserMainBasicAccessFactory()
        character_2 = CharacterFactory(user=user_2)
        CharacterSkillpointsFactory(character=character_2, total=1_000_000)

        user_3 = UserMainBasicAccessFactory()

        # when
        users = make_user_queryset(user_1, user_2, user_3)
        result = my_filter.audit_filter(users)

        # then
        self.assertEqual(len(result), 3)
        self.assertTrue(result[user_1.id]["check"])
        self.assertIn("Bruce Wayne", result[user_1.id]["message"])
        self.assertIn("Clark Kent", result[user_1.id]["message"])
        self.assertFalse(result[user_2.id]["check"])
        self.assertFalse(result[user_3.id]["check"])


class TestTimeInCorporationFilter_AuditFilter(NoSocketsTestCase):
    def test_should_return_audit_data_with_one_user_passing_and_one_not_passing(self):
        # given
        my_filter = TimeInCorporationFilterFactory(minimum_days=30)
        eve_corporation = EveCorporationInfoFactory()
        user_1 = UserMainBasicAccessFactory(
            main_character__character=EveCharacterFactory(corporation=eve_corporation)
        )
        character_1 = CharacterFactory(user=user_1)
        corporation = EveEntityCorporationFactory(id=eve_corporation.corporation_id)

        CharacterCorporationHistoryFactory(
            character=character_1,
            corporation=corporation,
            start_date=now() - dt.timedelta(days=30),
        )

        user_2 = UserMainBasicAccessFactory()
        character_2 = CharacterFactory(user=user_2)

        CharacterCorporationHistoryFactory(
            record_id=1,
            character=character_2,
            start_date=now() - dt.timedelta(days=100),
        )
        CharacterCorporationHistoryFactory(
            record_id=2,
            character=character_2,
            corporation=corporation,
            start_date=now() - dt.timedelta(days=29),
        )
        users = User.objects.filter(pk__in=[user_1.pk, user_2.pk])

        # when
        result = my_filter.audit_filter(users)

        # then
        expected = {
            user_1.id: {"message": "30 days", "check": True},
            user_2.id: {"message": "29 days", "check": False},
        }
        self.assertDictEqual(dict(result), expected)


class TestTimeInCorporationFilter_ProcessFilter(NoSocketsTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        corporation = EveCorporationInfoFactory()
        cls.user = UserMainBasicAccessFactory(
            main_character__character=EveCharacterFactory(corporation=corporation)
        )
        cls.character = CharacterFactory(user=cls.user)
        cls.corporation = EveEntityCorporationFactory(id=corporation.corporation_id)

    def test_should_return_name(self):
        # given
        my_filter = TimeInCorporationFilterFactory()

        # when/then
        self.assertTrue(my_filter.name)

    def test_should_return_true_when_main_membership_was_long_enough(self):
        # given
        CharacterCorporationHistoryFactory(
            character=self.character,
            corporation=self.corporation,
            start_date=now() - dt.timedelta(days=30),
        )
        my_filter = TimeInCorporationFilterFactory(minimum_days=30)

        # when/then
        self.assertTrue(my_filter.process_filter(self.user))

    def test_should_return_false_when_main_membership_was_not_long_enough(self):
        # given
        CharacterCorporationHistoryFactory(
            character=self.character,
            corporation=self.corporation,
            start_date=now() - dt.timedelta(days=29),
        )
        my_filter = TimeInCorporationFilterFactory(minimum_days=30)

        # when/then
        self.assertFalse(my_filter.process_filter(self.user))

    def test_should_return_false_when_main_membership_was_longer_than_defined(self):
        # given
        CharacterCorporationHistoryFactory(
            character=self.character,
            corporation=self.corporation,
            start_date=now() - dt.timedelta(days=30),
        )
        my_filter = TimeInCorporationFilterFactory(minimum_days=30, reversed_logic=True)

        # when/then
        self.assertFalse(my_filter.process_filter(self.user))

    def test_should_return_true_when_main_membership_was_not_long_enough(self):
        # given
        CharacterCorporationHistoryFactory(
            character=self.character,
            corporation=self.corporation,
            start_date=now() - dt.timedelta(days=29),
        )
        my_filter = TimeInCorporationFilterFactory(minimum_days=30, reversed_logic=True)

        # when/then
        self.assertTrue(my_filter.process_filter(self.user))

    def test_should_return_false_when_no_membership_data_for_main(self):
        # given
        my_filter = TimeInCorporationFilterFactory(minimum_days=30)

        # when/then
        self.assertFalse(my_filter.process_filter(self.user))

    def test_should_return_false_when_user_has_no_memberaudit_character(self):
        # given
        my_filter = TimeInCorporationFilterFactory(minimum_days=30)
        user = UserMainBasicAccessFactory()

        # when/then
        self.assertFalse(my_filter.process_filter(user))
