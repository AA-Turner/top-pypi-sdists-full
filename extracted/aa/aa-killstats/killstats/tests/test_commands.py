# Standard Library
from io import StringIO
from unittest.mock import Mock, patch

# Third Party
# Alliance Auth (Factories)
from evesde_factory.allianceauth import (
    EveAllianceInfoFactory,
    EveCharacterFactory,
    EveCorporationInfoFactory,
)
from evesde_factory.eve_sde import SolarSystemFactory

# Django
from django.core.cache import cache
from django.core.management import call_command

# AA Killstats
from killstats.models.general import EveEntity
from killstats.models.killboard import Attacker, Killmail
from killstats.models.killstatsaudit import CorporationsAudit
from killstats.tests import AuthTestCase
from killstats.tests.testdata.killstats import (
    AlliancesAuditFactory,
    AttackerFactory,
    CorporationsAuditFactory,
    EveEntityFactory,
    KillmailFactory,
)


class TestKillstatsDeleteNpcKillmails(AuthTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()

        # Set up a player audited corporation
        cls.player_corp = EveCorporationInfoFactory()
        cls.player_char = EveCharacterFactory(corporation=cls.player_corp)
        cls.corp_audit = CorporationsAuditFactory(
            corporation=cls.player_corp,
            owner=cls.player_char,
        )

        # Set up a player audited alliance
        cls.player_alliance = EveAllianceInfoFactory(
            executor_corp_id=cls.player_corp.corporation_id,
        )
        cls.alliance_audit = AlliancesAuditFactory(
            alliance=cls.player_alliance,
            owner=cls.player_char,
        )

    def test_no_killmails_found(self):
        out = StringIO()
        call_command("killstats_delete_npc_killmails", "--yes", stdout=out)
        output = out.getvalue()
        self.assertIn("Found 0 killmail(s)", output)
        self.assertIn("No NPC killmails or NPC audits found to delete", output)

    def test_protected_killmails_not_deleted(self):
        # 1. Killmail where victim is player corp, attacker is NPC corp (1000125)
        km1 = KillmailFactory(
            victim_corporation_id=self.player_corp.corporation_id,
            victim_alliance_id=self.player_alliance.alliance_id,
        )
        npc_entity = EveEntityFactory(
            id=1000125,
            category=EveEntity.CATEGORY_CORPORATION,
        )
        AttackerFactory(
            killmail=km1,
            corporation=npc_entity,
        )

        # 2. Killmail where attacker is player corp, victim is NPC corp (1000035)
        km2 = KillmailFactory(
            victim_corporation_id=1000035,
        )
        player_entity = EveEntityFactory(
            id=self.player_corp.corporation_id,
            category=EveEntity.CATEGORY_CORPORATION,
        )
        AttackerFactory(
            killmail=km2,
            corporation=player_entity,
        )

        out = StringIO()
        call_command("killstats_delete_npc_killmails", "--yes", stdout=out)
        output = out.getvalue()

        self.assertIn("Found 0 killmail(s)", output)
        self.assertTrue(Killmail.objects.filter(killmail_id=km1.killmail_id).exists())
        self.assertTrue(Killmail.objects.filter(killmail_id=km2.killmail_id).exists())

    def test_npc_killmail_deleted_with_yes_flag(self):
        # NPC killmail completely unconnected to any audit
        km = KillmailFactory(
            victim_corporation_id=1000035,
        )
        npc_entity = EveEntityFactory(
            id=1000125,
            category=EveEntity.CATEGORY_CORPORATION,
        )
        AttackerFactory(
            killmail=km,
            corporation=npc_entity,
        )

        out = StringIO()
        call_command("killstats_delete_npc_killmails", "--yes", stdout=out)
        output = out.getvalue()

        self.assertIn("Found 1 killmail(s)", output)
        self.assertIn("Successfully deleted 1 NPC killmail(s)", output)
        self.assertFalse(Killmail.objects.filter(killmail_id=km.killmail_id).exists())
        self.assertFalse(Attacker.objects.filter(killmail_id=km.killmail_id).exists())

    @patch("builtins.input", return_value="n")
    def test_npc_killmail_cancelled_by_user(self, mock_input):
        km = KillmailFactory(
            victim_corporation_id=1000035,
        )

        out = StringIO()
        call_command("killstats_delete_npc_killmails", stdout=out)
        output = out.getvalue()

        self.assertIn("Found 1 killmail(s)", output)
        self.assertIn("Deletion cancelled", output)
        self.assertTrue(Killmail.objects.filter(killmail_id=km.killmail_id).exists())
        mock_input.assert_called_once()

    @patch("builtins.input", return_value="y")
    def test_npc_killmail_confirmed_by_user(self, mock_input):
        km = KillmailFactory(
            victim_corporation_id=1000035,
        )

        out = StringIO()
        call_command("killstats_delete_npc_killmails", stdout=out)
        output = out.getvalue()

        self.assertIn("Found 1 killmail(s)", output)
        self.assertIn("Successfully deleted 1 NPC killmail(s)", output)
        self.assertFalse(Killmail.objects.filter(killmail_id=km.killmail_id).exists())
        mock_input.assert_called_once()

    def test_dry_run_flag(self):
        km = KillmailFactory(
            victim_corporation_id=1000035,
        )

        out = StringIO()
        call_command("killstats_delete_npc_killmails", "--dry-run", stdout=out)
        output = out.getvalue()

        self.assertIn("Found 1 killmail(s)", output)
        self.assertIn("[DRY-RUN] Would delete 1 killmail(s)", output)
        self.assertTrue(Killmail.objects.filter(killmail_id=km.killmail_id).exists())

    def test_npc_audit_cleanup(self):
        npc_corp = EveCorporationInfoFactory(
            corporation_id=1000125,
        )
        npc_audit = CorporationsAuditFactory(
            corporation=npc_corp,
            owner=self.player_char,
        )

        out = StringIO()
        call_command("killstats_delete_npc_killmails", "--yes", stdout=out)
        output = out.getvalue()

        self.assertIn("Found 1 NPC corporation audit(s)", output)
        self.assertIn("Deleted 1 invalid NPC audit(s)", output)
        self.assertFalse(CorporationsAudit.objects.filter(id=npc_audit.id).exists())


class TestKillstatsUpdateSolarSystems(AuthTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.solar_system = SolarSystemFactory()

    def setUp(self) -> None:
        super().setUp()
        cache.clear()
        cache.set("esi:bucket:killmail", 1200, 900)

    def tearDown(self) -> None:
        super().tearDown()
        cache.clear()

    def test_update_solar_systems_none_matching(self):
        # Test Data
        KillmailFactory(
            victim_solar_system_id=self.solar_system.id,
        )
        out = StringIO()
        # Test Action
        call_command("killstats_update_solar_systems", sleep=0, stdout=out)
        output = out.getvalue()
        # Expected Result
        self.assertIn("No killmails found with missing solar_system_id", output)

    @patch("requests.get")
    def test_update_solar_systems_success(self, mock_requests_get):
        # Test Data: Killmail with missing victim_solar_system_id and victim_region_id
        km = KillmailFactory(
            victim_solar_system_id=None,
            victim_region_id=None,
        )

        # Mock ESI response returning solar_system_id
        mock_response = patch("requests.Response").start()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "killmail_id": km.killmail_id,
            "solar_system_id": self.solar_system.id,
        }
        mock_requests_get.return_value = mock_response

        out = StringIO()

        # Test Action
        call_command("killstats_update_solar_systems", sleep=0, stdout=out)
        output = out.getvalue()
        # Expected Result
        self.assertIn("Found 1 killmail(s) matching criteria", output)
        self.assertIn("Updated: 1", output)

        km.refresh_from_db()
        self.assertEqual(km.victim_solar_system_id, self.solar_system.id)
        self.assertIsNotNone(km.victim_region_id)
        self.assertEqual(km.victim_region_id, self.solar_system.constellation.region_id)

    @patch("requests.get")
    def test_update_solar_systems_dry_run(self, mock_requests_get):
        # Test Data: Killmail with missing victim_solar_system_id
        km = KillmailFactory(
            victim_solar_system_id=None,
        )
        out = StringIO()
        # Test Action: Run the management command in dry-run mode
        call_command("killstats_update_solar_systems", "--dry-run", sleep=0, stdout=out)
        output = out.getvalue()

        # Expected Result: The command should indicate a dry-run and not make any HTTP requests
        self.assertIn("[DRY-RUN] Would check and update 1 killmail(s)", output)
        mock_requests_get.assert_not_called()

        km.refresh_from_db()
        self.assertIsNone(km.victim_solar_system_id)

    @patch("requests.get")
    def test_update_solar_systems_failed_fetch(self, mock_requests_get):
        # Test Data: Killmail with missing victim_solar_system_id
        km = KillmailFactory(
            victim_solar_system_id=None,
        )

        # Mock ESI 404 response to simulate failed fetch
        mock_response = patch("requests.Response").start()
        mock_response.status_code = 404
        mock_requests_get.return_value = mock_response

        out = StringIO()
        # Test Action: Run the management command to update solar systems
        call_command("killstats_update_solar_systems", sleep=0, stdout=out)
        output = out.getvalue()

        # Expected Result: The command should indicate a failed fetch for the killmail
        self.assertIn("Failed (could not fetch): 1", output)
        km.refresh_from_db()
        self.assertIsNone(km.victim_solar_system_id)

    @patch("requests.get")
    def test_update_solar_systems_missing_only_flag(self, mock_requests_get):
        # Test Data: One killmail with a solar system and one without
        solar_system = SolarSystemFactory()
        km_with_system = KillmailFactory(
            victim_solar_system_id=solar_system.id,
        )
        km_without_system = KillmailFactory(
            victim_solar_system_id=None,
        )

        mock_response = patch("requests.Response").start()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "killmail_id": km_without_system.killmail_id,
            "solar_system_id": solar_system.id,
        }
        mock_requests_get.return_value = mock_response

        out = StringIO()
        # Test Action: Run the management command to update solar systems
        call_command(
            "killstats_update_solar_systems", "--missing-only", sleep=0, stdout=out
        )
        output = out.getvalue()

        # Expected Result: The command should indicate it is checking only killmails with missing solar_system_id
        self.assertIn(
            "Mode: Checking ONLY killmails with missing solar_system_id", output
        )
        self.assertIn("Found 1 killmail(s) matching criteria", output)
        self.assertIn("Updated: 1", output)

        km_without_system.refresh_from_db()
        self.assertEqual(km_without_system.victim_solar_system_id, solar_system.id)
        km_with_system.refresh_from_db()
        self.assertEqual(km_with_system.victim_solar_system_id, solar_system.id)

    @patch("requests.get")
    def test_update_solar_systems_limit(self, mock_requests_get):
        # Test Data: Two killmails without solar system IDs, limit the update to 1
        solar_system = SolarSystemFactory()
        KillmailFactory(
            victim_solar_system_id=None,
        )
        km2 = KillmailFactory(
            victim_solar_system_id=None,
        )

        mock_response = patch("requests.Response").start()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "killmail_id": km2.killmail_id,
            "solar_system_id": solar_system.id,
        }
        mock_requests_get.return_value = mock_response

        out = StringIO()
        # Test Action: Run the management command with a limit of 1
        call_command(
            "killstats_update_solar_systems", "--limit", "1", sleep=0, stdout=out
        )
        output = out.getvalue()

        # Expected Result: The command should indicate it found 2 killmails but only updated 1 due to the limit
        self.assertIn("Found 2 killmail(s) matching criteria (limited to 1)", output)
        self.assertIn("Updated: 1", output)

    @patch("requests.get")
    def test_update_solar_systems_zero_solar_system_id(self, mock_requests_get):
        # Test Data: One killmail with a solar system ID of 0
        solar_system = SolarSystemFactory()
        km_zero = KillmailFactory(
            victim_solar_system_id=0,
        )

        mock_response = patch("requests.Response").start()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "killmail_id": km_zero.killmail_id,
            "solar_system_id": solar_system.id,
        }
        mock_requests_get.return_value = mock_response

        out = StringIO()
        # Test Action: Run the management command to update solar systems
        call_command("killstats_update_solar_systems", "-m", sleep=0, stdout=out)
        output = out.getvalue()

        # Expected Result: The command should indicate it found 1 killmail and updated it
        self.assertIn("Found 1 killmail(s) matching criteria", output)
        self.assertIn("Updated: 1", output)

        km_zero.refresh_from_db()
        self.assertEqual(km_zero.victim_solar_system_id, solar_system.id)

    @patch("requests.get")
    def test_update_solar_systems_zkb_fallback(self, mock_requests_get):
        # Test Data: One killmail without a solar system ID, ESI returns 404, fallback to zkb succeeds
        solar_system = SolarSystemFactory()
        km = KillmailFactory(
            victim_solar_system_id=None,
        )

        resp_esi = Mock(status_code=404)
        resp_zkb = Mock(
            status_code=200,
            json=Mock(return_value=[{"solar_system_id": solar_system.id}]),
        )
        mock_requests_get.side_effect = [resp_esi, resp_zkb]

        out = StringIO()
        # Test Action: Run the management command to update solar systems
        call_command("killstats_update_solar_systems", sleep=0, stdout=out)
        output = out.getvalue()

        # Expected Result: The command should indicate it updated 1 killmail
        self.assertIn("Updated: 1", output)
        km.refresh_from_db()
        self.assertEqual(km.victim_solar_system_id, solar_system.id)

    @patch("requests.get")
    def test_update_solar_systems_rate_limit_stops_early(self, mock_requests_get):
        KillmailFactory(
            victim_solar_system_id=None,
        )
        # Test Data: Token bucket is below the default reserve, should stop early due to rate limit

        # Token bucket is at 550, which is below default reserve of 600
        cache.set("esi:bucket:killmail", 550, 900)

        out = StringIO()
        # Test Action: Run the management command to update solar systems
        call_command("killstats_update_solar_systems", sleep=0, stdout=out)
        output = out.getvalue()
        # Expected Result: The command should indicate it stopped early due to rate limit
        self.assertIn("[RATE-LIMIT]", output)
        self.assertIn("at or below reserve (600)", output)
        self.assertIn("Stopped by rate limit reserve: Yes", output)
        mock_requests_get.assert_not_called()

    @patch("requests.get")
    def test_update_solar_systems_custom_min_reserve(self, mock_requests_get):
        # Test Data: One killmail without a solar system ID, token bucket above custom min reserve
        solar_system = SolarSystemFactory()
        km = KillmailFactory(
            victim_solar_system_id=None,
        )

        # Token bucket is at 300
        cache.set("esi:bucket:killmail", 300, 900)

        mock_response = patch("requests.Response").start()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "killmail_id": km.killmail_id,
            "solar_system_id": solar_system.id,
        }
        mock_requests_get.return_value = mock_response

        # Test Action: Run the management command with a custom min reserve of 200
        # With --min-reserve 200, 300 is above reserve -> should process
        out = StringIO()
        call_command(
            "killstats_update_solar_systems",
            "--min-reserve",
            "200",
            sleep=0,
            stdout=out,
        )
        output = out.getvalue()
        # Expected Result: The command should indicate it updated 1 killmail and did not stop due to rate limit
        self.assertIn("Updated: 1", output)
        self.assertIn("Stopped by rate limit reserve: No", output)
        km.refresh_from_db()
        self.assertEqual(km.victim_solar_system_id, solar_system.id)


