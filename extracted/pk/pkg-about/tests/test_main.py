# Copyright (c) 2020 Adam Karpierz
# SPDX-License-Identifier: Zlib

import unittest
import sys
import os
import copy
import stat
import shutil
from pathlib import Path

from . import test_dir

import pkg_about
from pkg_about._about import adict


class MainTestCase(unittest.TestCase):

    @staticmethod
    def is_namedtuple_instance(obj):
        return (isinstance(obj, tuple) and
                hasattr(obj, '_fields') and
                isinstance(obj._fields, tuple) and
                all(isinstance(field, str) for field in obj._fields))

    @classmethod
    def setUpClass(cls):
        pyproject_path = Path(__file__).resolve().parent.parent/"pyproject.toml"
        if sys.version_info >= (3, 11):
            import tomllib
        else:  # pragma: no cover
            import tomli as tomllib
        with pyproject_path.open("rb") as file:
            metadata = tomllib.load(file).get("project", {})
        cls.version_expected = metadata["version"]
        version_parts = cls.version_expected.split(".")
        cls.version_major_expected = int(version_parts[0])
        cls.version_minor_expected = int(version_parts[1])
        cls.version_micro_expected = int(version_parts[2])

    def test_about(self):
        ret_about = pkg_about.about("pkg_about")
        self.assertIs(__title__, ret_about.__title__)
        self.assertIs(__version__, ret_about.__version__)
        self.assertIs(__version_info__, ret_about.__version_info__)
        self.assertIs(__summary__, ret_about.__summary__)
        self.assertIs(__uri__, ret_about.__uri__)
        self.assertIs(__author__, ret_about.__author__)
        self.assertIs(__email__, ret_about.__email__)
        self.assertIs(__author_email__, ret_about.__author_email__)
        self.assertIs(__maintainer__, ret_about.__maintainer__)
        self.assertIs(__maintainer_email__, ret_about.__maintainer_email__)
        self.assertIs(__license__, ret_about.__license__)
        self.assertIs(__copyright__, ret_about.__copyright__)
        self._check_about(ret_about)
        with self.assertRaises(NameError):
           about
        with self.assertRaises(NameError):
           __metadata__
        self.assertTrue(hasattr(ret_about, "__metadata__"))

    def _check_about(self, about):
        self.assertIsInstance(about, dict)
        self.assertIsInstance(about, adict)
        self.assertEqual(about.__title__, "pkg_about")
        self.assertEqual(about.__version__, self.version_expected)
        self.assertTrue(self.is_namedtuple_instance(about.__version_info__))
        self.assertEqual(about.__version_info__.major, self.version_major_expected)
        self.assertEqual(about.__version_info__.minor, self.version_minor_expected)
        self.assertEqual(about.__version_info__.micro, self.version_micro_expected)
        self.assertEqual(about.__version_info__.releaselevel, "final")
        self.assertEqual(about.__version_info__.serial, 0)
        self.assertEqual(about.__summary__, "Unified access to Python package metadata at runtime.")
        self.assertEqual(about.__uri__, "https://pypi.org/project/pkg-about/")
        self.assertEqual(about.__author__, "Adam Karpierz")
        self.assertEqual(about.__email__, about.__author_email__)
        self.assertEqual(about.__author_email__, "Adam Karpierz <adam@karpierz.net>")
        self.assertEqual(about.__maintainer__, "Adam Karpierz")
        self.assertEqual(about.__maintainer_email__, "Adam Karpierz <adam@karpierz.net>")
        self.assertEqual(about.__license__, "Zlib")
        self.assertEqual(about.__copyright__, __author__)

    def test_about_from_setup(self):
        package_path = Path(__file__).resolve().parent.parent
        setup_cfg = shutil.copy(test_dir/"data/setup.cfg", package_path/"setup.cfg")
        try:
            ret_about = pkg_about.about_from_setup(package_path)
            with self.assertRaises(NameError):
                about
            self._check_about_from_setup(ret_about)
            self.assertTrue(hasattr(ret_about, "__metadata__"))
            # Backward compatibility check
            ret_about = pkg_about.about_from_setup()
            self._check_about_from_setup(about)
            self._check_about_from_setup(ret_about)
            self.assertFalse(hasattr(about, "__metadata__"))
            self.assertTrue(hasattr(ret_about, "__metadata__"))
        finally:
            os.chmod(setup_cfg, stat.S_IWRITE)
            setup_cfg.unlink()

    def _check_about_from_setup(self, about):
        self.assertIsInstance(about, dict)
        self.assertIsInstance(about, adict)
        self.assertEqual(about.__title__, "pkg_about")
        self.assertEqual(about.__version__, self.version_expected)
        self.assertTrue(self.is_namedtuple_instance(about.__version_info__))
        self.assertEqual(about.__version_info__.major, self.version_major_expected)
        self.assertEqual(about.__version_info__.minor, self.version_minor_expected)
        self.assertEqual(about.__version_info__.micro, self.version_micro_expected)
        self.assertEqual(about.__version_info__.releaselevel, "final")
        self.assertEqual(about.__version_info__.serial, 0)
        self.assertEqual(about.__summary__, "Unified access to Python package metadata at runtime.")
        self.assertEqual(about.__uri__, "https://pypi.org/project/pkg-about/")
        self.assertEqual(about.__author__, "John Smith, Adam Karpierz")
        self.assertEqual(about.__email__, about.__author_email__)
        self.assertEqual(about.__author_email__, "Adam Karpierz <adam@karpierz.net>")
        self.assertEqual(about.__maintainer__, "John Smith, Adam Karpierz")
        self.assertEqual(about.__maintainer_email__, "Adam Karpierz <adam@karpierz.net>")
        self.assertEqual(about.__license__, "Zlib")
        self.assertEqual(about.__copyright__, about.__author__)

    def test_about_appdirs(self):
        ret_about = pkg_about.about("appdirs")
        self.assertIsInstance(ret_about, dict)
        self.assertIsInstance(ret_about, adict)
        self.assertIs(__title__, ret_about.__title__)
        self.assertIs(__version__, ret_about.__version__)
        self.assertIs(__version_info__, ret_about.__version_info__)
        self.assertIs(__summary__, ret_about.__summary__)
        self.assertIs(__uri__, ret_about.__uri__)
        self.assertIs(__author__, ret_about.__author__)
        self.assertIs(__email__, ret_about.__email__)
        self.assertIs(__author_email__, ret_about.__author_email__)
        self.assertIs(__maintainer__, ret_about.__maintainer__)
        self.assertIs(__maintainer_email__, ret_about.__maintainer_email__)
        self.assertIs(__license__, ret_about.__license__)
        self.assertIs(__copyright__, ret_about.__copyright__)
        self.assertEqual(ret_about.__title__, "appdirs")
        self.assertEqual(ret_about.__version__, "1.4.4")
        self.assertTrue(self.is_namedtuple_instance(ret_about.__version_info__))
        self.assertEqual(ret_about.__version_info__.major, 1)
        self.assertEqual(ret_about.__version_info__.minor, 4)
        self.assertEqual(ret_about.__version_info__.micro, 4)
        self.assertEqual(ret_about.__version_info__.releaselevel, "final")
        self.assertEqual(ret_about.__version_info__.serial, 0)
        self.assertEqual(ret_about.__summary__, ('A small Python module for determining appropriate'
                                             ' platform-specific dirs, e.g. a "user data dir".'))
        self.assertEqual(ret_about.__uri__, "http://github.com/ActiveState/appdirs")
        self.assertEqual(ret_about.__author__, "Trent Mick")
        self.assertEqual(ret_about.__email__, ret_about.__author_email__)
        self.assertEqual(ret_about.__author_email__, "trentm@gmail.com")
        self.assertEqual(ret_about.__maintainer__, "Jeff Rouse")
        self.assertEqual(ret_about.__maintainer_email__, "jr@its.to")
        self.assertEqual(ret_about.__license__, "MIT")
        self.assertEqual(ret_about.__copyright__, __author__)


