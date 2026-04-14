import re
from pathlib import Path
from typing import List

import html5lib
from jinja2 import Environment
from jinja2.exceptions import TemplateSyntaxError

from abstra_internals.repositories.linter.models import LinterIssue, LinterRule
from abstra_internals.services.fs import FileSystemService
from abstra_internals.settings import Settings


class HtmlOrJinja2SyntaxErrorsFound(LinterIssue):
    def __init__(self, file_path: Path, errors: List[str]):
        bullets = "\n".join(f"  - {err}" for err in errors)
        self.label = f"Errors in {file_path}:\n{bullets}"
        self.fixes = []


# parse() expects a full document with <!DOCTYPE html>. Since user HTML files
# may be fragments or simply omit the doctype, we ignore these errors.
IGNORED_ERRORS = {
    "expected-doctype-but-got-start-tag",
    "expected-doctype-but-got-chars",
    "expected-doctype-but-got-eof",
}

# Matches Jinja2 expressions ({{ ... }}), statements ({% ... %}), and
# comments ({# ... #}). DOTALL so multi-line {% block %}...{% endblock %}
# inner content is matched when needed.
_JINJA2_TOKEN_RE = re.compile(r"\{\{.*?\}\}|\{%.*?%\}|\{#.*?#\}", re.DOTALL)


def _has_jinja2(content: str) -> bool:
    return "{{" in content or "{%" in content or "{#" in content


def _strip_jinja2(content: str) -> str:
    # Replace Jinja2 tokens with spaces while preserving newlines, so that
    # line/column numbers reported by html5lib still point at the user's
    # original file positions.
    def repl(match: "re.Match[str]") -> str:
        return re.sub(r"[^\n]", " ", match.group())

    return _JINJA2_TOKEN_RE.sub(repl, content)


def _display_path(file_path: Path, root: Path) -> Path:
    try:
        return file_path.relative_to(root)
    except ValueError:
        return file_path


class HtmlAndJinja2Syntax(LinterRule):
    label = "HTML and Jinja2 syntax errors"
    type = "bug"
    fix_with_ai = True

    def find_issues(self) -> List[LinterIssue]:
        issues: List[LinterIssue] = []
        root = Settings.root_path
        jinja_env = Environment()

        for html_file in FileSystemService.list_files(root, allowed_suffixes=[".html"]):
            try:
                content = html_file.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue

            file_errors: List[str] = []

            if _has_jinja2(content):
                try:
                    jinja_env.parse(content)
                except TemplateSyntaxError as e:
                    file_errors.append(f"Jinja2: {e.message} at line {e.lineno}")
                    # Skip HTML validation when Jinja2 is broken: errors from
                    # html5lib on the stripped content would be noise.
                    issues.append(
                        HtmlOrJinja2SyntaxErrorsFound(
                            _display_path(html_file, root), file_errors
                        )
                    )
                    continue
                content = _strip_jinja2(content)

            parser = html5lib.HTMLParser()
            parser.parse(content)

            for (line, col), error_code, details in parser.errors:
                if error_code in IGNORED_ERRORS:
                    continue
                msg = f"HTML: {error_code} at line {line}, col {col}"
                if details:
                    msg += f" ({', '.join(f'{k}={v}' for k, v in details.items())})"
                file_errors.append(msg)

            if file_errors:
                issues.append(
                    HtmlOrJinja2SyntaxErrorsFound(
                        _display_path(html_file, root), file_errors
                    )
                )

        return issues
