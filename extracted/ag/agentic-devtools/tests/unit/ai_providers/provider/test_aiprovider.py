import pytest

from agentic_devtools.ai_providers.errors import ProviderError
from agentic_devtools.ai_providers.models import ModelRecord, TaskHandle, TaskRequest, TaskState
from agentic_devtools.ai_providers.provider import AIProvider


class DummyProvider(AIProvider):
    def __init__(
        self,
        *,
        bad_get_result: object = None,
        use_bad_get_result: bool = False,
        bad_create_result: object = None,
        use_bad_create_result: bool = False,
    ) -> None:
        self.seen_task_id: str | None = None
        self.seen_request: TaskRequest | None = None
        self._bad_get_result = bad_get_result
        self._use_bad_get_result = use_bad_get_result
        self._bad_create_result = bad_create_result
        self._use_bad_create_result = use_bad_create_result

    @property
    def provider_name(self) -> str:
        return "DummyProvider"

    def _discover_models(self) -> list[ModelRecord]:
        return []

    def _create_task(self, request: TaskRequest) -> TaskHandle:
        self.seen_request = request
        if self._use_bad_create_result:
            return self._bad_create_result  # type: ignore[return-value]
        return TaskHandle(task_id="123", state=None, failure=None, metadata={})

    def _get_task(self, task_id: str) -> TaskState:
        self.seen_task_id = task_id
        if self._use_bad_get_result:
            return self._bad_get_result  # type: ignore[return-value]
        return TaskState(
            state="completed",
            failure=None,
            created_at="2023-01-01T00:00:00Z",
            metadata={},
        )


def test_ai_provider_impl() -> None:
    provider = DummyProvider()
    assert provider.provider_name == "DummyProvider"

    assert provider.discover_models() == []
    handle = provider.create_task(TaskRequest(model_id="m", prompt="p", context=None, parameters={}, metadata=None))
    assert handle.task_id == "123"

    state = provider.get_task("123")
    assert state.state == "completed"
    assert provider.seen_task_id == "123"


@pytest.mark.parametrize("task_id", [None, "", "bad id", "slash/value", 123, True])
def test_get_task_rejects_invalid_task_ids(task_id: object) -> None:
    provider = DummyProvider()

    with pytest.raises(
        ProviderError,
        match=r"task_id must be a non-empty string matching \^\[A-Za-z0-9_-\]\+\$",
    ):
        provider.get_task(task_id)  # type: ignore[arg-type]

    assert provider.seen_task_id is None


def test_ai_provider_rejects_overridden_get_task() -> None:
    with pytest.raises(
        TypeError,
        match="AIProvider subclasses must implement _get_task\\(\\) instead of overriding get_task\\(\\)\\.",
    ):

        class InvalidProvider(AIProvider):
            @property
            def provider_name(self) -> str:
                return "InvalidProvider"

            def _discover_models(self) -> list[ModelRecord]:
                return []

            def _create_task(self, request: TaskRequest) -> TaskHandle:
                return TaskHandle(task_id="123", state=None, failure=None, metadata={})

            def get_task(self, task_id: str) -> TaskState:  # type: ignore[misc]
                return TaskState(
                    state="completed",
                    failure=None,
                    created_at="2023-01-01T00:00:00Z",
                    metadata={},
                )


def test_ai_provider_rejects_mro_bypassed_get_task() -> None:
    class GetTaskMixin:
        def get_task(self, task_id: str) -> TaskState:
            return TaskState(
                state="completed",
                failure=None,
                created_at="2023-01-01T00:00:00Z",
                metadata={},
            )

    with pytest.raises(
        TypeError,
        match="AIProvider subclasses must implement _get_task\\(\\) instead of overriding get_task\\(\\)\\.",
    ):

        class InvalidMroProvider(GetTaskMixin, AIProvider):  # type: ignore[misc]
            @property
            def provider_name(self) -> str:
                return "InvalidMroProvider"

            def _discover_models(self) -> list[ModelRecord]:
                return []

            def _create_task(self, request: TaskRequest) -> TaskHandle:
                return TaskHandle(task_id="123", state=None, failure=None, metadata={})

            def _get_task(self, task_id: str) -> TaskState:
                return TaskState(
                    state="completed",
                    failure=None,
                    created_at="2023-01-01T00:00:00Z",
                    metadata={},
                )


@pytest.mark.parametrize("bad_result", [None, {"state": "completed"}, "completed", 42])
def test_get_task_rejects_non_task_state_result(bad_result: object) -> None:
    provider = DummyProvider(bad_get_result=bad_result, use_bad_get_result=True)

    with pytest.raises(
        ProviderError,
        match=r"_get_task\(\) must return a TaskState instance; got ",
    ):
        provider.get_task("valid-id")


@pytest.mark.parametrize("bad_request", [None, "text", 42, {"model_id": "m"}, True])
def test_create_task_rejects_non_task_request(bad_request: object) -> None:
    provider = DummyProvider()

    with pytest.raises(
        ProviderError,
        match=r"create_task\(\) requires a TaskRequest instance; got ",
    ):
        provider.create_task(bad_request)  # type: ignore[arg-type]

    assert provider.seen_request is None


@pytest.mark.parametrize("bad_result", [None, {"task_id": "123"}, "handle", 42])
def test_create_task_rejects_non_task_handle_result(bad_result: object) -> None:
    provider = DummyProvider(bad_create_result=bad_result, use_bad_create_result=True)

    with pytest.raises(
        ProviderError,
        match=r"_create_task\(\) must return a TaskHandle instance; got ",
    ):
        provider.create_task(TaskRequest(model_id="m", prompt="p", context=None, parameters={}, metadata=None))


def test_ai_provider_rejects_overridden_create_task() -> None:
    with pytest.raises(
        TypeError,
        match="AIProvider subclasses must implement _create_task\\(\\) instead of overriding create_task\\(\\)\\.",
    ):

        class InvalidProvider(AIProvider):
            @property
            def provider_name(self) -> str:
                return "InvalidProvider"

            def _discover_models(self) -> list[ModelRecord]:
                return []

            def create_task(self, request: TaskRequest) -> TaskHandle:  # type: ignore[misc]
                return TaskHandle(task_id="123", state=None, failure=None, metadata={})

            def _get_task(self, task_id: str) -> TaskState:
                return TaskState(
                    state="completed",
                    failure=None,
                    created_at="2023-01-01T00:00:00Z",
                    metadata={},
                )
