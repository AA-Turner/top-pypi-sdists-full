"""Target-policy support choices survive serialization and fail closed before submission."""

from __future__ import annotations

import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch
from concurrent.futures import Future

import pytest

from fireworks.training.sdk._core import TrainingClient
from fireworks.training.sdk.client import FiretitanTrainingClient, _CreateModelResponse
from fireworks.training.sdk._core.lib._pydantic_conv import to_pydantic_input
from fireworks.training.sdk.types.forward_backward_input import ForwardBackwardInput
from fireworks.training.sdk._core.lib.public_interfaces.api_future import AwaitableConcurrentFuture


@pytest.mark.parametrize("support_choice", ["full_vocabulary", "sampling_support", "candidates"])
def test_support_choice_mode_survives_wire_conversion(support_choice):
    config = {"target_logprob_support": support_choice, "clip_low_threshold": 0.2}
    body = to_pydantic_input(ForwardBackwardInput(data=[], loss_fn="ppo", loss_fn_config=config)).model_dump(
        mode="json"
    )
    assert body["loss_fn_config"] == config
    assert body["loss_fn_config"]["target_logprob_support"] == support_choice


@pytest.mark.parametrize("value", [None, False, True, 1, "true"])
@pytest.mark.parametrize(
    "field",
    [
        "supports_target_logprob_support",
        "supports_reinforce",
        "supports_score_centering",
        "supports_policy_importance_sampling",
        "supports_policy_diagnostics",
    ],
)
def test_only_explicit_boolean_capability_is_known(value, field: str) -> None:
    response = _CreateModelResponse(model_id="m", **{field: value})
    assert getattr(response, field) is (value if type(value) is bool else None)


@pytest.mark.parametrize(
    "reinforce,centering,config",
    [
        (None, True, None),
        (False, True, None),
        (True, None, {"score_centering": True}),
        (True, False, {"score_centering": True}),
    ],
)
@pytest.mark.parametrize("method", ["forward", "forward_backward"])
def test_unsupported_reinforce_fails_before_submission(reinforce, centering, config, method: str) -> None:
    client = FiretitanTrainingClient.__new__(FiretitanTrainingClient)
    TrainingClient.__init__(client, SimpleNamespace(), 0, "model-test")
    client.supports_reinforce = reinforce
    client.supports_score_centering = centering
    with pytest.raises(ValueError, match="Trainer does not advertise"):
        getattr(client, method)([], "reinforce", config)


@pytest.mark.parametrize("config", [None, {"score_centering": False}, {"score_centering": True, "weighting": "mis"}])
def test_reinforce_configuration_reaches_submission_unchanged(config) -> None:
    client = FiretitanTrainingClient.__new__(FiretitanTrainingClient)
    TrainingClient.__init__(client, SimpleNamespace(), 0, "model-test")
    client.supports_reinforce = True
    client.supports_score_centering = (config or {}).get("score_centering", False)
    with (
        patch.object(client, "_log_r3_request_error"),
        patch.object(client, "_can_run_firetitan_chunked_requests", return_value=False),
        patch.object(TrainingClient, "forward_backward", return_value="submitted") as submit,
    ):
        assert client.forward_backward([], "reinforce", config) == "submitted"
        submit.assert_called_once_with([], "reinforce", config)


@pytest.mark.parametrize("capability", [False, None])
def test_sampling_support_on_old_trainer_fails_before_submission(capability):
    client = FiretitanTrainingClient.__new__(FiretitanTrainingClient)
    TrainingClient.__init__(client, SimpleNamespace(), 0, "model-test")
    client.supports_target_logprob_support = capability
    with pytest.raises(ValueError, match="does not advertise target_logprob_support"):
        client.forward_backward([], "ppo", {"target_logprob_support": "sampling_support"})


@pytest.mark.parametrize(
    "config", [None, {"target_logprob_support": "full_vocabulary"}, {"target_logprob_support": "sampling_support"}]
)
def test_support_choice_selection_reaches_submission_unchanged(config):
    client = FiretitanTrainingClient.__new__(FiretitanTrainingClient)
    TrainingClient.__init__(client, SimpleNamespace(), 0, "model-test")
    client.supports_target_logprob_support = (config or {}).get("target_logprob_support") == "sampling_support"
    with (
        patch.object(client, "_log_r3_request_error"),
        patch.object(client, "_can_run_firetitan_chunked_requests", return_value=False),
        patch.object(TrainingClient, "forward_backward", return_value="submitted") as submit,
    ):
        assert client.forward_backward([], "ppo", config) == "submitted"
        submit.assert_called_once_with([], "ppo", config)


def test_candidates_support_reaches_submission_unchanged():
    client = FiretitanTrainingClient.__new__(FiretitanTrainingClient)
    TrainingClient.__init__(client, SimpleNamespace(), 0, "model-test")
    config = {"target_logprob_support": "candidates"}
    with (
        patch.object(client, "_log_r3_request_error"),
        patch.object(client, "_can_run_firetitan_chunked_requests", return_value=False),
        patch.object(TrainingClient, "forward_backward", return_value="submitted") as submit,
    ):
        client.forward_backward([], "cross_entropy", config)
        submit.assert_called_once_with([], "cross_entropy", config)


