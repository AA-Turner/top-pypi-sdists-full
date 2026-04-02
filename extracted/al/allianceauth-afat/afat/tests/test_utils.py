# Standard Library
from unittest.mock import MagicMock, PropertyMock, patch

# Alliance Auth
from allianceauth.eveonline.models import (
    EveAllianceInfo,
    EveCharacter,
    EveCorporationInfo,
)

# Alliance Auth AFAT
from afat.tests import BaseTestCase
from afat.utils import (
    NoDataError,
    get_or_create_alliance_info,
    get_or_create_character,
    get_or_create_corporation_info,
)


class TestGetOrCreateAllianceInfo(BaseTestCase):
    """
    Test the get_or_create_alliance_info function
    """

    @patch("allianceauth.eveonline.models.EveAllianceInfo.objects.create_alliance")
    def test_returns_existing_alliance_info(self, mock_create_alliance):
        """
        Test that the function returns existing alliance info

        :param mock_create_alliance:
        :type mock_create_alliance:
        :return:
        :rtype:
        """

        mock_alliance = EveAllianceInfo(
            alliance_id=12345, alliance_name="Existing Alliance"
        )
        mock_create_alliance.return_value = mock_alliance

        result = get_or_create_alliance_info(alliance_id=12345)

        self.assertEqual(result, mock_alliance)

    @patch("afat.utils.logger.info")
    @patch("allianceauth.eveonline.models.EveAllianceInfo.objects.create_alliance")
    def test_creates_new_alliance_info_when_not_found(
        self, mock_create_alliance, mock_logger
    ):
        """
        Test that the function creates new alliance info when not found

        :param mock_create_alliance:
        :type mock_create_alliance:
        :param mock_logger:
        :type mock_logger:
        :return:
        :rtype:
        """

        mock_create_alliance.return_value = EveAllianceInfo(
            alliance_id=67890, alliance_name="Test Alliance"
        )

        result = get_or_create_alliance_info(alliance_id=67890)

        self.assertEqual(result.alliance_id, 67890)
        self.assertEqual(result.alliance_name, "Test Alliance")
        mock_logger.assert_called_once_with(
            msg="EveAllianceInfo object created: Test Alliance"
        )


class TestGetOrCreateCorporationInfo(BaseTestCase):
    """
    Test the get_or_create_corporation_info function
    """

    @patch(
        "allianceauth.eveonline.models.EveCorporationInfo.objects.create_corporation"
    )
    def test_returns_existing_corporation_info(self, mock_create_corporation):
        """
        Test that the function returns existing corporation info

        :param mock_create_corporation:
        :type mock_create_corporation:
        :return:
        :rtype:
        """

        mock_corporation = MagicMock()
        mock_corporation.corporation_id = 12345
        mock_corporation.corporation_name = "Existing Corporation"
        with patch(
            "allianceauth.eveonline.models.EveCorporationInfo.objects.get",
            return_value=mock_corporation,
        ):
            result = get_or_create_corporation_info(corporation_id=12345)

            self.assertEqual(result, mock_corporation)
            mock_create_corporation.assert_not_called()

    @patch("afat.utils.logger.info")
    @patch(
        "allianceauth.eveonline.models.EveCorporationInfo.objects.create_corporation"
    )
    def test_creates_new_corporation_info_when_not_found(
        self, mock_create_corporation, mock_logger
    ):
        """
        Test that the function creates new corporation info when not found

        :param mock_create_corporation:
        :type mock_create_corporation:
        :param mock_logger:
        :type mock_logger:
        :return:
        :rtype:
        """

        mock_create_corporation.return_value = MagicMock(
            corporation_id=67890, corporation_name="Test Corporation"
        )

        with patch(
            "allianceauth.eveonline.models.EveCorporationInfo.objects.get",
            side_effect=EveCorporationInfo.DoesNotExist,
        ):
            result = get_or_create_corporation_info(corporation_id=67890)

            self.assertEqual(result.corporation_id, 67890)
            self.assertEqual(result.corporation_name, "Test Corporation")
            mock_logger.assert_called_once_with(
                msg="EveCorporationInfo object created: Test Corporation"
            )


