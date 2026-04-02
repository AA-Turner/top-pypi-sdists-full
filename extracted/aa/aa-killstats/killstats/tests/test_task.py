# Standard Library
from unittest.mock import Mock, patch

# Django
from django.core.cache import cache

# AA Killstats
from killstats import __title__
from killstats.tasks import (
    run_tracker_alliance,
    run_tracker_corporation,
    run_zkb_r2z2,
)
from killstats.tests import NoSocketsTestCase

HELPER_PATH = "killstats.helpers.killmail"
MODULE_PATH = "killstats.tasks"


class TestTasks(NoSocketsTestCase):
    def setUp(self) -> None:
        cache.clear()

    @patch(MODULE_PATH + ".logger.error")
    @patch(HELPER_PATH + ".KillmailBody.get_sequence_from_r2z2")
    def test_run_zkb_r2z2_handles_sequence_exception(
        self, mock_get_sequence, mock_logger_error
    ):
        mock_get_sequence.side_effect = Exception("boom")

        run_zkb_r2z2()

        mock_logger_error.assert_called_once()

    @patch(HELPER_PATH + ".KillmailBody.create_from_r2z2_sequence")
    @patch(HELPER_PATH + ".KillmailBody.get_sequence_from_r2z2", return_value=None)
    def test_run_zkb_r2z2_returns_when_no_sequence(
        self, _mock_get_sequence, mock_create_from_sequence
    ):
        run_zkb_r2z2()

        mock_create_from_sequence.assert_not_called()

    @patch(MODULE_PATH + ".run_tracker_alliance.delay")
    @patch(MODULE_PATH + ".run_tracker_corporation.delay")
    @patch(MODULE_PATH + ".AlliancesAudit.objects.all")
    @patch(MODULE_PATH + ".CorporationsAudit.objects.all")
    @patch(HELPER_PATH + ".KillmailBody.create_from_r2z2_sequence")
    @patch(HELPER_PATH + ".KillmailBody.get_sequence_from_r2z2", return_value=100)
    def test_run_zkb_r2z2_processes_and_dispatches_trackers(
        self,
        _mock_get_sequence,
        mock_create_from_sequence,
        mock_corps_all,
        mock_allys_all,
        mock_run_tracker_corp_delay,
        mock_run_tracker_ally_delay,
    ):
        corporation_audit = Mock()
        corporation_audit.corporation.corporation_id = 2001
        mock_corps_all.return_value = [corporation_audit]

        alliance_audit = Mock()
        alliance_audit.alliance.alliance_id = 3001
        mock_allys_all.return_value = [alliance_audit]

        killmail = Mock()
        killmail.id = 123456
        killmail.save = Mock()

        mock_create_from_sequence.side_effect = [killmail, None]

        run_zkb_r2z2()

        killmail.save.assert_called_once()
        mock_create_from_sequence.assert_any_call(100)
        self.assertEqual(mock_create_from_sequence.call_count, 2)

        mock_run_tracker_corp_delay.assert_called_once_with(
            corporation_id=2001,
            killmail_id=123456,
        )
        mock_run_tracker_ally_delay.assert_called_once_with(
            alliance_id=3001,
            killmail_id=123456,
        )
        self.assertEqual(mock_run_tracker_corp_delay.call_count, 1)
        self.assertEqual(mock_run_tracker_ally_delay.call_count, 1)

    @patch(MODULE_PATH + ".Chain")
    @patch(MODULE_PATH + ".store_killmail.si")
    @patch(HELPER_PATH + ".KillmailBody.get")
    @patch(MODULE_PATH + ".CorporationsAudit.objects.get")
    def test_run_tracker_corporation_triggers_store_chain_when_new(
        self,
        mock_corporation_get,
        mock_killmail_get,
        mock_store_killmail_signature,
        mock_chain,
    ):
        corporation = Mock()
        corporation.process_killmail.return_value = True
        mock_corporation_get.return_value = corporation

        killmail = Mock()
        killmail.id = 999
        mock_killmail_get.return_value = killmail

        signature = Mock()
        mock_store_killmail_signature.return_value = signature

        chain_instance = Mock()
        mock_chain.return_value = chain_instance

        run_tracker_corporation(corporation_id=2001, killmail_id=999)

        corporation.process_killmail.assert_called_once_with(killmail)
        mock_store_killmail_signature.assert_called_once_with(999)
        mock_chain.assert_called_once_with(signature)
        chain_instance.delay.assert_called_once()

    @patch(MODULE_PATH + ".Chain")
    @patch(MODULE_PATH + ".store_killmail.si")
    @patch(HELPER_PATH + ".KillmailBody.get")
    @patch(MODULE_PATH + ".AlliancesAudit.objects.get")
    def test_run_tracker_alliance_triggers_store_chain_when_new(
        self,
        mock_alliance_get,
        mock_killmail_get,
        mock_store_killmail_signature,
        mock_chain,
    ):
        alliance = Mock()
        alliance.process_killmail.return_value = True
        mock_alliance_get.return_value = alliance

        killmail = Mock()
        killmail.id = 555
        mock_killmail_get.return_value = killmail

        signature = Mock()
        mock_store_killmail_signature.return_value = signature

        chain_instance = Mock()
        mock_chain.return_value = chain_instance

        run_tracker_alliance(alliance_id=3001, killmail_id=555)

        alliance.process_killmail.assert_called_once_with(killmail)
        mock_store_killmail_signature.assert_called_once_with(555)
        mock_chain.assert_called_once_with(signature)
        chain_instance.delay.assert_called_once()
