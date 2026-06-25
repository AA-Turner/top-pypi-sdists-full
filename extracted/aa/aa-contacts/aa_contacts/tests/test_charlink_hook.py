from unittest import mock

from allianceauth.eveonline.models import EveCharacter
from app_utils.testdata_factories import (
    EveAllianceInfoFactory,
    EveCharacterFactory,
    EveCorporationInfoFactory,
    UserMainFactory,
)
from django.contrib.messages.storage.fallback import FallbackStorage
from django.test import RequestFactory, TestCase

from aa_contacts.charlink_hook import (
    _alliance_login,
    _alliance_users_with_perms,
    _corporation_login,
    _corporation_users_with_perms,
    alliance_scopes,
    app_import,
    corporation_scopes,
)
from aa_contacts.models import AllianceToken, CorporationToken


def _request_with_messages():
    """A request that the ``messages`` framework can write to."""
    request = RequestFactory().post("/")
    request.session = {}
    request._messages = FallbackStorage(request)
    return request


def _messages(request):
    return [str(m) for m in request._messages]


class TestAllianceLogin(TestCase):
    def setUp(self):
        self.request = _request_with_messages()

    @mock.patch("aa_contacts.charlink_hook.update_alliance_contacts.delay")
    def test_creates_token_and_triggers_update(self, mock_delay):
        user = UserMainFactory(main_character__scopes=alliance_scopes)
        token = user.token_set.first()
        alliance = user.profile.main_character.alliance

        _alliance_login(self.request, token)

        self.assertTrue(
            AllianceToken.objects.filter(alliance=alliance, token=token).exists()
        )
        mock_delay.assert_called_once_with(alliance.alliance_id)
        self.assertEqual(_messages(self.request), [])

    @mock.patch("aa_contacts.charlink_hook.update_alliance_contacts.delay")
    def test_character_without_alliance(self, mock_delay):
        char = EveCharacterFactory(corporation__create_alliance=False)
        user = UserMainFactory(
            main_character__character=char, main_character__scopes=alliance_scopes
        )
        token = user.token_set.first()

        with self.assertRaises(AssertionError):
            _alliance_login(self.request, token)

        self.assertEqual(AllianceToken.objects.count(), 0)
        mock_delay.assert_not_called()
        self.assertTrue(any("not in an alliance" in m for m in _messages(self.request)))

    @mock.patch("aa_contacts.charlink_hook.update_alliance_contacts.delay")
    def test_alliance_already_has_token(self, mock_delay):
        user = UserMainFactory(main_character__scopes=alliance_scopes)
        token = user.token_set.first()
        alliance = user.profile.main_character.alliance
        AllianceToken.objects.create(alliance=alliance, token=token)

        with self.assertRaises(AssertionError):
            _alliance_login(self.request, token)

        self.assertEqual(AllianceToken.objects.filter(alliance=alliance).count(), 1)
        mock_delay.assert_not_called()
        self.assertTrue(
            any("has a token already" in m for m in _messages(self.request))
        )

    @mock.patch("aa_contacts.charlink_hook.update_alliance_contacts.delay")
    @mock.patch("aa_contacts.charlink_hook.EveAllianceInfo.objects.create_alliance")
    def test_creates_missing_alliance(self, mock_create, mock_delay):
        new_alliance = EveAllianceInfoFactory()
        mock_create.return_value = new_alliance

        # ``alliance_id`` pointing at no existing ``EveAllianceInfo`` forces the
        # ``DoesNotExist`` fallback that fetches/creates it from ESI.
        char = EveCharacterFactory(corporation__create_alliance=False)
        char.alliance_id = 99_888_777
        char.save()
        user = UserMainFactory(
            main_character__character=char, main_character__scopes=alliance_scopes
        )
        token = user.token_set.first()

        _alliance_login(self.request, token)

        mock_create.assert_called_once_with(99_888_777)
        self.assertTrue(
            AllianceToken.objects.filter(alliance=new_alliance, token=token).exists()
        )
        mock_delay.assert_called_once_with(new_alliance.alliance_id)


class TestCorporationLogin(TestCase):
    def setUp(self):
        self.request = _request_with_messages()

    @mock.patch("aa_contacts.charlink_hook.update_corporation_contacts.delay")
    def test_creates_token_and_triggers_update(self, mock_delay):
        user = UserMainFactory(main_character__scopes=corporation_scopes)
        token = user.token_set.first()
        corporation = user.profile.main_character.corporation

        _corporation_login(self.request, token)

        self.assertTrue(
            CorporationToken.objects.filter(
                corporation=corporation, token=token
            ).exists()
        )
        mock_delay.assert_called_once_with(corporation.corporation_id)
        self.assertEqual(_messages(self.request), [])

    @mock.patch("aa_contacts.charlink_hook.update_corporation_contacts.delay")
    def test_corporation_already_has_token(self, mock_delay):
        user = UserMainFactory(main_character__scopes=corporation_scopes)
        token = user.token_set.first()
        corporation = user.profile.main_character.corporation
        CorporationToken.objects.create(corporation=corporation, token=token)

        with self.assertRaises(AssertionError):
            _corporation_login(self.request, token)

        self.assertEqual(
            CorporationToken.objects.filter(corporation=corporation).count(), 1
        )
        mock_delay.assert_not_called()
        self.assertTrue(
            any("has a token already" in m for m in _messages(self.request))
        )

    @mock.patch("aa_contacts.charlink_hook.update_corporation_contacts.delay")
    @mock.patch(
        "aa_contacts.charlink_hook.EveCorporationInfo.objects.create_corporation"
    )
    def test_creates_missing_corporation(self, mock_create, mock_delay):
        new_corp = EveCorporationInfoFactory()
        mock_create.return_value = new_corp

        char = EveCharacterFactory()
        char.corporation_id = 98_777_666
        char.save()
        user = UserMainFactory(
            main_character__character=char, main_character__scopes=corporation_scopes
        )
        token = user.token_set.first()

        _corporation_login(self.request, token)

        mock_create.assert_called_once_with(98_777_666)
        self.assertTrue(
            CorporationToken.objects.filter(corporation=new_corp, token=token).exists()
        )
        mock_delay.assert_called_once_with(new_corp.corporation_id)


