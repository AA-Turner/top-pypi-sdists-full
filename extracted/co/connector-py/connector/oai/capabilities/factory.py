from collections.abc import Mapping, Sequence
from functools import partial
from typing import TYPE_CHECKING, Generic, TypeVar

from connector_sdk_types.oai.capability import Request
from connector_sdk_types.oai.modules.credentials_module_types import (
    AuthSetting,
    CredentialConfig,
    CredentialIdCombination,
    OAuthConfig,
)
from pydantic import BaseModel

from connector.oai.capability import CapabilityCallableProto, get_capability_annotations
from connector.oai.errors import ErrorMap, handle_exception
from connector.observability.instrument import Instrument

from .errors import CapabilityNotImplementedError
from .executor import CapabilityExecutor

if TYPE_CHECKING:
    from connector.oai.integration import CapabilityMetadata

REQUEST = TypeVar("REQUEST", bound=Request)
SETTINGS = TypeVar("SETTINGS", bound=BaseModel)


class CapabilityExecutorFactory(Generic[REQUEST, SETTINGS]):
    """A factory for building capability executors."""

    def __init__(
        self,
        *,
        app_id: str,
        capabilities: Mapping[str, CapabilityCallableProto[REQUEST]],
        capability_metadata: Mapping[str, "CapabilityMetadata"] | None = None,
        settings_model: type[SETTINGS],
        auth_setting: AuthSetting | None,
        credentials: Sequence[CredentialConfig | OAuthConfig],
        allowed_credentials: Sequence[CredentialIdCombination] | None = None,
        exception_handlers: ErrorMap,
    ) -> None:
        self._app_id = app_id
        self._capabilites = capabilities
        self._capability_metadata: Mapping[str, "CapabilityMetadata"] = capability_metadata or {}
        self._settings_model = settings_model
        self._auth_setting = auth_setting
        self._credentials_by_id = {cred.id: cred for cred in credentials}
        self._allowed_credentials = allowed_credentials
        self._exception_handlers = exception_handlers
        self._instrument = Instrument.integrations.connector.tags(
            app_id=app_id,
        )

        self._cached_executors: dict[str, CapabilityExecutor[REQUEST, SETTINGS]] = {}

    def create(self, name: str) -> CapabilityExecutor[REQUEST, SETTINGS]:
        """Attempts to create a capability executor for the provided capability name.

        Raises:
            CapabilityNotImplementedError: If the capability is not implemented.
        """
        capability_instrument = self._instrument.capability.tags(
            capability=name,
        )
        with capability_instrument.create.latency_ms.timer():
            return self._create(name, capability_instrument)

    def _create(
        self,
        name: str,
        capability_instrument: Instrument,
    ) -> CapabilityExecutor[REQUEST, SETTINGS]:
        """Creates a capability executor, if possible, and captures factory performance
        statistics.
        """

        # If we've already created this executor, return it.
        if executor := self._cached_executors.get(name):
            capability_instrument.cache.count.tags(result="hit").incr()
            return executor

        capability_instrument.cache.count.tags(result="miss").incr()

        capability = self._capabilites.get(name)
        if capability is None:
            capability_instrument.not_implemented.count.incr()
            raise CapabilityNotImplementedError(
                self._app_id,
                message=f"Capability '{name}' is not implemented.",
            )

        request_annotation, _ = get_capability_annotations(capability)

        # Creates an exception handler for this capability.
        exception_handle = partial(
            handle_exception,
            exception_classes=self._exception_handlers,
            capability=capability,
            app_id=self._app_id,
        )

        metadata = self._capability_metadata.get(name)
        executor = CapabilityExecutor(
            app_id=self._app_id,
            capability_name=name,
            capability=capability,
            credentials_by_id=self._credentials_by_id,
            allowed_credentials=self._allowed_credentials,
            settings_model=self._settings_model,
            auth_setting=self._auth_setting,
            exception_handle=exception_handle,
            request_validate_json=request_annotation.model_validate_json,
            instrument=capability_instrument.executor,
            capability_rate_limit_mode=metadata.rate_limit_mode if metadata else None,
        )

        # Cache the executor
        self._cached_executors[name] = executor
        capability_instrument.created.latency_ms.incr()

        return executor
