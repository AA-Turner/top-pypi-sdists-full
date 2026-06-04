import io
import json
from contextlib import redirect_stderr
from multiprocessing import Pipe
from pathlib import Path
from uuid import uuid4

from abstra_internals.controllers.execution.execution import ExecutionController
from abstra_internals.controllers.execution.execution_client_hook import HookClient
from abstra_internals.entities.execution_context import HookContext, Request, Response
from abstra_internals.modules import import_as_new
from abstra_internals.repositories.project.project import HookStage
from tests.fixtures import BaseTest


class ExecutionControllerTest(BaseTest):
    def setUp(self) -> None:
        super().setUp()

        self.request = Request(
            body={"a": 1}.__str__(),
            headers={"auth": "some_secret_token"},
            query_params={"c": "3"},
            method="GET",
        )

        self.context = HookContext(
            request=Request(
                body={"a": 1}.__str__(),
                headers={"auth": "some_secret_token"},
                query_params={"c": "3"},
                method="GET",
            ),
            response=Response(headers={}, status=200, body=""),
        )

        self.project = self.repositories.project.load(include_disabled_stages=False)
        self.stage = HookStage.create(
            title="mock_stage",
            file="mock_file.py",
            id="mock_hook_id",
            workflow_position=(0, 1),
        )
        Path(self.stage.file).write_text("print('Hello, World!')", encoding="utf-8")
        self.project.add_stage(self.stage)
        self.repositories.project.save(self.project)

        self.parent_conn, child_conn = Pipe()
        self.hook_client = HookClient(
            self.context, conn=child_conn, production_mode=False
        )

    def test_run_initial_returns_dto(self):
        ExecutionController(
            repositories=self.repositories,
            stage=self.stage,
            context=self.context,
            client=self.hook_client,
        ).run(execution_id=uuid4().__str__(), worker_id="mock-worker-id")

        started_msg_str = self.parent_conn.recv()
        assert isinstance(started_msg_str, str), (
            f"Expected str, got {type(started_msg_str)}"
        )

        started_msg = json.loads(started_msg_str)
        assert started_msg["type"] == "execution:started"
        assert "executionId" in started_msg

        response = self.parent_conn.recv()

        if not response:
            self.fail("Response was not set")

        if not isinstance(response, Response):
            response = Response(
                headers=response.get("headers", {}),
                status=response.get("status", 200),
                body=response.get("body", ""),
            )

        self.assertEqual(response.status, 200)

    def test_execution_started_message_is_json_serializable(self):
        """Test that ExecutionStartedMessage is properly serialized to JSON"""
        ExecutionController(
            repositories=self.repositories,
            stage=self.stage,
            context=self.context,
            client=self.hook_client,
        ).run(execution_id="test_execution_id", worker_id="mock-worker-id")

        # Receive and verify the message is a valid JSON string
        started_msg_str = self.parent_conn.recv()
        self.assertIsInstance(started_msg_str, str)

        # Verify it can be parsed as JSON
        try:
            started_msg = json.loads(started_msg_str)
        except json.JSONDecodeError:
            self.fail("ExecutionStartedMessage is not valid JSON")

        # Verify the structure
        self.assertEqual(started_msg["type"], "execution:started")
        self.assertIn("executionId", started_msg)
        self.assertIsInstance(started_msg["executionId"], str)

    def _controller(self) -> ExecutionController:
        return ExecutionController(
            repositories=self.repositories,
            stage=self.stage,
            context=self.context,
            client=self.hook_client,
        )

    def _print_filtered(self, exception: Exception, entrypoint: Path) -> str:
        buffer = io.StringIO()
        with redirect_stderr(buffer):
            self._controller().print_filtered_exception(exception, entrypoint)
        return buffer.getvalue()

    def test_syntax_error_traceback_crops_internal_frames(self):
        """A SyntaxError in the entrypoint fails at compile time, so the user
        frame never reaches the traceback. The internal frames must still be
        cropped, leaving just the SyntaxError and its location."""
        entrypoint = Path("syntax_error_stage.py")
        entrypoint.write_text(
            "from abc import ABC\n\npersonal_details = [\n    1,\n]\n]\n",
            encoding="utf-8",
        )

        try:
            import_as_new(entrypoint.as_posix())
            self.fail("Expected a SyntaxError to be raised")
        except SyntaxError as e:
            output = self._print_filtered(e, entrypoint)

        self.assertIn("SyntaxError", output)
        self.assertIn(entrypoint.name, output)
        # No internal abstra frames nor importlib machinery should leak.
        self.assertNotIn("abstra_internals", output)
        self.assertNotIn("import_as_new", output)
        self.assertNotIn("exec_module", output)
        self.assertNotIn("importlib", output)

    def test_runtime_error_traceback_keeps_user_frame(self):
        """A runtime error in the entrypoint must keep the user frame while
        still cropping the internal frames that precede it."""
        entrypoint = Path("runtime_error_stage.py")
        entrypoint.write_text(
            "def boom():\n    raise ValueError('kaboom')\n\nboom()\n",
            encoding="utf-8",
        )

        try:
            import_as_new(entrypoint.as_posix())
            self.fail("Expected a ValueError to be raised")
        except ValueError as e:
            output = self._print_filtered(e, entrypoint)

        self.assertIn("ValueError", output)
        self.assertIn("kaboom", output)
        self.assertIn(entrypoint.name, output)
        self.assertIn("boom", output)
        # The module-level call site must be kept too (full user chain).
        self.assertIn("in <module>", output)
        # Internal frames before the user entrypoint must be cropped.
        self.assertNotIn("import_as_new", output)
        self.assertNotIn("exec_module", output)

    def test_top_level_name_error_keeps_user_frame(self):
        """A NameError raised directly in the module body (no nested function)
        must keep the entrypoint frame and crop the internal frames."""
        entrypoint = Path("name_error_stage.py")
        entrypoint.write_text("print(undefined_variable)\n", encoding="utf-8")

        try:
            import_as_new(entrypoint.as_posix())
            self.fail("Expected a NameError to be raised")
        except NameError as e:
            output = self._print_filtered(e, entrypoint)

        self.assertIn("NameError", output)
        self.assertIn("undefined_variable", output)
        self.assertIn(entrypoint.name, output)
        self.assertNotIn("import_as_new", output)
        self.assertNotIn("exec_module", output)
        self.assertNotIn("importlib", output)

    def test_zero_division_error_keeps_user_frame(self):
        """A ZeroDivisionError raised deep in nested user calls must keep every
        user frame while still cropping the leading internal frames."""
        entrypoint = Path("zero_division_stage.py")
        entrypoint.write_text(
            "def inner():\n"
            "    return 1 / 0\n"
            "\n"
            "def outer():\n"
            "    return inner()\n"
            "\n"
            "outer()\n",
            encoding="utf-8",
        )

        try:
            import_as_new(entrypoint.as_posix())
            self.fail("Expected a ZeroDivisionError to be raised")
        except ZeroDivisionError as e:
            output = self._print_filtered(e, entrypoint)

        self.assertIn("ZeroDivisionError", output)
        self.assertIn("inner", output)
        self.assertIn("outer", output)
        self.assertIn(entrypoint.name, output)
        self.assertNotIn("import_as_new", output)
        self.assertNotIn("exec_module", output)

    def test_import_error_keeps_user_frame(self):
        """A ModuleNotFoundError raised while importing a nonexistent module is
        a runtime error in the entrypoint body, so its frame must be kept."""
        entrypoint = Path("import_error_stage.py")
        entrypoint.write_text(
            "import this_module_does_not_exist_xyz\n", encoding="utf-8"
        )

        try:
            import_as_new(entrypoint.as_posix())
            self.fail("Expected a ModuleNotFoundError to be raised")
        except ModuleNotFoundError as e:
            output = self._print_filtered(e, entrypoint)

        self.assertIn("ModuleNotFoundError", output)
        self.assertIn("this_module_does_not_exist_xyz", output)
        self.assertIn(entrypoint.name, output)
        self.assertNotIn("import_as_new", output)

    def test_indentation_error_crops_internal_frames(self):
        """IndentationError is a SyntaxError subclass raised at compile time, so
        like SyntaxError it must drop the fully-internal traceback."""
        entrypoint = Path("indentation_error_stage.py")
        entrypoint.write_text("def f():\n    x = 1\n      y = 2\n", encoding="utf-8")

        try:
            import_as_new(entrypoint.as_posix())
            self.fail("Expected an IndentationError to be raised")
        except IndentationError as e:
            output = self._print_filtered(e, entrypoint)

        self.assertIn("IndentationError", output)
        self.assertIn(entrypoint.name, output)
        self.assertNotIn("abstra_internals", output)
        self.assertNotIn("import_as_new", output)
        self.assertNotIn("exec_module", output)
        self.assertNotIn("importlib", output)

    def test_execution_ended_message_is_json_serializable(self):
        """Test that ExecutionEndedMessage is properly serialized to JSON"""
        ExecutionController(
            repositories=self.repositories,
            stage=self.stage,
            context=self.context,
            client=self.hook_client,
        ).run(execution_id="test_execution_id", worker_id="mock-worker-id")

        # Skip the started message
        self.parent_conn.recv()

        # Skip response
        self.parent_conn.recv()

        # Get the ended message
        ended_msg_str = self.parent_conn.recv()
        self.assertIsInstance(ended_msg_str, str)

        # Verify it can be parsed as JSON
        try:
            ended_msg = json.loads(ended_msg_str)
        except json.JSONDecodeError:
            self.fail("ExecutionEndedMessage is not valid JSON")

        # Verify the structure
        self.assertEqual(ended_msg["type"], "execution:ended")
        self.assertIn("exitStatus", ended_msg)
        self.assertEqual(ended_msg["exitStatus"], "SUCCESS")