class TestGetOrCreateCharacter(BaseTestCase):
    """
    Test the get_or_create_character function
    """

    @patch("afat.utils.esi", new=MagicMock())
    @patch("afat.utils.esi_handler.result")
    def test_returns_None_when_name_resolution_returns_no_characters(self, mock_result):
        """
        Test that the function returns None when name resolution returns no characters

        :param mock_result:
        :type mock_result:
        :return:
        :rtype:
        """

        mock_result.return_value = MagicMock(characters=None)

        result = get_or_create_character(name="NonExistent")

        self.assertIsNone(result)

    @patch("afat.utils.esi", new=MagicMock())
    @patch("afat.utils.esi_handler.result")
    @patch("afat.utils.EveCharacter.objects.filter")
    def test_returns_existing_character_when_found_by_name(
        self, mock_filter, mock_result
    ):
        """
        Test that the function returns existing character when found by name

        :param mock_filter:
        :type mock_filter:
        :param mock_result:
        :type mock_result:
        :return:
        :rtype:
        """

        esi_char = MagicMock(id=12345)
        mock_result.return_value = MagicMock(characters=[esi_char])
        existing = MagicMock(character_id=12345)
        mock_filter.return_value = [existing]

        character = get_or_create_character(name="ExistingName")

        self.assertEqual(character.character_id, 12345)

    @patch("afat.utils.esi", new=MagicMock())
    @patch("afat.utils.EveCharacter.objects.filter")
    def test_returns_existing_character_when_found_by_id(self, mock_filter):
        """
        Test that the function returns existing character when found by ID

        :param mock_filter:
        :type mock_filter:
        :return:
        :rtype:
        """

        existing = MagicMock(character_id=11111)
        mock_filter.return_value = [existing]

        character = get_or_create_character(character_id=11111)

        self.assertEqual(character.character_id, 11111)

    @patch("afat.utils.esi", new=MagicMock())
    @patch("afat.utils.EveCorporationInfo.objects.create_corporation")
    @patch("afat.utils.EveCorporationInfo.objects.filter")
    @patch("afat.utils.EveCharacter.objects.get")
    @patch("afat.utils.EveCharacter.objects.create_character")
    @patch("afat.utils.EveCharacter.objects.filter")
    def test_creates_character_and_corporation_info_when_no_alliance(
        self,
        mock_eve_filter,
        mock_create_character,
        mock_get,
        mock_corp_filter,
        mock_create_corp,
    ):
        """
        Test that the function creates character and corporation info when no alliance

        :param mock_eve_filter:
        :type mock_eve_filter:
        :param mock_create_character:
        :type mock_create_character:
        :param mock_get:
        :type mock_get:
        :param mock_corp_filter:
        :type mock_corp_filter:
        :param mock_create_corp:
        :type mock_create_corp:
        :return:
        :rtype:
        """

        mock_eve_filter.return_value = []
        created = MagicMock(
            pk=1, character_name="NewChar", alliance_id=None, corporation_id=33333
        )
        mock_create_character.return_value = created
        mock_get.return_value = created
        mock_corp_filter.return_value.exists.return_value = False

        character = get_or_create_character(character_id=22222)

        self.assertEqual(character.character_name, "NewChar")
        mock_create_corp.assert_called_once_with(corp_id=33333)

    @patch("afat.utils.esi", new=MagicMock())
    @patch("afat.utils.EveAllianceInfo.objects.create_alliance")
    @patch("afat.utils.EveAllianceInfo.objects.filter")
    @patch("afat.utils.EveCharacter.objects.get")
    @patch("afat.utils.EveCharacter.objects.create_character")
    @patch("afat.utils.EveCharacter.objects.filter")
    def test_creates_character_and_alliance_info_when_alliance_present(
        self,
        mock_eve_filter,
        mock_create_character,
        mock_get,
        mock_alliance_filter,
        mock_create_alliance,
    ):
        """
        Test that the function creates character and alliance info when alliance present

        :param mock_eve_filter:
        :type mock_eve_filter:
        :param mock_create_character:
        :type mock_create_character:
        :param mock_get:
        :type mock_get:
        :param mock_alliance_filter:
        :type mock_alliance_filter:
        :param mock_create_alliance:
        :type mock_create_alliance:
        :return:
        :rtype:
        """

        mock_eve_filter.return_value = []
        created = MagicMock(
            pk=2, character_name="NewChar2", alliance_id=44444, corporation_id=55555
        )
        mock_create_character.return_value = created
        mock_get.return_value = created
        mock_alliance_filter.return_value.exists.return_value = False

        character = get_or_create_character(character_id=33333)

        self.assertEqual(character.character_name, "NewChar2")
        mock_create_alliance.assert_called_once_with(alliance_id=44444)

    @patch("afat.utils.esi", new=MagicMock())
    @patch("afat.utils.esi_handler.result")
    def test_returns_none_when_character_not_found_by_name(self, mock_result):
        """
        Test that the function returns None when character not found by name

        :param mock_result:
        :type mock_result:
        :return:
        :rtype:
        """

        mock_result.return_value = MagicMock(characters=None)

        result = get_or_create_character(name="Nonexistent Character")

        self.assertIsNone(result)

    def test_raises_error_when_no_name_or_id_provided(self):
        """
        Test that the function raises NoDataError when no name or ID is provided

        :return:
        :rtype:
        """

        with self.assertRaises(NoDataError):
            get_or_create_character()

    @patch("afat.utils.esi.__class__.client", new_callable=PropertyMock)
    @patch("allianceauth.eveonline.models.EveCharacter.objects.create_character")
    @patch("allianceauth.eveonline.models.EveCharacter.objects.get")
    @patch("allianceauth.eveonline.models.EveCharacter.objects.filter")
    def test_creates_new_character_and_related_objects(
        self,
        mock_filter,
        mock_get,
        mock_create_character,
        mock_client_prop,
    ):
        mock_universe = MagicMock()
        mock_universe.PostUniverseIds.return_value.results.return_value = {
            "characters": [{"id": 12345}]
        }
        mock_client_prop.return_value = MagicMock(Universe=mock_universe)
        mock_filter.return_value = []
        mock_character = EveCharacter(
            character_id=12345, character_name="New Character", alliance_id=67890
        )
        mock_create_character.return_value = mock_character
        mock_get.return_value = mock_character

        with (
            patch(
                "allianceauth.eveonline.models.EveAllianceInfo.objects.filter"
            ) as mock_alliance_filter,
            patch(
                "allianceauth.eveonline.models.EveAllianceInfo.objects.create_alliance"
            ) as mock_create_alliance,
        ):
            mock_alliance_filter.return_value.exists.return_value = False
            mock_create_alliance.return_value = EveAllianceInfo(alliance_id=67890)

            result = get_or_create_character(name="New Character")
            self.assertEqual(result, mock_character)
            mock_create_alliance.assert_called_once_with(alliance_id=67890)
