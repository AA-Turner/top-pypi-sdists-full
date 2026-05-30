from types import SimpleNamespace
from unittest.mock import MagicMock, PropertyMock, patch

from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase

from esi.exceptions import HTTPNotModified
from esi.models import Token

from allianceauth.tests.auth_utils import AuthUtils

from ..evelinks import eveimageserver
from ..models import (
    EveAllianceInfo, EveCharacter, EveCorporationInfo, EveFactionInfo,
)
from .esi_client_stub import EsiClientStub


def response_stub() -> SimpleNamespace:
    return SimpleNamespace(headers={"Last-Modified": "Tue, 20 May 2025 13:24:00 GMT"})


def http_not_modified() -> HTTPNotModified:
    return HTTPNotModified(status_code=304, headers={})


class EveCharacterTestCase(TestCase):
    def test_is_biomassed(self) -> None:
        alive = EveCharacter(
            character_id=42,
            character_name="Alive",
            corporation_id=123,
            corporation_name="Alive Corp",
            corporation_ticker="ALV",
        )
        dead = EveCharacter(
            character_id=43,
            character_name="Dead",
            corporation_id=1000001,
            corporation_name="Doomheim",
            corporation_ticker="DOOM",
        )

        self.assertFalse(alive.is_biomassed)
        self.assertTrue(dead.is_biomassed)

    def test_corporation_prop(self) -> None:
        """
        Test that the correct corporation is returned by the corporation property
        """
        character = EveCharacter.objects.create(
            character_id=1234,
            character_name='character.name',
            corporation_id=2345,
            corporation_name='character.corp.name',
            corporation_ticker='cc1',
            alliance_id=12345,
            alliance_name='character.alliance.name',
        )

        expected = EveCorporationInfo.objects.create(
            corporation_id=2345,
            corporation_name='corp.name',
            corporation_ticker='cc1',
            member_count=10,
            alliance=None,
        )

        incorrect = EveCorporationInfo.objects.create(
            corporation_id=9999,
            corporation_name='corp.name1',
            corporation_ticker='cc11',
            member_count=10,
            alliance=None,
        )

        self.assertEqual(character.corporation, expected)
        self.assertNotEqual(character.corporation, incorrect)

    def test_corporation_prop_exception(self) -> None:
        """
        Check that an exception is raised when the expected
        object is not in the database
        """
        character = EveCharacter.objects.create(
            character_id=1234,
            character_name='character.name',
            corporation_id=2345,
            corporation_name='character.corp.name',
            corporation_ticker='cc1',
            alliance_id=123456,
            alliance_name='character.alliance.name',
        )

        with self.assertRaises(EveCorporationInfo.DoesNotExist):
            _ = character.corporation

    def test_alliance_prop(self) -> None:
        """
        Test that the correct alliance is returned by the alliance property
        """
        character = EveCharacter.objects.create(
            character_id=1234,
            character_name='character.name',
            corporation_id=2345,
            corporation_name='character.corp.name',
            corporation_ticker='cc1',
            alliance_id=3456,
            alliance_name='character.alliance.name',
        )

        expected = EveAllianceInfo.objects.create(
            alliance_id=3456,
            alliance_name='alliance.name',
            alliance_ticker='ac2',
            executor_corp_id=2345,
        )

        incorrect = EveAllianceInfo.objects.create(
            alliance_id=9001,
            alliance_name='alliance.name1',
            alliance_ticker='ac1',
            executor_corp_id=2654,
        )

        self.assertEqual(character.alliance, expected)
        self.assertNotEqual(character.alliance, incorrect)

    def test_alliance_prop_exception(self) -> None:
        """
        Check that an exception is raised when the expected
        object is not in the database
        """
        character = EveCharacter.objects.create(
            character_id=1234,
            character_name='character.name',
            corporation_id=2345,
            corporation_name='character.corp.name',
            corporation_ticker='cc1',
            alliance_id=3456,
            alliance_name='character.alliance.name',
        )

        with self.assertRaises(EveAllianceInfo.DoesNotExist):
            _ = character.alliance

    def test_alliance_prop_none(self) -> None:
        """
        Check that None is returned when the character has no alliance
        """
        character = EveCharacter.objects.create(
            character_id=1234,
            character_name='character.name',
            corporation_id=2345,
            corporation_name='character.corp.name',
            corporation_ticker='cc1',
            alliance_id=None,
            alliance_name='',
        )

        self.assertIsNone(character.alliance)

    def test_faction_prop(self) -> None:
        """
        Test that the correct faction is returned by the alliance property
        """
        character = EveCharacter.objects.create(
            character_id=1234,
            character_name='character.name',
            corporation_id=2345,
            corporation_name='character.corp.name',
            corporation_ticker='cc1',
            alliance_id=3456,
            alliance_name='character.alliance.name',
            faction_id=1337,
            faction_name='character.faction.name'
        )

        expected = EveFactionInfo.objects.create(faction_id=1337, faction_name='faction.name')
        incorrect = EveFactionInfo.objects.create(faction_id=8008, faction_name='faction.badname')

        self.assertEqual(character.faction, expected)
        self.assertNotEqual(character.faction, incorrect)

    def test_faction_prop_exception(self) -> None:
        """
        Check that an exception is raised when the expected
        object is not in the database
        """
        character = EveCharacter.objects.create(
            character_id=1234,
            character_name='character.name',
            corporation_id=2345,
            corporation_name='character.corp.name',
            corporation_ticker='cc1',
            alliance_id=3456,
            alliance_name='character.alliance.name',
            faction_id=1337,
            faction_name='character.faction.name'
        )

        with self.assertRaises(EveFactionInfo.DoesNotExist):
            _ = character.faction

    def test_faction_prop_none(self) -> None:
        """
        Check that None is returned when the character has no alliance
        """
        character = EveCharacter.objects.create(
            character_id=1234,
            character_name='character.name',
            corporation_id=2345,
            corporation_name='character.corp.name',
            corporation_ticker='cc1',
            alliance_id=None,
            alliance_name='',
            faction_id=None,
            faction_name='',
        )

        self.assertIsNone(character.faction)

    @patch('allianceauth.eveonline.models.open_api_provider.get_character')
    def test_update_character(self, mock_get_character) -> None:
        EveAllianceInfo.objects.create(
            alliance_id=3001,
            alliance_name='Dummy Alliance 1',
            alliance_ticker='DA1',
            executor_corp_id=2001,
        )
        EveFactionInfo.objects.create(
            faction_id=1337,
            faction_name='Dummy Faction 1',
        )
        EveCorporationInfo.objects.create(
            corporation_id=2001,
            corporation_name='Dummy Corp 1',
            corporation_ticker='DC1',
            member_count=10,
            alliance=None,
        )
        EveCorporationInfo.objects.create(
            corporation_id=2002,
            corporation_name='Dummy Corp 2',
            corporation_ticker='DC2',
            member_count=34,
            alliance=None,
        )

        mock_get_character.return_value = (
            SimpleNamespace(
                corporation_id=2002,
                alliance_id=None,
                faction_id=None,
                birthday=None,
                bloodline_id=None,
                description="",
                gender="",
                name='Bruce X. Wayne',
                race_id=None,
                security_status=0.0,
                title="",
            ),
            response_stub(),
        )

        my_character = EveCharacter.objects.create(
            character_id=1001,
            character_name='Bruce Wayne',
            corporation_id=2001,
            corporation_name='Dummy Corp 1',
            corporation_ticker='DC1',
            alliance_id=3001,
            alliance_name='Dummy Alliance 1',
            faction_id=1337,
            faction_name='Dummy Faction 1',
        )

        my_character.update_character()
        my_character.refresh_from_db()
        self.assertEqual(my_character.character_name, 'Bruce X. Wayne')
        self.assertEqual(my_character.corporation_name, 'Dummy Corp 2')
        self.assertFalse(my_character.faction_id)

    @patch('allianceauth.eveonline.models.open_api_provider.get_character')
    def test_update_character_wo_object(self, mock_get_character) -> None:
        mock_get_character.side_effect = http_not_modified()
        my_character = EveCharacter.objects.create(
            character_id=1001,
            character_name='Bruce Wayne',
            corporation_id=2001,
            corporation_name='Dummy Corp 1',
            corporation_ticker='DC1',
            alliance_id=3001,
            alliance_name='Dummy Alliance 1',
            faction_id=1337,
            faction_name='Dummy Faction 1',
        )

        result = my_character.update_character()
        my_character.refresh_from_db()

        self.assertEqual(result, my_character)
        self.assertEqual(my_character.character_name, 'Bruce Wayne')

    @patch('allianceauth.eveonline.models.open_api_provider.get_character')
    def test_update_character_creates_missing_related_objects(self, mock_get_character) -> None:
        my_character = EveCharacter.objects.create(
            character_id=1001,
            character_name='Bruce Wayne',
            corporation_id=2001,
            corporation_name='Dummy Corp 1',
            corporation_ticker='DC1',
            alliance_id=None,
        )
        mock_get_character.return_value = (
            SimpleNamespace(
                corporation_id=2002,
                alliance_id=3001,
                faction_id=1337,
                birthday=None,
                bloodline_id=None,
                description='Updated description',
                gender='Male',
                name='Bruce Updated',
                race_id=1,
                security_status=0.0,
                title='CEO',
            ),
            response_stub(),
        )

        with patch.object(EveCorporationInfo.objects, 'get', side_effect=EveCorporationInfo.DoesNotExist), patch.object(
            EveCorporationInfo.objects,
            'create_corporation',
            return_value=SimpleNamespace(corporation_name='Created Corp', corporation_ticker='CC1'),
        ) as mock_create_corporation, patch.object(EveAllianceInfo.objects, 'get', side_effect=EveAllianceInfo.DoesNotExist), patch.object(
            EveAllianceInfo.objects,
            'create_alliance',
            return_value=SimpleNamespace(alliance_name='Created Alliance', alliance_ticker='CA1'),
        ) as mock_create_alliance, patch.object(EveFactionInfo.objects, 'get', side_effect=EveFactionInfo.DoesNotExist), patch.object(
            EveFactionInfo.objects,
            'create_faction',
            return_value=SimpleNamespace(faction_name='Created Faction'),
        ) as mock_create_faction:
            my_character.update_character()

        my_character.refresh_from_db()
        mock_create_corporation.assert_called_once_with(corporation_id=2002)
        mock_create_alliance.assert_called_once_with(alliance_id=3001)
        mock_create_faction.assert_called_once_with(faction_id=1337)
        self.assertEqual(my_character.corporation_name, 'Created Corp')
        self.assertEqual(my_character.alliance_name, 'Created Alliance')
        self.assertEqual(my_character.faction_name, 'Created Faction')

    def test_image_url(self) -> None:
        self.assertEqual(
            EveCharacter.generic_portrait_url(42),
            eveimageserver._eve_entity_image_url('character', 42)
        )
        self.assertEqual(
            EveCharacter.generic_portrait_url(42, 256),
            eveimageserver._eve_entity_image_url('character', 42, 256)
        )

    def test_portrait_urls(self) -> None:
        x = EveCharacter(
            character_id=42,
            character_name='character.name',
            corporation_id=123,
            corporation_name='corporation.name',
            corporation_ticker='ABC',
        )
        self.assertEqual(
            x.portrait_url(),
            eveimageserver._eve_entity_image_url('character', 42)
        )
        self.assertEqual(
            x.portrait_url(64),
            eveimageserver._eve_entity_image_url('character', 42, size=64)
        )
        self.assertEqual(
            x.portrait_url_32,
            eveimageserver._eve_entity_image_url('character', 42, size=32)
        )
        self.assertEqual(
            x.portrait_url_64,
            eveimageserver._eve_entity_image_url('character', 42, size=64)
        )
        self.assertEqual(
            x.portrait_url_128,
            eveimageserver._eve_entity_image_url('character', 42, size=128)
        )
        self.assertEqual(
            x.portrait_url_256,
            eveimageserver._eve_entity_image_url('character', 42, size=256)
        )

    def test_corporation_logo_urls(self) -> None:
        x = EveCharacter(
            character_id=42,
            character_name='character.name',
            corporation_id=123,
            corporation_name='corporation.name',
            corporation_ticker='ABC',
        )
        self.assertEqual(
            x.corporation_logo_url(),
            eveimageserver._eve_entity_image_url('corporation', 123)
        )
        self.assertEqual(
            x.corporation_logo_url(256),
            eveimageserver._eve_entity_image_url('corporation', 123, size=256)
        )
        self.assertEqual(
            x.corporation_logo_url_32,
            eveimageserver._eve_entity_image_url('corporation', 123, size=32)
        )
        self.assertEqual(
            x.corporation_logo_url_64,
            eveimageserver._eve_entity_image_url('corporation', 123, size=64)
        )
        self.assertEqual(
            x.corporation_logo_url_128,
            eveimageserver._eve_entity_image_url('corporation', 123, size=128)
        )
        self.assertEqual(
            x.corporation_logo_url_256,
            eveimageserver._eve_entity_image_url('corporation', 123, size=256)
        )

    def test_alliance_logo_urls(self) -> None:
        x = EveCharacter(
            character_id=42,
            character_name='character.name',
            corporation_id=123,
            corporation_name='corporation.name',
            corporation_ticker='ABC',
        )
        self.assertEqual(
            x.alliance_logo_url(),
            ''
        )
        self.assertEqual(
            x.alliance_logo_url_32,
            ''
        )
        self.assertEqual(
            x.alliance_logo_url_64,
            ''
        )
        self.assertEqual(
            x.alliance_logo_url_128,
            ''
        )
        self.assertEqual(
            x.alliance_logo_url_256,
            ''
        )
        x.alliance_id = 987
        self.assertEqual(
            x.alliance_logo_url(),
            eveimageserver._eve_entity_image_url('alliance', 987)
        )
        self.assertEqual(
            x.alliance_logo_url(128),
            eveimageserver._eve_entity_image_url('alliance', 987, size=128)
        )
        self.assertEqual(
            x.alliance_logo_url_32,
            eveimageserver._eve_entity_image_url('alliance', 987, size=32)
        )
        self.assertEqual(
            x.alliance_logo_url_64,
            eveimageserver._eve_entity_image_url('alliance', 987, size=64)
        )
        self.assertEqual(
            x.alliance_logo_url_128,
            eveimageserver._eve_entity_image_url('alliance', 987, size=128)
        )
        self.assertEqual(
            x.alliance_logo_url_256,
            eveimageserver._eve_entity_image_url('alliance', 987, size=256)
        )

    def test_faction_logo_urls(self) -> None:
        x = EveCharacter(
            character_id=42,
            character_name='character.name',
            corporation_id=123,
            corporation_name='corporation.name',
            corporation_ticker='ABC',
        )
        self.assertEqual(x.faction_logo_url(), '')
        self.assertEqual(x.faction_logo_url_32, '')
        self.assertEqual(x.faction_logo_url_64, '')
        self.assertEqual(x.faction_logo_url_128, '')
        self.assertEqual(x.faction_logo_url_256, '')

        x.faction_id = 555

        self.assertEqual(
            x.faction_logo_url(),
            eveimageserver._eve_entity_image_url('corporation', 555)
        )
        self.assertEqual(
            x.faction_logo_url(128),
            eveimageserver._eve_entity_image_url('corporation', 555, size=128)
        )
        self.assertEqual(
            x.faction_logo_url_32,
            eveimageserver._eve_entity_image_url('corporation', 555, size=32)
        )
        self.assertEqual(
            x.faction_logo_url_64,
            eveimageserver._eve_entity_image_url('corporation', 555, size=64)
        )
        self.assertEqual(
            x.faction_logo_url_128,
            eveimageserver._eve_entity_image_url('corporation', 555, size=128)
        )
        self.assertEqual(
            x.faction_logo_url_256,
            eveimageserver._eve_entity_image_url('corporation', 555, size=256)
        )


