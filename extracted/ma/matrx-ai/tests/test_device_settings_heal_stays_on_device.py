"""The settings self-heal never moves a device run, and never re-sends it after a device error.

``UnifiedAIClient``'s dispatch loop re-sends through ``_SettingsSelfHeal`` in two cases: a
setting rejection it can repair (``handle_failure``) and an empty 200 (``empty_answer_retry``).

* A device error is typed by ``providers/device/classify.py`` and attached; the heal reads it as
  is, so even a 400 ``device_invalid_request`` never becomes the safety net's ``invalid_setting``
  candidate → no resend (rename ``device_invalid_request`` to ``invalid_request`` and this is red).
* The one resend a device run CAN get (an empty answer, sent once more at the safe minimum)
  rewrites optional settings only: the model and ``served_via`` stay, and the loop re-dispatches
  with the SAME resolved device profile (``route_kind == "device"``).
"""

from __future__ import annotations

import pytest

from matrx_ai.config.served_via import ServedVia

DEVICE = "6f1c2a7e-3b9d-4c1e-8f0a-2d4b6c8e0a13"
MODEL_ID = "2c4e6a80-9b1d-4f3e-8a5c-7e9f1b3d5a70"
SV = {"provider": "device", "app_instance_id": DEVICE, "local_model_id": MODEL_ID}


def _heal():
    from matrx_ai.config import MessageList, UnifiedConfig
    from matrx_ai.providers.unified_client import _SettingsSelfHeal
    from matrx_ai.testing.profile_factory import make_profile

    profile = make_profile(
        model_name="qwen3.5-2b", wire_format="device_chat", vendor="device"
    ).model_copy(
        update={
            "route_kind": "device",
            "served_via": ServedVia.model_validate(SV),
            "model_id": MODEL_ID,
        }
    )
    config = UnifiedConfig(
        model=MODEL_ID, served_via=SV, temperature=0.4, top_p=0.9, messages=MessageList()
    )
    return _SettingsSelfHeal(provider="device", profile=profile, config=config), profile, config


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "error",
    [
        "DeviceInvalidRequestError",
        "DeviceStreamDroppedError",
        "ModelBusyError",
        "DeviceFailedError",
    ],
)
async def test_a_device_error_is_never_healed_and_resent(error) -> None:
    from matrx_ai.providers.device import errors
    from matrx_ai.providers.device.classify import make_device_error

    heal, _profile, config = _heal()
    exc = make_device_error(
        getattr(errors, error), "The model server refused the request: temperature"
    )
    assert await heal.handle_failure(exc, streamed_before=0) is False
    assert heal.repair is None and heal.safe_min is None
    assert config.served_via == ServedVia.model_validate(SV)


@pytest.mark.asyncio
async def test_the_empty_answer_resend_keeps_the_device_route() -> None:
    from matrx_ai.config import UnifiedResponse

    heal, profile, config = _heal()
    empty = UnifiedResponse(messages=[], usage=None)
    resent = await heal.empty_answer_retry(empty, streamed_before=None)
    # Whether or not it resends, nothing about WHERE it runs may change.
    assert config.model == MODEL_ID
    assert config.served_via == ServedVia.model_validate(SV)
    assert heal.profile is profile and profile.route_kind == "device"
    assert profile.wire_format == "device_chat"
    assert resent in (True, False)
