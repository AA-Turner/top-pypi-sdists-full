from http import HTTPStatus

from django.test import TestCase
from django.test.utils import override_settings

from allauth.socialaccount.models import SocialAccount
from allauth.socialaccount.providers.bitbucket_oauth2.provider import (
    BitbucketOAuth2Provider,
)
from tests.apps.socialaccount.base import OAuth2TestsMixin
from tests.mocking import MockedResponse


@override_settings(SOCIALACCOUNT_QUERY_EMAIL=True, SOCIALACCOUNT_STORE_TOKENS=True)
class BitbucketOAuth2Tests(OAuth2TestsMixin, TestCase):
    provider_id = BitbucketOAuth2Provider.id

    response_data = {
        "account_id": "557123:51e26c4c-1234-dead-cafe-ec0cb6962000",
        "account_status": "active",
        "created_on": "2010-05-19T08:33:59.197853+00:00",
        "display_name": "pennersr",
        "has_2fa_enabled": None,
        "is_staff": False,
        "links": {
            "avatar": {"href": "https://secure.gravatar.com/avatar/some.png"},
            "hooks": {
                "href": "https://api.bitbucket.org/2.0/workspaces/{41c6d04b-dead-cafe-1234-9bffd94346b3}/hooks"
            },
            "html": {
                "href": "https://bitbucket.org/%7B41c6d04b-dead-cafe-1234-9bffd94346b3%7D/"
            },
            "repositories": {
                "href": "https://api.bitbucket.org/2.0/repositories/%7B41c6d04b-dead-cafe-1234-9bffd94346b3%7D"
            },
            "self": {
                "href": "https://api.bitbucket.org/2.0/users/%7B41c6d04b-dead-cafe-1234-9bffd94346b3%7D"
            },
            "snippets": {
                "href": "https://api.bitbucket.org/2.0/snippets/%7B41c6d04b-dead-cafe-1234-9bffd94346b3%7D"
            },
        },
        "location": None,
        "nickname": "pennersr",
        "type": "user",
        "username": "pennersr",
        "uuid": "{41c6d04b-dead-cafe-1234-9bffd94346b3}",
    }

    email_response_data = {
        "page": 1,
        "pagelen": 10,
        "size": 1,
        "values": [
            {
                "email": "tutorials@bitbucket.org",
                "is_confirmed": True,
                "is_primary": True,
                "links": {
                    "self": {
                        "href": "https://api.bitbucket.org/2.0/user/emails/tutorials@bitbucket.org"
                    }
                },
                "type": "email",
            },
            {
                "email": "tutorials+secondary@bitbucket.org",
                "is_confirmed": True,
                "is_primary": True,
                "links": {
                    "self": {
                        "href": "https://api.bitbucket.org/2.0/user/emails/tutorials+secondary@bitbucket.org"
                    }
                },
                "type": "email",
            },
        ],
    }

    def get_mocked_response(self):
        return [
            MockedResponse(HTTPStatus.OK, self.response_data),
            MockedResponse(HTTPStatus.OK, self.email_response_data),
            MockedResponse(HTTPStatus.OK, self.response_data),
            MockedResponse(HTTPStatus.OK, self.email_response_data),
        ]

    def get_expected_to_str(self):
        return "pennersr"

    def test_provider_account(self):
        self.login(self.get_mocked_response())
        socialaccount = SocialAccount.objects.get(uid=self.response_data["account_id"])
        self.assertEqual(socialaccount.user.username, "pennersr")
        self.assertEqual(socialaccount.user.email, "tutorials@bitbucket.org")
        account = socialaccount.get_provider_account()
        self.assertEqual(account.to_str(), "pennersr")
        self.assertEqual(account.get_profile_url(), "https://bitbucket.org/pennersr")
        self.assertEqual(
            account.get_avatar_url(), "https://secure.gravatar.com/avatar/some.png"
        )
