"""
Prompt Registry and Versioning.

Provides prompt management with version control, templates, and variables.
"""

import builtins
import hashlib
import json
import logging
import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

logger = logging.getLogger(__name__)


@dataclass
class PromptVersion:
    """A specific version of a prompt.

    Attributes:
        version: Version string (semantic versioning, e.g., "1.0.0")
        template: The prompt template string
        variables: List of variable names used in the template
        created_at: When this version was created
        description: Optional description of changes
        metadata: Additional metadata
        hash: Content hash for detecting changes
    """

    version: str
    template: str
    variables: list[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    description: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    hash: str = field(default="")

    def __post_init__(self):
        # Extract variables from template if not provided
        if not self.variables:
            self.variables = self._extract_variables(self.template)
        # Generate content hash
        if not self.hash:
            self.hash = self._generate_hash()

    def _extract_variables(self, template: str) -> list[str]:
        """Extract variable names from template."""
        # Match {variable_name} patterns
        pattern = r"\{(\w+)\}"
        matches = re.findall(pattern, template)
        # Remove duplicates while preserving order
        seen = set()
        return [v for v in matches if not (v in seen or seen.add(v))]

    def _generate_hash(self) -> str:
        """Generate a hash of the template content."""
        content = self.template.encode("utf-8")
        return hashlib.sha256(content).hexdigest()[:12]

    def render(self, **kwargs) -> str:
        """
        Render the template with provided variables.

        Args:
            **kwargs: Variable values to substitute

        Returns:
            Rendered prompt string

        Raises:
            KeyError: If a required variable is missing
        """
        # Check for missing variables
        missing = [v for v in self.variables if v not in kwargs]
        if missing:
            raise KeyError(f"Missing required variables: {missing}")

        # Substitute variables
        result = self.template
        for key, value in kwargs.items():
            result = result.replace(f"{{{key}}}", str(value))
        return result

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "version": self.version,
            "template": self.template,
            "variables": self.variables,
            "created_at": self.created_at.isoformat(),
            "description": self.description,
            "metadata": self.metadata,
            "hash": self.hash,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PromptVersion":
        """Create from dictionary."""
        created_at = data.get("created_at")
        if isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        elif created_at is None:
            created_at = datetime.now()

        return cls(
            version=data["version"],
            template=data["template"],
            variables=data.get("variables", []),
            created_at=created_at,
            description=data.get("description"),
            metadata=data.get("metadata", {}),
            hash=data.get("hash", ""),
        )


@dataclass
class PromptTemplate:
    """A prompt template with version history.

    Attributes:
        name: Unique name for the prompt
        description: Description of the prompt's purpose
        versions: List of all versions (newest first)
        tags: Tags for categorization
        metadata: Additional metadata
    """

    name: str
    description: str | None = None
    versions: list[PromptVersion] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def latest(self) -> PromptVersion | None:
        """Get the latest version."""
        return self.versions[0] if self.versions else None

    @property
    def latest_version(self) -> str | None:
        """Get the latest version string."""
        return self.versions[0].version if self.versions else None

    def get_version(self, version: str) -> PromptVersion | None:
        """Get a specific version."""
        for v in self.versions:
            if v.version == version:
                return v
        return None

    def add_version(
        self,
        template: str,
        version: str | None = None,
        description: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> PromptVersion:
        """
        Add a new version to the prompt.

        Args:
            template: The prompt template string
            version: Version string (auto-increments if not provided)
            description: Description of changes
            metadata: Additional metadata

        Returns:
            The new PromptVersion
        """
        # Auto-generate version if not provided
        if not version:
            version = self._increment_version()

        new_version = PromptVersion(
            version=version,
            template=template,
            description=description,
            metadata=metadata or {},
        )

        # Add to front of list (newest first)
        self.versions.insert(0, new_version)
        return new_version

    def _increment_version(self) -> str:
        """Auto-increment version number."""
        if not self.versions:
            return "1.0.0"

        latest = self.versions[0].version
        parts = latest.split(".")
        if len(parts) >= 3:
            # Increment patch version
            parts[2] = str(int(parts[2]) + 1)
            return ".".join(parts)
        return "1.0.0"

    def render(
        self,
        version: str | None = None,
        **kwargs,
    ) -> str:
        """
        Render a prompt version with variables.

        Args:
            version: Version to render (latest if not specified)
            **kwargs: Variable values

        Returns:
            Rendered prompt string
        """
        if version:
            prompt_version = self.get_version(version)
            if not prompt_version:
                raise ValueError(f"Version {version} not found")
        else:
            prompt_version = self.latest
            if not prompt_version:
                raise ValueError("No versions available")

        return prompt_version.render(**kwargs)

    def list_versions(self) -> list[str]:
        """List all available versions."""
        return [v.version for v in self.versions]

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "versions": [v.to_dict() for v in self.versions],
            "tags": self.tags,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PromptTemplate":
        """Create from dictionary."""
        versions = [PromptVersion.from_dict(v) for v in data.get("versions", [])]
        return cls(
            name=data["name"],
            description=data.get("description"),
            versions=versions,
            tags=data.get("tags", []),
            metadata=data.get("metadata", {}),
        )


class PromptRegistry:
    """
    Registry for managing prompt templates.

    Provides centralized storage and retrieval of prompts with version control.

    Example:
        >>> registry = PromptRegistry()
        >>> registry.register(
        ...     name="greeting",
        ...     template="Hello {name}, welcome to {service}!",
        ...     version="1.0.0",
        ... )
        >>> prompt = registry.get("greeting")
        >>> rendered = prompt.render(name="Alice", service="Aigie")
        >>> print(rendered)
        Hello Alice, welcome to Aigie!
    """

    def __init__(self):
        self._prompts: dict[str, PromptTemplate] = {}
        self._aliases: dict[str, str] = {}  # alias -> prompt name

    def register(
        self,
        name: str,
        template: str,
        version: str = "1.0.0",
        description: str | None = None,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> PromptTemplate:
        """
        Register a new prompt or add a version to existing prompt.

        Args:
            name: Unique name for the prompt
            template: The prompt template string
            version: Version string (default: "1.0.0")
            description: Description of the prompt/changes
            tags: Tags for categorization
            metadata: Additional metadata

        Returns:
            The PromptTemplate
        """
        if name in self._prompts:
            # Add new version to existing prompt
            prompt = self._prompts[name]
            prompt.add_version(
                template=template,
                version=version,
                description=description,
                metadata=metadata,
            )
        else:
            # Create new prompt template
            prompt_version = PromptVersion(
                version=version,
                template=template,
                description=description,
                metadata=metadata or {},
            )
            prompt = PromptTemplate(
                name=name,
                description=description,
                versions=[prompt_version],
                tags=tags or [],
                metadata=metadata or {},
            )
            self._prompts[name] = prompt

        return prompt

    def get(
        self,
        name: str,
        version: str | None = None,
    ) -> PromptTemplate | None:
        """
        Get a prompt template by name.

        Args:
            name: Prompt name or alias
            version: Specific version (returns template with all versions)

        Returns:
            PromptTemplate or None if not found
        """
        # Check aliases
        if name in self._aliases:
            name = self._aliases[name]

        return self._prompts.get(name)

    def render(
        self,
        name: str,
        version: str | None = None,
        **kwargs,
    ) -> str:
        """
        Render a prompt with variables.

        Args:
            name: Prompt name
            version: Version to render (latest if not specified)
            **kwargs: Variable values

        Returns:
            Rendered prompt string

        Raises:
            ValueError: If prompt not found
        """
        prompt = self.get(name)
        if not prompt:
            raise ValueError(f"Prompt '{name}' not found")
        return prompt.render(version=version, **kwargs)

    def list(self, tag: str | None = None) -> list[str]:
        """
        List all registered prompt names.

        Args:
            tag: Optional tag to filter by

        Returns:
            List of prompt names
        """
        if tag:
            return [name for name, prompt in self._prompts.items() if tag in prompt.tags]
        return list(self._prompts.keys())

    def list_versions(self, name: str) -> builtins.list[str]:
        """
        List all versions of a prompt.

        Args:
            name: Prompt name

        Returns:
            List of version strings
        """
        prompt = self.get(name)
        if not prompt:
            return []
        return prompt.list_versions()

    def alias(self, alias: str, name: str) -> None:
        """
        Create an alias for a prompt.

        Args:
            alias: Alias name
            name: Target prompt name
        """
        if name not in self._prompts:
            raise ValueError(f"Prompt '{name}' not found")
        self._aliases[alias] = name

    def delete(self, name: str) -> bool:
        """
        Delete a prompt.

        Args:
            name: Prompt name

        Returns:
            True if deleted, False if not found
        """
        if name in self._prompts:
            del self._prompts[name]
            # Remove any aliases pointing to this prompt
            self._aliases = {k: v for k, v in self._aliases.items() if v != name}
            return True
        return False

    def export(self) -> dict[str, Any]:
        """
        Export all prompts as a dictionary.

        Returns:
            Dictionary representation of all prompts
        """
        return {
            "prompts": {name: prompt.to_dict() for name, prompt in self._prompts.items()},
            "aliases": self._aliases,
        }

    def import_prompts(self, data: dict[str, Any]) -> int:
        """
        Import prompts from a dictionary.

        Args:
            data: Dictionary from export()

        Returns:
            Number of prompts imported
        """
        count = 0
        for name, prompt_data in data.get("prompts", {}).items():
            prompt = PromptTemplate.from_dict(prompt_data)
            self._prompts[name] = prompt
            count += 1

        self._aliases.update(data.get("aliases", {}))
        return count

    def save(self, path: str) -> None:
        """
        Save prompts to a JSON file.

        Args:
            path: File path
        """
        with open(path, "w") as f:
            json.dump(self.export(), f, indent=2, default=str)

    def load(self, path: str) -> int:
        """
        Load prompts from a JSON file.

        Args:
            path: File path

        Returns:
            Number of prompts loaded
        """
        with open(path) as f:
            data = json.load(f)
        return self.import_prompts(data)


# Global registry instance
_global_registry: PromptRegistry | None = None


def get_registry() -> PromptRegistry:
    """Get or create the global prompt registry."""
    global _global_registry
    if _global_registry is None:
        _global_registry = PromptRegistry()
    return _global_registry
