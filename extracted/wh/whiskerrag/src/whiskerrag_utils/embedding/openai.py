import os
from typing import List, Optional

from langchain_openai import OpenAIEmbeddings

from whiskerrag_types.interface.embed_interface import BaseEmbedding, Image
from whiskerrag_types.model.knowledge import EmbeddingModelEnum
from whiskerrag_utils import RegisterTypeEnum, register


@register(RegisterTypeEnum.EMBEDDING, EmbeddingModelEnum.OPENAI)
class OpenAIEmbedding(BaseEmbedding):
    @classmethod
    async def health_check(cls) -> bool:
        try:
            if not os.getenv("OPENAI_API_KEY"):
                raise EnvironmentError(
                    "OPENAI_API_KEY is not set in the environment variables"
                )
            return True
        except Exception as e:
            print(f"OpenAIEmbedding health check failed: {e}")
            return False

    async def embed_text(self, text: str, timeout: Optional[int]) -> List[float]:
        embedding_client = OpenAIEmbeddings(timeout=timeout or 15)
        embedding = embedding_client.embed_query(text)
        return embedding

    async def embed_text_query(self, text: str, timeout: Optional[int]) -> List[float]:
        return await self.embed_text(text, timeout)

    async def embed_image(self, image: Image, timeout: Optional[int]) -> List[float]:
        raise NotImplementedError("OpenAI does not support image embedding")
        return []
