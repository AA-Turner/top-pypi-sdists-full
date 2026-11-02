"""Issue template system for rendering NormalizedIssue to issue.md.

Public API:
- render_issue: Pure rendering function (frontmatter + body)
- render_issue_md: Path-based wrapper (file I/O + type resolution + render)
- PropertyConfig: Exclusion configuration dataclass
- resolve_issue_type: 3-step type resolution
- slugify_type: Type slug normalization
- discover_templates: Preset-based template discovery
- select_template: Template selection with fallback
- validate_required_properties: Required property validation
- PresetLoadError: Raised when preset.yml is missing or cannot be parsed
- TemplateNotFoundError: Raised when template cannot be found
- TemplateValidationError: Raised when validation fails
"""

from __future__ import annotations

from agentic_devtools.cli.issue_template.discovery import (
    discover_templates,
    select_template,
)
from agentic_devtools.cli.issue_template.exceptions import (
    PresetLoadError,
    TemplateNotFoundError,
    TemplateValidationError,
)
from agentic_devtools.cli.issue_template.mapping_resolver import resolve_effective_mapping
from agentic_devtools.cli.issue_template.mapping_validation import (
    validate_issue_template_block,
    validate_property_section_mapping,
    validate_template_content,
)
from agentic_devtools.cli.issue_template.render_issue_md import render_issue_md
from agentic_devtools.cli.issue_template.renderer import PropertyConfig, render_issue
from agentic_devtools.cli.issue_template.type_resolver import (
    resolve_issue_type,
    slugify_type,
)
from agentic_devtools.cli.issue_template.validator import (
    validate_required_properties,
)

__all__ = [
    "PresetLoadError",
    "PropertyConfig",
    "TemplateNotFoundError",
    "TemplateValidationError",
    "discover_templates",
    "render_issue",
    "render_issue_md",
    "resolve_effective_mapping",
    "resolve_issue_type",
    "select_template",
    "slugify_type",
    "validate_issue_template_block",
    "validate_property_section_mapping",
    "validate_required_properties",
    "validate_template_content",
]