class EveFactionTestCase(TestCase):
    def test_str(self) -> None:
        faction = EveFactionInfo(faction_id=1337, faction_name="Test Faction")

        self.assertEqual(str(faction), "Test Faction")

    def test_image_url(self) -> None:
        self.assertEqual(
            EveFactionInfo.generic_logo_url(42),
            eveimageserver._eve_entity_image_url('corporation', 42)
        )
        self.assertEqual(
            EveFactionInfo.generic_logo_url(42, 256),
            eveimageserver._eve_entity_image_url('corporation', 42, 256)
        )

    def test_logo_url_and_name(self) -> None:
        faction = EveFactionInfo(faction_id=42, faction_name="Faction Name")

        self.assertEqual(faction.name, "Faction Name")
        self.assertEqual(faction.logo_url(), 'https://images.evetech.net/corporations/42/logo?size=32')
        self.assertEqual(faction.logo_url(64), 'https://images.evetech.net/corporations/42/logo?size=64')
        self.assertEqual(faction.logo_url_32, 'https://images.evetech.net/corporations/42/logo?size=32')
        self.assertEqual(faction.logo_url_64, 'https://images.evetech.net/corporations/42/logo?size=64')
        self.assertEqual(faction.logo_url_128, 'https://images.evetech.net/corporations/42/logo?size=128')
        self.assertEqual(faction.logo_url_256, 'https://images.evetech.net/corporations/42/logo?size=256')

    def test_related_corporations(self) -> None:
        corp = EveCorporationInfo.objects.create(
            corporation_id=2001,
            corporation_name='Corp',
            corporation_ticker='CORP',
            member_count=10,
        )
        militia = EveCorporationInfo.objects.create(
            corporation_id=2002,
            corporation_name='Militia',
            corporation_ticker='MIL',
            member_count=11,
        )
        faction = EveFactionInfo.objects.create(
            faction_id=1337,
            faction_name='Faction',
            corporation_id=corp.corporation_id,
            militia_corporation_id=militia.corporation_id,
        )
        missing_faction = EveFactionInfo.objects.create(
            faction_id=1338,
            faction_name='Missing Faction',
            corporation_id=9998,
            militia_corporation_id=9999,
        )

        self.assertEqual(faction.corporation, corp)
        self.assertEqual(faction.militia_corporation, militia)
        self.assertIsNone(missing_faction.corporation)
        self.assertIsNone(missing_faction.militia_corporation)


