from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.utils import override_settings

import pytest

from allauth.account import app_settings
from allauth.account.auth_backends import AuthenticationBackend
from allauth.account.models import EmailAddress


class AuthenticationBackendTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create(
            is_active=True, email="john@example.com", username="john"
        )
        user.set_password(user.username)
        user.save()
        self.user = user

    @override_settings(
        ACCOUNT_LOGIN_METHODS={app_settings.LoginMethod.USERNAME}
    )  # noqa
    def test_auth_by_username(self):
        user = self.user
        backend = AuthenticationBackend()
        self.assertEqual(
            backend.authenticate(
                request=None, username=user.username, password=user.username
            ).pk,
            user.pk,
        )
        self.assertEqual(
            backend.authenticate(
                request=None, username=user.username.upper(), password=user.username
            ).pk,
            user.pk,
        )
        self.assertEqual(
            backend.authenticate(
                request=None, username=user.email, password=user.username
            ),
            None,
        )

    @override_settings(
        ACCOUNT_LOGIN_METHODS={app_settings.LoginMethod.USERNAME}
    )  # noqa
    def test_auth_by_username_rejects_db_collation_equivalent(self):
        backend = AuthenticationBackend()
        candidates = get_user_model().objects.filter(pk=self.user.pk)
        with (
            patch(
                "allauth.account.internal.userkit.filter_users_by_username",
                return_value=candidates,
            ),
            patch.object(get_user_model(), "check_password") as check_password,
        ):
            user = backend.authenticate(
                request=None, username="jóhn", password=self.user.username
            )
        self.assertIsNone(user)
        check_password.assert_not_called()

    @override_settings(
        ACCOUNT_LOGIN_METHODS={app_settings.LoginMethod.USERNAME}
    )  # noqa
    def test_auth_by_username_rejects_ambiguous_match(self):
        other_user = get_user_model().objects.create(username="JOHN")
        backend = AuthenticationBackend()
        candidates = get_user_model().objects.filter(
            pk__in=[self.user.pk, other_user.pk]
        )
        with (
            patch(
                "allauth.account.internal.userkit.filter_users_by_username",
                return_value=candidates,
            ),
            patch.object(get_user_model(), "check_password") as check_password,
        ):
            user = backend.authenticate(
                request=None, username="John", password=self.user.username
            )
        self.assertIsNone(user)
        check_password.assert_not_called()

    @override_settings(ACCOUNT_LOGIN_METHODS={app_settings.LoginMethod.EMAIL})  # noqa
    def test_auth_by_email(self):
        user = self.user
        backend = AuthenticationBackend()
        self.assertEqual(
            backend.authenticate(
                request=None, username=user.email, password=user.username
            ).pk,
            user.pk,
        )
        self.assertEqual(
            backend.authenticate(
                request=None, username=user.email.upper(), password=user.username
            ).pk,
            user.pk,
        )
        self.assertEqual(
            backend.authenticate(
                request=None, username=user.username, password=user.username
            ),
            None,
        )

    @override_settings(ACCOUNT_LOGIN_METHODS={app_settings.LoginMethod.EMAIL})  # noqa
    def test_auth_by_email_rejects_unicode_ci_equivalent(self):
        equivalents = {
            "\ufb00oo@example.com": "ffoo@example.com",
            "\uff46oo@example.com": "foo@example.com",
            "stra\u00dfe@example.com": "strasse@example.com",
        }
        for submitted, stored in equivalents.items():
            with self.subTest(submitted=submitted):
                address = EmailAddress(user=self.user, email=stored, verified=True)
                backend = AuthenticationBackend()
                with (
                    patch(
                        "allauth.account.models.EmailAddress.objects.filter"
                    ) as filter_email_addresses,
                    patch.object(get_user_model(), "check_password") as check_password,
                ):
                    filter_email_addresses.return_value.select_related.return_value = [
                        address
                    ]
                    user = backend.authenticate(
                        request=None,
                        username=submitted,
                        password=self.user.username,
                    )
                self.assertIsNone(user)
                check_password.assert_not_called()

    @override_settings(ACCOUNT_LOGIN_METHODS={app_settings.LoginMethod.EMAIL})  # noqa
    def test_auth_by_email_rejects_user_field_unicode_ci_equivalent(self):
        self.user.email = "ffoo@example.com"
        backend = AuthenticationBackend()
        with (
            patch(
                "allauth.account.models.EmailAddress.objects.filter"
            ) as filter_email_addresses,
            patch.object(get_user_model().objects, "filter") as filter_user_email,
            patch.object(get_user_model(), "check_password") as check_password,
        ):
            filter_email_addresses.return_value.select_related.return_value = []
            filter_user_email.return_value.iterator.return_value = [self.user]
            user = backend.authenticate(
                request=None,
                username="\ufb00oo@example.com",
                password=self.user.username,
            )
        self.assertIsNone(user)
        check_password.assert_not_called()

    @override_settings(
        ACCOUNT_LOGIN_METHODS={
            app_settings.LoginMethod.EMAIL,
            app_settings.LoginMethod.USERNAME,
        }
    )  # noqa
    def test_auth_by_username_or_email(self):
        user = self.user
        backend = AuthenticationBackend()
        self.assertEqual(
            backend.authenticate(
                request=None, username=user.email, password=user.username
            ).pk,
            user.pk,
        )
        self.assertEqual(
            backend.authenticate(
                request=None, username=user.username, password=user.username
            ).pk,
            user.pk,
        )


@pytest.mark.parametrize(
    "login_methods",
    [
        {app_settings.LoginMethod.EMAIL},
        {app_settings.LoginMethod.USERNAME},
        {app_settings.LoginMethod.USERNAME, app_settings.LoginMethod.EMAIL},
    ],
)
def test_account_enumeration_timing_attack(user, db, rf, settings, login_methods):
    settings.ACCOUNT_LOGIN_METHODS = login_methods
    with patch("django.contrib.auth.models.User.set_password") as set_password_mock:
        with patch(
            "django.contrib.auth.models.User.check_password", new=set_password_mock
        ):
            backend = AuthenticationBackend()
            backend.authenticate(
                rf.get("/"),
                email="not@known.org",
                username="not-known",
                password="secret",
            )
            set_password_mock.assert_called_once()
            set_password_mock.reset_mock()
            backend.authenticate(rf.get("/"), username=user.username, password="secret")
            set_password_mock.assert_called_once()
            set_password_mock.reset_mock()
            backend.authenticate(
                rf.get("/"), email=user.email, username="not-known", password="secret"
            )
            set_password_mock.assert_called_once()


def test_account_enumeration_timing_attack_email_credentials(user, db, rf, settings):
    settings.ACCOUNT_LOGIN_METHODS = {
        app_settings.LoginMethod.USERNAME,
        app_settings.LoginMethod.EMAIL,
    }
    with patch("django.contrib.auth.models.User.set_password") as password_mock:
        with patch("django.contrib.auth.models.User.check_password", new=password_mock):
            backend = AuthenticationBackend()
            backend.authenticate(rf.get("/"), email="not@known.org", password="secret")
            password_mock.assert_called_once()
            password_mock.reset_mock()
            backend.authenticate(rf.get("/"), email=user.email, password="secret")
            password_mock.assert_called_once()
