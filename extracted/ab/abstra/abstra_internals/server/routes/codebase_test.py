import datetime
import tempfile
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
from abstra_internals.controllers.codebase import CodebaseController
from abstra_internals.repositories.factory import Repositories
from abstra_internals.server.routes.codebase import get_editor_bp
from abstra_internals.settings import Settings, SettingsController


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


class TestCodebaseControllerListFiles(unittest.TestCase):
    """Unit tests for CodebaseController.list_files logic."""

    def setUp(self):
        self.original_root_path = SettingsController._root_path
        SettingsController._root_path = Path("/tmp/foo")

        mock_project = MagicMock()
        mock_project.get_stages_by_file_path.return_value = []

        self.repos = MagicMock()
        self.repos.project.load.return_value = mock_project

        self.controller = CodebaseController(self.repos)

    def tearDown(self):
        SettingsController._root_path = self.original_root_path

    @patch("abstra_internals.controllers.codebase.FileSystemService")
    def test_list_files_inside_root_uses_relative_path_parts(self, mock_fs):
        """Files inside root are returned with relative path_parts."""
        mock_fs.list_files.return_value = [
            Path("/tmp/foo/form.py"),
        ]

        result = self.controller.list_files(None)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].file.path_parts, ["form.py"])

    @patch("abstra_internals.controllers.codebase.FileSystemService")
    def test_list_files_outside_root_uses_absolute_path_parts(self, mock_fs):
        """Files outside root are returned with absolute path_parts instead of being skipped."""
        mock_fs.list_files.return_value = [
            Path("/tmp/foo/form.py"),  # inside root
            Path("/tmp/agent_work_abc/script.py"),  # outside root
        ]

        result = self.controller.list_files(None)

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0].file.path_parts, ["form.py"])
        self.assertEqual(
            result[1].file.path_parts, ["/", "tmp", "agent_work_abc", "script.py"]
        )

    @patch("abstra_internals.controllers.codebase.FileSystemService")
    def test_list_files_does_not_raise_for_outside_root_paths(self, mock_fs):
        """list_files must not crash when paths outside root are returned."""
        mock_fs.list_files.return_value = [
            Path("/tmp/agent_work_abc/file.py"),
        ]

        try:
            result = self.controller.list_files(None)
        except ValueError as e:
            self.fail(f"list_files raised ValueError: {e}")

        self.assertEqual(len(result), 1)


class TestCodebaseControllerGetFile(unittest.TestCase):
    """Unit tests for CodebaseController.get_file logic."""

    def setUp(self):
        self.original_root_path = SettingsController._root_path
        SettingsController._root_path = Path("/tmp/foo")
        self.repos = MagicMock()
        self.controller = CodebaseController(self.repos)

        self.bp = get_editor_bp(self.repos)
        self.app = flask.Flask(__name__)
        self.app.register_blueprint(self.bp, url_prefix="/codebase")
        self.client = self.app.test_client()

    def tearDown(self):
        SettingsController._root_path = self.original_root_path

    def test_get_file_outside_root_returns_200(self):
        """Files outside root can be read (no 403)."""
        with patch("abstra_internals.controllers.codebase.flask") as mock_flask:
            mock_flask.abort = flask.abort
            mock_flask.send_file.return_value = flask.Response("content")

            outside_file = Path("/tmp/agent_work_abc/script.py")
            with (
                patch.object(outside_file.__class__, "exists", return_value=True),
                patch.object(
                    outside_file.__class__, "resolve", return_value=outside_file
                ),
            ):
                self.controller.get_file(str(outside_file))
                mock_flask.send_file.assert_called()

    def test_get_file_missing_outside_root_returns_404(self):
        """Missing files outside root still return 404."""
        resp = self.client.get(
            "/codebase/read-file?path=/tmp/agent_work_abc/nonexistent.py"
        )
        self.assertEqual(resp.status_code, 404)

    def test_get_file_relative_path_traversal_returns_403(self):
        """Relative paths escaping root (path traversal) are still blocked."""
        resp = self.client.get("/codebase/read-file?path=../../etc/passwd")
        self.assertEqual(resp.status_code, 403)


class TestCodebaseControllerRenameFile(unittest.TestCase):
    """Unit tests for CodebaseController.rename_file logic."""

    def setUp(self):
        self.original_root_path = SettingsController._root_path
        self.tmp_dir = tempfile.TemporaryDirectory()
        SettingsController._root_path = Path(self.tmp_dir.name)

        mock_project = MagicMock()
        mock_project.get_stages_by_file_path.return_value = []

        self.repos = MagicMock()
        self.repos.project.load.return_value = mock_project

        self.controller = CodebaseController(self.repos)

    def tearDown(self):
        SettingsController._root_path = self.original_root_path
        self.tmp_dir.cleanup()

    def test_rename_file_in_root(self):
        """Files in the project root rename correctly."""
        original = Path(self.tmp_dir.name) / "old.py"
        original.write_text("# hi")

        result = self.controller.rename_file(["old.py"], ["new.py"])

        self.assertTrue(result.ok)
        self.assertFalse(original.exists())
        self.assertTrue((Path(self.tmp_dir.name) / "new.py").exists())

    def test_rename_file_inside_subdirectory(self):
        """Files inside subdirectories rename without duplicating the directory.

        Regression test: previously, when newPathParts contained the full
        relative path (e.g. ['hey', 'another_fil.py']), the controller would
        join it onto the parent of the source path, producing
        '/root/hey/hey/another_fil.py' instead of '/root/hey/another_fil.py'.
        """
        subdir = Path(self.tmp_dir.name) / "hey"
        subdir.mkdir()
        original = subdir / "another_file.py"
        original.write_text("# hi")

        result = self.controller.rename_file(
            ["hey", "another_file.py"],
            ["hey", "another_fil.py"],
        )

        self.assertTrue(result.ok)
        self.assertFalse(original.exists())
        self.assertTrue((subdir / "another_fil.py").exists())
        self.assertFalse((subdir / "hey").exists())

    def test_rename_file_moves_across_directories(self):
        """Renaming can also move a file to a different directory."""
        src_dir = Path(self.tmp_dir.name) / "src"
        dst_dir = Path(self.tmp_dir.name) / "dst"
        src_dir.mkdir()
        dst_dir.mkdir()
        original = src_dir / "file.py"
        original.write_text("# hi")

        result = self.controller.rename_file(
            ["src", "file.py"],
            ["dst", "renamed.py"],
        )

        self.assertTrue(result.ok)
        self.assertFalse(original.exists())
        self.assertTrue((dst_dir / "renamed.py").exists())


if __name__ == "__main__":
    unittest.main()
