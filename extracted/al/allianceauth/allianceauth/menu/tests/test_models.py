from django.contrib.auth.models import AnonymousUser, Group
from django.test import TestCase

from allianceauth.authentication.models import State, User
from allianceauth.menu.models import MenuItem
from allianceauth.tests.auth_utils import AuthUtils

from .factories import (
    create_app_menu_item,
    create_folder_menu_item,
    create_link_menu_item,
    create_user,
)


class TestMenuItem(TestCase):
    def test_str(self):
        # given
        obj = create_link_menu_item()
        # when
        result = str(obj)
        # then
        self.assertIsInstance(result, str)

    def test_should_return_item_type(self):
        # given
        app_item = create_app_menu_item()
        link_item = create_link_menu_item()
        folder_item = create_folder_menu_item()

        cases = [
            (app_item, MenuItem.MenuItemType.APP),
            (link_item, MenuItem.MenuItemType.LINK),
            (folder_item, MenuItem.MenuItemType.FOLDER),
        ]
        # when
        for obj, expected in cases:
            with self.subTest(type=expected):
                self.assertEqual(obj.item_type, expected)

    def test_should_identify_if_item_is_a_child(self):
        # given
        folder = create_folder_menu_item()
        child = create_link_menu_item(parent=folder)
        not_child = create_link_menu_item()

        cases = [(child, True), (not_child, False)]
        # when
        for obj, expected in cases:
            with self.subTest(type=expected):
                self.assertIs(obj.is_child, expected)

    def test_should_identify_if_item_is_a_folder(self):
        # given
        app_item = create_app_menu_item()
        link_item = create_link_menu_item()
        folder_item = create_folder_menu_item()

        cases = [
            (app_item, False),
            (link_item, False),
            (folder_item, True),
        ]
        # when
        for obj, expected in cases:
            with self.subTest(type=expected):
                self.assertIs(obj.is_folder, expected)

    def test_should_identify_if_item_is_user_defined(self):
        # given
        app_item = create_app_menu_item()
        link_item = create_link_menu_item()
        folder_item = create_folder_menu_item()

        cases = [
            (app_item, False),
            (link_item, True),
            (folder_item, True),
        ]
        # when
        for obj, expected in cases:
            with self.subTest(type=expected):
                self.assertIs(obj.is_user_defined, expected)

    def test_should_identify_if_item_is_an_app_item(self):
        # given
        app_item = create_app_menu_item()
        link_item = create_link_menu_item()
        folder_item = create_folder_menu_item()

        cases = [
            (app_item, True),
            (link_item, False),
            (folder_item, False),
        ]
        # when
        for obj, expected in cases:
            with self.subTest(type=expected):
                self.assertIs(obj.is_app_item, expected)

    def test_should_identify_if_item_is_a_link_item(self):
        # given
        app_item = create_app_menu_item()
        link_item = create_link_menu_item()
        folder_item = create_folder_menu_item()

        cases = [
            (app_item, False),
            (link_item, True),
            (folder_item, False),
        ]
        # when
        for obj, expected in cases:
            with self.subTest(type=expected):
                self.assertIs(obj.is_link_item, expected)

    def test_should_not_allow_creating_invalid_app_item(self):
        # when
        obj = create_app_menu_item(hook_hash="")

        # then
        obj.refresh_from_db()
        self.assertIsNone(obj.hook_hash)

    def test_should_give_access_to_everyone_when_no_permissions_assigned(self):
        # given
        item = create_link_menu_item()

        cases = [create_user(), AnonymousUser()]
        # when
        for user in cases:
            with self.subTest(user=str(user)):
                self.assertTrue(item.user_has_access(user))

    def test_any_mode_should_give_access_when_user_has_one_permission(self):
        # given
        item = create_link_menu_item(
            permissions=["auth.add_group", "auth.change_group"],
            permission_mode=MenuItem.PermissionMode.ANY,
        )
        user = create_user(permissions=["auth.add_group"])

        # then
        self.assertTrue(item.user_has_access(user))

    def test_all_mode_should_give_access_when_user_has_all_permissions(self):
        # given
        item = create_link_menu_item(
            permissions=["auth.add_group", "auth.change_group"],
            permission_mode=MenuItem.PermissionMode.ALL,
        )
        user = create_user(permissions=["auth.add_group", "auth.change_group"])

        # then
        self.assertTrue(item.user_has_access(user))

    def test_all_mode_should_deny_access_when_user_has_only_some_permissions(self):
        # given
        item = create_link_menu_item(
            permissions=["auth.add_group", "auth.change_group"],
            permission_mode=MenuItem.PermissionMode.ALL,
        )
        user = create_user(permissions=["auth.add_group"])

        # then
        self.assertFalse(item.user_has_access(user))

    def test_should_deny_access_when_user_has_no_permissions(self):
        # given
        for mode in [MenuItem.PermissionMode.ANY, MenuItem.PermissionMode.ALL]:
            with self.subTest(mode=mode):
                item = create_link_menu_item(
                    permissions=["auth.add_group"], permission_mode=mode
                )

                cases = [create_user(), AnonymousUser()]
                # when
                for user in cases:
                    with self.subTest(user=str(user)):
                        self.assertFalse(item.user_has_access(user))

    def test_should_give_access_to_superusers(self):
        # given
        item = create_link_menu_item(permissions=["auth.add_group"])
        user = create_user(is_superuser=True)

        # then
        self.assertTrue(item.user_has_access(user))

    def test_should_give_access_when_permission_granted_through_group(self):
        # given
        item = create_link_menu_item(permissions=["auth.add_group"])
        group = Group.objects.create(name="dummy")
        group.permissions.add(AuthUtils.get_permission_by_name("auth.add_group"))
        user = create_user()
        user.groups.add(group)
        user = User.objects.get(pk=user.pk)  # avoid stale permission cache

        # then
        self.assertTrue(item.user_has_access(user))

    def test_should_give_access_when_permission_granted_through_state(self):
        # given
        item = create_link_menu_item(permissions=["auth.add_group"])
        state = State.objects.create(name="dummy", priority=200)
        state.permissions.add(AuthUtils.get_permission_by_name("auth.add_group"))
        user = create_user()
        AuthUtils.assign_state(user, state, disconnect_signals=True)
        user = User.objects.get(pk=user.pk)  # avoid stale permission cache

        # then
        self.assertTrue(item.user_has_access(user))


