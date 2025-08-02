import json
from typing import List
import numpy as np

from .search_handler_base import SearchHandlerBase
from ..helpers.azure_postgres_helper import AzurePostgresHelper
from ..common.source_document import SourceDocument

from ...utilities.helpers.env_helper import EnvHelper
from mgmt_config import logger
env_helper: EnvHelper = EnvHelper()
log_execution = env_helper.LOG_EXECUTION
log_args = env_helper.LOG_ARGS
log_result = env_helper.LOG_RESULT


class AzurePostgresHandler(SearchHandlerBase):

    def __init__(self, env_helper):
        self.azure_postgres_helper = AzurePostgresHelper()
        super().__init__(env_helper)


    @logger.trace_function(log_execution=log_execution, log_args=False, log_result=False)
    def query_search(self, question) -> List[SourceDocument]:
        logger.info(f"Starting query search for question: {question}")
        user_input = question
        query_embedding = self.azure_postgres_helper.llm_helper.generate_embeddings(
            user_input
        )

        embedding_array = np.array(query_embedding).tolist()

        search_results = self.azure_postgres_helper.get_vector_store(
            embedding_array
        )

        source_documents = self._convert_to_source_documents(search_results)
        logger.info(f"Found {len(source_documents)} source documents.")
        return source_documents

    @logger.trace_function(log_execution=log_execution, log_args=False, log_result=False)
    def _convert_to_source_documents(self, search_results) -> List[SourceDocument]:
        source_documents = []
        for source in search_results:
            source_document = SourceDocument(
                id=source["id"],
                title=source["title"],
                chunk=source["chunk"],
                offset=source["offset"],
                page_number=source["page_number"],
                content=source["content"],
                source=source["source"],
            )
            source_documents.append(source_document)
        return source_documents


    # Note: create_search_client method removed - PostgreSQL implementation doesn't use Azure Search client


    @logger.trace_function(log_execution=log_execution, log_args=False, log_result=False)
    def create_vector_store(self, documents_to_upload):
        logger.info(
            f"Creating vector store with {len(documents_to_upload)} documents."
        )
        return self.azure_postgres_helper.create_vector_store(documents_to_upload)

    @logger.trace_function(log_execution=log_execution, log_args=log_args, log_result=False)
    def perform_search(self, filename):
        logger.info(f"Performing search for filename: {filename}")
        return self.azure_postgres_helper.perform_search(filename)

    @logger.trace_function(log_execution=log_execution, log_args=False, log_result=False)
    def process_results(self, results):
        if results is None:
            logger.info("No results to process.")
            return []
        data = [
            [json.loads(result["metadata"]).get("chunk", i), result["content"]]
            for i, result in enumerate(results)
        ]
        logger.info(f"Processed {len(data)} results.")
        return data

    @logger.trace_function(log_execution=log_execution, log_args=log_args, log_result=False)
    def get_files(self):
        results = self.azure_postgres_helper.get_files()
        if results is None or len(results) == 0:
            logger.info("No files found.")
            return []
        logger.info(f"Found {len(results)} files.")
        return results


    @logger.trace_function(log_execution=log_execution, log_args=False, log_result=False)
    def output_results(self, results):
        files = {}
        for result in results:
            id = result["id"]
            filename = result["title"]
            if filename in files:
                files[filename].append(id)
            else:
                files[filename] = [id]

        return files


    @logger.trace_function(log_execution=log_execution, log_args=log_args, log_result=log_result)
    def delete_files(self, files):
        ids_to_delete = []
        files_to_delete = []

        for filename, ids in files.items():
            files_to_delete.append(filename)
            ids_to_delete += [{"id": id} for id in ids]
        self.azure_postgres_helper.delete_documents(ids_to_delete)

        return ", ".join(files_to_delete)

    @logger.trace_function(log_execution=log_execution, log_args=log_args, log_result=False)
    def search_by_blob_url(self, blob_url):
        logger.info(f"Searching by blob URL: {blob_url}")
        return self.azure_postgres_helper.search_by_blob_url(blob_url)

    @logger.trace_function(log_execution=log_execution, log_args=log_args, log_result=log_result)
    def delete_from_index(self, blob_url) -> None:
        logger.info(f"Deleting from index for blob URL: {blob_url}")
        documents = self.search_by_blob_url(blob_url)
        if documents is None or len(documents) == 0:
            logger.info("No documents found for blob URL.")
            return
        files_to_delete = self.output_results(documents)
        self.delete_files(files_to_delete)

    @logger.trace_function(log_execution=log_execution, log_args=log_args, log_result=log_result)
    def get_unique_files(self):
        results = self.azure_postgres_helper.get_unique_files()
        unique_titles = [row["title"] for row in results]
        return unique_titles
