from django.contrib.auth.models import Group, Permission, User
from django.test import TestCase

from allianceauth.tests.auth_utils import AuthUtils
from app_utils.django import (
    add_permissions_to_user_by_name,
    app_labels,
    permission_by_name,
    users_with_permission,
)
from app_utils.testdata_factories import UserFactory


class TestAppLabel(TestCase):
    def test_returns_set_of_app_labels(self):
        labels = app_labels()
        for label in ["authentication", "groupmanagement", "eveonline"]:
            self.assertIn(label, labels)


class TestUsersWithPermissionQS(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.permission = Permission.objects.first()
        if not cls.permission:
            raise RuntimeError("no permission found")
        cls.group, _ = Group.objects.get_or_create(name="Test Group")
        AuthUtils.add_permissions_to_groups([cls.permission], [cls.group])
        cls.state = AuthUtils.create_state(name="Test State", priority=75)
        cls.state.permissions.add(cls.permission)

    def setUp(self) -> None:
        self.user_1 = AuthUtils.create_user("Bruce Wayne")
        self.user_2 = AuthUtils.create_user("Lex Luther")
        self.user_3 = User.objects.create_superuser("Spiderman")

    @classmethod
    def user_with_permission_pks(cls, include_superusers=True) -> set:
        return set(
            users_with_permission(
                cls.permission, include_superusers=include_superusers
            ).values_list("pk", flat=True)
        )

    def test_should_return_users_with_user_permission(self):
        # given
        AuthUtils.add_permissions_to_user([self.permission], self.user_1)
        # when
        result = self.user_with_permission_pks()
        # then
        self.assertSetEqual(result, {self.user_1.pk, self.user_3.pk})

    def test_should_return_users_with_user_permission_excluding_superusers(self):
        # given
        AuthUtils.add_permissions_to_user([self.permission], self.user_1)
        # when
        result = self.user_with_permission_pks(include_superusers=False)
        # then
        self.assertSetEqual(result, {self.user_1.pk})

    def test_group_permission(self):
        """group permissions"""
        self.user_1.groups.add(self.group)
        self.assertSetEqual(
            self.user_with_permission_pks(), {self.user_1.pk, self.user_3.pk}
        )

    def test_state_permission(self):
        """state permissions"""
        AuthUtils.assign_state(self.user_1, self.state, disconnect_signals=True)
        self.assertSetEqual(
            self.user_with_permission_pks(), {self.user_1.pk, self.user_3.pk}
        )

    def test_distinct_qs(self):
        """only return one user object, despite multiple matches"""
        # given
        AuthUtils.add_permissions_to_user([self.permission], self.user_1)
        self.user_1.groups.add(self.group)
        AuthUtils.assign_state(self.user_1, self.state, disconnect_signals=True)
        # when
        result = self.user_with_permission_pks()
        # then
        self.assertSetEqual(result, {self.user_1.pk, self.user_3.pk})


class TestAddPermissionsToUserByName(TestCase):
    def test_can_add_permission_by_name(self):
        user = UserFactory()
        perm_name = "groupmanagement.request_groups"
        self.assertFalse(user.has_perm(perm_name))
        user = add_permissions_to_user_by_name(user, [perm_name])
        self.assertTrue(user.has_perm(perm_name))


class TestPermissionByName(TestCase):
    def test_should_return_permission_when_it_exists(self):
        got = permission_by_name("groupmanagement.request_groups")
        want = Permission.objects.get(
            content_type__app_label="groupmanagement", codename="request_groups"
        )
        self.assertEqual(got, want)

    def test_should_raise_exception_when_permission_does_not_exist_1(self):
        with self.assertRaises(Exception):
            permission_by_name("groupmanagement.invalid")

    def test_should_raise_exception_when_permission_does_not_exist_2(self):
        with self.assertRaises(Exception):
            permission_by_name("auth.request_groups")
