from unittest.mock import AsyncMock, patch

import pytest
from mistralai.client import models

from mistralai.workflows.plugins.mistralai.activities import (
    MistralEmbeddingsParams,
    mistralai_embeddings,
)

mock_response = models.EmbeddingResponse(
    id="embedding-123",
    object="embedding",
    model="mistral-embedding",
    data=[
        models.EmbeddingResponseData(
            index=0,
            embedding=[0.1, 0.2, 0.3],
        )
    ],
    usage=models.UsageInfo(prompt_tokens=10, total_tokens=10),
)

params = MistralEmbeddingsParams(model="mistral-embedding", inputs="Hello!")


class TestMistralEmbeddings:
    @pytest.mark.asyncio
    async def test_mistral_embeddings(self) -> None:
        with patch("mistralai.workflows.plugins.mistralai.utils._get_mistral_client") as mistral_cls:
            mock_mistral_instance = AsyncMock()
            mock_mistral_instance.embeddings.create_async.return_value = mock_response
            mock_mistral_instance.__aenter__.return_value = mock_mistral_instance
            mistral_cls.return_value = mock_mistral_instance

            result = await mistralai_embeddings(params)

            assert result.model_dump() == mock_response.model_dump()
            mock_mistral_instance.embeddings.create_async.assert_called_once_with(**params.model_dump(by_alias=True))
