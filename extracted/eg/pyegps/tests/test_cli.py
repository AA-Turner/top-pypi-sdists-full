"""Command line interface (cli) tests for pyEGPS."""

import pytest
from unittest.mock import patch

from pyegps import cli
from pyegps.fakes.powerstrip import FakePowerStrip

fake_devices = FakePowerStrip.search_for_devices()


@pytest.mark.parametrize(
    ("device_id", "cli_args", "return_code"),
    [
        # Device not found
        ("XX:XX:XX:XX", ("set", "--on", "0"), 1),
        # No socket specified
        ("DYPS:00:11:22", ("set", "--on"), 1),
        # Device has sockets 0..3, set socket 3
        ("DYPS:AA:BB:CC", ("set", "--on", "3"), 0),
        # Device has sockets 0..1, set socket 3
        ("DYPS:00:11:22", ("set", "--on", "3"), 1),
        # Device has sockets 0..3, receive status 0..3
        ("DYPS:AA:BB:CC", ("status", "0", "1", "2", "3"), 0),
        # Device has sockets 0..1, receive status 0..3
        ("DYPS:00:11:22", ("status", "0", "1", "2", "3"), 1),
        # Device has sockets 0..3, receive status summary
        ("DYPS:AA:BB:CC", ("status",), 0),
    ],
)
def test_exit_codes(device_id: str, cli_args: tuple["str"], return_code: int) -> None:
    """Checking error handling via exit codes."""
    with patch("pyegps.cli.search_for_devices", return_value=fake_devices):
        assert cli.cli(("--device", device_id) + cli_args) == return_code


def test_outputs(capsys):
    """Checking consistency of setting and reading socket status."""
    with patch("pyegps.cli.search_for_devices", return_value=fake_devices):
        # set status and read if it the same
        cli.cli(
            ["--device", "DYPS:AA:BB:CC", "set", "--on", "0", "2", "--off", "1", "3"]
        )
        cli.cli(["--device", "DYPS:AA:BB:CC", "status", "0", "1", "2", "3"])
        captured = capsys.readouterr()
        assert captured.out.strip() == "on off on off"
