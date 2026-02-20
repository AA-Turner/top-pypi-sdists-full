"""Jinja2 template rendering for AgentStage prompt templates.

This module provides a template renderer that uses Jinja2 to interpolate
variables into agent prompt templates. It supports the standard Jinja2
syntax including variables, conditionals, loops, and filters.

Example usage:
    renderer = JinjaTemplateRenderer()
    prompt = renderer.render(
        "Process task: {{ trigger_task.type }}",
        {"trigger_task": {"type": "approval", "payload": {...}}}
    )
"""

from typing import Any, Dict, Optional

from jinja2 import (
    BaseLoader,
    Environment,
    StrictUndefined,
    TemplateSyntaxError,
    UndefinedError,
)


class TemplateRenderError(Exception):
    """Raised when a template fails to render.

    Attributes:
        message: Human-readable description of the error.
        template_source: The original template string that failed.
        original_error: The underlying Jinja2 exception, if any.
    """

    def __init__(
        self,
        message: str,
        template_source: Optional[str] = None,
        original_error: Optional[Exception] = None,
    ):
        self.message = message
        self.template_source = template_source
        self.original_error = original_error
        super().__init__(message)

    def __str__(self) -> str:
        return self.message


class JinjaTemplateRenderer:
    """Renders Jinja2 templates with given context variables.

    This renderer is designed for AgentStage prompt templates where
    variables like `trigger_task` are interpolated into the prompt
    before sending to the AI agent.

    Args:
        strict: If True, raises TemplateRenderError for undefined variables.
            If False, undefined variables are replaced with empty strings.
            Default is False for lenient behavior.
        autoescape: If True, HTML-escapes variable values. Default is False
            since agent prompts typically don't need HTML escaping.
    """

    def __init__(self, strict: bool = False, autoescape: bool = False):
        self._strict = strict
        self._autoescape = autoescape
        self._env = self._create_environment()

    def _create_environment(self) -> Environment:
        """Create a Jinja2 environment with appropriate settings."""
        env = Environment(
            loader=BaseLoader(),
            autoescape=self._autoescape,
            undefined=StrictUndefined if self._strict else Environment().undefined,
            trim_blocks=False,
            lstrip_blocks=False,
        )
        return env

    def render(self, template_string: str, context: Dict[str, Any]) -> str:
        """Render a template string with the given context.

        Args:
            template_string: The Jinja2 template to render.
            context: Dictionary of variables available in the template.

        Returns:
            The rendered string with all variables interpolated.

        Raises:
            TemplateRenderError: If the template fails to render due to
                syntax errors or (in strict mode) undefined variables.
        """
        try:
            template = self._env.from_string(template_string)
            return template.render(**context)
        except TemplateSyntaxError as e:
            raise TemplateRenderError(
                message=f"Template syntax error at line {e.lineno}: {e.message}",
                template_source=template_string,
                original_error=e,
            )
        except UndefinedError as e:
            raise TemplateRenderError(
                message=f"Undefined variable in template: {str(e)}",
                template_source=template_string,
                original_error=e,
            )
        except Exception as e:
            raise TemplateRenderError(
                message=f"Failed to render template: {str(e)}",
                template_source=template_string,
                original_error=e,
            )

    def render_from_file(self, file_path: str, context: Dict[str, Any]) -> str:
        """Read a template from a file and render it.

        Args:
            file_path: Path to the .md template file.
            context: Dictionary of variables available in the template.

        Returns:
            The rendered string with all variables interpolated.

        Raises:
            TemplateRenderError: If the file cannot be read or template
                fails to render.
        """
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                template_string = f.read()
            return self.render(template_string, context)
        except FileNotFoundError:
            raise TemplateRenderError(
                message=f"Template file not found: {file_path}",
            )
        except IOError as e:
            raise TemplateRenderError(
                message=f"Failed to read template file: {file_path}",
                original_error=e,
            )
