from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest
from connector.oai.capabilities.errors import CapabilityNotImplementedError
from connector.oai.capabilities.factory import CapabilityExecutorFactory
from connector.oai.capability import CapabilityCallableProto
from connector_sdk_types.generated import StandardCapabilityName
from connector_sdk_types.oai.modules.credentials_module_types import EmptySettings


class TestCapabilityExecutorFactory:
    @pytest.fixture
    def mock_capability(self) -> MagicMock:
        return MagicMock()

    @pytest.fixture
    def mock_get_capability_annotations(self) -> Generator[MagicMock, None, None]:
        with patch("connector.oai.capabilities.factory.get_capability_annotations") as mock:
            yield mock

    @pytest.fixture
    def factory(
        self,
        mock_capability: CapabilityCallableProto,
    ) -> CapabilityExecutorFactory:
        return CapabilityExecutorFactory(
            app_id="FAKE_APP_ID",
            capabilities={
                StandardCapabilityName.APP_INFO: mock_capability,
            },
            auth_setting=None,
            settings_model=EmptySettings,
            credentials=[],
            exception_handlers=[],
        )

    def test_create_ok(
        self,
        mock_capability: MagicMock,
        mock_get_capability_annotations: MagicMock,
        factory: CapabilityExecutorFactory,
    ) -> None:
        mock_request_annotation = MagicMock()
        mock_get_capability_annotations.side_effect = ((mock_request_annotation, None),)
        # Should test that a capability is created, and test that the capability
        # is cached.
        executor = factory.create(StandardCapabilityName.APP_INFO)

        assert executor._app_id == factory._app_id
        assert executor._name == StandardCapabilityName.APP_INFO
        assert executor._capability == mock_capability
        assert executor._credentials_by_id == {}
        assert StandardCapabilityName.APP_INFO in factory._cached_executors
        assert executor._request_validate_json == mock_request_annotation.model_validate_json
        assert executor._instrument._stat_key == "integrations.connector.capability.executor"
        assert executor._instrument._tags == {
            "app_id": "FAKE_APP_ID",
            "capability": StandardCapabilityName.APP_INFO,
            "result": "miss",
        }

        factory.create(StandardCapabilityName.APP_INFO)

        # Asserts that we only built the executor once
        mock_get_capability_annotations.assert_called_once_with(
            mock_capability,
        )

    def test_create_cache_miss_not_implemented(
        self,
        factory: CapabilityExecutorFactory,
    ) -> None:
        # Should tests that a capability
        with pytest.raises(CapabilityNotImplementedError):
            factory.create("dne")
