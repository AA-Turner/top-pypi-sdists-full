import datetime
import unittest
from pathlib import Path
from unittest.mock import MagicMock, patch

import flask

from abstra_internals.contracts_generated import (
    AbstraLibApiEditorCodebaseDirPostResponse,
    AbstraLibApiEditorCodebaseFilesDeleteResponse,
    AbstraLibApiEditorCodebaseFilesGetResponseItem,
    AbstraLibApiEditorCodebaseFilesPatchResponse,
    AbstraLibApiEditorCodebaseFilesPutResponse,
    AbstraLibApiEditorCodebaseSettingsGetResponse,
    CommonFileNode,
)
from abstra_internals.repositories.factory import Repositories
from abstra_internals.server.routes.codebase import get_editor_bp
from abstra_internals.settings import Settings


class TestCodebaseRoutes(unittest.TestCase):
    def setUp(self):
        # Fix for Settings.root_path not being set during tests
        self.original_root_path = Settings._root_path
        Settings._root_path = Path(".")

        self.repos = MagicMock(spec=Repositories)

        # Patch CodebaseController in the routes module
        self.patcher = patch(
            "abstra_internals.server.routes.codebase.CodebaseController"
        )
        self.mock_controller_class = self.patcher.start()
        self.mock_controller_instance = self.mock_controller_class.return_value

        self.bp = get_editor_bp(self.repos)
        self.app = flask.Flask(__name__)
        self.app.register_blueprint(self.bp, url_prefix="/codebase")
        self.client = self.app.test_client()

    def tearDown(self):
        self.patcher.stop()
        Settings._root_path = self.original_root_path

    def test_list_files(self):
        mock_node = CommonFileNode(
            path_parts=["file.txt"],
            size=10,
            last_modified=datetime.datetime.now(),
            type="file",
        )
        mock_item = AbstraLibApiEditorCodebaseFilesGetResponseItem(
            file=mock_node, stages=[]
        )
        self.mock_controller_instance.list_files.return_value = [mock_item]

        resp = self.client.get("/codebase/files")
        self.assertEqual(resp.status_code, 200)
        assert resp.json is not None
        self.assertEqual(len(resp.json), 1)
        self.mock_controller_instance.list_files.assert_called()

    def test_get_file(self):
        self.mock_controller_instance.get_file.return_value = flask.Response("content")
        resp = self.client.get("/codebase/files/file.txt")
        self.assertEqual(resp.status_code, 200)
        self.mock_controller_instance.get_file.assert_called_with("file.txt")

    def test_create_file(self):
        mock_node = CommonFileNode(
            path_parts=["new.txt"],
            size=0,
            last_modified=datetime.datetime.now(),
            type="file",
        )
        self.mock_controller_instance.create_file.return_value = mock_node

        resp = self.client.post("/codebase/files/new.txt", data="content")
        self.assertEqual(resp.status_code, 200)
        self.mock_controller_instance.create_file.assert_called()

    def test_edit_file(self):
        self.mock_controller_instance.edit_file.return_value = (
            AbstraLibApiEditorCodebaseFilesPutResponse(ok=True)
        )

        resp = self.client.put(
            "/codebase/files/file.txt", json={"content": "new content"}
        )
        self.assertEqual(resp.status_code, 200)
        assert resp.json is not None
        self.assertTrue(resp.json["ok"])

    def test_delete_file(self):
        self.mock_controller_instance.delete_file.return_value = (
            AbstraLibApiEditorCodebaseFilesDeleteResponse(ok=True)
        )

        resp = self.client.delete("/codebase/files/file.txt")
        self.assertEqual(resp.status_code, 200)
        assert resp.json is not None
        self.assertTrue(resp.json["ok"])

    def test_rename_file(self):
        self.mock_controller_instance.rename_file.return_value = (
            AbstraLibApiEditorCodebaseFilesPatchResponse(ok=True)
        )

        resp = self.client.patch(
            "/codebase/files",
            json={"pathParts": ["old.txt"], "newPathParts": ["new.txt"]},
        )
        self.assertEqual(resp.status_code, 200)
        assert resp.json is not None
        self.assertTrue(resp.json["ok"])

    def test_mkdir(self):
        self.mock_controller_instance.mkdir.return_value = (
            AbstraLibApiEditorCodebaseDirPostResponse(ok=True)
        )

        resp = self.client.post("/codebase/dir/new_dir")
        self.assertEqual(resp.status_code, 200)
        assert resp.json is not None
        self.assertTrue(resp.json["ok"])

    def test_check_file(self):
        self.mock_controller_instance.check_file.return_value = {"exists": True}

        resp = self.client.get("/codebase/check-file?path=file.txt")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {"exists": True})

    def test_check_files(self):
        self.mock_controller_instance.check_files.return_value = {"file.txt": True}

        resp = self.client.post("/codebase/check-files", json={"paths": ["file.txt"]})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {"file.txt": True})

    def test_init_file(self):
        self.mock_controller_instance.init_file.return_value = None

        resp = self.client.post(
            "/codebase/init-file", json={"path": "script.py", "type": "scripts"}
        )
        self.assertEqual(resp.status_code, 200)
        self.mock_controller_instance.init_file.assert_called_with(
            "script.py", "scripts"
        )

    def test_list_files_invalid_mode(self):
        resp = self.client.get("/codebase/files?mode=invalid")
        self.assertEqual(resp.status_code, 400)
        self.mock_controller_instance.list_files.assert_not_called()

    def test_settings(self):
        self.mock_controller_instance.settings.return_value = (
            AbstraLibApiEditorCodebaseSettingsGetResponse(separator="/")
        )

        resp = self.client.get("/codebase/settings")
        self.assertEqual(resp.status_code, 200)
        assert resp.json is not None
        self.assertEqual(resp.json["separator"], "/")

    def test_type_check(self):
        mock_result = MagicMock()
        mock_result.success = True
        mock_result.stdout = "ok"
        mock_result.stderr = ""

        with (
            patch("abstra_internals.server.routes.codebase.Settings") as mock_settings,
            patch(
                "abstra_internals.server.routes.codebase.code_check",
                return_value=mock_result,
            ),
        ):
            mock_settings.root_path.joinpath.return_value = Path("script.py")
            resp = self.client.post("/codebase/type-check/script.py")
            self.assertEqual(resp.status_code, 200)
            assert resp.json is not None
            self.assertTrue(resp.json["success"])
            self.assertEqual(resp.json["stdout"], "ok")
            self.assertEqual(resp.json["stderr"], "")


if __name__ == "__main__":
    unittest.main()
