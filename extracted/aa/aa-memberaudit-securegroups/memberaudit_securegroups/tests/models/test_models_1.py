import datetime as dt
from typing import NamedTuple

from django.utils.timezone import now
from eveuniverse.tests.testdata.factories_2 import EveTypeFactory

from app_utils.testdata_factories import EveCharacterFactory, EveCorporationInfoFactory
from app_utils.testing import NoSocketsTestCase, add_character_to_user
from memberaudit.app_settings import MEMBERAUDIT_APP_NAME
from memberaudit.models import CharacterRole
from memberaudit.tests.testdata.factories_2 import (
    CharacterAssetFactory,
    CharacterDetailsFactory,
    CharacterFactory,
    CharacterOnlineStatusFactory,
    CharacterRoleFactory,
    CharacterTitleFactory,
    UserMainBasicAccessFactory,
)

from memberaudit_securegroups.tests.factories_2 import (
    ActivityFilterFactory,
    AgeFilterFactory,
    AssetFilterFactory,
    ComplianceFilterFactory,
    CorporationRoleFilterFactory,
    CorporationTitleFilterFactory,
)
from memberaudit_securegroups.tests.helpers import make_user_queryset


class TestActivityFilter(NoSocketsTestCase):
    def test_should_return_name(self):
        # given
        my_filter = ActivityFilterFactory()

        # when/then
        self.assertTrue(my_filter.name)

    def test_should_return_true_when_last_login_within_threshold(self):
        # given
        inactivity_threshold = 5
        my_filter = ActivityFilterFactory(inactivity_threshold=inactivity_threshold)
        user = UserMainBasicAccessFactory()
        character = CharacterFactory(user=user)

        class Case(NamedTuple):
            name: str
            last_login: dt.datetime
            last_logout: dt.datetime
            want: bool

        cases = [
            Case(
                name="login and logout after threshold",
                last_login=now() - dt.timedelta(minutes=30),
                last_logout=now() - dt.timedelta(minutes=5),
                want=True,
            ),
            Case(
                name="login before threshold, logout after threshold",
                last_login=now() - dt.timedelta(days=inactivity_threshold, minutes=30),
                last_logout=now() - dt.timedelta(minutes=5),
                want=True,
            ),
            Case(
                name="logout before threshold",
                last_login=now() - dt.timedelta(days=inactivity_threshold, minutes=30),
                last_logout=now() - dt.timedelta(days=inactivity_threshold, minutes=5),
                want=False,
            ),
        ]
        for tc in cases:
            with self.subTest(name=tc.name):
                status = CharacterOnlineStatusFactory(
                    character=character,
                    last_login=tc.last_login,
                    last_logout=tc.last_logout,
                )

                # when/then
                self.assertEqual(my_filter.process_filter(user), tc.want)
                status.delete()

    def test_should_return_false_when_no_online_data(self):
        # given
        inactivity_threshold = 5
        my_filter = ActivityFilterFactory(inactivity_threshold=inactivity_threshold)
        user = UserMainBasicAccessFactory()
        CharacterFactory(user=user)

        # when/then
        self.assertFalse(my_filter.process_filter(user))

    def test_should_return_correct_audit_data_for_users(self):
        # given
        inactivity_threshold = 5
        my_filter = ActivityFilterFactory(inactivity_threshold=inactivity_threshold)

        main_1 = EveCharacterFactory(character_name="Bruce Wayne")
        user_1 = UserMainBasicAccessFactory(main_character__character=main_1)
        character_11 = CharacterFactory(user=user_1)
        CharacterOnlineStatusFactory(
            character=character_11,
            last_login=now() - dt.timedelta(minutes=30),
            last_logout=now() - dt.timedelta(minutes=5),
        )
        alt_1 = EveCharacterFactory(character_name="Clark Kent")
        character_12 = CharacterFactory(user=user_1, is_main=False, alt_character=alt_1)
        CharacterOnlineStatusFactory(
            character=character_12,
            last_login=now() - dt.timedelta(minutes=30),
            last_logout=now() - dt.timedelta(minutes=5),
        )

        user_2 = UserMainBasicAccessFactory()
        character_2 = CharacterFactory(user=user_2)
        CharacterOnlineStatusFactory(
            character=character_2,
            last_login=now() - dt.timedelta(days=inactivity_threshold, minutes=30),
            last_logout=now() - dt.timedelta(days=inactivity_threshold, minutes=5),
        )

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


