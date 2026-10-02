"""get_vision_coordinates() — resolve a description to a point on the live screen.

The mobile twin of the playwright binding's helper of the same name. It is how a
recording GROUNDED BY VISION is re-grounded: a screen the accessibility tree
never described carries no selector to find, so the words the action was authored
with are the only durable handle it has.

There is deliberately no coordinate fallback. This helper is reached because the
other ways of locating the element are gone, and a recorded ratio describes a
layout that has already failed to produce it — replaying one would act
confidently in the wrong place.
"""
import logging
from contextlib import contextmanager
from contextvars import ContextVar

from testmu_appium import _config
from testmu_appium._helpers import _screen
from testmu_appium._errors import TestmuConfigError
from testmu_appium._helpers import _adapters
from testmu_appium._helpers._http import auth, headers, request_with_retry
from testmu_appium._helpers._perception import capture_perception

_log = logging.getLogger("testmu_appium")

_ENDPOINT = "/api/v1/vision/coordinates"

# Authoring already used vision to choose the point it is about to act on. The
# generated semantic call still has to be the code that runs and is recorded, so
# the host may seed that just-resolved point for this one execution. ContextVar
# keeps concurrent sessions isolated and asyncio.to_thread propagates its value
# into the binding worker. Standalone replay has no seed and reaches the service.
_authoring_points: ContextVar[dict[tuple[str, str], tuple[int, int]]] = ContextVar(
    "_authoring_vision_points", default={}
)


@contextmanager
def use_authoring_vision_points(points):
    """Temporarily provide live, non-recorded vision answers to generated code."""
    normalized = {
        (str(description), str(action_type)): (int(point[0]), int(point[1]))
        for (description, action_type), point in (points or {}).items()
    }
    token = _authoring_points.set(normalized)
    try:
        yield
    finally:
        _authoring_points.reset(token)


def _android_vision_window(driver) -> tuple[int, int]:
    size = _screen.window_size(driver)
    return size[0], size[1]


def _ios_vision_window(driver) -> tuple[int, int]:
    """The iOS basis is POINTS, which is what get_window_size reports.

    Deliberately the same call as Android's and a different unit. iOS taps in
    points, the parser publishes bounds in points, and the endpoint answers in
    whatever basis it is given — so asking in points and acting in points keeps
    one unit end to end. The screenshot's own pixel resolution is larger by the
    display scale and never enters this calculation.
    """
    size = _screen.window_size(driver)
    return size[0], size[1]


_adapters.register("screenshot_scaling", {
    "android": {"vision_window": _android_vision_window},
    "ios": {"vision_window": _ios_vision_window},
})


def _window(driver) -> tuple[int, int]:
    """The basis the answer comes back in — the platform row's declared window.

    The endpoint answers in the width and height it is GIVEN, not in the
    screenshot's own pixels, so the screenshot source's downscale (declared as
    per-source data on the ``screenshot_scaling`` registry) applies no
    correction here: ask in the row's basis, act in the same basis. The android
    row's basis is the device's own dimensions.
    """
    window = _adapters.adapter(
        "screenshot_scaling", "vision_window", "vision coordinate basis"
    )
    return window(driver)


def get_vision_coordinates(driver, description: str, action_type: str = "click"):
    """Where the element this description names is, right now.

    Args:
        driver: Live Appium driver — a fresh screenshot is captured from it.
        description: The element in words, as the action recorded it.
        action_type: What is about to be done there, for the model's context.

    Returns:
        ``(x, y)`` in device pixels.

    Raises:
        TestmuConfigError: smart is off. This is an AI-backed lookup with no
            local answer, so there is nothing to degrade to.
        RuntimeError: the endpoint failed, or reported the element not found.
    """
    seeded = _authoring_points.get().get((description, action_type))
    if seeded is not None:
        _log.info("    [vision_coordinates] using authoring point for %r", description[:60])
        return seeded

    if not _config.smart_enabled():
        raise TestmuConfigError(
            "get_vision_coordinates requires TESTMU_SMART=1 "
            "(AI-backed lookup, no local fallback)"
        )

    perception = capture_perception(
        driver, include_screenshot=True, require_screenshot=True
    )
    width, height = _window(driver)
    _log.info("    [vision_coordinates] query=%r", description[:60])

    host = _config.resolved("ai_api_host", _config._resolve_ai_api_host)
    url = f"{host}{_ENDPOINT}"
    body = {
        "screenshot_b64": perception.screenshot_b64,
        "action_instruction": description,
        "width": width,
        "height": height,
    }
    # The endpoint only has distinct handling for click/scroll; any other verb
    # (type, select, ...) needs a plain tap target, which is what the endpoint
    # extracts when the key is absent — sending the verb name would 422.
    if action_type in ("click", "scroll"):
        body["action_type"] = action_type
    response = request_with_retry(
        "POST", url, headers=headers(), auth=auth(), json_data=body,
    )
    if response.status_code != 200:
        raise RuntimeError(
            f"get_vision_coordinates: {_ENDPOINT} returned {response.status_code}: "
            f"{response.text[:500]}"
        )
    try:
        data = response.json()
    except ValueError as exc:
        raise RuntimeError(
            f"get_vision_coordinates: {_ENDPOINT} returned a non-JSON body: "
            f"{response.text[:500]}"
        ) from exc
    if not isinstance(data, dict) or not data.get("found"):
        raise RuntimeError(
            f"get_vision_coordinates: element not found for {description!r}"
        )
    point = (int(data["x"]), int(data["y"]))
    _log.info("    [vision_coordinates] found %s", point)
    return point
