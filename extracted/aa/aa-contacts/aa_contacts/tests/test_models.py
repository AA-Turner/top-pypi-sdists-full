from django.test import TestCase
from django.contrib.auth.models import User

from app_utils.testdata_factories import UserMainFactory, EveCorporationInfoFactory, EveAllianceInfoFactory, EveCharacterFactory
from app_utils.testing import add_character_to_user

from aa_contacts.models import StandingFilter, AllianceContact, CorporationContact


class TestStandingFilter(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.corp_red = EveCorporationInfoFactory()
        cls.corp_blue = EveCorporationInfoFactory()
        cls.alliance_red = EveAllianceInfoFactory()
        cls.alliance_blue = EveAllianceInfoFactory()
        corp_in_red = EveCorporationInfoFactory(alliance=cls.alliance_red)
        corp_in_blue = EveCorporationInfoFactory(alliance=cls.alliance_blue)

        cls.char_red_corp = EveCharacterFactory(corporation=cls.corp_red)
        cls.char_blue_corp = EveCharacterFactory(corporation=cls.corp_blue)
        cls.char_red_alliance = EveCharacterFactory(corporation=corp_in_red)
        cls.char_blue_alliance = EveCharacterFactory(corporation=corp_in_blue)

        cls.user = UserMainFactory()

        cls.corp_user = cls.user.profile.main_character.corporation
        cls.alliance_user = cls.user.profile.main_character.alliance

        AllianceContact.objects.bulk_create([
            AllianceContact(
                alliance=cls.alliance_user,
                contact_id=cls.alliance_red.alliance_id,
                contact_type=AllianceContact.ContactTypeOptions.ALLIANCE,
                standing=-10.0,
            ),
            AllianceContact(
                alliance=cls.alliance_user,
                contact_id=cls.alliance_blue.alliance_id,
                contact_type=AllianceContact.ContactTypeOptions.ALLIANCE,
                standing=10.0,
            ),
        ])

        CorporationContact.objects.bulk_create([
            CorporationContact(
                corporation=cls.corp_user,
                contact_id=cls.corp_red.corporation_id,
                contact_type=CorporationContact.ContactTypeOptions.CORPORATION,
                standing=-10.0,
            ),
            CorporationContact(
                corporation=cls.corp_user,
                contact_id=cls.corp_blue.corporation_id,
                contact_type=CorporationContact.ContactTypeOptions.CORPORATION,
                standing=10.0,
            ),
        ])

    def test_str(self):
        filter = StandingFilter.objects.create(
            name='Test Filter',
            description='Test Description',
            comparison=StandingFilter.ComparisonOptions.GREATER_THAN,
            standing=0.0,
        )
        self.assertEqual(str(filter), 'Test Filter: Test Description')

    def test_audit_filter_at_least_one_all_chars(self):
        filter = StandingFilter.objects.create(
            name='Test Filter',
            description='Test Description',
            comparison=StandingFilter.ComparisonOptions.GREATER_THAN,
            standing=0.0,
            check_type=StandingFilter.CheckTypeOptions.AT_LEAST_ONE_CHARACTER,
        )
        filter.alliances.add(self.alliance_user)

        filter_red = StandingFilter.objects.create(
            name='Test Filter Red',
            description='Test Description Red',
            comparison=StandingFilter.ComparisonOptions.LESS_THAN,
            standing=-5.0,
            check_type=StandingFilter.CheckTypeOptions.AT_LEAST_ONE_CHARACTER,
        )
        filter_red.alliances.add(self.alliance_user)

        user_blue_and_red = UserMainFactory(main_character__character=self.char_red_alliance)
        add_character_to_user(user_blue_and_red, self.char_blue_alliance)

        self.assertTrue(filter.audit_filter(
            User.objects.filter(pk=user_blue_and_red.pk)
        )[user_blue_and_red.pk]['check'])

        self.assertTrue(filter_red.audit_filter(
            User.objects.filter(pk=user_blue_and_red.pk)
        )[user_blue_and_red.pk]['check'])

        user_blue = UserMainFactory(main_character__character=self.char_blue_alliance)

        self.assertTrue(filter.audit_filter(
            User.objects.filter(pk=user_blue.pk)
        )[user_blue.pk]['check'])

        self.assertFalse(filter_red.audit_filter(
            User.objects.filter(pk=user_blue.pk)
        )[user_blue.pk]['check'])

    def test_audit_filter_at_least_one_only_main(self):
        filter = StandingFilter.objects.create(
            name='Test Filter',
            description='Test Description',
            comparison=StandingFilter.ComparisonOptions.GREATER_THAN,
            standing=0.0,
            check_type=StandingFilter.CheckTypeOptions.AT_LEAST_ONE_CHARACTER,
            only_main=True,
        )
        filter.alliances.add(self.alliance_user)

        filter_red = StandingFilter.objects.create(
            name='Test Filter Red',
            description='Test Description Red',
            comparison=StandingFilter.ComparisonOptions.LESS_THAN,
            standing=-5.0,
            check_type=StandingFilter.CheckTypeOptions.AT_LEAST_ONE_CHARACTER,
            only_main=True,
        )
        filter_red.alliances.add(self.alliance_user)

        user_blue_and_red = UserMainFactory(main_character__character=self.char_red_alliance)
        add_character_to_user(user_blue_and_red, self.char_blue_alliance)

        self.assertFalse(filter.audit_filter(
            User.objects.filter(pk=user_blue_and_red.pk)
        )[user_blue_and_red.pk]['check'])

        self.assertTrue(filter_red.audit_filter(
            User.objects.filter(pk=user_blue_and_red.pk)
        )[user_blue_and_red.pk]['check'])

    def test_audit_filter_all_characters_all_chars(self):
        filter = StandingFilter.objects.create(
            name='Test Filter',
            description='Test Description',
            comparison=StandingFilter.ComparisonOptions.GREATER_THAN,
            standing=0.0,
            check_type=StandingFilter.CheckTypeOptions.ALL_CHARACTERS,
        )
        filter.alliances.add(self.alliance_user)
        filter.corporations.add(self.corp_user)

        filter_red = StandingFilter.objects.create(
            name='Test Filter Red',
            description='Test Description Red',
            comparison=StandingFilter.ComparisonOptions.LESS_THAN,
            standing=-5.0,
            check_type=StandingFilter.CheckTypeOptions.ALL_CHARACTERS,
        )
        filter_red.alliances.add(self.alliance_user)
        filter_red.corporations.add(self.corp_user)

        user_blue_and_red = UserMainFactory(main_character__character=self.char_red_alliance)
        add_character_to_user(user_blue_and_red, self.char_blue_alliance)

        self.assertFalse(filter.audit_filter(
            User.objects.filter(pk=user_blue_and_red.pk)
        )[user_blue_and_red.pk]['check'])

        self.assertFalse(filter_red.audit_filter(
            User.objects.filter(pk=user_blue_and_red.pk)
        )[user_blue_and_red.pk]['check'])

        user_blue = UserMainFactory(main_character__character=self.char_blue_alliance)
        add_character_to_user(user_blue, self.char_blue_corp)

        self.assertTrue(filter.audit_filter(
            User.objects.filter(pk=user_blue.pk)
        )[user_blue.pk]['check'])

        self.assertFalse(filter_red.audit_filter(
            User.objects.filter(pk=user_blue.pk)
        )[user_blue.pk]['check'])

        user_red = UserMainFactory(main_character__character=self.char_red_alliance)
        add_character_to_user(user_red, self.char_red_corp)

        self.assertFalse(filter.audit_filter(
            User.objects.filter(pk=user_red.pk)
        )[user_red.pk]['check'])

        self.assertTrue(filter_red.audit_filter(
            User.objects.filter(pk=user_red.pk)
        )[user_red.pk]['check'])

    def test_audit_filter_all_characters_only_main(self):
        filter = StandingFilter.objects.create(
            name='Test Filter',
            description='Test Description',
            comparison=StandingFilter.ComparisonOptions.GREATER_THAN,
            standing=0.0,
            check_type=StandingFilter.CheckTypeOptions.ALL_CHARACTERS,
            only_main=True,
        )
        filter.alliances.add(self.alliance_user)
        filter.corporations.add(self.corp_user)

        filter_red = StandingFilter.objects.create(
            name='Test Filter Red',
            description='Test Description Red',
            comparison=StandingFilter.ComparisonOptions.LESS_THAN,
            standing=-5.0,
            check_type=StandingFilter.CheckTypeOptions.ALL_CHARACTERS,
            only_main=True,
        )
        filter_red.alliances.add(self.alliance_user)
        filter_red.corporations.add(self.corp_user)

        user_blue_and_red = UserMainFactory(main_character__character=self.char_red_alliance)
        add_character_to_user(user_blue_and_red, self.char_blue_alliance)

        self.assertFalse(filter.audit_filter(
            User.objects.filter(pk=user_blue_and_red.pk)
        )[user_blue_and_red.pk]['check'])

        self.assertTrue(filter_red.audit_filter(
            User.objects.filter(pk=user_blue_and_red.pk)
        )[user_blue_and_red.pk]['check'])

        user_blue = UserMainFactory(main_character__character=self.char_blue_alliance)
        add_character_to_user(user_blue, self.char_red_corp)

        self.assertTrue(filter.audit_filter(
            User.objects.filter(pk=user_blue.pk)
        )[user_blue.pk]['check'])

        self.assertFalse(filter_red.audit_filter(
            User.objects.filter(pk=user_blue.pk)
        )[user_blue.pk]['check'])

    def test_audit_filter_no_character_all_chars(self):
        filter = StandingFilter.objects.create(
            name='Test Filter',
            description='Test Description',
            comparison=StandingFilter.ComparisonOptions.GREATER_THAN,
            standing=0.0,
            check_type=StandingFilter.CheckTypeOptions.NO_CHARACTER,
        )
        filter.alliances.add(self.alliance_user)
        filter.corporations.add(self.corp_user)

        filter_red = StandingFilter.objects.create(
            name='Test Filter Red',
            description='Test Description Red',
            comparison=StandingFilter.ComparisonOptions.LESS_THAN,
            standing=-5.0,
            check_type=StandingFilter.CheckTypeOptions.NO_CHARACTER,
        )
        filter_red.alliances.add(self.alliance_user)
        filter_red.corporations.add(self.corp_user)

        user_blue_and_red = UserMainFactory(main_character__character=self.char_red_alliance)
        add_character_to_user(user_blue_and_red, self.char_blue_alliance)

        self.assertFalse(filter.audit_filter(
            User.objects.filter(pk=user_blue_and_red.pk)
        )[user_blue_and_red.pk]['check'])

        self.assertFalse(filter_red.audit_filter(
            User.objects.filter(pk=user_blue_and_red.pk)
        )[user_blue_and_red.pk]['check'])

        user_blue = UserMainFactory(main_character__character=self.char_blue_alliance)
        add_character_to_user(user_blue, self.char_blue_corp)

        self.assertFalse(filter.audit_filter(
            User.objects.filter(pk=user_blue.pk)
        )[user_blue.pk]['check'])

        self.assertTrue(filter_red.audit_filter(
            User.objects.filter(pk=user_blue.pk)
        )[user_blue.pk]['check'])

        user_red = UserMainFactory(main_character__character=self.char_red_alliance)
        add_character_to_user(user_red, self.char_red_corp)

        self.assertTrue(filter.audit_filter(
            User.objects.filter(pk=user_red.pk)
        )[user_red.pk]['check'])

        self.assertFalse(filter_red.audit_filter(
            User.objects.filter(pk=user_red.pk)
        )[user_red.pk]['check'])

    def test_audit_filter_no_characters_only_main(self):
        filter = StandingFilter.objects.create(
            name='Test Filter',
            description='Test Description',
            comparison=StandingFilter.ComparisonOptions.GREATER_THAN,
            standing=0.0,
            check_type=StandingFilter.CheckTypeOptions.NO_CHARACTER,
            only_main=True,
        )
        filter.alliances.add(self.alliance_user)
        filter.corporations.add(self.corp_user)

        filter_red = StandingFilter.objects.create(
            name='Test Filter Red',
            description='Test Description Red',
            comparison=StandingFilter.ComparisonOptions.LESS_THAN,
            standing=-5.0,
            check_type=StandingFilter.CheckTypeOptions.NO_CHARACTER,
            only_main=True,
        )
        filter_red.alliances.add(self.alliance_user)
        filter_red.corporations.add(self.corp_user)

        user_blue_and_red = UserMainFactory(main_character__character=self.char_red_alliance)
        add_character_to_user(user_blue_and_red, self.char_blue_alliance)

        self.assertTrue(filter.audit_filter(
            User.objects.filter(pk=user_blue_and_red.pk)
        )[user_blue_and_red.pk]['check'])

        self.assertFalse(filter_red.audit_filter(
            User.objects.filter(pk=user_blue_and_red.pk)
        )[user_blue_and_red.pk]['check'])