class TestAgeFilter(NoSocketsTestCase):
    def test_should_return_name(self):
        # given
        my_filter = AgeFilterFactory()

        # when/then
        self.assertTrue(my_filter.name)

    def test_should_return_true_when_main_older_then_threshold(self):
        # given
        age_threshold = 5
        my_filter = AgeFilterFactory(age_threshold=age_threshold)
        user = UserMainBasicAccessFactory()
        character = CharacterFactory(user=user)
        CharacterDetailsFactory(
            character=character,
            birthday=now() - dt.timedelta(days=age_threshold, seconds=1),
        )

        # when/then
        self.assertTrue(my_filter.process_filter(user))

    def test_should_return_false_when_main_younger_then_threshold(
        self,
    ):
        # given
        age_threshold = 5
        my_filter = AgeFilterFactory(age_threshold=age_threshold)
        user = UserMainBasicAccessFactory()
        character = CharacterFactory(user=user)
        CharacterDetailsFactory(character=character, birthday=now())

        # when/then
        self.assertFalse(my_filter.process_filter(user))

    def test_should_return_correct_audit_data_for_users(self):
        # given
        age_threshold = 5
        my_filter = AgeFilterFactory(age_threshold=age_threshold)

        main_1 = EveCharacterFactory(character_name="Bruce Wayne")
        user_1 = UserMainBasicAccessFactory(main_character__character=main_1)
        character_11 = CharacterFactory(user=user_1)
        CharacterDetailsFactory(
            character=character_11,
            birthday=now() - dt.timedelta(days=age_threshold, seconds=1),
        )
        alt_1 = EveCharacterFactory(character_name="Clark Kent")
        character_12 = CharacterFactory(user=user_1, is_main=False, alt_character=alt_1)
        CharacterDetailsFactory(
            character=character_12,
            birthday=now() - dt.timedelta(days=age_threshold, seconds=1),
        )

        user_2 = UserMainBasicAccessFactory()
        character_2 = CharacterFactory(user=user_2)
        CharacterDetailsFactory(character=character_2, birthday=now())

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


