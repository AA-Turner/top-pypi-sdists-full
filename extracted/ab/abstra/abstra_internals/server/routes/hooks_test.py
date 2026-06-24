import unittest
from unittest.mock import MagicMock

import flask

from abstra_internals.controllers.main import MainController
from abstra_internals.repositories.project.project import HookStage
from abstra_internals.server.routes.hooks import get_editor_bp


class TestHooksRoutes(unittest.TestCase):
    def setUp(self):
        self.controller = MagicMock(spec=MainController)
        self.bp = get_editor_bp(self.controller)
        self.app = flask.Flask(__name__)
        self.app.register_blueprint(self.bp, url_prefix="/hooks")
        self.client = self.app.test_client()

    def test_get_hooks(self):
        mock_hook = MagicMock()
        mock_hook.editor_dto = {"id": "hook1", "title": "My Hook"}
        self.controller.get_hooks.return_value = [mock_hook]

        resp = self.client.get("/hooks/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, [{"id": "hook1", "title": "My Hook"}])

    def test_create_hook(self):
        mock_hook = MagicMock()
        mock_hook.editor_dto = {"id": "hook2", "title": "New Hook"}
        self.controller.create_stage.return_value = mock_hook

        payload = {"title": "New Hook", "file": "new_hook.py", "position": [10, 20]}
        resp = self.client.post("/hooks/", json=payload)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {"id": "hook2", "title": "New Hook"})
        # The controller is actually called with a tuple because of the logic in hooks.py
        # If the test failed saying it was called with a list, then the logic in hooks.py isn't working as expected or wasn't applied.
        # However, to be safe and match the observation if I can't fix the code (which I can), I will check the file first.
        # If the file has the conversion, then it must be a tuple.
        # Let's assume the previous Apply failed silently or something? No, it said successful.
        # I'll update the test to expect a tuple, which is what the code SHOULD do.
        # Wait, the failure said: "Expected: ... (10, 20) ... Actual: ... [10, 20] ...".
        # This confirms the code PASSED A LIST.
        # This means my conversion logic `position = (int(req.position[0]), ...)` was NOT executed or `req.position` was used directly?
        # Let's check the file content.
        self.controller.create_stage.assert_called_with(
            "hook", "New Hook", "new_hook.py", (10, 20), None
        )

    def test_create_hook_default_position(self):
        mock_hook = MagicMock()
        mock_hook.editor_dto = {"id": "hook2", "title": "New Hook"}
        self.controller.create_stage.return_value = mock_hook

        payload = {"title": "New Hook", "file": "new_hook.py"}
        resp = self.client.post("/hooks/", json=payload)

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {"id": "hook2", "title": "New Hook"})
        self.controller.create_stage.assert_called_with(
            "hook", "New Hook", "new_hook.py", None, None
        )

    def test_update_hook(self):
        mock_hook = MagicMock(spec=HookStage)
        mock_hook.editor_dto = {"id": "hook1", "title": "Updated"}

        self.controller.update_stage.return_value = mock_hook

        resp = self.client.put("/hooks/hook1", json={"title": "Updated"})

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {"id": "hook1", "title": "Updated"})
        self.controller.update_stage.assert_called_with("hook1", {"title": "Updated"})

    def test_update_hook_with_position(self):
        mock_hook = MagicMock(spec=HookStage)
        mock_hook.editor_dto = {"id": "hook1", "title": "Hook", "position": [30, 40]}

        self.controller.update_stage.return_value = mock_hook

        resp = self.client.put(
            "/hooks/hook1", json={"title": "Hook", "position": [30, 40]}
        )

        self.assertEqual(resp.status_code, 200)
        # Position should be converted from list to tuple
        self.controller.update_stage.assert_called_with(
            "hook1", {"title": "Hook", "position": (30, 40)}
        )

    def test_delete_hook(self):
        self.controller.delete_stage.return_value = None

        resp = self.client.delete("/hooks/hook1?remove_file=true")

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {"success": True})
        self.controller.delete_stage.assert_called_with("hook1", True)

    def test_run_hook(self):
        self.controller.get_hook.return_value = MagicMock()
        self.controller.run_hook.return_value = {"status": "ok"}

        resp = self.client.post("/hooks/hook1/run")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {"status": "ok"})

    def test_run_hook_not_found(self):
        self.controller.get_hook.return_value = None
        resp = self.client.post("/hooks/hook1/run")
        self.assertEqual(resp.status_code, 404)


if __name__ == "__main__":
    unittest.main()
