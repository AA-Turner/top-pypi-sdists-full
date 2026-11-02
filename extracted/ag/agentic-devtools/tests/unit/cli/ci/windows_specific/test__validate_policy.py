"""Policy data must match the frozen seed exactly, including container shapes."""

import pytest

from agentic_devtools.cli.ci.windows_specific import EXPECTED_EXPANSIONS, EXPECTED_SELECTORS, _validate_policy


def test_python_policy():
    assert _validate_policy(EXPECTED_SELECTORS, EXPECTED_EXPANSIONS) == (
        EXPECTED_SELECTORS,
        tuple(EXPECTED_EXPANSIONS.items()),
    )


def test_json_arrays_are_normalized():
    policy = _validate_policy(
        list(EXPECTED_SELECTORS),
        {key: list(ids) for key, ids in EXPECTED_EXPANSIONS.items()},
        json_arrays=True,
    )
    assert policy == (EXPECTED_SELECTORS, tuple(EXPECTED_EXPANSIONS.items()))
    assert isinstance(policy.selectors, tuple)
    assert all(isinstance(ids, tuple) for _, ids in policy.expansions)


@pytest.mark.parametrize(
    "selectors",
    [
        None,
        "not a tuple",
        list(EXPECTED_SELECTORS),
        (),
        EXPECTED_SELECTORS[:-1],
        EXPECTED_SELECTORS[::-1],
        EXPECTED_SELECTORS + (EXPECTED_SELECTORS[0],),
        (EXPECTED_SELECTORS[0],) * 15,
        (None,) + EXPECTED_SELECTORS[1:],
        ("other",) + EXPECTED_SELECTORS[1:],
    ],
)
def test_invalid_selectors(selectors):
    with pytest.raises(ValueError):
        _validate_policy(selectors, EXPECTED_EXPANSIONS)


@pytest.mark.parametrize(
    "expansions",
    [
        None,
        [],
        {},
        dict(reversed(EXPECTED_EXPANSIONS.items())),
        {**EXPECTED_EXPANSIONS, "other": ()},
        {EXPECTED_SELECTORS[0]: EXPECTED_EXPANSIONS[EXPECTED_SELECTORS[0]]},
        {**EXPECTED_EXPANSIONS, EXPECTED_SELECTORS[0]: []},
        {**EXPECTED_EXPANSIONS, EXPECTED_SELECTORS[0]: "linux"},
        {**EXPECTED_EXPANSIONS, EXPECTED_SELECTORS[0]: ("win32", "linux")},
        {**EXPECTED_EXPANSIONS, EXPECTED_SELECTORS[0]: ("linux",)},
        {**EXPECTED_EXPANSIONS, EXPECTED_SELECTORS[0]: ("linux", "linux")},
        {
            **EXPECTED_EXPANSIONS,
            EXPECTED_SELECTORS[1]: ("R&D", "path with spaces", "O'Brien", "$cash", "`tick`", "(build)"),
        },
        {**EXPECTED_EXPANSIONS, EXPECTED_SELECTORS[1]: (None,) * 6},
    ],
)
def test_invalid_expansions(expansions):
    with pytest.raises(ValueError):
        _validate_policy(EXPECTED_SELECTORS, expansions)


def test_json_must_use_arrays():
    with pytest.raises(ValueError):
        _validate_policy(EXPECTED_SELECTORS, EXPECTED_EXPANSIONS, json_arrays=True)
    with pytest.raises(ValueError):
        _validate_policy(list(EXPECTED_SELECTORS), EXPECTED_EXPANSIONS, json_arrays=True)
