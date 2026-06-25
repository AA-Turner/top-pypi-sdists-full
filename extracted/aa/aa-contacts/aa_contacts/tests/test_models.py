from typing import ClassVar
from unittest import mock

from allianceauth.eveonline.models import (
    EveAllianceInfo,
    EveCharacter,
    EveCorporationInfo,
    EveFactionInfo,
)
from app_utils.testdata_factories import (
    EveAllianceInfoFactory,
    EveCharacterFactory,
    EveCorporationInfoFactory,
    UserMainFactory,
)
from app_utils.testing import add_character_to_user
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.test import SimpleTestCase, TestCase

from aa_contacts.models import (
    AllianceContact,
    AnySchemeURLField,
    AnySchemeURLValidator,
    Contact,
    CorporationContact,
    StandingFilter,
)


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

        AllianceContact.objects.bulk_create(
            [
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
            ]
        )

        CorporationContact.objects.bulk_create(
            [
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
            ]
        )

    def test_str(self):
        standing_filter = StandingFilter.objects.create(
            name="Test Filter",
            description="Test Description",
            comparison=StandingFilter.ComparisonOptions.GREATER_THAN,
            standing=0.0,
        )
        self.assertEqual(str(standing_filter), "Test Filter: Test Description")

    def test_standing_lookup(self):
        cases = [
            (StandingFilter.ComparisonOptions.GREATER_THAN, Q(standing__gt=2.5)),
            (StandingFilter.ComparisonOptions.GREATER_OR_EQUAL, Q(standing__gte=2.5)),
            (StandingFilter.ComparisonOptions.LESS_THAN, Q(standing__lt=2.5)),
            (StandingFilter.ComparisonOptions.LESS_OR_EQUAL, Q(standing__lte=2.5)),
            (StandingFilter.ComparisonOptions.EQUAL, Q(standing=2.5)),
        ]
        for comparison, expected in cases:
            with self.subTest(comparison=comparison):
                standing_filter = StandingFilter(comparison=comparison, standing=2.5)
                self.assertEqual(standing_filter._standing_lookup, expected)

    def test_audit_filter_at_least_one_all_chars(self):
        standing_filter = StandingFilter.objects.create(
            name="Test Filter",
            description="Test Description",
            comparison=StandingFilter.ComparisonOptions.GREATER_THAN,
            standing=0.0,
            check_type=StandingFilter.CheckTypeOptions.AT_LEAST_ONE_CHARACTER,
        )
        standing_filter.alliances.add(self.alliance_user)

        filter_red = StandingFilter.objects.create(
            name="Test Filter Red",
            description="Test Description Red",
            comparison=StandingFilter.ComparisonOptions.LESS_THAN,
            standing=-5.0,
            check_type=StandingFilter.CheckTypeOptions.AT_LEAST_ONE_CHARACTER,
        )
        filter_red.alliances.add(self.alliance_user)

        user_blue_and_red = UserMainFactory(
            main_character__character=self.char_red_alliance
        )
        add_character_to_user(user_blue_and_red, self.char_blue_alliance)

        self.assertTrue(
            standing_filter.audit_filter(
                User.objects.filter(pk=user_blue_and_red.pk),
            )[user_blue_and_red.pk]["check"]
        )

        self.assertTrue(
            filter_red.audit_filter(
                User.objects.filter(pk=user_blue_and_red.pk),
            )[user_blue_and_red.pk]["check"]
        )

        user_blue = UserMainFactory(main_character__character=self.char_blue_alliance)

        self.assertTrue(
            standing_filter.audit_filter(
                User.objects.filter(pk=user_blue.pk),
            )[user_blue.pk]["check"]
        )

        self.assertFalse(
            filter_red.audit_filter(
                User.objects.filter(pk=user_blue.pk),
            )[user_blue.pk]["check"]
        )

    def test_audit_filter_at_least_one_only_main(self):
        standing_filter = StandingFilter.objects.create(
            name="Test Filter",
            description="Test Description",
            comparison=StandingFilter.ComparisonOptions.GREATER_THAN,
            standing=0.0,
            check_type=StandingFilter.CheckTypeOptions.AT_LEAST_ONE_CHARACTER,
            only_main=True,
        )
        standing_filter.alliances.add(self.alliance_user)

        filter_red = StandingFilter.objects.create(
            name="Test Filter Red",
            description="Test Description Red",
            comparison=StandingFilter.ComparisonOptions.LESS_THAN,
            standing=-5.0,
            check_type=StandingFilter.CheckTypeOptions.AT_LEAST_ONE_CHARACTER,
            only_main=True,
        )
        filter_red.alliances.add(self.alliance_user)

        user_blue_and_red = UserMainFactory(
            main_character__character=self.char_red_alliance
        )
        add_character_to_user(user_blue_and_red, self.char_blue_alliance)

        self.assertFalse(
            standing_filter.audit_filter(
                User.objects.filter(pk=user_blue_and_red.pk),
            )[user_blue_and_red.pk]["check"]
        )

        self.assertTrue(
            filter_red.audit_filter(
                User.objects.filter(pk=user_blue_and_red.pk),
            )[user_blue_and_red.pk]["check"]
        )

    def test_audit_filter_all_characters_all_chars(self):
        standing_filter = StandingFilter.objects.create(
            name="Test Filter",
            description="Test Description",
            comparison=StandingFilter.ComparisonOptions.GREATER_THAN,
            standing=0.0,
            check_type=StandingFilter.CheckTypeOptions.ALL_CHARACTERS,
        )
        standing_filter.alliances.add(self.alliance_user)
        standing_filter.corporations.add(self.corp_user)

        filter_red = StandingFilter.objects.create(
            name="Test Filter Red",
            description="Test Description Red",
            comparison=StandingFilter.ComparisonOptions.LESS_THAN,
            standing=-5.0,
            check_type=StandingFilter.CheckTypeOptions.ALL_CHARACTERS,
        )
        filter_red.alliances.add(self.alliance_user)
        filter_red.corporations.add(self.corp_user)

        user_blue_and_red = UserMainFactory(
            main_character__character=self.char_red_alliance
        )
        add_character_to_user(user_blue_and_red, self.char_blue_alliance)

        self.assertFalse(
            standing_filter.audit_filter(
                User.objects.filter(pk=user_blue_and_red.pk),
            )[user_blue_and_red.pk]["check"]
        )

        self.assertFalse(
            filter_red.audit_filter(
                User.objects.filter(pk=user_blue_and_red.pk),
            )[user_blue_and_red.pk]["check"]
        )

        user_blue = UserMainFactory(main_character__character=self.char_blue_alliance)
        add_character_to_user(user_blue, self.char_blue_corp)

        self.assertTrue(
            standing_filter.audit_filter(
                User.objects.filter(pk=user_blue.pk),
            )[user_blue.pk]["check"]
        )

        self.assertFalse(
            filter_red.audit_filter(
                User.objects.filter(pk=user_blue.pk),
            )[user_blue.pk]["check"]
        )

        user_red = UserMainFactory(main_character__character=self.char_red_alliance)
        add_character_to_user(user_red, self.char_red_corp)

        self.assertFalse(
            standing_filter.audit_filter(
                User.objects.filter(pk=user_red.pk),
            )[user_red.pk]["check"]
        )

        self.assertTrue(
            filter_red.audit_filter(
                User.objects.filter(pk=user_red.pk),
            )[user_red.pk]["check"]
        )

    def test_audit_filter_all_characters_only_main(self):
        standing_filter = StandingFilter.objects.create(
            name="Test Filter",
            description="Test Description",
            comparison=StandingFilter.ComparisonOptions.GREATER_THAN,
            standing=0.0,
            check_type=StandingFilter.CheckTypeOptions.ALL_CHARACTERS,
            only_main=True,
        )
        standing_filter.alliances.add(self.alliance_user)
        standing_filter.corporations.add(self.corp_user)

        filter_red = StandingFilter.objects.create(
            name="Test Filter Red",
            description="Test Description Red",
            comparison=StandingFilter.ComparisonOptions.LESS_THAN,
            standing=-5.0,
            check_type=StandingFilter.CheckTypeOptions.ALL_CHARACTERS,
            only_main=True,
        )
        filter_red.alliances.add(self.alliance_user)
        filter_red.corporations.add(self.corp_user)

        user_blue_and_red = UserMainFactory(
            main_character__character=self.char_red_alliance
        )
        add_character_to_user(user_blue_and_red, self.char_blue_alliance)

        self.assertFalse(
            standing_filter.audit_filter(
                User.objects.filter(pk=user_blue_and_red.pk),
            )[user_blue_and_red.pk]["check"]
        )

        self.assertTrue(
            filter_red.audit_filter(
                User.objects.filter(pk=user_blue_and_red.pk),
            )[user_blue_and_red.pk]["check"]
        )

        user_blue = UserMainFactory(main_character__character=self.char_blue_alliance)
        add_character_to_user(user_blue, self.char_red_corp)

        self.assertTrue(
            standing_filter.audit_filter(
                User.objects.filter(pk=user_blue.pk),
            )[user_blue.pk]["check"]
        )

        self.assertFalse(
            filter_red.audit_filter(
                User.objects.filter(pk=user_blue.pk),
            )[user_blue.pk]["check"]
        )

    def test_audit_filter_no_character_all_chars(self):
        standing_filter = StandingFilter.objects.create(
            name="Test Filter",
            description="Test Description",
            comparison=StandingFilter.ComparisonOptions.GREATER_THAN,
            standing=0.0,
            check_type=StandingFilter.CheckTypeOptions.NO_CHARACTER,
        )
        standing_filter.alliances.add(self.alliance_user)
        standing_filter.corporations.add(self.corp_user)

        filter_red = StandingFilter.objects.create(
            name="Test Filter Red",
            description="Test Description Red",
            comparison=StandingFilter.ComparisonOptions.LESS_THAN,
            standing=-5.0,
            check_type=StandingFilter.CheckTypeOptions.NO_CHARACTER,
        )
        filter_red.alliances.add(self.alliance_user)
        filter_red.corporations.add(self.corp_user)

        user_blue_and_red = UserMainFactory(
            main_character__character=self.char_red_alliance
        )
        add_character_to_user(user_blue_and_red, self.char_blue_alliance)

        self.assertFalse(
            standing_filter.audit_filter(
                User.objects.filter(pk=user_blue_and_red.pk),
            )[user_blue_and_red.pk]["check"]
        )

        self.assertFalse(
            filter_red.audit_filter(
                User.objects.filter(pk=user_blue_and_red.pk),
            )[user_blue_and_red.pk]["check"]
        )

        user_blue = UserMainFactory(main_character__character=self.char_blue_alliance)
        add_character_to_user(user_blue, self.char_blue_corp)

        self.assertFalse(
            standing_filter.audit_filter(
                User.objects.filter(pk=user_blue.pk),
            )[user_blue.pk]["check"]
        )

        self.assertTrue(
            filter_red.audit_filter(
                User.objects.filter(pk=user_blue.pk),
            )[user_blue.pk]["check"]
        )

        user_red = UserMainFactory(main_character__character=self.char_red_alliance)
        add_character_to_user(user_red, self.char_red_corp)

        self.assertTrue(
            standing_filter.audit_filter(
                User.objects.filter(pk=user_red.pk),
            )[user_red.pk]["check"]
        )

        self.assertFalse(
            filter_red.audit_filter(
                User.objects.filter(pk=user_red.pk),
            )[user_red.pk]["check"]
        )

    def test_audit_filter_no_characters_only_main(self):
        standing_filter = StandingFilter.objects.create(
            name="Test Filter",
            description="Test Description",
            comparison=StandingFilter.ComparisonOptions.GREATER_THAN,
            standing=0.0,
            check_type=StandingFilter.CheckTypeOptions.NO_CHARACTER,
            only_main=True,
        )
        standing_filter.alliances.add(self.alliance_user)
        standing_filter.corporations.add(self.corp_user)

        filter_red = StandingFilter.objects.create(
            name="Test Filter Red",
            description="Test Description Red",
            comparison=StandingFilter.ComparisonOptions.LESS_THAN,
            standing=-5.0,
            check_type=StandingFilter.CheckTypeOptions.NO_CHARACTER,
            only_main=True,
        )
        filter_red.alliances.add(self.alliance_user)
        filter_red.corporations.add(self.corp_user)

        user_blue_and_red = UserMainFactory(
            main_character__character=self.char_red_alliance
        )
        add_character_to_user(user_blue_and_red, self.char_blue_alliance)

        self.assertTrue(
            standing_filter.audit_filter(
                User.objects.filter(pk=user_blue_and_red.pk),
            )[user_blue_and_red.pk]["check"]
        )

        self.assertFalse(
            filter_red.audit_filter(
                User.objects.filter(pk=user_blue_and_red.pk),
            )[user_blue_and_red.pk]["check"]
        )