class TestMenuItemToHookObj(TestCase):
    def test_should_create_from_link_item(self):
        # given
        obj = create_link_menu_item(text="Alpha")

        # when
        hook_obj = obj.to_hook_obj()

        # then
        self.assertEqual(hook_obj.text, "Alpha")
        self.assertEqual(hook_obj.url, obj.url)
        self.assertEqual(hook_obj.html_id, "")
        self.assertFalse(hook_obj.is_folder)

    def test_should_create_from_folder(self):
        # given
        obj = create_folder_menu_item(text="Alpha", classes="dummy")

        # when
        hook_obj = obj.to_hook_obj()

        # then
        self.assertEqual(hook_obj.text, "Alpha")
        self.assertEqual(hook_obj.classes, "dummy")
        self.assertEqual(hook_obj.url, "")
        self.assertTrue(hook_obj.html_id)
        self.assertTrue(hook_obj.is_folder)

    def test_should_create_from_folder_and_use_default_icon_classes(self):
        # given
        obj = create_folder_menu_item(classes="")

        # when
        hook_obj = obj.to_hook_obj()

        # then
        self.assertEqual(hook_obj.classes, "fa-solid fa-folder")

    def test_should_create_from_app_item(self):
        # given
        obj = create_app_menu_item(text="Alpha")

        # when
        with self.assertRaises(ValueError):
            obj.to_hook_obj()
