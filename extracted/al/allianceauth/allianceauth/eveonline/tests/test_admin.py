from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory, TestCase

from esi.exceptions import HTTPClientError, HTTPNotModified

from allianceauth.authentication.models import User
from allianceauth.eveonline.admin import (
    EveAllianceForm, EveAllianceInfoAdmin, EveCharacterAdmin, EveCharacterForm,
    EveCorporationForm, EveCorporationInfoAdmin, EveEntityExistsError,
    EveEntityForm, EveEntityNotFoundError, EveFactionForm, EveFactionInfoAdmin,
    get_faction_choices, update_alliances_blocking,
    update_alliances_blocking_forcerefresh, update_alliances_queued,
    update_characters_blocking, update_characters_blocking_forcerefresh,
    update_characters_queued, update_corporations_blocking,
    update_corporations_blocking_forcerefresh, update_corporations_queued,
    update_factions_blocking, update_factions_queued,
)
from allianceauth.eveonline.models import (
    EveAllianceInfo, EveCharacter, EveCorporationInfo, EveFactionInfo,
)


def _http_client_error() -> HTTPClientError:
    return HTTPClientError(status_code=404, headers={}, data={})


def _http_not_modified() -> HTTPNotModified:
    return HTTPNotModified(status_code=304, headers={})


class _DummyEntityForm(EveEntityForm):
    class Meta:
        model = EveCharacter
        fields = ["id"]


