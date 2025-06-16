from typing import Dict, List

from whiskerrag_types.interface.retriever_interface import BaseRetriever
from whiskerrag_types.model.retrieval import RetrievalChunk
from whiskerrag_utils.registry import RegisterTypeEnum, register


@register(RegisterTypeEnum.RETRIEVER, "similarity")
class SimpleRetriever(BaseRetriever):
    chunk_list: List[RetrievalChunk]
    chunk_index: Dict[str, RetrievalChunk]
    doc_index: Dict[str, RetrievalChunk]

    def __init__(self, chunk_list: List[RetrievalChunk]):
        self.chunk_list = chunk_list
        self.chunk_index = self._build_index()

    def _build_index(self) -> Dict[str, RetrievalChunk]:
        return {
            chunk.chunk_id: chunk
            for chunk in self.chunk_list
            if chunk.chunk_id is not None
        }
