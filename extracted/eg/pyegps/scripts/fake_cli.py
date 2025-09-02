"""Allows direct execution of CLI with dummy devices."""
from unittest.mock import patch
import sys
import os

sys.path.append( os.path.join(os.path.dirname(__file__), "..","src") )

import pyegps
from pyegps.fakes.powerstrip import FakePowerStrip

def take_dummy_devices():
    return patch("pyegps.search_for_devices", return_value=FakePowerStrip.search_for_devices() )


if __name__ == "__main__":
    with take_dummy_devices() as mock:
        from pyegps import cli
        sys.exit(cli.cli(sys.argv[1:]))
