from http import HTTPStatus

from django.test import TestCase

from allauth.socialaccount.providers.klaviyo.provider import KlaviyoProvider
from tests.apps.socialaccount.base import OAuth2TestsMixin
from tests.mocking import MockedResponse


class KlaviyoTests(OAuth2TestsMixin, TestCase):
    provider_id = KlaviyoProvider.id

    def get_mocked_response(self):
        return MockedResponse(
            HTTPStatus.OK,
            """{
                "data": [
                    {
                        "type": "account",
                        "id": "ACC123",
                        "attributes": {
                            "test_account": false,
                            "contact_information": {
                                "default_sender_name": "Acme",
                                "default_sender_email": "contact@acme.com",
                                "organization_name": "Acme",
                                "street_address": {
                                    "address1": "1 Main St",
                                    "address2": "",
                                    "city": "Boston",
                                    "region": "MA",
                                    "country": "United States",
                                    "zip": "02118"
                                }
                            },
                            "industry": "Software / SaaS",
                            "timezone": "US/Eastern",
                            "preferred_currency": "USD",
                            "public_api_key": "ABC123",
                            "locale": "en-US"
                        },
                        "links": {
                            "self": "https://a.klaviyo.com/api/accounts/ACC123/"
                        }
                    }
                ]
            }""",
        )

    def get_expected_to_str(self):
        return "Acme"
