import os
import shutil
import zipfile
from pathlib import Path
from tempfile import mkdtemp
from unittest import TestCase

from abstra_internals.interface.cli.deploy import _generate_zip_file
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
