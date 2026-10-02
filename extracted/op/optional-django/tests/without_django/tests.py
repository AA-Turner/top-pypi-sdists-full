import os
import unittest
from optional_django import conf
from optional_django.exceptions import ConfigurationError
from optional_django.staticfiles import find
from optional_django.env import DJANGO_INSTALLED, DJANGO_CONFIGURED, DJANGO_SETTINGS
from optional_django import six
from optional_django.serializers import JSONEncoder
from optional_django.safestring import mark_safe


class TestOptionalDjangoWithoutDjango(unittest.TestCase):
    def test_env_detection(self):
        self.assertTrue(DJANGO_INSTALLED)
        self.assertFalse(DJANGO_CONFIGURED)
        self.assertIsNone(DJANGO_SETTINGS)

    def test_basic_conf_instance(self):
        class Conf(conf.Conf):
            django_namespace = 'TEST_SETTINGS'

            TEST_SETTING_1 = 1
            TEST_SETTING_2 = {
                'FOO': 'BAR'
            }

        settings = Conf()

        self.assertEqual(settings.TEST_SETTING_1, 1)
        self.assertEqual(settings.TEST_SETTING_2, {'FOO': 'BAR'})

        self.assertRaises(ConfigurationError, setattr, settings, 'TEST_SETTING_1', 2)

    def test_conf_instance_can_be_configured_at_runtime(self):
        class Conf(conf.Conf):
            TEST_SETTING_1 = 1
            TEST_SETTING_2 = {
                'FOO': 'BAR'
            }

        settings = Conf()

        self.assertFalse(settings._has_been_configured)

        settings.configure(
            TEST_SETTING_2='foo'
        )

        self.assertTrue(settings._has_been_configured)

        self.assertEqual(settings.TEST_SETTING_1, 1)
        self.assertEqual(settings.TEST_SETTING_2, 'foo')

        self.assertRaises(ConfigurationError, settings.configure, TEST_SETTING_2='this should fail')

    def test_conf_instance_can_not_have_attributes_set(self):
        class Conf(conf.Conf):
            TEST_SETTING_1 = 1
            TEST_SETTING_2 = {
                'FOO': 'BAR'
            }

        settings = Conf()

        self.assertRaises(ConfigurationError, setattr, settings, 'TEST_SETTING_1', 2)

    def test_staticfiles_find_only_matches_absolute_paths(self):
        self.assertIsNone(find('test.js'))
        self.assertIsNone(find('test_app/static/test.js'))
        abs_path = os.path.join(os.path.dirname(__file__), 'test_app', 'static', 'test.js')
        self.assertTrue(os.path.exists(abs_path))
        self.assertEqual(find(abs_path), abs_path)

    def test_six_is_accessible(self):
        self.assertTrue(six.PY2 or six.PY3)

    def test_json_encoders_are_available(self):
        from django.core.serializers.json import DjangoJSONEncoder
        self.assertNotEqual(JSONEncoder, DjangoJSONEncoder)
        from json import JSONEncoder as _JSONEncoder
        self.assertEqual(JSONEncoder, _JSONEncoder)

    def test_mark_safe_is_available(self):
        from django.utils.safestring import mark_safe as _mark_safe
        self.assertNotEqual(mark_safe, _mark_safe)
        string = 'foo'
        self.assertEqual(mark_safe(string), string)