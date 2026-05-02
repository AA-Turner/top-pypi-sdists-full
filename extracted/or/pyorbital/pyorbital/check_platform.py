"""Check if a satellite is supported on default.

If not the name and its NORAD number needs to be added to a local copy of the
platforms.txt file, which then needs to be placed in the directory pointed to
by the environment variable PYORBITAL_CONFIG_PATH.

"""

import argparse
import logging

from pyorbital.logger import logging_on
from pyorbital.tlefile import check_is_platform_supported

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Check if a satellite is supported.")
    parser.add_argument("-s", "--satellite",
                        help=("Name of the Satellite [in upper case] - following WMO Oscar naming."),
                        default=None,
                        required=True,
                        type=str)

    args = parser.parse_args()
    satellite_name = args.satellite

    logging_on(logging.INFO)
    check_is_platform_supported(satellite_name)
