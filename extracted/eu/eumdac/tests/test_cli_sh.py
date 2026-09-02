import os
import unittest
from io import StringIO
from itertools import islice
from pathlib import Path
from shutil import rmtree
from unittest.mock import mock_open, patch

import pytest

from eumdac.cli import cli

from .base import INTEGRATION_TESTING


@pytest.fixture
@unittest.skipIf(INTEGRATION_TESTING, "Covered by integration testing")
def temp_output_dir(request):
    output_dir_name = f"output_dir_{request.node.name}"
    yield Path(output_dir_name)
    rmtree(output_dir_name)


@pytest.fixture
@unittest.skipIf(INTEGRATION_TESTING, "Covered by integration testing")
def temp_config_dir(request):
    config_dir_name = Path(f"config_dir_{request.node.name}")
    os.environ["EUMDAC_CONFIG_DIR"] = str(config_dir_name)
    config_dir_name.mkdir(exist_ok=True)
    yield config_dir_name
    rmtree(config_dir_name)
    del os.environ["EUMDAC_CONFIG_DIR"]


@pytest.fixture
@unittest.skipIf(INTEGRATION_TESTING, "Covered by integration testing")
def temp_credentials(temp_config_dir):
    credentials_path = temp_config_dir / "credentials"
    with credentials_path.open("w") as fobj:
        fobj.write("user,password")
    yield credentials_path


def eumdac(args):
    test_out = StringIO()
    test_err = StringIO()

    with patch("sys.stdout", test_out), patch("sys.stderr", test_err), patch(
        "eumdac.cli.sys.stdin", new_callable=mock_open()
    ) as mock_stdin:
        mock_stdin.isatty.return_value = False
        try:
            cli(args)
        except SystemExit as exc:
            if exc.code != 0:
                raise exc

    return test_out.getvalue(), test_err.getvalue()


def assert_eumdac_output(args, expected_lines):
    out, err = eumdac(args)
    print(out)
    expected_block = "\n".join(str(x) for x in expected_lines)
    error_msg = "\n{}\nvs\n{}".format(expected_block, out)
    assert_list_contains(out.splitlines(), expected_lines, error_msg)
    assert not err, "stderr not empty!\n" "Contents:\n" f"{err}"


def assert_list_contains(outlist, expectedlist, msg=None):
    iout = iter(outlist)
    iexpected = iter(expectedlist)
    for exp in iexpected:
        print(exp)
        if isinstance(exp, tuple) and exp[0] == "order_does_not_matter":
            inner_expectation = sorted(exp[1])
            out_slice = sorted(islice(iout, len(exp[1])))
            print(inner_expectation)
            print(out_slice)
            assert_list_contains(out_slice, inner_expectation)
        else:
            out = next(iout)
            if msg:
                assert exp in out, msg
            else:
                assert exp in out


def test_assert_list_contains():
    assert_list_contains(["A1", "A2", "A3", "B1"], ["A", "A", "A", "B"])


def test_assert_list_contains_simple_assertion_error():
    with pytest.raises(AssertionError):
        assert_list_contains(["A1", "A2", "A3", "B1"], ["A", "B", "A", "B"])


def test_assert_list_contains_assertion_error_unequal_len():
    with pytest.raises(AssertionError):
        assert_list_contains(["A1", "A2", "A3"], ["A", "B", "A", "B"])


def test_assert_list_contains_with_indifferent_order():
    assert_list_contains(
        ["A1", "A2", "A3", "B1"], ["A", ("order_does_not_matter", ["B", "A", "A"])]
    )


@unittest.skipIf(INTEGRATION_TESTING, "Covered by unit testing")
def test_set_credentials(temp_config_dir):
    args = "--set-credentials user password".split()
    expected = (
        "Credentials are correct. Token was generated:",
        "Credentials are written to file",
    )
    with patch("eumdac.token.AccessToken.access_token", "TOKEN"):
        assert_eumdac_output(args, expected)


@unittest.skipIf(INTEGRATION_TESTING, "Covered by unit testing")
def test_download_product(temp_credentials, temp_output_dir):
    args = f"download -c MockCollection -p MockProduct -o {temp_output_dir} --test".split()
    expected = (
        "Processing",
        "Using order",
        "Output directory:",
        "Preparing download",
        "Download complete: MockProduct",
        "Removing successfully finished order",
    )
    assert_eumdac_output(args, expected)


@unittest.skipIf(INTEGRATION_TESTING, "Covered by unit testing")
def test_skip_download_product(temp_credentials, temp_output_dir):
    args = f"download -c MockCollection -p MockProduct -o {temp_output_dir} --test".split()
    expected = ("Processing", "Using order", "Output directory:", "Skip")

    # First run to ensure the file exists already
    eumdac(args)
    assert_eumdac_output(args, expected)


@unittest.skipIf(INTEGRATION_TESTING, "Covered by unit testing")
def test_download_product_entry(temp_credentials, temp_output_dir):
    args = f"download -c MockCollection -p MockProduct --entry *.nc -o {temp_output_dir} --test".split()
    # we expect a folder with the product name to be created when --entry is given
    expected = (
        "Processing",
        "Using order",
        "Output directory:",
        (
            "order_does_not_matter",
            [
                "Job 1: Preparing download",
                "Job 1: Preparing download",
                "Job 1: Download complete",
                "Job 1: Download complete",
            ],
        ),
        "Removing successfully finished order",
    )
    assert_eumdac_output(args, expected)


@unittest.skipIf(INTEGRATION_TESTING, "Covered by unit testing")
def test_download_output_dir(temp_credentials, temp_output_dir):
    args = f"download -c MockCollection --time-range 2020-03-01 2020-03-01T12:15 -o {temp_output_dir} --test".split()
    expected = (
        "Processing",
        "Using order",
        "Output directory:",
        (
            "order_does_not_matter",
            [
                "Job 1: Preparing download",
                "Job 2: Preparing download",
                "Job 1: Download complete",
                "Job 2: Download complete",
            ],
        ),
        "Removing successfully finished order",
    )
    assert_eumdac_output(args, expected)
