from types import SimpleNamespace
from typing import Any, cast
from unittest.mock import patch

from django.test import TestCase, TransactionTestCase, override_settings

from esi.exceptions import HTTPClientError

from ..models import EveAllianceInfo, EveCharacter, EveCorporationInfo
from ..tasks import (
    chunks, run_model_update, update_all_factions, update_alliance,
    update_character, update_character_chunk, update_corp,
)
from .esi_client_stub import EsiClientStub


class TestUpdateTasks(TestCase):
    def test_should_update_alliance(self) -> None:
        with patch("allianceauth.eveonline.tasks.EveAllianceInfo.objects.get") as mock_get_alliance:
            mock_alliance = mock_get_alliance.return_value

            update_alliance(3001)

            self.assertEqual(mock_get_alliance.call_count, 2)
            mock_get_alliance.assert_any_call(alliance_id=3001)
            mock_alliance.update_alliance.assert_called_once_with()
            mock_alliance.populate_alliance.assert_called_once_with()

    def test_should_update_character(self) -> None:
        # given
        with patch("allianceauth.eveonline.providers.open_api_provider._client", EsiClientStub()):
            my_character = EveCharacter.objects.create(
                character_id=1001,
                character_name="Bruce Wayne",
                corporation_id=2002,
                corporation_name="Wayne Food",
                corporation_ticker="WYF",
                alliance_id=None
            )
            # when
            update_character(my_character.character_id)
            # then
            my_character.refresh_from_db()
            self.assertEqual(my_character.corporation_id, 2001)

    def test_should_update_corp(self) -> None:
        # given
        with patch("allianceauth.eveonline.providers.open_api_provider._client", EsiClientStub()):
            EveAllianceInfo.objects.create(
                alliance_id=3001,
                alliance_name="Wayne Enterprises",
                alliance_ticker="WYE",
                executor_corp_id=2003
            )
            my_corporation = EveCorporationInfo.objects.create(
                corporation_id=2003,
                corporation_name="Wayne Food",
                corporation_ticker="WFO",
                member_count=1,
                alliance=None,
                ceo_id=1999
            )
            # when
            update_corp(my_corporation.corporation_id)
            # then
            my_corporation.refresh_from_db()
            self.assertIsNotNone(my_corporation.alliance)
            assert my_corporation.alliance is not None
            self.assertEqual(my_corporation.alliance.alliance_id, 3001)

    def test_should_update_all_factions(self) -> None:
        with patch(
            "allianceauth.eveonline.tasks.EveFactionInfo.objects.update_factions"
        ) as mock_update_factions:
            update_all_factions()

            mock_update_factions.assert_called_once_with()

    # @patch('allianceauth.eveonline.tasks.EveCharacter')
    # def test_update_character(self, mock_EveCharacter):
    #     update_character(42)
    #     self.assertEqual(
    #         mock_EveCharacter.objects.update_character.call_count, 1
    #     )
    #     self.assertEqual(
    #         mock_EveCharacter.objects.update_character.call_args[0][0], 42
    #     )


@override_settings(CELERY_ALWAYS_EAGER=True)
@patch('allianceauth.eveonline.tasks.update_character_chunk')
@patch('allianceauth.eveonline.tasks.update_alliance')
@patch('allianceauth.eveonline.tasks.update_corp')
@patch('allianceauth.eveonline.tasks.CHARACTER_AFFILIATION_CHUNK_SIZE', 2)
class TestRunModelUpdate(TransactionTestCase):
    def test_should_run_updates(
        self,
        spy_update_corp,
        spy_update_alliance,
        spy_update_character_chunk,
    ) -> None:
        # given
        with patch("allianceauth.eveonline.providers.open_api_provider._client", EsiClientStub()):
            EveCorporationInfo.objects.create(
                corporation_id=2001,
                corporation_name="Wayne Technologies",
                corporation_ticker="WTE",
                member_count=10,
                alliance=None,
            )
            EveAllianceInfo.objects.create(
                alliance_id=3001,
                alliance_name="Wayne Enterprises",
                alliance_ticker="WYE",
                executor_corp_id=2003
            )
            EveCorporationInfo.objects.create(
                corporation_id=2003,
                corporation_name="Wayne Energy",
                corporation_ticker="WEG",
                member_count=99,
                alliance=None,
            )
            character_1001 = EveCharacter.objects.create(
                character_id=1001,
                character_name="Bruce Wayne",
                corporation_id=2002,
                corporation_name="Wayne Food",
                corporation_ticker="WYF",
                alliance_id=None
            )
            # when
            run_model_update()
            # then
            self.assertSetEqual(
                {x.kwargs["args"][0] for x in spy_update_corp.apply_async.call_args_list},
                {2001, 2003},
            )
            self.assertSetEqual(
                {x.kwargs["args"][0] for x in spy_update_alliance.apply_async.call_args_list},
                {3001},
            )
            self.assertEqual(
                [x.kwargs["args"][0] for x in spy_update_character_chunk.apply_async.call_args_list],
                [[character_1001.character_id]],
            )


