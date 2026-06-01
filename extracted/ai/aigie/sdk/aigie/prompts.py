"""
Prompt Management for Aigie SDK.

Provides prompt template management with:
- Version control and history
- A/B testing support
- Chat prompt support (OpenAI format)
- Variable interpolation with {{variable}} syntax
- Production deployment tracking
- LangChain integration
"""

import builtins
import hashlib
import json
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

logger = logging.getLogger(__name__)


class PromptFormat(Enum):
    """Supported prompt formats."""

    TEXT = "text"
    CHAT = "chat"


@dataclass
class PromptVersion:
    """A specific version of a prompt template."""

    version: int
    template: str | list[dict[str, str]]
    format: PromptFormat
    variables: list[str]
    created_at: datetime
    config: dict[str, Any] | None = None
    is_active: bool = False
    labels: list[str] = field(default_factory=list)

    @property
    def hash(self) -> str:
        """Generate hash of prompt content for change detection."""
        if isinstance(self.template, str):
            content_str = self.template
        else:
            content_str = json.dumps(self.template, sort_keys=True)
        return hashlib.sha256(content_str.encode()).hexdigest()[:12]


@dataclass
class Prompt:
    """
    Represents a prompt template with versioning.

    Supports both text prompts and chat prompts (OpenAI format).

    Usage:
        # Text prompt
        prompt = Prompt(
            name="customer_support",
            template="You are a helpful assistant. Customer: {{customer_name}}",
            version="1.0"
        )
        rendered = prompt.render(customer_name="John")

        # Chat prompt
        chat_prompt = Prompt.chat(
            name="research_agent",
            messages=[
                {"role": "system", "content": "You are a research assistant."},
                {"role": "user", "content": "Research: {{query}}"}
            ],
            config={"temperature": 0.7}
        )
        messages = chat_prompt.render(query="AI trends")
    """

    name: str
    template: str | list[dict[str, str]]
    version: str = "1.0"
    format: PromptFormat = PromptFormat.TEXT
    config: dict[str, Any] | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    tags: list[str] = field(default_factory=list)
    labels: list[str] = field(default_factory=list)
    id: str | None = None
    created_at: datetime | None = None
    versions: list[PromptVersion] = field(default_factory=list)

    def __post_init__(self):
        """Extract variables from template."""
        self.variables = self._extract_variables(self.template)
        self.created_at = self.created_at or datetime.utcnow()

        # Determine format if not set
        if isinstance(self.template, list):
            self.format = PromptFormat.CHAT

    @classmethod
    def text(
        cls,
        name: str,
        template: str,
        version: str = "1.0",
        config: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
        tags: list[str] | None = None,
        labels: list[str] | None = None,
    ) -> "Prompt":
        """Create a text prompt template."""
        return cls(
            name=name,
            template=template,
            version=version,
            format=PromptFormat.TEXT,
            config=config,
            metadata=metadata or {},
            tags=tags or [],
            labels=labels or [],
        )

    @classmethod
    def chat(
        cls,
        name: str,
        messages: list[dict[str, str]],
        version: str = "1.0",
        config: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
        tags: list[str] | None = None,
        labels: list[str] | None = None,
    ) -> "Prompt":
        """
        Create a chat prompt template (OpenAI format).

        Args:
            name: Template name
            messages: List of message dicts with 'role' and 'content' keys
            version: Version string
            config: Optional model config (temperature, max_tokens, etc.)
            metadata: Optional metadata
            tags: Optional tags
            labels: Optional labels (e.g., ["production", "v2"])

        Example:
            prompt = Prompt.chat(
                name="research_agent",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "Help me with: {{query}}"}
                ],
                config={"temperature": 0.7, "max_tokens": 1000}
            )
        """
        return cls(
            name=name,
            template=messages,
            version=version,
            format=PromptFormat.CHAT,
            config=config,
            metadata=metadata or {},
            tags=tags or [],
            labels=labels or [],
        )

    def _extract_variables(self, template: str | list[dict[str, str]]) -> list[str]:
        """Extract variable names from template content."""
        if isinstance(template, str):
            # Match {{variable}} or {variable} patterns
            pattern = r"\{\{?\s*(\w+)\s*\}?\}"
            return list(set(re.findall(pattern, template)))
        if isinstance(template, list):
            # Extract from all message contents
            all_vars = []
            for msg in template:
                if isinstance(msg, dict) and "content" in msg:
                    pattern = r"\{\{?\s*(\w+)\s*\}?\}"
                    all_vars.extend(re.findall(pattern, msg["content"]))
            return list(set(all_vars))
        return []

    def render(self, **kwargs) -> str | list[dict[str, str]]:
        """
        Render the prompt template with provided variables.

        Args:
            **kwargs: Variables to substitute in template

        Returns:
            Rendered prompt string or messages list

        Raises:
            ValueError: If required variables are missing
        """
        # Validate all required variables are provided
        missing = set(self.variables) - set(kwargs.keys())
        if missing:
            raise ValueError(f"Missing required variables: {missing}")

        if isinstance(self.template, str):
            result = self.template
            for var, value in kwargs.items():
                # Replace both {{var}} and {var} patterns
                result = re.sub(rf"\{{\{{\s*{var}\s*\}}\}}|\{{\s*{var}\s*\}}", str(value), result)
            return result

        if isinstance(self.template, list):
            compiled_messages = []
            for msg in self.template:
                if isinstance(msg, dict):
                    compiled_msg = msg.copy()
                    if "content" in compiled_msg:
                        content = compiled_msg["content"]
                        for var, value in kwargs.items():
                            content = re.sub(
                                rf"\{{\{{\s*{var}\s*\}}\}}|\{{\s*{var}\s*\}}", str(value), content
                            )
                        compiled_msg["content"] = content
                    compiled_messages.append(compiled_msg)
            return compiled_messages

        return self.template

    def to_langchain_messages(self, **kwargs):
        """
        Convert to LangChain message objects.

        Args:
            **kwargs: Variables to substitute

        Returns:
            List of LangChain message objects
        """
        try:
            from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
        except ImportError:
            raise ImportError("LangChain not installed. Run: pip install langchain-core")

        if self.format != PromptFormat.CHAT:
            # Convert text to single HumanMessage
            return [HumanMessage(content=self.render(**kwargs))]

        messages = self.render(**kwargs)
        lc_messages = []
        for msg in messages:
            role = msg.get("role", "user").lower()
            content = msg.get("content", "")

            if role == "system":
                lc_messages.append(SystemMessage(content=content))
            elif role in {"assistant", "ai"}:
                lc_messages.append(AIMessage(content=content))
            else:  # user, human, etc.
                lc_messages.append(HumanMessage(content=content))

        return lc_messages

    def to_dict(self) -> dict[str, Any]:
        """Convert prompt to dictionary."""
        return {
            "name": self.name,
            "template": self.template,
            "version": self.version,
            "format": self.format.value,
            "config": self.config,
            "metadata": self.metadata,
            "tags": self.tags,
            "labels": self.labels,
            "variables": self.variables,
            "id": self.id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Prompt":
        """Create prompt from dictionary."""
        created_at = None
        if data.get("created_at"):
            created_at = datetime.fromisoformat(data["created_at"])

        format_str = data.get("format", "text")
        try:
            prompt_format = PromptFormat(format_str)
        except ValueError:
            prompt_format = PromptFormat.TEXT

        return cls(
            name=data["name"],
            template=data["template"],
            version=data.get("version", "1.0"),
            format=prompt_format,
            config=data.get("config"),
            metadata=data.get("metadata", {}),
            tags=data.get("tags", []),
            labels=data.get("labels", []),
            id=data.get("id"),
            created_at=created_at,
        )

    @property
    def hash(self) -> str:
        """Generate hash of prompt content for change detection."""
        if isinstance(self.template, str):
            content_str = self.template
        else:
            content_str = json.dumps(self.template, sort_keys=True)
        return hashlib.sha256(content_str.encode()).hexdigest()[:12]


class PromptManager:
    """
    Manages prompts for Aigie SDK.

    Provides:
    - Prompt creation and versioning
    - A/B testing support
    - Production/staging labels
    - Platform sync
    - LangChain integration

    Usage:
        manager = PromptManager(aigie_client)

        # Create a text prompt
        prompt = await manager.create(
            name="customer_support",
            template="You are a helpful assistant. Customer: {{customer_name}}",
            version="1.0"
        )

        # Create a chat prompt
        chat_prompt = await manager.create_chat(
            name="research_agent",
            messages=[
                {"role": "system", "content": "You are a research assistant."},
                {"role": "user", "content": "Research: {{query}}"}
            ],
            config={"temperature": 0.7}
        )

        # Use in trace
        async with aigie.trace("support") as trace:
            rendered = prompt.render(customer_name="John")
            trace.set_prompt(prompt)
    """

    def __init__(self, aigie_client=None):
        """
        Initialize prompt manager.

        Args:
            aigie_client: Optional Aigie client instance
        """
        self.aigie = aigie_client
        self._local_prompts: dict[str, Prompt] = {}  # Cache for local prompts
        self._labels_index: dict[str, list[str]] = {}  # label -> [prompt_keys]

    async def create(
        self,
        name: str,
        template: str | list[dict[str, str]],
        version: str = "1.0",
        config: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
        tags: list[str] | None = None,
        labels: list[str] | None = None,
    ) -> Prompt:
        """
        Create a new prompt.

        Args:
            name: Prompt name
            template: Prompt template string or messages list
            version: Prompt version
            config: Optional model config (temperature, max_tokens, etc.)
            metadata: Optional metadata
            tags: Optional tags
            labels: Optional labels (e.g., ["production", "v2"])

        Returns:
            Prompt object
        """
        prompt = Prompt(
            name=name,
            template=template,
            version=version,
            config=config,
            metadata=metadata or {},
            tags=tags or [],
            labels=labels or [],
        )

        # Store locally
        key = self._get_prompt_key(prompt)
        self._local_prompts[key] = prompt

        # Update labels index
        for label in labels or []:
            if label not in self._labels_index:
                self._labels_index[label] = []
            if key not in self._labels_index[label]:
                self._labels_index[label].append(key)

        return prompt

    async def create_chat(
        self,
        name: str,
        messages: list[dict[str, str]],
        version: str = "1.0",
        config: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
        tags: list[str] | None = None,
        labels: list[str] | None = None,
    ) -> Prompt:
        """
        Create a chat prompt (convenience method).

        Args:
            name: Prompt name
            messages: List of message dicts with 'role' and 'content' keys
            version: Prompt version
            config: Optional model config (temperature, max_tokens, etc.)
            metadata: Optional metadata
            tags: Optional tags
            labels: Optional labels

        Returns:
            Prompt object
        """
        return await self.create(
            name=name,
            template=messages,
            version=version,
            config=config,
            metadata=metadata,
            tags=tags,
            labels=labels,
        )

    def register(self, prompt: Prompt) -> None:
        """Register a prompt in the manager."""
        key = self._get_prompt_key(prompt)
        self._local_prompts[key] = prompt

        # Update labels index
        for label in prompt.labels:
            if label not in self._labels_index:
                self._labels_index[label] = []
            if key not in self._labels_index[label]:
                self._labels_index[label].append(key)

    async def get(
        self, name: str, version: str | None = None, label: str | None = None
    ) -> Prompt | None:
        """
        Get a prompt by name and version or label.

        Args:
            name: Prompt name
            version: Optional version (defaults to latest)
            label: Optional label to filter by (e.g., "production")

        Returns:
            Prompt if found, None otherwise
        """
        if version:
            key = f"{name}:{version}"
            return self._local_prompts.get(key)

        # If label specified, find prompt with that label
        if label and label in self._labels_index:
            for key in self._labels_index[label]:
                prompt = self._local_prompts.get(key)
                if prompt and prompt.name == name:
                    return prompt

        # Find latest version
        matching = [p for k, p in self._local_prompts.items() if k.startswith(f"{name}:")]
        if not matching:
            return None

        # Sort by version and return latest
        matching.sort(key=lambda p: p.version, reverse=True)
        return matching[0]

    def get_production(self, name: str) -> Prompt | None:
        """Get production-labeled prompt by name (sync convenience method)."""
        if "production" in self._labels_index:
            for key in self._labels_index["production"]:
                prompt = self._local_prompts.get(key)
                if prompt and prompt.name == name:
                    return prompt
        return None

    async def list(self, name: str | None = None, label: str | None = None) -> list[Prompt]:
        """
        List prompts.

        Args:
            name: Optional name filter
            label: Optional label filter

        Returns:
            List of prompts
        """
        prompts = list(self._local_prompts.values())

        if name:
            prompts = [p for p in prompts if p.name == name]

        if label:
            label_keys = self._labels_index.get(label, [])
            prompts = [p for p in prompts if self._get_prompt_key(p) in label_keys]

        return prompts

    async def push_to_platform(self) -> dict[str, bool]:
        """
        Push all registered prompts to the Aigie platform.

        Returns:
            Dict mapping prompt keys to success status
        """
        if not self.aigie:
            logger.warning("No Aigie client - cannot push to platform")
            return {}

        results = {}
        for key, _prompt in self._local_prompts.items():
            try:
                # TODO: Implement actual API call when backend supports it
                # await self.aigie.create_prompt(prompt)
                results[key] = True
            except Exception as e:
                logger.error(f"Failed to push prompt {key}: {e}")
                results[key] = False
        return results

    async def pull_from_platform(self, names: builtins.list[str] | None = None) -> int:
        """
        Pull prompts from the Aigie platform.

        Args:
            names: Optional list of prompt names to pull (all if None)

        Returns:
            Number of prompts pulled
        """
        if not self.aigie:
            logger.warning("No Aigie client - cannot pull from platform")
            return 0

        # TODO: Implement actual API call when backend supports it
        # prompts = await self.aigie.list_prompts(names=names)
        # for prompt_data in prompts:
        #     prompt = Prompt.from_dict(prompt_data)
        #     self.register(prompt)
        return 0

    def _get_prompt_key(self, prompt: Prompt) -> str:
        """Get cache key for prompt."""
        return f"{prompt.name}:{prompt.version}"


# Global prompt manager instance
_global_manager: PromptManager | None = None


def get_prompt_manager(aigie_client=None) -> PromptManager:
    """Get the global prompt manager."""
    global _global_manager
    if _global_manager is None:
        _global_manager = PromptManager(aigie_client)
    elif aigie_client and not _global_manager.aigie:
        _global_manager.aigie = aigie_client
    return _global_manager


def register_prompt(prompt: Prompt) -> None:
    """Register a prompt in the global manager."""
    get_prompt_manager().register(prompt)


def get_prompt(name: str, version: str | None = None) -> Prompt | None:
    """Get a prompt from the global manager (sync)."""
    manager = get_prompt_manager()
    if version:
        return manager._local_prompts.get(f"{name}:{version}")

    # Find latest version
    matching = [p for k, p in manager._local_prompts.items() if k.startswith(f"{name}:")]
    if not matching:
        return None
    matching.sort(key=lambda p: p.version, reverse=True)
    return matching[0]


# Convenience aliases
TextPrompt = Prompt.text
ChatPrompt = Prompt.chat
