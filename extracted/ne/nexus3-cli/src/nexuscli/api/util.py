import functools
import json
import pathlib
import warnings
from typing import Any, Callable, List, TypeVar, Type, Union, cast

import requests
import semver

import nexuscli
from nexuscli import exception

# https://mypy.readthedocs.io/en/stable/generics.html#declaring-decorators
F = TypeVar('F', bound=Callable[..., Any])


def script_for_version(
        script_name: str,
        server_version: semver.VersionInfo,
        versions: List[semver.VersionInfo]) -> str:
    """
    Determine if a certain nexus server version requires a different version of
    the given groovy script.

    :param script_name: original name of the script.
    :param server_version: VersionInfo for the Nexus server.
    :param versions: list of VersionInfo. Each element represents an existing
        groovy script that must be used with server_version or greater.
    :return: the version-specific name of script_name.
    """
    if server_version is None:
        return script_name

    for breaking_version in sorted(versions, reverse=True):
        if server_version >= breaking_version:
            script_path = pathlib.Path(script_name)
            # e.g.: nexus3-cli-repository-create_3.21.0.groovy
            return f'{script_path.stem}_{breaking_version}{script_path.suffix}'

    return script_name


def with_min_version(min_version: str) -> Callable[[F], F]:
    """Verifies that the `nexus_client` instance has version greater or equal to min_version"""
    def decorator(f):
        @functools.wraps(f)
        # be explicit that args[0] is `self` in the context of the calling class instance
        def wrapper(collection: 'nexuscli.api.base_collection.BaseCollection', *args, **kwargs):
            try:
                if collection._http.server_version is None:
                    raise ValueError('server_version is None')

                min_semver = semver.VersionInfo.parse(min_version)
            except ValueError:
                warnings.warn(
                    'Invalid semver string; skipping version capability check', stacklevel=2)
                return f(collection, *args, **kwargs)

            if collection._http.server_version < min_semver:
                raise exception.NexusClientCapabilityUnsupported(
                    f'{f} requires version {min_semver}; server has '
                    f'version {collection._http.server_version}')

            return f(collection, *args, **kwargs)

        return cast(F, wrapper)
    return decorator


def validate_response(response: requests.Response,
                      accepted_codes: Union[int, List[int]],
                      exc_class: Type[Exception] = exception.NexusClientAPIError) -> None:
    """
    Ensure that :py:attr:`response.status_code` is one of ``accepted_codes``, otherwise raise
    exception ``exc_class`` using the response content as the error message.
    """
    if isinstance(accepted_codes, int):
        accepted_codes = [accepted_codes]

    if response.status_code not in accepted_codes:
        message = response.text
        try:
            nexus_messages = response.json()
            error_messages = [f'{x["id"]} {x["message"]}' for x in nexus_messages]
            message = '\n'.join(error_messages)
        except (IndexError, KeyError, TypeError, json.JSONDecodeError):
            pass
        raise exc_class(message)
