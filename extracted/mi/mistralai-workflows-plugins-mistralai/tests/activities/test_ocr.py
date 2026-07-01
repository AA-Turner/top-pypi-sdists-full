from unittest.mock import AsyncMock, patch

import pytest
from mistralai.client import models
from mistralai.client.models import OCRRequest

from mistralai.workflows.plugins.mistralai.activities import mistralai_ocr

mock_response = models.OCRResponse(
    pages=[
        models.OCRPageObject(
            index=0,
            markdown="Hello! How can I help you?",
            images=[],
            dimensions=None,
        )
    ],
    model="mistral-ocr",
    usage_info=models.OCRUsageInfo(
        pages_processed=1,
    ),
)

params = OCRRequest(
    model="mistral-ocr",
    document=models.ImageURLChunk(image_url=models.ImageURL(url="https://example.com/image.png")),
)


class TestMistralOCR:
    @pytest.mark.asyncio
    async def test_mistral_ocr(self) -> None:
        with patch("mistralai.workflows.plugins.mistralai.utils._get_mistral_client") as mistral_cls:
            mock_mistral_instance = AsyncMock()
            mock_mistral_instance.ocr.process_async.return_value = mock_response
            mock_mistral_instance.__aenter__.return_value = mock_mistral_instance
            mistral_cls.return_value = mock_mistral_instance

            result = await mistralai_ocr(params)

            assert result == mock_response
            mock_mistral_instance.ocr.process_async.assert_called_once_with(**params.model_dump(by_alias=True))
