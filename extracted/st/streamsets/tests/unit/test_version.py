# Copyright 2019 StreamSets Inc.

# fmt: off
import pytest

from streamsets.sdk.exceptions import InvalidVersionError
from streamsets.sdk.utils import Version

# fmt: on


# Version Parameter: version string, tuple of expected parsed values
@pytest.mark.parametrize(
    'raw_string, expected',
    (
        # bare version numbers
        ['3.0.0.0', (None, [3, 0, 0, 0], None)],
        ['3.0.1', (None, [3, 0, 1, 0], None)],
        ['12.0', (None, [12, 0, 0, 0], None)],
        ['0.0.0', (None, [0, 0, 0, 0], None)],
        ['1.12.24', (None, [1, 12, 24, 0], None)],
        ['0.0.0.1', (None, [0, 0, 0, 1], None)],
        # from int/float
        [3.8, (None, [3, 8, 0, 0], None)],
        [3, (None, [3, 0, 0, 0], None)],
        # with version specifier
        ['3.0.1-SNAPSHOT', (None, [3, 0, 1, 0], 'SNAPSHOT')],
        ['3.8.2-RC2', (None, [3, 8, 2, 0], 'RC2')],
        ['3.8.2RC2', (None, [3, 8, 2, 0], 'RC2')],
        ['3.8.2SNAPSHOT', (None, [3, 8, 2, 0], 'SNAPSHOT')],
        ['3.8.2.42SNAPSHOT', (None, [3, 8, 2, 42], 'SNAPSHOT')],
        # with a name
        ['foo-3.0.1', ("foo", [3, 0, 1, 0], None)],
        ['foo3.0.1RC2', ("foo", [3, 0, 1, 0], "RC2")],
    ),
)
def test_version_parser(raw_string, expected):
    parsed_version = Version(raw_string)
    assert (parsed_version.name, parsed_version.version, parsed_version.specifier) == expected


@pytest.mark.parametrize(
    "initial, expected",
    (
        ["3.0", "<Version: None, 3.0.0.0, None>"],
        ["3.0.1RC2", "<Version: None, 3.0.1.0, 'RC2'>"],
        ["foo3.0.1RC2", "<Version: 'foo', 3.0.1.0, 'RC2'>"],
        ["foo-3.0.1-RC2", "<Version: 'foo', 3.0.1.0, 'RC2'>"],
        ["foo-3.0.1", "<Version: 'foo', 3.0.1.0, None>"],
        ["foo-3.0.1.4", "<Version: 'foo', 3.0.1.4, None>"],
    ),
)
def test_version_repr(initial, expected):
    assert repr(Version(initial)) == expected


@pytest.mark.parametrize(
    "initial, expected",
    (
        ["NotAVersion", InvalidVersionError],
        ["3.2.1.", InvalidVersionError],
        [None, InvalidVersionError],
        [[], InvalidVersionError],
    ),
)
def test_invalid_version(initial, expected):
    with pytest.raises(expected):
        Version(initial)


@pytest.mark.parametrize(
    "initial, expected",
    (
        ["3.0", "3.0.0.0"],
        ["3.0.1RC2", "3.0.1.0-RC2"],
        ["foo3.0.1RC2", "foo-3.0.1.0-RC2"],
        ["foo-3.0.1", "foo-3.0.1.0"],
        ["foo-3.0.1.4", "foo-3.0.1.4"],
    ),
)
def test_version_str(initial, expected):
    assert str(Version(initial)) == expected


@pytest.mark.parametrize(
    'lhs, rhs, expected',
    (
        # strict version ordering checks
        [Version('3.0.0.0'), Version('3.0'), True],
        [Version('3.0.1'), Version('3.0.1.0'), True],
        [Version('3.0.1.0'), Version('3.0.1.4'), False],
        [Version('3.1.0'), Version('3.0.1'), False],
        # ignore any release specifiers
        [Version('3.8.0-latest'), Version('3.8-SNAPSHOT'), True],
        [Version('3.8.0-latest'), Version('3.8'), True],
        # version-to-object comparisons
        [Version("3.1"), "3.1", True],
        [Version("3.1"), "3.2", False],
        [Version(5), 5, True],
        [Version(5), 6, False],
        [Version("3.1-RC4"), "3.1-snapshot2", True],
    ),
)
def test_version_object_equality(lhs, rhs, expected):
    assert (lhs == rhs) == expected


@pytest.mark.parametrize(
    'lhs, rhs, expected',
    (
        # strict version ordering checks
        [Version('3.0.0.0'), Version('3.0.0.1'), True],
        [Version('3.0.1'), Version('3.0.2.0'), True],
        [Version('3.0.0'), Version('12.0.1.0'), True],
        [Version('3.5.1'), Version('3.5.0'), False],
        # ignore any release specifiers
        [Version('3.8-latest'), Version('3.8.1-SNAPSHOT'), True],
        [Version('3.8-post3'), Version('3.8.1-alpha12'), True],
        # version-to-object comparisons
        [Version("3.1"), "3.1.4", True],
        [Version(5), 6, True],
        [Version("3.1-RC2"), "3.2-snapshot2", True],
        [Version("3.1-RC2"), "3.1-snapshot2", False],
    ),
)
def test_version_object_comparison(lhs, rhs, expected):
    assert (lhs < rhs) == expected
