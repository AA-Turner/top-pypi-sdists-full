from datetime import datetime, timezone
from types import SimpleNamespace
from unittest import mock

from django.db.utils import IntegrityError
from django.test import TestCase

from esi.exceptions import HTTPNotModified

from ..models import (
    EveAllianceInfo, EveCharacter, EveCorporationInfo, EveFactionInfo,
)


def response_stub() -> SimpleNamespace:
    return SimpleNamespace(
        headers={
            "Date": "Tue, 20 May 2025 13:24:00 GMT",
            "Last-Modified": "Tue, 20 May 2025 13:24:00 GMT",
        }
    )


class EveCharacterManagerTestCase(TestCase):
    def test_exclude_biomassed(self) -> None:
        alive = EveCharacter.objects.create(
            character_id=1234,
            character_name="Alive",
            corporation_id=2001,
            corporation_name="Alive Corp",
            corporation_ticker="AC1",
        )
        EveCharacter.objects.create(
            character_id=1666,
            character_name="Biomassed",
            corporation_id=1000001,
            corporation_name="Doomheim",
            corporation_ticker="DOOM",
        )

        self.assertQuerySetEqual(
            EveCharacter.objects.exclude_biomassed(),
            [alive],
            transform=lambda obj: obj,
        )

    @mock.patch("allianceauth.eveonline.managers.open_api_provider.get_affiliations")
    @mock.patch("allianceauth.eveonline.managers.open_api_provider.get_character")
    def test_create_character_1_with_existing_alliance_and_without_faction(
        self, provider_get_character, provider_get_affiliations
    ) -> None:
        alliance = EveAllianceInfo.objects.create(
            alliance_id=3001,
            alliance_name="Test Alliance",
            alliance_ticker="TEST",
            executor_corp_id=2001,
        )
        faction = EveFactionInfo.objects.create(
            faction_id=1337,
            faction_name="Test Faction",
        )
        EveCorporationInfo.objects.create(
            corporation_id=2001,
            corporation_name="Test Corp",
            corporation_ticker="TC1",
            member_count=1,
            alliance=alliance,
            faction=faction,
        )
        provider_get_character.return_value = (
            SimpleNamespace(
                corporation_id=2001,
                alliance_id=3001,
                faction_id=None,
                birthday=None,
                bloodline_id=None,
                description="",
                gender="",
                name="Test Character",
                race_id=None,
                security_status=0.0,
                title="",
            ),
            response_stub(),
        )
        provider_get_affiliations.return_value = (
            [
                SimpleNamespace(
                    character_id=1234,
                    corporation_id=2001,
                    alliance_id=3001,
                    faction_id=None,
                )
            ],
            response_stub(),
        )

        with mock.patch.object(
            EveCharacter.objects,
            "create",
            side_effect=lambda **kwargs: SimpleNamespace(**kwargs),
        ):
            result = EveCharacter.objects.create_character(1234)

        self.assertEqual(result.character_id, 1234)
        self.assertEqual(result.character_name, "Test Character")
        self.assertEqual(result.corporation_id, 2001)
        self.assertEqual(result.corporation_name, "Test Corp")
        self.assertEqual(result.alliance_id, 3001)
        self.assertEqual(result.alliance_name, "Test Alliance")
        self.assertEqual(result.alliance_ticker, "TEST")
        self.assertIsNone(result.faction_id)
        self.assertEqual(result.faction_name, "")

    @mock.patch("allianceauth.eveonline.managers.open_api_provider.get_affiliations")
    @mock.patch("allianceauth.eveonline.managers.open_api_provider.get_character")
    def test_create_character_2_with_existing_faction_birthday_bloodline_and_race(
        self, provider_get_character, provider_get_affiliations
    ) -> None:
        birthday = datetime(2023, 7, 14, 8, 30, tzinfo=timezone.utc)
        faction = EveFactionInfo.objects.create(
            faction_id=4009,
            faction_name="Created Faction",
        )
        EveCorporationInfo.objects.create(
            corporation_id=2009,
            corporation_name="Created Corp",
            corporation_ticker="CC1",
            member_count=1,
            faction=faction,
        )
        provider_get_character.return_value = (
            SimpleNamespace(
                corporation_id=2009,
                alliance_id=None,
                faction_id=4009,
                birthday=birthday,
                bloodline_id=12,
                description="",
                gender="Male",
                name="Typed Character",
                race_id=8,
                security_status=0.0,
                title="",
            ),
            response_stub(),
        )
        provider_get_affiliations.return_value = (
            [
                SimpleNamespace(
                    character_id=4323,
                    corporation_id=2009,
                    alliance_id=None,
                    faction_id=4009,
                )
            ],
            response_stub(),
        )

        with mock.patch.object(
            EveCharacter.objects,
            "create",
            side_effect=lambda **kwargs: SimpleNamespace(**kwargs),
        ):
            result = EveCharacter.objects.create_character(4323)

        self.assertEqual(result.faction_id, faction.faction_id)
        self.assertEqual(result.faction_name, faction.faction_name)
        self.assertEqual(result.birthday, birthday)
        self.assertEqual(result.bloodline_id, 12)
        self.assertEqual(result.race_id, 8)

    @mock.patch("allianceauth.eveonline.managers.open_api_provider.get_affiliations")
    @mock.patch("allianceauth.eveonline.managers.open_api_provider.get_character")
    def test_create_character_3_without_alliance_sets_empty_cached_alliance(
        self, provider_get_character, provider_get_affiliations
    ) -> None:
        faction = EveFactionInfo.objects.create(
            faction_id=4009,
            faction_name="Created Faction",
        )
        EveCorporationInfo.objects.create(
            corporation_id=2009,
            corporation_name="Created Corp",
            corporation_ticker="CC1",
            member_count=1,
        )
        provider_get_character.return_value = (
            SimpleNamespace(
                corporation_id=2009,
                alliance_id=None,
                faction_id=4009,
                birthday=None,
                bloodline_id=None,
                description="",
                gender="Male",
                name="No Alliance",
                race_id=None,
                security_status=0.0,
                title="",
            ),
            response_stub(),
        )
        provider_get_affiliations.return_value = (
            [
                SimpleNamespace(
                    character_id=4322,
                    corporation_id=2009,
                    alliance_id=None,
                    faction_id=4009,
                )
            ],
            response_stub(),
        )

        with mock.patch.object(
            EveCharacter.objects,
            "create",
            side_effect=lambda **kwargs: SimpleNamespace(**kwargs),
        ):
            result = EveCharacter.objects.create_character(4322)

        self.assertIsNone(result.alliance_id)
        self.assertEqual(result.alliance_name, "")
        self.assertEqual(result.alliance_ticker, "")
        self.assertEqual(result.faction_id, faction.faction_id)
        self.assertEqual(result.faction_name, faction.faction_name)

    @mock.patch("allianceauth.eveonline.managers.open_api_provider.get_affiliations")
    @mock.patch("allianceauth.eveonline.managers.open_api_provider.get_character")
    def test_create_character_4_creates_missing_related_objects(
        self, provider_get_character, provider_get_affiliations
    ) -> None:
        provider_get_character.return_value = (
            SimpleNamespace(
                corporation_id=2009,
                alliance_id=3009,
                faction_id=4009,
                birthday=None,
                bloodline_id=None,
                description="bio",
                gender="Male",
                name="Missing Relations",
                race_id=None,
                security_status=1.5,
                title="CEO",
            ),
            response_stub(),
        )
        provider_get_affiliations.return_value = (
            [
                SimpleNamespace(
                    character_id=4321,
                    corporation_id=2009,
                    alliance_id=3009,
                    faction_id=4009,
                )
            ],
            response_stub(),
        )

        with mock.patch.object(
            EveCorporationInfo.objects,
            "create_corporation",
            return_value=SimpleNamespace(
                corporation_name="Created Corp",
                corporation_ticker="CC1",
            ),
        ) as mock_create_corporation, mock.patch.object(
            EveAllianceInfo.objects,
            "create_alliance",
            return_value=SimpleNamespace(
                alliance_name="Created Alliance",
                alliance_ticker="CA1",
            ),
        ) as mock_create_alliance, mock.patch.object(
            EveFactionInfo.objects,
            "create_faction",
            return_value=SimpleNamespace(
                faction_name="Created Faction",
            ),
        ) as mock_create_faction, mock.patch.object(
            EveCharacter.objects,
            "create",
            side_effect=lambda **kwargs: SimpleNamespace(**kwargs),
        ):
            result = EveCharacter.objects.create_character(4321)

        mock_create_corporation.assert_called_once_with(corporation_id=2009)
        mock_create_alliance.assert_called_once_with(alliance_id=3009)
        mock_create_faction.assert_called_once_with(faction_id=4009)
        self.assertEqual(result.corporation_name, "Created Corp")
        self.assertEqual(result.alliance_name, "Created Alliance")
        self.assertEqual(result.faction_id, 4009)
        self.assertEqual(result.faction_name, "Created Faction")

    @mock.patch("allianceauth.eveonline.models.open_api_provider.get_affiliations")
    def test_update_character(self, provider_get_affiliations) -> None:
        alliance = EveAllianceInfo.objects.create(
            alliance_id=3001,
            alliance_name="Test Alliance",
            alliance_ticker="TEST",
            executor_corp_id=2001,
        )
        faction = EveFactionInfo.objects.create(
            faction_id=1337,
            faction_name="Test Faction",
        )
        EveCorporationInfo.objects.create(
            corporation_id=2001,
            corporation_name="Test Corp",
            corporation_ticker="TC1",
            member_count=1,
            alliance=alliance,
            faction=faction,
        )
        EveCharacter.objects.create(
            character_id=1234,
            character_name="Old Character",
            corporation_id=2001,
            corporation_name="Old Corp",
            corporation_ticker="OC1",
            alliance_id=3001,
            alliance_name="Old Alliance",
            alliance_ticker="OLD",
            faction_id=1337,
            faction_name="Old Faction",
        )
        provider_get_affiliations.return_value = (
            [
                SimpleNamespace(
                    character_id=1234,
                    corporation_id=2001,
                    alliance_id=None,
                    faction_id=None,
                )
            ],
            response_stub(),
        )

        result = EveCharacter.objects.update_character(1234)

        self.assertEqual(result.character_name, "Old Character")
        self.assertEqual(result.corporation_name, "Test Corp")
        self.assertIsNone(result.alliance_id)
        self.assertIsNone(result.faction_id)

    def test_get_character_by_id(self) -> None:
        EveCharacter.objects.create(
            character_id=1234,
            character_name="character.name",
            corporation_id=2345,
            corporation_name="character.corp.name",
            corporation_ticker="cc1",
            alliance_id=3456,
            alliance_name="character.alliance.name",
        )

        result = EveCharacter.objects.get_character_by_id(1234)

        self.assertEqual(result.character_id, 1234)
        self.assertEqual(result.character_name, "character.name")
        self.assertIsNone(EveCharacter.objects.get_character_by_id(9999))


