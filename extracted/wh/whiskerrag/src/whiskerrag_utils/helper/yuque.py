from typing import Dict, Iterator, List, Union

from langchain_community.document_loaders.yuque import YuqueLoader
from langchain_core.documents import Document


class ExtendedYuqueLoader(YuqueLoader):
    """Extended Yuque loader with additional API support."""

    def __init__(
        self,
        access_token: str,
        api_url: str = "https://www.yuque.com",
    ):
        super().__init__(access_token, api_url)

    @property
    def headers(self) -> Dict[str, str]:
        return {
            "Content-Type": "application/json",
            "X-Auth-Token": self.access_token,
        }

    def get_book_toc(self, group_login: str, book_slug: str) -> Dict:
        """Get table of contents for a book."""
        url = f"{self.api_url}/api/v2/repos/{group_login}/{book_slug}/toc"
        response = self.http_get(url=url)
        return response["data"]  # type: ignore

    def get_book_detail(self, group_login: str, book_slug: str) -> Dict:
        """Get detailed information about a book."""
        url = f"{self.api_url}/api/v2/repos/{group_login}/{book_slug}"
        response = self.http_get(url=url)
        return response["data"]  # type: ignore

    def get_doc_detail(
        self, group_login: str, book_slug: str, doc_id: Union[str, int]
    ) -> Dict:
        """Get detailed information about a document."""
        url = f"{self.api_url}/api/v2/repos/{group_login}/{book_slug}/docs/{doc_id}"
        response = self.http_get(url=url)
        return response["data"]  # type: ignore

    def parse_document(self, document: Dict) -> Document:
        """Parse document into Document format."""
        content = self.parse_document_body(document.get("body", ""))
        metadata = {
            "id": document.get("id"),
            "title": document.get("title"),
            "description": document.get("description"),
            "created_at": document.get("created_at"),
            "updated_at": document.get("updated_at"),
            "published_at": document.get("published_at"),
            "word_count": document.get("word_count"),
            "book_id": document.get("book_id"),
            "user_id": document.get("user_id"),
        }
        return Document(page_content=content, metadata=metadata)

    def get_book_documents_by_path(
        self, group_login: str, book_slug: str
    ) -> List[dict]:
        """get all documents from a specific book."""
        # Get book TOC
        toc = self.get_book_toc(group_login, book_slug)

        # Filter only DOC type entries
        doc_entries = [entry for entry in toc if entry["type"] == "DOC"]
        return doc_entries

    def load_book_by_path(self, group_login: str, book_slug: str) -> Iterator[Document]:
        """Load all documents from a specific book."""
        doc_entries = self.get_book_documents_by_path(group_login, book_slug)
        for entry in doc_entries:
            doc_id = entry["doc_id"]
            doc_detail = self.get_doc_detail(group_login, book_slug, doc_id)
            yield self.parse_document(doc_detail)

    def load_document_by_path(
        self, group_login: str, book_slug: str, document_id: Union[str, int]
    ) -> Document:
        """Load a specific document by its ID.

        Args:
            group_login: The group/user login name
            book_slug: The book identifier
            document_id: The specific document ID to load

        Returns:
            Iterator yielding a single Document object

        Yields:
            Document: The parsed document
        """
        try:
            # Get document detail directly using the API
            doc_detail = self.get_doc_detail(group_login, book_slug, document_id)
            return self.parse_document(doc_detail)

        except Exception as e:
            raise ValueError(f"Failed to load document {document_id}: {str(e)}")
