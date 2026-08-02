from pathlib import Path

import pytest

from seba_sqlite.sqlite_storage import _get_merit_values

_EXPECTED_MERIT_VALUES = [
    3054.234997314962,
    2256.6167197749464,
    1868.0214697526965,
    1471.8065224810757,
    510.06264381532543,
    260.7170745396887,
    149.2235529982198,
    142.59317366082274,
    141.81258696063966,
    137.08476080305778,
    132.64289518309434,
    132.14666340080663,
    129.7008972049017,
    129.05748465999798,
    128.59785798582016,
    128.4537006805766,
    126.63084841410672,
    14.623548799856016,
    6.412988849883518,
    2.7506196569290444,
    2.743501292940923,
    2.7265958029762998,
    2.7250152271657315,
    2.7243548636160897,
    0.48876899979305044,
    0.4605514423197748,
]


@pytest.mark.database
def test__get_merit_values() -> None:
    merit_values = _get_merit_values(
        Path(__file__).parent / "test_data" / "merit_value" / "merit.out",
    )
    assert [item["value"] for item in merit_values] == _EXPECTED_MERIT_VALUES

    merit_items = _get_merit_values(
        Path(__file__).parent / "test_data" / "merit_value" / "no_merit.out",
    )
    assert len(list(merit_items)) == 0


@pytest.mark.database
def test__get_merit_values_broken() -> None:
    merit_values = _get_merit_values(
        Path(__file__).parent / "test_data" / "merit_value" / "merit_broken.out",
    )
    assert [item["value"] for item in merit_values] == _EXPECTED_MERIT_VALUES
