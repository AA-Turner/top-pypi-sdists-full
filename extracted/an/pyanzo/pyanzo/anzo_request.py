from typing import Any, Dict, List
from urllib.parse import quote
import os
import requests
import json

# /*******************************************************************************
#  * Copyright (c) 2019 - 2022 Cambridge Semantics Incorporated.
#  * All rights reserved.
#  *
#  * Contributors:
#  *     Cambridge Semantics Incorporated
#  *******************************************************************************/


class AnzoRequest:
    """Encodes a request against Anzo and supports executing the request.

    Instances of AnzoRequest are typically constructed with an
    AnzoRequestBuilder. When a request is executed, a RunTimeError may be
    raised depending on the status code of the HTTP response.

    Attributes:
        url: The url for connecting to the anzo server
        username: Username of the user with which to interact with Anzo.
        password: The password of the user
        headers: The HTTP headers included in the request
        data: The body of the HTTP request
        timeout_seconds: Timeout for the request in seconds
    """

    COOKIE_KEY = "Cookie"

    def __init__(self, url: str, username: str, password: str, auth_token: str,
                 headers: Dict[str, Any], data: Any,
                 timeout_seconds: float) -> None:
        self.url = url
        self.username = username
        self.password = password
        self.auth_token = auth_token
        self.headers = headers
        self.data = data
        self.timeout_seconds = timeout_seconds

    def execute_request(self) -> str:
        """Executes the anzo request and returns the body of the response.

        Returns:
            The body of the HTTP response.

        Raises:
            RunTimeError: If anything goes wrong in executing the request
                or if a non-success HTTP response is received.
        """

        try:
            if self.username and self.password:
                authorization = (self.username, self.password)
            else:
                authorization = ("", "")

            if self.auth_token:
                self.headers[self.COOKIE_KEY] = self.auth_token

            response = requests.post(self.url,
                                     headers=self.headers,
                                     data=self.data,
                                     auth=authorization,
                                     verify=self.ssl_verify(),
                                     timeout=self.timeout_seconds)

        except requests.exceptions.ReadTimeout:
            msg = (f"Request timed out with the timeout set to "
                   f"{self.timeout_seconds} seconds")
            raise TimeoutError(msg) from None
        except Exception as e:
            raise RuntimeError from e

        if response.status_code > 299:
            error = (f"Response from {self.url} returned with "
                     f"non-success status code {response.status_code} "
                     f"and response text: {response.text}")

            raise RuntimeError(error)
        return response.text

    def ssl_verify(self):
        verify = os.getenv('REQUESTS_CA_BUNDLE', False)
        if verify and not os.path.isfile(verify):
            raise IOError("Configured CA Bundle does not exist: " + verify)
        return verify

    def __str__(self) -> str:
        return (f"<AnzoRequest url='{self.url}, "
                f"username='{self.username}', "
                f"password='{self.password}'>")


