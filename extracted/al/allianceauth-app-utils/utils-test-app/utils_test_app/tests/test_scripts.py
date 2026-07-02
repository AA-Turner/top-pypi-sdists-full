import shutil
import tempfile
from pathlib import Path
from unittest import TestCase

from app_utils import scripts


class TestStartDjango(TestCase):
    def setUp(self) -> None:
        self.root_path = Path(tempfile.mkdtemp())
        self.myauth_path = self.root_path / "myauth"
        self.myauth_path.mkdir(parents=True, exist_ok=True)
        (self.myauth_path / "manage.py").touch()

    def tearDown(self) -> None:
        shutil.rmtree(str(self.root_path))

    def test_should_find_project_folder(self):
        # given
        script_path = self.root_path / "one" / "two" / "three" / "four"
        script_path.mkdir(parents=True, exist_ok=True)

        # when
        result = scripts._find_django_path(script_path, 5, "myauth")

        # then
        self.assertEqual(result, self.myauth_path)

    def test_should_return_none_when_project_not_found(self):
        # given
        script_path = self.root_path / "one" / "two" / "three" / "four"
        script_path.mkdir(parents=True, exist_ok=True)

        # when
        result = scripts._find_django_path(script_path, 2, "myauth")

        # then
        self.assertIsNone(result)