class TestContactImageSrc(TestCase):
    """``Contact.image_src`` returns the right CDN URL per contact type."""

    @staticmethod
    def _contact(contact_type, contact_id):
        # Unsaved instance is enough: ``image_src`` only reads type and id.
        return AllianceContact(contact_type=contact_type, contact_id=contact_id)

    def test_character(self):
        contact = self._contact(Contact.ContactTypeOptions.CHARACTER, 95465499)
        self.assertEqual(contact.image_src, EveCharacter.generic_portrait_url(95465499))

    def test_corporation(self):
        contact = self._contact(Contact.ContactTypeOptions.CORPORATION, 98000001)
        self.assertEqual(
            contact.image_src, EveCorporationInfo.generic_logo_url(98000001)
        )

    def test_alliance(self):
        contact = self._contact(Contact.ContactTypeOptions.ALLIANCE, 99000001)
        self.assertEqual(contact.image_src, EveAllianceInfo.generic_logo_url(99000001))

    def test_faction(self):
        contact = self._contact(Contact.ContactTypeOptions.FACTION, 500001)
        self.assertEqual(contact.image_src, EveFactionInfo.generic_logo_url(500001))

    def test_unknown_type_returns_empty_string(self):
        contact = self._contact("unknown", 1)
        self.assertEqual(contact.image_src, "")