class EveAllianceManagerTestCase(TestCase):
    @mock.patch("allianceauth.eveonline.managers.open_api_provider.get_alliance")
    def test_create_alliance(self, provider_get_alliance) -> None:
        provider_get_alliance.return_value = (
            SimpleNamespace(
                name="Test Alliance",
                ticker="TEST",
                executor_corporation_id=2345,
                faction_id=None,
                creator_corporation_id=None,
                creator_id=None,
                date_founded=None,
            ),
            response_stub(),
        )

        result = EveAllianceInfo.objects.create_alliance(3456)

        self.assertEqual(result.alliance_id, 3456)
        self.assertEqual(result.alliance_name, "Test Alliance")
        self.assertEqual(result.executor_corp_id, 2345)

    @mock.patch("allianceauth.eveonline.managers.open_api_provider.get_alliance")
    def test_create_alliance_with_faction(self, provider_get_alliance) -> None:
        provider_get_alliance.return_value = (
            SimpleNamespace(
                name="Test Alliance",
                ticker="TEST",
                executor_corporation_id=2345,
                faction_id=1337,
                creator_corporation_id=None,
                creator_id=None,
                date_founded=None,
            ),
            response_stub(),
        )

        with mock.patch.object(
            EveFactionInfo.objects,
            "create_faction",
            return_value=EveFactionInfo(faction_id=1337, faction_name="Faction"),
        ), mock.patch.object(
            EveAllianceInfo.objects,
            "create",
            side_effect=lambda **kwargs: SimpleNamespace(**kwargs),
        ):
            result = EveAllianceInfo.objects.create_alliance(3456)

        self.assertEqual(result.faction.faction_id, 1337)

    def test_get_or_create_esi_returns_existing_alliance(self) -> None:
        alliance = EveAllianceInfo.objects.create(
            alliance_id=3456,
            alliance_name="Existing Alliance",
            alliance_ticker="EXI",
            executor_corp_id=2345,
        )

        result = EveAllianceInfo.objects.get_or_create_esi(3456)

        self.assertEqual(result, alliance)

    def test_get_or_create_esi_handles_integrity_error_for_alliance(self) -> None:
        existing = EveAllianceInfo.objects.create(
            alliance_id=3456,
            alliance_name="Existing Alliance",
            alliance_ticker="EXI",
            executor_corp_id=2345,
        )

        with mock.patch.object(
            EveAllianceInfo.objects,
            "get",
            side_effect=[EveAllianceInfo.DoesNotExist, existing],
        ), mock.patch.object(
            EveAllianceInfo.objects,
            "create_alliance",
            side_effect=IntegrityError,
        ):
            result = EveAllianceInfo.objects.get_or_create_esi(3456)

        self.assertEqual(result, existing)

    @mock.patch("allianceauth.eveonline.managers.open_api_provider.get_alliance")
    def test_update_alliance(self, provider_get_alliance) -> None:
        EveAllianceInfo.objects.create(
            alliance_id=3456,
            alliance_name="Old Alliance",
            alliance_ticker="OLD",
            executor_corp_id=2345,
        )
        provider_get_alliance.return_value = (
            SimpleNamespace(
                name="Updated Alliance",
                ticker="UPD",
                executor_corporation_id=2001,
                faction_id=None,
                creator_corporation_id=None,
                creator_id=None,
                date_founded=None,
            ),
            response_stub(),
        )

        result = EveAllianceInfo.objects.update_alliance(3456)

        self.assertEqual(result.executor_corp_id, 2001)
        self.assertEqual(result.alliance_name, "Updated Alliance")


