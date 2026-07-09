import os
import shutil
import zipfile
from pathlib import Path
from tempfile import mkdtemp
from unittest import TestCase
from unittest.mock import MagicMock, patch

import requests

from abstra_internals.interface.cli.deploy import (
    MissingCredentialsError,
    _generate_zip_file,
    _upload_file,
    deploy_without_git,
)
from abstra_internals.services.fs import FileSystemService
from abstra_internals.settings import Settings


class TestGenerateZipFile(TestCase):
    def setUp(self):
        self.original_cwd = Path.cwd()
        self.test_dir = Path(mkdtemp()) / "deploy_zip_test"
        self.test_dir.mkdir(parents=True, exist_ok=True)
        Settings.set_root_path(str(self.test_dir.absolute()))
        FileSystemService.clear_gitignore_cache()

        (self.test_dir / "abstra.json").write_text("{}")
        (self.test_dir / "main.py").write_text("print('hi')")
        (self.test_dir / ".env").write_text("SECRET=should-not-ship")

    def tearDown(self):
        os.chdir(self.original_cwd)
        FileSystemService.clear_gitignore_cache()
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir, ignore_errors=True)

    def _zip_contents(self) -> list:
        zip_path = _generate_zip_file()
        try:
            with zipfile.ZipFile(zip_path, "r") as zf:
                return zf.namelist()
        finally:
            zip_path.unlink(missing_ok=True)

    def test_excludes_root_dotenv_when_not_in_gitignore(self):
        names = self._zip_contents()
        self.assertNotIn(".env", names)
        self.assertIn("abstra.json", names)
        self.assertIn("main.py", names)

    def test_excludes_root_dotenv_when_in_gitignore(self):
        (self.test_dir / ".gitignore").write_text(".env\n")
        names = self._zip_contents()
        self.assertNotIn(".env", names)

    def test_does_not_exclude_nested_dotenv(self):
        nested = self.test_dir / "pkg"
        nested.mkdir()
        (nested / ".env").write_text("ok")
        names = self._zip_contents()
        self.assertIn("pkg/.env", names)


def _http_error(status_code: int) -> requests.HTTPError:
    response = MagicMock()
    response.status_code = status_code
    error = requests.HTTPError(response=response)
    response.raise_for_status.side_effect = error
    return error


def _ok_response() -> MagicMock:
    response = MagicMock()
    response.raise_for_status.return_value = None
    return response


class TestUploadFile(TestCase):
    def setUp(self):
        self.test_dir = Path(mkdtemp()) / "deploy_upload_test"
        self.test_dir.mkdir(parents=True, exist_ok=True)
        self.file_path = self.test_dir / "bundle.zip"
        self.file_path.write_bytes(b"payload")

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_success_does_not_raise(self):
        with patch(
            "abstra_internals.interface.cli.deploy.requests.put",
            return_value=_ok_response(),
        ) as put:
            _upload_file(url="https://s3/upload", file_path=self.file_path)
        put.assert_called_once()

    def test_4xx_fails_fast_without_retry(self):
        # An expired/invalid presigned URL returns 403 — retrying is pointless.
        response = MagicMock()
        response.raise_for_status.side_effect = _http_error(403)
        with (
            patch(
                "abstra_internals.interface.cli.deploy.requests.put",
                return_value=response,
            ) as put,
            patch("abstra_internals.interface.cli.deploy.time.sleep") as sleep,
        ):
            with self.assertRaises(requests.HTTPError):
                _upload_file(url="https://s3/upload", file_path=self.file_path)
        put.assert_called_once()
        sleep.assert_not_called()

    def test_retries_transient_5xx_then_raises(self):
        response = MagicMock()
        response.raise_for_status.side_effect = _http_error(500)
        with (
            patch(
                "abstra_internals.interface.cli.deploy.requests.put",
                return_value=response,
            ) as put,
            patch("abstra_internals.interface.cli.deploy.time.sleep"),
        ):
            with self.assertRaises(requests.HTTPError):
                _upload_file(url="https://s3/upload", file_path=self.file_path)
        self.assertEqual(put.call_count, 3)

    def test_retries_then_succeeds(self):
        ok = _ok_response()
        timeout = requests.Timeout("boom")
        with (
            patch(
                "abstra_internals.interface.cli.deploy.requests.put",
                side_effect=[timeout, ok],
            ) as put,
            patch("abstra_internals.interface.cli.deploy.time.sleep"),
        ):
            _upload_file(url="https://s3/upload", file_path=self.file_path)
        self.assertEqual(put.call_count, 2)


class TestDeployWithoutGitCredentials(TestCase):
    def test_raises_and_does_not_build_when_no_credentials(self):
        # resolve_headers returns None when the user isn't logged in. The deploy
        # must fail loudly (so the editor route returns 400) instead of returning
        # silently and reporting success.
        with (
            patch(
                "abstra_internals.interface.cli.deploy.resolve_headers",
                return_value=None,
            ),
            patch("abstra_internals.interface.cli.deploy.create_build") as create_build,
        ):
            with self.assertRaises(MissingCredentialsError):
                deploy_without_git(show_start_message=False)
        # It must not proceed to create a build with no credentials.
        create_build.assert_not_called()
