"""
VRC700 ventilation boost + fan-stage use the correct endpoints.

Verified live against the Vaillant cloud on a recoVAIR VAR 260/4 + VRC700:
- boost on/off:  POST/DELETE .../ventilation-boost  (same endpoint as TLI; it is
                 NOT blocked on VRC700, the previous ValueError was wrong)
- fan stage:     PATCH .../ventilation/{i}/{day,night}-fan-stage with
                 {"maximumFanStage": N}  (the /fan-stage endpoint with a ``type``
                 body returns 404 on VRC700)
"""

import pytest

from ..api import MyPyllantAPI
from ..enums import (
    VentilationFanStageType,
    VentilationOperationModeVRC700,
    ZoneCurrentSpecialFunction,
)
from ..models import Ventilation
from .utils import get_system_or_skip, load_test_data
from .generate_test_data import DATA_DIR


VRC700_TEST_DATA = load_test_data(DATA_DIR / "vrc700")


def _last_request(aio):
    method, url = list(aio.requests.keys())[-1]
    request = list(aio.requests.values())[-1][0]
    return method, str(url), request


def _make_vrc700_ventilation(system) -> Ventilation:
    # The VRC700 test data has no ventilation device, so build one from the system.
    return Ventilation(
        system_id=system.id,
        index=0,
        control_identifier=system.control_identifier,
        maximum_day_fan_stage=6,
        maximum_night_fan_stage=6,
        operation_mode_ventilation=VentilationOperationModeVRC700.AUTO,
        time_program_ventilation={},
    )


async def test_vrc700_set_ventilation_boost_uses_system_endpoint(
    mypyllant_aioresponses, mocked_api: MyPyllantAPI
) -> None:
    """set_ventilation_boost must work on VRC700 (no ValueError) and POST to the
    system-level ventilation-boost endpoint."""
    with mypyllant_aioresponses(VRC700_TEST_DATA) as aio:
        system = await get_system_or_skip(mocked_api)
        assert system.control_identifier.is_vrc700, "Expected a VRC700 system"

        await mocked_api.set_ventilation_boost(system)

        method, url, _ = _last_request(aio)
        assert method == "POST"
        assert url.endswith("/ventilation-boost"), url
        assert system.zones and all(
            z.current_special_function == ZoneCurrentSpecialFunction.VENTILATION_BOOST
            for z in system.zones
        )
        await mocked_api.aiohttp_session.close()


async def test_vrc700_cancel_ventilation_boost(
    mypyllant_aioresponses, mocked_api: MyPyllantAPI
) -> None:
    """cancel_ventilation_boost must work on VRC700 and DELETE the same endpoint."""
    with mypyllant_aioresponses(VRC700_TEST_DATA) as aio:
        system = await get_system_or_skip(mocked_api)

        await mocked_api.cancel_ventilation_boost(system)

        method, url, _ = _last_request(aio)
        assert method == "DELETE"
        assert url.endswith("/ventilation-boost"), url
        assert system.zones and all(
            z.current_special_function == ZoneCurrentSpecialFunction.NONE
            for z in system.zones
        )
        await mocked_api.aiohttp_session.close()


@pytest.mark.parametrize(
    "stage_type,segment,attr",
    [
        (VentilationFanStageType.DAY, "day-fan-stage", "maximum_day_fan_stage"),
        (VentilationFanStageType.NIGHT, "night-fan-stage", "maximum_night_fan_stage"),
    ],
)
async def test_vrc700_set_fan_stage_uses_day_night_endpoint(
    mypyllant_aioresponses, mocked_api: MyPyllantAPI, stage_type, segment, attr
) -> None:
    """On VRC700, set_ventilation_fan_stage must PATCH the day/night-specific URL
    with only ``maximumFanStage`` (no ``type`` field)."""
    with mypyllant_aioresponses(VRC700_TEST_DATA) as aio:
        system = await get_system_or_skip(mocked_api)
        ventilation = _make_vrc700_ventilation(system)

        await mocked_api.set_ventilation_fan_stage(ventilation, 3, stage_type)

        method, url, request = _last_request(aio)
        assert method == "PATCH"
        assert url.endswith(f"/ventilation/0/{segment}"), url
        assert request.kwargs["json"] == {"maximumFanStage": 3}
        assert getattr(ventilation, attr) == 3
        await mocked_api.aiohttp_session.close()
