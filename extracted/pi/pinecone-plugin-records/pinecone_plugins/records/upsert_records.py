from typing import Optional, Dict, List
import json
from pinecone_plugin_interface import PineconePlugin

from .db_data.core.client.api.vector_operations_api import VectorOperationsApi
from .db_data.core.client import ApiClient
from .db_data.core.client.models import UpsertRecord
from .version import API_VERSION


class UpsertRecords(PineconePlugin):
    """
    The `UpsertRecords` class adds functionality to the Pinecone SDK to allow upserting records.\

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
        records: List[Dict],
    ):
        """
        Upsert records to a namespace.

        Converts records into embeddings and upserts them into a namespacce in the index.

        :param namespace: The namespace of the index to upsert records to.
        :type namespace: str, required
        :param records: The records to upsert into the index.
        :type records: List[Dict], required
        """
        if not namespace:
            raise Exception("Namespace is required when upserting records")
        if not records:
            raise Exception("No records provided")

        records_to_upsert = []
        for record in records:
            if not record.get("_id") and not record.get("id"):
                raise Exception("Each record must have an '_id' or 'id' value")

            records_to_upsert.append(
                UpsertRecord(
                    record.pop("_id", None) or record.pop("id", None), **(record)
                )
            )

        self.db_data_api.upsert_records_namespace(namespace, records_to_upsert)
