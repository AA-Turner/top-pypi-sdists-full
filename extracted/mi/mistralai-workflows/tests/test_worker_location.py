import pytest

from mistralai.workflows.core.config.config import DeploymentLocationConfig
from mistralai.workflows.protocol.v1.workflow import LocationType


class TestDeploymentLocationAutoDetection:
    def test_detects_k8s_from_service_host(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("KUBERNETES_SERVICE_HOST", "10.0.0.1")
        monkeypatch.delenv("DEPLOYMENT_LOCATION_LOCATION_TYPE", raising=False)
        monkeypatch.delenv("DEPLOYMENT_LOCATION_K8S_CLUSTER", raising=False)
        monkeypatch.delenv("DEPLOYMENT_LOCATION_K8S_NAMESPACE", raising=False)

        cfg = DeploymentLocationConfig()
        assert cfg.location_type == LocationType.k8s

    def test_explicit_override_beats_auto_detection(self, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("KUBERNETES_SERVICE_HOST", "10.0.0.1")
        monkeypatch.setenv("DEPLOYMENT_LOCATION_LOCATION_TYPE", "local")
        monkeypatch.delenv("DEPLOYMENT_LOCATION_K8S_CLUSTER", raising=False)
        monkeypatch.delenv("DEPLOYMENT_LOCATION_K8S_NAMESPACE", raising=False)

        cfg = DeploymentLocationConfig()
        assert cfg.location_type == LocationType.local
