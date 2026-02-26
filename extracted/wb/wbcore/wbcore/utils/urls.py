import urllib.parse
from typing import Dict, Tuple

from django.conf import settings
from django.contrib.sites.models import Site
from django.http.request import QueryDict
from django.utils.http import urlencode


def clean_shareable_url(url):
    endpoint = url.split("?widget_endpoint=")[-1]
    parse_url = urllib.parse.urlsplit(urllib.parse.unquote(endpoint))
    endpoint = parse_url.path
    if params := dict(urllib.parse.parse_qsl(parse_url.query)):
        params_repr = "&".join([f"{k}={v}" for k, v in params.items()])
        endpoint += f"?{params_repr}"
    return endpoint


def get_parse_endpoint(endpoint: str) -> Tuple[str, Dict[str, str]]:
    """
    Takes a URL endpoint and outputs the path and the params separately.

    Parameters
    ----------
    endpoint: The endpoint string

    Returns
    -------
    Returns a tuple in the form of (path: str, params: dict[str, str]). Where path is the url and params are the parameters of the endpoint.
    """

    path = urllib.parse.urljoin(endpoint, urllib.parse.urlparse(endpoint).path)
    params = dict(urllib.parse.parse_qsl(urllib.parse.urlsplit(endpoint).query))
    return path, params


def get_urlencode_endpoint(endpoint: str, params: Dict[str, str]) -> str:
    """
    Takes a URL path and params and creates an endpoint from it.

    Parameters
    ----------
    endpoint: The URL string
    params: The params dictonary

    Returns
    -------
    Returns an endpoint string with the params attached.
    """
    if isinstance(params, QueryDict):
        params = params.dict()
    return f"{endpoint}?{urlencode(params)}"


def base_domain() -> str:
    """A utility method that assembles the current domain. Utilizes the site app from django

    Returns:
        A string containing the current domain as noted in the curret `Site` prefixed with the http scheme

    """
    scheme = "https" if settings.SECURE_SSL_REDIRECT else "http"
    base_domain = Site.objects.get_current().domain
    return f"{scheme}://{base_domain}"


def new_mode(url: str) -> str:
    operator = "&" if "?" in url else "?"
    return url + f"{operator}new_mode=true"


def get_multi_request_value(request, field_name: str, sep: str = ",") -> list:
    if value := request.GET.get(field_name):
        value = value[0] if isinstance(value, list) else value
        return urllib.parse.unquote(value).split(sep)
    return []
