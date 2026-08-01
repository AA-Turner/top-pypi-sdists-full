import unittest
from unittest.mock import patch

from abstra_internals.controllers.web_editor import WebEditorController
from abstra_internals.services.api_key_status import ApiKeyStatus

_MOD = "abstra_internals.controllers.web_editor"


class TestWebEditorApiKeyRepair(unittest.TestCase):
    def tearDown(self):
        ApiKeyStatus._invalid = False

    def test_delegates_the_repair_with_the_session_token(self):
        controller = WebEditorController()

        with (
            patch(f"{_MOD}.EDITOR_MODE", "web"),
            patch.object(ApiKeyStatus, "repair", return_value=True) as repair,
        ):
            self.assertTrue(controller.repair_api_key("session-token"))

        repair.assert_called_once_with("session-token")

    def test_does_nothing_without_a_session_token(self):
        controller = WebEditorController()

        with (
            patch(f"{_MOD}.EDITOR_MODE", "web"),
            patch.object(ApiKeyStatus, "repair") as repair,
        ):
            self.assertFalse(controller.repair_api_key(None))

        repair.assert_not_called()

    def test_does_nothing_in_a_local_install(self):
        # There is no deployment credential to repair locally; an invalid token
        # means `abstra login`, which owns its own flow.
        controller = WebEditorController()

        with (
            patch(f"{_MOD}.EDITOR_MODE", "local"),
            patch.object(ApiKeyStatus, "repair") as repair,
        ):
            self.assertFalse(controller.repair_api_key("session-token"))

        repair.assert_not_called()

    def test_reports_a_failed_repair(self):
        controller = WebEditorController()

        with (
            patch(f"{_MOD}.EDITOR_MODE", "web"),
            patch.object(ApiKeyStatus, "repair", return_value=False),
        ):
            self.assertFalse(controller.repair_api_key("session-token"))

    def test_inspect_reports_the_api_key_status(self):
        controller = WebEditorController()

        with patch(f"{_MOD}.WAITING_ROOM_URL", "https://console.test/wr"):
            self.assertTrue(controller.inspect().api_key_valid)
            ApiKeyStatus._invalid = True
            self.assertFalse(controller.inspect().api_key_valid)


if __name__ == "__main__":
    unittest.main()