class TestContactName(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.alliance = EveAllianceInfoFactory()

    def _contact(self, contact_type, contact_id):
        return AllianceContact.objects.create(
            alliance=self.alliance,
            contact_type=contact_type,
            contact_id=contact_id,
            standing=0.0,
        )

    def test_load_contact_name_character(self):
        char = EveCharacterFactory()
        contact = self._contact(Contact.ContactTypeOptions.CHARACTER, char.character_id)
        self.assertEqual(contact._load_contact_name, char.character_name)

    def test_load_contact_name_corporation(self):
        corp = EveCorporationInfoFactory()
        contact = self._contact(
            Contact.ContactTypeOptions.CORPORATION, corp.corporation_id
        )
        self.assertEqual(contact._load_contact_name, corp.corporation_name)

    def test_load_contact_name_alliance(self):
        alliance = EveAllianceInfoFactory()
        contact = self._contact(
            Contact.ContactTypeOptions.ALLIANCE, alliance.alliance_id
        )
        self.assertEqual(contact._load_contact_name, alliance.alliance_name)

    def test_load_contact_name_faction(self):
        faction = EveFactionInfo.objects.create(
            faction_id=500001, faction_name="Caldari State"
        )
        contact = self._contact(Contact.ContactTypeOptions.FACTION, faction.faction_id)
        self.assertEqual(contact._load_contact_name, faction.faction_name)

    def test_load_contact_name_unknown_type_raises(self):
        contact = self._contact("unknown", 1)
        with self.assertRaises(ValueError):
            _ = contact._load_contact_name

    @mock.patch("aa_contacts.models.EveCharacter.objects.create_character")
    def test_load_contact_name_creates_missing_character(self, mock_create):
        mock_create.return_value = mock.Mock(character_name="Fetched Name")
        contact = self._contact(Contact.ContactTypeOptions.CHARACTER, 1_999_999_001)
        self.assertEqual(contact._load_contact_name, "Fetched Name")
        mock_create.assert_called_once_with(1_999_999_001)

    @mock.patch("aa_contacts.models.EveCorporationInfo.objects.create_corporation")
    def test_load_contact_name_creates_missing_corporation(self, mock_create):
        mock_create.return_value = mock.Mock(corporation_name="Fetched Corp")
        contact = self._contact(Contact.ContactTypeOptions.CORPORATION, 1_999_999_002)
        self.assertEqual(contact._load_contact_name, "Fetched Corp")
        mock_create.assert_called_once_with(1_999_999_002)

    @mock.patch("aa_contacts.models.EveAllianceInfo.objects.create_alliance")
    def test_load_contact_name_creates_missing_alliance(self, mock_create):
        mock_create.return_value = mock.Mock(alliance_name="Fetched Alliance")
        contact = self._contact(Contact.ContactTypeOptions.ALLIANCE, 1_999_999_003)
        self.assertEqual(contact._load_contact_name, "Fetched Alliance")
        mock_create.assert_called_once_with(1_999_999_003)

    @mock.patch("aa_contacts.models.EveFactionInfo.objects.create_faction")
    def test_load_contact_name_creates_missing_faction(self, mock_create):
        mock_create.return_value = mock.Mock(faction_name="Fetched Faction")
        contact = self._contact(Contact.ContactTypeOptions.FACTION, 1_999_999_004)
        self.assertEqual(contact._load_contact_name, "Fetched Faction")
        mock_create.assert_called_once_with(1_999_999_004)

    def test_contact_name_prefers_annotation(self):
        char = EveCharacterFactory()
        contact = AllianceContact(
            contact_type=Contact.ContactTypeOptions.CHARACTER,
            contact_id=char.character_id,
        )
        contact.contact_name_annotation = "Annotated Name"
        self.assertEqual(contact.contact_name, "Annotated Name")

    def test_contact_name_falls_back_when_annotation_empty(self):
        char = EveCharacterFactory()
        contact = AllianceContact(
            contact_type=Contact.ContactTypeOptions.CHARACTER,
            contact_id=char.character_id,
        )
        contact.contact_name_annotation = ""
        self.assertEqual(contact.contact_name, char.character_name)

    def test_contact_name_falls_back_without_annotation(self):
        char = EveCharacterFactory()
        contact = AllianceContact(
            contact_type=Contact.ContactTypeOptions.CHARACTER,
            contact_id=char.character_id,
        )
        self.assertEqual(contact.contact_name, char.character_name)

    def test_with_contact_name_populates_annotation(self):
        char = EveCharacterFactory()
        self._contact(Contact.ContactTypeOptions.CHARACTER, char.character_id)
        contact = AllianceContact.objects.with_contact_name().get(
            contact_id=char.character_id
        )
        self.assertEqual(contact.contact_name_annotation, char.character_name)
        self.assertEqual(contact.contact_name, char.character_name)


class TestFilterMissingContactName(TestCase):
    """``filter_missing_contact_name`` flags contacts with no eve object."""

    @classmethod
    def setUpTestData(cls):
        cls.alliance = EveAllianceInfoFactory()

    def _contact(self, contact_type, contact_id):
        return AllianceContact.objects.create(
            alliance=self.alliance,
            contact_type=contact_type,
            contact_id=contact_id,
            standing=0.0,
        )

    def test_returns_only_contacts_without_eve_object(self):
        char = EveCharacterFactory()
        corp = EveCorporationInfoFactory()

        existing_char = self._contact(
            Contact.ContactTypeOptions.CHARACTER, char.character_id
        )
        existing_corp = self._contact(
            Contact.ContactTypeOptions.CORPORATION, corp.corporation_id
        )
        missing_char = self._contact(
            Contact.ContactTypeOptions.CHARACTER, 1_999_999_001
        )
        missing_alliance = self._contact(
            Contact.ContactTypeOptions.ALLIANCE, 1_999_999_002
        )

        result = AllianceContact.filter_missing_contact_name(
            [
                existing_char.pk,
                existing_corp.pk,
                missing_char.pk,
                missing_alliance.pk,
            ]
        )

        self.assertCountEqual(result, [missing_char.pk, missing_alliance.pk])

    def test_empty_input_returns_empty_list(self):
        self.assertEqual(AllianceContact.filter_missing_contact_name([]), [])


class TestAllianceContactPermissions(TestCase):
    def test_can_view_notes(self):
        self.assertTrue(
            AllianceContact.can_view_notes(
                UserMainFactory(permissions=["aa_contacts.view_alliance_notes"])
            )
        )
        self.assertFalse(AllianceContact.can_view_notes(UserMainFactory()))

    def test_can_edit_notes_requires_manage_and_view(self):
        full = UserMainFactory(
            permissions=[
                "aa_contacts.manage_alliance_contacts",
                "aa_contacts.view_alliance_notes",
            ]
        )
        self.assertTrue(AllianceContact.can_edit_notes(full))

        manage_only = UserMainFactory(
            permissions=["aa_contacts.manage_alliance_contacts"]
        )
        self.assertFalse(AllianceContact.can_edit_notes(manage_only))

        view_only = UserMainFactory(permissions=["aa_contacts.view_alliance_notes"])
        self.assertFalse(AllianceContact.can_edit_notes(view_only))

    def test_can_view_server_links(self):
        self.assertTrue(
            AllianceContact.can_view_server_links(
                UserMainFactory(permissions=["aa_contacts.view_alliance_server_links"])
            )
        )
        self.assertFalse(AllianceContact.can_view_server_links(UserMainFactory()))

    def test_can_manage_server_links_requires_manage_and_view(self):
        full = UserMainFactory(
            permissions=[
                "aa_contacts.manage_alliance_contacts",
                "aa_contacts.view_alliance_server_links",
            ]
        )
        self.assertTrue(AllianceContact.can_manage_server_links(full))

        manage_only = UserMainFactory(
            permissions=["aa_contacts.manage_alliance_contacts"]
        )
        self.assertFalse(AllianceContact.can_manage_server_links(manage_only))

        view_only = UserMainFactory(
            permissions=["aa_contacts.view_alliance_server_links"]
        )
        self.assertFalse(AllianceContact.can_manage_server_links(view_only))


class TestCorporationContactPermissions(TestCase):
    def test_can_view_notes(self):
        self.assertTrue(
            CorporationContact.can_view_notes(
                UserMainFactory(permissions=["aa_contacts.view_corporation_notes"])
            )
        )
        self.assertFalse(CorporationContact.can_view_notes(UserMainFactory()))

    def test_can_edit_notes_requires_manage_and_view(self):
        full = UserMainFactory(
            permissions=[
                "aa_contacts.manage_corporation_contacts",
                "aa_contacts.view_corporation_notes",
            ]
        )
        self.assertTrue(CorporationContact.can_edit_notes(full))

        manage_only = UserMainFactory(
            permissions=["aa_contacts.manage_corporation_contacts"]
        )
        self.assertFalse(CorporationContact.can_edit_notes(manage_only))

        view_only = UserMainFactory(permissions=["aa_contacts.view_corporation_notes"])
        self.assertFalse(CorporationContact.can_edit_notes(view_only))

    def test_can_view_server_links(self):
        self.assertTrue(
            CorporationContact.can_view_server_links(
                UserMainFactory(
                    permissions=["aa_contacts.view_corporation_server_links"]
                )
            )
        )
        self.assertFalse(CorporationContact.can_view_server_links(UserMainFactory()))

    def test_can_manage_server_links_requires_manage_and_view(self):
        full = UserMainFactory(
            permissions=[
                "aa_contacts.manage_corporation_contacts",
                "aa_contacts.view_corporation_server_links",
            ]
        )
        self.assertTrue(CorporationContact.can_manage_server_links(full))

        manage_only = UserMainFactory(
            permissions=["aa_contacts.manage_corporation_contacts"]
        )
        self.assertFalse(CorporationContact.can_manage_server_links(manage_only))

        view_only = UserMainFactory(
            permissions=["aa_contacts.view_corporation_server_links"]
        )
        self.assertFalse(CorporationContact.can_manage_server_links(view_only))


class TestContactBasePermissionsNotImplemented(TestCase):
    """The abstract ``Contact`` base leaves permission checks to subclasses."""

    def test_permission_methods_raise(self):
        user = UserMainFactory()
        for method in (
            Contact.can_view_notes,
            Contact.can_edit_notes,
            Contact.can_view_server_links,
            Contact.can_manage_server_links,
        ):
            with self.assertRaises(NotImplementedError):
                method(user)


class TestAnySchemeURLValidator(SimpleTestCase):
    """``AnySchemeURLValidator`` accepts any well-formed scheme but still
    rejects malformed URLs (it is used on the server link ``url`` field)."""

    VALID_URLS: ClassVar[list[str]] = [
        # Standard web schemes.
        "http://example.com",
        "https://example.com",
        "https://example.com:8080/path?query=1#frag",
        "https://192.168.1.1",
        "ftp://files.example.com",
        # Custom/non-default schemes a server link may legitimately use.
        "ts3server://ts.example.com",
        "mumble://mumble.example.com:64738",
        "discord://discord.gg/abc",
        "ventrilo://vent.example.com",
        # Scheme casing is normalised, not rejected.
        "HTTPS://example.com",
    ]

    INVALID_URLS: ClassVar[list[str]] = [
        "",
        "not a url",
        "example.com",
        "justtext",
        "https://",
        "http://",
        "://example.com",
        "https://exa mple.com",
    ]

    def setUp(self):
        self.validator = AnySchemeURLValidator()

    def test_accepts_valid_urls(self):
        for url in TestAnySchemeURLValidator.VALID_URLS:
            with self.subTest(url=url):
                self.validator(url)  # must not raise

    def test_rejects_invalid_urls(self):
        for url in TestAnySchemeURLValidator.INVALID_URLS:
            with self.subTest(url=url), self.assertRaises(ValidationError):
                self.validator(url)

    def test_field_uses_validator(self):
        self.assertTrue(
            any(
                isinstance(v, AnySchemeURLValidator)
                for v in AnySchemeURLField().default_validators
            )
        )
