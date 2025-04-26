
import pytest

from snowflake.core.alert import Alert, MinutesSchedule
from snowflake.core.schema import Schema
from tests.utils import random_string

from ...utils import ensure_snowflake_version


@pytest.fixture
def temp_alert(alerts, snowflake_version):
    ensure_snowflake_version(snowflake_version, "8.36.0")

    alert_name = random_string(10, 'test_alert_')
    alert_handle = alerts.create(Alert(
        name=alert_name,
        condition="SELECT 1",
        action="SELECT 2",
        schedule=MinutesSchedule(minutes=1),
        comment="ThIs iS a ComMeNT"
    ))

    try:
        yield alert_handle
    finally:
        alerts[alert_name].drop()


def test_clone(alerts, temp_alert):
    alert_name = random_string(10, 'test_alert_clone_')

    cloned_alert = alerts.create(alert_name,
        clone_alert=temp_alert.name
    )

    try:
        cloned_handle = cloned_alert.fetch()
        assert cloned_handle.name.upper() == alert_name.upper()
        assert cloned_handle.condition == "SELECT 1"
        assert cloned_handle.action == "SELECT 2"
        assert cloned_handle.schedule.minutes == 1
        assert cloned_handle.comment == "ThIs iS a ComMeNT"
    finally:
        alerts[alert_name].drop()

def test_clone_across_schema(temp_alert, temp_schema):
    alert_name = random_string(10, "test_clone_alert_across_schema_")

    created_handle = temp_schema.alerts.create(
        alert_name,
        clone_alert = f"{temp_alert.schema.name}.{temp_alert.name}"
    ).fetch()

    try:
        assert created_handle.database_name.upper() == temp_schema.database.name.upper()
        assert created_handle.schema_name.upper() == temp_schema.name.upper()
        assert created_handle.comment == "ThIs iS a ComMeNT"
        assert created_handle.name.upper() == alert_name.upper()
        assert created_handle.condition == "SELECT 1"
        assert created_handle.action == "SELECT 2"
        assert created_handle.schedule.minutes == 1
    finally:
        temp_schema.alerts[alert_name].drop()


def test_clone_across_database(temp_alert, temp_db):
    schema_name = random_string(10, "test_create_clone_across_database_schema_name_")
    created_schema = temp_db.schemas.create(
        Schema(name=schema_name)
    )
    alert_name = random_string(10, "test_alert_clone_across_database_")

    try:
        created_handle = created_schema.alerts.create(
            alert_name,
            clone_alert = f"{temp_alert.database.name}.{temp_alert.schema.name}.{temp_alert.name}"
        ).fetch()

        assert created_handle.database_name.upper() == created_schema.database.name.upper()
        assert created_handle.schema_name.upper() == created_schema.name.upper()
        assert created_handle.comment == "ThIs iS a ComMeNT"
        assert created_handle.name.upper() == alert_name.upper()
        assert created_handle.condition == "SELECT 1"
        assert created_handle.action == "SELECT 2"
        assert created_handle.schedule.minutes == 1
    finally:
        created_schema.drop()
