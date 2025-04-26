from enum import Enum
from typing import Dict, Any

from openapi_client import ProtoLLMDocument


class DocumentParserType(Enum):
    OPENPARSE = "openparse"
    RAGFLOW = "ragflow"


class DocumentChunkingType(Enum):
    CHARACTER_SPLITTING = "character_splitting"
    FIXED_SIZE = "fixed_size"
    NAIVE_SPLITTING = "naive_splitting"
    NLTK = "nltk"
    SPACY = "spacy"


class Document:
    def __init__(self, document: ProtoLLMDocument):
        self.id: int = document.id
        self.filename: str = document.filename
        self.extension: str = document.extension
        self.size: str = document.size

        try:
            self.parser_type: DocumentParserType = DocumentParserType(document.parser_type)
        except ValueError:
            raise ValueError(f"Invalid parser_type: {document.parser_type}")

        try:
            self.chunking_type: DocumentChunkingType = DocumentChunkingType(document.chunking_type)
        except ValueError:
            raise ValueError(f"Invalid chunking_type: {document.chunking_type}")

        self.chunking_method_params: Dict[str, Any] = document.chunking_method_params
