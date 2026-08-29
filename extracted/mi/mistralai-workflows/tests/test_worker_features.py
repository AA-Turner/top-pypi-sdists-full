from typing import Annotated, Any

import httpx
import pytest
from pydantic_settings import BaseSettings, SettingsConfigDict

from mistralai.workflows.core.config import config_discovery
from mistralai.workflows.core.config.config import (
    GraphConfig,
    RemotelyOverridable,
    apply_remote_defaults,
    config,
)
from mistralai.workflows.core.config.config_discovery import WorkerRuntimeConfig, apply_worker_runtime_config
from mistralai.workflows.exceptions import WorkflowsException
from mistralai.workflows.protocol.v1.worker import WorkerFeatures
from mistralai.workflows.worker_client.models import WorkerInfo as GeneratedWorkerInfo

from .utils import create_http_test_worker_client

BASE_PAYLOAD: dict[str, Any] = {"scheduler_url": "https://temporal.example.com:7233", "namespace": "customer:workspace"}


def _runtime_config(**features: bool) -> WorkerRuntimeConfig:
    return WorkerRuntimeConfig(**BASE_PAYLOAD, features=WorkerFeatures(**features))


@pytest.fixture
def graph_config(monkeypatch: pytest.MonkeyPatch):
    """Install a GraphConfig resolved from the given `UPLOAD_GRAPH` value, restored after the test.

    `apply` reads `model_fields_set`, so the graph settings must be rebuilt from the environment the
    test declares rather than the one the process started with.
    """

    def _install(upload_graph_env: str | None = None) -> GraphConfig:
        if upload_graph_env is None:
            monkeypatch.delenv("UPLOAD_GRAPH", raising=False)
        else:
            monkeypatch.setenv("UPLOAD_GRAPH", upload_graph_env)
        graph = GraphConfig()
        monkeypatch.setattr(config.worker, "graph", graph)
        return graph

    return _install


@pytest.fixture
def whoami(monkeypatch: pytest.MonkeyPatch):
    """Serve a whoami payload over a mock transport, through the real worker client."""

    def _serve(**payload: Any) -> None:
        transport = httpx.MockTransport(lambda _request: httpx.Response(200, json=payload))
        client = create_http_test_worker_client(transport)
        monkeypatch.setattr(config_discovery, "get_worker_client", lambda **kwargs: client)

    return _serve


class TestFeaturePrecedence:
    def test_unset_adopts_the_server_value(self, graph_config) -> None:
        graph = graph_config()

        effective = _runtime_config(upload_graph=True).apply()

        assert graph.upload_graph is True
        assert effective == {"upload_graph": True}

    @pytest.mark.parametrize(
        ("env_value", "expected"),
        [("false", False), ("true", True), ("0", False), ("1", True)],
    )
    def test_explicit_local_value_wins_over_the_server(self, graph_config, env_value: str, expected: bool) -> None:
        graph = graph_config(env_value)

        effective = _runtime_config(upload_graph=not expected).apply()

        assert graph.upload_graph is expected
        assert effective == {"upload_graph": expected}

    def test_server_silence_leaves_an_unset_value_at_the_sdk_default(self, graph_config) -> None:
        graph = graph_config()

        _runtime_config().apply()

        assert graph.upload_graph is False
        assert "upload_graph" not in graph.model_fields_set


class _DefaultOnConfig(BaseSettings):
    """Stands in for a flag whose SDK default has graduated to on, which no real flag has yet."""

    flag: Annotated[bool, RemotelyOverridable()] = True

    model_config = SettingsConfigDict(env_prefix="TEST_REMOTE_DEFAULT_")


class TestServerSilence:
    """Silence must stay distinguishable from an explicit `False`.

    Once a flag's SDK default is on, a server that predates the change would otherwise keep sending
    its own stale `False` and silently turn the flag back off.
    """

    def test_silence_leaves_a_default_on_flag_on(self) -> None:
        settings = _DefaultOnConfig()

        assert apply_remote_defaults(settings, {"flag": None}) == {"flag": True}
        assert settings.flag is True

    def test_explicit_false_turns_a_default_on_flag_off(self) -> None:
        settings = _DefaultOnConfig()

        assert apply_remote_defaults(settings, {"flag": False}) == {"flag": False}
        assert settings.flag is False


class TestFeatureFlagWiring:
    """A flag reaches worker configuration through a `RemotelyOverridable` field, or not at all."""

    def test_every_feature_flag_has_a_marked_settings_field(self, graph_config) -> None:
        graph_config()

        effective = _runtime_config().apply()

        assert set(effective) == set(WorkerFeatures.model_fields)

    def test_flag_without_a_marked_settings_field_is_rejected(self) -> None:
        with pytest.raises(WorkflowsException):
            apply_remote_defaults(config, {"not_a_settings_field": True})


class TestGeneratedClientTolerance:
    """The generated client must ignore what it does not declare, not reject it.

    This is what makes a worker running an SDK older than a flag degrade to its compiled-in default
    instead of failing at startup. The generated `model_config` never states `extra`, so the
    property rests on the pydantic default — a regeneration could silently take it away.
    """

    def test_unknown_top_level_field_is_dropped(self) -> None:
        info = GeneratedWorkerInfo.model_validate({**BASE_PAYLOAD, "some_future_block": {"enabled": True}})

        assert "some_future_block" not in info.model_dump(mode="json")

    def test_unknown_feature_field_is_dropped_without_losing_known_ones(self) -> None:
        info = GeneratedWorkerInfo.model_validate(
            {**BASE_PAYLOAD, "features": {"upload_graph": True, "some_future_flag": True}}
        )

        assert info.model_dump(mode="json")["features"] == {"upload_graph": True}


class TestConfigDiscoveryVersionSkew:
    """End to end from the wire payload, across every seam the response actually crosses.

    A whoami response is validated into the generated model, translated into the protocol model via
    `model_dump(mode="json")`, re-validated into `WorkerRuntimeConfig`, and applied. Each of those
    steps can drop a field, so version skew is only meaningfully tested through the whole chain.
    """

    async def test_server_value_reaches_worker_configuration(self, graph_config, whoami) -> None:
        graph = graph_config()
        whoami(**BASE_PAYLOAD, tls=True, features={"upload_graph": True})

        runtime_config = await apply_worker_runtime_config()

        assert runtime_config is not None
        assert runtime_config.features.upload_graph is True
        assert graph.upload_graph is True
        assert config.temporal.namespace == "customer:workspace"

    async def test_api_older_than_the_flag_leaves_the_default(self, graph_config, whoami) -> None:
        graph = graph_config()
        whoami(**BASE_PAYLOAD)

        runtime_config = await apply_worker_runtime_config()

        assert runtime_config is not None
        assert runtime_config.features == WorkerFeatures()
        assert graph.upload_graph is False

    async def test_api_newer_than_the_sdk_keeps_current_behaviour(self, graph_config, whoami) -> None:
        graph = graph_config()
        whoami(**BASE_PAYLOAD, features={"some_future_flag": True}, some_future_block={"enabled": True})

        runtime_config = await apply_worker_runtime_config()

        assert runtime_config is not None
        assert graph.upload_graph is False

    async def test_explicit_local_value_survives_the_full_path(self, graph_config, whoami) -> None:
        graph = graph_config("false")
        whoami(**BASE_PAYLOAD, features={"upload_graph": True})

        await apply_worker_runtime_config()

        assert graph.upload_graph is False
