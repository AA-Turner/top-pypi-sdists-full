import pytest

from snowflake.core.alert import Alert, MinutesSchedule
from snowflake.core.exceptions import NotFoundError
from tests.utils import random_string


@pytest.mark.min_sf_ver("8.36.0")
def test_drop(alerts):
    alert_name = random_string(10, 'test_alert_')

    alert_handle = alerts.create(Alert(
        name=alert_name,
        condition="SELECT 1",
        action="SELECT 2",
        schedule=MinutesSchedule(minutes=1),
        comment="ThIs iS a ComMeNT"
    ))


    alert_handle.drop()

    with pytest.raises(
        NotFoundError
    ):
        alert_handle.drop()

    alert_handle.drop(if_exists=True)
