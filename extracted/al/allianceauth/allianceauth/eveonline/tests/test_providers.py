from unittest.mock import PropertyMock, patch

from django.test import TestCase

from esi import __url__ as esi_url, __version__ as esi_version
from esi.exceptions import HTTPClientError

from allianceauth import __url__ as aa_url, __version__ as aa_version

from ..providers import EveOpenAPIProvider
from . import set_logger
from .esi_client_stub import EsiClientStub

MODULE_PATH = "allianceauth.eveonline.providers"

set_logger(MODULE_PATH, __file__)


class TestEveOpenAPIProvider(TestCase):
    @patch.object(EveOpenAPIProvider, "client", new_callable=PropertyMock)
    def test_get_alliance(self, mock_client) -> None:
        mock_client.return_value = EsiClientStub()
        provider = EveOpenAPIProvider()

        alliance, response = provider.get_alliance(3001)
        self.assertEqual(alliance.name, "Wayne Enterprises")
        self.assertEqual(alliance.ticker, "WYE")
        self.assertEqual(alliance.executor_corporation_id, 2001)
        self.assertEqual(response.status_code, 200)

        with self.assertRaises(HTTPClientError):
            provider.get_alliance(3999)

    @patch.object(EveOpenAPIProvider, "client", new_callable=PropertyMock)
    def test_get_alliance_corps(self, mock_client) -> None:
        mock_client.return_value = EsiClientStub()
        provider = EveOpenAPIProvider()

        corp_ids = provider.get_alliance_corps(3001)
        self.assertListEqual(corp_ids, [2001, 2002, 2003])

    @patch.object(EveOpenAPIProvider, "client", new_callable=PropertyMock)
    def test_get_corporation(self, mock_client) -> None:
        mock_client.return_value = EsiClientStub()
        provider = EveOpenAPIProvider()

        corporation, response = provider.get_corporation(2001)
        self.assertEqual(corporation.name, "Wayne Technologies")
        self.assertEqual(corporation.ticker, "WTE")
        self.assertEqual(corporation.alliance_id, 3001)
        self.assertEqual(response.status_code, 200)

    @patch.object(EveOpenAPIProvider, "client", new_callable=PropertyMock)
    def test_get_character(self, mock_client) -> None:
        mock_client.return_value = EsiClientStub()
        provider = EveOpenAPIProvider()

        character, response = provider.get_character(1001)
        self.assertEqual(character.name, "Bruce Wayne")
        self.assertEqual(character.corporation_id, 2001)
        self.assertEqual(response.status_code, 200)

    @patch.object(EveOpenAPIProvider, "client", new_callable=PropertyMock)
    def test_get_all_factions(self, mock_client) -> None:
        mock_client.return_value = EsiClientStub()
        provider = EveOpenAPIProvider()

        factions, response = provider.get_all_factions()
        self.assertEqual(len(factions), 2)
        self.assertEqual(factions[0].faction_id, 5001)
        self.assertEqual(response.status_code, 200)

    @patch.object(EveOpenAPIProvider, "client", new_callable=PropertyMock)
    def test_get_faction(self, mock_client) -> None:
        mock_client.return_value = EsiClientStub()
        provider = EveOpenAPIProvider()

        faction, response = provider.get_faction(5002)
        self.assertEqual(faction.faction_id, 5002)
        self.assertEqual(faction.name, "Faction Two")
        self.assertEqual(response.status_code, 200)

        missing_faction, missing_response = provider.get_faction(9999)
        self.assertIsNone(missing_faction)
        self.assertEqual(missing_response.status_code, 200)

    @patch.object(EveOpenAPIProvider, "client", new_callable=PropertyMock)
    def test_get_affiliations(self, mock_client) -> None:
        mock_client.return_value = EsiClientStub()
        provider = EveOpenAPIProvider()

        affiliations = provider.get_affiliations([1001, 1002, 1666])
        self.assertEqual({getattr(x, "character_id") for x in affiliations}, {1001, 1002, 1666})

    @patch.object(EveOpenAPIProvider, "client", new_callable=PropertyMock)
    def test_post_names(self, mock_client) -> None:
        mock_client.return_value = EsiClientStub()
        provider = EveOpenAPIProvider()

        names = provider.post_names([1001, 2001, 1666])
        self.assertEqual({getattr(x, "id") for x in names}, {1001, 2001, 1666})

    @patch.object(EveOpenAPIProvider, "client", new_callable=PropertyMock)
    def test_client_can_be_accessed(self, mock_client) -> None:
        stub = EsiClientStub()
        mock_client.return_value = stub
        provider = EveOpenAPIProvider()
        self.assertIs(provider.client, stub)

    def test_user_agent_header(self) -> None:
        provider = EveOpenAPIProvider()
        client = provider.client
        expected = (
            f"AllianceAuth/{aa_version} (dummy@example.net; +{aa_url}) "
            f"DjangoEsi/{esi_version} (+{esi_url})"
        )
        session_factory = getattr(client.api, "_session_factory")
        with session_factory() as session:
            self.assertEqual(session.headers.get("User-Agent"), expected)
