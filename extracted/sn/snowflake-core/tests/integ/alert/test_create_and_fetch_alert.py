
from contextlib import suppress

import pytest

from snowflake.core._common import CreateMode
from snowflake.core.alert import Alert, MinutesSchedule
from snowflake.core.exceptions import ConflictError, NotFoundError
from tests.utils import random_string


@pytest.mark.min_sf_ver("8.36.0")
def test_create_and_fetch(alerts):
    alert_name = random_string(10, 'test_alert_')

    try:
        alert = alerts.create(
            Alert(
                name=alert_name,
                condition="SELECT 1",
                action="SELECT 2",
                schedule=MinutesSchedule(minutes=1),
                comment="asdf"
            )
        )

        alert_handle = alert.fetch()

        assert alert_handle.name.upper() == alert_name.upper()
        assert alert_handle.condition == "SELECT 1"
        assert alert_handle.action == "SELECT 2"
        assert alert_handle.schedule.minutes == 1
        assert alert_handle.comment == "asdf"
    finally:
        with suppress(NotFoundError):
            alerts[alert_name].drop()


@pytest.mark.min_sf_ver("8.36.0")
def test_create_and_update(alerts):
    alert_name = random_string(10, 'test_alert_')

    try:
        alerts.create(
            Alert(
                name=alert_name,
                condition="SELECT 1",
                action="SELECT 2",
                schedule=MinutesSchedule(minutes=1),
                comment="asdf"
            )
        )

        with pytest.raises(ConflictError):
            alerts.create(
                Alert(
                    name=alert_name,
                    condition="SELECT 1",
                    action="SELECT 2",
                    schedule=MinutesSchedule(minutes=1),
                    comment="asdf"
                )
            )

        alerts.create(
            Alert(
                name=alert_name,
                condition="SELECT 5",
                action="SELECT 6",
                schedule=MinutesSchedule(minutes=7),
                comment="fdsa"
            ),
            mode=CreateMode.or_replace
        )

        alert_handle = alerts[alert_name].fetch()

        assert alert_handle.name.upper() == alert_name.upper()
        assert alert_handle.condition == "SELECT 5"
        assert alert_handle.action == "SELECT 6"
        assert alert_handle.schedule.minutes == 7
        assert alert_handle.comment == "fdsa"
    finally:
        with suppress(NotFoundError):
            alerts[alert_name].drop()
