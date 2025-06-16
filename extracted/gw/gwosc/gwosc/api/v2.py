# Copyright (C) Cardiff University (2018-2021)
# SPDX-License-Identifier: MIT
import logging
import time
import warnings
from urllib import parse

import requests

from gwosc import __version__

from . import DEFAULT_URL

logger = logging.getLogger(__name__)

#: Cache of downloaded blobs
JSON_CACHE = {}

#: Number of pages to fetch that trigger a warning
LARGE_NUM_PAGES_WARN = 100
# Number of request retries after a 429 code, before we raise an exception
MAX_RETRIES = 10
# Default wait time before we retry, if the `Retry-After` header key in the
# response is not set, or if it can't be parsed as an integer
RETRY_DEFAULT_WAIT_TIME = 1  # seconds
# Timeout before a request is dropped
TIMEOUT = 10  # seconds


# -- JSON handling ------------------------------------------------------------


def fetch_json(url, **kwargs):
    """Fetch JSON data from a remote URL

    Parameters
    ----------
    url : `str`
        the remote URL to fetch

    **kwargs
        other keyword arguments are passed directly to :func:`requests.get`

    Returns
    ------
    data : `dict` or `list`
        the data fetched from ``url`` as parsed by
        :meth:`requests.Response.json`

    See also
    --------
    json.loads
        for details of the JSON parsing
    """
    if url in JSON_CACHE.keys():
        return JSON_CACHE[url]

    logger.debug("fetching %s", url)
    client_headers = {"User-Agent": f"python-gwosc/{__version__}"}
    resp = requests.get(url, headers=client_headers, timeout=TIMEOUT, **kwargs)
    retry_attempt = 0
    while resp.status_code == 429 and retry_attempt < MAX_RETRIES:
        # we made too many requests per second
        try:
            retry_after = int(resp.headers.get("Retry-After", RETRY_DEFAULT_WAIT_TIME))
        except ValueError:
            retry_after = RETRY_DEFAULT_WAIT_TIME
        time.sleep(retry_after)
        resp = requests.get(url, headers=client_headers, timeout=TIMEOUT, **kwargs)
        retry_attempt = retry_attempt + 1
    resp.raise_for_status()
    return JSON_CACHE.setdefault(url, resp.json())


def produce_fetched_objects(url):
    current_page = fetch_json(url)
    num_pages = current_page["num_pages"]
    if num_pages > LARGE_NUM_PAGES_WARN:
        warn_message = (
            f"Your request will need to fetch for {num_pages} pages. "
            "Try to constraint your request if possible."
        )
        warnings.warn(warn_message)
        logger.warning(warn_message)
    yield from current_page["results"]
    # Iterate over the rest of the pages
    next_page = current_page["next"]
    while next_page is not None:
        current_page = fetch_json(next_page)
        next_page = current_page["next"]
        yield from current_page["results"]


def fetch_run_strain_files(
    run=None,
    detector=None,
    start=None,
    end=None,
    sample_rate=None,
    host=DEFAULT_URL,
):
    """Return strain file objects from bulk-data releases.

    Parameters
    ----------
    run : `str`, optional
        the ID of a run, e.g. ``'O1'``

    detector : `str`, optional
        the prefix of the GW detector, e.g. ``'L1'``

    start : `int`, optional
        the GPS start of the desired interval

    end : `int`, optional
        the GPS end of the desired interval

    sample_rate : `int`, optional
        the sample rate of the strain file data, either 4096 or 16384 [Hz]

    host : `str`, optional
        the URL of the GWOSC host to query, defaults to
        https://gwosc.org

    Returns
    -------
    data : `iterable[dict]`
        An iterable of strain file dictionaries.
    """

    if run is not None:
        if "KHZ_R1" in run:
            run = run.split("_")[0]
        strain_url = f"{host}/api/v2/runs/{run}/strain-files"
    else:
        strain_url = f"{host}/api/v2/strain-files"

    # Prepare query parameters
    start = None if start is None else int(start)
    end = None if end is None else int(end)
    sample_rate = {4096: 4, 16_384: 16}.get(sample_rate, sample_rate)
    query_params = {
        k: v
        for k, v in {
            "detector": detector,
            "start": start,
            "stop": end,
            "sample-rate": sample_rate,
        }.items()
        if v is not None
    }
    query_string = parse.urlencode(query_params)

    if query_string:
        strain_url = f"{strain_url}?{query_string}"

    yield from produce_fetched_objects(strain_url)


