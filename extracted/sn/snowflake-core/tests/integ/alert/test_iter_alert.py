from contextlib import suppress

import pytest

from snowflake.core.alert import Alert, MinutesSchedule
from snowflake.core.exceptions import NotFoundError
from tests.utils import random_string

from ...utils import ensure_snowflake_version


@pytest.fixture(scope="module")
def alerts_extended(alerts, snowflake_version):
    ensure_snowflake_version(snowflake_version, "8.36.0")

    name_list = []
    for _ in range(5):
        name_list.append(random_string(10, 'test_alert_iter_a_'))
    for _ in range(7):
        name_list.append(random_string(10, 'test_alert_iter_b_'))
    for _ in range(3):
        name_list.append(random_string(10, 'test_alert_iter_c_'))

    for alert_name in name_list:
        alerts.create(Alert(
            name=alert_name,
            condition="SELECT 1",
            action="SELECT 2",
            schedule=MinutesSchedule(minutes=1),
            comment="ThIs iS a ComMeNT"
        ))

    try:
        yield alerts
    finally:
        for alert_name in name_list:
            with suppress(NotFoundError):
                alerts[alert_name].drop()

def test_iter_raw(alerts_extended):
    assert len(list(alerts_extended.iter())) >= 15


def test_iter_like(alerts_extended):
    assert len(list(alerts_extended.iter(like="test_alert_iter_"))) == 0
    assert len(list(alerts_extended.iter(like="test_alert_iter_a_%%"))) == 5
    assert len(list(alerts_extended.iter(like="test_alert_iter_b_%%"))) == 7
    assert len(list(alerts_extended.iter(like="test_alert_iter_c_%%"))) == 3


def test_iter_show_limit(alerts_extended):
    assert len(list(alerts_extended.iter(like="test_alert_iter_a_%%"))) == 5
    assert len(list(alerts_extended.iter(like="test_alert_iter_a_%%", show_limit=2))) == 2
    assert len(list(alerts_extended.iter(show_limit=2))) == 2


def test_iter_starts_with(alerts_extended):
    assert len(list(alerts_extended.iter(starts_with="test_alert_iter_a_".upper()))) == 5


def test_iter_from_name(alerts_extended):
    assert len(list(alerts_extended.iter(from_name='test_alert_iter_b_'))) >= 10
