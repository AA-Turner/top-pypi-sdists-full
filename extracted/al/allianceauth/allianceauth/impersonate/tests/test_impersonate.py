import re

from django.contrib.auth.models import User
from django.test import RequestFactory, TestCase
from django.urls import reverse

from allianceauth.impersonate.admin import ImpersonationLogAdmin
from allianceauth.impersonate.models import ImpersonationLog
from allianceauth.impersonate.permissions import can_impersonate
from allianceauth.impersonate.utils import (
    SESSION_KEY, get_impersonator_pk, is_impersonating,
)
from allianceauth.tests.auth_utils import AuthUtils
from allianceauth.utils.testing import NoSocketsTestCase


def create_superuser(username):
    user = AuthUtils.create_user(username)
    user.is_superuser = True
    user.is_staff = True
    user.save()
    return user


def user_info_classes(response) -> str:
    """Return the class attribute of the sidebar user info block."""
    match = re.search(r'id="aa-user-info"\s+class="([^"]*)"', response.content.decode())
    return match.group(1)


class ImpersonationTestCase(NoSocketsTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.superuser = create_superuser("boss")
        AuthUtils.add_main_character_2(cls.superuser, "Boss Char", 1001)
        cls.target = AuthUtils.create_member("target")
        AuthUtils.add_main_character_2(cls.target, "Target Char", 1002)
        cls.member = AuthUtils.create_member("member")
        AuthUtils.add_main_character_2(cls.member, "Member Char", 1003)

    def start(self, user):
        return self.client.post(reverse("impersonate:start"), {"user_pk": user.pk})

    def stop(self):
        return self.client.post(reverse("impersonate:stop"))

    def session_user_pk(self):
        return int(self.client.session["_auth_user_id"])


class TestCanImpersonate(ImpersonationTestCase):
    def test_superuser_can_impersonate_member(self):
        self.assertTrue(can_impersonate(hijacker=self.superuser, hijacked=self.target))

    def test_member_cannot_impersonate(self):
        self.assertFalse(can_impersonate(hijacker=self.member, hijacked=self.target))

    def test_staff_cannot_impersonate(self):
        self.member.is_staff = True
        self.assertFalse(can_impersonate(hijacker=self.member, hijacked=self.target))

    def test_cannot_impersonate_superuser(self):
        other = create_superuser("boss2")
        self.assertFalse(can_impersonate(hijacker=self.superuser, hijacked=other))

    def test_cannot_impersonate_self(self):
        self.assertFalse(can_impersonate(hijacker=self.superuser, hijacked=self.superuser))

    def test_cannot_impersonate_inactive(self):
        self.target.is_active = False
        self.assertFalse(can_impersonate(hijacker=self.superuser, hijacked=self.target))


class TestConfirmView(ImpersonationTestCase):
    def test_superuser_sees_confirm_page(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse("impersonate:confirm", args=[self.target.pk]))
        self.assertContains(response, reverse("impersonate:start"))
        self.assertContains(response, "Target Char")

    def test_member_is_denied(self):
        self.client.force_login(self.member)
        response = self.client.get(reverse("impersonate:confirm", args=[self.target.pk]))
        self.assertEqual(response.status_code, 403)

    def test_unknown_user_is_404(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse("impersonate:confirm", args=[999999]))
        self.assertEqual(response.status_code, 404)


class TestStartStop(ImpersonationTestCase):
    def test_superuser_can_start(self):
        last_login = User.objects.get(pk=self.target.pk).last_login
        self.client.force_login(self.superuser)

        response = self.start(self.target)

        self.assertRedirects(response, reverse("authentication:dashboard"), fetch_redirect_response=False)
        self.assertEqual(self.session_user_pk(), self.target.pk)
        self.assertEqual(self.client.session[SESSION_KEY], [str(self.superuser.pk)])
        self.assertEqual(User.objects.get(pk=self.target.pk).last_login, last_login)

    def test_start_is_post_only(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse("impersonate:start"), {"user_pk": self.target.pk})
        self.assertNotEqual(self.session_user_pk(), self.target.pk)
        self.assertEqual(response.status_code, 400)

    def test_member_cannot_start(self):
        self.client.force_login(self.member)
        response = self.start(self.target)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.session_user_pk(), self.member.pk)

    def test_superuser_cannot_start_on_superuser(self):
        other = create_superuser("boss2")
        self.client.force_login(self.superuser)
        response = self.start(other)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.session_user_pk(), self.superuser.pk)

    def test_cannot_nest(self):
        self.client.force_login(self.superuser)
        self.start(self.target)
        response = self.start(self.member)
        self.assertEqual(response.status_code, 403)
        self.assertEqual(self.session_user_pk(), self.target.pk)

    def test_stop_returns_to_superuser(self):
        self.client.force_login(self.superuser)
        self.start(self.target)
        self.stop()
        self.assertEqual(self.session_user_pk(), self.superuser.pk)
        self.assertFalse(self.client.session.get(SESSION_KEY))

    def test_stop_works_for_user_without_main(self):
        no_main = AuthUtils.create_member("no_main")
        self.client.force_login(self.superuser)
        self.start(no_main)
        self.stop()
        self.assertEqual(self.session_user_pk(), self.superuser.pk)

    def set_display_preferences(self):
        session = self.client.session
        session["THEME"] = "allianceauth.theme.darkly.auth_hooks.DarklyThemeHook"
        session["NIGHT_MODE"] = True
        session.save()

    def assertDisplayPreferencesKept(self):
        self.assertEqual(self.client.session["THEME"], "allianceauth.theme.darkly.auth_hooks.DarklyThemeHook")
        self.assertTrue(self.client.session["NIGHT_MODE"])

    def test_start_keeps_display_preferences(self):
        self.client.force_login(self.superuser)
        self.set_display_preferences()
        self.start(self.target)
        self.assertEqual(self.session_user_pk(), self.target.pk)
        self.assertDisplayPreferencesKept()

    def test_stop_keeps_display_preferences(self):
        self.client.force_login(self.superuser)
        self.start(self.target)
        self.set_display_preferences()
        self.stop()
        self.assertEqual(self.session_user_pk(), self.superuser.pk)
        self.assertDisplayPreferencesKept()

    def test_denied_start_leaves_session_alone(self):
        self.client.force_login(self.member)
        self.set_display_preferences()
        self.start(self.target)
        self.assertEqual(self.session_user_pk(), self.member.pk)
        self.assertDisplayPreferencesKept()

    def test_stop_when_not_impersonating_is_denied(self):
        self.client.force_login(self.member)
        response = self.stop()
        self.assertEqual(response.status_code, 403)


