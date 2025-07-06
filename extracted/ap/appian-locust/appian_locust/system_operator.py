from requests.models import Response
from typing import Optional, Dict, Any

from ._actions import _Actions
from ._interactor import _Interactor


class SystemOperator:
    """
    Class for providing the ability to perform activities that do not require a UI interaction
    i.e. triggering an action without a startform.
    """

    def __init__(self, interactor: _Interactor, actions: _Actions):
        self.__interactor = interactor
        self.__actions = actions

    def start_action(self, action_name: str, skip_design_call: bool = False,
                     exact_match: bool = False) -> Response:
        """
        Perform the post operation on action's API to start specific action.
        Actions that do not have a UI can be called directly without using "GET" to retrieve the UI.
        this is controlled by the optional skip_design_call parameter

        Args:
            action_name(str): Name of the action
            skip_design_call(bool, optional): to skip the "GET" call for the action's UI. Default : False
            exact_match (bool, optional): Should action name match exactly or to be partial match. Default : False

        Returns: requests.models.Response

        Example:

            >>> self.appian.site_helper.start_action("action_name")

        """
        return self.__actions.start_action(action_name, skip_design_call, exact_match)

    def get_webapi(self, uri: str, headers: Optional[Dict[str, Any]] = None, locust_request_label: Optional[str] = None,
                   query_parameters: Dict[str, Any] = {}) -> Response:
        """
        Make a GET request to a web api endpoint
        Args:
            uri: API URI to be called
            headers: header for the REST API Call
            locust_request_label: the label to be displayed by locust
            query_parameters: Queries/Filters

        Returns: Json response of GET operation

        To set custom headers

        >>> headers = {'Is-Admin': 'true'}
        ... self.appian.system_operator.get_webapi('/suite/webapi/headers', headers=headers)

        To set custom query parameters

        >>> params = {'age': 5, 'start-date': '10-05-2020'}
        ... self.appian.system_operator.get_webapi('/suite/webapi/query', query_parameters=params)
        """
        querystring = []
        for k, v in query_parameters.items():
            querystring.append("{}={}".format(k, v))

        uri += "?" + "&".join(querystring)
        resp = self.__interactor.get_page(uri, headers=headers, label=locust_request_label)
        return resp

    def post_webapi(
        self,
        uri: str,
        headers: Optional[Dict[str, Any]] = None,
        locust_request_label: Optional[str] = None,
    ) -> Response:
        """
        Make a GET request to a web api endpoint
        Args:
            uri: API URI to be called
            headers: header for the REST API Call
            locust_request_label: the label to be displayed by locust

        Returns: Json response of GET operation

        To set custom headers

        >>> headers = {'Is-Admin': 'true'}
        ... self.appian.system_operator.post_webapi('/suite/webapi/headers', headers=headers)
        """
        resp = self.__interactor.post_page(uri, headers=headers, label=locust_request_label)
        return resp

    def fetch_autosuggestions(
        self,
        payload: Dict[str, Any],
        locust_request_label: Optional[str] = None,
    ) -> Response:
        """
        Retrieve suggestions from autosuggest endpoint
        Args:
            payload: payload containing expression details to retrieve suggestions for
            locust_request_label: the label to be displayed by locust

        Returns: Json response of suggestions
        """
        uri = "/suite/rest/a/interfacedesigner/latest/autosuggest"
        headers = self.__interactor.setup_sail_headers()
        headers["Accept"] = "application/vnd.appian.tv+json"
        resp = self.__interactor.post_page(
            uri, payload=payload, headers=headers, label=locust_request_label)
        return resp

    def fetch_content(self, opaque_id: str, locust_request_label: Optional[str]) -> Response:
        """
        Fetch a content element, such as an image
        Args:
            opaque_id: The opaque id of the content to download
            locust_request_label: label to associate request with

        Returns: Response object containing information of downloaded content

        """
        locust_request_label = locust_request_label or f"system_operator.DownloadContent.{opaque_id}"
        uri = f"/suite/rest/a/content/latest/{opaque_id}/o"
        headers = self.__interactor.setup_content_headers()
        return self.__interactor.get_page(
            uri=uri, headers=headers, label=locust_request_label)
