import os
import os.path
import sys
import tempfile
import unittest

skip_cli = False
try:
    import click.testing
except ImportError:
    skip_cli = True

try:
    from urllib.error import URLError
except ImportError:
    from urllib2 import URLError

from confusable_homoglyphs import cli
from confusable_homoglyphs.cli import generate_categories, generate_confusables
from confusable_homoglyphs.utils import get, delete, path


def unicode_org_down():
    try:
        get('ftp://ftp.unicode.org/Public', timeout=5)
        return False
    except URLError:
        return True


@unittest.skipIf(unicode_org_down(), 'www.unicode.org is down')
class TestUpdate(unittest.TestCase):
    def test_generate_categories(self):
        delete('categories.json')
        self.assertFalse(os.path.isfile(path('categories.json')))

        generate_categories()
        self.assertTrue(os.path.isfile(path('categories.json')))

    def test_generate_confusables(self):
        delete('confusables.json')
        self.assertFalse(os.path.isfile(path('confusables.json')))

        generate_confusables()
        self.assertTrue(os.path.isfile(path('confusables.json')))

class TestDataPath(unittest.TestCase):
    def test_default_location(self):
        os.environ.pop("CONFUSABLE_DATA")
        self.assertTrue(os.path.isfile(path('categories.json')))

    def test_custom_non_existing_location(self):
        os.environ["CONFUSABLE_DATA"] = "/path/to/non/existing"
        self.assertFalse(os.path.isfile(path('categories.json')))

    @unittest.skipIf(
        sys.version_info < (3, 10),
        "NamedTemporaryFile worked differently on older python",
    )
    def test_existing_custom_location(self):
        with tempfile.NamedTemporaryFile() as tmp:
            temp_dir, temp_name = os.path.split(tmp.file.name)
            os.environ["CONFUSABLE_DATA"] = temp_dir
            self.assertTrue(os.path.isfile(path(temp_name)))


@unittest.skipIf(skip_cli, 'install click to test the cli')
class TestCheck(unittest.TestCase):
    def test_check_safe(self):
        runner = click.testing.CliRunner()
        res = runner.invoke(
            cli.cli,
            ["check", "-"],
            input="This is safe"
        )
        self.assertEqual(res.exit_code, 0)
        self.assertEqual(res.output, "")

    def test_check_dangerous(self):
        runner = click.testing.CliRunner()
        for s in [
            " ρττ a",
            "ρττ a",
        ]:
            res = runner.invoke(
                cli.cli,
                ["check", "-"],
                input=s,
            )
            self.assertEqual(res.exit_code, 2)
            self.assertIn(s, res.output)