class TestImpersonationLog(ImpersonationTestCase):
    def test_start_and_stop_are_logged(self):
        self.client.force_login(self.superuser)
        self.start(self.target)

        log = ImpersonationLog.objects.get()
        self.assertEqual(log.impersonator, self.superuser)
        self.assertEqual(log.impersonator_username, "boss")
        self.assertEqual(log.target, self.target)
        self.assertEqual(log.target_username, "target")
        self.assertIsNone(log.ended)

        self.stop()
        log.refresh_from_db()
        self.assertIsNotNone(log.ended)

    def test_logout_ends_log(self):
        self.client.force_login(self.superuser)
        self.start(self.target)
        self.client.post(reverse("logout"))
        self.assertIsNotNone(ImpersonationLog.objects.get().ended)

    def test_log_survives_user_deletion(self):
        self.client.force_login(self.superuser)
        self.start(self.target)
        self.target.delete()
        log = ImpersonationLog.objects.get()
        self.assertIsNone(log.target)
        self.assertEqual(log.target_username, "target")

    def test_admin_is_read_only(self):
        request = RequestFactory().get("/")
        request.user = self.superuser
        model_admin = ImpersonationLogAdmin(ImpersonationLog, None)
        self.assertFalse(model_admin.has_add_permission(request))
        self.assertFalse(model_admin.has_change_permission(request))
        self.assertFalse(model_admin.has_delete_permission(request))


