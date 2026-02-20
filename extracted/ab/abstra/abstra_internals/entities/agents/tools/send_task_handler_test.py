from unittest.mock import MagicMock

from abstra_internals.entities.agents.tools.send_task_handler import SendTaskHandler


class TestSendTaskHandlerProperties:
    def test_name(self):
        handler = SendTaskHandler(task_type="review", task_sdk=MagicMock())
        assert handler.name == "send_task_review"

    def test_description_without_schema(self):
        handler = SendTaskHandler(task_type="review", task_sdk=MagicMock())
        assert "review" in handler.description
        assert "schema" not in handler.description.lower()

    def test_description_with_schema(self):
        schema = {"type": "object", "properties": {"name": {"type": "string"}}}
        handler = SendTaskHandler(
            task_type="review", task_sdk=MagicMock(), task_schema=schema
        )
        assert "review" in handler.description
        assert "schema" in handler.description.lower()

    def test_input_schema_without_task_schema(self):
        handler = SendTaskHandler(task_type="review", task_sdk=MagicMock())
        schema = handler.input_schema
        assert schema["type"] == "object"

    def test_input_schema_with_task_schema(self):
        custom_schema = {
            "type": "object",
            "properties": {"amount": {"type": "number"}},
        }
        handler = SendTaskHandler(
            task_type="pay", task_sdk=MagicMock(), task_schema=custom_schema
        )
        assert handler.input_schema == custom_schema


class TestSendTaskHandlerExecute:
    def test_execute_calls_send_task(self):
        mock_sdk = MagicMock()
        handler = SendTaskHandler(task_type="process", task_sdk=mock_sdk)

        result = handler.execute({"key": "value"})

        mock_sdk.send_task.assert_called_once_with(
            type="process",
            payload={"key": "value"},
            show_warning=False,
        )
        assert "successfully" in result

    def test_execute_accumulates_sent_tasks(self):
        mock_sdk = MagicMock()
        handler = SendTaskHandler(task_type="notify", task_sdk=mock_sdk)

        handler.execute({"msg": "hello"})
        handler.execute({"msg": "world"})

        sent = handler.get_sent_tasks()
        assert len(sent) == 2
        assert sent[0] == {"type": "notify", "payload": {"msg": "hello"}}
        assert sent[1] == {"type": "notify", "payload": {"msg": "world"}}

    def test_get_sent_tasks_returns_copy(self):
        mock_sdk = MagicMock()
        handler = SendTaskHandler(task_type="x", task_sdk=mock_sdk)

        handler.execute({"a": 1})
        tasks1 = handler.get_sent_tasks()
        tasks1.clear()

        # Original list should not be affected
        assert len(handler.get_sent_tasks()) == 1

    def test_execute_error_handling(self):
        mock_sdk = MagicMock()
        mock_sdk.send_task.side_effect = RuntimeError("network timeout")
        handler = SendTaskHandler(task_type="fail", task_sdk=mock_sdk)

        result = handler.execute({"data": 123})

        assert "Error" in result
        assert "network timeout" in result

    def test_execute_error_does_not_add_to_sent_tasks(self):
        mock_sdk = MagicMock()
        mock_sdk.send_task.side_effect = RuntimeError("boom")
        handler = SendTaskHandler(task_type="fail", task_sdk=mock_sdk)

        handler.execute({"data": 1})

        assert len(handler.get_sent_tasks()) == 0

    def test_get_sent_tasks_initially_empty(self):
        handler = SendTaskHandler(task_type="x", task_sdk=MagicMock())
        assert handler.get_sent_tasks() == []
