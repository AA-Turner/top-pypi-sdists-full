import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import flask

from abstra_internals.controllers.main import MainController
from abstra_internals.server.routes.deploy import get_editor_bp
from abstra_internals.settings import Settings


class TestDeployRoutes(unittest.TestCase):
    def setUp(self):
        # Fix for Settings.root_path not being set
        self.original_root_path = Settings._root_path
        Settings._root_path = Path(".")

        self.controller = MagicMock(spec=MainController)

        # Patch GitController where it is used (in the deploy route module)
        self.git_patcher = patch("abstra_internals.server.routes.deploy.GitController")
        self.mock_git_controller_class = self.git_patcher.start()
        self.mock_git_controller = self.mock_git_controller_class.return_value

        self.bp = get_editor_bp(self.controller)
        self.app = flask.Flask(__name__)
        self.app.register_blueprint(self.bp, url_prefix="/deploy")
        self.client = self.app.test_client()

    def tearDown(self):
        self.git_patcher.stop()
        Settings._root_path = self.original_root_path

    def test_deploy_direct_success(self):
        self.controller.deploy_without_git.return_value = None

        resp = self.client.post("/deploy/", json={"strategy": "direct"})

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {"success": True})
        self.controller.deploy_without_git.assert_called_once()

    def test_deploy_direct_failure(self):
        self.controller.deploy_without_git.side_effect = Exception("Deploy failed")

        resp = self.client.post("/deploy/", json={"strategy": "direct"})

        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json, {"success": False, "message": "Deploy failed"})

    def test_deploy_git_invalid_strategy(self):
        resp = self.client.post("/deploy/", json={"strategy": "unknown"})

        self.assertEqual(resp.status_code, 400)
        assert resp.json is not None
        self.assertTrue(resp.json["message"].startswith("Unknown strategy"))


if __name__ == "__main__":
    unittest.main()
