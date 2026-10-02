"""Unit tests for KillmailManager and Killmail querysets."""

# Standard Library
from http import HTTPStatus

# Third Party
import pook
from evesde_factory.eve_sde import ItemCategoryFactory, ItemTypeFactory

# AA Killstats
from killstats.models import Attacker, Killmail
from killstats.tests import AuthTestCase
from killstats.tests.testdata.killstats import (
    AttackerFactory,
    EveEntityFactory,
    KillmailBodyFactory,
    KillmailFactory,
    UserMainFactory,
)


class TestKillmailQuerySet(AuthTestCase):
    def test_visible_to_should_return_all_for_superuser(self):
        # Test Data
        km1 = KillmailFactory()
        km2 = KillmailFactory()

        # Test Action
        result = Killmail.objects.visible_to(self.superuser)

        # Expected Result
        self.assertIn(km1, result)
        self.assertIn(km2, result)

    def test_visible_to_should_return_all_for_admin_access(self):
        # Test Data
        admin_user = UserMainFactory(permissions__=["killstats.admin_access"])
        km1 = KillmailFactory()
        km2 = KillmailFactory()

        # Test Action
        result = Killmail.objects.visible_to(admin_user)

        # Expected Result
        self.assertIn(km1, result)
        self.assertIn(km2, result)

    def test_visible_to_should_return_none_for_normal_user(self):
        # Test Data
        normal_user = UserMainFactory(permissions__=["killstats.basic_access"])
        KillmailFactory()

        # Test Action
        result = Killmail.objects.visible_to(normal_user)

        # Expected Result
        self.assertFalse(result.exists())


class TestKillmailQueryCoreFilters(AuthTestCase):
    def test_filter_entities_kills_should_return_attacker_killmails(self):
        # Test Data
        km1 = KillmailFactory()
        km2 = KillmailFactory()
        AttackerFactory(killmail=km1, character__id=5001)

        # Test Action
        result = Killmail.objects.filter_entities_kills([5001])

        # Expected Result
        self.assertIn(km1, result)
        self.assertNotIn(km2, result)

    def test_filter_entities_losses_should_return_victim_killmails(self):
        # Test Data
        km1 = KillmailFactory(victim_corporation_id=88001)
        km2 = KillmailFactory(victim_corporation_id=88002)

        # Test Action
        result = Killmail.objects.filter_entities_losses([88001])

        # Expected Result
        self.assertIn(km1, result)
        self.assertNotIn(km2, result)

    def test_filter_entities_should_combine_kills_and_losses(self):
        # Test Data
        km_kill = KillmailFactory()
        AttackerFactory(killmail=km_kill, corporation__id=88001)
        km_loss = KillmailFactory(victim_corporation_id=88001)
        km_other = KillmailFactory(victim_corporation_id=88002)

        # Test Action
        result = Killmail.objects.filter_entities([88001])

        # Expected Result
        self.assertIn(km_kill, result)
        self.assertIn(km_loss, result)
        self.assertNotIn(km_other, result)

    def test_filter_structure_exclude_false_should_return_structures(self):
        # Test Data
        cat_struct = ItemCategoryFactory(id=65)
        cat_ship = ItemCategoryFactory(id=6)
        structure_ship = ItemTypeFactory(group__category=cat_struct)
        normal_ship = ItemTypeFactory(group__category=cat_ship)
        km_struct = KillmailFactory(victim_ship=structure_ship)
        km_ship = KillmailFactory(victim_ship=normal_ship)

        # Test Action
        result = Killmail.objects.filter_structure(exclude=False)

        # Expected Result
        self.assertIn(km_struct, result)
        self.assertNotIn(km_ship, result)

    def test_filter_structure_exclude_true_should_exclude_structures(self):
        # Test Data
        cat_struct = ItemCategoryFactory(id=65)
        cat_ship = ItemCategoryFactory(id=6)
        structure_ship = ItemTypeFactory(group__category=cat_struct)
        normal_ship = ItemTypeFactory(group__category=cat_ship)
        km_struct = KillmailFactory(victim_ship=structure_ship)
        km_ship = KillmailFactory(victim_ship=normal_ship)

        # Test Action
        result = Killmail.objects.filter_structure(exclude=True)

        # Expected Result
        self.assertIn(km_ship, result)
        self.assertNotIn(km_struct, result)

    def test_filter_threshold_should_filter_by_value(self):
        # Test Data
        km_high = KillmailFactory(victim_total_value=2000000)
        km_low = KillmailFactory(victim_total_value=500000)

        # Test Action
        result = Killmail.objects.all().filter_threshold(1000000)

        # Expected Result
        self.assertIn(km_high, result)
        self.assertNotIn(km_low, result)


