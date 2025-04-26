"""A Python parser for the a-deck data posted online by the Automated Tropical Cyclone Forecasting System."""
from __future__ import annotations

import gzip
import io

import pandas as pd
import requests
from retry import retry


@retry()
def get_gzipped_url(url: str) -> str:
    """Open a gzipped file from a URL and return its contents as a list of strings.

    Parameters
    ----------
    url : str
        URL of the gzipped file.

    Returns
    -------
    str
        List of strings representing the lines of the file.

    Examples
    --------
    >>> url = "https://ftp.nhc.noaa.gov/atcf/aid_public/aep182023.dat.gz"
    >>> get_gzipped_url(url)
    """
    # Read in the  URL
    r = requests.get(url)

    # Unzip the file
    f = io.BytesIO(r.content)

    # Read the unzipped file
    with gzip.GzipFile(fileobj=f) as fh:
        # Convert the file to a list of strings
        content = fh.read().decode("utf-8")

    # Close the file
    f.close()

    # Return the file contents
    return content


def get_dataframe(url: str) -> pd.DataFrame:
    """Parse a fixed-width file into a pandas DataFrame.

    Parameters
    ----------
    url : str
        URL of the gzipped file.

    Returns
    -------
    pandas.DataFrame
        DataFrame containing the parsed data.

    Examples
    --------
    >>> url = "https://ftp.nhc.noaa.gov/atcf/aid_public/aep182023.dat.gz"
    >>> get_dataframe(url)
    """
    data = get_gzipped_url(url)
    return pd.read_fwf(
        io.StringIO(data),
        colspecs=[
            (0, 2),
            (4, 6),
            (8, 18),
            (20, 22),
            (24, 28),
            (30, 33),
            (35, 39),
            (41, 46),
            (48, 51),
            (53, 57),
            (59, 61),
            (63, 66),
            (68, 71),
            (73, 77),
            (79, 83),
            (85, 89),
            (91, 95),
            (97, 101),
            (103, 107),
            (109, 112),
            (114, 117),
            (119, 122),
            (124, 127),
            (129, 132),
            (134, 137),
            (139, 142),
            (144, 147),
            (149, 159),
            (161, 162),
            (164, 166),
            (168, 171),
            (173, 177),
            (179, 183),
            (185, 189),
            (191, 195),
            (197, 210),
            (212, 412),
        ],
        header=None,
        names=[
            "BASIN",
            "CY",
            "YYYYMMDDHH",
            "TECHNUM/MIN",
            "TECH",
            "TAU",
            "LATN/S",
            "LONE/W",
            "VMAX",
            "MSLP",
            "TY",
            "RAD",
            "WINDCODE",
            "RAD1",
            "RAD2",
            "RAD3",
            "RAD4",
            "POUTER",
            "ROUTER",
            "RMW",
            "GUSTS",
            "EYE",
            "SUBREGION",
            "MAXSEAS",
            "INITIALS",
            "DIR",
            "SPEED",
            "STORMNAME",
            "DEPTH",
            "SEAS",
            "SEASCODE",
            "SEAS1",
            "SEAS2",
            "SEAS3",
            "SEAS4",
            "USERDEFINED",
            "USERDATA",
        ],
    )
