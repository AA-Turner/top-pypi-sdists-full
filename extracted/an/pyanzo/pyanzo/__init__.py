"""Library for interacting with Anzo

PyAnzo is a python library for interacting with an AnzoServer

Usage::
    anzo_client = AnzoClient(server="localhost", port="443",
                             username="user", password="password")

    query = "SELECT * WHERE { ?s ?p ?o } LIMIT 10",
    graphmart = "urn://graphmart_uri"
    query_result = anzo_client.query_graphmart(graphmart, query_string=query)
    result_as_list = query_result.as_table_result.as_list()
"""

__author__ = """Cambridge Semantics"""
__email__ = ''
__version__ = '4.0.0'

from .anzo_client import AnzoClient
from .query_result import QueryResult, TableResult
from .anzo_request import AnzoRequestBuilder, AnzoRequest
from .quad_store import Quad, QuadStore, semantic_type_to_python_object
from .uris import ALL_NAMED_GRAPHS_URI, TYPE_PRED

__all__ = [
    'AnzoClient',
    'QueryResult',
    'TableResult',
    'AnzoRequest',
    'AnzoRequestBuilder',
    'LDSManager',
    'Quad',
    'QuadStore',
    'semantic_type_to_python_object',
    'ALL_NAMED_GRAPHS_URI',
    'TYPE_PRED',
]