class EveCorporationManagerTestCase(TestCase):
    def test_exclude_closed(self) -> None:
        open_corp = EveCorporationInfo.objects.create(
            corporation_id=2345,
            corporation_name="Open Corp",
            corporation_ticker="OPEN",
            member_count=10,
            ceo_id=1001,
        )
        EveCorporationInfo.objects.create(
            corporation_id=2346,
            corporation_name="Closed Corp",
            corporation_ticker="CLOS",
            member_count=0,
            ceo_id=1,
        )

        self.assertQuerySetEqual(
            EveCorporationInfo.objects.exclude_closed(),
            [open_corp],
            transform=lambda obj: obj,
        )

    @mock.patch("allianceauth.eveonline.managers.open_api_provider.get_corporation")
    def test_create_corporation(self, provider_get_corporation) -> None:
        alliance = EveAllianceInfo.objects.create(
            alliance_id=3456,
            alliance_name="Test Alliance",
            alliance_ticker="TEST",
            executor_corp_id=2345,
        )
        provider_get_corporation.return_value = (
            SimpleNamespace(
                alliance_id=3456,
                faction_id=None,
                ceo_id=1234,
                creator_id=None,
                date_founded=None,
                description="",
                home_station_id=None,
                member_count=1,
                name="Test Corp",
                shares=None,
                tax_rate=None,
                ticker="0BUGS",
                url="",
                war_eligible=False,
            ),
            response_stub(),
        )

        result = EveCorporationInfo.objects.create_corporation(2345)

        self.assertEqual(result.corporation_id, 2345)
        self.assertEqual(result.corporation_name, "Test Corp")
        self.assertEqual(result.alliance, alliance)

    @mock.patch("allianceauth.eveonline.managers.open_api_provider.get_corporation")
    def test_create_corporation_creates_missing_related_objects(
        self, provider_get_corporation
    ) -> None:
        provider_get_corporation.return_value = (
            SimpleNamespace(
                alliance_id=3456,
                faction_id=1337,
                ceo_id=1234,
                creator_id=None,
                date_founded=None,
                description="",
                home_station_id=None,
                member_count=1,
                name="Test Corp",
                shares=None,
                tax_rate=0.5,
                ticker="0BUGS",
                url="",
                war_eligible=False,
            ),
            response_stub(),
        )

        with mock.patch.object(
            EveAllianceInfo.objects,
            "create_alliance",
            return_value=EveAllianceInfo(
                alliance_id=3456,
                alliance_name="Created Alliance",
                alliance_ticker="CA1",
            ),
        ), mock.patch.object(
            EveFactionInfo.objects,
            "create_faction",
            return_value=EveFactionInfo(
                faction_id=1337,
                faction_name="Created Faction",
            ),
        ), mock.patch.object(
            EveCorporationInfo.objects,
            "create",
            side_effect=lambda **kwargs: SimpleNamespace(**kwargs),
        ):
            result = EveCorporationInfo.objects.create_corporation(2345)

        self.assertEqual(result.alliance.alliance_id, 3456)
        self.assertEqual(result.faction.faction_id, 1337)

    @mock.patch("allianceauth.eveonline.managers.open_api_provider.get_corporation")
    def test_create_corporation_no_alliance(self, provider_get_corporation) -> None:
        provider_get_corporation.return_value = (
            SimpleNamespace(
                alliance_id=None,
                faction_id=None,
                ceo_id=1234,
                creator_id=None,
                date_founded=None,
                description="",
                home_station_id=None,
                member_count=1,
                name="Test Corp",
                shares=None,
                tax_rate=None,
                ticker="0BUGS",
                url="",
                war_eligible=False,
            ),
            response_stub(),
        )

        result = EveCorporationInfo.objects.create_corporation(2345)

        self.assertEqual(result.corporation_id, 2345)
        self.assertIsNone(result.alliance)

    @mock.patch("allianceauth.eveonline.managers.open_api_provider.get_corporation")
    def test_update_corporation(self, provider_get_corporation) -> None:
        alliance = EveAllianceInfo.objects.create(
            alliance_id=3456,
            alliance_name="Old Alliance",
            alliance_ticker="OLD",
            executor_corp_id=2345,
        )
        EveCorporationInfo.objects.create(
            corporation_id=2345,
            corporation_name="Old Corp",
            corporation_ticker="OLD",
            member_count=10,
            alliance=alliance,
        )
        provider_get_corporation.return_value = (
            SimpleNamespace(
                alliance_id=3456,
                faction_id=None,
                ceo_id=1234,
                creator_id=None,
                date_founded=None,
                description="",
                home_station_id=None,
                member_count=22,
                name="Updated Corp",
                shares=None,
                tax_rate=None,
                ticker="UPD",
                url="",
                war_eligible=False,
            ),
            response_stub(),
        )

        result = EveCorporationInfo.objects.update_corporation(2345)

        self.assertEqual(result.member_count, 22)
        self.assertEqual(result.corporation_name, "Updated Corp")

    def test_get_or_create_esi_returns_existing_corporation(self) -> None:
        corporation = EveCorporationInfo.objects.create(
            corporation_id=2345,
            corporation_name="Existing Corp",
            corporation_ticker="EXI",
            member_count=10,
        )

        result = EveCorporationInfo.objects.get_or_create_esi(2345)

        self.assertEqual(result, corporation)

    def test_get_or_create_esi_handles_integrity_error_for_corporation(self) -> None:
        existing = EveCorporationInfo.objects.create(
            corporation_id=2345,
            corporation_name="Existing Corp",
            corporation_ticker="EXI",
            member_count=10,
        )

        with mock.patch.object(
            EveCorporationInfo.objects,
            "get",
            side_effect=[EveCorporationInfo.DoesNotExist, existing],
        ), mock.patch.object(
            EveCorporationInfo.objects,
            "create_corporation",
            side_effect=IntegrityError,
        ):
            result = EveCorporationInfo.objects.get_or_create_esi(2345)

        self.assertEqual(result, existing)


