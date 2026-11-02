"""Commit template creation and validation for ``agdt-setup``.

Provides:
- ``ensure_commit_template(git_root)`` — creates the provider-aware default
  template if missing
- ``validate_commit_template(git_root)`` — checks an existing template for
  required variables (adapter-aware)

The default template differs by issue provider (``platform.issue_adapter`` in
``.github/agdt-config.json``).  The **title never uses a markdown link** for any
provider; only the Jira footer keeps a full markdown link, because GitHub
auto-links bare ``#NNN`` references while it does not auto-link Jira keys.
"""

from __future__ import annotations

from pathlib import Path

import jinja2
import jinja2.meta

from ...config import load_platform_config
from ..git.commit_template import REQUIRED_VARIABLES, TEMPLATE_PATH

# GitHub default: bare ``#NNN`` scope + bare ``#NNN`` footer (GitHub auto-links).
_TEMPLATE_GITHUB = """\
{{ issueType }}(#{{ issueKey }}): {{ commitMessageTitle }}

{{ commitMessageBody }}

#{{ issueKey }}
"""

# Jira default: bare key scope (key already carries ``PROJECT-``) + full markdown
# link footer to the Jira browse URL (GitHub does not auto-link Jira keys).
_TEMPLATE_JIRA = """\
{{ issueType }}({{ issueKey }}): {{ commitMessageTitle }}

{{ commitMessageBody }}

[{{ issueKey }}]({{ issueLink }})
"""

# Markdown (provider-agnostic) default: bare key scope + plain-text key footer.
_TEMPLATE_MARKDOWN = """\
{{ issueType }}({{ issueKey }}): {{ commitMessageTitle }}

{{ commitMessageBody }}

{{ issueKey }}
"""


def _default_template_for(adapter: str) -> str:
    """Return the default commit template content for an issue adapter.

    ``jira`` and ``markdown`` map to their dedicated templates; every other
    value (including ``github`` and any unexpected adapter) falls back to the
    GitHub template, which is the safe default for the ``#NNN`` convention.
    """
    if adapter == "jira":
        return _TEMPLATE_JIRA
    if adapter == "markdown":
        return _TEMPLATE_MARKDOWN
    return _TEMPLATE_GITHUB


def ensure_commit_template(git_root: Path) -> bool:
    """Create the provider-aware default commit template if it does not exist.

    The adapter is resolved from ``platform.issue_adapter`` in the target repo's
    ``.github/agdt-config.json`` (via :func:`load_platform_config`).  Running
    ``agdt-setup --reconfigure`` rewrites the template to match the current
    adapter (the reconfigure path deletes the file first, so this re-creates it).

    Args:
        git_root: Repository root path.

    Returns:
        ``True`` if the template was created, ``False`` if it already existed.
    """
    template_file = git_root / TEMPLATE_PATH
    if template_file.is_file():
        return False

    adapter = str(load_platform_config(str(git_root))["issue_adapter"])
    template_content = _default_template_for(adapter)

    # Create directory structure (FR-008)
    template_file.parent.mkdir(parents=True, exist_ok=True)
    template_file.write_text(template_content, encoding="utf-8")
    return True


def validate_commit_template(git_root: Path) -> list[str]:
    """Validate an existing commit template for required variables.

    Uses Jinja2 AST parsing to extract referenced variables and checks that all
    required variables are present.  Validation is **adapter-aware**: the Jira
    adapter additionally requires ``{{ issueLink }}`` (its footer links to the
    Jira browse URL), while GitHub/markdown templates legitimately omit it and
    therefore are not warned about its absence.

    Args:
        git_root: Repository root path.

    Returns:
        List of warning messages (empty if template is valid). Each entry
        describes a missing required variable.
    """
    template_file = git_root / TEMPLATE_PATH
    if not template_file.is_file():
        return []

    try:
        content = template_file.read_text(encoding="utf-8")
    except OSError as exc:
        return [f"Cannot read commit template: {exc}"]

    if not content.strip():
        return ["Commit template file is empty or whitespace-only"]

    try:
        # autoescape=True is a no-op for validation (parse() never renders output)
        # but keeps the environment safe if it is ever reused for rendering later.
        env = jinja2.Environment(loader=jinja2.BaseLoader(), autoescape=True)
        ast = env.parse(content)
        referenced = jinja2.meta.find_undeclared_variables(ast)
    except jinja2.TemplateSyntaxError as exc:
        return [f"Commit template has Jinja2 syntax error: {exc}"]

    required = set(REQUIRED_VARIABLES)
    adapter = str(load_platform_config(str(git_root))["issue_adapter"])
    if adapter == "jira":
        required.add("issueLink")

    missing = required - referenced
    warnings_list: list[str] = []
    for var in sorted(missing):
        warnings_list.append(
            f"Commit template does not reference required variable '{{{{ {var} }}}}' — "
            f"add it to the template so it appears in generated commit messages"
        )

    return warnings_list