class TestAdict(unittest.TestCase):

    def test_item_assignment(self):
        d = adict()
        self.assertNotIn("x", d)
        d["x"] = 10
        self.assertEqual(d.x, 10)
        self.assertEqual(d["x"], 10)

    def test_attribute_assignment(self):
        d = adict()
        self.assertNotIn("x", d)
        d.x = 20
        self.assertEqual(d["x"], 20)
        self.assertEqual(d.x, 20)

    def test_missing_item_raises(self):
        d = adict()
        with self.assertRaises(KeyError):
            _ = d["missing"]

    def test_missing_attribute_raises(self):
        d = adict()
        with self.assertRaises(AttributeError):
            _ = d.missing

    def test_item_deletion(self):
        d = adict(x=5)
        self.assertIn("x", d)
        del d["x"]
        self.assertNotIn("x", d)

    def test_attribute_deletion(self):
        d = adict(x=5)
        self.assertIn("x", d)
        del d.x
        self.assertNotIn("x", d)

    def test_missing_item_deletion_raises(self):
        d = adict()
        with self.assertRaises(KeyError):
            del d["missing"]

    def test_missing_attribute_deletion_raises(self):
        d = adict()
        with self.assertRaises(AttributeError):
            del d.missing

    def test_self_copy_returns_new_instance(self):
        d1 = adict(a=1, b=2)
        d2 = d1.copy()
        self.assertIsInstance(d1, adict)
        self.assertIsInstance(d2, adict)
        self.assertEqual(d2, d1)
        self.assertIsNot(d1, d2)

    def test_copy_returns_new_instance(self):
        d1 = adict(a=1, b=2)
        d2 = copy.copy(d1)
        self.assertIsInstance(d1, adict)
        self.assertIsInstance(d2, adict)
        self.assertEqual(d2, d1)
        self.assertIsNot(d1, d2)

    def test_fromkeys_creates_instance(self):
        d = adict.fromkeys(["a", "b"], 0)
        self.assertIsInstance(d, adict)
        self.assertEqual(d["a"], 0)
        self.assertEqual(d.a, 0)
        self.assertEqual(d["b"], 0)
        self.assertEqual(d.b, 0)