@pytest.mark.parametrize("value", [True, None, "top_tokens"])
@pytest.mark.parametrize("operation", ["forward", "forward_backward"])
def test_invalid_support_choice_is_rejected_before_submission(value, operation):
    client = FiretitanTrainingClient.__new__(FiretitanTrainingClient)
    TrainingClient.__init__(client, SimpleNamespace(), 0, "model-test")
    with pytest.raises(ValueError, match="target_logprob_support must be"):
        getattr(client, operation)([], "ppo", {"target_logprob_support": value})


@pytest.mark.parametrize(
    "key,value",
    [
        ("replay", False),
        ("replay", True),
        ("logprob_normalization", "sampling_support"),
        ("importance_sampling", {"target_policy": {"support": "behavior_policy"}}),
    ],
)
@pytest.mark.parametrize("operation", ["forward", "forward_backward"])
def test_old_support_keys_are_rejected_with_migration_hint(key, value, operation):
    client = FiretitanTrainingClient.__new__(FiretitanTrainingClient)
    TrainingClient.__init__(client, SimpleNamespace(), 0, "model-test")
    with pytest.raises(ValueError, match=f"{key} is unsupported; use loss_fn_config.target_logprob_support"):
        getattr(client, operation)([], "ppo", {key: value})


@pytest.mark.parametrize("capability", [False, True])
@pytest.mark.parametrize("support", ["sampling_support", "candidates"])
def test_non_vocabulary_support_forward_fails_before_submission(capability, support):
    client = FiretitanTrainingClient.__new__(FiretitanTrainingClient)
    TrainingClient.__init__(client, SimpleNamespace(), 0, "model-test")
    client.supports_target_logprob_support = capability
    with pytest.raises(ValueError, match=f"'{support}' requires forward_backward, not forward"):
        client.forward([], "cross_entropy", {"target_logprob_support": support})


@pytest.mark.parametrize("config", [None, {"target_logprob_support": "full_vocabulary"}])
def test_full_vocabulary_forward_reaches_submission_unchanged(config):
    client = FiretitanTrainingClient.__new__(FiretitanTrainingClient)
    TrainingClient.__init__(client, SimpleNamespace(), 0, "model-test")

    def complete(coro):
        pending = Future()
        pending.set_result(asyncio.run(coro))
        return AwaitableConcurrentFuture(pending)

    client.holder = SimpleNamespace(_client_config=None, run_coroutine_threadsafe=complete)

    async def submit(chunks, send, *, request_type):
        assert request_type == "Forward"
        future = asyncio.get_running_loop().create_future()
        future.set_result(await send(0, []))
        return future

    with (
        patch.object(client, "_log_r3_request_error"),
        patch.object(client, "_chunked_requests", return_value=[]),
        patch.object(client, "_run_chunked_requests", side_effect=submit),
        patch.object(client, "_send_single_forward_request", new_callable=AsyncMock, return_value="submitted") as send,
    ):
        assert client.forward([], "ppo", config).result() == "submitted"
        send.assert_awaited_once_with(0, [], "ppo", config)


@pytest.mark.parametrize("method", ["forward", "forward_backward"])
@pytest.mark.parametrize("capability", [None, False])
def test_server_policy_correction_requires_capability(method: str, capability: bool | None) -> None:
    client = FiretitanTrainingClient.__new__(FiretitanTrainingClient)
    TrainingClient.__init__(client, SimpleNamespace(), 0, "model-test")
    client.supports_policy_importance_sampling = capability
    with pytest.raises(ValueError, match="does not advertise server policy TIS/MIS"):
        getattr(client, method)([], "ppo", {"weighting": "mis", "anchor_logprob_source": "current_detached"})


@pytest.mark.parametrize("diagnostics", [False, True])
def test_supported_policy_correction_is_submitted_unchanged(diagnostics) -> None:
    client = FiretitanTrainingClient.__new__(FiretitanTrainingClient)
    TrainingClient.__init__(client, SimpleNamespace(), 0, "model-test")
    client.supports_policy_importance_sampling = True
    client.supports_policy_diagnostics = diagnostics
    config = {"weighting": "mis", "anchor_logprob_source": "current_detached", "weight_low": 0.2, "weight_high": 5.0}
    if diagnostics:
        config["report_policy_diagnostics"] = True
    with (
        patch.object(client, "_log_r3_request_error"),
        patch.object(client, "_can_run_firetitan_chunked_requests", return_value=False),
        patch.object(TrainingClient, "forward_backward", return_value="submitted") as submit,
    ):
        assert client.forward_backward([], "ppo", config) == "submitted"
        submit.assert_called_once_with([], "ppo", config)


@pytest.mark.parametrize("method", ["forward", "forward_backward"])
@pytest.mark.parametrize("capability", [None, False])
def test_policy_diagnostics_requires_capability(method, capability):
    client = FiretitanTrainingClient.__new__(FiretitanTrainingClient)
    TrainingClient.__init__(client, SimpleNamespace(), 0, "model-test")
    client.supports_policy_diagnostics = capability
    with pytest.raises(ValueError, match="does not advertise replay policy diagnostics"):
        getattr(client, method)([], "ppo", {"report_policy_diagnostics": True})
