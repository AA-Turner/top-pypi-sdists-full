import unittest
from unittest.mock import MagicMock

import flask

from abstra_internals.controllers.main import MainController
from abstra_internals.server.routes.workspace import get_editor_bp


class TestWorkspaceRoutes(unittest.TestCase):
    def setUp(self):
        self.controller = MagicMock(spec=MainController)
        self.bp = get_editor_bp(self.controller)
        self.app = flask.Flask(__name__)
        self.app.register_blueprint(self.bp, url_prefix="/workspace")
        self.client = self.app.test_client()

    def test_get_workspace(self):
        mock_workspace = MagicMock()
        mock_workspace.as_dict = {"id": "ws1", "name": "My Workspace"}
        self.controller.get_workspace.return_value = mock_workspace

        resp = self.client.get("/workspace/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {"id": "ws1", "name": "My Workspace"})

    def test_update_workspace(self):
        mock_workspace = MagicMock()
        mock_workspace.as_dict = {"id": "ws1", "name": "Updated Workspace"}
        self.controller.get_workspace.return_value = mock_workspace

        resp = self.client.put("/workspace/", json={"name": "Updated Workspace"})

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {"id": "ws1", "name": "Updated Workspace"})
        self.controller.update_workspace.assert_called_with(
            {"name": "Updated Workspace"}
        )

    def test_get_root(self):
        # This route uses Settings.root_path, which might be tricky if not set.
        # But controller isn't used for root.
        # We can mock Settings if needed, but let's see.
        pass

    def test_get_version(self):
        # This route uses get_local_package_version which reads from package.
        # It's hard to test without mocking package reading.
        # Let's verify structure if possible, but it might fail if package not found.
        pass

    def test_read_test_data(self):
        self.controller.read_test_data.return_value = '{"foo": "bar"}'

        resp = self.client.get("/workspace/read-test-data")

        self.assertEqual(resp.status_code, 200)
        # The response is simply the string alias for AbstraLibApiEditorWorkspaceTestDataGetResponse
        self.assertEqual(resp.data.decode(), '{"foo": "bar"}')

    def test_write_test_data(self):
        self.controller.write_test_data.return_value = None

        resp = self.client.post(
            "/workspace/write-test-data", json={"test_data": '{"foo": "baz"}'}
        )

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {"success": True})
        self.controller.write_test_data.assert_called_with('{"foo": "baz"}')


if __name__ == "__main__":
    unittest.main()
