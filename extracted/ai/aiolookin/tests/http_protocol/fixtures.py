from __future__ import annotations

from typing import Any

import pytest

from aiolookin.protocol import LookInHttpProtocol


@pytest.fixture
def lookin_http_protocol():
    def wrapper(test_client):
        return LookInHttpProtocol(
            session=test_client.session,
            api_uri=str(test_client.make_url("")),
        )

    return wrapper


@pytest.fixture
def get_info_response() -> dict[str, str]:
    return {
        "Type": "Remote",
        "MRDC": "02000105001K17E3",
        "Status": "Running",
        "ID": "98F33011",
        "Name": "living_room",
        "Time": "1634495587",
        "Timezone": "+3",
        "PowerMode": "5v",
        "CurrentVoltage": "5889",
        "Firmware": "2.38",
        "Temperature": "57",
        "HomeKit": "1",
        "EcoMode": "off",
        "SensorMode": "0",
    }


@pytest.fixture
def get_meteo_sensor_response() -> dict[str, str]:
    return {
        "Humidity": "38.6",
        "Pressure": "99649.6",
        "Temperature": "24.6",
        "Updated": "1634499757",
    }


@pytest.fixture
def get_devices_response() -> list[dict[str, str]]:
    return [
        {"Type": "01", "UUID": "49C2", "Updated": "1630089608"},
        {"Type": "03", "UUID": "703A", "Updated": "1631862703"},
        {"Type": "06", "UUID": "AE74", "Updated": "1632039732"},
        {"Type": "07", "UUID": "1234", "Updated": "1632129287"},
        {"Type": "04", "UUID": "1235", "Updated": "1632129287"},
        {"Type": "05", "UUID": "1236", "Updated": "1632129287"},
        {"Type": "EF", "UUID": "460E", "Updated": "1634283385"},
    ]


@pytest.fixture
def get_device_response() -> dict[str, Any]:
    return {
        "Type": "07",
        "Name": "Fan",
        "Updated": "1632129287",
        "Status": "1000",
        "Functions": [
            {"Name": "power", "Type": "single"},
            {"Name": "speed", "Type": "single"},
            {"Name": "swing", "Type": "single"},
        ],
    }


@pytest.fixture
def get_conditioner_response() -> dict[str, Any]:
    return {
        "Type": "EF",
        "Name": "Зал",
        "Updated": "1634283385",
        "Extra": "0001",
        "Status": "3701",
        "LastStatus": "1100",
        "Functions": [],
    }


@pytest.fixture
def get_media_sources() -> dict[str, Any]:
    return {
        "Type": "toggle",
        "Signals": [
            {"Operand": "20DFF00F", "Protocol": "01"},
            {"Operand": "20DF5AA5", "Protocol": "01"},
            {"Operand": "20DF639C", "Protocol": "01"},
        ],
    }


@pytest.fixture
def get_no_media_sources() -> dict[str, str | list[Any]]:
    return {"Type": "toggle", "Signals": []}


@pytest.fixture
def item_not_exist_error() -> dict[str, str]:
    return {
        "success": "false",
        "Message": "Item didn't exists",
    }