class TestKillstatsMigrateEveEntity(AuthTestCase):
    def test_migrate_eveentity_without_eveuniverse(self):
        # Test Data: eveuniverse is not installed
        with patch.dict(
            "sys.modules", {"eveuniverse": None, "eveuniverse.models": None}
        ):
            out = StringIO()
            # Test Action
            call_command("killstats_migrate_eveentity", stdout=out)
            output = out.getvalue()

            # Expected Result: command exits gracefully without error
            self.assertNotIn("Migrated", output)

    def test_migrate_eveentity_success(self):
        # Test Data
        # Standard Library
        from types import ModuleType, SimpleNamespace

        mock_old_entity_1 = SimpleNamespace(
            id=60001, name="Migrated Char", category=EveEntity.CATEGORY_CHARACTER
        )
        mock_old_entity_2 = SimpleNamespace(
            id=60002, name="Migrated Corp", category=EveEntity.CATEGORY_CORPORATION
        )

        mock_qs = Mock()
        mock_qs.exclude.return_value = mock_qs
        mock_qs.only.return_value = mock_qs
        mock_qs.count.return_value = 2
        mock_qs.iterator.return_value = [mock_old_entity_1, mock_old_entity_2]

        mock_old_class = Mock()
        mock_old_class.objects = mock_qs

        eveuniverse_mod = ModuleType("eveuniverse")
        eveuniverse_models = ModuleType("eveuniverse.models")
        eveuniverse_models.EveEntity = mock_old_class

        with patch.dict(
            "sys.modules",
            {"eveuniverse": eveuniverse_mod, "eveuniverse.models": eveuniverse_models},
        ):
            out = StringIO()
            # Test Action
            call_command("killstats_migrate_eveentity", stdout=out)
            output = out.getvalue()

            # Expected Result
            self.assertIn("Migrated 2 EveEntity records out of 2", output)
            self.assertTrue(
                EveEntity.objects.filter(id=60001, name="Migrated Char").exists()
            )
            self.assertTrue(
                EveEntity.objects.filter(id=60002, name="Migrated Corp").exists()
            )

    def test_migrate_eveentity_empty(self):
        # Test Data: no old entities to migrate
        # Standard Library
        from types import ModuleType

        mock_qs = Mock()
        mock_qs.exclude.return_value = mock_qs
        mock_qs.only.return_value = mock_qs
        mock_qs.count.return_value = 0
        mock_qs.iterator.return_value = []

        mock_old_class = Mock()
        mock_old_class.objects = mock_qs

        eveuniverse_mod = ModuleType("eveuniverse")
        eveuniverse_models = ModuleType("eveuniverse.models")
        eveuniverse_models.EveEntity = mock_old_class

        with patch.dict(
            "sys.modules",
            {"eveuniverse": eveuniverse_mod, "eveuniverse.models": eveuniverse_models},
        ):
            out = StringIO()
            # Test Action
            call_command("killstats_migrate_eveentity", stdout=out)
            output = out.getvalue()

            # Expected Result
            self.assertIn("Migrated 0 EveEntity records out of 0", output)