def fetch_event_strain_data(
    event,
    detector=None,
    version=None,
    catalog=None,
    sample_rate=None,
    duration=None,
    format="hdf5",
    host=DEFAULT_URL,
):
    """Return strain file objects from single-event releases.

    Parameters
    ----------
    event : `str` or `None`
        the ID of an event, e.g. ``'GW150914'``

    detector : `str`
        the prefix of the GW detector, e.g. ``'L1'``

    version : `int`
        the version number of the requested event

    catalog : `str`
        the catalog in which the requested event appears

    sample_rate : `int`
        the sample rate of the strain file data, either 4096 or 16384 [Hz]

    duration : `int`
        the duration of the strain file, 32 or 4096 [s]

    format : `str`
        the file format of the strain file.
        One of ``'hdf'``, ``'gwf'``, ``'txt'``

    host : `str`, optional
        the URL of the GWOSC host to query, defaults to
        https://gwosc.org

    Returns
    -------
    data : `iterable[dict]`
        An iterable of strain file dictionaries.
    """

    # Prepare event ID
    event_id = event
    if "-v" not in event:
        if version is not None:
            event_id = f"{event}-v{version}"
        elif catalog is not None:
            event_id = f"{event}@{catalog}"

    strain_url = f"{host}/api/v2/event-versions/{event_id}/strain-files"

    # Prepare query parameters
    format = "hdf" if format == "hdf5" else format
    sample_rate = {4096: 4, 16_384: 16}.get(sample_rate, sample_rate)
    query_params = {
        k: v
        for k, v in {
            "detector": detector,
            "sample-rate": sample_rate,
            "file-format": format,
            "duration": duration,
        }.items()
        if v is not None
    }
    query_string = parse.urlencode(query_params)

    if query_string:
        strain_url = f"{strain_url}?{query_string}"

    yield from produce_fetched_objects(strain_url)


def fetch_segments(flag, start, end, host=DEFAULT_URL):
    """Return segment dictionaries in the (start, end) GPS time interval.

    Parameters
    ----------
    flag : `str`
        name of flag, e.g. ``'H1_DATA'``

    start : `int`
        the GPS start time of your query

    end : `int`
        the GPS end time of your query

    host : `str`, optional
        the URL of the GWOSC host to query, defaults to
        https://gwosc.org

    Returns
    -------
    data : `iterable[dict]`
        An iterable of segment dictionaries.
    """
    segments_url = f"{host}/api/v2/timelines/{flag}/segments?start={start}&stop={end}"
    yield from produce_fetched_objects(segments_url)


def fetch_runs(host=DEFAULT_URL):
    """Return a list of all past runs

    Parameters
    ----------
    host : `str`, optional
        the URL of the GWOSC host to query, defaults to
        https://gwosc.org

    Returns
    -------
    data : `iterable[dict]`
        An iterable of runs.
    """
    yield from produce_fetched_objects(f"{host}/api/v2/runs")


def fetch_catalogs(host=DEFAULT_URL):
    """Returns a list with all catalogs

    Parameters
    ----------
    host : `str`, optional
        the URL of the GWOSC host to query, defaults to
        https://gwosc.org

    Returns
    -------
    data : `iterable[dict]`
        A list of catalogs
    """
    yield from produce_fetched_objects(f"{host}/api/v2/catalogs")


def fetch_event_versions(
    name=None, segment=None, catalogs=None, select=None, host=DEFAULT_URL
):
    """Returns an event

    Parameters
    ----------
    name: `str`, optional
        a full or partial name for an event

    segment: `tuple`, optional
        a gps time tuple (start, end) to restrict the search

    catalogs: `str`, `iterable`, optional
        a single catalog name or a list of catalog names

    select: `dict`, optional
        a dictionary with query parameters, e.g. {'min-p-astro': 0.5}

    host: `str`, optional
        the URL of the GWOSC host to query, defaults to
        https://gwosc.org

    Returns
    -------
    data : `iterable[dict]`
        A list of event version dictionaries
    """
    events_url = f"{host}/api/v2/event-versions"

    query = {}
    if name is not None:
        query["name-contains"] = name

    if segment is not None:
        query["min-gps-time"], query["max-gps-time"] = segment

    if catalogs is not None:
        if isinstance(catalogs, str):
            query["release"] = catalogs
        else:
            if len(catalogs) > 0:
                query["release"] = ",".join(catalogs)

    if select is not None:
        query = {**query, **select}

    query_string = parse.urlencode(query)

    if query_string:
        events_url = f"{events_url}?{query_string}"

    yield from produce_fetched_objects(events_url)


def fetch_run(run, host=DEFAULT_URL):
    """Return a run detail

    Parameters
    ----------

    run : `str`
        the name of the run, e.g. O1

    host : `str`, optional
        the URL of the GWOSC host to query, defaults to
        https://gwosc.org

    Returns
    -------
    data : `dict`
        A dictionary with the run detail
    """
    try:
        run = fetch_json(f"{host}/api/v2/runs/{run}")
    except requests.HTTPError:
        raise ValueError(f"Run '{run}' not found.")
    return run


def fetch_event_version(event, catalog=None, version=None, host=DEFAULT_URL):
    """Returns an event

    Parameters
    ----------
    event : `str`
        the name of the event

    catalog : `str`, optional
        name of catalogue that hosts this event

    version : `int`, `None`, optional
        the version of the data release to use,
        defaults to the highest available version

    host : `str`, optional
        the URL of the GWOSC host to query, defaults to
        https://gwosc.org

    Returns
    -------
    data : `dict`
        A dictionary with the event detail
    """
    event_string = event
    if "-v" in event:
        event_string = event
    elif version is not None:
        event_string = f"{event}-v{version}"
    elif catalog is not None:
        event_string = f"{event}@{catalog}"
    event_url = f"{host}/api/v2/event-versions/{event_string}"

    return fetch_json(event_url)


def fetch_allowed_params(host=DEFAULT_URL):
    return list(produce_fetched_objects(f"{host}/api/v2/default-parameters"))
