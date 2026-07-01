from __future__ import annotations

from mistralai.workflows.conversational import (
    ChatAssistantWorkingTask,
    CommandResultFailed,
    CommandResultRunning,
    CommandResultSuccess,
    CommandToolUIState,
    CreateFileOperation,
    DeleteFileOperation,
    FileToolUIState,
    GenericToolUIState,
    ReplaceFileOperation,
    SearchReplaceBlock,
    ToolResultFailed,
    ToolResultPending,
    ToolResultRunning,
    ToolResultSuccess,
)


class TestFileToolUIStateSerialization:
    def test_create_operation(self) -> None:
        state = FileToolUIState(
            toolCallId="tc-1",
            operations=[CreateFileOperation(uri="file:///workspace/new.py", content="print('hi')")],
        )
        dumped = state.model_dump(mode="json")
        assert dumped == {
            "type": "file",
            "toolCallId": "tc-1",
            "operations": [
                {
                    "type": "create",
                    "uri": "file:///workspace/new.py",
                    "content": "print('hi')",
                }
            ],
        }

    def test_replace_operation(self) -> None:
        state = FileToolUIState(
            toolCallId="tc-2",
            operations=[
                ReplaceFileOperation(
                    uri="file:///workspace/main.py",
                    fileContentBefore="old code",
                    blocks=[SearchReplaceBlock(search="old", replace="new")],
                )
            ],
        )
        dumped = state.model_dump(mode="json")
        assert dumped == {
            "type": "file",
            "toolCallId": "tc-2",
            "operations": [
                {
                    "type": "replace",
                    "uri": "file:///workspace/main.py",
                    "fileContentBefore": "old code",
                    "blocks": [{"search": "old", "replace": "new"}],
                }
            ],
        }

    def test_delete_operation(self) -> None:
        state = FileToolUIState(
            toolCallId="tc-3",
            operations=[DeleteFileOperation(uri="file:///workspace/old.py")],
        )
        dumped = state.model_dump(mode="json")
        assert dumped == {
            "type": "file",
            "toolCallId": "tc-3",
            "operations": [{"type": "delete", "uri": "file:///workspace/old.py"}],
        }

    def test_multiple_operations(self) -> None:
        state = FileToolUIState(
            toolCallId="tc-4",
            operations=[
                CreateFileOperation(uri="file:///a.py", content="a"),
                ReplaceFileOperation(
                    uri="file:///b.py",
                    fileContentBefore="before",
                    blocks=[
                        SearchReplaceBlock(search="x", replace="y"),
                        SearchReplaceBlock(search="z", replace="w"),
                    ],
                ),
                DeleteFileOperation(uri="file:///c.py"),
            ],
        )
        dumped = state.model_dump(mode="json")
        assert len(dumped["operations"]) == 3
        assert dumped["operations"][0]["type"] == "create"
        assert dumped["operations"][1]["type"] == "replace"
        assert len(dumped["operations"][1]["blocks"]) == 2
        assert dumped["operations"][2]["type"] == "delete"


class TestGenericToolUIStateSerialization:
    def test_running(self) -> None:
        state = GenericToolUIState(
            toolCallId="tc-1",
            name="bash",
            arguments={"command": "ls"},
            result=ToolResultRunning(),
        )
        dumped = state.model_dump(mode="json")
        assert dumped == {
            "type": "generic_tool",
            "toolCallId": "tc-1",
            "name": "bash",
            "arguments": {"command": "ls"},
            "result": {"status": "running"},
        }

    def test_pending(self) -> None:
        state = GenericToolUIState(
            toolCallId="tc-1",
            name="bash",
            arguments={},
            result=ToolResultPending(),
        )
        dumped = state.model_dump(mode="json")
        assert dumped["result"] == {"status": "pending"}

    def test_success(self) -> None:
        state = GenericToolUIState(
            toolCallId="tc-2",
            name="grep",
            arguments={"pattern": "TODO"},
            result=ToolResultSuccess(value={"matches": ["line1"]}),
        )
        dumped = state.model_dump(mode="json")
        assert dumped["result"] == {"status": "success", "value": {"matches": ["line1"]}}

    def test_failed(self) -> None:
        state = GenericToolUIState(
            toolCallId="tc-3",
            name="bash",
            arguments={"command": "false"},
            result=ToolResultFailed(error="exit code 1"),
        )
        dumped = state.model_dump(mode="json")
        assert dumped["result"] == {"status": "failed", "error": "exit code 1"}


class TestChatAssistantWorkingTaskWithToolUIState:
    def test_tool_ui_state_none_by_default(self) -> None:
        task = ChatAssistantWorkingTask(title="Running", content="...")
        dumped = task.model_dump(mode="json")
        assert dumped["toolUIState"] is None

    def test_file_tool_ui_state_serialized(self) -> None:
        task = ChatAssistantWorkingTask(
            title="Writing file",
            content="",
            toolUIState=FileToolUIState(
                toolCallId="tc-1",
                operations=[CreateFileOperation(uri="file:///f.py", content="x")],
            ),
        )
        dumped = task.model_dump(mode="json")
        assert dumped["toolUIState"]["type"] == "file"
        assert dumped["toolUIState"]["operations"][0]["type"] == "create"

    def test_generic_tool_ui_state_serialized(self) -> None:
        task = ChatAssistantWorkingTask(
            title="Running bash",
            content="",
            toolUIState=GenericToolUIState(
                toolCallId="tc-1",
                name="bash",
                arguments={"command": "ls"},
                result=ToolResultRunning(),
            ),
        )
        dumped = task.model_dump(mode="json")
        assert dumped["toolUIState"]["type"] == "generic_tool"
        assert dumped["toolUIState"]["result"]["status"] == "running"


class TestCommandToolUIStateSerialization:
    def test_command_running(self) -> None:
        state = CommandToolUIState(
            toolCallId="tc-1",
            command="npm install",
            result=CommandResultRunning(),
        )
        dumped = state.model_dump(mode="json")
        assert dumped == {
            "type": "command",
            "toolCallId": "tc-1",
            "command": "npm install",
            "result": {"status": "running"},
        }

    def test_command_success(self) -> None:
        state = CommandToolUIState(
            toolCallId="tc-2",
            command="pytest",
            result=CommandResultSuccess(output="All tests passed"),
        )
        dumped = state.model_dump(mode="json")
        assert dumped["result"] == {"status": "success", "output": "All tests passed"}

    def test_command_failed(self) -> None:
        state = CommandToolUIState(
            toolCallId="tc-3",
            command="invalid-command",
            result=CommandResultFailed(error="Command not found"),
        )
        dumped = state.model_dump(mode="json")
        assert dumped["result"] == {"status": "failed", "error": "Command not found"}


class TestChatAssistantWorkingTaskWithCommandToolUIState:
    def test_command_tool_ui_state_serialized(self) -> None:
        task = ChatAssistantWorkingTask(
            title="Running tests",
            content="Executing pytest",
            toolUIState=CommandToolUIState(
                toolCallId="tc-1",
                command="pytest",
                result=CommandResultRunning(),
            ),
        )
        dumped = task.model_dump(mode="json")
        assert dumped["toolUIState"]["type"] == "command"
        assert dumped["toolUIState"]["command"] == "pytest"
        assert dumped["toolUIState"]["result"]["status"] == "running"
