"""Define a functions for modifying incoming data."""

from datetime import datetime, timedelta
from typing import Any, Optional, Union
from zoneinfo import ZoneInfo

from .exceptions import BlueCurrentException, RequestLimitReached, WebsocketError

TZ = ZoneInfo("Europe/Amsterdam")

ERRORS: dict[int, BlueCurrentException] = {
    0: WebsocketError("Unknown command"),
    1: WebsocketError("Invalid Auth Token"),
    2: WebsocketError("Not authorized"),
    9: WebsocketError("Unknown error"),
    42: RequestLimitReached("Request limit reached"),
}

SMART_CHARGING: set[str] = set()


def calculate_average_usage_from_phases(phases: list[float | None]) -> float:
    """Get the average of the phases that are not 0."""
    used_phases = [p for p in phases if p]
    if len(used_phases):
        return round(sum(used_phases) / len(used_phases), 1)
    return 0


def join_numbers_with_commas(numbers: list[int]) -> str:
    """Convert a list of numbers to a string with commas."""
    return "[" + ",".join(str(num) for num in numbers) + "]"


def calculate_total_kw(c_avg: float, v_avg: float) -> float:
    """Calculate the total kW."""
    return round((c_avg * v_avg * 1.732 / 1000), 2)


def create_datetime(timestamp: str) -> Optional[datetime]:
    """Get a datetime object from an timestamp."""

    if timestamp == "":
        return None

    if "+" in timestamp:
        return datetime.strptime(timestamp, "%Y%m%d %H:%M:%S%z")

    time = datetime.strptime(timestamp, "%Y%m%d %H:%M:%S")
    time = time.replace(tzinfo=TZ)
    return time


def get_vehicle_status(vehicle_status_key: str) -> str:
    """Get the vehicle status."""
    statuses = {
        "A": "standby",
        "B": "vehicle_detected",
        "C": "ready",
        "D": "ready",
        "E": "no_power",
        "F": "vehicle_error",
    }

    return statuses[vehicle_status_key]


def get_exception(message: dict[str, Any]) -> BlueCurrentException:
    """Return a defined error message or one from the server"""
    error = message["error"]
    message = message["message"]

    if error in ERRORS:
        return ERRORS[error]
    return WebsocketError(message)


def set_smart_charging(evse_id: str, smart_charging: bool) -> None:
    """Add or discard evse_id in SMART_CHARGING"""
    if smart_charging:
        SMART_CHARGING.add(evse_id)
    else:
        SMART_CHARGING.discard(evse_id)


def handle_charge_points(message: dict[str, Any]) -> None:
    """Store the evse_id if it has smart charging enabled"""
    for charge_point in message["data"]:
        set_smart_charging(charge_point["evse_id"], charge_point["smart_charging"])


def set_current_left(message: dict[str, Any], c_avg: float) -> None:
    """Set current_left"""
    max_usage = message["data"]["max_usage"]
    smart_charging_max_usage = message["data"]["smartcharging_max_usage"]

    if message["evse_id"] in SMART_CHARGING:
        message["data"]["current_left"] = smart_charging_max_usage - c_avg
    else:
        message["data"]["current_left"] = max_usage - c_avg


def handle_status(message: dict[str, Any]) -> None:
    """Transform status values and add others."""
    voltage1: float = message["data"]["actual_v1"]
    voltage2: float = message["data"]["actual_v2"]
    voltage3: float = message["data"]["actual_v3"]

    v_avg = calculate_average_usage_from_phases([voltage1, voltage2, voltage3])
    message["data"]["avg_voltage"] = v_avg

    current1: float = message["data"]["actual_p1"]
    current2: float = message["data"]["actual_p2"]
    current3: float = message["data"]["actual_p3"]

    c_avg = calculate_average_usage_from_phases([current1, current2, current3])
    message["data"]["avg_current"] = c_avg

    set_current_left(message, c_avg)

    message["data"]["total_kw"] = calculate_total_kw(c_avg, v_avg)

    vehicle_status_key = message["data"]["vehicle_status"]
    message["data"]["vehicle_status"] = get_vehicle_status(vehicle_status_key)

    start_datetime = message["data"]["start_datetime"]
    new_start_datetime = create_datetime(start_datetime)

    stop_datetime = message["data"]["stop_datetime"]
    new_stop_datetime = create_datetime(stop_datetime)

    message["data"]["start_datetime"] = new_start_datetime
    message["data"]["stop_datetime"] = new_stop_datetime

    offline_since = message["data"]["offline_since"]
    message["data"]["offline_since"] = create_datetime(offline_since)


def handle_settings(message: dict[str, Any]) -> None:
    """Transform settings object"""

    message["data"]["plug_and_charge"] = message["data"]["plug_and_charge"]["value"]
    message["data"]["linked_charge_cards_only"] = not message["data"][
        "public_charging"
    ]["value"]

    set_smart_charging(message["data"]["evse_id"], message["data"]["smart_charging"])


def handle_grid(message: dict[str, Any]) -> None:
    """Add grid total and avg to a message."""
    if "CURRENT" in message["object"]:
        message["data"] = {}
        message["data"]["grid_actual_p1"] = message.pop("grid_actual_p1")
        message["data"]["grid_actual_p2"] = message.pop("grid_actual_p2")
        message["data"]["grid_actual_p3"] = message.pop("grid_actual_p3")

    current1: float = message["data"]["grid_actual_p1"]
    current2: float = message["data"]["grid_actual_p2"]
    current3: float = message["data"]["grid_actual_p3"]

    c_avg = calculate_average_usage_from_phases([current1, current2, current3])
    message["data"]["grid_avg_current"] = c_avg
    c_max = max(current1, current2, current3)
    message["data"]["grid_max_current"] = c_max


def handle_setting_change(message: dict[str, Any]) -> None:
    """Change result to a boolean."""
    message["result"] = "true" in message["result"]["setting"]

    if message["object"] == "STATUS_SET_PUBLIC_CHARGING":
        message["object"] = "LINKED_CHARGE_CARDS_ONLY"
        message["result"] = not message["result"]
    else:
        message["object"] = message["object"].replace("STATUS_SET_", "")


def handle_session_messages(message: dict[str, Any]) -> None:
    """handle session messages."""

    object_name = message["object"].replace("STATUS_", "").replace("RECEIVED_", "")

    if "STATUS" in message["object"] and message["error"]:
        name = object_name.lower()
        error = message["error"].lower()
        evse_id = message["evse_id"]
        message["error"] = f"{name} {error} for chargepoint: {evse_id}"
    message["object"] = object_name


def get_dummy_message(evse_id: str) -> dict[str, Union[str, dict[str, Any]]]:
    """Return a CH_STATUS message with the current time as start_datetime"""
    return {
        "object": "CH_STATUS",
        "data": {
            "start_datetime": datetime.now(TZ),
            "evse_id": evse_id,
        },
    }


def get_next_reset_delta() -> timedelta:
    """Returns the timedelta to the next midnight"""
    now = datetime.now(TZ)
    return now.replace(hour=0, minute=0, second=30) + timedelta(days=1) - now
