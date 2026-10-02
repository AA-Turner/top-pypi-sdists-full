"""DRIVER-mode set_geolocation verb — mock the device GPS fix.

Cloud sessions ride the LambdaTest "lambda-gps-location" hook — the exact call
the legacy V2 exported runtime makes (auteur models/appium_uiActions.py::
execute_gps_location). A local session falls back to Appium's
"mobile: setGeolocation" through the platform adapter registry; the ios row is
declared empty so that path raises loudly instead of degrading.
"""
import logging

from testmu_appium import _config
from testmu_appium._helpers import _adapters
from testmu_appium._vars import var

_log = logging.getLogger("testmu_appium")


def _android_set_geolocation(driver, latitude: float, longitude: float) -> None:
    driver.execute_script(
        "mobile: setGeolocation",
        {"latitude": latitude, "longitude": longitude, "altitude": 0},
    )


_adapters.register("geolocation", {
    "android": {"set": _android_set_geolocation},
    "ios": {},
})


def set_geolocation(driver, *, latitude, longitude, description: str = "") -> None:
    """Set the device's mocked GPS position.

    Args:
        driver: Live Appium webdriver session.
        latitude / longitude: Decimal degrees; may carry {{var}} templates.
        description: Optional human-readable label for the INFO log line.

    Raises:
        ValueError: a coordinate does not resolve to a number.
        UnsupportedOnPlatform: local run on iOS (empty adapter row).
    """
    try:
        lat = float(str(var(latitude)))
        lon = float(str(var(longitude)))
    except (TypeError, ValueError):
        raise ValueError(
            f"set_geolocation needs numeric coordinates; "
            f"got latitude={latitude!r} longitude={longitude!r}"
        ) from None

    suffix = f" — {description}" if description else ""
    if _config.run_target == "cloud":
        driver.execute_script(
            "lambda-gps-location", {"latitude": lat, "longitude": lon}
        )
    else:
        _adapters.adapter("geolocation", "set", "set_geolocation")(driver, lat, lon)
    _log.info("set_geolocation: %s,%s%s", lat, lon, suffix)
