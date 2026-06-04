import time
from pathlib import Path

from abstra_internals.contracts_generated import (
    AbstraLibApiEditorCodebaseFilesPutRequest,
)
from tests.fixtures import BaseTest


class ReadFilePaginationMtimeTest(BaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.file_path = self.root / "foo.py"
        self.file_path.write_text("print('hello')\nprint('world')\n", encoding="utf-8")

    def test_read_returns_mtime(self) -> None:
        result = self.controller.read_file_with_pagination("foo.py")
        assert result is not None
        self.assertIn("mtime", result)
        self.assertIsInstance(result["mtime"], float)
        self.assertGreater(result["mtime"], 0.0)

    def test_read_mtime_matches_stat(self) -> None:
        result = self.controller.read_file_with_pagination("foo.py")
        assert result is not None
        self.assertAlmostEqual(
            result["mtime"], self.file_path.stat().st_mtime, places=3
        )

    def test_read_empty_range_returns_mtime(self) -> None:
        result = self.controller.read_file_with_pagination(
            "foo.py", start_line=100, end_line=200
        )
        assert result is not None
        self.assertIn("mtime", result)

    def test_read_nested_file_returns_posix_path(self) -> None:
        nested_dir = self.root / "forms"
        nested_dir.mkdir(parents=True, exist_ok=True)
        (nested_dir / "x.py").write_text("print('nested')\n", encoding="utf-8")

        result = self.controller.read_file_with_pagination("forms/x.py")
        assert result is not None
        self.assertEqual(result["file"], "forms/x.py")
        self.assertNotIn("\\", result["file"])

    def test_read_path_outside_project_is_rejected(self) -> None:
        result = self.controller._read_file_lines_with_pagination(
            Path(__file__), None, None, 500
        )
        assert result is not None
        self.assertIn("error", result)


class IfUnmodifiedSincePutTest(BaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.client = self.get_editor_flask_client()
        self.file_path = self.root / "foo.py"
        self.file_path.write_text("original\n", encoding="utf-8")
        self.put_url = "/_editor/api/codebase/files/foo.py"
        self.put_body = AbstraLibApiEditorCodebaseFilesPutRequest(
            content="changed\n"
        ).to_dict()

    def test_put_without_header_succeeds(self) -> None:
        response = self.client.put(self.put_url, json=self.put_body)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.file_path.read_text(encoding="utf-8"), "changed\n")

    def test_put_with_fresh_mtime_succeeds(self) -> None:
        mtime = self.file_path.stat().st_mtime
        response = self.client.put(
            self.put_url,
            json=self.put_body,
            headers={"X-Expected-Mtime": str(mtime)},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.file_path.read_text(encoding="utf-8"), "changed\n")

    def test_put_with_stale_mtime_returns_412(self) -> None:
        stale_mtime = self.file_path.stat().st_mtime
        time.sleep(0.05)
        self.file_path.write_text("external edit\n", encoding="utf-8")

        response = self.client.put(
            self.put_url,
            json=self.put_body,
            headers={"X-Expected-Mtime": str(stale_mtime)},
        )
        self.assertEqual(response.status_code, 412)
        body = response.json or {}
        self.assertEqual(body.get("error"), "stale_file")
        self.assertIn("currentMtime", body)
        self.assertIn("expectedMtime", body)
        self.assertEqual(self.file_path.read_text(encoding="utf-8"), "external edit\n")

    def test_put_with_malformed_header_returns_400(self) -> None:
        response = self.client.put(
            self.put_url,
            json=self.put_body,
            headers={"X-Expected-Mtime": "not-a-number"},
        )
        self.assertEqual(response.status_code, 400)


class IfUnmodifiedSincePostOverwriteTest(BaseTest):
    def setUp(self) -> None:
        super().setUp()
        self.client = self.get_editor_flask_client()
        self.file_path = self.root / "foo.py"
        self.file_path.write_text("original\n", encoding="utf-8")

    def test_overwrite_with_stale_mtime_returns_412(self) -> None:
        stale_mtime = self.file_path.stat().st_mtime
        time.sleep(0.05)
        self.file_path.write_text("external edit\n", encoding="utf-8")

        response = self.client.post(
            "/_editor/api/codebase/files/foo.py?overwrite=true",
            data=b"smart chat content",
            headers={"X-Expected-Mtime": str(stale_mtime)},
        )
        self.assertEqual(response.status_code, 412)
        self.assertEqual(self.file_path.read_text(encoding="utf-8"), "external edit\n")

    def test_overwrite_with_fresh_mtime_succeeds(self) -> None:
        mtime = self.file_path.stat().st_mtime
        response = self.client.post(
            "/_editor/api/codebase/files/foo.py?overwrite=true",
            data=b"smart chat content",
            headers={"X-Expected-Mtime": str(mtime)},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            self.file_path.read_text(encoding="utf-8"), "smart chat content"
        )

    def test_create_new_file_ignores_header(self) -> None:
        response = self.client.post(
            "/_editor/api/codebase/files/new.py",
            data=b"new content",
            headers={"X-Expected-Mtime": "999999"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            (self.root / "new.py").read_text(encoding="utf-8"), "new content"
        )
