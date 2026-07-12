from django.contrib.auth.models import Permission
from django.test import TestCase

from app_utils.django import (
    add_permissions_to_user_by_name,
    app_labels,
    permission_by_name,
    users_with_permission,
)
from app_utils.testdata_factories import (
    EveCharacterFactory,
    GroupFactory,
    StateFactory,
    UserFactory,
    UserMainFactory,
)


class TestAppLabel(TestCase):
    def test_returns_set_of_app_labels(self):
        labels = app_labels()
        for label in ["authentication", "groupmanagement", "eveonline"]:
            self.assertIn(label, labels)


class TestUsersWithPermission(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.perm = Permission.objects.first()
        if not cls.perm:
            raise RuntimeError("no permission found")

        cls.perm_name = f"{cls.perm.content_type.app_label}.{cls.perm.codename}"

    def test_should_include_superusers(self):
        # given
        user = UserFactory(is_superuser=True)
        UserFactory()

        # when
        got = users_with_permission(permission=self.perm)

        # then
        self.assertCountEqual(got, [user])

    def test_should_not_include_superusers(self):
        # given
        UserFactory(is_superuser=True)

        # when
        got = users_with_permission(permission=self.perm, include_superusers=False)

        # then
        self.assertFalse(got)

    def test_should_include_user_with_permission(self):
        # given
        user = UserFactory(permissions=[self.perm_name])
        UserFactory()

        # when
        got = users_with_permission(permission=self.perm)

        # then
        self.assertCountEqual(got, [user])

    def test_should_include_users_inheriting_permission_from_a_group(self):
        # given
        group = GroupFactory()
        group.permissions.add(self.perm.pk)
        user = UserFactory()
        user.groups.add(group)

        UserFactory()

        # when
        got = users_with_permission(permission=self.perm)

        # then
        self.assertCountEqual(got, [user])

    def test_should_include_users_inheriting_permission_from_state(self):
        # given
        character = EveCharacterFactory()
        state = StateFactory(member_characters=[character])
        state.permissions.add(self.perm.pk)
        user = UserMainFactory(main_character__character=character)

        UserMainFactory()

        # when
        got = users_with_permission(permission=self.perm)

        # then
        self.assertCountEqual(got, [user])

    def test_should_return_distinct_objects(self):
        # given
        character = EveCharacterFactory()
        state = StateFactory(member_characters=[character])
        state.permissions.add(self.perm.pk)
        group = GroupFactory()
        group.permissions.add(self.perm.pk)
        user = UserMainFactory(
            main_character__character=character, permissions=[self.perm_name]
        )
        user.groups.add(group)

        UserMainFactory()

        # when
        got = users_with_permission(permission=self.perm)

        # then
        self.assertCountEqual(got, [user])


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