class AnzoRequestBuilder:
    """Builds an AnzoRequest for executing a request against Anzo.

    Builds an AnzoRequest step-by-step. Once a request is fully specified,
    build() returns an AnzoRequest object which can be executed.

    Attributes:
        payload_dict: The body of the HTTP request. If payload_dict is defined,
            then payload_list must be empty
        payload_list: The body of the HTTP request. If payload_list is defined,
            then payload_dict must be empty
        base_url: The base url used to connect to the anzo server
        url_postfix: A postfix to the url that specifies the type of request
            (e.g. query, semantic service, wtc.)
        username: Username of the user with which to interact with Anzo.
        password: The password of the user
        headers: The HTTP headers included in the request
        timeout_seconds: Timeout for the request in seconds

    Usage:
        arb = AnzoRequestBuilder()
        arb.with_url(self.domain, self.port, self.path)
        arb.with_auth(self.username, self.password, self.auth_token)
        arb.with_graphmart(graphmart)
        arb.with_query_string(query_string)
        anzo_request = arb.build()
        response = anzo_request.execute_request()
    """

    JSON_FORMAT = 'JSON'  # this is case sensitive
    TEXT_JSON_FORMAT = 'text/json'
    APP_JSON_FORMAT = 'application/json'

    PAYLOAD_QUERY_KEY = "query"
    PAYLOAD_FORMAT_KEY = "format"
    PAYLOAD_UPDATE_KEY = "update"
    DEFAULT_NAMED_GRAPH_KEY = "default-named-graph-uri"
    NAMED_GRAPH_KEY = "named-graph-uri"
    DEFAULT_GRAPH_KEY = "default-graph-uri"
    USING_GRAPH_KEY = "using-graph-uri"
    USING_NAMED_GRAPH_KEY = "using-named-graph-uri"
    URI_KEY = "uri"

    JOURNAL_QUERY_POSTFIX = "sparql"
    GRAPHMART_QUERY_POSTFIX = "sparql/graphmart"
    LDS_QUERY_POSTFIX = "sparql/lds"
    SEMANTIC_SERVICE_POSTFIX = "anzoclient/call"
    GET_POSTFIX = "anzoclient/get"
    ADD_POSTFIX = "anzoclient/add"
    REMOVE_POSTFIX = "anzoclient/remove"

    HEADER_URI_KEY = "uri"
    HEADER_FORMAT_KEY = "format"
    HEADER_CONTENT_TYPE_KEY = "Content-Type"
    SKIP_CACHE = "skipCache"

    def __init__(self) -> None:
        self.payload_dict: Dict[str, Any] = {}
        self.payload_list: List = []
        self.headers: Dict[str, Any] = {}
        self.base_url = ""
        self.url_postfix = ""
        self.username = ""
        self.password = ""
        self.auth_token = ""
        self.timeout_seconds = None

    def _raise_if_url_postfix_is_set(self) -> None:
        if self.url_postfix:
            raise RuntimeError("URL Postfix has already been set")

    def with_url(self, domain: str, port: str, path: str) -> None:
        """Adds the url to the AnzoRequestBuilder.

        Raises:
            RuntimeError: If the url has already been set.
        """

        if self.base_url:
            raise RuntimeError("Base URL has already been set")
        if path:
            self.base_url = f'https://{domain}:{port}/{path}'
        else:
            self.base_url = f'https://{domain}:{port}'

    def with_auth(self, username: str, password: str, auth_token: str) -> None:
        """Adds either a username and password or an auth_token
           to the AnzoRequestBuilder.

        Raises:
            RuntimeError: If the username, password, or
                          auth_token has already been set.
            ValueError: If it is not the case that either a username and
                        password have been specified or an auth_token
                        has been specified then an a ValueError is raised.
        """

        if self.username or self.password or self.auth_token:
            raise RuntimeError("Username or password has already been set")

        if username and password and auth_token:
            error = ("Only one of username and password"
                     " or auth_token may be specified")
            raise ValueError(error)

        if not (username or password or auth_token):
            error = "Some form of authentication must be used."
            raise ValueError(error)

        if (username and not password) or (password and not username):
            error = "Both a username and a password must be specified"
            raise ValueError(error)

        if username and password:
            self.username = username
            self.password = password
        else:
            self.auth_token = auth_token

    def with_timeout_seconds(self, timeout_seconds: float) -> None:
        self.timeout_seconds = timeout_seconds

    def with_query_string(self, query_string: str) -> None:
        """Adds the query to the AnzoRequestBuilder.
        """

        self.payload_dict[self.PAYLOAD_QUERY_KEY] = query_string
        self.payload_dict[self.PAYLOAD_FORMAT_KEY] = self.TEXT_JSON_FORMAT

    def with_query_file(self, query_file: str) -> None:
        """Adds the query to the AnzoRequestBuilder.
        """

        _, query_file_extension = os.path.splitext(query_file)
        if query_file_extension != '.rq':
            raise RuntimeError("Query Filepaths must end in '.rq'")

        with open(query_file, 'r') as query_file_handle:
            query_string = query_file_handle.read()
            self.payload_dict[self.PAYLOAD_QUERY_KEY] = query_string
        self.payload_dict[self.PAYLOAD_FORMAT_KEY] = self.TEXT_JSON_FORMAT

    def with_update_string(self, query_string: str) -> None:
        """Adds the query to the AnzoRequestBuilder.
        """

        self.payload_dict[self.PAYLOAD_UPDATE_KEY] = query_string
        self.payload_dict[self.PAYLOAD_FORMAT_KEY] = self.TEXT_JSON_FORMAT

    def with_update_file(self, query_file: str) -> None:
        """Adds the query to the AnzoRequestBuilder.
        """

        _, query_file_extension = os.path.splitext(query_file)
        if query_file_extension != '.rq':
            raise RuntimeError("Query Filepaths must end in '.rq'")

        with open(query_file, 'r') as query_file_handle:
            query_string = query_file_handle.read()
            self.payload_dict[self.PAYLOAD_UPDATE_KEY] = query_string
        self.payload_dict[self.PAYLOAD_FORMAT_KEY] = self.TEXT_JSON_FORMAT

    def with_graphmart(self,
                       graphmart_uri: str,
                       named_graphs: List[str] = None) -> None:
        """Adds the graphmart postfix and uri to the AnzoRequestBuilder.
        """

        encoded_graphmart_uri = quote(graphmart_uri, safe='')
        self.url_postfix = (
            f"{self.GRAPHMART_QUERY_POSTFIX}/{encoded_graphmart_uri}")

        if named_graphs:
            self.payload_dict[self.DEFAULT_GRAPH_KEY] = named_graphs
            self.payload_dict[self.NAMED_GRAPH_KEY] = named_graphs

    def with_query_journal(self, named_graphs: List[str] = None) -> None:
        """Adds the journal postfix to the AnzoRequestBuilder and sets up
        for a query against the journal.

        Raises:
            RuntimeError: If the postfix has already been set.
        """

        self._raise_if_url_postfix_is_set()
        self.url_postfix = self.JOURNAL_QUERY_POSTFIX

        # Don't serialize the named graphs to a single string - we want
        # multiple graphs to be included under the same header, which
        # requires a list. See
        # https://stackoverflow.com/questions/23384230/how-to-post-multiple-value-with-same-key-in-python-requests  # noqa
        # for more info.

        if named_graphs:
            self.payload_dict[self.DEFAULT_NAMED_GRAPH_KEY] = named_graphs
            self.payload_dict[self.NAMED_GRAPH_KEY] = named_graphs

    def with_update_journal(self, named_graphs: List[str] = None) -> None:
        """Adds the journal postfix to the AnzoRequestBuilder and sets up
        for an update query against the journal.

        Raises:
            RuntimeError: If the postfix has already been set.
        """

        self._raise_if_url_postfix_is_set()
        self.url_postfix = self.JOURNAL_QUERY_POSTFIX

        # Don't serialize the named graphs to a single string - we want
        # multiple graphs to be included under the same header, which
        # requires a list. See
        # https://stackoverflow.com/questions/23384230/how-to-post-multiple-value-with-same-key-in-python-requests  # noqa
        # for more info.

        if named_graphs:
            self.payload_dict[self.USING_GRAPH_KEY] = named_graphs
            self.payload_dict[self.USING_NAMED_GRAPH_KEY] = named_graphs

    def with_lds_cat_entry(self,
                           lds_cat_entry: str,
                           named_graphs: List[str] = None) -> None:
        """Adds the lds postfix and uri to the AnzoRequestBuilder.

        Raises:
            RuntimeError: If the postfix has already been set.
        """

        self._raise_if_url_postfix_is_set()
        encoded_lds_cat_entry = quote(lds_cat_entry, safe='')
        self.url_postfix = f'{self.LDS_QUERY_POSTFIX}/{encoded_lds_cat_entry}'

        if named_graphs:
            self.payload_dict[self.DEFAULT_GRAPH_KEY] = named_graphs
            self.payload_dict[self.NAMED_GRAPH_KEY] = named_graphs

    def with_semantic_service(self, service_uri: str, request: List) -> None:
        """Adds the semantic service postfix and payload to the AnzoRequestBuilder.

        Raises:
            RuntimeError: If the postfix has already been set.
        """

        self._raise_if_url_postfix_is_set()
        self.url_postfix = self.SEMANTIC_SERVICE_POSTFIX
        self.headers[self.HEADER_URI_KEY] = service_uri
        self.headers[self.HEADER_FORMAT_KEY] = self.JSON_FORMAT
        self.headers[self.HEADER_CONTENT_TYPE_KEY] = self.APP_JSON_FORMAT
        self.payload_list = request

    def with_get(self, named_graph_uri: str) -> None:
        """Adds the get postfix and named_graph_uri to the payload

        Raises:
            RuntimeError: If the postfix has already been set.
        """

        self._raise_if_url_postfix_is_set()
        self.url_postfix = self.GET_POSTFIX
        self.payload_dict[self.URI_KEY] = named_graph_uri

    def with_add(self, request: List) -> None:
        """Adds the add postfix and payload to the AnzoRequestBuilder.

        Raises:
            RuntimeError: If the postfix has already been set.
        """

        self._raise_if_url_postfix_is_set()
        self.url_postfix = self.ADD_POSTFIX
        self.headers[self.HEADER_FORMAT_KEY] = self.JSON_FORMAT
        self.headers[self.HEADER_CONTENT_TYPE_KEY] = self.APP_JSON_FORMAT
        self.payload_list = request

    def with_remove(self, request: List) -> None:
        """Adds the remove postfix and payload to the AnzoRequestBuilder.

        Raises:
            RuntimeError: If the postfix has already been set.
        """

        self._raise_if_url_postfix_is_set()
        self.url_postfix = self.REMOVE_POSTFIX
        self.headers[self.HEADER_FORMAT_KEY] = self.JSON_FORMAT
        self.headers[self.HEADER_CONTENT_TYPE_KEY] = self.APP_JSON_FORMAT
        self.payload_list = request

    def with_cache_skipped(self, skip_cache: bool):
        """Adds the option to skip AnzoGraph's query cache.

        Raises:
            RuntimeError: We currently don't support skipping the cache
                   so if a user tries to do it, an error is raised.
        """
        if skip_cache:
            self.payload_dict[self.SKIP_CACHE] = "true"

    def build(self) -> AnzoRequest:
        """
        Combine all of the relevant components to build an AnzoRequest.

        Returns:
            A fully developed AnzoRequest object

        Raises:
            ValueError: If any of the relevant components (base_url,
                url_postfix, username and password or authentication,
                and payload_dict OR
                payload_list) of the request are missing.
        """

        if not self.base_url:
            raise ValueError("Can't build an AnzoRequest because "
                             "self.base_url is missing")

        if not self.url_postfix:
            raise ValueError("Can't build an AnzoRequest because "
                             "self.url_postfix is missing")

        if not ((self.username and self.password) or self.auth_token):
            raise ValueError(
                "Can't build AnzoRequest because authorization is missing")

        if self.payload_dict and self.payload_list:
            raise ValueError("Both self.payload_dict and self.payload_list"
                             "cannot be populated")

        if not self.timeout_seconds:
            raise ValueError("A timeout for the request must be specified")

        # Set the data of the request based on the payload.
        # Python-Requests is generous with the type that data can be,
        # so we have two cases:
        # (a) The payload is a dict in which case we pass data as a dict
        # (b) the payload is a list, in which case we pass the serialied
        #     list as a string

        data: Any = None
        if self.payload_dict:
            data = self.payload_dict
        elif self.payload_list:
            data = json.dumps(self.payload_list)

        full_url = f"{self.base_url}/{self.url_postfix}"

        return AnzoRequest(full_url, self.username, self.password,
                           self.auth_token, self.headers, data,
                           self.timeout_seconds)
