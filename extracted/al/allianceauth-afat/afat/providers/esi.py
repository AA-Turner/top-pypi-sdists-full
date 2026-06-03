"""
ESI provider
"""

# Standard Library
from typing import Any

# Third Party
from aiopenapi3 import ContentTypeError, RequestError
from httpx import Response

# Alliance Auth
from allianceauth.services.hooks import get_extension_logger
from esi.exceptions import HTTPClientError, HTTPNotModified
from esi.openapi_clients import ESIClientProvider, EsiOperation

# Alliance Auth AFAT
from afat import (
    __app_name_verbose__,
    __esi_compatibility_date__,
    __github_url__,
    __version__,
)
from afat.providers.applogger import AppLogger

logger = AppLogger(my_logger=get_extension_logger(__name__))

# ESI client
esi = ESIClientProvider(
    # Use the latest compatibility date, see https://esi.evetech.net/meta/compatibility-dates
    compatibility_date=__esi_compatibility_date__,
    # User agent for the ESI client
    ua_appname=__app_name_verbose__,
    ua_version=__version__,
    ua_url=__github_url__,
    operations=[
        "GetCharactersCharacterIdCorporationhistory",
        "GetCharactersCharacterIdFleet",
        "GetCharactersCharacterIdLocation",
        "GetCharactersCharacterIdOnline",
        "GetCharactersCharacterIdShip",
        "GetCorporationsCorporationIdAlliancehistory",
        "GetFleetsFleetIdMembers",
        "PostUniverseIds",
    ],
)


class ESIHandler:
    """
    Handler for ESI operations, providing a method to retrieve results while handling exceptions.
    """

    @classmethod
    def result(  # pylint: disable=too-many-arguments, too-many-positional-arguments
        cls,
        operation: EsiOperation,
        use_etag: bool = True,
        return_response: bool = False,
        force_refresh: bool = False,
        use_cache: bool = True,
        **extra,
    ) -> Any | tuple[Any, Response] | None:
        """
        Retrieve the result of an ESI operation, handling HTTPNotModified exceptions.

        :param operation: The ESI operation to execute.
        :type operation: EsiOperation
        :param use_etag: Whether to use ETag for caching.
        :type use_etag: bool
        :param return_response: Whether to return the full response object.
        :type return_response: bool
        :param force_refresh: Whether to force a refresh of the data.
        :type force_refresh: bool
        :param use_cache: Whether to use cached data.
        :type use_cache: bool
        :param extra: Additional parameters to pass to the operation.
        :type extra: dict
        :return: The result of the ESI operation.
        :rtype: Any | tuple[Any, Response] | None
        """

        logger.debug(f"Handling ESI operation: {operation.operation.operationId}")
        logger.debug(
            f"Operation parameters: use_etag={use_etag}, return_response={return_response}, force_refresh={force_refresh}, use_cache={use_cache}, extra={extra}"
        )

        response: Response | None = None

        try:
            # Call operation.result differently depending on whether the caller
            # requested the raw Response object. Some implementations return a
            # single result when return_response is False and a (result, response)
            # tuple when True, so only unpack when return_response is True.
            if return_response:
                esi_result, response = operation.result(
                    use_etag=use_etag,
                    return_response=return_response,
                    force_refresh=force_refresh,
                    use_cache=use_cache,
                    **extra,
                )

                logger.debug(
                    f"ESI Response for operation: {operation.operation.operationId}: {response}"
                )
            else:
                esi_result = operation.result(
                    use_etag=use_etag,
                    return_response=return_response,
                    force_refresh=force_refresh,
                    use_cache=use_cache,
                    **extra,
                )
        except HTTPNotModified:
            logger.debug(
                f"ESI returned 304 Not Modified for operation: {operation.operation.operationId} - Skipping update."
            )

            esi_result = None
        except ContentTypeError:
            logger.warning(
                msg="ESI returned gibberish (ContentTypeError) - Skipping update."
            )

            esi_result = None
        except (HTTPClientError, RequestError) as exc:
            logger.error(msg=f"Error while fetching data from ESI: {str(exc)}")

            esi_result = None

        # If caller requested the raw response, return a tuple (result, response)
        if return_response:
            return esi_result, response

        return esi_result
