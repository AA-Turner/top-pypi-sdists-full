import time

from contextlib import suppress

import pytest

from snowflake.core.alert import Alert, MinutesSchedule
from snowflake.core.exceptions import NotFoundError
from snowflake.core.table import Table, TableColumn
from tests.utils import random_string


@pytest.mark.min_sf_ver("8.36.0")
def test_execute(alerts, tables):
    alert_name = random_string(10, 'test_alert_')
    temp_table = tables.create(Table(
            name=random_string(10, 'test_table_'),
            columns=[
                TableColumn(name="c1", datatype="varchar"),
                TableColumn(name="c2", datatype="varchar"),
            ],
        )
    )

    alert_handle = alerts.create(Alert(
        name=alert_name,
        condition="SELECT 1",
        action=f"DROP TABLE {temp_table.name}",
        schedule=MinutesSchedule(minutes=1),
        comment="ThIs iS a ComMeNT"
    ))

    try:
        temp_table.fetch()

        alert_handle.execute()

        # Wait for the alert to execute
        time.sleep(61)

        with pytest.raises(
            NotFoundError
        ):
            temp_table.fetch()
    finally:
        with suppress(NotFoundError):
            temp_table.drop()
        alert_handle.drop()
