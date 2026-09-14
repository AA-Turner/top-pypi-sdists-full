from django.test import TestCase

from allianceauth.menu.constants import DEFAULT_FOLDER_ICON_CLASSES
from allianceauth.menu.forms import (
    AppMenuItemAdminForm,
    FolderMenuItemAdminForm,
    LinkMenuItemAdminForm,
)


class TestFolderMenuItemAdminForm(TestCase):
    def test_should_set_default_icon_classes(self):
        # given
        form_data = {"text": "Alpha", "order": 1}
        form = FolderMenuItemAdminForm(data=form_data)

        # when
        obj = form.save(commit=False)

        # then
        self.assertEqual(obj.classes, DEFAULT_FOLDER_ICON_CLASSES)

    def test_should_use_icon_classes_from_input(self):
        # given
        form_data = {"text": "Alpha", "order": 1, "classes": "dummy"}
        form = FolderMenuItemAdminForm(data=form_data)

        # when
        obj = form.save(commit=False)

        # then
        self.assertEqual(obj.classes, "dummy")


class TestPermissionFormFields(TestCase):
    def test_link_form_should_include_permission_fields(self):
        # given
        form = LinkMenuItemAdminForm()

        # then
        self.assertIn("permissions", form.fields)
        self.assertIn("permission_mode", form.fields)

    def test_other_forms_should_not_include_permission_fields(self):
        for form_class in [AppMenuItemAdminForm, FolderMenuItemAdminForm]:
            with self.subTest(form=form_class.__name__):
                # given
                form = form_class()

                # then
                self.assertNotIn("permissions", form.fields)
                self.assertNotIn("permission_mode", form.fields)