class EveAllianceTestCase(TestCase):

    def test_str(self) -> None:
        my_alliance = EveAllianceInfo(
            alliance_id=3001,
            alliance_name='Dummy Alliance 1',
            alliance_ticker='DA1',
            executor_corp_id=2001
        )
        self.assertEqual(str(my_alliance), 'Dummy Alliance 1')

    @patch('allianceauth.eveonline.models.open_api_provider.get_alliance_corps')
    @patch('allianceauth.eveonline.models.EveCorporationInfo.objects.create_corporation')
    def test_populate_alliance(self, mock_create_corporation, mock_get_alliance_corps) -> None:

        def create_corp(corporation_id):
            if corporation_id == 2002:
                EveCorporationInfo.objects.create(
                    corporation_id=2002,
                    corporation_name='Dummy Corporation 2',
                    corporation_ticker='DC2',
                    member_count=87,
                )
            else:
                raise ValueError()

        mock_get_alliance_corps.return_value = [2001, 2002]
        mock_create_corporation.side_effect = create_corp

        EveCorporationInfo.objects.create(
            corporation_id=2001,
            corporation_name='Dummy Corporation 1',
            corporation_ticker='DC1',
            member_count=42,
        )

        my_alliance = EveAllianceInfo(
            alliance_id=3001,
            alliance_name='Dummy Alliance 1',
            alliance_ticker='DA1',
            executor_corp_id=2001
        )
        my_alliance.save()
        my_alliance.populate_alliance()

        for corporation in (
            EveCorporationInfo.objects.filter(corporation_id__in=[2001, 2002])
        ):
            self.assertEqual(corporation.alliance, my_alliance)

    @patch('allianceauth.eveonline.models.open_api_provider.get_alliance_corps')
    def test_populate_alliance_wo_object(self, mock_get_alliance_corps) -> None:
        mock_get_alliance_corps.side_effect = http_not_modified()
        my_alliance = EveAllianceInfo.objects.create(
            alliance_id=3001,
            alliance_name='Dummy Alliance 1',
            alliance_ticker='DA1',
            executor_corp_id=2001,
        )
        corp = EveCorporationInfo.objects.create(
            corporation_id=2001,
            corporation_name='Dummy Corporation 1',
            corporation_ticker='DC1',
            member_count=42,
            alliance=my_alliance,
        )

        result = my_alliance.populate_alliance()
        corp.refresh_from_db()

        self.assertEqual(result, my_alliance)
        self.assertEqual(corp.alliance, my_alliance)

    @patch('allianceauth.eveonline.models.open_api_provider.get_alliance')
    def test_update_alliance_with_object(self, mock_get_alliance) -> None:
        my_alliance = EveAllianceInfo.objects.create(
            alliance_id=3001,
            alliance_name='Dummy Alliance 1',
            alliance_ticker='DA1',
            executor_corp_id=2001
        )
        mock_get_alliance.return_value = (
            SimpleNamespace(
                name='Dummy Alliance 2',
                ticker='DA2',
                executor_corporation_id=2004,
                faction_id=None,
                creator_corporation_id=None,
                creator_id=None,
                date_founded=None,
            ),
            response_stub(),
        )
        my_alliance.update_alliance()
        my_alliance.refresh_from_db()
        self.assertEqual(int(my_alliance.executor_corp_id), 2004)

        # potential bug
        # update_alliance() is only updateting executor_corp_id when object is given

    @patch('allianceauth.eveonline.models.open_api_provider.get_alliance')
    def test_update_alliance_creates_missing_faction(self, mock_get_alliance) -> None:
        my_alliance = EveAllianceInfo.objects.create(
            alliance_id=3001,
            alliance_name='Dummy Alliance 1',
            alliance_ticker='DA1',
            executor_corp_id=2001
        )
        faction = EveFactionInfo.objects.create(
            faction_id=1337,
            faction_name='Created Faction',
        )
        mock_get_alliance.return_value = (
            SimpleNamespace(
                name='Dummy Alliance 2',
                ticker='DA2',
                executor_corporation_id=2004,
                faction_id=1337,
                creator_corporation_id=None,
                creator_id=None,
                date_founded=None,
            ),
            response_stub(),
        )

        with patch.object(EveFactionInfo.objects, 'get', side_effect=EveFactionInfo.DoesNotExist), patch.object(
            EveFactionInfo.objects,
            'create_faction',
            return_value=faction,
        ) as mock_create_faction:
            my_alliance.update_alliance()

        my_alliance.refresh_from_db()
        mock_create_faction.assert_called_once_with(faction_id=1337)
        self.assertEqual(my_alliance.faction.faction_id, 1337)

    @patch('allianceauth.eveonline.models.open_api_provider.get_alliance')
    def test_update_alliance_wo_object(self, mock_get_alliance) -> None:
        mock_get_alliance.side_effect = http_not_modified()

        my_alliance = EveAllianceInfo.objects.create(
            alliance_id=3001,
            alliance_name='Dummy Alliance 1',
            alliance_ticker='DA1',
            executor_corp_id=2001
        )
        my_alliance.save()
        my_alliance.update_alliance()
        my_alliance.refresh_from_db()
        self.assertEqual(int(my_alliance.executor_corp_id), 2001)

        # potential bug
        # update_alliance() is only updateting executor_corp_id nothing else ???

    def test_image_url(self) -> None:
        self.assertEqual(
            EveAllianceInfo.generic_logo_url(42),
            eveimageserver._eve_entity_image_url('alliance', 42)
        )
        self.assertEqual(
            EveAllianceInfo.generic_logo_url(42, 256),
            eveimageserver._eve_entity_image_url('alliance', 42, 256)
        )

    def test_logo_url(self) -> None:
        x = EveAllianceInfo(
            alliance_id=42,
            alliance_name='alliance.name',
            alliance_ticker='ABC',
            executor_corp_id=123
        )
        self.assertEqual(
            x.logo_url(),
            'https://images.evetech.net/alliances/42/logo?size=32'
        )
        self.assertEqual(
            x.logo_url(64),
            'https://images.evetech.net/alliances/42/logo?size=64'
        )
        self.assertEqual(
            x.logo_url_32,
            'https://images.evetech.net/alliances/42/logo?size=32'
        )
        self.assertEqual(
            x.logo_url_64,
            'https://images.evetech.net/alliances/42/logo?size=64'
        )
        self.assertEqual(
            x.logo_url_128,
            'https://images.evetech.net/alliances/42/logo?size=128'
        )
        self.assertEqual(
            x.logo_url_256,
            'https://images.evetech.net/alliances/42/logo?size=256'
        )

    def test_helper_properties(self) -> None:
        creator_corp = EveCorporationInfo.objects.create(
            corporation_id=123,
            corporation_name='Creator Corp',
            corporation_ticker='CRT',
            member_count=10,
        )
        executor_corp = EveCorporationInfo.objects.create(
            corporation_id=456,
            corporation_name='Executor Corp',
            corporation_ticker='EXE',
            member_count=20,
        )
        alliance = EveAllianceInfo.objects.create(
            alliance_id=42,
            alliance_name='Alliance Name',
            alliance_ticker='ALY',
            creator_corporation_id=creator_corp.corporation_id,
            executor_corp_id=executor_corp.corporation_id,
        )
        missing = EveAllianceInfo.objects.create(
            alliance_id=43,
            alliance_name='Missing Corp Alliance',
            alliance_ticker='MIS',
            creator_corporation_id=9998,
            executor_corp_id=9999,
        )
        no_executor = EveAllianceInfo.objects.create(
            alliance_id=44,
            alliance_name='No Exec',
            alliance_ticker='NON',
            executor_corp_id=None,
        )

        self.assertEqual(alliance.name, 'Alliance Name')
        self.assertEqual(alliance.ticker, 'ALY')
        self.assertEqual(alliance.creator_corporation, creator_corp)
        self.assertEqual(alliance.executor_corporation, executor_corp)
        self.assertEqual(alliance.executor_corporation_id, executor_corp.corporation_id)
        self.assertIsNone(missing.creator_corporation)
        self.assertIsNone(missing.executor_corporation)
        self.assertIsNone(no_executor.executor_corporation)
        self.assertIsNone(no_executor.executor_corporation_id)


