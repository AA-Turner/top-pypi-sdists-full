import pytest

from novita_sandbox.core.template.main import TemplateBase
from novita_sandbox.core.template.types import InstructionType


class TestPatchCmd:
    def test_single_string_serializes_correctly(self):
        t = TemplateBase()
        builder = t.from_python_image("3.12")
        builder.set_patch_cmd('echo "patch complete" && touch /tmp/patch-done')
        builder.set_start_cmd("python app.py", "echo ready")

        result = t._serialize([])

        assert result["startCmd"] == "python app.py"
        assert result["fromImage"] == "python:3.12"
        assert "preBootScript" in result
        assert result["preBootScript"] == 'echo "patch complete" && touch /tmp/patch-done'

    def test_not_set_produces_no_field(self):
        t = TemplateBase()
        builder = t.from_python_image("3.12")
        builder.set_start_cmd("python app.py", "echo ready")

        result = t._serialize([])

        assert "preBootScript" not in result

    def test_chaining_with_other_methods(self):
        t = TemplateBase()
        builder = t.from_python_image("3.12")
        builder.set_patch_cmd("mkdir -p /app/data && echo configured > /tmp/provision.log")
        builder.run_cmd("echo hello")
        builder.copy("app.py", "/home/user/app.py")
        builder.set_start_cmd("python app.py", "echo ready")

        result = t._serialize([])

        assert "preBootScript" in result
        assert result["fromImage"] == "python:3.12"

        types = [inst["type"] for inst in t._instructions]
        assert InstructionType.RUN in types
        assert InstructionType.COPY in types

    def test_serialized_with_ready_cmd(self):
        t = TemplateBase()
        builder = t.from_python_image("3.12")
        builder.set_patch_cmd("mkdir -p /app/data")
        builder.set_start_cmd(
            "python app.py", "curl -f http://localhost:8080/health"
        )

        result = t._serialize([])

        assert result["preBootScript"] == "mkdir -p /app/data"
        assert result["startCmd"] == "python app.py"
        assert result["readyCmd"] == "curl -f http://localhost:8080/health"
