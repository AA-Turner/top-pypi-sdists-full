import unittest
from unittest.mock import MagicMock, patch

from abstra_internals import credentials as credentials_module
from abstra_internals.services.api_key_status import ApiKeyStatus

_MOD = "abstra_internals.services.api_key_status"

DEAD_TOKEN = "token-from-the-deployment"
LIVE_KEY = "live-key"
SESSION_TOKEN = "editor-session-token"


def _api_key_info(reason=None, logged=False):
    return {"logged": logged} if logged else {"logged": False, "reason": reason}


class ApiKeyStatusTestCase(unittest.TestCase):
    def setUp(self):
        self._reset()

    def tearDown(self):
        self._reset()

    def _reset(self):
        credentials_module._rejected_tokens.clear()
        ApiKeyStatus._invalid = False
        ApiKeyStatus._last_probe_at = 0.0
        ApiKeyStatus._repair_fn = None
        ApiKeyStatus._recovering.active = False


class TestConfirmation(ApiKeyStatusTestCase):
    """A 401 is not proof: routes that take a session token answer 401 for an
    expired one too, and swapping the API key would not fix that."""

    def test_flags_and_rejects_the_token_cloud_api_refuses(self):
        with (
            patch(f"{_MOD}.get_credentials", return_value=DEAD_TOKEN),
            patch(f"{_MOD}.resolve_headers", return_value={"Api-Authorization": "k"}),
            patch(
                f"{_MOD}.get_api_key_info",
                return_value=_api_key_info("INVALID_API_TOKEN"),
            ),
        ):
            ApiKeyStatus.recover_from_unauthorized()

        self.assertFalse(ApiKeyStatus.is_valid())
        self.assertTrue(credentials_module._is_rejected(DEAD_TOKEN))

    def test_stays_valid_when_the_key_still_works(self):
        with (
            patch(f"{_MOD}.get_credentials", return_value=DEAD_TOKEN),
            patch(f"{_MOD}.resolve_headers", return_value={"Api-Authorization": "k"}),
            patch(f"{_MOD}.get_api_key_info", return_value=_api_key_info(logged=True)),
        ):
            self.assertFalse(ApiKeyStatus.recover_from_unauthorized())

        self.assertTrue(ApiKeyStatus.is_valid())
        self.assertFalse(credentials_module._is_rejected(DEAD_TOKEN))

    def test_stays_valid_when_cloud_api_is_unreachable_or_broken(self):
        for reason in ("CONNECTION_ERROR", "SERVER_ERROR", "UNKNOWN_ERROR"):
            with self.subTest(reason=reason):
                self._reset()
                with (
                    patch(f"{_MOD}.get_credentials", return_value=DEAD_TOKEN),
                    patch(
                        f"{_MOD}.resolve_headers",
                        return_value={"Api-Authorization": "k"},
                    ),
                    patch(
                        f"{_MOD}.get_api_key_info", return_value=_api_key_info(reason)
                    ),
                ):
                    self.assertFalse(ApiKeyStatus.recover_from_unauthorized())

                self.assertTrue(ApiKeyStatus.is_valid())

    def test_probes_once_per_burst_when_the_key_is_fine(self):
        with (
            patch(f"{_MOD}.get_credentials", return_value=DEAD_TOKEN),
            patch(f"{_MOD}.resolve_headers", return_value={"Api-Authorization": "k"}),
            patch(
                f"{_MOD}.get_api_key_info", return_value=_api_key_info(logged=True)
            ) as probe,
        ):
            for _ in range(5):
                ApiKeyStatus.recover_from_unauthorized()

        probe.assert_called_once()

    def test_flags_invalid_when_there_are_no_credentials_at_all(self):
        with (
            patch(f"{_MOD}.get_credentials", return_value=None),
            patch(f"{_MOD}.resolve_headers", return_value=None),
        ):
            ApiKeyStatus.recover_from_unauthorized()

        self.assertFalse(ApiKeyStatus.is_valid())