class EveCorporationTestCase(TestCase):

    def setUp(self) -> None:
        my_alliance = EveAllianceInfo.objects.create(
            alliance_id=3001,
            alliance_name='Dummy Alliance 1',
            alliance_ticker='DA1',
            executor_corp_id=2001
        )
        self.my_corp = EveCorporationInfo(
            corporation_id=2001,
            corporation_name='Dummy Corporation 1',
            corporation_ticker='DC1',
            member_count=42,
            alliance=my_alliance
        )

    def test_str(self) -> None:
        self.assertEqual(str(self.my_corp), 'Dummy Corporation 1')

    def test_name_and_ticker(self) -> None:
        self.assertEqual(self.my_corp.name, 'Dummy Corporation 1')
        self.assertEqual(self.my_corp.ticker, 'DC1')

    @patch('allianceauth.eveonline.models.open_api_provider.get_corporation')
    def test_update_corporation_from_object_w_alliance(self, mock_get_corporation) -> None:
        mock_get_corporation.return_value = (
            SimpleNamespace(
                alliance_id=3001,
                faction_id=None,
                ceo_id=1001,
                creator_id=None,
                date_founded=None,
                description="",
                home_station_id=None,
                member_count=87,
                name='Dummy Corporation 1',
                shares=None,
                tax_rate=None,
                ticker='DC1',
                url="",
                war_eligible=False,
            ),
            response_stub(),
        )
        self.my_corp.save()
        self.my_corp.update_corporation()
        self.assertEqual(self.my_corp.member_count, 87)

        # potential bug
        # update_corporation updates member_count only

    @patch('allianceauth.eveonline.models.open_api_provider.get_corporation')
    def test_update_corporation_creates_missing_related_objects(self, mock_get_corporation) -> None:
        faction = EveFactionInfo.objects.create(
            faction_id=1337,
            faction_name='Created Faction',
        )
        alliance = EveAllianceInfo.objects.create(
            alliance_id=3002,
            alliance_name='Created Alliance',
            alliance_ticker='CA1',
            executor_corp_id=2002,
        )
        mock_get_corporation.return_value = (
            SimpleNamespace(
                alliance_id=3002,
                faction_id=1337,
                ceo_id=1001,
                creator_id=1002,
                date_founded=None,
                description='Updated description',
                home_station_id=600001,
                member_count=87,
                name='Dummy Corporation 1',
                shares=42,
                tax_rate=0.5,
                ticker='DC1',
                url='https://example.com',
                war_eligible=True,
            ),
            response_stub(),
        )

        with patch.object(EveAllianceInfo.objects, 'get', side_effect=EveAllianceInfo.DoesNotExist), patch.object(
            EveAllianceInfo.objects,
            'create_alliance',
            return_value=alliance,
        ) as mock_create_alliance, patch.object(EveFactionInfo.objects, 'get', side_effect=EveFactionInfo.DoesNotExist), patch.object(
            EveFactionInfo.objects,
            'create_faction',
            return_value=faction,
        ) as mock_create_faction:
            self.my_corp.save()
            self.my_corp.update_corporation()

        mock_create_alliance.assert_called_once_with(alliance_id=3002)
        mock_create_faction.assert_called_once_with(faction_id=1337)
        self.assertEqual(self.my_corp.alliance, alliance)
        self.assertEqual(self.my_corp.faction, faction)
        self.assertEqual(self.my_corp.home_station_id, 600001)
        self.assertEqual(self.my_corp.shares, 42)
        self.assertEqual(self.my_corp.tax_rate, 0.5)
        self.assertTrue(self.my_corp.war_eligible)

    @patch('allianceauth.eveonline.models.open_api_provider.get_corporation')
    def test_update_corporation_no_object_w_alliance(self, mock_get_corporation) -> None:
        mock_get_corporation.side_effect = http_not_modified()

        self.my_corp.save()
        self.my_corp.update_corporation()
        self.assertEqual(self.my_corp.member_count, 42)

    @patch('allianceauth.eveonline.models.open_api_provider.get_corporation')
    def test_update_corporation_from_object_wo_alliance(self, mock_get_corporation) -> None:
        my_corp2 = EveCorporationInfo(
            corporation_id=2011,
            corporation_name='Dummy Corporation 11',
            corporation_ticker='DC11',
            member_count=6
        )
        mock_get_corporation.return_value = (
            SimpleNamespace(
                alliance_id=None,
                faction_id=None,
                ceo_id=1001,
                creator_id=None,
                date_founded=None,
                description="",
                home_station_id=None,
                member_count=8,
                name='Dummy Corporation 11',
                shares=None,
                tax_rate=None,
                ticker='DC11',
                url="",
                war_eligible=False,
            ),
            response_stub(),
        )
        my_corp2.save()
        my_corp2.update_corporation()
        self.assertEqual(my_corp2.member_count, 8)
        self.assertIsNone(my_corp2.alliance)

    def test_image_url(self) -> None:
        self.assertEqual(
            EveCorporationInfo.generic_logo_url(42),
            eveimageserver._eve_entity_image_url('corporation', 42)
        )
        self.assertEqual(
            EveCorporationInfo.generic_logo_url(42, 256),
            eveimageserver._eve_entity_image_url('corporation', 42, 256)
        )

    def test_logo_url(self) -> None:
        self.assertEqual(
            self.my_corp.logo_url(),
            'https://images.evetech.net/corporations/2001/logo?size=32'
        )
        self.assertEqual(
            self.my_corp.logo_url(64),
            'https://images.evetech.net/corporations/2001/logo?size=64'
        )
        self.assertEqual(
            self.my_corp.logo_url_32,
            'https://images.evetech.net/corporations/2001/logo?size=32'
        )
        self.assertEqual(
            self.my_corp.logo_url_64,
            'https://images.evetech.net/corporations/2001/logo?size=64'
        )
        self.assertEqual(
            self.my_corp.logo_url_128,
            'https://images.evetech.net/corporations/2001/logo?size=128'
        )
        self.assertEqual(
            self.my_corp.logo_url_256,
            'https://images.evetech.net/corporations/2001/logo?size=256'
        )


