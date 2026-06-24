import unittest
from unittest.mock import MagicMock, patch

from abstra_internals.controllers import docs as docs_module
from abstra_internals.controllers.docs import DocsController


def _make_controller():
    controller = MagicMock()
    controller.get_stage_guide = DocsController.get_stage_guide.__get__(controller)
    controller.describe_class = DocsController.describe_class.__get__(controller)
    controller.describe_function = DocsController.describe_function.__get__(controller)
    return controller


class TestGetStageGuide(unittest.TestCase):
    def test_page_guide_reads_from_docs(self):
        controller = _make_controller()
        controller.read_abstra_docs.return_value = "page guide content"

        result = controller.get_stage_guide(topic="page", kind="guide")

        controller.read_abstra_docs.assert_called_once_with(
            "/docs/md/workflow/pages/pages.md"
        )
        self.assertEqual(result, "page guide content")

    def test_form_guide_reads_from_docs(self):
        controller = _make_controller()
        controller.read_abstra_docs.return_value = "form guide content"

        result = controller.get_stage_guide(topic="form", kind="guide")

        controller.read_abstra_docs.assert_called_once_with(
            "/docs/md/workflow/forms/step-types.md"
        )
        self.assertEqual(result, "form guide content")

    def test_page_examples_reads_from_local_file(self):
        controller = _make_controller()
        fake_path = MagicMock()
        fake_path.exists.return_value = True
        fake_path.read_text.return_value = "page examples content"
        fake_dir = MagicMock()
        fake_dir.__truediv__.return_value = fake_path

        with patch.object(docs_module, "_AI_GUIDES_DIR", fake_dir):
            result = controller.get_stage_guide(topic="page", kind="examples")

        fake_dir.__truediv__.assert_called_once_with("pages_examples.md")
        self.assertEqual(result, "page examples content")
        controller.read_abstra_docs.assert_not_called()

    def test_form_examples_reads_from_local_file(self):
        controller = _make_controller()
        fake_path = MagicMock()
        fake_path.exists.return_value = True
        fake_path.read_text.return_value = "form examples content"
        fake_dir = MagicMock()
        fake_dir.__truediv__.return_value = fake_path

        with patch.object(docs_module, "_AI_GUIDES_DIR", fake_dir):
            result = controller.get_stage_guide(topic="form", kind="examples")

        fake_dir.__truediv__.assert_called_once_with("forms_examples.md")
        self.assertEqual(result, "form examples content")

    def test_examples_returns_placeholder_when_file_missing(self):
        controller = _make_controller()
        fake_path = MagicMock()
        fake_path.exists.return_value = False
        fake_dir = MagicMock()
        fake_dir.__truediv__.return_value = fake_path

        with patch.object(docs_module, "_AI_GUIDES_DIR", fake_dir):
            result = controller.get_stage_guide(topic="page", kind="examples")

        self.assertEqual(result, "No examples available yet.")
        fake_path.read_text.assert_not_called()

    def test_default_kind_is_guide(self):
        controller = _make_controller()
        controller.read_abstra_docs.return_value = "page guide"

        result = controller.get_stage_guide(topic="page")

        controller.read_abstra_docs.assert_called_once_with(
            "/docs/md/workflow/pages/pages.md"
        )
        self.assertEqual(result, "page guide")


def _sdk_with_class():
    return {
        "abstra.forms": {
            "TextInput": {
                "init": {"params": ["label", "key"]},
                "properties": ["value", "required"],
                "parent_classes": ["Input"],
                "examples": ["TextInput('Name', 'name')"],
            }
        }
    }


def _sdk_with_function():
    return {
        "abstra.tasks": {
            "send_task": {
                "params": ["target", "data"],
                "examples": ["send_task('next', {})"],
                "return_type": "TaskDTO",
            }
        }
    }


class TestDescribeClass(unittest.TestCase):
    def test_default_returns_all_projections(self):
        controller = _make_controller()
        controller.sdk = _sdk_with_class()

        result = controller.describe_class(
            module_name="abstra.forms", class_name="TextInput"
        )

        self.assertEqual(
            result,
            {
                "params": ["label", "key"],
                "properties": ["value", "required"],
                "parents": ["Input"],
                "examples": ["TextInput('Name', 'name')"],
            },
        )

    def test_include_filter_narrows_response(self):
        controller = _make_controller()
        controller.sdk = _sdk_with_class()

        result = controller.describe_class(
            module_name="abstra.forms",
            class_name="TextInput",
            include=["params", "examples"],
        )

        self.assertEqual(
            result,
            {
                "params": ["label", "key"],
                "examples": ["TextInput('Name', 'name')"],
            },
        )

    def test_empty_include_returns_empty_dict(self):
        controller = _make_controller()
        controller.sdk = _sdk_with_class()

        result = controller.describe_class(
            module_name="abstra.forms", class_name="TextInput", include=[]
        )

        self.assertEqual(result, {})

    def test_unknown_projection_in_include_is_skipped(self):
        controller = _make_controller()
        controller.sdk = _sdk_with_class()

        result = controller.describe_class(
            module_name="abstra.forms",
            class_name="TextInput",
            include=["params", "bogus"],  # type: ignore[list-item]
        )

        self.assertEqual(result, {"params": ["label", "key"]})

    def test_incomplete_class_data_does_not_raise(self):
        controller = _make_controller()
        # SDK introspection data missing 'init'/'properties' must not crash.
        controller.sdk = {"abstra.forms": {"TextInput": {"examples": ["TextInput()"]}}}

        result = controller.describe_class(
            module_name="abstra.forms", class_name="TextInput"
        )

        self.assertEqual(
            result,
            {
                "params": None,
                "properties": None,
                "parents": None,
                "examples": ["TextInput()"],
            },
        )


class TestDescribeFunction(unittest.TestCase):
    def test_default_returns_all_projections(self):
        controller = _make_controller()
        controller.sdk = _sdk_with_function()

        result = controller.describe_function(
            module_name="abstra.tasks", function_name="send_task"
        )

        self.assertEqual(
            result,
            {
                "params": ["target", "data"],
                "examples": ["send_task('next', {})"],
                "return_type": "TaskDTO",
            },
        )

    def test_include_filter_returns_only_return_type(self):
        controller = _make_controller()
        controller.sdk = _sdk_with_function()

        result = controller.describe_function(
            module_name="abstra.tasks",
            function_name="send_task",
            include=["return_type"],
        )

        self.assertEqual(result, {"return_type": "TaskDTO"})

    def test_incomplete_function_data_does_not_raise(self):
        controller = _make_controller()
        # SDK introspection data missing 'params' must not crash (regression:
        # this previously raised KeyError('params') even when not requested).
        controller.sdk = {"abstra.tasks": {"send_task": {"return_type": "TaskDTO"}}}

        result = controller.describe_function(
            module_name="abstra.tasks",
            function_name="send_task",
            include=["params"],
        )

        self.assertEqual(result, {"params": None})


if __name__ == "__main__":
    unittest.main()
