import json
from typing import List, Optional
from .query_result import QueryResult, QuadStore
from .anzo_request import AnzoRequestBuilder
from .uris import ALL_NAMED_GRAPHS_URI
# /*******************************************************************************
#  * Copyright (c) 2019 - 2022 Cambridge Semantics Incorporated.
#  * All rights reserved.
#  * 
#  * Contributors:
#  *     Cambridge Semantics Incorporated
#  *******************************************************************************/


class AnzoClient:
    """A class for interacting with an Anzo Server.

    This wraps the anzo HTTP endpoints in order to ask questions of Anzo
    and invoke actions on the Anzo server.

    The general patterns throughout this class are:

    - ValueError is raised if the arguments are invalid
    - Arguments are checked frequently and strictly
    - An error is raised if the operation was unsuccessful (e.g., a query
      with a syntax error)
        - A TimeoutError is raised if the operation times out
        - A RuntimError is thrown otherwise
    - Query results are returned as a QueryResult object, from which the user
      can retrieve the results in whichever form is most useful

    Attributes:
        domain: The domain of the server that Anzo is running on.
        port: The port on which Anzo is listening for HTTPS traffic.
            Often 443 or 8443.
        path: Any additional path configuration information.
        auth_token: The authentication token that is being used
        username: Username of the user with which to interact with Anzo.
        password: The password of the user
        timeout_seconds: Timeout for operations in seconds

    Usage:
        anzo_client = AnzoClient(
            "anzo.cambridgesemantics.com", "8080", "username", "password"
        )

        query_result = anzo_client.query_graphmart(
            "urn://graphmart_uri",
            query_string="SELECT * WHERE { ?s ?p ?o } LIMIT 10",
        )

        ss_result = anzo_client.execute_semantic_service("urn://service", [])
    """

    SYSTEM_TABLE_LDS_URI = "http://openanzo.org/catEntry(%5Bhttp%3A%2F%2Fcambridgesemantics.com%2Fontologies%2F2009%2F05%2FLinkedData%23AnzoXray%5D%40%5Bhttp%3A%2F%2Fcambridgesemantics.com%2Fdatasource%2FSystemTables%5D)"  # noqa

    def __init__(self,
                 domain: str,
                 port: str,
                 path: str = "",
                 username: str = "",
                 password: str = "",
                 auth_token: str = "",
                 timeout_seconds: float = 7200.,
                 ssl_workaround = True) -> None:
        """Constructs an AnzoClient for interacting with an Anzo server.

        Args:
            domain: The domain of the server that Anzo is running on.
            port: The port on which Anzo is listening for HTTPS traffic.
                Often 443 or 8443.
            path (optional): Any additional path required for authentication.
            username (optional): Username of the user with which
                to interactwith Anzo.
            password (optional): The password of the user
            auth_token (optional): An authorization token.
            timeout_seconds (optional): Timeout for operations in seconds
            ssl_workaround (optional): Add lower security SSL DH cipher enabled by default for convenience.

        Returns:
            An AnzoClient object

        Note: An AnzoClient must be passed either a username
                and password or an auth_token, but not both.
        """

        self.domain = domain 
        self.port = port
        self.path = path
        if ssl_workaround:
            self.__ssl_config()
        
        if username and not password:
            error = "If a username is specified a password also needs to be"
            raise ValueError(error)

        if password and not username:
            error = "If password is specified a username also needs to be"
            raise ValueError(error)

        if username and password and auth_token:
            error = "Username and password specified as well as an auth_token"
            raise ValueError(error)

        if not (username or password or auth_token):
            error = "Some form of authentication must be provided."
            raise ValueError(error)

        self.username = username
        self.password = password
        self.auth_token = auth_token
        self.timeout_seconds = timeout_seconds

    def query_graphmart(self,
                        graphmart: str,
                        query_string: str = "",
                        query_file: str = "",
                        data_layers: List[str] = None,
                        skip_cache: bool = False) -> QueryResult:
        """Executes a SPARQL query against a Graphmart.

        Args:
            graphmart: URI of the graphmart to query
            query_string: (optional) SPARQL query string to execute against the
                graphmart. Either query_string or query_file must be provided,
                but not both.
            query_file: (optional) File with SPARQL query to execute against
                the graphmart. Either query_string or query_file must be
                provided, but not both.
            data_layers (optional): List of data layers to query. The uris
                of the layers should be specified in individual strings
                like ["urn://layer1", "urn://layer1"]. The default is to
                query all data layers graphs in the graphmart.
            skip_cache (optional): A boolean, when set to True skips Anzo's
                query cache to compute as opposed to look up the query's results.

        Returns:
            The result of the query in a QueryResult object.
        """
        # Check if either a query_string or a query_file, but not both.
        if not query_string and not query_file:
            raise ValueError(
                "Method query_graphmart requires either a query string "
                "or query file"
            )

        if query_string and query_file:
            raise ValueError(
                "Method query_graphmart received both a query string "
                "and a query file. Only one should be provided"
            )

        if not graphmart:
            raise ValueError("A graphmart is required")

        arb = AnzoRequestBuilder()
        arb.with_url(self.domain, self.port, self.path)
        arb.with_auth(self.username, self.password, self.auth_token)
        arb.with_timeout_seconds(self.timeout_seconds)
        arb.with_graphmart(graphmart, data_layers)

        if query_string:
            arb.with_query_string(query_string)
        elif query_file:
            arb.with_query_file(query_file)

        arb.with_cache_skipped(skip_cache)

        anzo_request = arb.build()
        response_text = anzo_request.execute_request()
        return QueryResult(response_text)

    def query_journal(self, query_string: str = "",
                      query_file: str = "",
                      named_graphs: List[str] = None) -> QueryResult:
        """Executes a SPARQL query against the Anzo journal.

        Given some query, execute a query against the Anzo journal.
        Either a query_string or query_file must be provided, but not both.

        Args:
            query_string: (optional) SPARQL query string to execute against the
                journal. Either query_string or query_file must be provided,
                but not both.
            query_file: (optional) File with SPARQL query to execute against
                the journal. Either query_string or query_file must be
                provided, but not both.
            named_graphs  (optional): List of named graphs to query. The graphs
                should be specified in individual strings like
                ["urn://graph1", "urn://graph2"]. The default is to
                query all named graphs in the journal.

        Returns:
            The result of the query in a QueryResult object.
        """

        if not query_string and not query_file:
            raise ValueError(
                "Method query_journal requires either a query string "
                "or query file"
            )

        if query_string and query_file:
            raise ValueError(
                "Method query_journal received both a query string "
                "and a query file. Only one should be provided"
            )

        if not named_graphs:
            named_graphs = [ALL_NAMED_GRAPHS_URI]

        arb = AnzoRequestBuilder()
        arb.with_url(self.domain, self.port, self.path)
        arb.with_auth(self.username, self.password, self.auth_token)
        arb.with_timeout_seconds(self.timeout_seconds)
        arb.with_query_journal(named_graphs)

        if query_string:
            arb.with_query_string(query_string)
        elif query_file:
            arb.with_query_file(query_file)

        anzo_request = arb.build()
        response_text = anzo_request.execute_request()
        return QueryResult(response_text)

    def update_journal(self, query_string: str = "",
                       query_file: str = "") -> QueryResult:
        """Executes a SPARQL update query against the Anzo journal.

        The query must be conform the UPDATE query spec, as outlined in
        https://www.w3.org/TR/sparql11-update/.

        In summary, it's expected the query have one of the following clauses:
        INSERT, DELETE, INSERT DATA, DELETE DATA. Other clauses, which
        are outlined in the spec linked above, are supported but not
        as well tested.

        Args:
            query_string: (optional) SPARQL query string to execute against the
                journal. Either query_string or query_file must be provided,
                but not both.
            query_file: (optional) File with SPARQL update query to execute
                against the journal. Either query_string or query_file must be
                provided, but not both.

        Returns:
            The result of the query in a QueryResult object.
        """

        if not query_string and not query_file:
            raise ValueError(
                "Method query_journal requires either a query string "
                "or query file"
            )

        if query_string and query_file:
            raise ValueError(
                "Method query_journal received both a query string "
                "and a query file. Only one should be provided"
            )

        named_graphs = [ALL_NAMED_GRAPHS_URI]

        arb = AnzoRequestBuilder()
        arb.with_url(self.domain, self.port, self.path)
        arb.with_auth(self.username, self.password, self.auth_token)
        arb.with_timeout_seconds(self.timeout_seconds)
        arb.with_update_journal(named_graphs)

        if query_string:
            arb.with_update_string(query_string)
        elif query_file:
            arb.with_update_file(query_file)

        anzo_request = arb.build()
        response_text = anzo_request.execute_request()
        return QueryResult(response_text)

    def query_lds(self, lds_cat_entry: str, query_string: str = "",
                  query_file: str = "",
                  named_graphs: Optional[List[str]] = None
                  ) -> QueryResult:
        """Executes a SPARQL query against an Anzo linked dataset catalog entry

        Args:
            lds_cat_entry: URI of the linked dataset catalog entry to query.
                This URI will encode both the linked dataset and the associated
                volume datasource.
            query_string: (optional) SPARQL query string to execute against the
                lds_cat_entry. Either query_string or query_file must be
                provided, but not both.
            query_file: (optional) File with SPARQL query to execute against
                the lds_cat_entry. Either query_string or query_file must be
                provided, but not both.
            named_graphs  (optional): List of addiontal named graphs to query
                that are not already in the specified LDS. The graphs
                should be specified in individual strings like
                ["urn://graph1", "urn://graph2"].

        Returns:
            The result of the query in a QueryResult object.
        """

        if not query_string and not query_file:
            raise ValueError(
                "Method query_lds requires either a query string "
                "or query file"
            )

        arb = AnzoRequestBuilder()
        arb.with_url(self.domain, self.port, self.path)
        arb.with_auth(self.username, self.password, self.auth_token)
        arb.with_timeout_seconds(self.timeout_seconds)
        arb.with_lds_cat_entry(lds_cat_entry, named_graphs)

        if query_string:
            arb.with_query_string(query_string)
        elif query_file:
            arb.with_query_file(query_file)

        anzo_request = arb.build()
        response_text = anzo_request.execute_request()
        return QueryResult(response_text)

    def query_system_tables(self,
                            query_string: str = "",
                            query_file: str = "",
                            ) -> QueryResult:
        """Executes a SPARQL query against the anzo system tables

        Args:
            query_string: (optional) SPARQL query string to execute against the
                system tables. Either query_string or query_file must be
                provided, but not both.
            query_file: (optional) File with SPARQL query to execute against
                the system tables. Either query_string or query_file must be
                provided, but not both.

        Returns:
            The result of the query in a QueryResult object.
        """

        return self.query_lds(
            self.SYSTEM_TABLE_LDS_URI, query_string, query_file,
            named_graphs=[ALL_NAMED_GRAPHS_URI]
        )

    def execute_semantic_service(self,
                                 service_uri: str,
                                 request: QuadStore) -> QuadStore:
        """Executes a Semantic Service on Anzo

        Args:
            service_uri: URI of the semantic service
            request: The request payload as a quadstore

        Returns:
            A QuadStore object with the contents of the response from the
            semenatic service call
        """
        arb = AnzoRequestBuilder()
        arb.with_url(self.domain, self.port, self.path)
        arb.with_auth(self.username, self.password, self.auth_token)
        arb.with_timeout_seconds(self.timeout_seconds)
        arb.with_semantic_service(service_uri, request.as_anzo_json_list())
        anzo_request = arb.build()
        response_json = json.loads(anzo_request.execute_request())
        return QuadStore.from_anzo_json_list(response_json)

    def get(self, named_graph_uri: str,
            include_metadata_graph: bool = False) -> QuadStore:
        """Gets the contents of a named graph and optionally its
        metadata graph

        If the graph doesn't exist, then a ValueError is raised.

        Args:
            named_graph_uri: URI of the named graph to get
            include_metadata_graph (optional): If true, then the metadata graph
                is included in the returned QuadStore, and otherwise
                it's not included. The value is false by default.

        Returns:
            A QuadStore with the contents of the named graph and optionally
            its metadata graph.
        """

        arb = AnzoRequestBuilder()
        arb.with_url(self.domain, self.port, self.path)
        arb.with_auth(self.username, self.password, self.auth_token)
        arb.with_timeout_seconds(self.timeout_seconds)
        arb.with_get(named_graph_uri)
        anzo_request = arb.build()
        response_json = json.loads(anzo_request.execute_request())
        quad_store = QuadStore.from_anzo_json_list(response_json)

        if not include_metadata_graph:
            quad_store = quad_store.filter(graph=named_graph_uri)

        return quad_store

    def add(self,
            quad_store: Optional[QuadStore] = None,
            trig_filename: Optional[str] = None) -> None:
        """Adds the quads in the quad_store to the system journal

        If the named graph doesn't exist, then it is created and registered.

        Args:
            quad_store (optional): Set of quads to add to the
               Anzo system journal
            trig_filename (optional): The file path to a trig file to add to
                the Anzo system journal
        Raises:
            ValueError: Exactly one of quad_store and trig_filename must be specified
                  otherwise a ValueError is raised.
        """
        if not (quad_store or trig_filename):
            err = "Either quad_store or trig_filename must be specified"
            raise ValueError(err)

        if quad_store and trig_filename:
            err = "Cannot specify both quad_store and trig_filename"
            raise ValueError(err)

        arb = AnzoRequestBuilder()
        arb.with_url(self.domain, self.port, self.path)
        arb.with_auth(self.username, self.password, self.auth_token)
        arb.with_timeout_seconds(self.timeout_seconds)
        if trig_filename:
            quad_store = QuadStore.from_trig_file(trig_filename)
        arb.with_add(quad_store.as_anzo_json_list())
        anzo_request = arb.build()
        anzo_request.execute_request()

    def remove(self,
               quad_store: Optional[QuadStore] = None,
               trig_filename: Optional[str] = None) -> None:
        """Removes the quads in the quad_store to the system journal

        If some or all of the quads don't exist, an error is not raised.

        Args:
            quad_store: Set of quads to remove from the Anzo system journal
            trig_filename (optional): The file path to a trig file to remove from
                Anzo.
        Raises:
            ValueError: Exactly one of quad_store and trig_filename must be specified
        """
        if not (quad_store or trig_filename):
            err = "Either quad_store or trig_filename must be specified"
            raise ValueError(err)

        if quad_store and trig_filename:
            err = "Cannot specify both quad_store and trig_filename"
            raise ValueError(err)

        arb = AnzoRequestBuilder()
        arb.with_url(self.domain, self.port, self.path)
        arb.with_auth(self.username, self.password, self.auth_token)
        arb.with_timeout_seconds(self.timeout_seconds)
        if not quad_store:
            quad_store = QuadStore.from_trig_file(trig_filename)
        arb.with_remove(quad_store.as_anzo_json_list())
        anzo_request = arb.build()
        anzo_request.execute_request()
        
    ## Work around for SSL related DH Key errors
    # ex: [SSL: SSL_NEGATIVE_LENGTH] dh key too small (_ssl.c:600)
    def __ssl_config(self):
        import requests
        try:
            requests.packages.urllib3.util.ssl_.DEFAULT_CIPHERS += 'HIGH:!DH:!aNULL'
            requests.packages.urllib3.contrib.pyopenssl.DEFAULT_SSL_CIPHER_LIST += 'HIGH:!DH:!aNULL'
        except AttributeError:
            # no pyopenssl support used / needed / available
            pass
