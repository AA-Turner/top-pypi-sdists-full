from http import HTTPStatus

from django.test import TestCase

from allauth.socialaccount.providers.pinterest.provider import PinterestProvider
from tests.apps.socialaccount.base import OAuth2TestsMixin
from tests.mocking import MockedResponse


class PinterestTests(OAuth2TestsMixin, TestCase):
    provider_id = PinterestProvider.id

    def get_mocked_response(self):
        return MockedResponse(
            HTTPStatus.OK,
            {
                "account_type": "BUSINESS",
                "id": "351247977031674143",
                "profile_image": "https://i.pinimg.com/280x280_RS/5c/88/2f/5c882f4b02468fcd6cda2ce569c2c166.jpg",
                "website_url": "https://sns-sdks.github.io/",
                "username": "john_doe",
            },
        )

    def get_expected_to_str(self):
        return "john_doe"

    def test_extract_uid(self):
        data = {"id": "351247977031674143", "username": "john_doe"}
        assert self.provider.extract_uid(data) == "351247977031674143"