class TestChunks(TestCase):
    def test_should_split_list_into_remainder_chunk(self) -> None:
        self.assertEqual(list(chunks([1, 2, 3], 2)), [[1, 2], [3]])


@override_settings(CELERY_ALWAYS_EAGER=True)
@patch('allianceauth.eveonline.tasks.update_character', wraps=update_character)
@patch('allianceauth.eveonline.tasks.CHARACTER_AFFILIATION_CHUNK_SIZE', 2)
class TestUpdateCharacterChunk(TestCase):
    @staticmethod
    def _updated_character_ids(spy_update_character) -> set:
        """Character IDs passed to update_character task for update."""
        return {
            x[1]["args"][0] for x in spy_update_character.apply_async.call_args_list
        }

    def test_should_update_corp_change(
        self, spy_update_character
    ) -> None:
        # given
        with patch("allianceauth.eveonline.providers.open_api_provider._client", EsiClientStub()):
            character_1001 = EveCharacter.objects.create(
                character_id=1001,
                character_name="Bruce Wayne",
                corporation_id=2003,
                corporation_name="Wayne Energy",
                corporation_ticker="WEG",
                alliance_id=3001,
                alliance_name="Wayne Enterprises",
                alliance_ticker="WYE",
            )
            character_1002 = EveCharacter.objects.create(
                character_id=1002,
                character_name="Peter Parker",
                corporation_id=2001,
                corporation_name="Wayne Technologies",
                corporation_ticker="WTE",
                alliance_id=3001,
                alliance_name="Wayne Enterprises",
                alliance_ticker="WYE",
            )
            # when
            update_character_chunk([
                character_1001.character_id, character_1002.character_id
            ])
            # then
            self.assertSetEqual(self._updated_character_ids(spy_update_character), {1001})

    def test_should_update_name_change(
        self, spy_update_character
    ) -> None:
        # given
        with patch("allianceauth.eveonline.providers.open_api_provider._client", EsiClientStub()):
            character_1001 = EveCharacter.objects.create(
                character_id=1001,
                character_name="Batman",
                corporation_id=2001,
                corporation_name="Wayne Technologies",
                corporation_ticker="WTE",
                alliance_id=3001,
                alliance_name="Wayne Technologies",
                alliance_ticker="WYT",
            )
            # when
            update_character_chunk([character_1001.character_id])
            # then
            self.assertSetEqual(self._updated_character_ids(spy_update_character), {1001})

    def test_should_update_alliance_change(
        self, spy_update_character
    ) -> None:
        # given
        with patch("allianceauth.eveonline.providers.open_api_provider._client", EsiClientStub()):
            character_1001 = EveCharacter.objects.create(
                character_id=1001,
                character_name="Bruce Wayne",
                corporation_id=2001,
                corporation_name="Wayne Technologies",
                corporation_ticker="WTE",
                alliance_id=None,
            )
            # when
            update_character_chunk([character_1001.character_id])
            # then
            self.assertSetEqual(self._updated_character_ids(spy_update_character), {1001})

    def test_should_ignore_name_change_when_bulk_names_missing(
        self, spy_update_character
    ) -> None:
        with patch(
            "allianceauth.eveonline.tasks.open_api_provider.get_affiliations",
            return_value=[
                SimpleNamespace(
                    character_id=1001,
                    corporation_id=2001,
                    alliance_id=3001,
                    name=None,
                )
            ],
        ), patch(
            "allianceauth.eveonline.tasks.open_api_provider.post_names",
            return_value=[],
        ):
            EveCharacter.objects.create(
                character_id=1001,
                character_name="Bruce Wayne",
                corporation_id=2001,
                corporation_name="Wayne Technologies",
                corporation_ticker="WTE",
                alliance_id=3001,
                alliance_name="Wayne Enterprises",
                alliance_ticker="WYE",
            )

            update_character_chunk([1001])

            self.assertSetEqual(self._updated_character_ids(spy_update_character), set())

    def test_should_ignore_unmatched_bulk_names(
        self, spy_update_character
    ) -> None:
        with patch(
            "allianceauth.eveonline.tasks.open_api_provider.get_affiliations",
            return_value=[
                SimpleNamespace(
                    character_id=1001,
                    corporation_id=2001,
                    alliance_id=3001,
                    name=None,
                )
            ],
        ), patch(
            "allianceauth.eveonline.tasks.open_api_provider.post_names",
            return_value=[SimpleNamespace(id=9999, name="Not Bruce Wayne")],
        ):
            EveCharacter.objects.create(
                character_id=1001,
                character_name="Bruce Wayne",
                corporation_id=2001,
                corporation_name="Wayne Technologies",
                corporation_ticker="WTE",
                alliance_id=3001,
                alliance_name="Wayne Enterprises",
                alliance_ticker="WYE",
            )

            update_character_chunk([1001])

            self.assertSetEqual(self._updated_character_ids(spy_update_character), set())

    def test_should_not_update_when_not_changed(
        self, spy_update_character
    ) -> None:
        # given
        with patch("allianceauth.eveonline.providers.open_api_provider._client", EsiClientStub()):
            character_1001 = EveCharacter.objects.create(
                character_id=1001,
                character_name="Bruce Wayne",
                corporation_id=2001,
                corporation_name="Wayne Technologies",
                corporation_ticker="WTE",
                alliance_id=3001,
                alliance_name="Wayne Technologies",
                alliance_ticker="WYT",
            )
            # when
            update_character_chunk([character_1001.character_id])
            # then
            self.assertSetEqual(self._updated_character_ids(spy_update_character), set())

    def test_should_not_update_when_affiliation_missing(
        self, spy_update_character
    ) -> None:
        with patch(
            "allianceauth.eveonline.tasks.open_api_provider.get_affiliations",
            return_value=[],
        ), patch(
            "allianceauth.eveonline.tasks.open_api_provider.post_names",
            return_value=[],
        ):
            EveCharacter.objects.create(
                character_id=1001,
                character_name="Bruce Wayne",
                corporation_id=2001,
                corporation_name="Wayne Technologies",
                corporation_ticker="WTE",
                alliance_id=3001,
                alliance_name="Wayne Enterprises",
                alliance_ticker="WYE",
            )

            update_character_chunk([1001])

            self.assertSetEqual(self._updated_character_ids(spy_update_character), set())

    def test_should_fall_back_to_single_updates_when_bulk_update_failed(
        self, spy_update_character
    ) -> None:
        # given
        with patch(
            "allianceauth.eveonline.tasks.open_api_provider.get_affiliations",
            side_effect=HTTPClientError(
                status_code=403,
                headers={},
                data=cast(Any, {}),
            ),
        ), patch(
            "allianceauth.eveonline.tasks.open_api_provider.post_names",
            return_value=[],
        ):
            with patch("allianceauth.eveonline.providers.open_api_provider._client", EsiClientStub()):
                character_1001 = EveCharacter.objects.create(
                    character_id=1001,
                    character_name="Bruce Wayne",
                    corporation_id=2001,
                    corporation_name="Wayne Technologies",
                    corporation_ticker="WTE",
                    alliance_id=3001,
                    alliance_name="Wayne Technologies",
                    alliance_ticker="WYT",
                )
                # when
                update_character_chunk([character_1001.character_id])
                # then
                self.assertSetEqual(self._updated_character_ids(spy_update_character), {1001})