class TestKillmailQueryMiningFilters(AuthTestCase):
    def test_filter_barge_should_return_only_barges(self):
        # Test Data
        barge_type = ItemTypeFactory(group__id=463)
        other_type = ItemTypeFactory(group__id=123)
        km_barge = KillmailFactory(victim_ship=barge_type)
        km_other = KillmailFactory(victim_ship=other_type)

        # Test Action
        result = Killmail.objects.all().filter_barge()

        # Expected Result
        self.assertIn(km_barge, result)
        self.assertNotIn(km_other, result)

    def test_filter_exhumer_should_return_only_exhumers(self):
        # Test Data
        exhumer_type = ItemTypeFactory(group__id=543)
        other_type = ItemTypeFactory(group__id=123)
        km_exhumer = KillmailFactory(victim_ship=exhumer_type)
        km_other = KillmailFactory(victim_ship=other_type)

        # Test Action
        result = Killmail.objects.all().filter_exhumer()

        # Expected Result
        self.assertIn(km_exhumer, result)
        self.assertNotIn(km_other, result)

    def test_filter_indu_command_ship_should_return_only_command_ships(self):
        # Test Data
        indu_type = ItemTypeFactory(group__id=941)
        other_type = ItemTypeFactory(group__id=123)
        km_indu = KillmailFactory(victim_ship=indu_type)
        km_other = KillmailFactory(victim_ship=other_type)

        # Test Action
        result = Killmail.objects.all().filter_indu_command_ship()

        # Expected Result
        self.assertIn(km_indu, result)
        self.assertNotIn(km_other, result)

    def test_filter_capital_indu_ship_should_return_only_capital_indu_ships(self):
        # Test Data
        capital_type = ItemTypeFactory(group__id=883)
        other_type = ItemTypeFactory(group__id=123)
        km_capital = KillmailFactory(victim_ship=capital_type)
        km_other = KillmailFactory(victim_ship=other_type)

        # Test Action
        result = Killmail.objects.all().filter_capital_indu_ship()

        # Expected Result
        self.assertIn(km_capital, result)
        self.assertNotIn(km_other, result)


class TestKillmailManagerCheckMissingKillmails(AuthTestCase):
    def test_check_missing_killmails_without_corp_or_alliance_should_raise_value_error(
        self,
    ):
        # Test Action & Expected Result
        with self.assertRaises(ValueError):
            Killmail.objects.check_missing_killmails()

    @pook.on
    def test_check_missing_killmails_should_fetch_and_filter_existing_using_pook(
        self,
    ):
        # Test Data
        KillmailFactory(killmail_id=12345)
        pook.get(
            "https://zkillboard.com/api/corporationID/98000001/page/1/",
            reply=HTTPStatus.OK,
            response_json=[
                {
                    "killmail_id": 12345,
                    "zkb": {
                        "hash": "abc1",
                        "totalValue": 1000.0,
                        "fittedValue": 500.0,
                        "droppedValue": 100.0,
                        "destroyedValue": 400.0,
                        "points": 1,
                        "npc": False,
                        "solo": False,
                        "awox": False,
                    },
                    "killmail_time": "2026-01-01T12:00:00Z",
                    "solar_system_id": 30000142,
                    "victim": {
                        "character_id": 1001,
                        "corporation_id": 98000001,
                        "ship_type_id": 606,
                        "damage_taken": 100,
                    },
                    "attackers": [
                        {
                            "character_id": 1002,
                            "corporation_id": 98000002,
                            "damage_done": 100,
                            "final_blow": True,
                            "security_status": 5.0,
                        }
                    ],
                },
                {
                    "killmail_id": 12346,
                    "zkb": {
                        "hash": "abc2",
                        "totalValue": 2000.0,
                        "fittedValue": 1000.0,
                        "droppedValue": 200.0,
                        "destroyedValue": 800.0,
                        "points": 2,
                        "npc": False,
                        "solo": False,
                        "awox": False,
                    },
                    "killmail_time": "2026-01-01T13:00:00Z",
                    "solar_system_id": 30000142,
                    "victim": {
                        "character_id": 1003,
                        "corporation_id": 98000001,
                        "ship_type_id": 606,
                        "damage_taken": 200,
                    },
                    "attackers": [
                        {
                            "character_id": 1004,
                            "corporation_id": 98000002,
                            "damage_done": 200,
                            "final_blow": True,
                            "security_status": 5.0,
                        }
                    ],
                },
            ],
        )

        # Test Action
        missing = Killmail.objects.check_missing_killmails(
            corporation_id=98000001, pages=1, delay_between_pages=0
        )

        # Expected Result
        self.assertEqual(len(missing), 1)
        self.assertEqual(missing[0].killmail_id, 12346)

    @pook.on
    def test_check_missing_killmails_on_error_should_return_empty_list_gracefully(
        self,
    ):
        # Test Data
        pook.get(
            "https://zkillboard.com/api/allianceID/99000001/page/1/",
            reply=HTTPStatus.BAD_GATEWAY,
            response_json={"error": "Service unavailable"},
        )

        # Test Action
        missing = Killmail.objects.check_missing_killmails(
            alliance_id=99000001, pages=1, delay_between_pages=0
        )

        # Expected Result
        self.assertEqual(missing, [])