class TestUsersWithPerms(TestCase):
    def test_alliance_users_with_perms(self):
        member = UserMainFactory(permissions=["aa_contacts.manage_alliance_contacts"])
        outsider = UserMainFactory()
        superuser = UserMainFactory(is_superuser=True)

        result = _alliance_users_with_perms()

        self.assertIn(member, result)
        self.assertIn(superuser, result)
        self.assertNotIn(outsider, result)

    def test_corporation_users_with_perms(self):
        member = UserMainFactory(
            permissions=["aa_contacts.manage_corporation_contacts"]
        )
        outsider = UserMainFactory()
        superuser = UserMainFactory(is_superuser=True)

        result = _corporation_users_with_perms()

        self.assertIn(member, result)
        self.assertIn(superuser, result)
        self.assertNotIn(outsider, result)


class TestAppImport(TestCase):
    def test_app_label_and_unique_ids(self):
        self.assertEqual(app_import.app_label, "aa_contacts")
        self.assertEqual(
            {import_.unique_id for import_ in app_import.imports},
            {"alliance", "corporation"},
        )

    def test_validate_import(self):
        # Raises ``AssertionError`` if the import is misconfigured.
        app_import.validate_import()

    def test_scopes(self):
        self.assertEqual(app_import.get("alliance").scopes, alliance_scopes)
        self.assertEqual(app_import.get("corporation").scopes, corporation_scopes)

    def test_alliance_check_permissions(self):
        import_ = app_import.get("alliance")
        member = UserMainFactory(permissions=["aa_contacts.manage_alliance_contacts"])
        outsider = UserMainFactory()

        self.assertTrue(import_.check_permissions(member))
        self.assertFalse(import_.check_permissions(outsider))

    def test_corporation_check_permissions(self):
        import_ = app_import.get("corporation")
        member = UserMainFactory(
            permissions=["aa_contacts.manage_corporation_contacts"]
        )
        outsider = UserMainFactory()

        self.assertTrue(import_.check_permissions(member))
        self.assertFalse(import_.check_permissions(outsider))

    def test_alliance_is_character_added(self):
        import_ = app_import.get("alliance")
        user = UserMainFactory(main_character__scopes=alliance_scopes)
        char = user.profile.main_character
        token = user.token_set.first()

        self.assertFalse(import_.is_character_added(char))

        AllianceToken.objects.create(alliance=char.alliance, token=token)
        self.assertTrue(import_.is_character_added(char))

    def test_alliance_is_character_added_annotation(self):
        import_ = app_import.get("alliance")
        user = UserMainFactory(main_character__scopes=alliance_scopes)
        char = user.profile.main_character
        token = user.token_set.first()
        AllianceToken.objects.create(alliance=char.alliance, token=token)

        annotated = (
            EveCharacter.objects.filter(pk=char.pk)
            .annotate(added=import_.is_character_added_annotation)
            .first()
        )
        self.assertTrue(annotated.added)

    def test_corporation_is_character_added(self):
        import_ = app_import.get("corporation")
        user = UserMainFactory(main_character__scopes=corporation_scopes)
        char = user.profile.main_character
        token = user.token_set.first()

        self.assertFalse(import_.is_character_added(char))

        CorporationToken.objects.create(corporation=char.corporation, token=token)
        self.assertTrue(import_.is_character_added(char))

    def test_corporation_is_character_added_annotation(self):
        import_ = app_import.get("corporation")
        user = UserMainFactory(main_character__scopes=corporation_scopes)
        char = user.profile.main_character
        token = user.token_set.first()
        CorporationToken.objects.create(corporation=char.corporation, token=token)

        annotated = (
            EveCharacter.objects.filter(pk=char.pk)
            .annotate(added=import_.is_character_added_annotation)
            .first()
        )
        self.assertTrue(annotated.added)

    def test_get_users_with_perms_wired(self):
        alliance_member = UserMainFactory(
            permissions=["aa_contacts.manage_alliance_contacts"]
        )
        corp_member = UserMainFactory(
            permissions=["aa_contacts.manage_corporation_contacts"]
        )

        self.assertIn(
            alliance_member, app_import.get("alliance").get_users_with_perms()
        )
        self.assertIn(corp_member, app_import.get("corporation").get_users_with_perms())
