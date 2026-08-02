from __future__ import annotations

import json
import logging
import threading
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Mapping, Optional, Sequence, Tuple

from python_agent.common.constants import CONSOLE_MESSAGE_PREFIX

_PLACEHOLDER_PATTERN = re.compile(r"{{\s*([a-zA-Z_][a-zA-Z0-9_]*)\s*}}")

log = logging.getLogger(__name__)

class ConsoleMessageTemplateError(RuntimeError):
    """Base exception for console message template issues."""


class ConsoleMessageTemplateNotFound(ConsoleMessageTemplateError):
    """Raised when a requested template is missing."""


class ConsoleMessageTemplateRenderError(ConsoleMessageTemplateError):
    """Raised when rendering a template fails."""

    def __init__(
        self, message: str, missing_placeholders: Optional[Sequence[str]] = None
    ) -> None:
        super().__init__(message)
        self.missing_placeholders: Tuple[str, ...] = tuple(
            missing_placeholders or ()
        )


@dataclass(frozen=True)
class _TemplateRecord:
    elements: Tuple[str, ...]
    text: str
    metadata: Dict[str, Any]
    placeholders: Tuple[str, ...]


class ConsoleMessageTemplates:
    """Singleton responsible for loading and rendering console message templates."""

    _instance: "ConsoleMessageTemplates" = None  # type: ignore[assignment]
    _lock = threading.Lock()
    _disabled = os.environ.get("CONSOLE_MESSAGE_TEMPLATES_DISABLED", "false").lower() == "true"
    _quiet = False
    
    def __init__(self) -> None:
        if getattr(self, "_initialized", False):
            return

        self._templates: Dict[str, _TemplateRecord] = {}
        self._load_templates()
        self._initialized = True

    @classmethod
    def instance(cls) -> "ConsoleMessageTemplates":
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = cls()
        return cls._instance

    @classmethod
    def render(cls, template_type: str, **kwargs: Any) -> str:
        return cls.instance()._render(template_type, **kwargs)

    @classmethod
    def set_quiet(cls, quiet: bool) -> None:
        """Set the quiet mode flag to suppress console messages."""
        cls._quiet = quiet
    
    @classmethod
    def is_quiet(cls) -> bool:
        """Check if quiet mode is enabled."""
        return cls._quiet
    
    @classmethod
    def render_and_print(cls, template_type: str, **kwargs: Any) -> None:
        try:
            if cls._disabled or cls._quiet:
                return
            elements = cls.instance()._render_to_elements(template_type, kwargs)
            for element in elements:
                print(f"[{CONSOLE_MESSAGE_PREFIX}] {element}")
        except ConsoleMessageTemplateNotFound:
            log.debug(
                "console message type {0} not found".format(template_type)
            )
        except ConsoleMessageTemplateRenderError as exc:
            if exc.missing_placeholders:
                placeholders = ", ".join(exc.missing_placeholders)
                log.debug(
                    "failed to render message {0}. template value for {1} are missing".format(
                        template_type, placeholders
                    )
                )  
        except Exception as exc:
            log.debug(
                "failed to render message {0}: {1}".format(template_type, exc)
            )
        

    def get_metadata(self, template_type: str) -> Dict[str, Any]:
        record = self._templates.get(template_type)
        if record is None:
            raise ConsoleMessageTemplateNotFound(
                "Console message template '{0}' was not found.".format(template_type)
            )
        return dict(record.metadata)

    def _render(self, template_type: str, **kwargs: Any) -> str:
        elements = self._render_to_elements(template_type, kwargs)
        return "\n".join(elements)

    def _render_to_elements(
        self, template_type: str, arguments: Mapping[str, Any]
    ) -> Tuple[str, ...]:
        record = self._templates.get(template_type)
        if record is None:
            raise ConsoleMessageTemplateNotFound(
                "Console message template '{0}' was not found.".format(template_type)
            )

        context = self._normalize_arguments(arguments)

        missing_placeholders = [
            placeholder
            for placeholder in record.placeholders
            if placeholder not in context
        ]
        if missing_placeholders:
            missing_as_text = ", ".join(missing_placeholders)
            raise ConsoleMessageTemplateRenderError(
                "Missing argument while rendering console message template '{0}': {1}".format(
                    template_type, missing_as_text
                ),
                missing_placeholders=missing_placeholders,
            )

        rendered_elements = tuple(
            self._render_element(element, context) for element in record.elements
        )
        return rendered_elements

    def _load_templates(self) -> None:
        base_dir = self._templates_directory()
        if not base_dir.exists():
            raise ConsoleMessageTemplateError(
                "Console messages directory '{0}' does not exist.".format(base_dir)
            )

        for file_path in sorted(base_dir.rglob("*.json")):
            namespace = ".".join(
                file_path.relative_to(base_dir).with_suffix("").parts
            )
            self._load_template_file(namespace, file_path)

    def _load_template_file(self, namespace: str, file_path: Path) -> None:
        try:
            with file_path.open("r", encoding="utf-8") as handle:
                payload = json.load(handle)
        except json.JSONDecodeError as exc:
            raise ConsoleMessageTemplateError(
                "Failed parsing console message template file '{0}': {1}".format(
                    file_path, exc
                )
            ) from exc

        if not isinstance(payload, dict):
            raise ConsoleMessageTemplateError(
                "Console message template file '{0}' must contain a JSON object.".format(
                    file_path
                )
            )

        for name, definition in payload.items():
            if not isinstance(definition, dict):
                # Allow ancillary metadata entries (e.g., package.json values).
                continue
            template_elements = self._extract_template_elements(
                namespace, name, definition
            )
            template_text = "\n".join(template_elements)
            metadata = {
                key: value
                for key, value in definition.items()
                if key != "template"
            }

            full_key = "{0}.{1}".format(namespace, name)
            if full_key in self._templates:
                raise ConsoleMessageTemplateError(
                    "Duplicate console message template key '{0}' detected.".format(
                        full_key
                    )
                )

            self._templates[full_key] = _TemplateRecord(
                elements=template_elements,
                text=template_text,
                metadata=metadata,
                placeholders=self._collect_placeholders(template_elements),
            )

    def _extract_template_elements(
        self, namespace: str, name: str, definition: Dict[str, Any]
    ) -> Tuple[str, ...]:
        if "template" not in definition:
            raise ConsoleMessageTemplateError(
                "Template '{0}.{1}' is missing the 'template' field.".format(
                    namespace, name
                )
            )

        template_value = definition["template"]
        if isinstance(template_value, str):
            return (template_value,)
        if isinstance(template_value, list):
            return tuple(str(line) for line in template_value)

        raise ConsoleMessageTemplateError(
            "Template '{0}.{1}' must define 'template' as string or list of strings.".format(
                namespace, name
            )
        )

    def _normalize_arguments(self, arguments: Mapping[str, Any]) -> Dict[str, Any]:
        context: Dict[str, Any] = dict(arguments)
        for key, value in arguments.items():
            if self._is_snake_case(key):
                camel_key = self._to_camel_case(key)
                if camel_key not in context:
                    context[camel_key] = value
        return context

    def _render_element(self, element: str, context: Mapping[str, Any]) -> str:
        def replace(match: re.Match) -> str:
            key = match.group(1)
            return self._stringify_value(context[key])

        return _PLACEHOLDER_PATTERN.sub(replace, element)

    def _collect_placeholders(self, elements: Sequence[str]) -> Tuple[str, ...]:
        ordered: Dict[str, None] = {}
        for element in elements:
            for placeholder in _PLACEHOLDER_PATTERN.findall(element):
                if placeholder not in ordered:
                    ordered[placeholder] = None
        return tuple(ordered.keys())

    def _stringify_value(self, value: Any) -> str:
        if isinstance(value, str):
            return value
        return str(value)

    def _is_snake_case(self, key: str) -> bool:
        return "_" in key and key.lower() == key

    def _to_camel_case(self, key: str) -> str:
        parts = key.split("_")
        if not parts:
            return key
        first = parts[0]
        rest = [
            part[:1].upper() + part[1:] if part else ""
            for part in parts[1:]
        ]
        return first + "".join(rest)

    def _templates_directory(self) -> Path:
        base_dir = Path(__file__).resolve().parents[2] / "console_messages"
        return base_dir


console_message_templates = ConsoleMessageTemplates.instance()

__all__ = [
    "ConsoleMessageTemplateError",
    "ConsoleMessageTemplateNotFound",
    "ConsoleMessageTemplateRenderError",
    "ConsoleMessageTemplates",
    "console_message_templates",
]

