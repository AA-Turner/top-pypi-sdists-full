from abc import ABC, abstractmethod
from ..helpers.env_helper import EnvHelper
from ..common.source_document import SourceDocument


class SearchHandlerBase(ABC):
    _VECTOR_FIELD = "content_vector"
    _IMAGE_VECTOR_FIELD = "image_vector"

    def __init__(self, env_helper: EnvHelper):
        self.env_helper = env_helper
        # Note: PostgreSQL implementation doesn't use search_client
        # self.search_client = self.create_search_client()

    def delete_from_index(self, blob_url) -> None:
        documents = self.search_by_blob_url(blob_url)
        if documents is None or len(documents) == 0:
            return
        files_to_delete = self.output_results(documents)
        self.delete_files(files_to_delete)

    @abstractmethod
    def perform_search(self, filename):
        pass

    @abstractmethod
    def process_results(self, results):
        pass

    @abstractmethod
    def get_files(self):
        """Get files from the search index."""
        pass

    @abstractmethod
    def output_results(self, results):
        pass

    @abstractmethod
    def delete_files(self, files):
        """Delete files from the search index.
        
        Args:
            files: List of files to delete.
        """
        pass

    @abstractmethod
    def query_search(self, question) -> list[SourceDocument]:
        """Search for documents based on a question.
        
        Args:
            question: The search question.
        """
        pass

    @abstractmethod
    def search_by_blob_url(self, blob_url):
        pass
