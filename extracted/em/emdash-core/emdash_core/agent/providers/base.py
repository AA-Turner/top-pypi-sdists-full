"""Base classes for LLM providers."""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Optional, Union


@dataclass
class ToolCall:
    """Represents a tool call from the LLM."""

    id: str
    name: str
    arguments: str  # JSON string of arguments


@dataclass
class ImageContent:
    """Represents an image for vision-capable models."""

    image_data: bytes  # Raw image bytes
    format: str = "png"  # Image format (png, jpeg, gif)

    @property
    def base64_url(self) -> str:
        """Get base64 data URL for the image."""
        import base64
        encoded = base64.b64encode(self.image_data).decode("utf-8")
        return f"data:image/{self.format};base64,{encoded}"


@dataclass
class LLMResponse:
    """Unified response from any LLM provider."""

    content: Optional[str] = None
    thinking: Optional[str] = None  # Model's chain-of-thought reasoning
    tool_calls: list[ToolCall] = field(default_factory=list)
    raw: Any = None  # Original provider response
    stop_reason: Optional[str] = None
    input_tokens: int = 0  # Tokens in the request
    output_tokens: int = 0  # Tokens in the response
    thinking_tokens: int = 0  # Tokens used for thinking (if available)

    def to_dict(self, model: str | None = None) -> dict[str, Any]:
        """Serialize to dict for events (excludes raw provider response).
        
        Args:
            model: Optional model string for cost calculation
            
        Returns:
            Dict with token counts and optional cost
        """
        from .models import calculate_cost
        
        result = {
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "thinking_tokens": self.thinking_tokens,
            "stop_reason": self.stop_reason,
        }
        
        if model:
            result["cost"] = calculate_cost(
                self.input_tokens,
                self.output_tokens,
                model,
                self.thinking_tokens,
            )
        
        return result


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    def __init__(self, model: str):
        self.model = model

    @abstractmethod
    def chat(
        self,
        messages: list[dict],
        tools: Optional[list[dict]] = None,
        system: Optional[str] = None,
        reasoning: bool = False,
        thinking: bool = False,
        images: Optional[list[ImageContent]] = None,
    ) -> LLMResponse:
        """Send a chat completion request.

        Args:
            messages: List of message dicts with 'role' and 'content'
            tools: Optional list of tool schemas
            system: Optional system prompt (will be prepended or handled per provider)
            reasoning: Enable reasoning mode (for models that support it)
            thinking: Enable extended thinking (for models that support it)
            images: Optional list of images for vision-capable models

        Returns:
            LLMResponse with content and/or tool calls
        """
        pass

    @abstractmethod
    def get_context_limit(self) -> int:
        """Get the context window size for this model."""
        pass

    @abstractmethod
    def get_max_image_size(self) -> int:
        """Get maximum image size in bytes for this model."""
        return 5 * 1024 * 1024  # Default 5MB

    @abstractmethod
    def supports_vision(self) -> bool:
        """Check if this model supports image input."""
        return False

    @abstractmethod
    def format_tool_result(self, tool_call_id: str, result: str) -> dict:
        """Format a tool result message for this provider.

        Args:
            tool_call_id: ID of the tool call being responded to
            result: JSON string result from the tool

        Returns:
            Message dict in provider's expected format
        """
        pass

    @abstractmethod
    def format_assistant_message(self, response: LLMResponse) -> dict:
        """Format an assistant response to add back to messages.

        Args:
            response: The LLMResponse from a chat call

        Returns:
            Message dict in provider's expected format
        """
        pass

    def format_content_with_images(
        self,
        text: str,
        images: Optional[list[ImageContent]] = None
    ) -> Union[str, list[dict]]:
        """Format message content with optional images.

        For vision models, returns a list of content blocks.
        For non-vision models, returns text only (images stripped).

        Args:
            text: Text content
            images: Optional list of images

        Returns:
            Content formatted for this provider
        """
        if not images:
            return text

        if self.supports_vision():
            content = [{"type": "text", "text": text}]
            for img in images:
                content.append({
                    "type": "image_url",
                    "image_url": {"url": img.base64_url}
                })
            return content

        # Non-vision model: strip images, warn
        return text
