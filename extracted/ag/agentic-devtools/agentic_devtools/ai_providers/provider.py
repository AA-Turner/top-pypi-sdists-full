from abc import ABC, abstractmethod
from typing import final

from .errors import ProviderError
from .models import ModelRecord, TaskHandle, TaskRequest, TaskState, _require_task_id_or_none


def _require_task_id(task_id: object) -> str:
    try:
        validated = _require_task_id_or_none("task_id", task_id)
    except ValueError as exc:
        raise ProviderError(str(exc), category="validation_error") from exc
    if validated is None:
        raise ProviderError(
            "task_id must be a non-empty string matching ^[A-Za-z0-9_-]+$",
            category="validation_error",
        )
    return validated


class ModelDiscovery(ABC):
    """
    ModelDiscovery is a provider-facing interface contract with an explicit
    discovery method and a normalized output type.
    """

    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        discover_owner = next((base for base in cls.__mro__ if "discover_models" in base.__dict__), None)
        if discover_owner is not None and discover_owner is not ModelDiscovery:
            raise TypeError(
                "ModelDiscovery subclasses must implement _discover_models() instead of overriding discover_models()."
            )

    @final
    def discover_models(self) -> list[ModelRecord]:
        """
        Returns a list of discovered models after validating the provider result.
        Raises ProviderError on provider-side failures or invalid result types.
        """
        result = self._discover_models()
        if not isinstance(result, list):
            raise ProviderError(
                f"_discover_models() must return a list; got {type(result).__name__!r}",
                category="logic_error",
            )
        for i, item in enumerate(result):
            if not isinstance(item, ModelRecord):
                raise ProviderError(
                    f"_discover_models() must return a list of ModelRecord instances; "
                    f"item at index {i} is {type(item).__name__!r}",
                    category="logic_error",
                )
        return result

    @abstractmethod
    def _discover_models(self) -> list[ModelRecord]:
        """
        Provider-specific model discovery implementation.
        Raises ProviderError on provider-side failures.
        """
        ...  # pragma: no cover


class AIProvider(ModelDiscovery):
    """
    AIProvider is the abstract base class and the single canonical boundary.
    """

    def __init_subclass__(cls, **kwargs: object) -> None:
        super().__init_subclass__(**kwargs)
        get_task_owner = next((base for base in cls.__mro__ if "get_task" in base.__dict__), None)
        if get_task_owner is not None and get_task_owner is not AIProvider:
            raise TypeError("AIProvider subclasses must implement _get_task() instead of overriding get_task().")
        create_task_owner = next((base for base in cls.__mro__ if "create_task" in base.__dict__), None)
        if create_task_owner is not None and create_task_owner is not AIProvider:
            raise TypeError("AIProvider subclasses must implement _create_task() instead of overriding create_task().")

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """
        The canonical name of the provider.
        """
        ...  # pragma: no cover

    @final
    def create_task(self, request: TaskRequest) -> TaskHandle:
        """
        Creates a task and returns a TaskHandle after validating the shared contract.
        Must not raise for validation or transport failures that are
        already represented in the returned payload.
        """
        if not isinstance(request, TaskRequest):
            raise ProviderError(
                f"create_task() requires a TaskRequest instance; got {type(request).__name__!r}",
                category="validation_error",
            )
        result = self._create_task(request)
        if not isinstance(result, TaskHandle):
            raise ProviderError(
                f"_create_task() must return a TaskHandle instance; got {type(result).__name__!r}",
                category="logic_error",
            )
        return result

    @abstractmethod
    def _create_task(self, request: TaskRequest) -> TaskHandle:
        """
        Provider-specific task creation for a validated TaskRequest.
        """
        ...  # pragma: no cover

    @final
    def get_task(self, task_id: str) -> TaskState:
        """
        Retrieves the task state by task_id after validating the shared contract.
        """
        result = self._get_task(_require_task_id(task_id))
        if not isinstance(result, TaskState):
            raise ProviderError(
                f"_get_task() must return a TaskState instance; got {type(result).__name__!r}",
                category="logic_error",
            )
        return result

    @abstractmethod
    def _get_task(self, task_id: str) -> TaskState:
        """
        Provider-specific task lookup for a validated task_id.
        """
        ...  # pragma: no cover