class TestAssetFilter_ProcessFilter(NoSocketsTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.user = UserMainBasicAccessFactory()
        cls.character = CharacterFactory(user=cls.user)

    def test_should_return_name(self):
        # given
        my_filter = AssetFilterFactory()

        # when/then
        self.assertTrue(my_filter.name)

    def test_should_return_false_when_user_does_not_have_asset(self):
        # given
        eve_type_1 = EveTypeFactory()
        my_filter = AssetFilterFactory(assets=[eve_type_1])
        eve_type_2 = EveTypeFactory()
        CharacterAssetFactory(character=self.character, eve_type=eve_type_2)

        # when/then
        self.assertFalse(my_filter.process_filter(self.user))

    def test_should_return_true_when_user_has_asset(self):
        # given
        eve_type = EveTypeFactory()
        my_filter = AssetFilterFactory(assets=[eve_type])
        CharacterAssetFactory(character=self.character, eve_type=eve_type)

        # when/then
        self.assertTrue(my_filter.process_filter(self.user))

    def test_should_return_true_when_user_has_at_least_one_asset(self):
        # given
        eve_type_1 = EveTypeFactory()
        eve_type_2 = EveTypeFactory()
        my_filter = AssetFilterFactory(assets=[eve_type_1, eve_type_2])
        CharacterAssetFactory(character=self.character, eve_type=eve_type_1)

        # when/then
        self.assertTrue(my_filter.process_filter(self.user))


class TestAssetFilter_AuditFilters(NoSocketsTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        cls.user = UserMainBasicAccessFactory()
        cls.character = CharacterFactory(user=cls.user)

    def test_should_return_audit_data_for_one_matching_one_not_matching_user(self):
        # given a filter for Merlins
        my_filter = AssetFilterFactory()
        eve_type = EveTypeFactory(name="Merlin")
        my_filter.assets.add(eve_type)

        # and user's character has a Merlin
        user_1 = UserMainBasicAccessFactory(
            main_character__character=EveCharacterFactory(character_name="Bruce Wayne")
        )
        character_1 = CharacterFactory(user=user_1)
        CharacterAssetFactory(character=character_1, eve_type=eve_type)

        # and main user's 2nd character also has a Merlin
        character_2 = CharacterFactory(
            user=user_1,
            is_main=False,
            alt_character=EveCharacterFactory(character_name="Clark Kent"),
        )
        CharacterAssetFactory(character=character_2, eve_type=eve_type)

        # and a 2nd user has a registered character, but no Merlin
        user_2 = UserMainBasicAccessFactory()
        CharacterFactory(user=user_2)

        # and a 3rd user is not registered
        user_3 = UserMainBasicAccessFactory()

        # when
        users = make_user_queryset(user_1, user_2, user_3)
        result = my_filter.audit_filter(users)

        # then
        self.assertDictEqual(
            result[user_1.id],
            {"message": "Bruce Wayne (Merlin), Clark Kent (Merlin)", "check": True},
        )
        self.assertDictEqual(
            result[user_2.id],
            {"message": "No matching assets found", "check": False},
        )
        self.assertDictEqual(
            result[user_3.id], {"message": "No audit information found", "check": False}
        )
        self.assertEqual(len(result), 3)

    def test_should_return_audit_data_when_no_matches(self):
        # given
        my_filter = AssetFilterFactory()

        # when
        users = make_user_queryset(self.user)
        result = my_filter.audit_filter(users)

        # then
        self.assertEqual(len(result), 1)
        self.assertDictEqual(
            result[self.user.id],
            {"message": "No matching assets found", "check": False},
        )


class TestComplianceFilter_ProcessFiler(NoSocketsTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.compliance_filter = ComplianceFilterFactory()
        cls.compliance_filter_reversed = ComplianceFilterFactory(reversed_logic=True)

    def test_should_return_name(self):
        self.assertTrue(self.compliance_filter.name)

    def test_should_return_true_when_user_is_compliant_1(self):
        # given a user with 1 registered character
        user = UserMainBasicAccessFactory()
        CharacterFactory(user=user)

        # when/then
        self.assertTrue(self.compliance_filter.process_filter(user))

    def test_should_return_true_when_user_is_compliant_2(self):
        # given a user with 2 registered character
        user = UserMainBasicAccessFactory()
        CharacterFactory(user=user)
        CharacterFactory(user=user, is_main=False)

        # when/then
        self.assertTrue(self.compliance_filter.process_filter(user))

    def test_should_return_false_when_user_is_compliant_1_reversed(self):
        # given a user with 1 registered character
        user = UserMainBasicAccessFactory()
        CharacterFactory(user=user)

        # when/then
        self.assertFalse(self.compliance_filter_reversed.process_filter(user))

    def test_should_return_false_when_user_is_compliant_2_reversed(self):
        # given a user with 2 registered character
        user = UserMainBasicAccessFactory()
        CharacterFactory(user=user)
        CharacterFactory(user=user, is_main=False)

        # when/then
        self.assertFalse(self.compliance_filter_reversed.process_filter(user))

    def test_should_return_false_when_user_is_not_compliant_1(self):
        user = UserMainBasicAccessFactory()
        self.assertFalse(self.compliance_filter.process_filter(user))

    def test_should_return_false_when_user_is_not_compliant_2(self):
        # given a user with 1 registered and 1 unregistered character
        user = UserMainBasicAccessFactory()
        CharacterFactory(user=user)
        add_character_to_user(user, EveCharacterFactory())

        # when/then
        self.assertFalse(self.compliance_filter.process_filter(user))

    def test_should_return_true_when_user_is_not_compliant_1_reversed(self):
        user = UserMainBasicAccessFactory()
        self.assertTrue(self.compliance_filter_reversed.process_filter(user))

    def test_should_return_true_when_user_is_not_compliant_2_reversed(self):
        # given a user with 1 registered and 1 unregistered character
        user = UserMainBasicAccessFactory()
        CharacterFactory(user=user)
        add_character_to_user(user, EveCharacterFactory())

        # when/then
        self.assertTrue(self.compliance_filter_reversed.process_filter(user))


class TestComplianceFilter_AuditFilter(NoSocketsTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.compliance_filter = ComplianceFilterFactory()
        cls.compliance_filter_reversed = ComplianceFilterFactory(reversed_logic=True)

    def test_should_return_audit_data_for_users(self):
        # given
        user_1 = UserMainBasicAccessFactory()
        CharacterFactory(user=user_1)
        CharacterFactory(user=user_1, is_main=False)
        user_2 = UserMainBasicAccessFactory()

        # when
        users = make_user_queryset(user_1, user_2)
        result = self.compliance_filter.audit_filter(users)

        # then
        self.assertEqual(len(result), 2)
        result_user_1 = result[user_1.pk]
        self.assertTrue(result_user_1["check"])
        self.assertEqual(
            result_user_1["message"],
            f"All characters have been added to {MEMBERAUDIT_APP_NAME}",
        )
        result_user_2 = result[user_2.pk]
        self.assertFalse(result_user_2["check"])
        user_2_name = user_2.profile.main_character.character_name
        self.assertIn(user_2_name, result_user_2["message"])

    def test_should_return_audit_data_for_users_reversed(self):
        # given
        user_1 = UserMainBasicAccessFactory()
        CharacterFactory(user=user_1)
        CharacterFactory(user=user_1, is_main=False)
        user_2 = UserMainBasicAccessFactory()

        # when
        users = make_user_queryset(user_1, user_2)
        result = self.compliance_filter_reversed.audit_filter(users)

        # then
        self.assertEqual(len(result), 2)

        result_user_1 = result[user_1.pk]
        self.assertFalse(result_user_1["check"])
        self.assertEqual(
            result_user_1["message"],
            f"All characters have been added to {MEMBERAUDIT_APP_NAME}",
        )

        result_user_2 = result[user_2.pk]
        self.assertTrue(result_user_2["check"])
        user_2_name = user_2.profile.main_character.character_name
        self.assertIn(user_2_name, result_user_2["message"])

    def test_should_return_audit_data_for_non_compliant_user_with_1_character(self):
        # when
        eve_character = EveCharacterFactory(character_name="Bruce Wayne")
        user = UserMainBasicAccessFactory(main_character__character=eve_character)
        users = make_user_queryset(user)
        result = self.compliance_filter.audit_filter(users)

        # then
        expected = {
            user.pk: {
                "check": False,
                "message": "Missing character: Bruce Wayne",
            },
        }
        self.assertDictEqual(result, expected)

    def test_should_return_audit_data_for_non_compliant_user_with_1_character_reversed(
        self,
    ):
        # when
        eve_character = EveCharacterFactory(character_name="Bruce Wayne")
        user = UserMainBasicAccessFactory(main_character__character=eve_character)
        users = make_user_queryset(user)
        result = self.compliance_filter_reversed.audit_filter(users)

        # then
        expected = {
            user.pk: {
                "check": True,
                "message": "Missing character: Bruce Wayne",
            },
        }
        self.assertDictEqual(result, expected)

    def test_should_return_audit_data_for_non_compliant_user_with_2_characters(self):
        # given
        eve_character_1 = EveCharacterFactory(character_name="Bruce Wayne")
        user = UserMainBasicAccessFactory(main_character__character=eve_character_1)
        add_character_to_user(user, EveCharacterFactory(character_name="Clark Kent"))

        # when
        users = make_user_queryset(user)
        result = self.compliance_filter.audit_filter(users)

        # then
        expected = {
            user.pk: {
                "check": False,
                "message": "Missing characters: Bruce Wayne, Clark Kent",
            },
        }
        self.assertDictEqual(result, expected)

    def test_should_return_audit_data_for_non_compliant_user_with_2_characters_reversed(
        self,
    ):
        # given
        eve_character_1 = EveCharacterFactory(character_name="Bruce Wayne")
        user = UserMainBasicAccessFactory(main_character__character=eve_character_1)
        add_character_to_user(user, EveCharacterFactory(character_name="Clark Kent"))

        # when
        users = make_user_queryset(user)
        result = self.compliance_filter_reversed.audit_filter(users)

        # then
        expected = {
            user.pk: {
                "check": True,
                "message": "Missing characters: Bruce Wayne, Clark Kent",
            },
        }
        self.assertDictEqual(result, expected)


class TestCorporationRoleFilter_ProcessFilter(NoSocketsTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.corporation = EveCorporationInfoFactory()
        cls.user = UserMainBasicAccessFactory(
            main_character__character=EveCharacterFactory(corporation=cls.corporation)
        )
        cls.character = CharacterFactory(user=cls.user)

    def test_should_return_name(self):
        # given
        my_filter = CorporationRoleFilterFactory(corporations=[])

        # when/then
        self.assertTrue(my_filter.name)

    def test_should_return_false_when_user_does_not_have_role(self):
        # given
        my_filter = CorporationRoleFilterFactory(corporations=[self.corporation])

        # when/then
        self.assertFalse(my_filter.process_filter(self.user))

    def test_should_return_true_when_user_has_character_with_role_in_corp(self):
        # given
        my_filter = CorporationRoleFilterFactory(
            corporations=[self.corporation], role=CharacterRole.Role.DIRECTOR
        )
        CharacterRoleFactory(character=self.character, role=CharacterRole.Role.DIRECTOR)
        # when/then
        self.assertTrue(my_filter.process_filter(self.user))

    def test_should_return_false_when_user_role_is_not_universal(self):
        # given
        my_filter = CorporationRoleFilterFactory(
            corporations=[self.corporation], role=CharacterRole.Role.DIRECTOR
        )
        CharacterRoleFactory(
            character=self.character,
            role=CharacterRole.Role.DIRECTOR,
            location=CharacterRole.Location.OTHER,
        )
        # when/then
        self.assertFalse(my_filter.process_filter(self.user))

    def test_should_return_false_when_character_with_role_is_in_wrong_corp(self):
        # given
        my_filter = CorporationRoleFilterFactory(
            corporations=[EveCorporationInfoFactory()], role=CharacterRole.Role.DIRECTOR
        )
        my_filter.corporations.add(EveCorporationInfoFactory())
        CharacterRoleFactory(
            character=self.character,
            role=CharacterRole.Role.DIRECTOR,
        )
        # when/then
        self.assertFalse(my_filter.process_filter(self.user))

    def test_should_return_false_character_with_role_owned_by_other_user(self):
        # given
        my_filter = CorporationRoleFilterFactory(
            corporations=[EveCorporationInfoFactory()], role=CharacterRole.Role.DIRECTOR
        )
        character_2 = CharacterFactory()
        CharacterRoleFactory(character=character_2, role=CharacterRole.Role.DIRECTOR)
        # when/then
        self.assertFalse(my_filter.process_filter(self.user))

    def test_should_return_false_when_character_with_role_is_not_main(self):
        # given filter for mains only
        my_filter = CorporationRoleFilterFactory(
            corporations=[self.corporation],
            role=CharacterRole.Role.DIRECTOR,
            include_alts=False,
        )
        # and character has role, but is not main
        character_2 = CharacterFactory(user=self.user, is_main=False)
        CharacterRoleFactory(character=character_2, role=CharacterRole.Role.DIRECTOR)
        # when/then
        self.assertFalse(my_filter.process_filter(self.user))

    def test_should_return_true_when_character_with_role_is_not_main_but_allowed(self):
        # given including alts
        my_filter = CorporationRoleFilterFactory(
            corporations=[self.corporation],
            role=CharacterRole.Role.DIRECTOR,
            include_alts=True,
        )

        # and character has role, but is not main
        user = UserMainBasicAccessFactory()
        character_2 = CharacterFactory(
            user=user,
            is_main=False,
            alt_character=EveCharacterFactory(corporation=self.corporation),
        )
        CharacterRoleFactory(character=character_2, role=CharacterRole.Role.DIRECTOR)

        # when/then
        self.assertTrue(my_filter.process_filter(user))


class TestCorporationRoleFilter_AuditFilters(NoSocketsTestCase):
    def test_should_return_audit_data_for_three_users_and_no_alts(self):
        # given
        corporation = EveCorporationInfoFactory()
        my_filter = CorporationRoleFilterFactory(
            corporations=[corporation, EveCorporationInfoFactory()],
            role=CharacterRole.Role.DIRECTOR,
            include_alts=False,
        )

        user_1 = UserMainBasicAccessFactory(
            main_character__character=EveCharacterFactory(corporation=corporation)
        )
        character_1 = CharacterFactory(user=user_1)
        CharacterRoleFactory(character=character_1, role=CharacterRole.Role.DIRECTOR)

        user_2 = UserMainBasicAccessFactory()
        character_2 = CharacterFactory(user=user_2)
        CharacterRoleFactory(character=character_2, role=CharacterRole.Role.DIRECTOR)

        user_3 = UserMainBasicAccessFactory()

        # when
        users = make_user_queryset(user_1, user_2, user_3)
        result = my_filter.audit_filter(users)

        # then
        self.assertEqual(len(result), 3)
        self.assertTrue(result[user_1.pk]["check"])
        self.assertFalse(result[user_2.pk]["check"])
        self.assertFalse(result[user_3.pk]["check"])

    def test_should_return_audit_data_for_two_users_with_alts(self):
        # given
        corporation_1 = EveCorporationInfoFactory()
        corporation_2 = EveCorporationInfoFactory()
        my_filter = CorporationRoleFilterFactory(
            corporations=[corporation_1, corporation_2],
            role=CharacterRole.Role.DIRECTOR,
            include_alts=True,
        )

        main_1 = EveCharacterFactory(
            character_name="Bruce Wayne", corporation=corporation_1
        )
        user_1 = UserMainBasicAccessFactory(main_character__character=main_1)
        character_11 = CharacterFactory(user=user_1)
        CharacterRoleFactory(character=character_11, role=CharacterRole.Role.DIRECTOR)
        alt = EveCharacterFactory(
            character_name="Clark Kent", corporation=corporation_1
        )
        character_12 = CharacterFactory(user=user_1, is_main=False, alt_character=alt)
        CharacterRoleFactory(character=character_12, role=CharacterRole.Role.DIRECTOR)

        main_2 = EveCharacterFactory(
            character_name="Lex Luther", corporation=corporation_2
        )
        user_2 = UserMainBasicAccessFactory(main_character__character=main_2)
        character_2 = CharacterFactory(user=user_2)
        CharacterRoleFactory(character=character_2, role=CharacterRole.Role.DIRECTOR)

        user_3 = UserMainBasicAccessFactory()

        # when
        users = make_user_queryset(user_1, user_2, user_3)
        result = my_filter.audit_filter(users)

        # then
        self.assertEqual(len(result), 3)
        self.assertDictEqual(
            result[user_1.id],
            {"message": "Bruce Wayne, Clark Kent", "check": True},
        )
        self.assertDictEqual(
            result[user_2.id], {"message": "Lex Luther", "check": True}
        )
        self.assertDictEqual(
            result[user_3.id],
            {"message": "No matching character found", "check": False},
        )


class TestCorporationTitleFilter_ProcessFilter(NoSocketsTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.corporation = EveCorporationInfoFactory()
        main_1 = EveCharacterFactory(corporation=cls.corporation)
        cls.user_1 = UserMainBasicAccessFactory(main_character__character=main_1)
        cls.character_1 = CharacterFactory(user=cls.user_1)

    def test_should_return_name(self):
        # given
        my_filter = CorporationTitleFilterFactory(corporations=[])

        # when/then
        self.assertTrue(my_filter.name)

    def test_should_return_false_when_user_does_not_have_title(self):
        # given
        my_filter = CorporationTitleFilterFactory(corporations=[])

        # when/then
        self.assertFalse(my_filter.process_filter(self.user_1))

    def test_should_return_true_when_user_has_character_with_title_in_corp(self):
        # given
        my_filter = CorporationTitleFilterFactory(
            corporations=[self.corporation], title="Alpha"
        )
        CharacterTitleFactory(character=self.character_1, name="Alpha")

        # when/then
        self.assertTrue(my_filter.process_filter(self.user_1))

    def test_should_not_return_true_when_user_has_character_with_title_but_corp_not_defined(
        self,
    ):
        # given
        my_filter = CorporationTitleFilterFactory(corporations=[], title="Alpha")
        CharacterTitleFactory(character=self.character_1, name="Alpha")

        # when/then
        self.assertFalse(my_filter.process_filter(self.user_1))

    def test_should_return_false_when_character_with_title_is_in_wrong_corp(self):
        # given
        my_filter = CorporationTitleFilterFactory(
            corporations=[EveCorporationInfoFactory()], title="Alpha"
        )
        CharacterTitleFactory(character=self.character_1, name="Alpha")

        # when/then
        self.assertFalse(my_filter.process_filter(self.user_1))

    def test_should_return_false_character_with_title_is_owned_by_other_user(self):
        # given
        my_filter = CorporationTitleFilterFactory(
            corporations=[self.corporation], title="Alpha"
        )
        character_2 = CharacterFactory()
        CharacterTitleFactory(character=character_2, name="Alpha")

        # when/then
        self.assertFalse(my_filter.process_filter(self.user_1))

    def test_should_return_false_when_character_with_title_is_not_main(self):
        # given filter for mains only
        my_filter = CorporationTitleFilterFactory(
            corporations=[self.corporation], title="Alpha", include_alts=False
        )
        # and owned character has title, but is not main
        alt = EveCharacterFactory(corporation=self.corporation)
        character_2 = CharacterFactory(
            user=self.user_1, is_main=False, alt_character=alt
        )
        CharacterTitleFactory(character=character_2, name="Alpha")

        # when/then
        self.assertFalse(my_filter.process_filter(self.user_1))

    def test_should_return_true_when_character_with_title_is_not_main_but_allowed(self):
        # given filter for mains only
        my_filter = CorporationTitleFilterFactory(
            corporations=[self.corporation], title="Alpha", include_alts=True
        )

        # and character has title, but is not main
        alt = EveCharacterFactory(corporation=self.corporation)
        character_2 = CharacterFactory(
            user=self.user_1, is_main=False, alt_character=alt
        )
        CharacterTitleFactory(character=character_2, name="Alpha")

        # when/then
        self.assertTrue(my_filter.process_filter(self.user_1))


class TestCorporationTitleFilter_AuditFilter(NoSocketsTestCase):
    def test_should_return_audit_data_for_users_and_mains_only(self):
        # given
        corporation = EveCorporationInfoFactory()
        my_filter = CorporationTitleFilterFactory(
            corporations=[corporation, EveCorporationInfoFactory()],
            title="Alpha",
            include_alts=False,
        )

        main_1 = EveCharacterFactory(
            corporation=corporation, character_name="Bruce Wayne"
        )
        user_1 = UserMainBasicAccessFactory(main_character__character=main_1)
        character_11 = CharacterFactory(user=user_1)
        CharacterTitleFactory(character=character_11, name="Alpha")
        alt_1 = EveCharacterFactory(corporation=corporation)
        character_12 = CharacterFactory(user=user_1, is_main=False, alt_character=alt_1)
        CharacterTitleFactory(character=character_12, name="Alpha")

        user_2 = UserMainBasicAccessFactory()
        alt_2 = EveCharacterFactory(corporation=corporation)
        character_2 = CharacterFactory(user=user_2, is_main=False, alt_character=alt_2)
        CharacterTitleFactory(character=character_2, name="Alpha")

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
        corporation = EveCorporationInfoFactory()
        my_filter = CorporationTitleFilterFactory(
            corporations=[corporation, EveCorporationInfoFactory()],
            title="Alpha",
            include_alts=True,
        )

        main_1 = EveCharacterFactory(
            corporation=corporation, character_name="Bruce Wayne"
        )
        user_1 = UserMainBasicAccessFactory(main_character__character=main_1)
        character_11 = CharacterFactory(user=user_1)
        CharacterTitleFactory(character=character_11, name="Alpha")
        alt_1 = EveCharacterFactory(corporation=corporation)
        character_12 = CharacterFactory(user=user_1, is_main=False, alt_character=alt_1)
        CharacterTitleFactory(character=character_12, name="Alpha")

        user_2 = UserMainBasicAccessFactory()
        alt_2 = EveCharacterFactory(corporation=corporation)
        character_2 = CharacterFactory(user=user_2, is_main=False, alt_character=alt_2)
        CharacterTitleFactory(character=character_2, name="Alpha")

        user_3 = UserMainBasicAccessFactory()

        # when
        users = make_user_queryset(user_1, user_2, user_3)
        result = my_filter.audit_filter(users)

        # then
        self.assertEqual(len(result), 3)
        self.assertTrue(result[user_1.id]["check"])
        self.assertTrue(result[user_2.id]["check"])
        self.assertFalse(result[user_3.id]["check"])
