from typing import List
import re
import requests
from bs4 import BeautifulSoup
from .document_loading_base import DocumentLoadingBase
from ..common.source_document import SourceDocument
from mgmt_config import logger
from ...utilities.helpers.env_helper import EnvHelper
env_helper: EnvHelper = EnvHelper()
log_execution = env_helper.LOG_EXECUTION
log_args = env_helper.LOG_ARGS
log_result = env_helper.LOG_RESULT

class SimpleWebDocument:
    """Simple document class to replace LangChain's Document."""
    def __init__(self, page_content: str, metadata: dict):
        self.page_content = page_content
        self.metadata = metadata


class SimpleWebLoader:
    """Simple web loader to replace LangChain's WebBaseLoader."""
    
    def __init__(self, url: str):
        self.url = url
    
    @logger.trace_function(log_execution=log_execution, log_args=False, log_result=False)
    def load(self) -> List[SimpleWebDocument]:
        """Load web content from URL."""
        try:
            # Fetch the webpage
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(self.url, headers=headers, timeout=30)
            response.raise_for_status()
            
            # Parse HTML content
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Remove script and style elements
            for script in soup(["script", "style"]):
                script.decompose()
            
            # Get text content
            text = soup.get_text()
            
            # Clean up text
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = ' '.join(chunk for chunk in chunks if chunk)
            
            return [SimpleWebDocument(
                page_content=text,
                metadata={"source": self.url}
            )]
        
        except Exception as e:
            # Return empty content if loading fails
            return [SimpleWebDocument(
                page_content="",
                metadata={"source": self.url, "error": str(e)}
            )]


class WebDocumentLoading(DocumentLoadingBase):
    def __init__(self) -> None:
        super().__init__()

    @logger.trace_function(log_execution=log_execution, log_args=False, log_result=False)
    def load(self, document_url: str) -> List[SourceDocument]:
        loader = SimpleWebLoader(document_url)
        documents = loader.load()
        
        for document in documents:
            document.page_content = re.sub("\n{3,}", "\n\n", document.page_content)
            # Remove half non-ascii character from start/end of doc content
            pattern = re.compile(
                r"[\x00-\x1f\x7f\u0080-\u00a0\u2000-\u3000\ufff0-\uffff]"
            )
            document.page_content = re.sub(pattern, "", document.page_content)
            if document.page_content == "":
                documents.remove(document)
        
        source_documents: List[SourceDocument] = [
            SourceDocument(
                content=document.page_content,
                source=document.metadata["source"],
            )
            for document in documents
        ]
        return source_documents
