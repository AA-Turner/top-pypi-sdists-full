from __future__ import annotations

import abc
import logging
import typing as t
import urllib.parse

from globus_sdk._internal.remarshal import commajoin
from globus_sdk._missing import filter_missing

from ..response import OAuthAuthorizationCodeResponse

log = logging.getLogger(__name__)


class GlobusOAuthFlowManager(abc.ABC):
    """
    An abstract class definition that defines the interface for the Flow
    Managers for Globus Auth.
    Flow Managers are really just bundles of parameters to Globus Auth's OAuth2
    mechanisms, along with some useful utility methods.
    Primarily they can be used as a simple way of tracking small amounts of
    state in your application as it leverages Globus Auth for authentication.

    For sophisticated use cases, the provided Flow Managers will *NOT* be
    sufficient, but you should consider the provided objects a model.

    This way of managing OAuth2 flows is inspired by
    `oauth2client <https://github.com/google/oauth2client>`_. However, because
    ``oauth2client`` has an uncertain future (as of 2016-08-31), and we would
    have to wrap it in order to provide a clean API surface anyway, we
    implement our own set of Flow objects.
    """

    @abc.abstractmethod
    def get_authorize_url(self, query_params: dict[str, t.Any] | None = None) -> str:
        """
        This method consumes no arguments or keyword arguments, and produces a
        string URL for the Authorize Step of a 3-legged OAuth2 flow.
        Most typically, this is the first step of the flow, and the user may be
        redirected to the URL or provided with a link.

        The authorize_url may be (usually is) parameterized over attributes of
        the specific flow manager instance which is generating it.

        :param query_params: Any additional parameters to be passed through
            as query params on the URL.
        """

    @staticmethod
    def _get_authorize_url(
        *,
        base_url: str,
        base_query_params: dict[str, t.Any],
        query_params: dict[str, t.Any] | None,
    ) -> str:
        """
        Get an authorize URL.

        Query parameters may be formatted or excluded to meet known requirements.

        :param base_url:
            The base URL, which may include a path.
        :param base_query_params:
            The base query parameters that are provided by the subclass.
        :param query_params:
            Query parameters that are provided by callers.
            These will always override *base_query_params*
            but are still subject to format and exclusion requirements.
        """

        log.debug(f"Building authorization URI. Base URL: {base_url}")
        log.debug(f"query_params={query_params}")

        params = {
            **base_query_params,
            **(query_params or {}),
        }
        params = filter_missing(params)

        # Format well-known keys, if they have truth-y values.
        comma_joined_keys = {
            "session_required_identities",
            "session_required_single_domain",
            "session_required_policies",
        }
        for key in comma_joined_keys:
            # Pop the value and only re-set it if it's truth-y.
            value = params.pop(key, None)
            if value:
                params[key] = commajoin(value)

        encoded_params = urllib.parse.urlencode(params)
        return f"{base_url}?{encoded_params}"

    @abc.abstractmethod
    def exchange_code_for_tokens(
        self, auth_code: str
    ) -> OAuthAuthorizationCodeResponse:
        """
        This method takes an auth_code and produces a response object
        containing one or more tokens.
        Most typically, this is the second step of the flow, and consumes the
        auth_code that was sent to a redirect URI used in the authorize step.

        The exchange process may be parameterized over attributes of the
        specific flow manager instance which is generating it.

        :param auth_code: The authorization code which was produced from the
            authorization flow
        """
