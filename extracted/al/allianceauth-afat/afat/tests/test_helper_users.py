# Django
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType

# Alliance Auth AFAT
from afat.helper.users import users_with_permission
from afat.tests import BaseTestCase


class TestUsersWithPermission(BaseTestCase):
    def test_returns_users_with_specific_permission(self):
        """
        Test returns users with specific permission

        :return:
        :rtype:
        """

        content_type = ContentType.objects.get_for_model(User)
        permission = Permission.objects.create(
            codename="can_view", name="Can view", content_type=content_type
        )
        user = User.objects.create(username="user1")
        user.user_permissions.add(permission)

        result = users_with_permission(permission=permission)

        self.assertIn(user, result)

    def test_includes_superusers_when_flag_is_true(self):
        """
        Test includes superusers when flag is true

        :return:
        :rtype:
        """

        content_type = ContentType.objects.get_for_model(User)
        permission = Permission.objects.create(
            codename="can_edit", name="Can edit", content_type=content_type
        )
        superuser = User.objects.create(username="superuser", is_superuser=True)

        result = users_with_permission(permission=permission, include_superusers=True)

        self.assertIn(superuser, result)

    def test_excludes_superusers_when_flag_is_false(self):
        """
        Test excludes superusers when flag is false

        :return:
        :rtype:
        """

        content_type = ContentType.objects.get_for_model(User)
        permission = Permission.objects.create(
            codename="can_delete", name="Can delete", content_type=content_type
        )
        superuser = User.objects.create(username="superuser", is_superuser=True)

        result = users_with_permission(permission=permission, include_superusers=False)

        self.assertNotIn(superuser, result)

    def test_returns_distinct_users_when_user_belongs_to_multiple_groups(self):
        """
        Test returns distinct users when user belongs to multiple groups

        :return:
        :rtype:
        """

        content_type = ContentType.objects.get_for_model(User)
        permission = Permission.objects.create(
            codename="can_manage", name="Can manage", content_type=content_type
        )

        group1 = Group.objects.create(name="Group1")
        group2 = Group.objects.create(name="Group2")

        user = User.objects.create(username="user2")
        user.groups.add(group1, group2)

        group1.permissions.add(permission)
        group2.permissions.add(permission)

        result = users_with_permission(permission=permission)

        self.assertEqual(result.count(), 1)
        self.assertIn(user, result)

    def test_returns_empty_queryset_when_no_users_have_permission(self):
        """
        Test returns empty queryset when no users have permission

        :return:
        :rtype:
        """

        content_type = ContentType.objects.get_for_model(User)
        permission = Permission.objects.create(
            codename="can_publish", name="Can publish", content_type=content_type
        )

        result = users_with_permission(permission=permission)

        self.assertEqual(result.count(), 0)
