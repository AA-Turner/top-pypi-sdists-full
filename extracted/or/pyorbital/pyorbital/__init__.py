"""Package file."""

import numpy as np

from pyorbital.version import __version__  # noqa


def dt2np(utc_time):
    """Convert datetime to numpy datetime64 object."""
    try:
        return np.datetime64(utc_time)
    except ValueError:
        return utc_time.astype("datetime64[ns]")