class TestRecovery(ApiKeyStatusTestCase):
    def _confirmed_dead(self):
        return (
            patch(f"{_MOD}.get_credentials", return_value=DEAD_TOKEN),
            patch(f"{_MOD}.resolve_headers", return_value={"Api-Authorization": "k"}),
            patch(
                f"{_MOD}.get_api_key_info",
                return_value=_api_key_info("INVALID_API_TOKEN"),
            ),
            patch(f"{_MOD}.resolve_ambient_session_token", return_value=SESSION_TOKEN),
        )

    def test_repairs_and_asks_for_a_retry(self):
        repair_fn = MagicMock(return_value=LIVE_KEY)
        ApiKeyStatus.configure_repair(repair_fn)
        creds, headers, info, ambient = self._confirmed_dead()

        with creds, headers, info, ambient, patch(f"{_MOD}.set_credentials") as store:
            self.assertTrue(ApiKeyStatus.recover_from_unauthorized())

        repair_fn.assert_called_once_with(SESSION_TOKEN)
        store.assert_called_once_with(LIVE_KEY)
        # Healthy again, so the frontend stops asking for a repair...
        self.assertTrue(ApiKeyStatus.is_valid())
        # ...but the revoked token stays out of the way, or get_credentials would
        # prefer it again and the editor would flap.
        self.assertTrue(credentials_module._is_rejected(DEAD_TOKEN))

    def test_no_retry_when_cloud_api_refuses_to_hand_over_a_key(self):
        repair_fn = MagicMock(return_value=None)
        ApiKeyStatus.configure_repair(repair_fn)
        creds, headers, info, ambient = self._confirmed_dead()

        with creds, headers, info, ambient, patch(f"{_MOD}.set_credentials") as store:
            self.assertFalse(ApiKeyStatus.recover_from_unauthorized())

        store.assert_not_called()
        self.assertFalse(ApiKeyStatus.is_valid())

    def test_no_retry_without_a_session_token_to_repair_with(self):
        repair_fn = MagicMock(return_value=LIVE_KEY)
        ApiKeyStatus.configure_repair(repair_fn)

        with (
            patch(f"{_MOD}.get_credentials", return_value=DEAD_TOKEN),
            patch(f"{_MOD}.resolve_headers", return_value={"Api-Authorization": "k"}),
            patch(
                f"{_MOD}.get_api_key_info",
                return_value=_api_key_info("INVALID_API_TOKEN"),
            ),
            patch(f"{_MOD}.resolve_ambient_session_token", return_value=None),
        ):
            self.assertFalse(ApiKeyStatus.recover_from_unauthorized())

        repair_fn.assert_not_called()
        # Still flagged, so the frontend-driven repair can pick it up with the
        # cookie of whoever is looking at the editor.
        self.assertFalse(ApiKeyStatus.is_valid())

    def test_no_retry_when_no_repair_is_wired(self):
        creds, headers, info, ambient = self._confirmed_dead()

        with creds, headers, info, ambient:
            self.assertFalse(ApiKeyStatus.recover_from_unauthorized())

        self.assertFalse(ApiKeyStatus.is_valid())

    def test_never_recovers_underneath_its_own_repair_call(self):
        # The repair reaches cloud-api through the same client, so its response
        # must not start another recovery on this thread.
        seen = {}

        def repair_fn(_token):
            seen["reentrant"] = ApiKeyStatus.recover_from_unauthorized()
            return LIVE_KEY

        ApiKeyStatus.configure_repair(repair_fn)
        creds, headers, info, ambient = self._confirmed_dead()

        with creds, headers, info, ambient, patch(f"{_MOD}.set_credentials"):
            self.assertTrue(ApiKeyStatus.recover_from_unauthorized())

        self.assertFalse(seen["reentrant"])

    def test_retries_without_repairing_when_the_credential_already_changed(self):
        # Concurrent requests overlap: this one went out with the dead token while
        # another was already replacing it. Nothing left to repair, and the request
        # only needs replaying with what is current now.
        repair_fn = MagicMock(return_value=LIVE_KEY)
        ApiKeyStatus.configure_repair(repair_fn)

        with patch(
            f"{_MOD}.resolve_headers",
            return_value={"Api-Authorization": "Bearer live"},
        ):
            self.assertTrue(ApiKeyStatus.recover_from_unauthorized("Bearer dead"))

        repair_fn.assert_not_called()

    def test_repairs_when_the_credential_is_still_the_current_one(self):
        repair_fn = MagicMock(return_value=LIVE_KEY)
        ApiKeyStatus.configure_repair(repair_fn)

        with (
            patch(f"{_MOD}.get_credentials", return_value=DEAD_TOKEN),
            patch(
                f"{_MOD}.resolve_headers",
                return_value={"Api-Authorization": "Bearer dead"},
            ),
            patch(
                f"{_MOD}.get_api_key_info",
                return_value=_api_key_info("INVALID_API_TOKEN"),
            ),
            patch(f"{_MOD}.resolve_ambient_session_token", return_value=SESSION_TOKEN),
            patch(f"{_MOD}.set_credentials"),
        ):
            self.assertTrue(ApiKeyStatus.recover_from_unauthorized("Bearer dead"))

        repair_fn.assert_called_once_with(SESSION_TOKEN)

    def test_a_failing_repair_never_raises_into_the_request(self):
        ApiKeyStatus.configure_repair(MagicMock(side_effect=Exception("boom")))
        creds, headers, info, ambient = self._confirmed_dead()

        with creds, headers, info, ambient, patch(f"{_MOD}.AbstraLogger") as logger:
            self.assertFalse(ApiKeyStatus.recover_from_unauthorized())

        logger.capture_exception.assert_called_once()


class TestFrontendDrivenRepair(ApiKeyStatusTestCase):
    """The repair the frontend triggers (router guard, status poll) never probes
    first, so `repair` itself has to put the stored key in front of the one it
    replaces. Without that, /_editor/api/login keeps answering "not logged in"
    right after a successful repair and the guard falls through to the console."""

    def test_rejects_the_credential_it_replaces(self):
        ApiKeyStatus.configure_repair(MagicMock(return_value=LIVE_KEY))

        with patch(f"{_MOD}.get_credentials", return_value=DEAD_TOKEN):
            with patch(f"{_MOD}.set_credentials"):
                self.assertTrue(ApiKeyStatus.repair(SESSION_TOKEN))

        self.assertTrue(credentials_module._is_rejected(DEAD_TOKEN))

    def test_keeps_the_credential_when_cloud_api_hands_back_the_same_key(self):
        # A repair on a healthy pod (the guard calls it whenever login says "no")
        # must not reject the key that is working.
        ApiKeyStatus.configure_repair(MagicMock(return_value=LIVE_KEY))

        with patch(f"{_MOD}.get_credentials", return_value=LIVE_KEY):
            with patch(f"{_MOD}.set_credentials"):
                self.assertTrue(ApiKeyStatus.repair(SESSION_TOKEN))

        self.assertFalse(credentials_module._is_rejected(LIVE_KEY))


class TestReset(ApiKeyStatusTestCase):
    def test_reset_clears_the_flag_but_not_the_rejection(self):
        credentials_module.mark_token_rejected(DEAD_TOKEN)
        ApiKeyStatus._invalid = True

        ApiKeyStatus.reset()

        self.assertTrue(ApiKeyStatus.is_valid())
        self.assertTrue(credentials_module._is_rejected(DEAD_TOKEN))


if __name__ == "__main__":
    unittest.main()
