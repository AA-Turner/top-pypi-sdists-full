"""
Example: Custom Operator

This is a complete example showing how to create a custom Operator and use it in an Agent.
"""
import logging
from typing import Dict, Any

from dslighting.operators import Operator
from dslighting.services import LLMService

logger = logging.getLogger(__name__)


class TextAnalysisOperator(Operator):
    """
    Text analysis operator - example.

    Uses an LLM to analyze text.
    """

    def __init__(
        self,
        llm_service: LLMService,
        analysis_type: str = "sentiment",
        **kwargs
    ):
        """
        Initialize.

        Args:
            llm_service: LLM service.
            analysis_type: Analysis type (sentiment, keywords, summary).
        """
        super().__init__(name="TextAnalysisOperator", **kwargs)
        self.llm_service = llm_service
        self.analysis_type = analysis_type

    async def __call__(
        self,
        text: str,
        custom_instruction: str = ""
    ) -> Dict[str, Any]:
        """
        Analyze text.

        Args:
            text: Text to analyze.
            custom_instruction: Optional custom instruction.

        Returns:
            Analysis result dict.
        """
        logger.info(f"[{self.name}] Analyzing text (type: {self.analysis_type})")

        # Build prompt.
        if self.analysis_type == "sentiment":
            prompt = f"""
Please analyze the sentiment of the following text.
Respond with a JSON object containing:
- sentiment: "positive", "negative", or "neutral"
- confidence: a number between 0 and 1
- key_points: list of key points

Text:
{text}
"""
        elif self.analysis_type == "keywords":
            prompt = f"""
Please extract the main keywords from the following text.
Respond with a JSON object containing:
- keywords: list of keywords
- topics: list of main topics

Text:
{text}
"""
        elif self.analysis_type == "summary":
            prompt = f"""
Please provide a concise summary of the following text.
Respond with a JSON object containing:
- summary: the summary text
- word_count: number of words in summary

Text:
{text}
"""
        else:
            raise ValueError(f"Unknown analysis type: {self.analysis_type}")

        # Add custom instruction.
        if custom_instruction:
            prompt += f"\n\nAdditional instruction:\n{custom_instruction}"

        # Call LLM.
        try:
            response = await self.llm_service.call(prompt)
            logger.info(f"[{self.name}] Analysis completed")

            return {
                "analysis_type": self.analysis_type,
                "raw_response": response,
                "text_length": len(text),
            }

        except Exception as e:
            logger.error(f"[{self.name}] Analysis failed: {e}")
            raise


# Also exported in custom/__init__.py
# from .example_operator import TextAnalysisOperator