class TestAdminForms(TestCase):
    def test_base_entity_form_methods(self) -> None:
        form = _DummyEntityForm()

        with self.assertRaises(NotImplementedError):
            form.clean_id()
        with self.assertRaises(NotImplementedError):
            form.save()

        self.assertIsNone(form.save_m2m())

    def test_get_faction_choices_filters_to_player_factions(self) -> None:
        with patch(
            "allianceauth.eveonline.admin.open_api_provider.get_all_factions",
            return_value=(
                [
                    SimpleNamespace(faction_id=5001, name="Faction One", militia_corporation_id=123),
                    SimpleNamespace(faction_id=5002, name="Faction Two", militia_corporation_id=None),
                ],
                SimpleNamespace(headers={}),
            ),
        ):
            self.assertEqual(get_faction_choices(), [(5001, "Faction One")])

    def test_entity_error_messages(self) -> None:
        self.assertIn("already exists", str(EveEntityExistsError("character", 1)))
        self.assertIn("not found", str(EveEntityNotFoundError("character", 1)))

    def test_faction_form_clean_and_save(self) -> None:
        with patch(
            "allianceauth.eveonline.admin.open_api_provider.get_faction",
            return_value=(SimpleNamespace(faction_id=5001), SimpleNamespace(headers={})),
        ):
            form = EveFactionForm(data={"id": "5001"})
            form.fields["id"].choices = [(5001, "Faction One")]
            self.assertTrue(form.is_valid())
            self.assertEqual(form.cleaned_data["id"], 5001)

        with patch.object(EveFactionForm, "clean_id", return_value=5001), patch.object(
            EveFactionInfo.objects,
            "create_faction",
            return_value=SimpleNamespace(faction_id=5001),
        ) as mock_create:
            form = EveFactionForm()
            result = form.save()
            mock_create.assert_called_once_with(faction_id=5001)
            self.assertEqual(result.faction_id, 5001)

    def test_faction_form_errors(self) -> None:
        with patch(
            "allianceauth.eveonline.admin.open_api_provider.get_faction",
            side_effect=_http_client_error(),
        ):
            form = EveFactionForm(data={"id": "5001"})
            form.fields["id"].choices = [(5001, "Faction One")]
            self.assertFalse(form.is_valid())
            self.assertIsInstance(form.errors["id"].as_data()[0], EveEntityNotFoundError)

        with patch(
            "allianceauth.eveonline.admin.open_api_provider.get_faction",
            side_effect=_http_not_modified(),
        ):
            EveFactionInfo.objects.create(faction_id=5001, faction_name="Faction One")
            form = EveFactionForm(data={"id": "5001"})
            form.fields["id"].choices = [(5001, "Faction One")]
            self.assertFalse(form.is_valid())
            self.assertIsInstance(form.errors["id"].as_data()[0], EveEntityExistsError)

    def test_character_form_clean_and_save(self) -> None:
        with patch(
            "allianceauth.eveonline.admin.open_api_provider.get_character",
            return_value=(SimpleNamespace(character_id=1001), SimpleNamespace(headers={})),
        ):
            form = EveCharacterForm(data={"id": "1001"})
            self.assertTrue(form.is_valid())

        with patch.object(EveCharacterForm, "clean_id", return_value=1001), patch.object(
            EveCharacter.objects,
            "create_character",
            return_value=SimpleNamespace(character_id=1001),
        ) as mock_create:
            form = EveCharacterForm()
            result = form.save()
            mock_create.assert_called_once_with(character_id=1001)
            self.assertEqual(result.character_id, 1001)

    def test_character_form_errors(self) -> None:
        with patch(
            "allianceauth.eveonline.admin.open_api_provider.get_character",
            side_effect=_http_client_error(),
        ):
            form = EveCharacterForm(data={"id": "1001"})
            self.assertFalse(form.is_valid())

        EveCharacter.objects.create(
            character_id=1001,
            character_name="Bruce Wayne",
            corporation_id=2001,
            corporation_name="Wayne Technologies",
            corporation_ticker="WT",
        )
        with patch(
            "allianceauth.eveonline.admin.open_api_provider.get_character",
            side_effect=_http_not_modified(),
        ):
            form = EveCharacterForm(data={"id": "1001"})
            self.assertFalse(form.is_valid())
            self.assertIsInstance(form.errors["id"].as_data()[0], EveEntityExistsError)

    def test_corporation_form_clean_and_save(self) -> None:
        with patch(
            "allianceauth.eveonline.admin.open_api_provider.get_corporation",
            return_value=(SimpleNamespace(corporation_id=2001), SimpleNamespace(headers={})),
        ):
            form = EveCorporationForm(data={"id": "2001"})
            self.assertTrue(form.is_valid())

        with patch.object(EveCorporationForm, "clean_id", return_value=2001), patch.object(
            EveCorporationInfo.objects,
            "create_corporation",
            return_value=SimpleNamespace(corporation_id=2001),
        ) as mock_create:
            form = EveCorporationForm()
            result = form.save()
            mock_create.assert_called_once_with(corporation_id=2001)
            self.assertEqual(result.corporation_id, 2001)

    def test_corporation_form_errors(self) -> None:
        with patch(
            "allianceauth.eveonline.admin.open_api_provider.get_corporation",
            side_effect=_http_client_error(),
        ):
            form = EveCorporationForm(data={"id": "2001"})
            self.assertFalse(form.is_valid())

        EveCorporationInfo.objects.create(
            corporation_id=2001,
            corporation_name="Wayne Technologies",
            corporation_ticker="WT",
            member_count=1,
            alliance=None,
        )
        with patch(
            "allianceauth.eveonline.admin.open_api_provider.get_corporation",
            side_effect=_http_not_modified(),
        ):
            form = EveCorporationForm(data={"id": "2001"})
            self.assertFalse(form.is_valid())
            self.assertIsInstance(form.errors["id"].as_data()[0], EveEntityExistsError)

    def test_alliance_form_clean_and_save(self) -> None:
        with patch(
            "allianceauth.eveonline.admin.open_api_provider.get_alliance",
            return_value=(SimpleNamespace(alliance_id=3001), SimpleNamespace(headers={})),
        ):
            form = EveAllianceForm(data={"id": "3001"})
            self.assertTrue(form.is_valid())

        with patch.object(EveAllianceForm, "clean_id", return_value=3001), patch.object(
            EveAllianceInfo.objects,
            "create_alliance",
            return_value=SimpleNamespace(alliance_id=3001),
        ) as mock_create:
            form = EveAllianceForm()
            result = form.save()
            mock_create.assert_called_once_with(alliance_id=3001)
            self.assertEqual(result.alliance_id, 3001)

    def test_alliance_form_errors(self) -> None:
        with patch(
            "allianceauth.eveonline.admin.open_api_provider.get_alliance",
            side_effect=_http_client_error(),
        ):
            form = EveAllianceForm(data={"id": "3001"})
            self.assertFalse(form.is_valid())

        EveAllianceInfo.objects.create(
            alliance_id=3001,
            alliance_name="Wayne Enterprises",
            alliance_ticker="WE",
            executor_corp_id=2001,
        )
        with patch(
            "allianceauth.eveonline.admin.open_api_provider.get_alliance",
            side_effect=_http_not_modified(),
        ):
            form = EveAllianceForm(data={"id": "3001"})
            self.assertFalse(form.is_valid())
            self.assertIsInstance(form.errors["id"].as_data()[0], EveEntityExistsError)


