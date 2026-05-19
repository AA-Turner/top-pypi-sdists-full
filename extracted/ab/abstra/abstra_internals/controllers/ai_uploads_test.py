import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import MagicMock

from werkzeug.datastructures import FileStorage

from abstra_internals.controllers.ai import AiController
from abstra_internals.settings import SettingsController


class TestAiControllerUploads(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.original_root_path = SettingsController._root_path
        SettingsController._root_path = Path(self.tempdir.name)

        self.mock_main_controller = MagicMock()
        self.mock_main_controller.repositories = MagicMock()
        self.controller = AiController(self.mock_main_controller)

    def tearDown(self):
        SettingsController._root_path = self.original_root_path
        self.tempdir.cleanup()

    def _make_file_storage(self, content: bytes, filename: str, mimetype: str):
        from io import BytesIO

        return FileStorage(
            stream=BytesIO(content), filename=filename, content_type=mimetype
        )

    def test_save_uploaded_file_writes_to_ai_uploads_dir(self):
        fs = self._make_file_storage(b"hello", "report.txt", "text/plain")

        result = self.controller.save_uploaded_file(fs, "conv-1")

        self.assertTrue(
            result["filePath"].startswith(os.path.join(".abstra/ai_uploads", "conv-1"))
        )
        self.assertTrue(result["filePath"].endswith("report.txt"))
        self.assertEqual(result["fileName"], "report.txt")
        self.assertEqual(result["fileSize"], 5)
        self.assertEqual(result["mimeType"], "text/plain")

        full = Path(self.tempdir.name) / result["filePath"]
        self.assertTrue(full.exists())
        self.assertEqual(full.read_bytes(), b"hello")

    def test_save_uploaded_file_does_not_overwrite_same_filename(self):
        first = self.controller.save_uploaded_file(
            self._make_file_storage(b"first", "report.txt", "text/plain"), "conv-1"
        )
        second = self.controller.save_uploaded_file(
            self._make_file_storage(b"second", "report.txt", "text/plain"), "conv-1"
        )

        self.assertNotEqual(first["filePath"], second["filePath"])
        self.assertEqual(
            (Path(self.tempdir.name) / first["filePath"]).read_bytes(), b"first"
        )
        self.assertEqual(
            (Path(self.tempdir.name) / second["filePath"]).read_bytes(), b"second"
        )

    def test_save_uploaded_file_strips_path_components_in_name(self):
        fs = self._make_file_storage(b"x", "../../../etc/passwd", "text/plain")
        result = self.controller.save_uploaded_file(fs, "conv-1")
        self.assertEqual(result["fileName"], "passwd")
        self.assertTrue(
            result["filePath"].startswith(os.path.join(".abstra/ai_uploads", "conv-1"))
        )

    def test_save_uploaded_file_sanitizes_conversation_id(self):
        fs = self._make_file_storage(b"x", "a.txt", "text/plain")
        result = self.controller.save_uploaded_file(fs, "../escape")
        # sanitize_filename collapses path separators so there is no real
        # traversal — the resolved path must stay inside ai_uploads.
        full = Path(self.tempdir.name) / result["filePath"]
        self.assertTrue(full.exists())
        uploads_root = (Path(self.tempdir.name) / ".abstra/ai_uploads").resolve()
        self.assertTrue(str(full.resolve()).startswith(str(uploads_root) + os.sep))

    def test_delete_uploaded_file_removes_file(self):
        fs = self._make_file_storage(b"x", "a.txt", "text/plain")
        result = self.controller.save_uploaded_file(fs, "conv-1")
        full = Path(self.tempdir.name) / result["filePath"]
        self.assertTrue(full.exists())

        self.controller.delete_uploaded_file(result["filePath"])
        self.assertFalse(full.exists())

    def test_delete_uploaded_file_rejects_path_traversal(self):
        with self.assertRaises(ValueError):
            self.controller.delete_uploaded_file("../../../etc/passwd")

    def test_delete_uploaded_file_rejects_outside_uploads_dir(self):
        # Create a file outside .abstra/ai_uploads
        outside = Path(self.tempdir.name) / "other" / "secret.txt"
        outside.parent.mkdir(parents=True, exist_ok=True)
        outside.write_text("secret")

        with self.assertRaises(ValueError):
            self.controller.delete_uploaded_file("other/secret.txt")
        self.assertTrue(outside.exists())

    def test_delete_uploaded_file_is_noop_when_missing(self):
        # Should not raise if the file doesn't exist
        self.controller.delete_uploaded_file(".abstra/ai_uploads/conv-x/missing.txt")

    def test_delete_uploaded_file_rejects_uploads_root(self):
        uploads_root = Path(self.tempdir.name) / ".abstra" / "ai_uploads"
        uploads_root.mkdir(parents=True, exist_ok=True)
        with self.assertRaises(ValueError):
            self.controller.delete_uploaded_file(".abstra/ai_uploads")
        self.assertTrue(uploads_root.exists())

    def test_delete_uploaded_file_rejects_directory_inside_uploads(self):
        conv_dir = Path(self.tempdir.name) / ".abstra" / "ai_uploads" / "conv-1"
        conv_dir.mkdir(parents=True, exist_ok=True)
        with self.assertRaises(ValueError):
            self.controller.delete_uploaded_file(".abstra/ai_uploads/conv-1")
        self.assertTrue(conv_dir.exists())


if __name__ == "__main__":
    unittest.main()
