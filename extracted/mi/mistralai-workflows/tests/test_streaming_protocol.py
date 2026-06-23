from mistralai.workflows.protocol.v1.streaming import StreamEventSse, StreamEventSseErrorData


class TestStreamEventSse:
    def test_error_event_data_preserves_reason_and_message(self) -> None:
        event = StreamEventSse.model_validate(
            {
                "event": "error",
                "data": {
                    "error": "Stream read error: Failed to read stream: nats: timeout",
                    "reason": "read_error",
                },
            }
        )

        assert isinstance(event.data, StreamEventSseErrorData)
        assert event.data.reason == "read_error"
        assert event.data.error == "Stream read error: Failed to read stream: nats: timeout"