class EveFactionManagerTestCase(TestCase):
    @mock.patch("allianceauth.eveonline.managers.open_api_provider.get_faction")
    def test_create_faction(self, provider_get_faction) -> None:
        provider_get_faction.return_value = (
            SimpleNamespace(
                faction_id=1337,
                corporation_id=2001,
                description="Faction description",
                militia_corporation_id=2002,
                name="Test Faction",
                size_factor=1,
                solar_system_id=30000142,
                station_count=10,
                station_system_count=5,
            ),
            response_stub(),
        )

        result = EveFactionInfo.objects.create_faction(1337)

        self.assertEqual(result.faction_name, "Test Faction")
        self.assertEqual(result.corporation_id, 2001)
        self.assertEqual(result.militia_corporation_id, 2002)

    def test_get_or_create_esi_returns_existing_faction(self) -> None:
        faction = EveFactionInfo.objects.create(
            faction_id=1337,
            faction_name="Existing Faction",
        )

        result = EveFactionInfo.objects.get_or_create_esi(1337)

        self.assertEqual(result, faction)

    def test_get_or_create_esi_handles_integrity_error_for_faction(self) -> None:
        existing = EveFactionInfo.objects.create(
            faction_id=1337,
            faction_name="Existing Faction",
        )

        with mock.patch.object(
            EveFactionInfo.objects,
            "get",
            side_effect=[EveFactionInfo.DoesNotExist, existing],
        ), mock.patch.object(
            EveFactionInfo.objects,
            "create_faction",
            side_effect=IntegrityError,
        ):
            result = EveFactionInfo.objects.get_or_create_esi(1337)

        self.assertEqual(result, existing)

    @mock.patch("allianceauth.eveonline.managers.open_api_provider.get_all_factions")
    def test_update_factions_returns_self_when_not_modified(
        self, provider_get_all_factions
    ) -> None:
        provider_get_all_factions.side_effect = HTTPNotModified(status_code=304, headers={})

        result = EveFactionInfo.objects.update_factions()

        self.assertEqual(result, EveFactionInfo.objects)

    @mock.patch("allianceauth.eveonline.managers.open_api_provider.get_all_factions")
    def test_update_factions_updates_existing_and_new_values(
        self, provider_get_all_factions
    ) -> None:
        faction = EveFactionInfo.objects.create(
            faction_id=1337,
            faction_name="Old Faction",
            description="Old",
        )
        provider_get_all_factions.return_value = (
            [
                SimpleNamespace(
                    faction_id=1337,
                    corporation_id=2001,
                    description="New Description",
                    militia_corporation_id=2002,
                    name="Updated Faction",
                    size_factor=0,
                    solar_system_id=0,
                    station_count=0,
                    station_system_count=0,
                )
            ],
            response_stub(),
        )

        EveFactionInfo.objects.update_factions()
        faction.refresh_from_db()

        self.assertEqual(faction.faction_name, "Updated Faction")
        self.assertEqual(faction.corporation_id, 2001)
        self.assertEqual(faction.description, "New Description")
        self.assertIsNone(faction.size_factor)
        self.assertIsNone(faction.solar_system_id)
        self.assertIsNone(faction.station_count)
        self.assertIsNone(faction.station_system_count)
