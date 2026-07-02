import json
from unittest.mock import patch

from django.test import TestCase
from django.utils.timezone import now

from app_utils.helpers import chunks
from app_utils.json import JSONDateTimeDecoder, JSONDateTimeEncoder
from app_utils.urls import site_absolute_url

MODULE_PATH = "app_utils"


class TestChunks(TestCase):
    def test_chunks(self):
        a0 = [1, 2, 3, 4, 5, 6]
        a1 = list(chunks(a0, 2))
        self.assertListEqual(a1, [[1, 2], [3, 4], [5, 6]])


class TestGetSiteBaseUrl(TestCase):
    @patch(
        MODULE_PATH + ".urls.settings.ESI_SSO_CALLBACK_URL",
        "https://www.mysite.com/sso/callback",
    )
    def test_return_url_if_url_defined_and_valid(self):
        expected = "https://www.mysite.com"
        self.assertEqual(site_absolute_url(), expected)

    @patch(
        MODULE_PATH + ".urls.settings.ESI_SSO_CALLBACK_URL",
        "https://www.mysite.com/not-valid/",
    )
    def test_return_dummy_if_url_defined_but_not_valid(self):
        expected = ""
        self.assertEqual(site_absolute_url(), expected)

    @patch(MODULE_PATH + ".urls.settings")
    def test_return_dummy_if_url_not_defined(self, mock_settings):
        delattr(mock_settings, "ESI_SSO_CALLBACK_URL")
        expected = ""
        self.assertEqual(site_absolute_url(), expected)


class TestJsonSerializer(TestCase):
    def test_encode_decode(self):
        my_dict = {"alpha": "hello", "bravo": now()}
        my_json = json.dumps(my_dict, cls=JSONDateTimeEncoder)
        my_dict_new = json.loads(my_json, cls=JSONDateTimeDecoder)
        self.assertDictEqual(my_dict, my_dict_new)
