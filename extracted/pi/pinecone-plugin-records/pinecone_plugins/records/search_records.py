from typing import Optional, Dict, Union, List

from pinecone_plugin_interface import PineconePlugin

from .db_data.core.client.api.vector_operations_api import VectorOperationsApi
from .db_data.core.client import ApiClient
from .db_data.core.client.models import (
    SearchRecordsRequest,
    SearchRecordsRequestQuery,
    SearchRecordsRequestRerank,
    SearchRecordsVector,
    SearchRecordsResponse,
    VectorValues,
)
from .models import SearchQuery, SearchRerank
from .version import API_VERSION


class SearchRecords(PineconePlugin):
    """
    The `SearchRecords` class adds functionality to the Pinecone SDK to allow searching for records.

    :param config: A `pinecone.config.Config` object, configured and built in the Pinecone class.
    :type config: `pinecone.config.Config`, required
    """

    def __init__(self, config, openapi_client_builder):
        self.config = config
        self.db_data_api = openapi_client_builder(
            ApiClient, VectorOperationsApi, API_VERSION
        )

    def __call__(
        self,
        namespace: str,
        query: Union[Dict, SearchQuery],
        rerank: Optional[Union[Dict, SearchRerank]] = None,
        fields: Optional[List[str]] = ["*"],  # Default to returning all fields
    ) -> SearchRecordsResponse:
        """
        Search for records.

        This operation converts a query to a vector embedding and then searches a namespace. You
        can optionally provide a reranking operation as part of the search.

        :param namespace: The namespace in the index to search.
        :type namespace: str, required
        :param query: The SearchQuery to use for the search.
        :type query: Union[Dict, SearchQuery], required
        :param rerank: The SearchRerank to use with the search request.
        :type rerank: Union[Dict, SearchRerank], optional
        :return: The records that match the search.
        :rtype: RecordModel
        """

        if not namespace:
            raise Exception("Namespace is required when searching records")

        # extract vector from query and convert to VectorValues
        query_dict = query.as_dict() if isinstance(query, SearchQuery) else query
        vector_dict = query_dict.pop("vector", None)

        rerank_dict = rerank.as_dict() if isinstance(rerank, SearchRerank) else rerank

        query = SearchRecordsRequestQuery(**query_dict)
        if vector_dict is not None:
            vector_values = None
            if "values" in vector_dict:
                vector_values = VectorValues(value=vector_dict.pop("values"))
            query.vector = SearchRecordsVector(**vector_dict, values=vector_values)

        request = SearchRecordsRequest(
            query=query,
            fields=fields,
        )
        if rerank_dict is not None:
            request.rerank = SearchRecordsRequestRerank(**rerank_dict)

        return self.db_data_api.search_records_namespace(namespace, request)