class TestKillmailManagerCreation(AuthTestCase):
    @pook.on
    def test_create_from_killmail_should_create_killmail_and_attackers(self):
        # Test Data
        killmail_body = KillmailBodyFactory()
        ItemTypeFactory(id=killmail_body.esi.victim.ship_type_id)
        EveEntityFactory(
            id=killmail_body.esi.victim.character_id,
            category="character",
        )
        for attacker in killmail_body.esi.attackers:
            if attacker.ship_type_id:
                ItemTypeFactory(id=attacker.ship_type_id)
            if attacker.character_id:
                EveEntityFactory(id=attacker.character_id, category="character")
            if attacker.corporation_id:
                EveEntityFactory(id=attacker.corporation_id, category="corporation")
            if attacker.alliance_id:
                EveEntityFactory(id=attacker.alliance_id, category="alliance")

        # Mock ESI in case any entity bulk fetch is triggered
        pook.post(
            "https://esi.evetech.net/universe/names",
            reply=HTTPStatus.OK,
            response_json=[],
        ).persist()

        # Test Action
        km = Killmail.objects.create_from_killmail(killmail_body)

        # Expected Result
        self.assertEqual(km.killmail_id, killmail_body.esi.killmail_id)
        self.assertEqual(km.victim_total_value, killmail_body.zkb.totalValue)
        self.assertTrue(Attacker.objects.filter(killmail=km).exists())

    @pook.on
    def test_update_or_create_from_killmail_should_create_and_update(self):
        # Test Data
        killmail_body = KillmailBodyFactory()
        ItemTypeFactory(id=killmail_body.esi.victim.ship_type_id)
        EveEntityFactory(
            id=killmail_body.esi.victim.character_id,
            category="character",
        )
        for attacker in killmail_body.esi.attackers:
            if attacker.ship_type_id:
                ItemTypeFactory(id=attacker.ship_type_id)
            if attacker.character_id:
                EveEntityFactory(id=attacker.character_id, category="character")
            if attacker.corporation_id:
                EveEntityFactory(id=attacker.corporation_id, category="corporation")
            if attacker.alliance_id:
                EveEntityFactory(id=attacker.alliance_id, category="alliance")

        # Mock ESI in case any entity bulk fetch is triggered
        pook.post(
            "https://esi.evetech.net/universe/names",
            reply=HTTPStatus.OK,
            response_json=[],
        ).persist()

        # Test Action 1: Create
        km1, created1 = Killmail.objects.update_or_create_from_killmail(killmail_body)

        # Expected Result 1
        self.assertTrue(created1)
        self.assertEqual(km1.killmail_id, killmail_body.esi.killmail_id)

        # Test Action 2: Update (re-creates existing)
        km2, created2 = Killmail.objects.update_or_create_from_killmail(killmail_body)

        # Expected Result 2
        self.assertFalse(created2)
        self.assertEqual(km2.killmail_id, killmail_body.esi.killmail_id)