@patch("allianceauth.eveonline.models.notify")
class TestCharacterUpdate(TestCase):
    def test_should_update_normal_character(self, mock_notify) -> None:
        # given
        with patch("allianceauth.eveonline.providers.open_api_provider._client", EsiClientStub()):
            my_character = EveCharacter.objects.create(
                character_id=1001,
                character_name="not my name",
                corporation_id=2002,
                corporation_name="Wayne Food",
                corporation_ticker="WYF",
                alliance_id=None
            )
            # when
            my_character.update_character()
            # then
            my_character.refresh_from_db()
            self.assertEqual(my_character.character_name, "Bruce Wayne")
            self.assertEqual(my_character.corporation_id, 2001)
            self.assertEqual(my_character.corporation_name, "Wayne Technologies")
            self.assertEqual(my_character.corporation_ticker, "WTE")
            self.assertEqual(my_character.alliance_id, 3001)
            self.assertEqual(my_character.alliance_name, "Wayne Enterprises")
            self.assertEqual(my_character.alliance_ticker, "WYE")
            self.assertFalse(mock_notify.called)

    def test_should_update_dead_character_with_owner(
        self, mock_notify
    ):
        # given
        with patch("allianceauth.eveonline.providers.open_api_provider._client", EsiClientStub()):
            character_1666 = EveCharacter.objects.create(
                character_id=1666,
                character_name="Hal Jordan",
                corporation_id=2002,
                corporation_name="Wayne Food",
                corporation_ticker="WYF",
                alliance_id=None
            )
            user = AuthUtils.create_user("Bruce Wayne")
            token_1666 = Token.objects.create(
                user=user,
                character_id=character_1666.character_id,
                character_name=character_1666.character_name,
                character_owner_hash="ABC123-1666",
            )
            character_1001 = EveCharacter.objects.create(
                character_id=1001,
                character_name="Bruce Wayne",
                corporation_id=2001,
                corporation_name="Wayne Technologies",
                corporation_ticker="WYT",
                alliance_id=None
            )
            token_1001 = Token.objects.create(
                user=user,
                character_id=character_1001.character_id,
                character_name=character_1001.character_name,
                character_owner_hash="ABC123-1001",
            )
            # when
            character_1666.update_character()
            # then
            character_1666.refresh_from_db()
            self.assertTrue(character_1666.is_biomassed)
            self.assertNotIn(token_1666, user.token_set.all())
            self.assertIn(token_1001, user.token_set.all())
            with self.assertRaises(ObjectDoesNotExist):
                self.assertTrue(character_1666.character_ownership)
            user.profile.refresh_from_db()
            self.assertIsNone(user.profile.main_character)
            self.assertTrue(mock_notify.called)

    def test_should_handle_dead_character_without_owner(
        self, mock_notify
    ) -> None:
        # given
        with patch("allianceauth.eveonline.providers.open_api_provider._client", EsiClientStub()):
            character_1666 = EveCharacter.objects.create(
                character_id=1666,
                character_name="Hal Jordan",
                corporation_id=1011,
                corporation_name="LexCorp",
                corporation_ticker='LC',
                alliance_id=None
            )
            # when
            character_1666.update_character()
            # then
            character_1666.refresh_from_db()
            self.assertTrue(character_1666.is_biomassed)
            self.assertFalse(mock_notify.called)

    def test_should_ignore_dead_character_without_tokens(self, mock_notify) -> None:
        character_1666 = EveCharacter.objects.create(
            character_id=1666,
            character_name="Hal Jordan",
            corporation_id=1000001,
            corporation_name="Doomheim",
            corporation_ticker="DOOM",
            alliance_id=None,
        )
        user = AuthUtils.create_user("Bruce Wayne")
        token_qs = MagicMock()
        token_qs.count.return_value = 0

        with patch.object(
            EveCharacter,
            "character_ownership",
            new_callable=PropertyMock,
            return_value=SimpleNamespace(user=user),
        ), patch("allianceauth.eveonline.models.Token.objects.filter", return_value=token_qs):
            character_1666._remove_tokens_of_biomassed_character()

        token_qs.delete.assert_not_called()
        self.assertFalse(mock_notify.called)
