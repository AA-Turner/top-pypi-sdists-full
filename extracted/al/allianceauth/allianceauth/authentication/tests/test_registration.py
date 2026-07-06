from unittest.mock import patch

from django.core import signing
from django.test import TestCase, override_settings
from django.urls import reverse
from django_registration.backends.activation import REGISTRATION_SALT

from allianceauth.authentication.forms import RegistrationActivationForm
from allianceauth.authentication.models import User

MODULE_PATH = "allianceauth.authentication.views"

# Template rendering uses ManifestStaticFilesStorage which requires collectstatic.
# Override to the simple backend so view tests can render templates freely.
_STATIC_OVERRIDE = override_settings(
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    }
)


def _make_activation_key(username, email, days_offset=0):
    """Return a signed [username, email] activation key, optionally backdated."""
    key = signing.dumps(obj=[username, email], salt=REGISTRATION_SALT)
    if days_offset:
        # Backdate by patching timestamp — sign with a fixed timestamp instead
        # We just re-sign using signing internals for expiry testing; easier to
        # use TimestampSigner directly with a manipulated timestamp.
        import time
        with patch("django.core.signing.time") as mock_time:
            mock_time.time.return_value = time.time() - (days_offset * 86400)
            key = signing.dumps(obj=[username, email], salt=REGISTRATION_SALT)
    return key


@override_settings(ACCOUNT_ACTIVATION_DAYS=1)
class TestRegistrationActivationForm(TestCase):
    def test_valid_key_returns_username_email_pair(self):
        key = _make_activation_key("testuser", "test@example.com")
        form = RegistrationActivationForm(data={"activation_key": key})
        self.assertTrue(form.is_valid(), form.errors)
        self.assertEqual(form.cleaned_data["activation_key"], ["testuser", "test@example.com"])

    def test_expired_key_fails_validation(self):
        key = _make_activation_key("testuser", "test@example.com", days_offset=2)
        form = RegistrationActivationForm(data={"activation_key": key})
        self.assertFalse(form.is_valid())
        self.assertIn("expired", form.errors["activation_key"][0].lower())

    def test_invalid_key_fails_validation(self):
        form = RegistrationActivationForm(data={"activation_key": "not:a:valid:key"})
        self.assertFalse(form.is_valid())
        self.assertIn("invalid", form.errors["activation_key"][0].lower())

    def test_empty_key_fails_validation(self):
        form = RegistrationActivationForm(data={"activation_key": ""})
        self.assertFalse(form.is_valid())


@_STATIC_OVERRIDE
@override_settings(ACCOUNT_ACTIVATION_DAYS=1)
class TestRegistrationView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="newuser", email="", password="x", is_active=False
        )

    def _set_session_uid(self, uid):
        session = self.client.session
        session["registration_uid"] = uid
        session.save()

    def test_get_redirects_without_session_uid(self):
        response = self.client.get(reverse("registration_register"))
        self.assertEqual(response.status_code, 302)

    def test_get_shows_form_with_valid_session(self):
        self._set_session_uid(self.user.pk)
        response = self.client.get(reverse("registration_register"))
        self.assertEqual(response.status_code, 200)

    @patch(MODULE_PATH + ".RegistrationView.send_activation_email")
    def test_post_sends_activation_email(self, mock_send):
        self._set_session_uid(self.user.pk)
        response = self.client.post(
            reverse("registration_register"),
            data={"email": "new@example.com"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(mock_send.called)
        # user email not saved until activation
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    @override_settings(REGISTRATION_VERIFY_EMAIL=False)
    def test_post_activates_user_directly_when_verify_disabled(self):
        self._set_session_uid(self.user.pk)
        response = self.client.post(
            reverse("registration_register"),
            data={"email": "new@example.com"},
        )
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)
        self.assertEqual(self.user.email, "new@example.com")

    def test_get_activation_key_encodes_username_and_email(self):
        from allianceauth.authentication.views import RegistrationView
        view = RegistrationView()
        view.request = self.client.get(reverse("registration_register")).wsgi_request
        self.user.email = "encoded@example.com"
        key = view.get_activation_key(self.user)
        decoded = signing.loads(key, salt=REGISTRATION_SALT, max_age=86400)
        self.assertEqual(decoded, [self.user.username, "encoded@example.com"])

    @patch(MODULE_PATH + ".RegistrationView.send_activation_email")
    def test_get_email_context_url_uses_querystring(self, mock_send):
        from unittest.mock import MagicMock

        from allianceauth.authentication.views import RegistrationView
        self._set_session_uid(self.user.pk)
        # Capture what get_email_context produces via the real view
        view = RegistrationView()
        view.request = self.client.get(reverse("registration_register")).wsgi_request
        key = _make_activation_key(self.user.username, "q@example.com")
        context = view.get_email_context(key)
        self.assertIn("?activation_key=", context["url"])
        self.assertNotIn(key, context["url"].split("?")[0])  # key is not in the path


@_STATIC_OVERRIDE
@override_settings(ACCOUNT_ACTIVATION_DAYS=1)
class TestActivationView(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="activateuser", email="", password="x", is_active=False
        )
        self.email = "activate@example.com"
        self.valid_key = _make_activation_key(self.user.username, self.email)

    def test_get_with_valid_key_returns_200(self):
        url = reverse("registration_activate") + f"?activation_key={self.valid_key}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_get_with_valid_key_shows_form(self):
        url = reverse("registration_activate") + f"?activation_key={self.valid_key}"
        response = self.client.get(url)
        self.assertIn("form", response.context)
        self.assertEqual(
            response.context["form"].initial.get("activation_key"), self.valid_key
        )

    def test_post_with_valid_key_activates_user(self):
        response = self.client.post(
            reverse("registration_activate"),
            data={"activation_key": self.valid_key},
        )
        self.assertRedirects(
            response, reverse("registration_activation_complete"), fetch_redirect_response=False
        )
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)
        self.assertEqual(self.user.email, self.email)

    def test_post_with_valid_key_sets_email_from_key(self):
        different_email = "different@example.com"
        key = _make_activation_key(self.user.username, different_email)
        self.client.post(reverse("registration_activate"), data={"activation_key": key})
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, different_email)

    def test_post_with_expired_key_shows_error(self):
        expired_key = _make_activation_key(self.user.username, self.email, days_offset=2)
        response = self.client.post(
            reverse("registration_activate"),
            data={"activation_key": expired_key},
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["form"].is_valid())
        self.user.refresh_from_db()
        self.assertFalse(self.user.is_active)

    def test_post_with_invalid_key_shows_error(self):
        response = self.client.post(
            reverse("registration_activate"),
            data={"activation_key": "garbage:key:value"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["form"].is_valid())

    def test_post_with_already_active_user_shows_error(self):
        self.user.is_active = True
        self.user.save()
        response = self.client.post(
            reverse("registration_activate"),
            data={"activation_key": self.valid_key},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("activation_error", response.context)

    def test_post_with_nonexistent_user_shows_error(self):
        key = _make_activation_key("ghost_user_does_not_exist", self.email)
        response = self.client.post(
            reverse("registration_activate"),
            data={"activation_key": key},
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("activation_error", response.context)

    def test_get_without_key_returns_200(self):
        # No activation_key in querystring — form renders with empty initial data
        response = self.client.get(reverse("registration_activate"))
        self.assertEqual(response.status_code, 200)

    def test_post_without_key_shows_error(self):
        response = self.client.post(
            reverse("registration_activate"),
            data={"activation_key": ""},
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["form"].is_valid())