class TestForceRefreshAdminActions(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.request = self.factory.post("/admin/eveonline/")

    def test_should_force_refresh_corporations(self) -> None:
        corporation = EveCorporationInfo.objects.create(
            corporation_id=2001,
            corporation_name="Wayne Technologies",
            corporation_ticker="WT",
            member_count=42,
            alliance=None,
        )
        modeladmin = EveCorporationInfoAdmin(EveCorporationInfo, AdminSite())
        modeladmin.message_user = MagicMock()

        with patch.object(corporation, "update_corporation") as mock_update:
            update_corporations_blocking_forcerefresh(modeladmin, self.request, [corporation])

        mock_update.assert_called_once_with(force_refresh=True)
        modeladmin.message_user.assert_called_once_with(
            self.request,
            "Update from ESI performed for 1 corporations, clearing their ETags and Cache, please use responsibly",
        )

    def test_should_force_refresh_alliances(self) -> None:
        alliance = EveAllianceInfo.objects.create(
            alliance_id=3001,
            alliance_name="Wayne Enterprises",
            alliance_ticker="WE",
            executor_corp_id=2001,
        )
        modeladmin = EveAllianceInfoAdmin(EveAllianceInfo, AdminSite())
        modeladmin.message_user = MagicMock()

        with patch.object(alliance, "update_alliance") as mock_update:
            update_alliances_blocking_forcerefresh(modeladmin, self.request, [alliance])

        mock_update.assert_called_once_with(force_refresh=True)
        modeladmin.message_user.assert_called_once_with(
            self.request,
            "Update from ESI performed for 1 alliances, clearing their ETags and Cache, please use responsibly",
        )

    def test_should_force_refresh_characters(self) -> None:
        character = EveCharacter.objects.create(
            character_id=1001,
            character_name="Bruce Wayne",
            corporation_id=2001,
            corporation_name="Wayne Technologies",
            corporation_ticker="WT",
            alliance_id=3001,
            alliance_name="Wayne Enterprises",
            alliance_ticker="WE",
        )
        modeladmin = EveCharacterAdmin(EveCharacter, AdminSite())
        modeladmin.message_user = MagicMock()

        with patch.object(character, "update_character") as mock_update_affiliations, patch.object(
            character,
            "update_character_other",
        ) as mock_update_other:
            update_characters_blocking_forcerefresh(modeladmin, self.request, [character])

        mock_update_affiliations.assert_called_once_with()
        mock_update_other.assert_called_once_with(force_refresh=True)
        modeladmin.message_user.assert_called_once_with(
            self.request,
            "Update from ESI performed for 1 characters, clearing their ETags and Cache, please use responsibly",
        )


class TestAdminActionsAndConfig(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()
        self.request = self.factory.post("/admin/eveonline/")
        self.request.user = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="pass",
        )

    def test_faction_actions_and_admin(self) -> None:
        modeladmin = EveFactionInfoAdmin(EveFactionInfo, AdminSite())
        modeladmin.message_user = MagicMock()

        with patch.object(EveFactionInfo.objects, "update_factions") as mock_update:
            update_factions_blocking(modeladmin, self.request, [])
        mock_update.assert_called_once_with()

        with patch("allianceauth.eveonline.admin.update_all_factions.delay") as mock_delay:
            update_factions_queued(modeladmin, self.request, [])
        mock_delay.assert_called_once_with()

        self.assertFalse(modeladmin.has_change_permission(self.request))
        self.assertIs(modeladmin.get_form(self.request, obj=None), EveFactionForm)

        faction = EveFactionInfo.objects.create(faction_id=5001, faction_name="Faction One")
        self.assertIsNot(modeladmin.get_form(self.request, obj=faction), EveFactionForm)

    def test_corporation_actions_and_admin(self) -> None:
        corporation = EveCorporationInfo.objects.create(
            corporation_id=2001,
            corporation_name="Wayne Technologies",
            corporation_ticker="WT",
            member_count=42,
            alliance=None,
        )
        modeladmin = EveCorporationInfoAdmin(EveCorporationInfo, AdminSite())
        modeladmin.message_user = MagicMock()

        with patch.object(corporation, "update_corporation") as mock_update:
            update_corporations_blocking(modeladmin, self.request, [corporation])
        mock_update.assert_called_once_with()

        with patch("allianceauth.eveonline.admin.update_corp.delay") as mock_delay:
            update_corporations_queued(modeladmin, self.request, [corporation])
        mock_delay.assert_called_once_with(corporation.corporation_id)

        self.assertFalse(modeladmin.has_change_permission(self.request))
        self.assertIs(modeladmin.get_form(self.request, obj=None), EveCorporationForm)
        self.assertIsNot(modeladmin.get_form(self.request, obj=corporation), EveCorporationForm)

    def test_alliance_actions_and_admin(self) -> None:
        alliance = EveAllianceInfo.objects.create(
            alliance_id=3001,
            alliance_name="Wayne Enterprises",
            alliance_ticker="WE",
            executor_corp_id=2001,
        )
        modeladmin = EveAllianceInfoAdmin(EveAllianceInfo, AdminSite())
        modeladmin.message_user = MagicMock()

        with patch.object(alliance, "update_alliance") as mock_update:
            update_alliances_blocking(modeladmin, self.request, [alliance])
        mock_update.assert_called_once_with()

        with patch("allianceauth.eveonline.admin.update_alliance.delay") as mock_delay:
            update_alliances_queued(modeladmin, self.request, [alliance])
        mock_delay.assert_called_once_with(alliance.alliance_id)

        self.assertFalse(modeladmin.has_change_permission(self.request))
        self.assertIs(modeladmin.get_form(self.request, obj=None), EveAllianceForm)
        self.assertIsNot(modeladmin.get_form(self.request, obj=alliance), EveAllianceForm)

    def test_character_actions_and_admin(self) -> None:
        character = EveCharacter.objects.create(
            character_id=1001,
            character_name="Bruce Wayne",
            corporation_id=2001,
            corporation_name="Wayne Technologies",
            corporation_ticker="WT",
            alliance_id=3001,
            alliance_name="Wayne Enterprises",
            alliance_ticker="WE",
        )
        modeladmin = EveCharacterAdmin(EveCharacter, AdminSite())
        modeladmin.message_user = MagicMock()

        with patch.object(character, "update_character") as mock_update_affiliation, patch.object(
            character,
            "update_character_other",
        ) as mock_update_other:
            update_characters_blocking(modeladmin, self.request, [character])
        mock_update_affiliation.assert_called_once_with()
        mock_update_other.assert_called_once_with()

        with patch("allianceauth.eveonline.admin.update_character.delay") as mock_delay:
            update_characters_queued(modeladmin, self.request, [character])
        mock_delay.assert_called_once_with(character.character_id)

        self.assertFalse(modeladmin.has_change_permission(self.request))
        self.assertIs(modeladmin.get_form(self.request, obj=None), EveCharacterForm)
        self.assertIsNot(modeladmin.get_form(self.request, obj=character), EveCharacterForm)

    def test_character_admin_user_helpers(self) -> None:
        character = EveCharacter.objects.create(
            character_id=1001,
            character_name="Bruce Wayne",
            corporation_id=2001,
            corporation_name="Wayne Technologies",
            corporation_ticker="WT",
        )
        modeladmin = EveCharacterAdmin(EveCharacter, AdminSite())

        self.assertIsNone(modeladmin.user(character))
        self.assertIsNone(modeladmin.main_character(character))