class TestBanner(ImpersonationTestCase):
    def test_banner_shown_while_impersonating(self):
        self.client.force_login(self.superuser)
        self.start(self.target)
        response = self.client.get(reverse("authentication:dashboard"))
        self.assertContains(response, reverse("impersonate:stop"))

    def test_sidebar_shows_impersonation(self):
        self.client.force_login(self.superuser)
        self.start(self.target)
        response = self.client.get(reverse("authentication:dashboard"))
        self.assertContains(response, 'id="aa-user-info"')
        self.assertContains(response, "Impersonating target")
        self.assertIn("text-bg-warning", user_info_classes(response))
        # One stop form each in the banner and the sidebar menu
        self.assertContains(response, f'action="{reverse("impersonate:stop")}"', count=2)
        # Top menu icon points at the banner
        self.assertContains(response, 'href="#impersonation-banner"')
        self.assertContains(response, 'id="impersonation-banner"')

    def test_sidebar_shows_impersonation_for_user_without_main(self):
        no_main = AuthUtils.create_member("no_main")
        self.client.force_login(self.superuser)
        self.start(no_main)
        response = self.client.get(reverse("authentication:dashboard"))
        self.assertContains(response, "Impersonating no_main")

    def test_banner_not_shown_normally(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse("authentication:dashboard"))
        self.assertNotContains(response, reverse("impersonate:stop"))
        self.assertNotContains(response, "Impersonating")
        self.assertNotContains(response, 'href="#impersonation-banner"')
        self.assertNotIn("text-bg-warning", user_info_classes(response))


class TestBlockedWhileImpersonating(ImpersonationTestCase):
    def assertBlocked(self, response):
        self.assertRedirects(response, reverse("authentication:dashboard"), fetch_redirect_response=False)
        self.assertEqual(self.session_user_pk(), self.target.pk)

    def setUp(self):
        self.client.force_login(self.superuser)
        self.start(self.target)

    def test_add_character(self):
        self.assertBlocked(self.client.get(reverse("authentication:add_character")))

    def test_change_main_character(self):
        self.assertBlocked(self.client.get(reverse("authentication:change_main_character")))

    def test_esi_sso_callback(self):
        self.assertBlocked(self.client.get(reverse("esi:callback"), {"code": "x", "state": "y"}))

    def test_service_hook_views(self):
        self.assertBlocked(self.client.get(reverse("discord:activate")))

    def test_theme_change_is_not_saved_to_profile(self):
        self.target.profile.theme = None
        self.target.profile.save()
        self.client.post(reverse("theme"), {"theme": "some.theme"})
        self.target.profile.refresh_from_db()
        self.assertIsNone(self.target.profile.theme)


class TestNotBlockedNormally(ImpersonationTestCase):
    def test_add_character_goes_to_sso(self):
        self.client.force_login(self.member)
        response = self.client.get(reverse("authentication:add_character"))
        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(response["Location"], reverse("authentication:dashboard"))

    def test_theme_change_is_saved_to_profile(self):
        self.client.force_login(self.member)
        self.client.post(reverse("theme"), {"theme": "some.theme"})
        self.member.profile.refresh_from_db()
        self.assertEqual(self.member.profile.theme, "some.theme")


class TestUserAdmin(ImpersonationTestCase):
    def test_superuser_sees_impersonate_link(self):
        self.client.force_login(self.superuser)
        response = self.client.get(reverse("admin:authentication_user_changelist"))
        self.assertContains(response, reverse("impersonate:confirm", args=[self.target.pk]))
        self.assertNotContains(response, reverse("impersonate:confirm", args=[self.superuser.pk]))


class TestUtils(TestCase):
    def test_is_impersonating(self):
        request = RequestFactory().get("/")
        self.assertFalse(is_impersonating(request))  # no session at all

        request.session = {}
        self.assertFalse(is_impersonating(request))
        self.assertIsNone(get_impersonator_pk(request))

        request.session = {SESSION_KEY: ["42"]}
        self.assertTrue(is_impersonating(request))
        self.assertEqual(get_impersonator_pk(request), 42)
