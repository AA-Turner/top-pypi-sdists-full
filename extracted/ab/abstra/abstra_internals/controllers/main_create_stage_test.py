import unittest
from contextlib import contextmanager
from unittest.mock import MagicMock, patch

import pytest

from abstra_internals.controllers.main import MainController


def _make_controller():
    controller = MagicMock()
    controller.create_stage = MainController.create_stage.__get__(controller)

    @contextmanager
    def fake_atomic():
        yield controller.repositories.project

    controller.repositories.project.atomic = fake_atomic
    return controller


class TestCreateStage(unittest.TestCase):
    @patch("abstra_internals.controllers.main.FormStage")
    def test_form_instantiates_form_stage(self, FormStageMock):
        controller = _make_controller()
        sentinel = MagicMock(name="form_stage", file="form.py")
        FormStageMock.create.return_value = sentinel

        result = controller.create_stage(
            "form", "Title", "form.py", workflow_position=(1, 2), id="form-1"
        )

        FormStageMock.create.assert_called_once_with(
            "Title", "form.py", workflow_position=(1, 2), id="form-1"
        )
        controller.init_code_file.assert_called_once()
        controller.repositories.project.add_stage.assert_called_once_with(sentinel)
        self.assertIs(result, sentinel)

    @patch("abstra_internals.controllers.main.PageStage")
    def test_page_instantiates_page_stage(self, PageStageMock):
        controller = _make_controller()
        sentinel = MagicMock(name="page_stage", file="page.py")
        PageStageMock.create.return_value = sentinel

        result = controller.create_stage("page", "Title", "page.py")

        PageStageMock.create.assert_called_once_with(
            "Title", "page.py", workflow_position=(0, 0), id=None
        )
        controller.repositories.project.add_stage.assert_called_once_with(sentinel)
        self.assertIs(result, sentinel)

    @patch("abstra_internals.controllers.main.HookStage")
    def test_hook_instantiates_hook_stage(self, HookStageMock):
        controller = _make_controller()
        sentinel = MagicMock(name="hook_stage", file="hook.py")
        HookStageMock.create.return_value = sentinel

        result = controller.create_stage("hook", "Title", "hook.py")

        HookStageMock.create.assert_called_once()
        controller.repositories.project.add_stage.assert_called_once_with(sentinel)
        self.assertIs(result, sentinel)

    @patch("abstra_internals.controllers.main.JobStage")
    def test_job_instantiates_job_stage(self, JobStageMock):
        controller = _make_controller()
        sentinel = MagicMock(name="job_stage", file="job.py")
        JobStageMock.create.return_value = sentinel

        result = controller.create_stage("job", "Title", "job.py")

        JobStageMock.create.assert_called_once()
        controller.repositories.project.add_stage.assert_called_once_with(sentinel)
        self.assertIs(result, sentinel)

    @patch("abstra_internals.controllers.main.ScriptStage")
    def test_tasklet_instantiates_script_stage(self, ScriptStageMock):
        controller = _make_controller()
        sentinel = MagicMock(name="script_stage", file="tasklet.py")
        ScriptStageMock.create.return_value = sentinel

        result = controller.create_stage("tasklet", "Title", "tasklet.py")

        ScriptStageMock.create.assert_called_once()
        controller.repositories.project.add_stage.assert_called_once_with(sentinel)
        self.assertIs(result, sentinel)

    @patch("abstra_internals.controllers.main.FormStage")
    @patch("abstra_internals.controllers.main.ScriptStage")
    def test_only_one_stage_class_is_instantiated_per_call(
        self, ScriptStageMock, FormStageMock
    ):
        controller = _make_controller()
        FormStageMock.create.return_value = MagicMock(file="form.py")

        controller.create_stage("form", "Title", "form.py")

        FormStageMock.create.assert_called_once()
        ScriptStageMock.create.assert_not_called()

    def test_unknown_type_raises(self):
        controller = _make_controller()
        with pytest.raises(ValueError, match="Unknown stage type"):
            controller.create_stage("bogus", "Title", "file.py")  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
