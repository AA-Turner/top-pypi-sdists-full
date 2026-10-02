import os
import unittest
from optional_django import conf
from optional_django.env import DJANGO_INSTALLED, DJANGO_CONFIGURED, DJANGO_SETTINGS
from optional_django.exceptions import ConfigurationError
from optional_django.staticfiles import find
from optional_django import six
from optional_django.serializers import JSONEncoder
from optional_django.safestring import mark_safe


class TestConfUtilsDjangoIntegration(unittest.TestCase):
    def test_env_detection(self):
        self.assertTrue(DJANGO_INSTALLED)
        self.assertTrue(DJANGO_CONFIGURED)
        self.assertIsNotNone(DJANGO_SETTINGS)

    def test_staticfiles_find_matches_relative_and_absolute_paths(self):
        abs_path = os.path.join(os.path.dirname(__file__), 'test_app', 'static', 'test.js')
        self.assertEqual(abs_path, find('test.js'))
        self.assertIsNone(find('test_app/static/test.js'))
        self.assertTrue(os.path.exists(abs_path))
        self.assertEqual(find(abs_path), abs_path)

    def test_six_is_accessible(self):
        self.assertTrue(six.PY2 or six.PY3)

    def test_vendored_six_is_not_django_vendored_version(self):
        from django.utils import six as django_six
        self.assertNotEqual(six, django_six)

    def test_json_encoders_are_available(self):
        from json import JSONEncoder as _JSONEncoder
        self.assertNotEqual(JSONEncoder, _JSONEncoder)
        from django.core.serializers.json import DjangoJSONEncoder
        self.assertEqual(JSONEncoder, DjangoJSONEncoder)

    def test_mark_safe_is_available(self):
        from django.utils.safestring import mark_safe as _mark_safe
        self.assertEqual(mark_safe, _mark_safe)
        string = 'foo'
        self.assertEqual(mark_safe(string), string)