class TestKillstatsSyncKillmails(AuthTestCase):
    """Unit tests for killstats_sync_killmails management command."""

    def test_sync_killmails_without_args_should_show_error(self):
        # Test Data
        out = StringIO()
        err = StringIO()

        # Test Action
        call_command("killstats_sync_killmails", stdout=out, stderr=err)

        # Expected Result
        self.assertIn(
            "Please specify --corporation <id>, --alliance <id>, or --all",
            err.getvalue(),
        )

    @patch("killstats.models.killboard.Killmail.objects.create_from_killmail")
    @patch("killstats.models.killboard.Killmail.objects.check_missing_killmails")
    def test_sync_killmails_corporation_should_fetch_and_import(
        self, mock_check, mock_create
    ):
        # Test Data
        mock_km = Mock()
        mock_check.return_value = [mock_km]
        out = StringIO()

        # Test Action
        call_command(
            "killstats_sync_killmails",
            "--corporation",
            "98000001",
            "--pages",
            "5",
            "--delay",
            "0",
            stdout=out,
        )

        # Expected Result
        mock_check.assert_called_once_with(
            corporation_id=98000001,
            pages=5,
            delay_between_pages=0.0,
        )
        mock_create.assert_called_once_with(mock_km)
        self.assertIn("Found 1 missing killmail(s)", out.getvalue())
        self.assertIn("Successfully imported 1/1 killmail(s)", out.getvalue())

    @patch("killstats.models.killboard.Killmail.objects.create_from_killmail")
    @patch("killstats.models.killboard.Killmail.objects.check_missing_killmails")
    def test_sync_killmails_alliance_should_fetch_and_import(
        self, mock_check, mock_create
    ):
        # Test Data
        mock_km = Mock()
        mock_check.return_value = [mock_km]
        out = StringIO()

        # Test Action
        call_command(
            "killstats_sync_killmails",
            "--alliance",
            "99000001",
            "--pages",
            "3",
            "--delay",
            "0",
            stdout=out,
        )

        # Expected Result
        mock_check.assert_called_once_with(
            alliance_id=99000001,
            pages=3,
            delay_between_pages=0.0,
        )
        mock_create.assert_called_once_with(mock_km)
        self.assertIn("Found 1 missing killmail(s)", out.getvalue())
        self.assertIn("Successfully imported 1/1 killmail(s)", out.getvalue())

    @patch("killstats.models.killboard.Killmail.objects.create_from_killmail")
    @patch("killstats.models.killboard.Killmail.objects.check_missing_killmails")
    def test_sync_killmails_all_should_sync_all_audited_entities(
        self, mock_check, mock_create
    ):
        # Test Data
        CorporationsAuditFactory()
        AlliancesAuditFactory()
        mock_km = Mock()
        mock_check.return_value = [mock_km]
        out = StringIO()

        # Test Action
        call_command(
            "killstats_sync_killmails",
            "--all",
            "--pages",
            "2",
            "--delay",
            "0",
            stdout=out,
        )

        # Expected Result
        self.assertEqual(mock_check.call_count, 2)
        self.assertEqual(mock_create.call_count, 2)
        self.assertIn("Sync complete", out.getvalue())

    @patch("killstats.models.killboard.Killmail.objects.create_from_killmail")
    @patch("killstats.models.killboard.Killmail.objects.check_missing_killmails")
    def test_sync_killmails_should_handle_integrity_error_gracefully(
        self, mock_check, mock_create
    ):
        # Test Data
        # Django
        from django.db import IntegrityError

        mock_km = Mock()
        mock_km.esi.killmail_id = 12345
        mock_check.return_value = [mock_km]
        mock_create.side_effect = IntegrityError("Duplicate")
        out = StringIO()

        # Test Action
        call_command(
            "killstats_sync_killmails",
            "--corporation",
            "98000001",
            "--pages",
            "1",
            "--delay",
            "0",
            stdout=out,
        )

        # Expected Result
        mock_create.assert_called_once_with(mock_km)
        self.assertIn("Successfully imported 0/1 killmail(s)", out.getvalue())
