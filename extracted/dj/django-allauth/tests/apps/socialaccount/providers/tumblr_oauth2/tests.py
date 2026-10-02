from http import HTTPStatus

from django.test import TestCase

from allauth.socialaccount.providers.tumblr_oauth2.provider import TumblrOAuth2Provider
from tests.apps.socialaccount.base import OAuth2TestsMixin
from tests.mocking import MockedResponse


class TumblrTests(OAuth2TestsMixin, TestCase):
    provider_id = TumblrOAuth2Provider.id

    def get_mocked_response(self):
        return [
            MockedResponse(
                HTTPStatus.OK,
                {
                    "meta": {"msg": "OK", "status": 200},
                    "response": {
                        "user": {
                            "blogs": [
                                {
                                    "admin": True,
                                    "ask": True,
                                    "ask_anon": False,
                                    "ask_page_title": "Ask me anything",
                                    "asks_allow_media": False,
                                    "avatar": [
                                        {
                                            "accessories": [],
                                            "height": 512,
                                            "url": "https://assets.tumblr.com/images/default_avatar/pyramid_pink_purple_512.png",
                                            "width": 512,
                                        },
                                        {
                                            "accessories": [],
                                            "height": 200,
                                            "url": "https://assets.tumblr.com/images/default_avatar/pyramid_pink_purple_200.png",
                                            "width": 200,
                                        },
                                        {
                                            "accessories": [],
                                            "height": 128,
                                            "url": "https://assets.tumblr.com/images/default_avatar/pyramid_pink_purple_128.png",
                                            "width": 128,
                                        },
                                        {
                                            "accessories": [],
                                            "height": 96,
                                            "url": "https://assets.tumblr.com/images/default_avatar/pyramid_pink_purple_96.png",
                                            "width": 96,
                                        },
                                        {
                                            "accessories": [],
                                            "height": 64,
                                            "url": "https://assets.tumblr.com/images/default_avatar/pyramid_pink_purple_64.png",
                                            "width": 64,
                                        },
                                    ],
                                    "can_chat": False,
                                    "can_send_fan_mail": True,
                                    "can_subscribe": False,
                                    "description": "",
                                    "drafts": 0,
                                    "facebook": "N",
                                    "facebook_opengraph_enabled": "N",
                                    "followed": False,
                                    "followers": 0,
                                    "is_blocked_from_primary": False,
                                    "is_nsfw": False,
                                    "likes": 0,
                                    "messages": 0,
                                    "name": "django-allauth",
                                    "posts": 0,
                                    "primary": True,
                                    "queue": 0,
                                    "share_likes": True,
                                    "share_replies": True,
                                    "subscribed": False,
                                    "theme": {
                                        "avatar_shape": "circle",
                                        "background_color": "#FFFFFF",
                                        "body_font": "Helvetica Neue",
                                        "header_bounds": "",
                                        "header_image": "https://assets.tumblr.com/images/default_header/optica_pattern_13.png?_v=2f4063be1dd2ee91e4eca54332e25191",
                                        "header_image_focused": "https://assets.tumblr.com/images/default_header/optica_pattern_13_focused_v3.png?_v=2f4063be1dd2ee91e4eca54332e25191",
                                        "header_image_poster": "",
                                        "header_image_scaled": "https://assets.tumblr.com/images/default_header/optica_pattern_13_focused_v3.png?_v=2f4063be1dd2ee91e4eca54332e25191",
                                        "header_stretch": True,
                                        "link_color": "#00B8FF",
                                        "show_avatar": True,
                                        "show_description": True,
                                        "show_header_image": True,
                                        "show_title": True,
                                        "title_color": "#000000",
                                        "title_font": "Gibson",
                                        "title_font_weight": "bold",
                                    },
                                    "theme_id": 37310,
                                    "title": "Untitled",
                                    "total_posts": 0,
                                    "tweet": "N",
                                    "twitter_enabled": False,
                                    "twitter_send": False,
                                    "type": "public",
                                    "updated": 0,
                                    "url": "https://www.tumblr.com/blog/view/django-allauth",
                                    "uuid": "t:7RBdHLzN-MNzGhiBFKCaFe",
                                }
                            ],
                            "communities": [],
                            "default_post_format": "html",
                            "following": 0,
                            "likes": 0,
                            "name": "django-allauth",
                        }
                    },
                },
            )
        ]

    def get_expected_to_str(self):
        return "django-allauth"

    def test_extract_uid(self):
        data = {
            "name": "mutable-name",
            "blogs": [
                {"name": "other", "uuid": "t:other"},
                {"name": "mutable-name", "uuid": "t:stable", "primary": True},
            ],
        }
        assert self.provider.extract_uid(data) == "t:stable"
